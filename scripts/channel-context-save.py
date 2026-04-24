#!/usr/bin/env python3
"""
channel-context-save.py — Discover and save context from all Discord channels,
Telegram chats, and workspaces. Outputs structured JSON for the agent to synthesize.

Usage: python3 channel-context-save.py [--discover-only] [--since ISO_TIMESTAMP]
"""

import json
import sys
import os
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

WORKSPACE = Path("/Users/mrwolff/.openclaw/workspace")
STATE_FILE = WORKSPACE / "memory" / "channel-save-state.json"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
SESSIONS_FILE = Path.home() / ".openclaw" / "agents" / "main" / "sessions" / "sessions.json"

# ── Helpers ─────────────────────────────────────────────────────

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def discord_api(endpoint, token):
    """Call Discord REST API via curl (Python 3.9 urllib has TLS issues with Discord)."""
    url = f"https://discord.com/api/v10{endpoint}"
    try:
        result = subprocess.run(
            ["curl", "-s", url, "-H", f"Authorization: Bot {token}"],
            capture_output=True, text=True, timeout=15
        )
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        return {"error": str(e)}

def telegram_api(endpoint, token, params=None):
    """Call Telegram Bot API via curl."""
    url = f"https://api.telegram.org/bot{token}/{endpoint}"
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    try:
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True, text=True, timeout=15
        )
        data = json.loads(result.stdout)
        return data.get("result", data)
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        return {"error": str(e)}

def iso_to_snowflake(iso_str):
    """Convert ISO timestamp to Discord snowflake for message filtering."""
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    ms = int(dt.timestamp() * 1000)
    return (ms - 1420070400000) << 22

# ── Discovery ───────────────────────────────────────────────────

def discover_discord(config):
    """Discover all Discord guilds and channels across all bot accounts."""
    discord_cfg = config.get("channels", {}).get("discord", {})
    accounts = discord_cfg.get("accounts", {})
    
    results = []
    seen_channels = set()
    
    for account_name, account_cfg in accounts.items():
        token = account_cfg.get("token")
        if not token or not account_cfg.get("enabled", True):
            continue
        
        guilds = discord_api("/users/@me/guilds", token)
        if isinstance(guilds, dict) and "error" in guilds:
            print(f"  WARN: {account_name} bot guild fetch failed: {guilds['error']}", file=sys.stderr)
            continue
        
        for guild in guilds:
            guild_id = guild["id"]
            guild_name = guild["name"]
            
            channels = discord_api(f"/guilds/{guild_id}/channels", token)
            if isinstance(channels, dict) and "error" in channels:
                print(f"  WARN: {account_name} channel fetch for {guild_name} failed", file=sys.stderr)
                continue
            
            for ch in channels:
                if ch["type"] not in (0, 5):  # text and announcement only
                    continue
                if ch["id"] in seen_channels:
                    continue
                seen_channels.add(ch["id"])
                
                results.append({
                    "source": "discord",
                    "account": account_name,
                    "guild_id": guild_id,
                    "guild_name": guild_name,
                    "channel_id": ch["id"],
                    "channel_name": ch["name"],
                    "token": token
                })
    
    return results

def discover_telegram(config):
    """Discover Telegram chats from OpenClaw sessions."""
    results = []
    
    # Get known Telegram sessions
    sessions = load_json(SESSIONS_FILE)
    tg_cfg = config.get("channels", {}).get("telegram", {})
    accounts = tg_cfg.get("accounts", {})
    
    seen_chats = set()
    
    for session_key in sessions:
        if "telegram" not in session_key:
            continue
        # Parse: agent:main:telegram:direct:CHAT_ID or agent:main:telegram:slash:CHAT_ID
        parts = session_key.split(":")
        if len(parts) >= 5:
            chat_id = parts[-1]
            chat_type = parts[-2]  # direct, slash, group, etc.
            if chat_id not in seen_chats:
                seen_chats.add(chat_id)
                results.append({
                    "source": "telegram",
                    "chat_id": chat_id,
                    "chat_type": chat_type,
                    "session_key": session_key
                })
    
    # Also check recent updates from each bot for new chats
    for account_name, account_cfg in accounts.items():
        token = account_cfg.get("botToken")
        if not token or not account_cfg.get("enabled", True):
            continue
        
        updates = telegram_api("getUpdates", token, {"limit": "100"})
        if isinstance(updates, list):
            for update in updates:
                msg = update.get("message", update.get("channel_post", {}))
                if msg and "chat" in msg:
                    chat = msg["chat"]
                    cid = str(chat["id"])
                    if cid not in seen_chats:
                        seen_chats.add(cid)
                        results.append({
                            "source": "telegram",
                            "account": account_name,
                            "chat_id": cid,
                            "chat_type": chat.get("type", "unknown"),
                            "chat_name": chat.get("title", chat.get("first_name", "DM")),
                            "session_key": f"agent:main:telegram:direct:{cid}"
                        })
    
    return results

def discover_workspaces():
    """Discover all OpenClaw workspaces."""
    results = []
    
    # Known workspace locations
    workspace_dirs = [
        Path.home() / ".openclaw" / "workspace",
        Path.home() / ".openclaw" / "workspace-deb",
        Path.home() / ".openclaw" / "workspace-stan",
        Path.home() / ".openclaw" / "workspace-smuggs",
        Path.home() / "bubba-workspace",
        Path.home() / ".claude",
    ]
    
    # Also scan for any new workspace-* dirs
    openclaw_dir = Path.home() / ".openclaw"
    if openclaw_dir.exists():
        for d in openclaw_dir.iterdir():
            if d.is_dir() and d.name.startswith("workspace") and d not in workspace_dirs:
                workspace_dirs.append(d)
    
    for ws in workspace_dirs:
        if not ws.exists():
            continue
        
        has_git = (ws / ".git").exists()
        has_remote = False
        remote_url = None
        branch = "main"
        
        if has_git:
            try:
                result = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    cwd=ws, capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    has_remote = True
                    remote_url = result.stdout.strip()
            except Exception:
                pass
            
            try:
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=ws, capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0 and result.stdout.strip():
                    branch = result.stdout.strip()
            except Exception:
                pass
        
        # Check for recent changes
        recent_files = []
        if has_git:
            try:
                result = subprocess.run(
                    ["git", "diff", "--name-only", "HEAD"],
                    cwd=ws, capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    recent_files = [f for f in result.stdout.strip().split("\n") if f]
            except Exception:
                pass
            
            # Also untracked files
            try:
                result = subprocess.run(
                    ["git", "ls-files", "--others", "--exclude-standard"],
                    cwd=ws, capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    recent_files += [f for f in result.stdout.strip().split("\n") if f]
            except Exception:
                pass
        
        results.append({
            "source": "workspace",
            "path": str(ws),
            "name": ws.name,
            "has_git": has_git,
            "has_remote": has_remote,
            "remote_url": remote_url,
            "branch": branch,
            "pending_changes": len(recent_files),
            "changed_files": recent_files[:20]  # cap at 20
        })
    
    return results

# ── Fetch messages ──────────────────────────────────────────────

def fetch_discord_messages(channel, since_snowflake, limit=100):
    """Fetch messages from a Discord channel since a snowflake."""
    token = channel["token"]
    cid = channel["channel_id"]
    
    messages = discord_api(
        f"/channels/{cid}/messages?limit={limit}&after={since_snowflake}",
        token
    )
    
    if isinstance(messages, dict) and "error" in messages:
        return []
    
    if not isinstance(messages, list):
        return []
    
    # Filter and simplify
    result = []
    for msg in messages:
        # Skip empty bot messages unless they have embeds
        content = msg.get("content", "")
        embeds = msg.get("embeds", [])
        if not content and not embeds:
            continue
        
        author = msg.get("author", {})
        result.append({
            "id": msg["id"],
            "author": author.get("username", "unknown"),
            "is_bot": author.get("bot", False),
            "content": content[:500],  # truncate long messages
            "timestamp": msg.get("timestamp", ""),
            "has_embeds": len(embeds) > 0
        })
    
    return sorted(result, key=lambda m: m["id"])

# ── Main ────────────────────────────────────────────────────────

def main():
    discover_only = "--discover-only" in sys.argv
    
    # Load config
    config = load_json(OPENCLAW_CONFIG)
    state = load_json(STATE_FILE)
    
    # Determine since timestamp
    since_arg = None
    for i, arg in enumerate(sys.argv):
        if arg == "--since" and i + 1 < len(sys.argv):
            since_arg = sys.argv[i + 1]
    
    last_save = since_arg or state.get("lastSaveAt")
    if not last_save:
        last_save = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
    
    since_snowflake = iso_to_snowflake(last_save)
    
    print(json.dumps({"phase": "discovery", "since": last_save}))
    
    # Discover everything
    discord_channels = discover_discord(config)
    telegram_chats = discover_telegram(config)
    workspaces = discover_workspaces()
    
    inventory = {
        "phase": "inventory",
        "discord": {
            "channels": len(discord_channels),
            "guilds": list(set(f"{c['guild_name']} ({c['account']})" for c in discord_channels)),
            "details": [
                {
                    "guild": c["guild_name"],
                    "channel": f"#{c['channel_name']}",
                    "id": c["channel_id"],
                    "account": c["account"]
                }
                for c in discord_channels
            ]
        },
        "telegram": {
            "chats": len(telegram_chats),
            "details": [
                {
                    "chat_id": t["chat_id"],
                    "type": t["chat_type"],
                    "name": t.get("chat_name", "")
                }
                for t in telegram_chats
            ]
        },
        "workspaces": {
            "count": len(workspaces),
            "details": [
                {
                    "name": w["name"],
                    "path": w["path"],
                    "has_remote": w["has_remote"],
                    "pending_changes": w["pending_changes"]
                }
                for w in workspaces
            ]
        }
    }
    print(json.dumps(inventory))
    
    # Compare with previous inventory for new discoveries
    prev_channels = set(state.get("knownChannels", []))
    prev_chats = set(state.get("knownTelegramChats", []))
    prev_workspaces = set(state.get("knownWorkspaces", []))
    
    current_channels = set(c["channel_id"] for c in discord_channels)
    current_chats = set(t["chat_id"] for t in telegram_chats)
    current_workspaces = set(w["path"] for w in workspaces)
    
    new_channels = current_channels - prev_channels
    new_chats = current_chats - prev_chats
    new_workspaces = current_workspaces - prev_workspaces
    
    if new_channels or new_chats or new_workspaces:
        discoveries = {"phase": "new_discoveries"}
        if new_channels:
            discoveries["new_discord_channels"] = [
                f"#{c['channel_name']} in {c['guild_name']}"
                for c in discord_channels if c["channel_id"] in new_channels
            ]
        if new_chats:
            discoveries["new_telegram_chats"] = list(new_chats)
        if new_workspaces:
            discoveries["new_workspaces"] = list(new_workspaces)
        print(json.dumps(discoveries))
    
    if discover_only:
        print(json.dumps({"phase": "done", "mode": "discover-only"}))
        return
    
    # Fetch messages from all Discord channels
    channels_with_messages = []
    
    for channel in discord_channels:
        messages = fetch_discord_messages(channel, since_snowflake)
        if messages:
            channels_with_messages.append({
                "guild": channel["guild_name"],
                "channel": f"#{channel['channel_name']}",
                "channel_id": channel["channel_id"],
                "account": channel["account"],
                "message_count": len(messages),
                "messages": messages
            })
    
    print(json.dumps({
        "phase": "messages",
        "channels_with_activity": len(channels_with_messages),
        "total_messages": sum(c["message_count"] for c in channels_with_messages),
        "channels": channels_with_messages
    }))
    
    # Update state with full inventory
    new_state = {
        "lastSaveAt": datetime.now(timezone.utc).isoformat(),
        "previousSaveAt": last_save,
        "knownChannels": list(current_channels),
        "knownTelegramChats": list(current_chats),
        "knownWorkspaces": list(current_workspaces),
        "channelsSaved": [c["channel"] for c in channels_with_messages],
        "totalMessages": sum(c["message_count"] for c in channels_with_messages)
    }
    save_json(STATE_FILE, new_state)
    
    print(json.dumps({"phase": "done", "state_saved": True}))

if __name__ == "__main__":
    main()

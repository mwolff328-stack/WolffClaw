#!/usr/bin/env bash
# spawn-claude-dev.sh — Daily Claude Code session init for SurvivorPulse #dev
# Posts announcement to #dev and spawns ACP session via OpenClaw API

set -euo pipefail

DEV_CHANNEL="1495450229816823998"
GATEWAY_URL="http://127.0.0.1:18789"
OC_CONFIG="$HOME/.openclaw/openclaw.json"

# Get Discord bot token
BOT_TOKEN=$(python3 -c "import json; print(json.load(open('$OC_CONFIG'))['channels']['discord']['accounts']['default']['token'])")
# Get OpenClaw gateway token
GW_TOKEN=$(python3 -c "import json; print(json.load(open('$OC_CONFIG'))['gateway']['auth']['token'])")

DATE=$(date '+%A, %B %-d')

echo "[spawn-claude-dev] Starting — $DATE"

# 1. Post announcement to #dev
MSG=$(python3 -c "import json; print(json.dumps({'content': '☀️ **Claude Code session initializing for $DATE.** Starting up — ready in a moment.'}))")
curl -sf -X POST "https://discord.com/api/v10/channels/$DEV_CHANNEL/messages" \
  -H "Authorization: Bot $BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$MSG" > /dev/null
echo "[spawn-claude-dev] Posted announcement to #dev"

# 2. Spawn Claude ACP session via OpenClaw API bound to #dev thread
SPAWN_PAYLOAD=$(python3 -c "
import json
print(json.dumps({
  'runtime': 'acp',
  'agentId': 'claude',
  'mode': 'session',
  'thread': True,
  'label': 'SurvivorPulse Dev — $DATE',
  'task': 'Good morning! Daily Claude Code session initialized for SurvivorPulse dev work. Ready to work.'
}))
")

SESSION_RESULT=$(curl -sf -X POST "$GATEWAY_URL/api/sessions/spawn" \
  -H "Authorization: Bearer $GW_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$SPAWN_PAYLOAD" 2>&1 || echo '{"error":"spawn failed"}')

SESSION_KEY=$(echo "$SESSION_RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('sessionKey', d.get('error', 'unknown')))" 2>/dev/null || echo "unknown")

echo "[spawn-claude-dev] Session spawned: $SESSION_KEY"

# 3. Post follow-up to #dev with session info
FOLLOW_MSG=$(python3 -c "import json; print(json.dumps({'content': '✅ Claude Code session live. Session: \`$SESSION_KEY\`'}))")
curl -sf -X POST "https://discord.com/api/v10/channels/$DEV_CHANNEL/messages" \
  -H "Authorization: Bot $BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$FOLLOW_MSG" > /dev/null
echo "[spawn-claude-dev] Done"

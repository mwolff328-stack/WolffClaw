# WolffClaw

Luigi's workspace — SurvivorPulse agent infrastructure, scripts, and tooling.

## Setup

After cloning, run the hook installer to enable local secret scanning:

```bash
bash scripts/install-hooks.sh
```

This installs a pre-commit hook that blocks commits containing API keys, tokens, and credentials (Notion, OpenAI, Anthropic, AWS, GitHub, Stripe, etc.) before they reach GitHub.

To update hooks after pulling changes:

```bash
bash scripts/install-hooks.sh
```

> **Bypass (false positives only):** `git commit --no-verify`

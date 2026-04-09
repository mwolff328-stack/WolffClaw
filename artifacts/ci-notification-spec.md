# CI Notification Design Spec — SurvivorPulse

**Date:** 2026-04-09
**Scope:** GitHub Actions notification steps for Telegram and Discord after every push to main (pass or fail), with failing stage name included on failure.

---

## 1. Overview

Every push to `main` that runs CI should deliver a notification to both Telegram and Discord:
- **On success:** Green confirmation with commit SHA, branch, workflow name, and link to the run.
- **On failure:** Red alert with commit SHA, branch, workflow name, **name of the stage that failed**, and link to the run.

The spec uses a "track current stage" pattern: each test step writes its stage name to `$GITHUB_ENV` before executing. If the job fails, the notification step reads `FAILED_STAGE` to identify which stage broke.

---

## 2. GitHub Secrets Required

Add these four secrets to the SurvivorPulse GitHub repo (`Settings → Secrets and variables → Actions`):

| Secret name | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather (format: `123456:ABC-DEF...`) |
| `TELEGRAM_CHAT_ID` | Chat or channel ID where notifications should post (e.g., `-1001234567890` for a channel, personal chat ID for DMs) |
| `DISCORD_WEBHOOK_URL` | Full Discord webhook URL (format: `https://discord.com/api/webhooks/...`) |
| `SLACK_WEBHOOK_URL` | *(Optional — not in scope but reserve the name if Slack is added later)* |

**Getting `TELEGRAM_CHAT_ID`:** Start a conversation with your bot or add it to a channel, then call `https://api.telegram.org/bot<TOKEN>/getUpdates` to retrieve the `chat.id`.

---

## 3. Failure Stage Tracking Pattern

Insert one line at the start of each test stage step, **before** the actual command:

```yaml
- name: 'Stage 1: Unit tests'
  run: |
    echo "FAILED_STAGE=Stage 1: Unit tests" >> $GITHUB_ENV
    set -o pipefail
    npm run test:unit 2>&1 | tee /tmp/unit.log
```

If this step fails, `FAILED_STAGE` is already set in the environment. Subsequent steps that succeed will overwrite it — so by the time the job ends, `FAILED_STAGE` holds the name of the last step that *attempted to run*. On failure, that is the failing stage. On success, the notification step checks `job.status` and ignores `FAILED_STAGE`.

Add this to every named test stage. Infrastructure steps (checkout, npm ci, DB setup) can also be tracked if desired, but the test stages are the most actionable.

---

## 4. Notification Steps YAML

### 4a. Telegram Notification Step

```yaml
- name: Notify Telegram
  if: always()
  env:
    JOB_STATUS: ${{ job.status }}
    COMMIT_SHA: ${{ github.sha }}
    BRANCH: ${{ github.ref_name }}
    WORKFLOW: ${{ github.workflow }}
    RUN_ID: ${{ github.run_id }}
    REPO: ${{ github.repository }}
    SERVER_URL: ${{ github.server_url }}
    TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
    TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
  run: |
    SHORT_SHA="${COMMIT_SHA:0:7}"
    RUN_URL="${SERVER_URL}/${REPO}/actions/runs/${RUN_ID}"

    if [ "$JOB_STATUS" = "success" ]; then
      ICON="✅"
      STATUS_TEXT="Passed"
      BODY="${ICON} *CI ${STATUS_TEXT}* — ${WORKFLOW}"$'\n'"🔀 Branch: \`${BRANCH}\`"$'\n'"📝 Commit: \`${SHORT_SHA}\`"$'\n'"🔗 [View Run](${RUN_URL})"
    else
      ICON="❌"
      STATUS_TEXT="Failed"
      STAGE="${FAILED_STAGE:-Unknown stage}"
      BODY="${ICON} *CI ${STATUS_TEXT}* — ${WORKFLOW}"$'\n'"💥 Failed at: \`${STAGE}\`"$'\n'"🔀 Branch: \`${BRANCH}\`"$'\n'"📝 Commit: \`${SHORT_SHA}\`"$'\n'"🔗 [View Run](${RUN_URL})"
    fi

    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
      --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
      --data-urlencode "text=${BODY}" \
      --data-urlencode "parse_mode=Markdown" \
      --data-urlencode "disable_web_page_preview=true" \
      -w "\nHTTP %{http_code}\n"
```

**Example success message:**
```
✅ CI Passed — Pre-Publish Gate
🔀 Branch: `main`
📝 Commit: `a1b2c3d`
🔗 View Run
```

**Example failure message:**
```
❌ CI Failed — Pre-Publish Gate
💥 Failed at: `Stage 2c: HTTP integration tests (auth endpoints)`
🔀 Branch: `main`
📝 Commit: `a1b2c3d`
🔗 View Run
```

---

### 4b. Discord Notification Step (Embed format)

```yaml
- name: Notify Discord
  if: always()
  env:
    JOB_STATUS: ${{ job.status }}
    COMMIT_SHA: ${{ github.sha }}
    BRANCH: ${{ github.ref_name }}
    WORKFLOW: ${{ github.workflow }}
    RUN_ID: ${{ github.run_id }}
    REPO: ${{ github.repository }}
    SERVER_URL: ${{ github.server_url }}
    DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
  run: |
    SHORT_SHA="${COMMIT_SHA:0:7}"
    RUN_URL="${SERVER_URL}/${REPO}/actions/runs/${RUN_ID}"

    if [ "$JOB_STATUS" = "success" ]; then
      COLOR=3066993     # Green (#2ECC51)
      TITLE="✅ CI Passed — ${WORKFLOW}"
      FIELDS="[
        {\"name\": \"Branch\", \"value\": \"\`${BRANCH}\`\", \"inline\": true},
        {\"name\": \"Commit\", \"value\": \"[${SHORT_SHA}](${SERVER_URL}/${REPO}/commit/${COMMIT_SHA})\", \"inline\": true}
      ]"
    else
      COLOR=15158332    # Red (#E74C3C)
      STAGE="${FAILED_STAGE:-Unknown stage}"
      TITLE="❌ CI Failed — ${WORKFLOW}"
      FIELDS="[
        {\"name\": \"Failed Stage\", \"value\": \"\`${STAGE}\`\", \"inline\": false},
        {\"name\": \"Branch\", \"value\": \"\`${BRANCH}\`\", \"inline\": true},
        {\"name\": \"Commit\", \"value\": \"[${SHORT_SHA}](${SERVER_URL}/${REPO}/commit/${COMMIT_SHA})\", \"inline\": true}
      ]"
    fi

    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    PAYLOAD=$(jq -n \
      --arg title "$TITLE" \
      --argjson color "$COLOR" \
      --argjson fields "$FIELDS" \
      --arg url "$RUN_URL" \
      --arg ts "$TIMESTAMP" \
      '{
        embeds: [{
          title: $title,
          color: $color,
          fields: $fields,
          url: $url,
          footer: { text: "SurvivorPulse CI" },
          timestamp: $ts
        }]
      }')

    curl -s -X POST "${DISCORD_WEBHOOK_URL}" \
      -H "Content-Type: application/json" \
      -d "$PAYLOAD" \
      -w "\nHTTP %{http_code}\n"
```

**Notes on the Discord embed:**
- `color` is a decimal integer (not hex). Green = `3066993`, Red = `15158332`.
- The embed `url` makes the title clickable, linking directly to the Actions run.
- `jq` is available on `ubuntu-latest` by default.
- On failure, "Failed Stage" appears as the first field (not inline) so it stands out.

---

## 5. Full Drop-In Block (Both Channels Together)

This is the combined block to paste into either workflow. Place it as the **last two steps**, after the `Summary` step (or replace Summary if desired). Both use `if: always()`.

```yaml
      # ------------------------------------------------------------------
      # Notifications
      # ------------------------------------------------------------------
      - name: Notify Telegram
        if: always()
        env:
          JOB_STATUS: ${{ job.status }}
          COMMIT_SHA: ${{ github.sha }}
          BRANCH: ${{ github.ref_name }}
          WORKFLOW: ${{ github.workflow }}
          RUN_ID: ${{ github.run_id }}
          REPO: ${{ github.repository }}
          SERVER_URL: ${{ github.server_url }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          SHORT_SHA="${COMMIT_SHA:0:7}"
          RUN_URL="${SERVER_URL}/${REPO}/actions/runs/${RUN_ID}"
          if [ "$JOB_STATUS" = "success" ]; then
            BODY="✅ *CI Passed* — ${WORKFLOW}"$'\n'"🔀 Branch: \`${BRANCH}\`"$'\n'"📝 Commit: \`${SHORT_SHA}\`"$'\n'"🔗 [View Run](${RUN_URL})"
          else
            STAGE="${FAILED_STAGE:-Unknown stage}"
            BODY="❌ *CI Failed* — ${WORKFLOW}"$'\n'"💥 Failed at: \`${STAGE}\`"$'\n'"🔀 Branch: \`${BRANCH}\`"$'\n'"📝 Commit: \`${SHORT_SHA}\`"$'\n'"🔗 [View Run](${RUN_URL})"
          fi
          curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
            --data-urlencode "text=${BODY}" \
            --data-urlencode "parse_mode=Markdown" \
            --data-urlencode "disable_web_page_preview=true"

      - name: Notify Discord
        if: always()
        env:
          JOB_STATUS: ${{ job.status }}
          COMMIT_SHA: ${{ github.sha }}
          BRANCH: ${{ github.ref_name }}
          WORKFLOW: ${{ github.workflow }}
          RUN_ID: ${{ github.run_id }}
          REPO: ${{ github.repository }}
          SERVER_URL: ${{ github.server_url }}
          DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
        run: |
          SHORT_SHA="${COMMIT_SHA:0:7}"
          RUN_URL="${SERVER_URL}/${REPO}/actions/runs/${RUN_ID}"
          if [ "$JOB_STATUS" = "success" ]; then
            COLOR=3066993
            TITLE="✅ CI Passed — ${WORKFLOW}"
            FIELDS='[{"name":"Branch","value":"'"${BRANCH}"'","inline":true},{"name":"Commit","value":"'"${SHORT_SHA}"'","inline":true}]'
          else
            COLOR=15158332
            STAGE="${FAILED_STAGE:-Unknown stage}"
            TITLE="❌ CI Failed — ${WORKFLOW}"
            FIELDS='[{"name":"Failed Stage","value":"'"${STAGE}"'","inline":false},{"name":"Branch","value":"'"${BRANCH}"'","inline":true},{"name":"Commit","value":"'"${SHORT_SHA}"'","inline":true}]'
          fi
          TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
          curl -s -X POST "${DISCORD_WEBHOOK_URL}" \
            -H "Content-Type: application/json" \
            -d "{\"embeds\":[{\"title\":\"${TITLE}\",\"color\":${COLOR},\"fields\":${FIELDS},\"url\":\"${RUN_URL}\",\"footer\":{\"text\":\"SurvivorPulse CI\"},\"timestamp\":\"${TIMESTAMP}\"}]}"
```

---

## 6. Stage Tracking — Where to Add the Echo Line

For **pre-publish.yml**, add `echo "FAILED_STAGE=<stage name>" >> $GITHUB_ENV` as the first line of each of these steps:

```
Stage 1: Unit tests
Stage 2a: Integration tests (core)
Stage 2b: Integration tests (slow — full mode, 0 skips)
Stage 2c: Start server for HTTP integration tests
Stage 2c: HTTP integration tests (auth endpoints)
Stage 3: E2E tests
Stage 4a: Regression — module boundary check
Stage 4b: Regression — scoped test-data cleanup
Stage 4c: Regression — verify no test pools remain
```

For **release-guardian.yml**, add to:

```
Step A: Unit tests
Step B: Integration core tests
Step C: Integration slow tests
Step D: E2E tests
Step E: Tripwire
Step F: Canonical Spread Contract
Step G: CA1 Postmortem
Block committed .skip / .only
```

**Example (pre-publish.yml, Stage 2a):**
```yaml
      - name: 'Stage 2a: Integration tests (core)'
        run: |
          echo "FAILED_STAGE=Stage 2a: Integration tests (core)" >> $GITHUB_ENV
          set -o pipefail
          npm run test:integration:core 2>&1 | tee /tmp/integ-core.log
```

---

## 7. Composite Action Option (Future)

If the audit recommendation to extract shared DB setup into a composite action is implemented, the notification logic can also be extracted into `.github/actions/ci-notify/action.yml`:

```yaml
# .github/actions/ci-notify/action.yml
name: CI Notify
description: Send CI pass/fail notifications to Telegram and Discord

inputs:
  status:
    description: Job status (success/failure/cancelled)
    required: true
  failed_stage:
    description: Name of the stage that failed (if any)
    required: false
    default: ''
  telegram_bot_token:
    required: true
  telegram_chat_id:
    required: true
  discord_webhook_url:
    required: true

runs:
  using: composite
  steps:
    - name: Notify Telegram
      shell: bash
      env:
        JOB_STATUS: ${{ inputs.status }}
        FAILED_STAGE: ${{ inputs.failed_stage }}
        COMMIT_SHA: ${{ github.sha }}
        BRANCH: ${{ github.ref_name }}
        WORKFLOW: ${{ github.workflow }}
        RUN_ID: ${{ github.run_id }}
        REPO: ${{ github.repository }}
        SERVER_URL: ${{ github.server_url }}
        TELEGRAM_BOT_TOKEN: ${{ inputs.telegram_bot_token }}
        TELEGRAM_CHAT_ID: ${{ inputs.telegram_chat_id }}
      run: |
        # ... (same run block as section 4a)

    - name: Notify Discord
      shell: bash
      env:
        # ... (same as section 4b)
      run: |
        # ...
```

**Caller usage:**
```yaml
      - name: Notify
        if: always()
        uses: ./.github/actions/ci-notify
        with:
          status: ${{ job.status }}
          failed_stage: ${{ env.FAILED_STAGE }}
          telegram_bot_token: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          telegram_chat_id: ${{ secrets.TELEGRAM_CHAT_ID }}
          discord_webhook_url: ${{ secrets.DISCORD_WEBHOOK_URL }}
```

This replaces two ~30-line steps in each workflow with a single 8-line call.

---

## 8. Implementation Checklist

- [ ] Add `TELEGRAM_BOT_TOKEN` secret to GitHub repo
- [ ] Add `TELEGRAM_CHAT_ID` secret to GitHub repo
- [ ] Add `DISCORD_WEBHOOK_URL` secret to GitHub repo
- [ ] Add `echo "FAILED_STAGE=..."` line to each test stage in `pre-publish.yml`
- [ ] Add `echo "FAILED_STAGE=..."` line to each test stage in `release-guardian.yml`
- [ ] Add the two notification steps (Telegram + Discord) to `pre-publish.yml`
- [ ] Add the two notification steps (Telegram + Discord) to `release-guardian.yml`
- [ ] Test by pushing a commit that breaks a known test — verify message arrives with correct stage name
- [ ] *(Optional)* Extract into `.github/actions/ci-notify/action.yml` composite action

---

*Authored by Rita the Relay for SurvivorPulse CI pipeline review.*

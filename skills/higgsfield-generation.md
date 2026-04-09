---
name: Higgsfield Generation
description: Two-path generation skill — Higgsfield Cloud API (primary) and Playwright browser automation (fallback) for video and image generation.
autoInvoke: true
triggers:
  - video generation
  - image generation
  - Higgsfield
  - generate clip
  - generate frame
---

# Higgsfield Generation — Dual-Path Skill

## Primary Path: Higgsfield Cloud API

Use the `higgsfield-client` Python SDK via the project venv at `/opt/pipeline/.venv/`.

```python
from higgsfield_client import SyncClient, submit, status, result

client = SyncClient(api_key=os.environ['HIGGSFIELD_API_KEY'])
controller = submit(application='<model>', arguments={...})
# Poll for completion
while not controller.is_done():
    time.sleep(5)
# Download result
output = result(controller.request_id)
```

**When to use API:** All standard text-to-image, image-to-video, and model-based generations. This is the default for every generation task.

**API error handling:**
- Rate limit → wait 60 seconds, retry (max 3 retries)
- Credit exhaustion → STOP all generation, notify owner via Telegram
- Model unavailable → switch to next-best model (Kling 3.0 → Veo 3.1 → Sora 2)
- Network error → retry with exponential backoff (5s, 15s, 45s)

## Fallback Path: Playwright Browser Automation

Use only when the API doesn't expose a needed feature (Cinema Studio camera controls, Hero Frame workflows, lipsync studio).

**Stealth configuration:**
- Launch with `--browser-channel=chrome` (system Chrome, not Chromium)
- Use `--vision` mode (screenshot-based interaction)
- Add human-like timing: 50-200ms between keystrokes, 500-1500ms between actions
- Randomize mouse movements slightly
- Never navigate faster than a human would

**Login flow:**
1. Navigate to higgsfield.ai/login
2. Enter HIGGSFIELD_EMAIL and HIGGSFIELD_PASSWORD with realistic typing delays
3. Handle any 2FA or CAPTCHA — screenshot and analyze, escalate to owner if unsolvable
4. Verify login success by checking for dashboard elements

**DataDome detection recovery:**
If blocked by DataDome (page returns challenge/403/blank):
1. Close browser session
2. Switch to API path for this generation
3. Log the incident for debugging
4. If API cannot handle this specific task, notify owner via Telegram

## Model Selection Rules

| Shot Type | Model | Credits | Notes |
|-----------|-------|---------|-------|
| Establishing shots, truck footage, B-roll | Kling 3.0 | ~6 | Default for 80% of shots |
| Hero shots needing camera control | Cinema Studio + Kling 3.0 | ~12-20 | Via Playwright if API doesn't support Cinema Studio |
| Money shots (climax, reveal, CTA) | Veo 3.1 | 40-70 | Only after static frame passes QA |
| Static frame validation | Flux.2 Pro / Seedream / Nano Banana | 0-2 | Always generate still first for premium shots |

## Credit Protection

- NEVER generate a premium video clip (>20 credits) without a passed static frame first
- ALWAYS check remaining credits before starting a batch
- If credits drop below 500, notify owner and switch to Kling 3.0 only
- Log every generation with model, credits consumed, and generation_method in SQLite

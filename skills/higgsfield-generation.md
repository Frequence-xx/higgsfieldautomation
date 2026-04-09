---
name: Video Generation
description: AIMLAPI-first generation — Nano Banana Pro for hero frames, Kling v3 I2V for video animation. Higgsfield browser as fallback only.
autoInvoke: true
triggers:
  - video generation
  - image generation
  - Higgsfield
  - AIMLAPI
  - generate clip
  - generate frame
  - Kling
  - animate
---

# Video Generation — AIMLAPI-First Architecture

## Tier 1A: AIMLAPI — Hero Frame Generation (API)

Use AIMLAPI for hero frame (still image) generation. No browser needed.

```python
import httpx, os

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Nano Banana Pro (cheapest, good quality)
resp = httpx.post("https://api.aimlapi.com/v2/generate/image/google/generation", json={
    "model": "google/nano-banana-pro",
    "prompt": "<scene description with cinematic details>",
    "aspect_ratio": "16:9",
}, headers=headers, timeout=30)
```

**Image model options:**
- `google/nano-banana-pro` — cheapest, good for establishing shots and B-roll
- `flux-pro/v1.1` — higher quality, better for hero shots with fine detail
- `flux-pro/v1.1-ultra` — highest quality, money shots only
- `bytedance/seedream-v4-text-to-image` — alternative high-quality option

**After generating:** Run QA on the hero frame (8 dimensions + Shari'ah + cinematic quality). Only send to Tier 1B if it passes.

## Tier 1B: AIMLAPI — Video Animation (API)

Use AIMLAPI for all image-to-video animation. Clean REST API, no browser needed.

```python
import httpx, os

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Submit Kling v3 Standard I2V (audio OFF — cheapest option)
resp = httpx.post("https://api.aimlapi.com/v2/generate/video/kling/generation", json={
    "model": "kling-video/v3/standard/image-to-video",
    "image_url": "<hero_frame_cdn_url>",
    "prompt": "<motion description>",
    "duration": "5",
    "aspect_ratio": "16:9"
}, headers=headers, timeout=30)

task_id = resp.json()["id"]

# Poll for completion (every 10s, max 5 min)
import time
for i in range(30):
    time.sleep(10)
    sr = httpx.get("https://api.aimlapi.com/v2/generate/video/kling/generation",
                   params={"generation_id": task_id}, headers=headers, timeout=30)
    if sr.json()["status"] == "completed":
        video_url = sr.json()["video"]["url"]
        break
```

**AIMLAPI model strings:**
- `kling-video/v3/standard/image-to-video` — $0.42/5s (80% of shots)
- `kling-video/v3/pro/image-to-video` — $0.56/5s (hero shots)
- Veo 3.1, Wan 2.6 also available (see credit-efficiency.md for routing)

**CRITICAL: Always use I2V, NOT T2V. I2V is 2.6x cheaper.**
**CRITICAL: Always audio OFF. Add voiceover in post. Audio adds 50% surcharge.**

**Error handling:**
- 403 (out of credits) → STOP, notify owner via Telegram
- 404 (model not found) → check model string spelling
- Timeout → retry once with 30s timeout, then STOP
- Generation failed → log failure, do NOT auto-retry (costs credits)

## Tier 2 (Fallback): Higgsfield Cinema Studio 2.0 — Browser Generation

Use Patchright browser automation only when AIMLAPI image models cannot achieve a specific Cinema Studio feature (camera body/lens simulation, 3D scene exploration, character Elements).

**When to use:** Only when the prompt requires Cinema Studio 2.0-specific features not available via AIMLAPI text-to-image.

**Browser setup:** `/opt/pipeline/scripts/higgsfield_browser.py`
- Patchright + system Chrome (`channel="chrome"`)
- Persistent profile at `~/.config/higgsfield-profile/`
- Xvfb headed mode (`DISPLAY=:99`)
- Cookie injection from user's browser for auth

**Cinema Studio 2.0 workflow:**
1. Open Scenes panel → click "Cinema 2.0" to switch model
2. Set prompt, camera settings, aspect ratio, resolution
3. Click GENERATE once (2 credits per image)
4. Download the hero frame
5. Send hero frame URL to AIMLAPI Tier 1 for animation

## Tier 3 (Fallback): Higgsfield Cloud API — Soul/DoP

Use the Higgsfield Python SDK for their native models only (Soul image, DoP video).

```python
key = f"{os.environ['HF_API_KEY']}:{os.environ['HF_API_SECRET']}"
headers = {'Authorization': f'Key {key}', 'Content-Type': 'application/json'}

# Soul text-to-image
resp = httpx.post('https://platform.higgsfield.ai/v1/text2image/soul', json={...})
# DoP image-to-video
resp = httpx.post('https://platform.higgsfield.ai/v1/image2video/dop', json={...})
```

**When to use:** Only when Higgsfield-native models are specifically needed or AIMLAPI is unavailable.

## Generation Rules

1. **ONE generation at a time. Verify correct image before generating.**
2. For shots WITH characters: create character reference sheet first (see `character-consistency.md`), then use Kontext Max for hero frames + Kling O1 Reference for video
3. For shots WITHOUT characters: Nano Banana Pro for hero frame + Kling v3 Standard I2V for video
4. Generate hero frame → QA (8 dims + cinematic + Shari'ah) → animate via AIMLAPI → QA again → post-production
5. Log every generation in SQLite: model, cost, QA scores, pass/fail
6. Max 3 retries per clip. After 3 failures → STOP, escalate to owner
7. Never use text-to-video for final shots — always image-to-video from a QA-passed hero frame

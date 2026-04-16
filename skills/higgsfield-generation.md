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

## Prompt Engineering — Hero Frame Generation

### Universal Rules (Both Models)
- **Natural language over keyword lists.** Write like briefing a human cinematographer, not tagging a search engine.
- **Word order = priority.** Put the most important elements first: Subject → Action → Style → Camera → Context.
- **Sweet spot: 30–80 words.** Complex scenes may go to 100; simple shots can be shorter.
- **Avoid vague adjectives:** "beautiful", "stunning", "aesthetic" — replace with specific visual facts: "soft directional window light from the upper left", "shallow depth of field, smooth bokeh".

### Nano Banana Pro (`google/nano-banana-pro`) — Prompt Template

```
[Shot type and style] of [subject with specific physical details] [action/pose] in [setting/environment],
[lighting description with direction], [mood/atmosphere], [lens and aperture],
[camera angle and composition], [texture/materiality details like "worn leather", "wet pavement"].
```

**Working cinematic template (copy and adapt):**
```
Cinematic wide establishing shot of a large white moving truck with blue "Snel Verhuizen"
lettering parked outside a Dutch residential home on a quiet tree-lined street,
golden hour backlight with long shadows, warm amber highlights on chrome,
24mm anamorphic lens, slight lens flare, rule of thirds composition,
film grain, natural wear on asphalt, realistic fabric wrinkles on driver's jacket.
```

**Camera specs that work well with NBP:**
| Intent | Lens | Aperture | Notes |
|--------|------|----------|-------|
| Wide establishing | 24mm anamorphic | f/5.6–f/8 | Reveals full scene, slight barrel distortion |
| Truck beauty / product | 35mm | f/2.8–f/4 | Natural perspective, mild compression |
| Portrait / emotional | 85mm | f/1.4–f/2.2 | Subject isolation, smooth bokeh |
| Detail / texture | 100mm macro | f/2.8 | Object close-ups, tight DOF |
| Action / moving | 50mm | f/2.8 | Natural eye perspective |

**Lighting descriptions that trigger cinematic quality:**
- "Golden hour backlight with warm amber highlights and long foreground shadows"
- "Overcast soft diffused light, no harsh shadows, neutral whites"  
- "Three-point studio lighting, soft key from upper left, rim light separating subject from background"
- "Blue-hour twilight, streetlights casting warm pools, deep cool shadows"

**NBP-specific strengths:**
- Accurate Dutch street architecture (request "Amsterdam/Rotterdam residential street")
- Up to 14 reference images accepted — pass character reference sheet images in the API call
- Natural text rendering (truck logo, signage) — enclose text in quotes: "Snel Verhuizen"
- Reads conversational edits: "Make the sky more dramatic with storm clouds, keep everything else the same"

**What to avoid with NBP:**
- Vague qualifiers: "cinematic", "beautiful", "high quality" without specifics
- Multiple conflicting styles in one prompt
- Pronouns — name subjects explicitly: "the bearded man in the navy kufiya" not "he"

### Flux Kontext Max — Edit Instruction Format

Use Flux Kontext Max when you have a hero frame that's close but needs targeted adjustments:

**Edit instruction template:**
```
Change [specific element] to [new state], while keeping [everything else] exactly the same.
Maintain [subject's name or description] facial features, clothing, and pose unchanged.
```

**Working edit examples:**
- "Change the background to a rain-wet Amsterdam street at golden hour, while keeping the moving truck and crew in the exact same position and clothing"
- "Replace the grey overcast sky with dramatic golden hour clouds, maintaining all foreground elements unchanged"
- "Change the truck's livery color from white to cream, keeping all other elements the same"

**Kontext Max best practices:**
- Name subjects descriptively, never use pronouns: "the man with the white kufiya" not "him"
- Explicitly state what to preserve: "maintaining the original composition, lighting direction, and color grading"
- Iterative editing is stable — make multiple sequential edits without quality degradation
- Prompt upsampling available but disables reproducibility — skip for final production frames
- Optimal prompt length: 30–60 words for edits

## Generation Rules

1. **ONE generation at a time. Verify correct image before generating.**
2. For shots WITH characters: create character reference sheet first (see `character-consistency.md`), then use Kontext Max for hero frames + Kling O1 Reference for video
3. For shots WITHOUT characters: Nano Banana Pro for hero frame + Kling v3 Standard I2V for video
4. Generate hero frame → QA (8 dims + cinematic + Shari'ah) → animate via AIMLAPI → QA again → post-production
5. Log every generation in SQLite: model, cost, QA scores, pass/fail
6. Max 3 retries per clip. After 3 failures → STOP, escalate to owner
7. Never use text-to-video for final shots — always image-to-video from a QA-passed hero frame
8. **Prompt failure diagnosis:** If a frame fails QA, identify the specific failing dimension before re-prompting. Adjust only the relevant prompt element — don't rebuild the whole prompt.

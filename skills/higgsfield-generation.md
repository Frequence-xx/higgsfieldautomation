---
name: Video Generation (DEPRECATED)
description: DEPRECATED — Use generation-image.md and generation-video.md instead. AIMLAPI-first generation — Nano Banana Pro for hero frames, Kling v3 I2V for video animation. Higgsfield browser as fallback only.
autoInvoke: false
triggers:
  - video generation
  - image generation
  - Higgsfield
  - AIMLAPI
  - generate clip
  - generate frame
  - Kling
  - animate
negatives:
  - Do NOT invoke when doing post-production (captions, audio, FFmpeg assembly)
  - Do NOT invoke when performing QA scoring (use video-qa-rubric.md)
  - Do NOT invoke when writing briefs or shot lists (use brief-intake.md)
---

> **DEPRECATED** — This skill has been split into two focused skills. Use those instead:
> - **`generation-image.md`** — Tier 1A: Hero frame models (NBP, Kontext Max, Flux Pro), parameters, 9:16 native generation
> - **`generation-video.md`** — Tier 1B: I2V models (Kling v3), parameters, motion prompts, known failures, camera control
>
> This file is retained for historical reference only. Do NOT invoke for new work.

# Video Generation — AIMLAPI-First Architecture (DEPRECATED)

> **NOTE:** This skill has been split into two focused skills for better invocation:
> - **`generation-image.md`** — Tier 1A: Hero frame models (NBP, Kontext Max, Flux Pro), parameters, 9:16 native generation
> - **`generation-video.md`** — Tier 1B: I2V models (Kling v3), parameters, motion prompts, known failures, camera control
>
> This file remains as the combined reference. For new work, prefer the split versions.

## Tier 1A: AIMLAPI — Hero Frame Generation (API)

Use AIMLAPI for hero frame (still image) generation. No browser needed.

**CRITICAL: All hero frames MUST be generated natively in 9:16 for vertical platforms (Reels/TikTok/Shorts). Never crop, zoom, or pad a square image.**

### Endpoint
**POST** `https://api.aimlapi.com/v1/images/generations`

### Native 9:16 Generation — Verified Parameters (tested 2026-04-10)

#### Nano Banana Pro (text-to-image)
```python
import httpx, os

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/nano-banana-pro",
    "prompt": "<scene description with cinematic details>",
    "aspect_ratio": "9:16",   # VERIFIED: produces native 768x1376 vertical
    "resolution": "1K",       # Options: 1K, 2K, 4K
    "num_images": 1,
}, headers=headers, timeout=60)

hero_url = resp.json()["data"][0]["url"]
```

#### Nano Banana Pro Edit (reference-based, up to 14 images)
```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/nano-banana-pro-edit",
    "prompt": "<compositing instruction referencing input images>",
    "image_urls": ["<ref1_url>", "<ref2_url>", "<scene_url>"],  # up to 14
    "aspect_ratio": "9:16",   # Documented as supported
    "resolution": "1K",       # Options: 1K, 2K, 4K
    "num_images": 1,
}, headers=headers, timeout=60)

hero_url = resp.json()["data"][0]["url"]
```

#### Flux Kontext Max (image-to-image, character lock, up to 4 refs)
```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "flux/kontext-max/image-to-image",
    "prompt": "<scene description maintaining character identity>",
    "image_url": ["<character_ref1>", "<character_ref2>"],  # up to 4
    "aspect_ratio": "9:16",   # VERIFIED: produces native 752x1392 vertical
    "num_images": 1,
}, headers=headers, timeout=90)

hero_url = resp.json()["data"][0]["url"]
```

### 9:16 Resolution Reference Table (Nano Banana Pro / Edit)

| Resolution | 9:16 Dimensions | Cost    | Gen Time |
|------------|-----------------|---------|----------|
| 1K         | 768 x 1344      | ~$0.13  | ~13s     |
| 2K         | 1536 x 2688     | ~$0.13  | ~16s     |
| 4K         | 3072 x 5376     | ~$0.24  | ~22s     |

**Note:** Actual output may vary slightly (e.g., 768x1376 observed for 1K). The aspect ratio is correct; minor pixel differences do not affect composition or Kling I2V input.

### Supported Aspect Ratios (all models)

| Ratio | Use Case |
|-------|----------|
| 9:16  | Instagram Reels, TikTok, YouTube Shorts (PRIMARY) |
| 16:9  | YouTube landscape, desktop ads |
| 1:1   | Instagram feed, reference sheets |
| 4:3   | Legacy TV, some display ads |
| 2:3   | Pinterest, portrait photography |
| 21:9  | Ultrawide cinema |

### Model Selection for Hero Frames

| Model | Best For | Aspect Ratio Control | Max Refs |
|-------|----------|---------------------|----------|
| `google/nano-banana-pro` | Text-only scenes, B-roll, establishing shots | `aspect_ratio` param | 0 (text only) |
| `google/nano-banana-pro-edit` | Brand asset compositing (truck + character + box) | `aspect_ratio` param | 14 |
| `flux/kontext-max/image-to-image` | Character identity lock across scenes | `aspect_ratio` param | 4 |

**Additional image models (not yet tested for 9:16):**
- `flux-pro/v1.1` — higher quality, better for hero shots with fine detail
- `flux-pro/v1.1-ultra` — highest quality, money shots only
- `bytedance/seedream-v4-text-to-image` — alternative high-quality option

**After generating:** Run QA on the hero frame (8 dimensions + Shari'ah + cinematic quality). Only send to Tier 1B if it passes.

## Tier 1B: AIMLAPI — Video Animation (API)

Use AIMLAPI for all image-to-video animation. Clean REST API, no browser needed.

### Correct Model Strings (updated 2026-04-10)
- Standard (720p): `klingai/video-v3-standard-image-to-video` — $0.218/sec audio OFF = **$1.09/5s**
- Pro (1080p): `klingai/video-v3-pro-image-to-video` — $0.291/sec audio OFF = **$1.46/5s**
- **USE PRO FOR ALL FINAL OUTPUT** — Standard is only 720p, Pro gives native 1080p

### Resolution Output
- Standard: 720×1280 (9:16), 1280×720 (16:9), 960×960 (1:1)
- Pro: **1080×1920 (9:16)**, 1920×1080 (16:9), 1440×1440 (1:1)

### Complete API Call Template

```python
import httpx, os

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Submit Kling v3 Pro I2V — 1080p, audio OFF
resp = httpx.post("https://api.aimlapi.com/v2/generate/video/kling/generation", json={
    "model": "klingai/video-v3-pro-image-to-video",
    "image_url": "<hero_frame_cdn_url>",
    "prompt": "<motion description>",
    "duration": "5",
    "aspect_ratio": "9:16",
    "generate_audio": False,
    "cfg_scale": 0.5,
    "negative_prompt": "blurry, distorted, low quality, jittery, flickering, morphing faces",
    # Optional: camera control
    "camera_control": {
        "type": "simple",
        "config": {
            "horizontal": 0,
            "vertical": 0,
            "pan": 0,
            "tilt": 0,
            "roll": 0,
            "zoom": -2  # gentle push-in (negative = narrower FOV = zoom in)
        }
    },
    # Optional: character consistency (up to 4 elements)
    # "elements": [
    #     {
    #         "frontal_image_url": "<character_front.png>",
    #         "reference_image_urls": ["<character_3quarter.png>", "<character_profile.png>"]
    #     }
    # ],
    # Optional: end frame for smooth transitions
    # "tail_image_url": "<last_frame_url>"
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

### All Available Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| model | string | required | See model strings above |
| image_url | string | required | URL or base64. Min 300x300, max 10MB, JPG/PNG |
| prompt | string | required | Motion description, max 2500 chars |
| duration | int | 5 | 3-15 seconds |
| aspect_ratio | string | "16:9" | "16:9", "9:16", "1:1" |
| generate_audio | bool | true | **ALWAYS set false** — saves 33% |
| cfg_scale | float | 0.5 | 0-1, prompt adherence |
| negative_prompt | string | "" | Elements to avoid, max 2500 chars |
| tail_image_url | string | — | End frame for transitions |
| camera_control | object | — | See camera control section above |
| elements | array | — | Up to 4 character references for consistency |
| static_mask_url | string | — | Motion brush: static areas |
| dynamic_masks | array | — | Motion brush: animated paths |

**CRITICAL: Always set generate_audio: false. Audio ON adds 50% surcharge.**
**CRITICAL: Always set aspect_ratio to match target platform (9:16 for vertical).**
**CRITICAL: Use Pro model for 1080p output. Standard is only 720p.**

**Error handling:**
- 403 (out of credits) → STOP, notify owner via Telegram
- 404 (model not found) → check model string spelling
- Timeout → retry once with 30s timeout, then STOP
- Generation failed → log failure, do NOT auto-retry (costs credits)

### I2V Prompt Engineering (researched 2026-04-10, updated with deep research)

**Golden Rule: Only describe MOTION. Never redescribe what is in the image.**

The source image provides all visual information. The prompt directs motion only.

**I2V Prompt Formula (updated):**
`[What moves] + [How it moves] + [Speed modifier] + [What stays still] + [Camera instruction] + [Motion endpoint]`

**Optimal prompt length:** 15-40 words (much shorter than T2V's 50-80 words). Beyond ~80 words the model starts averaging conflicting instructions.

**The Six Commandments of I2V Prompting:**
1. ONE clear motion per subject — never give competing actions
2. Always include a speed modifier — "slowly", "gently", "smoothly" (unspecified = jitter)
3. Always include a motion endpoint — "eases to a gentle stop" (prevents 99% hangs)
4. Always specify what stays still — "background remains static", "truck stays stationary"
5. Use physical verbs — "walks", "lifts", "turns" (not abstract "dynamic energy")
6. Specify specific body parts — "hair moves", "fingers grip" (not "person moves")

**Motion endpoints (always include one):**
- "then settles back into place"
- "motion gradually slowing to stop"
- "eases to a gentle stop"
- "returning to stillness"

**What works vs what causes jitter:**
- ONE clear motion per subject (not multiple competing motions)
- Speed modifiers: "slowly", "gently", "smoothly" (not unspecified speed)
- Specific body parts: "hair moves", "fingers grip" (not "person moves around")
- Physical verbs: "walks", "lifts", "turns" (not abstract "dynamic energy")
- "Background remains static" constraint (prevents background morphing)
- NEVER include lighting descriptions in I2V prompts (image already has lighting)
- Anchor hands to objects: "fingers grip box edges" not "moves hands freely"
- Stage expression changes: "neutral → eyebrows lift → smile forms" (prevents morphing)

### CFG Scale Guidelines (researched 2026-04-10)

| Shot Type | cfg_scale | Reasoning |
|-----------|-----------|-----------|
| Establishing shots / B-roll | 0.4 | Creative interpretation acceptable |
| Character movement | 0.5 (default) | Balanced motion + adherence |
| Product/truck hero shots | 0.7 | Strict adherence to preserve branding |
| Branded transitions | 0.7 | Preserve specific visual elements |

Higher CFG does NOT always mean better quality — high values can reduce natural motion fluidity.

### Camera Control Best Practices (researched 2026-04-10)

All values range **-10 to 10**. Recommended values for cinematic work: **2-5**.

| Shot Type | Config | Notes |
|-----------|--------|-------|
| Gentle push-in | `zoom: -2` or `-3` | Emotional close-ups, intimacy |
| Slow pull-back reveal | `zoom: 2` or `3` | Reveals environment |
| Product orbit | `tilt: 3` to `5` | Moderate rotation around subject |
| Crane up | `vertical: 3, pan: -2` | Rise with slight downward angle |
| Lateral tracking | `horizontal: 3` to `5` | Smooth side tracking |
| Static (prompt-driven) | All zeros | Use prompt for micro-jitter |

**Rules:** Max 2 simultaneous movements. Values 7-10 are dramatic but unstable. Never combine opposing movements. Camera control overrides prompt-based camera direction — use one or the other.

### Negative Prompt Template (researched 2026-04-10, updated with deep research)

**Universal baseline (ALWAYS include ALL of these):**
```
blurry, distorted, low quality, jittery, flickering, morphing faces, warping, deformed hands, extra fingers, sliding feet, identity drift, watermark, camera shake, inconsistent lighting, plastic skin, cartoonish, color shift
```

**Add for character shots:**
```
face distortion, unnatural skin texture, floating limbs, breathing movement, body sway, weight shifting, expression change, mood shift
```

**Add for truck/product shots:**
```
vehicle movement, driving, rolling, ghost driving, text morphing, label warping, geometry distortion, reflection artifacts, surface inconsistency
```

**Add for camera movement shots:**
```
camera drift, sudden zooms, background shifting, unstable details, background morphing
```

Use 8-12 specific terms per category. Avoid vague terms like "bad quality" or "ugly" — be specific about the artifact to prevent.

### Duration Strategy (researched 2026-04-10)

| Complexity | Optimal Duration | Notes |
|------------|-----------------|-------|
| Simple (single subject) | Up to 10s | Full coherence maintained |
| Medium (multiple elements) | 6-8s | Sweet spot |
| Complex (multiple subjects) | 5s | Chain clips in post-production |

**Default to 5 seconds** for maximum quality per credit. Cost doubles with duration.
Test in Standard mode (~$1.09/5s), finalize in Pro (~$1.46/5s) to save ~19% on iteration.

### Source Image Quality Checklist (researched 2026-04-10)

Before submitting to I2V, verify the hero frame has:
1. Even lighting (no harsh shadows that confuse the motion model)
2. Clear facial geometry (direct or three-quarter view for best 3D mapping)
3. Simple textures (solid colors prevent outfit morphing)
4. Low noise/grain (noise converts to flicker in video)
5. Simple background (busy backgrounds morph during camera movement)
6. Matching aspect ratio (9:16 source for 9:16 output)
7. No unintentional text (text warps during generation unless constrained)

### Shot-Type Specific Presets (researched 2026-04-10)

**Establishing shot:**
```python
cfg_scale=0.4, duration="5", camera={"zoom": 2, "vertical": 1},
prompt="Slow pull-back revealing full street scene. Ambient leaves drift gently in breeze. All vehicles and buildings remain stationary. Lighting remains perfectly consistent throughout. Motion eases to stop.",
negative_prompt="jittery, flickering, inconsistent lighting, morphing, camera shake, blurry, vehicle movement, ghost driving, background shifting, color shift"
```

**Character close-up:**
```python
cfg_scale=0.5, duration="5", camera={"zoom": -2},
prompt="Subject blinks once naturally. Slight confident smile forms gradually. Hair moves gently. Maintains exact posture, no body sway. Background completely static. Lighting consistent. Expression settles.",
negative_prompt="face distortion, morphing faces, identity drift, breathing movement, body sway, expression change, extra fingers, plastic skin, flickering, sliding feet, color shift"
```

**Truck/product hero:**
```python
cfg_scale=0.7, duration="5", camera={"tilt": 3},
prompt="Slow camera orbit around truck. Light reflections glide gently across surface. Branding text stays perfectly sharp and stable. Truck completely stationary, no vehicle movement. Foreground leaves drift subtly. Motion gradually eases to stop.",
negative_prompt="vehicle movement, driving, rolling, ghost driving, text morphing, label warping, geometry distortion, reflection artifacts, blurry, flickering, color shift, jittery, inconsistent lighting"
```

**Walking/action:**
```python
cfg_scale=0.5, duration="5", camera={"horizontal": 3},
prompt="Man walks forward with natural stride, each step lands heel-first then rolls forward. Arms swing naturally. Coat fabric sways with movement. Steps grounded with visible weight transfer. Movement eases to gentle stop.",
negative_prompt="sliding feet, floating limbs, identity drift, jittery, morphing faces, extra fingers, camera shake, breathing artifacts, robotic movement"
```

**Box handoff (anchored hands):**
```python
cfg_scale=0.5, duration="5", camera={"horizontal": 2},
prompt="Man's fingers grip firmly around cardboard box edges. He extends arms slowly forward, handing box to second person. Both characters' feet remain planted. Truck completely stationary in background. Motion eases to stop.",
negative_prompt="floating limbs, extra fingers, deformed hands, sliding feet, identity drift, face distortion, vehicle movement, ghost driving, flickering, object morphing, color shift"
```

### CRITICAL: Preventing Known Production Failures (deep research 2026-04-10)

#### Preventing Ghost Driving (Truck Movement)
Our #1 production failure. Triple-lock approach:

1. **Prompt constraint:** ALWAYS include "truck remains completely stationary, no vehicle movement" in every truck shot
2. **Negative prompt:** ALWAYS include "vehicle movement, driving, rolling, ghost driving, sliding vehicle"
3. **Static mask (nuclear option):** Generate a mask image (white=freeze, black=allow motion) covering the truck and pass as `static_mask` parameter:
```python
"static_mask": "<url_to_mask_image_covering_truck_area>"
```

#### Preventing Breathing Artifacts
NEVER use these words in motion prompts: "breathing", "weight shift", "subtle body movement"
- For standing characters: "maintains exact posture, no body sway"
- Only describe the SPECIFIC motion you want: "blinks naturally" not "subtle life-like movement"
- Negative prompt: "breathing movement, chest expansion, body sway, weight shifting"

#### Preventing Expression Changes
- Add "maintains exact expression, no expression changes" for static expression shots
- For intentional changes, STAGE the transition: "neutral → eyebrows lift → eyes widen → smile forms"
- Negative prompt: "sudden expression change, mood shift, grimacing"

#### Preventing Color Shifts
- NEVER include lighting descriptions in I2V prompts (image provides lighting)
- Add "lighting remains consistent throughout" to every prompt
- Use cfg_scale 0.7 for branded shots (higher adherence preserves colors)
- Negative prompt: "color shift, lighting change, exposure drift, color grading change"

#### Hand/Finger Stability
- ALWAYS anchor hands to objects: "fingers grip the box edge firmly"
- Never let hands move freely: "She moves her hands" causes deformation
- Medium shots safer than extreme close-ups for hand interactions
- Negative prompt: "extra fingers, deformed hands, floating limbs"

#### Foot Grounding
- Describe heel-to-toe mechanics: "each step lands heel-first, then rolls forward"
- Keep characters centered in frame (model maintains proportions better)
- For standing characters: "feet remain planted on ground"
- Negative prompt: "sliding feet, floating, stiff legs, gliding, no foot contact"

### Static Mask API Usage (for object freezing)

When prompt + negative prompt alone cannot prevent object movement:

```python
# Create mask: white pixels = freeze, black pixels = allow motion
# Upload to accessible URL, then include in API call:
{
    "static_mask": "https://cdn.example.com/truck_freeze_mask.png",
    "prompt": "Camera slowly orbits. Foreground leaves drift. Motion eases to stop.",
    "negative_prompt": "vehicle movement, ghost driving, ..."
}
```

**When to use:** Truck in frame that MUST NOT move, branded signage, background objects that keep morphing.

### Elements (Character Binding) for I2V Consistency

```python
{
    "elements": [
        {
            "frontal_image_url": "https://cdn.example.com/character_front.png",
            "reference_image_urls": [
                "https://cdn.example.com/character_3quarter.png",
                "https://cdn.example.com/character_profile.png"
            ]
        }
    ]
}
```

Provide 3-4 angles (front, three-quarter, profile). Model maps character as 3D spatial anchor, maintaining identity even during camera movement.

### Hero Frame Prompting (Nano Banana Pro & Kontext Max)

**Nano Banana Pro (text-to-image):**
- Write like a Creative Director, not keyword tags
- Include camera specs: "50mm f/2.8, shallow depth of field"
- Wrap text in quotes: `displaying "SNELVERHUIZEN" in bold white sans-serif`
- Provide context: "for a premium Dutch moving company ad campaign"
- Keep text to 25 chars max per element for legibility

**Flux Kontext Max (character lock):**
- Reference images by position AND content: "the man from the first image"
- NEVER use pronouns — use descriptive names
- End with explicit preservation: "preserving exact facial features, expression, and outfit"
- For scene changes: "while keeping the person in the exact same position, scale, and pose"
- ALWAYS use original reference, never chain outputs as new references

**See `/opt/pipeline/output/research/prompting_guidelines_per_model.md` for complete templates.**

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

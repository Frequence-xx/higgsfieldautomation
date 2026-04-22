---
name: Generation — Video Animation (I2V)
description: Tier 1B video animation via AIMLAPI Kling v3 I2V. Covers motion prompting, camera control, negative prompts, cfg_scale, duration strategy, ghost-driving prevention, breathing artifact prevention, known failures, and API call templates.
autoInvoke: true
triggers:
  - video generation
  - animate
  - I2V
  - image to video
  - Kling
  - motion prompt
  - video clip
  - generate video
negatives:
  - Do NOT invoke when generating hero frames (use generation-image.md)
  - Do NOT invoke when performing QA or scoring (use video-qa-rubric.md)
  - Do NOT invoke when doing post-production, captions, or audio assembly
---

# Generation — Video Animation (I2V Models)

Tier 1B of the pipeline. Animate QA-passed hero frames into 5-second video clips via AIMLAPI Kling v3 I2V.

## Critical Rules

1. **MUST NOT animate a hero frame that has not passed QA AND received owner approval.** Static-first validation + owner sign-off are both mandatory before spending video credits.
2. **MUST set `generate_audio: false`** on every call. Audio ON adds 50% surcharge. Add audio in post.
3. **MUST set `aspect_ratio: "9:16"`** to match the hero frame and target platform.
4. **MUST use Pro model for final output** — Standard is only 720p. Pro gives native 1080p.
5. **MUST generate ONE clip at a time.** Verify before proceeding.
6. **SHOULD default to 5-second duration** for maximum quality per credit.

## Model Strings and Pricing

| Model | AIMLAPI String | Resolution | Cost (5s, audio OFF) |
|-------|---------------|------------|---------------------|
| Kling v3 Standard I2V | `klingai/video-v3-standard-image-to-video` | 720x1280 (9:16) | **$1.09** |
| Kling v3 Pro I2V | `klingai/video-v3-pro-image-to-video` | **1080x1920 (9:16)** | **$1.46** |

**Use Standard for iteration/testing, Pro for final output.**

## Complete API Call Template

```python
import httpx, os, time

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Submit Kling v3 Pro I2V
resp = httpx.post("https://api.aimlapi.com/v2/generate/video/kling/generation", json={
    "model": "klingai/video-v3-pro-image-to-video",
    "image_url": "<hero_frame_cdn_url>",
    "prompt": "<motion description ONLY — never redescribe the image>",
    "duration": "5",
    "aspect_ratio": "9:16",
    "generate_audio": False,
    "cfg_scale": 0.5,
    "negative_prompt": "blurry, distorted, low quality, jittery, flickering, morphing faces, warping, deformed hands, extra fingers, sliding feet, identity drift, watermark, camera shake, inconsistent lighting, plastic skin, cartoonish, color shift",
    # Optional: camera control
    "camera_control": {
        "type": "simple",
        "config": {
            "horizontal": 0, "vertical": 0, "pan": 0,
            "tilt": 0, "roll": 0, "zoom": -2
        }
    },
}, headers=headers, timeout=30)

task_id = resp.json()["id"]

# Poll for completion (every 10s, max 5 min)
for i in range(30):
    time.sleep(10)
    sr = httpx.get("https://api.aimlapi.com/v2/generate/video/kling/generation",
                   params={"generation_id": task_id}, headers=headers, timeout=30)
    if sr.json()["status"] == "completed":
        video_url = sr.json()["video"]["url"]
        break
```

## I2V Motion Prompting — The Six Commandments

**THE FUNDAMENTAL RULE: Never re-describe what is in the image. The image IS the scene. The prompt contains ONLY motion instructions.**

**Formula:** `[What moves] + [How it moves] + [Speed modifier] + [What stays still] + [Camera instruction] + [Motion endpoint]`

**Optimal length:** 15-40 words. Beyond ~80 words the model averages conflicting instructions.

1. **ONE clear motion per subject** — never give competing actions
2. **Always include a speed modifier** — "slowly", "gently", "smoothly" (unspecified = jitter)
3. **Always include a motion endpoint** — "eases to a gentle stop" (prevents 99% of hangs)
4. **Always specify what stays still** — "background remains static", "truck stays stationary"
5. **Use physical verbs** — "walks", "lifts", "turns" (not abstract "dynamic energy")
6. **Specify body parts** — "hair moves", "fingers grip" (not "person moves")

## CFG Scale Guidelines

| Shot Type | cfg_scale | Reasoning |
|-----------|-----------|-----------|
| Establishing / B-roll | 0.4 | Creative interpretation acceptable |
| Character movement | 0.5 (default) | Balanced motion + adherence |
| Truck / product hero | 0.7 | Strict adherence to preserve branding |
| Branded transitions | 0.7 | Preserve specific visual elements |

## Camera Control

**AIMLAPI supports only `"simple"` type** with a numeric config object. Named presets (`"down_back"`, `"forward_up"`, etc.) appear in fal.ai/PiAPI docs but are NOT available on AIMLAPI — do not use them.

All values range -10 to 10. Recommended for cinematic work: 2-5.

| Shot Type | Config | Notes |
|-----------|--------|-------|
| Gentle push-in | `zoom: -2` or `-3` | Emotional close-ups, intimacy |
| Slow pull-back reveal | `zoom: 2` or `3` | Reveals environment |
| Product orbit | `tilt: 3` to `5` | Moderate rotation around subject |
| Crane up | `vertical: 3, pan: -2` | Rise with slight downward angle |
| Lateral tracking | `horizontal: 3` to `5` | Smooth side tracking |
| Static (prompt-driven) | All zeros | Use prompt for micro-motion only |

**Rules:** Max 2 simultaneous movements. Values 7-10 are dramatic but unstable. Camera control overrides prompt-based camera direction — use one or the other.

## Negative Prompt Templates

### Universal Baseline (ALWAYS include ALL)

```
blurry, distorted, low quality, jittery, flickering, morphing faces, warping, deformed hands, extra fingers, sliding feet, identity drift, watermark, camera shake, inconsistent lighting, plastic skin, cartoonish, color shift
```

### Add for Character Shots

```
face distortion, unnatural skin texture, floating limbs, breathing movement, body sway, weight shifting, expression change, mood shift
```

### Add for Truck/Product Shots

```
vehicle movement, driving, rolling, ghost driving, text morphing, label warping, geometry distortion, reflection artifacts, surface inconsistency
```

### Add for Camera Movement Shots

```
camera drift, sudden zooms, background shifting, unstable details, background morphing
```

## Known Failure Patterns and Prevention

### Ghost Driving (Truck Movement) — HIGHEST PRIORITY

Triple-lock approach:

1. **Prompt constraint:** ALWAYS include "truck remains completely stationary, no vehicle movement"
2. **Negative prompt:** ALWAYS include "vehicle movement, driving, rolling, ghost driving, sliding vehicle"
3. **Static mask (nuclear option):** White pixels = freeze, black = allow motion. Pass as `static_mask` parameter.
4. **Tail image:** Use identical start/end frame via `tail_image_url` to force stationarity.

See `kling-truck-prompting.md` for the dedicated truck shot workflow.

### Breathing Artifacts

NEVER use: "breathing", "weight shift", "subtle body movement", "subtle natural movement"
- For standing: "maintains exact posture, no body sway"
- Negative: "breathing movement, chest expansion, body sway, weight shifting"

### Expression Changes

- Add "maintains exact expression, no expression changes" for static expression shots
- For intentional changes, STAGE: "neutral → eyebrows lift → eyes widen → smile forms"
- Negative: "sudden expression change, mood shift, grimacing"

### Color Shifts

- NEVER include lighting descriptions in I2V prompts (image already has lighting)
- Add "lighting remains consistent throughout"
- Use cfg_scale 0.7 for branded shots
- Negative: "color shift, lighting change, exposure drift"

### Hand/Finger Stability

- ALWAYS anchor hands to objects: "fingers grip the box edge firmly"
- Medium shots safer than extreme close-ups
- Negative: "extra fingers, deformed hands, floating limbs"

### Foot Grounding

- Describe heel-to-toe: "each step lands heel-first, then rolls forward"
- For standing: "feet remain planted on ground"
- Negative: "sliding feet, floating, stiff legs, gliding"

## Shot-Type Presets

### Establishing Shot
```python
cfg_scale=0.4, duration="5",
camera={"zoom": 2, "vertical": 1},
prompt="Slow pull-back revealing full street scene. Ambient leaves drift gently in breeze. All vehicles and buildings remain stationary. Lighting remains perfectly consistent throughout. Motion eases to stop.",
negative_prompt="jittery, flickering, inconsistent lighting, morphing, camera shake, blurry, vehicle movement, ghost driving, background shifting, color shift"
```

### Character Close-Up
```python
cfg_scale=0.5, duration="5",
camera={"zoom": -2},
prompt="Subject blinks once naturally. Slight confident smile forms gradually. Hair moves gently. Maintains exact posture, no body sway. Background completely static. Lighting consistent. Expression settles.",
negative_prompt="face distortion, morphing faces, identity drift, breathing movement, body sway, expression change, extra fingers, plastic skin, flickering, sliding feet, color shift"
```

### Truck/Product Hero
```python
cfg_scale=0.7, duration="5",
camera={"tilt": 3},
prompt="Slow camera orbit around truck. Light reflections glide gently across surface. Branding text stays perfectly sharp and stable. Truck completely stationary, no vehicle movement. Foreground leaves drift subtly. Motion gradually eases to stop.",
negative_prompt="vehicle movement, driving, rolling, ghost driving, text morphing, label warping, geometry distortion, reflection artifacts, blurry, flickering, color shift, jittery, inconsistent lighting"
```

### Walking/Action
```python
cfg_scale=0.5, duration="5",
camera={"horizontal": 3},
prompt="Man walks forward with natural stride, each step lands heel-first then rolls forward. Arms swing naturally. Coat fabric sways with movement. Steps grounded with visible weight transfer. Movement eases to gentle stop.",
negative_prompt="sliding feet, floating limbs, identity drift, jittery, morphing faces, extra fingers, camera shake, breathing artifacts, robotic movement"
```

## Duration Strategy

| Complexity | Optimal Duration | Notes |
|------------|-----------------|-------|
| Simple (single subject) | Up to 10s | Full coherence maintained |
| Medium (multiple elements) | 6-8s | Sweet spot |
| Complex (multiple subjects) | 5s | Chain clips in post |

**Default to 5 seconds.** Cost scales linearly with duration.

## All Available Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| model | string | required | See model strings above |
| image_url | string | required | URL or base64. Min 300x300, max 10MB |
| prompt | string | required | Motion description only, max 2500 chars |
| duration | int | 5 | 3-15 seconds |
| aspect_ratio | string | "16:9" | "16:9", "9:16", "1:1" |
| generate_audio | bool | true | **ALWAYS set false** |
| cfg_scale | float | 0.5 | 0-1, prompt adherence |
| negative_prompt | string | "" | Max 2500 chars |
| tail_image_url | string | — | End frame for transitions. **Incompatible with Multi-Prompting.** Same image = forces stationarity. |
| camera_control | object | — | Named preset OR simple config (not both). See camera control section. |
| elements | array | — | Character reference images for Subject Binding. Up to 4 refs per element. |
| static_mask_url | string | — | White=freeze, black=allow motion. **Must match source image aspect ratio exactly.** PNG/JPG/WEBP, max 10MB. |
| dynamic_masks | array | — | Motion brush paths. Up to 6 groups. See dynamic_masks section below. |

## Elements (Subject Binding) — Exact AIMLAPI Structure

Pass reference images to keep a character's face consistent across clips. **No `face_weight` parameter exists on AIMLAPI** — adherence is implicit in reference image quality and count.

```python
"elements": [
    {
        "frontal_image_url": "https://cdn.example.com/character_front.png",
        "reference_image_urls": [
            "https://cdn.example.com/character_3quarter.png",
            "https://cdn.example.com/character_profile.png"
        ]
    }
]
```

**Requirements for reference images:**
- Frontal: clear face, no occlusion, neutral expression
- References: 2-3 different angles (3/4, profile, full body)
- Resolution: 1024×1024+ preferred; min 300×300
- Background: solid (white or grey preferred)
- Lighting: consistent across all angles
- Max 4 elements (characters) per call

**Note:** CLAUDE.md refers to "Subject Binding face adherence 80-90" — this describes the quality target to achieve via reference image quality, not an API parameter value.

## Dynamic Masks — Exact Structure

Direct motion to specific image regions. Up to 6 mask groups per call. Each region uses a fixed RGB color and an array of (x, y) trajectory coordinates.

**Fixed color assignments (must match exactly):**

| Index | RGB | Hex |
|-------|-----|-----|
| 1 | rgb(114, 229, 40) | Green |
| 2 | rgb(171, 105, 255) | Purple |
| 3 | rgb(0, 170, 255) | Cyan |
| 4 | rgb(240, 38, 173) | Pink |
| 5 | rgb(255, 225, 29) | Yellow |
| 6 | rgb(255, 34, 0) | Red |

```python
"dynamic_masks": [
    {
        "mask": "https://cdn.example.com/mask_region1.png",  # Green pixels = region 1
        "trajectories": [
            {"x": 512, "y": 300},   # Start point
            {"x": 514, "y": 296},   # Intermediate (minimum 10 points recommended)
            {"x": 512, "y": 290},   # End point
        ]
    }
]
```

**Coordinate system:** Origin (0,0) top-left; x-axis right; y-axis down. Floating-point coordinates allowed. Minimum 2 points; 10+ recommended for smooth motion.

**static_mask_url notes:**
- Must match source image aspect ratio exactly — task fails otherwise
- Must also match dynamic_masks image resolution if both are used
- Supported: PNG/JPG/WEBP, max 10MB

## Error Handling

- **403 (out of credits):** STOP immediately. Notify owner via Telegram.
- **404 (model not found):** Check model string spelling.
- **Timeout:** Retry once with 30s timeout, then STOP.
- **Generation failed:** Log failure. Do NOT auto-retry (costs credits).

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
|-----------|-----------|----------|
| Establishing / B-roll | 0.4 | Creative interpretation acceptable |
| Character movement | 0.5 (default) | Balanced motion + adherence |
| Truck / product hero | 0.7 | Strict adherence to preserve branding |
| Branded transitions | 0.7 | Preserve specific visual elements |

## Motion Strength Guidelines

`motion_strength` (0–1) controls how aggressively the model animates. Low values = stable/frozen; high values = aggressive action. **Omit the parameter to use the model default** — do not set it unless you have a specific reason.

| Shot Type | motion_strength | Notes |
|-----------|----------------|-------|
| Stationary truck (primary) | 0.3–0.4 | Prevents physics artifacts on rigid objects |
| Character face close-up | 0.3 | Micro-motion only — blink, hair |
| Character walking / action | 0.5–0.6 | Natural movement range |
| Establishing / B-roll (no character) | Omit | Let model default drive environment motion |
| Aggressive action shot | 0.7–1.0 | Rarely needed; risks jitter above 0.8 |

**Interaction with cfg_scale:** These parameters are NOT redundant. `cfg_scale` controls how strictly the model follows the TEXT prompt; `motion_strength` controls the QUANTITY of motion regardless of prompt adherence. High cfg_scale + high motion_strength = lots of motion rigidly following prompt. Low cfg_scale + low motion_strength = minimal, freely interpreted motion. For truck shots use `cfg_scale 0.7 + motion_strength 0.3` — maximum prompt control + minimum motion budget.

**CAUTION — parameter name unverified:** `motion_strength` by this exact name is not confirmed in the official Kuaishou Kling v3 I2V API schema (as of May 2026 research). It appears in some third-party wrappers and UI sliders but may be a wrapper abstraction. If AIMLAPI returns a parameter error, omit `motion_strength` and rely on `cfg_scale` + prompt anchors for motion control. Verify against AIMLAPI's live schema before relying on it.

## Camera Control

**camera_control.type options:**

| Type | Description | AIMLAPI Status |
|------|-------------|---------------|
| `"simple"` | Custom config via horizontal/vertical/pan/tilt/roll/zoom values | **CONFIRMED — use this** |
| `"down_back"` | Camera descends and pulls backward | **UNVERIFIED on AIMLAPI** (Kling base API only) |
| `"forward_up"` | Camera moves forward and tilts upward | **UNVERIFIED on AIMLAPI** (Kling base API only) |
| `"right_turn_forward"` | Camera rotates right while moving forward | **UNVERIFIED on AIMLAPI** (Kling base API only) |
| `"left_turn_forward"` | Camera rotates left while moving forward | **UNVERIFIED on AIMLAPI** (Kling base API only) |

**Use `"simple"` for ALL AIMLAPI calls — it is the only confirmed type.** Named presets are documented in the base Kling API (klingai.com) but do NOT pass them to AIMLAPI until tested. AIMLAPI may silently ignore or error on unknown preset names.

**Simple config:** all values range -10 to 10. Recommended for cinematic work: 2-5. **Only ONE config value should be non-zero at a time** — the official Kling API spec is explicit about this constraint. Setting multiple non-zero values simultaneously is undefined behavior.

```python
"camera_control": {
    "type": "simple",
    "config": {
        "horizontal": 0, "vertical": 0, "pan": 0,
        "tilt": 3, "roll": 0, "zoom": 0
    }
}
```

| Shot Type | Config | Notes |
|-----------|--------|-------|
| Gentle push-in | `zoom: -2` or `-3` | Emotional close-ups, intimacy |
| Slow pull-back reveal | `zoom: 2` or `3` | Reveals environment |
| Product orbit | `tilt: 3` to `5` | Moderate rotation around subject |
| Crane up | `vertical: 3, pan: -2` | Rise with slight downward angle |
| Lateral tracking | `horizontal: 3` to `5` | Smooth side tracking |
| Static (prompt-driven) | All zeros | Use prompt for micro-motion only |

**Rules:** Only 1 simultaneous movement (one non-zero value). Values 7-10 are dramatic but unstable. Camera control overrides prompt-based camera direction — use one or the other.

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
| Simple (single subject) | Up to 15s | v3 supports 15s max; coherence holds for single-subject |
| Medium (multiple elements) | 6-8s | Sweet spot |
| Complex (multiple subjects) | 5s | Chain clips in post |

**Default to 5 seconds.** Cost scales linearly with duration.

## All Available Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| model | string | required | See model strings above |
| image_url | string | required | URL or base64. Min 300x300, max 10MB |
| prompt | string | required | Motion description only, max 2500 chars. Reference elements as `@Element1`, `@Element2`, etc. |
| duration | int | 5 | 3-15 seconds |
| aspect_ratio | string | "16:9" | "16:9", "9:16", "1:1" |
| generate_audio | bool | true | **ALWAYS set false** |
| cfg_scale | float | 0.5 | 0-1, prompt adherence |
| motion_strength | float | — | 0-1. Lower = less motion/more stable (0.3-0.4 for stationary subjects). Higher = more aggressive motion (0.8-1.0). Omit for default. |
| negative_prompt | string | "" | Max 2500 chars |
| tail_image_url | string | — | End frame for transitions. **Incompatible with multi_prompt.** Same image = forces stationarity. |
| camera_control | object | — | Named preset OR simple config (not both). See camera control section. |
| elements | array | — | Character reference images for Subject Binding. Max 3 elements per I2V call. **Must be referenced as `@Element1` etc. in prompt.** |
| static_mask_url | string | — | White=freeze, black=allow motion. **Must match source image aspect ratio exactly.** PNG/JPG/WEBP, max 10MB. |
| dynamic_masks | array | — | Motion brush paths. Up to 6 groups. See dynamic_masks section below. |
| multi_prompt | array | — | Multi-shot prompting (up to 6 shots) — **AIMLAPI parameter name**. Base Kling API calls this `guidances`. **Incompatible with tail_image_url.** Main `prompt` must be empty when used. See Multi-Shot section. |

## Elements (Subject Binding) — Exact AIMLAPI Structure

Pass reference images to keep a character's face consistent across clips. **No `face_weight` or `face_adherence` numeric parameter exists on AIMLAPI** — adherence is entirely driven by reference image quality and count.

### Image-based element (standard I2V)

```python
"elements": [
    {
        "frontal_image_url": "https://cdn.example.com/character_front.png",
        "reference_image_urls": [
            "https://cdn.example.com/character_3quarter.png",
            "https://cdn.example.com/character_profile.png",
            "https://cdn.example.com/character_profile_left.png"  # 3-4 angles preferred
        ]
    }
]
```

### Video-based element (when a source clip exists)

```python
"elements": [
    {
        "video_url": "https://cdn.example.com/character_reference_clip.mp4"
    }
]
```

### Referencing elements in the prompt — REQUIRED

After defining elements, you **must** reference them in the prompt using `@Element1`, `@Element2` etc. (positional, 1-indexed). Without the @reference, the element binding has no effect.

```
"prompt": "@Element1 walks forward carrying a box, confident stride..."
```

**Requirements for image reference images:**
- Frontal: clear face, no occlusion, neutral expression — this is the identity anchor
- References: 3-4 different angles (front, 3/4, side profile, back) — 4 angles gives model a 3D sense of identity
- Resolution: upscale to **1024×1024** before upload (min 300×300); higher resolution = stronger identity signal
- Background: solid white or grey — patterned backgrounds bleed into identity encoding
- Lighting: even, no harsh shadows — shadow on face degrades facial geometry
- Expression: neutral base image required; expression variants are optional additions
- **Max 3 elements per I2V call** (not 4 — confirmed across multiple sources)
- **More refs ≠ better**: 1-4 focused images optimal. More than 4 confuses the model and weakens binding
- **frontal_image_url is mandatory** — reference_image_urls alone (without frontal) will not bind correctly
- **Pose matters**: simple neutral poses (standing, arms at sides) produce far less identity drift than complex poses or strong non-frontal angles. Use complex reference poses only as supplemental refs, not as the frontal anchor.

**Note:** CLAUDE.md refers to "Subject Binding face adherence 80-90" — this describes the quality target to achieve via reference image quality, not an API parameter value.

## Multi-Shot Prompting (multi_prompt on AIMLAPI)

Kling v3 supports generating up to 6 sequential shots in one API call. **On AIMLAPI the parameter is `multi_prompt` (not `guidances` — that is the base Kling API name).** Confirmed available for T2V; I2V multi-shot works by combining a start frame with per-shot prompts.

**Constraints:**
- Main `prompt` field MUST be empty when `multi_prompt` is used
- `tail_image_url` is INCOMPATIBLE with multi-shot — omit it
- Total video duration = sum of all shot durations (max 15s total)
- Each shot minimum duration: **3 seconds** — do not set individual shot durations below 3s
- Each entry takes `prompt` and `duration` — no `index` field required on AIMLAPI

```python
"prompt": "",  # MUST be empty
"multi_prompt": [
    {"prompt": "@Element1 walks to the truck, confident stride", "duration": 5},
    {"prompt": "@Element1 loads a box into the truck, smooth motion", "duration": 5},
    {"prompt": "Truck parked on street, environment settling, motion eases to stop", "duration": 5}
]
```

**If AIMLAPI returns a parameter error:** fall back to single-prompt clips and chain in post via FFmpeg. Do NOT retry multi_prompt more than once per session — it costs credits on failure too.

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

**Coordinate system:** Origin (0,0) top-left; x-axis right; y-axis down. Floating-point coordinates allowed. Minimum 2 points; 10+ recommended for smooth motion. **Mask image background must be fully transparent (alpha=0), not black** — uncolored regions must have alpha=0; colored regions must be fully opaque. Use PNG with alpha channel.

**static_mask_url notes:**
- Must match source image aspect ratio exactly — task fails otherwise
- Must also match dynamic_masks image resolution if both are used
- Supported: PNG/JPG/WEBP, max 10MB

## Motion Control V2V (Video-to-Video Motion Transfer)

Separate from I2V. Kling v3 Motion Control animates a character image to match the motion in a reference video (e.g., a royalty-free walking clip). Useful for complex walking or action shots where you have a motion reference.

**AIMLAPI availability:** Confirmed for v2.6 (`klingai/video-v2-6-pro-motion-control`). Kling v3 Motion Control released March 5, 2026 and is available on WaveSpeedAI, Replicate, and fal.ai — but **NOT yet confirmed on AIMLAPI**. Continue using v2.6 string on AIMLAPI; do a canary test before switching if it appears in the model list.

**Key parameter:** `character_orientation`
- `"video"` — output character follows orientation from reference video (better for complex multi-directional motion, max 30s output)
- `"image"` — output character keeps orientation from source image (better for camera-led shots, max 10s)

**Framing rule:** Half-body image → pair with half-body motion reference. Full-body image → pair with full-body reference. Mismatch degrades motion transfer quality.

**When to use:** Walking shots where motion prompting alone produces robotic or sliding feet artifacts. Requires a royalty-free motion reference clip (3-30s, clear body movement, moderate speed).

## Kling O3 — Future Watch (Not Yet on AIMLAPI)

Kling O3 (Omni, released Feb 2026) is the premium reasoning tier above v3 Pro. **Confirmed NOT on AIMLAPI as of May 2026** — O3 migrated to fal.ai in April 2026 and is also on PiAPI and Atlas Cloud, but not AIMLAPI. Farouq AIMLAPI-only directive means O3 cannot be used until it appears there.

**O3 advantages worth monitoring:** Multi-image element building, multi-character coreference (3+ characters), 3D Spacetime Joint Attention for stronger physics and consistency, reference-to-video workflow. If O3 becomes available on AIMLAPI, evaluate it for character-heavy clips where v3 Pro produces identity drift.

**BREAKING CHANGE for O3:** When O3 is added, `cfg_scale` and `negative_prompt` are BOTH REMOVED — O3 handles them internally. Every gen script using these parameters will break. Update scripts before switching.

## Error Handling

- **403 (out of credits):** STOP immediately. Notify owner via Telegram.
- **404 (model not found):** Check model string spelling.
- **Timeout:** Retry once with 30s timeout, then STOP.
- **Generation failed:** Log failure. Do NOT auto-retry (costs credits).

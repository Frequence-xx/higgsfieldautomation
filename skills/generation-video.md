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
| Kling O1 Reference-to-Video | `klingai/video-o1-reference-to-video` | 1080p (9:16) | **$0.56** |
| Kling v3 Standard I2V | `klingai/video-v3-standard-image-to-video` | 720x1280 (9:16) | **$1.09** |
| Kling v3 Pro I2V | `klingai/video-v3-pro-image-to-video` | **1080x1920 (9:16)** | **$1.46** |

**Use Standard for iteration/testing, Pro for final output. O1 Reference-to-Video is the cheapest option for character shots requiring multi-image identity lock — see Kling O1 section below.**

**Confirmed AIMLAPI Kling model roster (June 2026):** Kling 2.6 Pro, Kling v3 Standard I2V, Kling v3 Pro I2V, Kling O1 Reference-to-Video, Kling O1 Video-to-Video Reference, Kling O1 Video-to-Video Edit, Kling 2.6 Pro Motion Control. **NOT on AIMLAPI:** Kling O3/Omni, Kling v3 Motion Control, Kling 4K (unverified).

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

**v3 range: 0.0–1.0 only** (v1.x allowed up to 2.0 — do not exceed 1.0 on v3, confirmed May 2026).

| Shot Type | cfg_scale | Reasoning |
|-----------|-----------|----------|
| Establishing / B-roll | 0.4 | Creative interpretation acceptable |
| Character movement | 0.5 (default) | Balanced motion + adherence |
| Truck / product hero | 0.7 | Strict adherence to preserve branding |
| Branded transitions | 0.7 | Preserve specific visual elements |
| Character multi-shot sequence | 0.8 | Tighter identity lock across multi-shot; documented in Kling API examples |

**Upper bound note:** 0.8 is the practical maximum for character shots. Values approaching 1.0 over-constrain motion and produce stiff, jittery output. Use 0.8 only for multi-shot sequences where identity consistency matters more than motion fluidity.

## Motion Strength — NOT a Standard I2V Parameter

**`motion_strength` does NOT exist in the standard Kling I2V schema (confirmed May 2026).** The Griptape Kling library (authoritative native API wrapper) documents all I2V parameters exhaustively — `motion_strength` is absent. It appears only in the Motion Control (V2V) variant (`video-v2.6-pro-motion-control`). Do NOT pass it in standard I2V calls — it will be ignored or return a parameter error.

**Control motion quantity in standard I2V via:**
- `cfg_scale` — how strictly the model follows the prompt (0.5 default; 0.7 for branded/truck shots)
- Prompt anchors — "slowly", "gently", explicit endpoints ("eases to stop")
- Negative prompt — "jittery", "erratic motion"

For truck shots: `cfg_scale: 0.7` + prompt "no vehicle movement" + negative "vehicle movement, ghost driving" is the correct substitute for what was previously listed as `motion_strength: 0.3`.

## Camera Control

**camera_control.type options:**

| Type | Description | AIMLAPI Status |
|------|-------------|---------------|
| `"simple"` | Custom config via horizontal/vertical/pan/tilt/roll/zoom values | **CONFIRMED — use this** |
| `"(Auto)"` | Model auto-selects camera movement; use when motion is desired but direction doesn't matter | **CANARY on AIMLAPI — confirmed in Griptape native wrapper (May 2026)** |
| `"down_back"` | Camera descends and pulls backward | **CONFIRMED on Kling API, ComfyUI, Griptape, fal.ai v3, WaveSpeedAI v3, Replicate v3, Kie AI — CANARY on AIMLAPI wrapper** |
| `"forward_up"` | Camera moves forward and tilts upward | **CONFIRMED on Kling API, ComfyUI, Griptape, fal.ai v3, WaveSpeedAI v3, Replicate v3, Kie AI — CANARY on AIMLAPI wrapper** |
| `"right_turn_forward"` | Camera rotates right while moving forward | **CONFIRMED on Kling API, ComfyUI, Griptape, fal.ai v3, WaveSpeedAI v3, Replicate v3, Kie AI — CANARY on AIMLAPI wrapper** |
| `"left_turn_forward"` | Camera rotates left while moving forward | **CONFIRMED on Kling API, ComfyUI, Griptape, fal.ai v3, WaveSpeedAI v3, Replicate v3, Kie AI — CANARY on AIMLAPI wrapper** |

**Use `"simple"` for ALL AIMLAPI calls until named presets are canary-tested.** Named presets are confirmed across 6+ platforms specifically for Kling v3 (not just v1/v2) as of May 2026 — high confidence they will work on AIMLAPI, but one canary call per preset is still required before production use.

**Simple config:** all values range -10 to 10. Recommended for cinematic work: **1-2** (Kling 3 Pro guides confirm lower values = cleaner, more stable motion; values ≥3 risk instability). **Only ONE config value should be non-zero at a time** — the official Kling API spec is explicit about this constraint. Setting multiple non-zero values simultaneously is undefined behavior.

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
| Gentle push-in | `zoom: -1` or `-2` | Emotional close-ups, intimacy |
| Slow pull-back reveal | `zoom: 1` or `2` | Reveals environment |
| Product orbit | `tilt: 1` to `2` | Slow rotation around subject |
| Crane up | `vertical: 1` to `2` | Smooth upward rise |
| Lateral tracking | `horizontal: 1` to `2` | Smooth side tracking |
| Static (prompt-driven) | All zeros | Use prompt for micro-motion only |

**Rules:** Only 1 simultaneous movement (one non-zero value). Values ≥3 risk instability; 7-10 are rarely usable. Camera control overrides prompt-based camera direction — use one or the other.

## Negative Prompt Templates

### Universal Baseline (ALWAYS include ALL)

```
blurry, distorted, low quality, jittery, flickering, morphing faces, warping, deformed hands, extra fingers, sliding feet, identity drift, watermark, camera shake, inconsistent lighting, plastic skin, cartoonish, color shift
```

### Add for Character Shots

```
face distortion, unnatural skin texture, floating limbs, breathing movement, body sway, weight shifting, expression change, mood shift
```

### Add for Uniformed Character Shots (Snelverhuizen crew)

Lock the crew uniform against drift. Add these to character shots where uniform identity matters:

```
outfit change, clothing color shift, missing logo, uniform drift, shirt color change, jeans color change, sneaker design change, logo disappear, brand color change
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
| motion_strength | — | — | **Not a standard I2V parameter.** Motion Control (V2V) variant only. Omit from all I2V calls. |
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
- **Clothing texture: solid colors and simple fabrics prevent outfit morphing during motion.** Patterned or printed clothing in reference images increases the risk of fabric "morphing" or color drift mid-clip. For the Snelverhuizen crew (black crewneck + orange logo), solid colors are ideal — this is already the correct uniform design.
- **Max 3 elements per I2V call** (not 4 — confirmed across multiple sources)
- **reference_image_urls are STRONGLY RECOMMENDED, not optional** — multiple sources (May 2026) indicate that passing frontal_image_url alone without reference_image_urls may trigger a model error. Minimum 2 total images per element (frontal + at least 1 reference angle).
- **More refs ≠ better**: 2-4 focused images optimal. More than 4 confuses the model and weakens binding
- **frontal_image_url is mandatory** — reference_image_urls alone (without frontal) will not bind correctly
- **Pose matters**: simple neutral poses (standing, arms at sides) produce far less identity drift than complex poses or strong non-frontal angles. Use complex reference poses only as supplemental refs, not as the frontal anchor.

**Prompt budget:** Each `@ElementN` reference consumes approximately 37 characters of the 2500-char prompt limit. With 3 elements, reserve ~111 chars for references before writing motion instructions.

**Motion Control limit:** When using Motion Control V2V, max 1 element is supported (vs 3 for standard I2V). Element binding in Motion Control also requires `character_orientation: "video"`.

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

**AIMLAPI availability:** Only v2.6 is confirmed (`klingai/video-v2-6-pro-motion-control`). Kling v3 Motion Control (Standard + Pro) released March 5, 2026 and is confirmed on WaveSpeedAI (`kwaivgi/kling-v3.0-pro/motion-control`), Replicate (`kwaivgi/kling-v3-motion-control`), fal.ai, Kie AI, ModelsLab (`kling-v3-motion-control`), MindStudio, EachLabs, and Media.io — but **NOT on AIMLAPI as of June 2026** (AIMLAPI docs index still shows only v2.6-pro/motion-control). Expected model strings when added: `klingai/video-v3-standard-motion-control` and `klingai/video-v3-pro-motion-control`. Farouq AIMLAPI-only directive means v3 Motion Control is blocked until it appears on AIMLAPI.

**Key parameter:** `character_orientation`
- `"video"` — output character follows orientation from reference video (better for complex multi-directional motion, max 30s output)
- `"image"` — output character keeps orientation from source image (better for camera-led shots, max 10s)

**Element limit:** Max 1 element per Motion Control call. Element binding requires `character_orientation: "video"` — image orientation mode does not support elements.

**Framing rule:** Half-body image → pair with half-body motion reference. Full-body image → pair with full-body reference. Mismatch degrades motion transfer quality.

**When to use:** Walking shots where motion prompting alone produces robotic or sliding feet artifacts. Requires a royalty-free motion reference clip (3-30s, clear body movement, moderate speed).

## Kling O1 Series — Available on AIMLAPI (Confirmed May 2026)

Three Kling O1 models are live on AIMLAPI. All use the `/v2/video/generations` endpoint.

| Model | AIMLAPI String | Cost | Primary Use |
|-------|---------------|------|------------|
| O1 Reference-to-Video | `klingai/video-o1-reference-to-video` | **$0.112/s ≈ $0.56/5s** | Multi-image → video with character lock |
| O1 Video-to-Video Reference | `klingai/video-o1-video-to-video-reference` | ~$0.111/s | Apply reference style/identity to existing footage |
| O1 Video-to-Video Edit | `klingai/video-o1-video-to-video-edit` | ~$0.111/s | Text-guided editing of existing video |

### O1 Reference-to-Video — Key Parameters

```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "klingai/video-o1-reference-to-video",
    "prompt": "The crew member walks confidently toward the truck carrying a box, natural stride",
    "image_list": [                          # 1–7 reference images (identity input)
        "https://cdn.example.com/crew/front.png",
        "https://cdn.example.com/crew/three_quarter.png",
        "https://cdn.example.com/crew/profile.png"
    ],
    "duration": 5,
    "aspect_ratio": "9:16",
    "generate_audio": False,
}, headers=headers, timeout=30)
```

**`image_list` vs `elements`:** O1 reference-to-video uses `image_list` (array, 1–7 images) as the identity input — this is different from the `elements` structure used by v3 Pro. The character-consistency.md Step 3 shows `elements` syntax for this model — canary test both; `image_list` is confirmed from AIMLAPI docs. **Do NOT assume `elements` syntax transfers from v3 Pro without a canary test.**

### O1 Video-to-Video Edit — Additional Parameters

- `video_url` (required): source video URL
- `image_list` (optional, 1–7): additional reference images
- `elements` (optional, max 4): character elements — max 4 (vs 3 for v3 Pro)
- `keep_audio` (bool, default false): preserve original audio

### O1 Cost vs v3 — When to Use

| Scenario | Model | 5s Cost | Savings |
|----------|-------|---------|---------|
| Draft character iteration | O1 Reference-to-Video | **$0.56** | 49% vs v3 Standard |
| Final character shot | v3 Pro | $1.46 | — |
| Multi-image identity lock (draft) | O1 Reference-to-Video | **$0.56** | 61% vs v3 Pro |

**Quality note:** v3 Pro has a slight edge for maintaining character identity across multi-shot sequences. O1 Reference-to-Video is the better cost choice for draft iterations where prompt tuning is still ongoing. Switch to v3 Pro for final approved takes per CLAUDE.md routing matrix. Do not change the routing matrix in CLAUDE.md without owner approval.

### O1 CANARY CHECKLIST (before production use)

- [ ] Test `image_list` parameter: 3 reference images → verify identity locked in output
- [ ] Test `elements` syntax — does O1 accept it or only `image_list`?
- [ ] Run InsightFace buffalo_l cosine similarity vs v3 Pro baseline on same refs
- [ ] Confirm 9:16 aspect ratio renders correctly (1080p)
- [ ] Confirm `generate_audio: false` accepted (no surcharge)

---

## Kling O3 — Future Watch (Not Yet on AIMLAPI)

Kling O3 (VIDEO 3.0 Omni, released Feb 5, 2026) is the premium tier above v3 Pro. **Confirmed NOT on AIMLAPI as of June 2026** — O3 (Replicate model string: `kwaivgi/kling-v3-omni-video`; expected AIMLAPI string when added: `klingai/video-v3-omni`) is available on fal.ai, Replicate, PiAPI, Atlas Cloud ($0.15/s), MindStudio, Vidguru, Picsart, and Runware (including a dedicated O3 4K variant) — but not AIMLAPI docs index. Farouq AIMLAPI-only directive means O3 cannot be used until it appears there.

**O3 advantages worth monitoring:**
- Multi-image element building: up to **7 reference images** per call (vs. 3 for v3 Pro)
- Combined input: up to **4 images + 1 reference video** in a single call (O3-exclusive)
- Multi-character coreference (3+ characters)
- **Voice binding from video element refs** — upload a clip to lock both the character's appearance AND voice tone; every time that character speaks, the voice stays consistent
- 3D Spacetime Joint Attention for stronger physics and consistency
- Native audio generation with lip-sync in 5 languages (EN, ZH, JA, KO, ES)

If O3 becomes available on AIMLAPI, evaluate it for character-heavy clips where v3 Pro produces identity drift.

**BREAKING CHANGE for O3 (confirmed):** When O3 is added, `cfg_scale` and `negative_prompt` are BOTH REMOVED — O3 handles them internally. Avoidance instructions must be **baked into the positive prompt** (e.g., "truck firmly stationary, wheels locked, branding sharp" instead of a negative prompt). Every gen script using these parameters will break on O3. Update scripts before switching.

## Kling 3.0 4K Variant — Future Watch (Not Yet Confirmed on AIMLAPI)

Kling 3.0 supports native 4K output (3840×2160, up to 60fps). **Released April 23, 2026.**

**How 4K works (native Kling API):** The native Kling API accepts `"mode": "4k"` as a top-level parameter. However, third-party API wrappers implement 4K differently: **fal.ai exposes it as a dedicated model endpoint** (`fal-ai/kling-video/v3/4k/image-to-video`), not a parameter toggle. Runware similarly exposes a separate "Kling VIDEO O3 4K API" model. This means AIMLAPI may use either a separate model string or the `mode` parameter — do NOT assume either approach without a canary test.

**4K I2V supported features:** single-shot (start frame only), multi-shot, start+end frame, element control with video character and multi-image inputs. Duration range: 3–15 seconds (same as pro mode). Motion Control and voice are NOT available in 4K mode.

**AIMLAPI status:** UNVERIFIED. Multiple sources describe 4K as a "mode toggle" (not a separate endpoint), which makes method 1 more likely. Two possible access methods — (1) pass `"mode": "4k"` alongside standard I2V parameters — **try this first, most likely to be correct**; (2) use a dedicated model string (e.g., `klingai/video-v3-4k-image-to-video`) — fal.ai uses this approach, AIMLAPI may not. Test method 1 first (zero extra cost if rejected); if AIMLAPI returns an error, check docs index for a 4K model string. Fall back to Pro 1080p if neither works. Use for final-delivery hero clips only.

## Error Handling

- **403 (out of credits):** STOP immediately. Notify owner via Telegram.
- **404 (model not found):** Check model string spelling.
- **Timeout:** Retry once with 30s timeout, then STOP.
- **Generation failed:** Log failure. Do NOT auto-retry (costs credits).

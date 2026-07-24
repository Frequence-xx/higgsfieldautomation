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
| Kling v3 Standard Turbo I2V | `klingai/video-v3-standard-turbo-image-to-video` | 720p (9:16) | **$0.73** ($0.146/sec) — Last frame OPTIONAL. ✓ CORRECTED 2026-06-21: Silent video by default in single-clip mode (AIMLAPI docs list `generate_audio` with default=true — ALWAYS pass `false` as safety; strip audio immediately as precaution). CANARY REQUIRED. |
| Kling v3 Standard Turbo T2V | `klingai/video-v3-standard-turbo-text-to-video` | 720p (9:16) | **$0.73** ($0.146/sec) — T2V variant. Same corrected audio behavior. ALWAYS pass `generate_audio: false`. CANARY REQUIRED. |
| **Kling v3 Turbo Pro I2V** | `klingai/video-v3-turbo-pro-image-to-video` | **1080p (9:16)** | **$0.91** ($0.182/sec — AIMLAPI pricing confirmed June 2026) — 37.7% cheaper than v3 Pro. ✓ CORRECTED 2026-06-21: Silent video by default in single-clip mode. ALWAYS pass `generate_audio: false`. Strip audio as safety precaution. CANARY REQUIRED. |
| **Kling v3 Turbo Pro T2V** | `klingai/video-v3-turbo-pro-text-to-video` | **1080p (9:16)** | **$0.91** ($0.182/sec) — ALWAYS pass `generate_audio: false`. CANARY REQUIRED. |
| Kling v3 Standard I2V | `klingai/video-v3-standard-image-to-video` | 720x1280 (9:16) | **$1.09** |
| Kling v3 Standard T2V | `klingai/video-v3-standard-text-to-video` | 720x1280 (9:16) | **$1.09** |
| Kling v3 Pro I2V | `klingai/video-v3-pro-image-to-video` | **1080x1920 (9:16)** | **$1.46** |
| Kling v3 Pro T2V | `klingai/video-v3-pro-text-to-video` | **1080x1920 (9:16)** | **$1.46** |

**Use Standard for iteration/testing, Pro for final output. O1 Reference-to-Video is the cheapest option for character shots requiring multi-image identity lock — see Kling O1 section below.**

**T2V vs I2V pricing:** Native Kling v3 T2V and I2V cost the same per second — AIMLAPI passes through the same rate. T2V with elements/subject binding is useful when no hero frame exists, but our static-first validation funnel almost always produces a hero frame first. Use I2V by default; T2V only when hero frame generation is not feasible.

**PRICING RESOLVED (June 2026):** AIMLAPI Kling v3 Standard = **$0.218/sec = $1.09/5s** (confirmed correct). The $0.084/sec figure causing the previous discrepancy is the **official Kling direct API rate** (kling.ai/dev/pricing) and **fal.ai rate** — NOT AIMLAPI pricing. AIMLAPI charges ~2.6× the native Kling rate for all v3 tiers: Standard $0.218/sec vs $0.084/sec native; Pro $0.291/sec vs $0.112/sec on fal.ai. This atypically high AIMLAPI markup (vs the ~1.3× assumed for most models) is confirmed. The $1.09/5s Standard and $1.46/5s Pro figures in the routing matrix are accurate — no changes needed.

**Confirmed AIMLAPI Kling model roster (July 5, 2026):** Kling 2.6 Pro, Kling v3 Standard I2V, Kling v3 Standard T2V, Kling v3 Pro I2V, Kling v3 Pro T2V, **Kling v3 Standard Turbo I2V, Kling v3 Standard Turbo T2V, Kling v3 Turbo Pro I2V, Kling v3 Turbo Pro T2V** (all launched June 17, 2026 — canary required), Kling O1 Reference-to-Video, Kling O1 Video-to-Video Reference, Kling O1 Video-to-Video Edit, Kling 2.6 Pro Motion Control. **NOT on AIMLAPI:** Kling O3/Omni (`klingai/video-v3-omni` — confirmed absent as of July 3, 2026; the June 17 Turbo launch did NOT bring O3 to AIMLAPI; available on fal.ai, Replicate, Runware, Freepik, Wiro AI, Picsart), Kling v3 Motion Control Standard/Pro (only v2.6 confirmed on AIMLAPI; v3 Motion Control is live on WaveSpeedAI, Eachlabs, Replicate, MindStudio — but not AIMLAPI as of July 3, 2026), Kling 4K (`klingai/video-o3-4k` — officially announced June 12, 2026; Runware-confirmed; AIMLAPI TBD since O3 itself is absent).

**fal.ai naming note:** fal.ai renamed v3 endpoints to `o3` on April 10, 2026, then reversed back to `v3` on May 23, 2026. For v3 Pro on fal.ai, use `fal-ai/kling-video/v3/pro/image-to-video`. For O3/Omni on fal.ai, it's a separate model: `fal-ai/kling-video/o3/standard/image-to-video`. **Kling O3 is NOT on AIMLAPI as of July 3, 2026** — confirmed absent from AIMLAPI docs index. The June 17, 2026 Turbo launch did NOT include O3/Omni on AIMLAPI — only the Turbo tier (Standard Turbo + Turbo Pro) was added. AIMLAPI's own blog post listing Kling models only mentions Kling 2.6 Pro and Kling v3 Pro. Also note: fal.ai Kling v3 Standard pricing ($0.084/sec) is ~2.6× cheaper than AIMLAPI ($0.218/sec) — the AIMLAPI-only mandate is a real cost penalty for Kling Standard tier.

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

**5-part spine (2026 community standard — alternative structure):**

| # | Part | What to specify | Example |
|---|------|-----------------|---------|
| 1 | **Camera** | How the lens behaves (set 3D space first) | "Slow dolly push forward" |
| 2 | **Scene** | Environment + current subject state (reference only) | "through the doorway, crew member standing" |
| 3 | **Action** | Motion arc: start → middle → settled end | "lifts box, pivots right, places it firmly, eases to rest" |
| 4 | **Vibe** | Light quality changes — NOT static description | "golden hour light plays across face" |
| 5 | **Time** | Temporal endpoint + stabilizer | "motion settles, eases to stop" |

Use as a pre-write checklist. Final prompt is still 15-40 words — CSAT is a planning tool, not a template to copy verbatim.

**Optimal length (Kling 3.0, July 2026):** I2V: **40-120 words**. T2V: **80-150 words**. The old 15-40 word guidance applied to Kling v1/v2 — v3's improved instruction following benefits from richer prompt detail. Community data (videoai.me, 2026): short prompts 30-60w average 2.3 rerolls; medium 80-150w is the sweet spot; 200+ w dilutes focus and causes hallucination. For I2V the lower floor (40w) applies because the image handles scene description — motion arc, camera, stationarity anchors, and endpoint need coverage, not appearance.

**Kling v3 I2V motion improvement (confirmed June 2026):** v3 significantly reduces "Ken Burns effect" — the model now produces genuine character/environment animation rather than defaulting to camera panning over a still image. Practical implication: on v3, if you include a character in the hero frame, it WILL attempt to animate them. Use explicit "no body sway, no breathing movement" in negative prompts if you want near-static characters. v1/v2 templates that relied on Ken Burns drift as a fallback will look different on v3.

1. **ONE clear motion per subject** — never give competing actions
2. **Always include a speed modifier** — "slowly", "gently", "smoothly" (unspecified = jitter)
3. **Always include a motion endpoint** — "eases to a gentle stop" (prevents 99% of hangs)
4. **Always specify what stays still** — "background remains static", "truck stays stationary"
5. **Use physical verbs** — "walks", "lifts", "turns" (not abstract "dynamic energy")
6. **Specify body parts** — "hair moves", "fingers grip" (not "person moves")
7. **Describe the temporal arc** — explicitly state beginning → middle → end within the 5s clip. Without this, Kling treats prompts as a frozen moment and generates minimal motion. Example: "starts walking forward → reaches midpoint with confident stride → eases to stop at truck door". (June 2026 finding from community prompt guides.)

### SCALE Framework (Alternative Structured Approach)

A production-tested mnemonic for building complete prompts before writing them:

| Letter | Component | What to specify |
|--------|-----------|----------------|
| **S** | Shot | Camera type + camera movement direction |
| **C** | Character | Who / what is in frame (reference only — image has the visual details) |
| **A** | Action | Motion timeline: what begins → what happens → how it settles |
| **L** | Lighting & Location | Light quality changes (shift, glide) — NOT static description |
| **E** | Extra | Style tags, texture, endpoint anchor |

**Use as a pre-write checklist, not a prompt template.** The final prompt should still be 15-40 words of pure motion instruction — SCALE just ensures you haven't forgotten a layer before writing.

**"Film director" framing (June 2026):** Kling performs best when prompts describe a scene being filmed, not just an image. Think: "this is what my virtual camera crew captures" rather than "this is what the image looks like."

**Active-verb physics triggering (July 2026):** Kling 3.0's physics engine responds to verbs that imply causality. "A glass falls off the table and shatters" triggers physics simulation; "a broken glass on the floor" does not. For motion prompts: use causal action chains ("lifts box → pivots right → places firmly → eases to rest") rather than static state descriptions. This applies both to desired motion AND stationarity (physics-framing the truck as "parking brake engaged, wheels locked and chocked, dead weight at rest" is a physics-engine instruction, not just prose).

**Front-load the camera instruction (July 2026):** Write the camera motion FIRST in the prompt text, even within the CSAT spine. "Slow dolly push forward" at the start outperforms the same phrase buried mid-sentence. The model weighs earlier tokens more heavily — camera sets the spatial frame before action is read.

**Alternative Scene-first ordering (July 2026 community alternative):** Some guides use Scene → Characters → Action → Camera → Audio & Style, arguing that grounding the model in the environment before camera prevents spatial confusion. Both orderings work in practice. Our default remains Camera-first (confirmed stronger by multiple sources) — Scene-first is a valid fallback if Camera-first generates compositional drift.

**Dolly ≠ Zoom: depth layers required (July 2026):** A dolly prompt without foreground, midground, and background elements in the hero frame becomes a zoom instead. The model cannot synthesize depth that isn't in the source image. Check the hero frame: if it's flat (subject against plain wall), use `zoom: -1` in camera_control instead. If you need a true dolly, ensure the hero frame has visible depth layers (street scene, doorway, furniture etc.).

**Micro-detail prompting for Kling 3.0 Pro (July 2026):** Kling 3.0's real breakthrough vs earlier versions is in micro-texture fidelity. Activating it requires explicit texture prompts — generic descriptions like "realistic" do not trigger it. For character close-ups, add physical specifics: "fabric creases on black crewneck, skin texture visible, light catching logo edge, film grain". For product/brand shots: "surface sheen on truck panel, paint texture, subtle light catch on lettering edge". Tactile language outputs tactile video.

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

**fal.ai April–May 2026 API parameter history (AIMLAPI unaffected):** On April 10, 2026 fal.ai temporarily dropped `cfg_scale` and `negative_prompt` when renaming their v3→o3 endpoints. On May 23 they reverted: /v3/ paths restored, `cfg_scale` and `negative_prompt` restored, and `image_url` switched back to `start_image_url`. **AIMLAPI kept `cfg_scale`, `negative_prompt`, and `image_url` throughout.** Do NOT copy fal.ai examples from April–May 2026 into AIMLAPI calls. Also: fal.ai uses `start_image_url`; AIMLAPI uses `image_url` — do not copy-paste between platforms.

## Motion Strength — NOT a Standard I2V Parameter

**`motion_strength` does NOT exist in the standard Kling I2V schema (confirmed May 2026).** The Griptape Kling library (authoritative native API wrapper) documents all I2V parameters exhaustively — `motion_strength` is absent. It appears only in the Motion Control (V2V) variant (`video-v2.6-pro-motion-control`). Do NOT pass it in standard I2V calls — it will be ignored or return a parameter error.

**Control motion quantity in standard I2V via:**
- `cfg_scale` — how strictly the model follows the prompt (0.5 default; 0.7 for branded/truck shots)
- Prompt anchors — "slowly", "gently", explicit endpoints ("eases to stop")
- Negative prompt — "jittery", "erratic motion"

For truck shots: `cfg_scale: 0.7` + prompt "no vehicle movement" + negative "vehicle movement, ghost driving" is the correct substitute for what was previously listed as `motion_strength: 0.3`.

## CRITICAL: Parameter Mutual Exclusivity (Kling v3)

**`tail_image_url`, `static_mask_url` (static_mask), `dynamic_masks`, and `camera_control` are MUTUALLY EXCLUSIVE in Kling v3. Only ONE can be used per API call.** Confirmed across multiple sources (June 2026). Passing more than one will cause API rejection or silent ignore.

**Choose ONE per shot:**
- `static_mask_url` — pixel-level freeze; strongest ghost-driving prevention for truck/stationary shots
- `camera_control` — explicit camera movement; cannot be combined with masks or tail frame
- `dynamic_masks` — motion brush for selective region animation; cannot be combined with others
- `tail_image_url` — end-frame anchoring; weakest stationarity control (allows mid-clip drift); cannot be combined with others

**This replaces the previous Five-Layer Truck Protocol which incorrectly combined all three. See `kling-truck-prompting.md` for the corrected two-template approach.**

---

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

**These 6 types are the COMPLETE API set — "orbit", "crane up", "boom", "pan", "tilt", "stationary", "handheld" are NOT `camera_control.type` API values.** They appear in Kling's UI Inspiration & Presets panel but do NOT map to distinct API type strings (confirmed July 2026 — Griptape README lists only the 6 types above, no orbit/crane/boom). Achieve them via `simple` config (crane up = `vertical: 1-2`, orbit = `tilt: 1-2`, boom = same as crane) or prompt text.

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

**Term ordering matters:** Kling weights earlier terms more heavily than later ones. Put your highest-priority failure prevention terms FIRST. For character shots: face/identity terms first. For truck shots: vehicle movement terms first.

**Native default is weak:** Kling's built-in default is only `"blur, distort, and low quality"`. ALWAYS override with our full custom template — the default provides near-zero protection against ghost driving, breathing artifacts, or identity drift.

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

**Kling 3.0 physics-first model architecture (confirmed June 2026):** Prompt adherence is the LAST priority. Model priority order: Physics → Temporal consistency → Motion quality → Visual fidelity → Prompt adherence. "Stationary truck" is a prompt instruction (lowest priority) — the physics engine can override it. Fix: frame stationarity as physics state using physics-framing language ("parking brake engaged, wheels locked, dead weight at rest on flat level ground") — this speaks to the physics engine directly, not just the text prompt. Static mask (pixel-level freeze) remains the only hard override that operates outside the physics engine.

**`motion intensity 0.1` (Prompt Syntax 2.0, June 2026):** Kling 3.0 responds to numeric motion intensity values embedded in prompt text. Add `"motion intensity 0.1"` literally in the `prompt` string for all truck shots — this targets the physics engine layer directly, the same layer driving ghost driving, and is stronger than prose description alone. Not an API parameter — must appear in the `prompt` string. Does not replace static_mask — use both.

**⚠️ Scale — July 18, 2026 update (SC223):** Earlier guides describe a 0.1–1.0 scale. July 2026 community guides now consistently show a 0–3 scale (examples: 0.4 = arabesque, 0.8 = energetic tracking, 2.8 = sprinting). The 0–3 scale is becoming the community consensus for Kling 3.0. Both scales describe prompt-embedded text, not an API parameter. **Practical implication for our pipeline:** `"motion intensity 0.1"` is the minimum extreme on either scale — use it as-is for truck/near-static shots. Do NOT use values above 1.0 for any Snelverhuizen shot (overkill; extreme action reserved). `camera_control` config values use a separate −10 to +10 range and must NOT be confused with this.

**UPDATED (June 2026):** In Kling v3, `static_mask_url`, `tail_image_url`, and `camera_control` are mutually exclusive — only ONE can be used per call. Previous multi-layer combinations are invalid.

**Strategy A — Maximum stationarity (final delivery shots):**
1. **Prompt constraint:** "stationary truck, parked, engine off, no vehicle movement, no forward creep"
2. **Negative prompt:** "vehicle movement, driving, rolling, ghost driving, sliding vehicle, wheel rotation, truck rocking"
3. **Static mask:** `static_mask_url` — white over entire truck body, black for environment. Strongest protection.
4. **cfg_scale: 0.7** — strict adherence
5. NO camera_control, NO tail_image_url (incompatible with static_mask in v3)

**Strategy B — Cinematic orbit (when camera movement is required):**
1. **Prompt constraint + negative prompt** (same as above)
2. **camera_control** with single non-zero value (e.g., `tilt: 2`)
3. **cfg_scale: 0.7**
4. NO static_mask_url, NO tail_image_url (incompatible with camera_control in v3)

See `kling-truck-prompting.md` for complete templates.

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

### Truck/Product Hero — Strategy A (static_mask, no camera_control)
```python
cfg_scale=0.7, duration="5",
# NO camera_control — incompatible with static_mask_url in Kling v3
static_mask_url=truck_freeze_mask_url,  # White over truck body, black for environment
prompt="Stationary truck, parked, engine off, no vehicle movement. Parking brake fully engaged, wheels locked and chocked, vehicle dead weight at rest on flat level ground. Vehicle remains rigid. Light reflections glide across surface. Branding text stays perfectly sharp. Foreground leaves drift subtly. Motion eases to stop.",
negative_prompt="vehicle movement, driving, rolling, ghost driving, text morphing, label warping, geometry distortion, reflection artifacts, blurry, flickering, color shift, jittery, inconsistent lighting"
```

### Truck/Product Hero — Strategy B (camera_control, no static_mask)
```python
cfg_scale=0.7, duration="5",
camera={"tilt": 2},  # ONE non-zero value. NO static_mask_url in this strategy.
prompt="Slow camera tilt upward. Stationary truck, parked, engine off, no vehicle movement. Parking brake fully engaged, wheels locked and chocked, vehicle dead weight at rest on flat level ground. Vehicle remains rigid. Light reflections glide across surface. Branding text stays perfectly sharp. Camera motion eases to stop.",
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
| tail_image_url / end_image_url | string | — | End frame for transitions. **Native Kling API name: `image_tail` (confirmed from Griptape official wrapper, SC230 July 19, 2026). AIMLAPI v1/v1.6 Pro docs use `end_image_url` (confirmed). fal.ai v3 Pro uses `end_image_url`. One SC223 snippet suggested `tail_image_url` for AIMLAPI v3 — but AIMLAPI's own v1/v1.6 naming and fal.ai's v3 naming both use `end_image_url`, making `end_image_url` the more likely AIMLAPI v3 name. CANARY REQUIRED: try `end_image_url` first; fall back to `tail_image_url` if rejected.** **⚠️ Pro-only in native Kling API** (SC223 July 18, 2026: Node.js wrapper documents `image_tail` as "end frame for interpolation (pro mode)") — Standard/Standard Turbo may not support end-frame conditioning natively. AIMLAPI wrapper behavior may differ — canary with Standard Turbo to confirm. **Incompatible with multi_prompt.** **Incompatible with static_mask_url, dynamic_masks, and camera_control (Kling v3 mutual exclusivity — pick only ONE of these four per call).** Same image = forces stationarity but allows mid-clip drift. |
| camera_control | object | — | Named preset OR simple config (not both). **Incompatible with static_mask_url, dynamic_masks, and end_image_url/tail_image_url (Kling v3 mutual exclusivity).** See camera control section. |
| elements | array | — | Character reference images for Subject Binding. Max 3 elements per I2V call. **Must be referenced as `@Element1` etc. in prompt.** |
| static_mask_url | string | — | White=freeze, black=allow motion. **Must match source image aspect ratio exactly.** PNG/JPG/WEBP, max 10MB. **⚠️ PARAMETER NAME:** AIMLAPI uses `static_mask_url` (confirmed from AIMLAPI docs: "URL of the image for Static Brush Application Area"). Native Kling API uses `static_mask`. Use `static_mask_url` on all AIMLAPI calls. |
| dynamic_masks | array | — | Motion brush paths. Up to 6 groups. See dynamic_masks section below. |
| multi_prompt | array | — | Multi-shot prompting (up to 6 shots) — **AIMLAPI parameter name**. Base Kling API calls this `guidances`. **Incompatible with tail_image_url.** Main `prompt` must be empty when used. See Multi-Shot section. |

## Elements (Subject Binding) — Exact AIMLAPI Structure

Pass reference images to keep a character's face consistent across clips.

**`face_consistency: true` is the confirmed v3 boolean for face identity lock** (June 2026). Set this in the generation body alongside `elements`. It forces the model to refer back to the element reference images to reconstruct the face even when partially occluded. This replaces the older numeric `face_adherence` slider (UI/wrapper abstraction — not the raw v3 API parameter name).

**⚠️ v3 dropped legacy face parameters (SC244 July 2026):** The following parameters from Kling v1/v2 do NOT exist in v3: `faceStrength`, `subjectStrength`, `faceNo`, `imageReference`, `reference`. Do NOT copy v1/v2 API examples into v3 calls — these parameters are silently ignored or return errors in v3.

**⚠️ "reference_strength" / "motion_strength" are NOT raw API parameters (SC244 July 2026):** Many community tutorials and some third-party wrapper guides (e.g., Flixly) reference "reference strength at 0.35/0.65/0.85" or "motion strength at 0.55" for Kling 3.0. These are kling.ai web UI slider abstractions or third-party wrapper-specific parameters — NOT raw API parameters on AIMLAPI. On raw AIMLAPI calls, character consistency is controlled via `face_consistency: true` + `elements` + `cfg_scale`. Do NOT copy these values into AIMLAPI JSON calls.

```python
"face_consistency": True,   # Add at generation root level alongside elements
"elements": [...]
```

**`elements` cannot coexist with `voice_list`** (mutual exclusivity confirmed). Since our pipeline never uses voice, this is documentation-only awareness — `voice_list` must never appear in our calls.

**No numeric `face_weight` or `face_adherence` parameter exists in raw v3 API** — adherence is driven by `face_consistency: true` + reference image quality and count. CLAUDE.md's "Subject Binding 80-90" describes the quality TARGET to achieve, not an API parameter value.

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
        "video_url": "https://cdn.example.com/character_reference_clip.mp4"  # max 8s
    }
]
```

**Video element max duration: 8 seconds.** The model builds a "Visual DNA" from the clip to lock face+clothing identity. Longer clips are not more effective — 3-8s of clear single-character footage is optimal.

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
- **Max 3 elements per I2V call** (not 4 — confirmed across multiple sources). **⚠️ fal.ai wrapper limitation:** fal.ai's Kling v3 I2V wrapper limits elements to 1 per call (wrapper limitation, NOT the native API limit). Native Kling API and AIMLAPI both allow up to 3. Do NOT copy `elements` code from fal.ai examples — their wrapper silently drops elements 2 and 3. (SC237, July 21, 2026)
- **reference_image_urls are STRONGLY RECOMMENDED, not optional** — multiple sources (May 2026) indicate that passing frontal_image_url alone without reference_image_urls may trigger a model error. Minimum 2 total images per element (frontal + at least 1 reference angle).
- **More refs ≠ better**: 2-4 focused images optimal. More than 4 confuses the model and weakens binding
- **frontal_image_url is mandatory** — reference_image_urls alone (without frontal) will not bind correctly
- **Pose matters**: simple neutral poses (standing, arms at sides) produce far less identity drift than complex poses or strong non-frontal angles. Use complex reference poses only as supplemental refs, not as the frontal anchor.

**Prompt budget:** Each `@ElementN` reference consumes approximately 37 characters of the 2500-char prompt limit. With 3 elements, reserve ~111 chars for references before writing motion instructions.

**Motion Control limit:** When using Motion Control V2V, max 1 element is supported (vs 3 for standard I2V). Element binding in Motion Control also requires `character_orientation: "video"`.

**Note:** CLAUDE.md refers to "Subject Binding face adherence 80-90" — this describes the quality target to achieve via reference image quality, not an API parameter value.

**Voice binding limitation:** Voice binding via video elements works ONLY with video elements (element containing `video_url`), NOT image elements (`frontal_image_url` + `reference_image_urls`). Passing a voice reference with an image-only element returns an error. For Snelverhuizen: we never use voice (Shari'ah compliance), so this is documentation-only awareness.

## Multi-Shot Prompting (multi_prompt on AIMLAPI)

Kling v3 supports generating up to 6 sequential shots in one API call. **On AIMLAPI the parameter is `multi_prompt` (not `guidances` — that is the base Kling API name).** Confirmed available for T2V and I2V.

**CRITICAL: `multi_shot: True` is REQUIRED to activate multi-shot mode for ALL Kling v3 variants (Standard and Pro, T2V and I2V).** Without this flag, `multi_prompt` is silently ignored and the model falls back to single-shot generation using the main `prompt` field. Confirmed across multiple Kling v3 platform implementations (June 2026). Previously documented as O3-only — this was incorrect; it applies to all v3 tiers.

**⚠️ Cross-platform naming trap (July 2026):** The native Kling API uses `multi_shots` (plural, boolean) and `sound` (boolean) for audio. AIMLAPI uses `multi_shot` (singular) and `generate_audio` (boolean). Do NOT copy-paste JSON from native Kling docs, KIE AI docs, or Griptape README into AIMLAPI calls — the parameter names diverge silently (wrong names are ignored, not rejected). AIMLAPI naming is what our pipeline uses throughout this document.

**⚠️ `elements` parameter cross-platform naming trap (July 2026):** Three different names for the same concept across platforms. AIMLAPI uses `elements` (array). KIE.ai uses `kling_elements` (array). AI SDK (ai-sdk.dev) uses `elementList`. None of these transfer between platforms — passing the wrong name silently no-ops the character binding. Our pipeline uses AIMLAPI `elements` exclusively. Do NOT copy element definitions from KIE.ai or AI SDK examples.

**HALAL RISK: Audio is always enabled in multi-shot mode.** `generate_audio: false` is ignored when `multi_shot: True` is set — the model generates audio for every multi-shot sequence. **Strip audio immediately post-generation:** `ffmpeg -i input.mp4 -an -c:v copy output_silent.mp4` — do NOT play audio before stripping.

**Constraints:**
- `multi_shot: True` MUST be set (top-level flag) — without it, multi_prompt is silently ignored
- Main `prompt` field MUST be empty when `multi_prompt` is used
- `tail_image_url` is INCOMPATIBLE with multi-shot — omit it
- Total video duration = sum of all shot durations (max 15s total)
- Each shot minimum duration: **3 seconds** on Magnific API (v3 wrapper) — do not set below 3s as the safe default. **⚠️ Discrepancy (SC244 July 2026):** Some fal.ai docs and community guides say 1 second minimum per shot; Magnific API docs say 3 seconds. AIMLAPI minimum is unconfirmed — use 3s until a canary confirms otherwise.
- Each entry takes `prompt` and `duration` — no `index` field required on AIMLAPI

```python
"multi_shot": True,   # REQUIRED — without this, multi_prompt is silently ignored
"prompt": "",         # MUST be empty
"generate_audio": False,  # Set this anyway, but NOTE: may be ignored in multi-shot mode
"multi_prompt": [
    {"prompt": "@Element1 walks to the truck, confident stride", "duration": 5},
    {"prompt": "@Element1 loads a box into the truck, smooth motion", "duration": 5},
    {"prompt": "Truck parked on street, environment settling, motion eases to stop", "duration": 5}
]
# AFTER GENERATION: strip audio before delivery
# ffmpeg -i input.mp4 -an -c:v copy output_silent.mp4
```

**Multi-shot failure modes (v3-specific — absent in single-shot Kling 2.6):**
- Character drift between shots (face/clothing changes at cut points)
- Audio desync at cut boundaries (if audio is enabled — always keep it off)
- Tonal shift between cuts (lighting or color grade jumps)
- Lighting inconsistency across shots
- **Silent fallback to single-shot (missing `multi_shot: True` flag)** — check output duration to confirm multi-shot fired

**Multi-shot anti-drift technique:** Restate a continuity anchor inside every shot prompt:
```python
"multi_prompt": [
    {"prompt": "@Element1 walks to the truck. Continuity: same face, same outfit, same lighting.", "duration": 5},
    {"prompt": "@Element1 loads a box into the truck. Continuity: same face, same outfit, same lighting.", "duration": 5},
]
```

**Multi-shot negative prompt additions** (add to standard negative template):
```
character drift between shots, tonal shift between cuts, lighting inconsistency across shots
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

**AIMLAPI availability:** Only v2.6 confirmed by dedicated docs page (`klingai/video-v2-6-pro-motion-control`). SC216, SC223, SC237 (July 21), and SC244 (July 24, 2026) searches found no AIMLAPI-sourced v3 Motion Control docs — docs index still only shows v2.6 motion control. Status: **POSSIBLE but NOT confirmed as of July 24, 2026**. Kling v3 Motion Control is confirmed live on Replicate (`kwaivgi/kling-v3-motion-control`), Eachlabs, ModelsLab, Kie AI, OpenArt, MindStudio, Media.io, and Artlist as of July 2026 — broad third-party availability increases likelihood it will land on AIMLAPI soon. Check AIMLAPI docs index before next walking-shot production. Kling v3 Motion Control is confirmed on WaveSpeedAI (`kwaivgi/kling-v3.0-pro/motion-control`), Replicate (`kwaivgi/kling-v3-motion-control`), fal.ai (`fal-ai/kling-video/v3/pro/motion-control`), Kie AI, ModelsLab, MindStudio, EachLabs, and Media.io. Expected AIMLAPI model strings: `klingai/video-v3-standard-motion-control` and `klingai/video-v3-pro-motion-control`. **CANARY REQUIRED before production use** — try the expected string on a 3s reference clip; if it returns 404, fall back to v2.6. Farouq AIMLAPI-only directive means attempting a canary is acceptable.

**Key parameter:** `character_orientation`
- `"video"` — output character follows orientation from reference video (better for complex multi-directional motion, max 30s output on v2.6; see v3 duration limits below)
- `"image"` — output character keeps orientation from source image (better for camera-led shots, max 10s)

**`background_source` parameter (v3 Motion Control, SC230 July 19, 2026):** New parameter confirmed in v3 Motion Control API calls. Value `"input_video"` uses the driving video as background source. CANARY REQUIRED — exact AIMLAPI parameter name may differ.

**v3 Motion Control duration limits (community-confirmed, kling3.pro, SC230 July 19, 2026):**
- Curve Dolly or Camera Shake feature: **10s max** (v3), **15s max** (O3)
- Multi-Elements 2 subjects: **8s max**
- Multi-Elements 3+ subjects: **6s max**
- Basic motion transfer (no Curve Dolly/Camera Shake/Multi-Elements): Likely 30s (same as v2.6 "video" orientation) — unconfirmed for v3

**Element limit (v2.6 / AIMLAPI current):** Max 1 element per Motion Control call. Element binding requires `character_orientation: "video"` — image orientation mode does not support elements.

**Framing rule:** Half-body image → pair with half-body motion reference. Full-body image → pair with full-body reference. Mismatch degrades motion transfer quality.

**When to use:** Walking shots where motion prompting alone produces robotic or sliding feet artifacts. Requires a royalty-free motion reference clip (3-30s, clear body movement, moderate speed).

### Kling v3 Motion Control — New Sub-Features (NOT on AIMLAPI yet; confirmed on fal.ai, Replicate, WaveSpeedAI, Kie AI, EachLabs, ComfyUI as of July 7, 2026)

Three new capabilities added in the v3 Motion Control tier that do not exist in v2.6:

**1. Multi-Elements (up to 4 subjects):** v2.6 limit was 1 element. v3 Motion Control allows 2–4 subject references, each with its own independent motion path. Each subject can have its own trajectory — solves multi-character scenes where v2.6 would merge or freeze secondary subjects. When O3/v3 Motion Control arrives on AIMLAPI, expect `elements` array with 4-entry limit (vs the 1-entry limit for v2.6 on AIMLAPI).

**2. Curve Dolly (camera path control):** More precise than simple `camera_control` config values. Curve Dolly sets keyframes at specific timestamps and interpolates between them, allowing compound camera movements (e.g., push-in that pivots into a tilt) without the single-non-zero-value constraint of standard `simple` camera_control. Standard I2V camera_control is unaffected — Curve Dolly is Motion Control-only. **Curve Dolly and Camera Shake can be combined** (SC230, July 19, 2026): use both simultaneously for camera movement with handheld character (e.g., Curve Dolly arc + Camera Shake intensity:2 frequency:3 = documentary orbiting shot). Duration cap when combined: still subject to the 10s v3 limit. **Duration cap when Curve Dolly is used alone: 10s max on v3** (15s on O3).

**3. Camera Shake:** Two independent parameters control handheld-feel:
- **Intensity**: amplitude of the shake movement
- **Frequency**: how rapidly the shake oscillates  
Combine low intensity + low frequency for subtle handheld; high intensity + high frequency for action/impact. Can be combined with Curve Dolly. Not available in standard I2V.

**Camera Shake production-tested example values (community-confirmed July 2026):**
| Effect | intensity | frequency | Use case |
|--------|-----------|-----------|----------|
| Gentle float | 1 | 1 | Subtle handheld establishing shot |
| Moderate handheld | **2** | **3** | Natural documentary feel — start here for canary |
| Large sway | 4 | 1 | Ocean/earthquake feel |
| Electronic vibration | 1 | 8 | Sci-fi/mechanical context |
Test with `intensity: 2, frequency: 3` first — the most balanced starting point for natural realism. Scale from there.

### Kling v3 Motion Control CANARY CHECKLIST (July 2026 — attempt if needed for walking shots)

- [ ] Try model string `klingai/video-v3-standard-motion-control` with a 3s motion reference clip
- [ ] If 404: also try `klingai/video-v3-pro-motion-control`
- [ ] If 404 for both: fall back to v2.6 (`klingai/video-v2-6-pro-motion-control`)
- [ ] If accepted: run short (3s) canary with half-body reference image + half-body motion clip
- [ ] Confirm cost vs v2.6 from AIMLAPI dashboard
- [ ] Run brand binary checklist and identity check before production use
- [ ] If confirmed: update AIMLAPI availability status above; add expected model strings to routing matrix

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

## Kling v3 Turbo Series — CONFIRMED ON AIMLAPI (launched June 17, 2026)

Two tiers confirmed on AIMLAPI:

| Tier | Model String | Resolution | Cost/5s | Cost/3s |
|------|-------------|-----------|---------|---------|
| Standard Turbo I2V | `klingai/video-v3-standard-turbo-image-to-video` | 720p | **$0.73** ($0.146/sec) | $0.44 |
| Standard Turbo T2V | `klingai/video-v3-standard-turbo-text-to-video` | 720p | **$0.73** ($0.146/sec) | $0.44 |
| **Turbo Pro I2V** | `klingai/video-v3-turbo-pro-image-to-video` | **1080p** | **$0.91** ($0.182/sec) | $0.55 |
| **Turbo Pro T2V** | `klingai/video-v3-turbo-pro-text-to-video` | **1080p** | **$0.91** ($0.182/sec) | $0.55 |

*Pricing source: AIMLAPI pricing page, confirmed June 2026. Native Kling: ¥0.8/s (720p) + ¥1/s (1080p), audio included at both tiers. AIMLAPI markup ~1.32×.*

**Last frame is OPTIONAL** (confirmed June 2026, multiple API providers — WaveSpeedAI: "end image is optional," Kie.ai: "first and/or last frame images"): Standard Turbo IS a drop-in for single-frame I2V. Last frame CAN be provided for A→B transitions or first=last ghost-driving lock.

**⚠️ MANDATORY AUDIO STRIP before any QA playback:**
Kling 3.0 Turbo "native audio included" is baked into the base pricing. `generate_audio` is **documented in AIMLAPI docs as an optional boolean with default=true** for Turbo models (June 2026 — AIMLAPI v3-standard-turbo-image-to-video page). Setting `false` is expected to suppress audio generation. However, mandatory strip-immediately rule stays in force as a safety precaution until a canary call confirms silence:
```bash
ffmpeg -i input.mp4 -an -c:v copy output_silent.mp4
```
Strip immediately on download. DO NOT play audio before stripping — AI-generated music is a Shari'ah violation.

**When to use Turbo vs Standard:**

| Need | Model | Cost/5s | Savings vs baseline |
|------|-------|---------|-------------------|
| Draft iteration (identity check, motion check) | **Standard Turbo I2V** | $0.73 | 33% vs Standard ($1.09) |
| Final delivery at 1080p (after canary) | **Turbo Pro I2V** | $0.91 | 37.7% vs v3 Pro ($1.46) |
| Final delivery guaranteed identity lock | v3 Pro I2V (current production) | $1.46 | — |
| A→B transition with defined start+end | Standard Turbo I2V | $0.73 | 33% vs Standard |
| Truck stationary (first=last frame) | Standard Turbo I2V | $0.73 | 50% vs Pro ($1.46) |

**Turbo Pro character consistency (multi-source confirmed July 2026):** Multiple independent reviews confirm Turbo Pro delivers "enhanced subject consistency — particularly important for faces, products, and brand assets" and "improved inter-frame stability and motion accuracy" vs Standard Turbo. In multi-shot sequences, "characters, wardrobe, and setting hold their look from cut to cut" (Atlas Cloud July 2026). This makes Turbo Pro a credible final-pass candidate for character shots (after canary). Confidence in quality is HIGH — canary is required for AIMLAPI cost/audio confirmation, not for quality validation.

**Turbo Pro final-pass savings (if canary passes):**
- 1 character final: $1.46 → $0.91 = saves **$0.55**
- 1 truck final: $1.46 → $0.91 = saves **$0.55**
- Typical 4-clip video (2 finals): saves **$1.10/video**
- Monthly 50 videos: saves **~$55/month**

### Turbo CANARY CHECKLIST (updated 2026-06-22)

**Standard Turbo I2V — draft replacement:**
- [ ] Submit one 5s I2V call with `klingai/video-v3-standard-turbo-image-to-video`, character hero frame, `aspect_ratio: "9:16"`, `generate_audio: false`
- [ ] Strip audio immediately: `ffmpeg -i input.mp4 -an -c:v copy output_silent.mp4`
- [ ] Record actual AIMLAPI cost from dashboard — confirm ~$0.73 ($0.146/sec)
- [ ] Confirm `image_url` alone (without `tail_image_url`) is accepted
- [ ] Confirm last-frame parameter name: try `tail_image_url` first (probable AIMLAPI name, one search snippet confirmed); also try native name `image_tail` if `tail_image_url` returns a parameter error. **Note (SC223):** native Kling API restricts `image_tail` to Pro mode — Standard Turbo may not support end-frame conditioning at all.
- [ ] Run QA: face identity retention vs Kling Standard baseline
- [ ] Check `generate_audio: false` effect — AIMLAPI docs document it as a boolean with default=true; verify it actually suppresses audio in the response
- [ ] If identity ≥ 80% AND audio confirmed suppressed → update Turbo audio warning to "CONFIRMED suppressed"; route all drafts here

**Turbo Pro I2V — final-pass candidate:**
- [ ] Submit one 5s I2V call with `klingai/video-v3-turbo-pro-image-to-video`, character hero frame, `aspect_ratio: "9:16"`, `generate_audio: false`
- [ ] Strip audio immediately before any playback
- [ ] Record actual AIMLAPI cost — confirm ~$0.91 ($0.182/sec)
- [ ] Confirm resolution from response metadata: must be 1080p
- [ ] Run InsightFace buffalo_l cosine similarity vs Kling v3 Pro baseline on identical prompt
- [ ] Run brand binary checklist + Shari'ah compliance
- [ ] If cosine ≥ 0.92 AND 1080p confirmed → Turbo Pro is viable final-pass model; update routing with owner approval

**Truck ghost-driving via first=last frame:**
- [ ] Pass same truck hero frame as `image_url` AND `tail_image_url`
- [ ] Run brand binary checklist: box sealed, no ghost driving, logo orange
- [ ] If passes → use as a cheaper alternative to static_mask_url + Kling Pro ($1.46)

---

## Kling O3 — Future Watch (Not Yet on AIMLAPI)

Kling O3 (VIDEO 3.0 Omni, released Feb 5, 2026) is the premium tier above v3 Pro. **Confirmed NOT on AIMLAPI as of July 24, 2026** — confirmed absent from AIMLAPI docs index and AIMLAPI's own blog post listing live Kling models (which lists only Kling 2.6 Pro and Kling v3 Pro, not O3). The June 17, 2026 Turbo launch did NOT include O3/Omni on AIMLAPI. A `site:aimlapi.com` search for "video-v3-omni" returns zero results as of July 14, 2026. O3 model string on Replicate: `kwaivgi/kling-v3-omni-video`; on fal.ai: `fal-ai/kling-video/o3/...`; expected AIMLAPI string when added: `klingai/video-v3-omni`. Available on fal.ai, Replicate, PiAPI, Atlas Cloud ($0.15/s), MindStudio, Vidguru, Picsart, Runware, and Freepik API — but **NOT AIMLAPI**. A 4K O3 variant (`klingai/video-o3-4k`, Runware-confirmed) was announced June 12, 2026 — expect both O3 base and O3 4K to land on AIMLAPI together. Farouq AIMLAPI-only directive means O3 cannot be used until it appears there.

**O3 advantages worth monitoring:**
- Multi-image element building: up to **7 reference images** per call (vs. 3 for v3 Pro)
- Combined input: up to **4 images + 1 reference video** in a single call (O3-exclusive)
- Multi-character coreference (3+ characters)
- **Voice binding from video element refs** — upload a clip to lock both the character's appearance AND voice tone; every time that character speaks, the voice stays consistent
- 3D Spacetime Joint Attention for stronger physics and consistency
- Native audio generation with lip-sync in 5 languages (EN, ZH, JA, KO, ES)

If O3 becomes available on AIMLAPI, evaluate it for character-heavy clips where v3 Pro produces identity drift.

**O3 API structure changes (confirmed across fal.ai/Runware/Atlas/Freepik/PiAPI — character-consistency.md pass 12; element syntax corrected SC149):**
- `elements` array → replaced by `kling_elements` array (`name` + `description` + `element_input_urls` of 2–4 images)
- **Element reference syntax (corrected SC149):** Native Kling API uses `<<<element_1>>>`, `<<<element_2>>>` triple-bracket syntax in prompt text. Third-party wrappers (fal.ai) use `@Element1` positional syntax. `@name` (name-value based) is web UI only — NOT valid at the raw API level. When O3 lands on AIMLAPI, canary-test which syntax the wrapper accepts before production use.
- `multi_shot: True` required to activate `multi_prompt` (without it, multi_prompt is silently ignored) — NOTE: singular (`multi_shot`), not `multi_shots`
- `generate_audio` defaults **ON** in O3 — ALWAYS set `False` explicitly
- `cfg_scale` and `negative_prompt` are **STILL PRESENT** — do NOT remove them when switching to O3
- `start_image_url` → renamed to `image_url` (same as v3 Pro on AIMLAPI — no change needed for our pipeline)
- `end_image_url` for end frame (NOT `tail_image_url` or `image_tail`) — O3-specific naming on fal.ai; confirm on AIMLAPI when O3 lands

**O3 June 17, 2026 upgrade:** Kling extended O3's *editing* pipeline (Omni Edit) to support 3–15s video input/output and 4K resolution. This is a V2V editing capability upgrade — the I2V reference-to-video character parameters are unchanged. O3 is still NOT on AIMLAPI as of July 3, 2026.

See `character-consistency.md` O3 section for the complete `kling_elements` call template.

**Voice control in v3 T2V (AIMLAPI, confirmed June 2026 — DO NOT USE in our pipeline):** AIMLAPI v3 Standard T2V now supports `voice_list` parameter for character dialogue ($0.154/sec surcharge). Voice references in prompts use `<<<voice_1>>>` triple-angle-bracket syntax (distinct from element `@Element1` syntax). **Our pipeline never uses audio (Shari'ah compliance) — always set `generate_audio: false`. This feature is documented for awareness only.**

## Kling 3.0 4K Variant — Future Watch (Not Yet Confirmed on AIMLAPI)

Kling 3.0 supports native 4K output (3840×2160, up to 60fps, 16-bit HDR). **4K API rollout: April 23, 2026.** Runware confirms model string `klingai:kling-video@o3-4k` (O3-based, not a standalone model). fal.ai exposes it as `fal-ai/kling-video/v3/4k/image-to-video`. June 12, 2026: Kling launched a $25,000 4K creative contest (not a new model announcement — 4K was already live).

**How 4K works (native Kling API):** The native Kling API accepts `"mode": "4k"` as a top-level parameter. However, third-party API wrappers implement 4K differently: **fal.ai exposes it as a dedicated model endpoint** (`fal-ai/kling-video/v3/4k/image-to-video`), not a parameter toggle. Runware similarly exposes a separate "Kling VIDEO O3 4K API" model. This means AIMLAPI may use either a separate model string or the `mode` parameter — do NOT assume either approach without a canary test.

**fal.ai 4K confirmed pricing: $0.42/sec ($2.10/5s)** — 44% more expensive than v3 Pro on fal.ai and ~44% more than Kling Pro on AIMLAPI ($1.46/5s). Only justified for final hero delivery clips, not draft iterations.

**4K I2V supported features:** single-shot (start frame only), multi-shot, start+end frame, element control with video character and multi-image inputs. Duration range: 3–15 seconds (same as pro mode). Motion Control and voice are NOT available in 4K mode.

**Native Kling API approach (confirmed):** `mode` parameter selects resolution tier: `"std"` (720p), `"pro"` (1080p), `"4k"` (3840×2160). Pass `"mode": "4k"` on the existing model string.

**Third-party model strings:** Runware uses `klingai:kling-video@3-4k` (v3 base) and `klingai:kling-video@o3-4k` (O3 4K). fal.ai uses dedicated path `fal-ai/kling-video/v3/4k/image-to-video`.

**AIMLAPI status:** UNCONFIRMED. No 4K-specific model page appears in AIMLAPI docs index. Neither `klingai/video-v3-pro-4k` nor a `mode: "4k"` mention appears in AIMLAPI's indexed model pages. Since O3 itself (`klingai/video-v3-omni`) is also absent from AIMLAPI, access to the O3-based 4K variant is doubly blocked. The most likely AIMLAPI access path when it lands: `mode: "4k"` on existing v3 Pro string (canonical approach from native API) — try this first; dedicated model string as fallback. Fall back to 1080p Pro if neither works. Use only for final-delivery hero clips; 4K costs ~44% more than Pro 1080p.

## Hailuo 2.3 Fast — B-roll I2V (CANARY REQUIRED)

Available on AIMLAPI. AIMLAPI model string: **`minimax/hailuo-2.3-fast`** (confirmed July 2026).

**Key parameters on AIMLAPI:**
- `image_url` — first frame (same parameter name as Kling on AIMLAPI; native MiniMax API uses `first_frame_image` — do NOT copy native docs)
- `prompt`, `duration`, `generate_audio: false`

**Cost:** ~$0.208/5s (routing matrix value). External sources cite ~$0.19/generation at Fast tier, suggesting pricing may be slightly under $0.208 — canary will confirm exact AIMLAPI rate.

**Use case:** B-roll and transition clips where a static first-frame anchor is available and no characters appear. 24–36% cheaper per clip than Veo 3.1 Lite ($0.52/5s) depending on confirmed rate. CANARY REQUIRED before production use — run one 5s call, check audio (always strip: `ffmpeg -i in.mp4 -an -c:v copy out_silent.mp4`), confirm cost in AIMLAPI dashboard.

---

## Error Handling

- **403 (out of credits):** STOP immediately. Notify owner via Telegram.
- **404 (model not found):** Check model string spelling.
- **Timeout:** Retry once with 30s timeout, then STOP.
- **Generation failed:** Log failure. Do NOT auto-retry (costs credits).

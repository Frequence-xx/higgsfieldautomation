---
name: Kling Truck Prompting
description: Dedicated prompting workflow for Kling v3 I2V truck/vehicle shots. Prevents ghost driving, preserves branding, manages static masks, and provides the full negative prompt template for vehicle scenes.
autoInvoke: true
triggers:
  - truck shot
  - vehicle
  - truck animation
  - ghost driving
  - stationary truck
  - truck I2V
negatives:
  - Do NOT invoke when the shot contains no vehicle (use generation-video.md for general I2V)
  - Do NOT invoke when generating a hero frame of the truck (use generation-image.md)
  - Do NOT invoke when the truck is intentionally driving (e.g., driving-away outro shot — use with extreme caution)
---

# Kling Truck Prompting — Anti-Ghost-Driving Workflow

The Snel Verhuizen truck appearing in video is the #1 source of production failures. Ghost driving (truck appearing to move when it should be parked) has caused 3/3 video rejections. This skill provides the complete workflow for truck I2V shots.

## The Problem

Kling v3 interprets any vehicle in frame as potentially moving. Without explicit multi-layer constraints, the truck will:
- Creep forward ("ghost driving")
- Rock or bounce on suspension
- Have wheels that appear to rotate
- Deform the cargo box geometry
- Morph the SNELVERHUIZEN branding text

## The Solution: Five-Layer Freeze Protocol

Every truck shot MUST apply ALL five layers. Omitting any layer increases ghost-driving risk.

### Layer 1: Prompt Constraint

MUST include ALL of these phrases in the motion prompt:

```
stationary truck, parked, engine off, no vehicle movement, no forward creep,
the vehicle remains rigid and solid, metal does not deform
```

### Layer 2: Negative Prompt

MUST include this full negative prompt block for every truck shot:

```
vehicle movement, driving, rolling, ghost driving, sliding vehicle,
wheel rotation, truck rocking, suspension bounce, forward creep,
vehicle deformation, metal warping, chassis flex, door opening,
text morphing, label warping, branding distortion, logo change,
geometry distortion, reflection artifacts, surface inconsistency,
blurry, distorted, low quality, jittery, flickering, morphing faces,
warping, deformed hands, extra fingers, sliding feet, identity drift,
watermark, camera shake, inconsistent lighting, plastic skin, color shift
```

### Layer 3: Static Mask (Motion Brush)

Generate a mask image where:
- **White pixels** = FREEZE (no motion allowed)
- **Black pixels** = ALLOW motion

Paint the ENTIRE vehicle body WHITE (frozen). Leave the environment (sky, trees, people, ground) BLACK.

**MUST NOT paint the vehicle body black.** The vehicle body MUST remain unpainted (white = frozen).

**Mask technical requirements:**
- **Aspect ratio MUST exactly match the hero frame** (e.g., 9:16 → mask must also be 9:16). Mismatch = task failure.
- If using dynamic_masks simultaneously, mask resolution must also match exactly.
- Supported formats: PNG, JPG, JPEG, WEBP. Max 10MB.

```python
# Include in API call:
{
    "static_mask_url": "<url_to_mask_covering_entire_truck>"
}
```

### Layer 4: Endpoint Frame (Tail Image)

Use the SAME hero frame as both `image_url` (start) and `tail_image_url` (end). This forces the model to return to the identical composition at the final frame — preventing net displacement. **Important:** this does NOT guarantee zero motion during the clip. The truck can still drift forward and back between the start and end frames. Use tail_image_url as a second-order safeguard; primary stationarity control must be in the prompt (Layer 1) and negative prompt (Layer 2).

```python
{
    "image_url": hero_frame_url,
    "tail_image_url": hero_frame_url,  # Same image — forces stationarity
}
```

### Layer 5: CFG Scale

MUST use `cfg_scale: 0.7` for all truck shots. Higher adherence preserves the hero frame composition more strictly, reducing drift.

For shots where the truck is secondary (background element): `cfg_scale: 0.5` MAY be acceptable, but include all other layers.

## Complete API Call Template — Truck Shot

```python
resp = httpx.post("https://api.aimlapi.com/v2/generate/video/kling/generation", json={
    "model": "klingai/video-v3-pro-image-to-video",
    "image_url": hero_frame_url,
    "tail_image_url": hero_frame_url,
    "prompt": "Slow camera orbit. Stationary truck, parked, engine off, no vehicle movement, no forward creep. The vehicle remains rigid and solid, metal does not deform. Light reflections glide gently across truck surface. Foreground leaves drift subtly. Branding text stays perfectly sharp. Motion gradually eases to stop.",
    "duration": "5",
    "aspect_ratio": "9:16",
    "generate_audio": False,
    "cfg_scale": 0.7,
    "negative_prompt": "vehicle movement, driving, rolling, ghost driving, sliding vehicle, wheel rotation, truck rocking, suspension bounce, forward creep, vehicle deformation, metal warping, chassis flex, door opening, text morphing, label warping, branding distortion, logo change, geometry distortion, reflection artifacts, surface inconsistency, blurry, distorted, low quality, jittery, flickering, morphing faces, warping, deformed hands, extra fingers, sliding feet, identity drift, watermark, camera shake, inconsistent lighting, plastic skin, color shift",
    "static_mask_url": truck_freeze_mask_url,
    "camera_control": {
        "type": "simple",
        "config": {
            "horizontal": 0, "vertical": 0, "pan": 0,
            "tilt": 3, "roll": 0, "zoom": 0
        }
    },
}, headers=headers, timeout=30)
```

## Motion Parameters for Truck Scenes

| Parameter | Value | Reasoning |
|-----------|-------|----------|
| cfg_scale | **0.5** (people primary) / **0.7** (truck primary) | Higher adherence for branded asset |
| motion_strength | **Not a standard I2V parameter** | Motion Control-only; omit from all standard I2V calls. |
| duration | **5s** | Minimize time for artifacts to accumulate |
| generate_audio | **false** | Always — add audio in post |
| face_consistency | **false** | No character face binding needed for truck-primary shots |

**motion_strength is NOT a valid standard I2V parameter (confirmed May 2026).** It is Motion Control (V2V) only and absent from the standard Kling I2V schema. Do not pass it. Use `cfg_scale: 0.7` + prompt anchors for truck stationarity.

## Camera Control Presets — Reference List (simple type only is confirmed on AIMLAPI; named presets below are from Kling base API docs, unverified on AIMLAPI)

Use `camera_control.type` to choose camera movement. For truck shots prefer `simple` with low values (2–5) or all-zero lock.

| Type | Motion | Best for truck shot |
|------|--------|---------------------|
| `simple` | Custom via sub-params (range −10 to +10) | ✅ Preferred — full control |
| `down_back` | Camera descends + moves backward | ❌ Reveals top, not recommended |
| `forward_up` | Camera moves forward + tilts up | ❌ Creates approach illusion |
| `right_turn_forward` | Rotate right + move forward | ⚠️ Use only for reveal approach |
| `left_turn_forward` | Rotate left + move forward | ⚠️ Use only for reveal approach |

`simple` sub-params meaning:
- `horizontal` — side-to-side dolly (±)
- `vertical` — up/down movement (±)
- `pan` — horizontal scan/rotation (x-axis)
- `tilt` — vertical angle change (y-axis)
- `roll` — z-axis tilt (rarely useful)
- `zoom` — push-in/zoom in (−) / pull-back/zoom out (+)  ← negative = narrower FOV = zoom in

**Gentle cinematic orbit:** `tilt: 2–3, pan: 2–3` — enough movement to feel alive, low enough to avoid physics artifacts.

## What Motion IS Allowed in Truck Scenes

The truck MUST remain frozen. Motion SHOULD come from:

- **Environment:** Leaves, clouds, light reflections, wind in trees, birds
- **People:** Crew walking around/near the truck (with character consistency refs)
- **Camera:** Gentle orbit, push-in, or pull-back (values 2-5)
- **Atmospheric:** Golden hour light playing across surfaces, shadows shifting slightly

## QA Checklist for Truck Clips

After generating each truck clip, extract 5 evenly-spaced frames and verify:

- [ ] Truck has NOT moved position between first and last frame
- [ ] Wheels are NOT rotating
- [ ] Cargo box geometry is consistent across all frames
- [ ] SNELVERHUIZEN text is legible and not morphed in any frame
- [ ] Orange branding band (#FC8434) is consistent color across frames
- [ ] No side door has appeared on the cargo box
- [ ] Truck shadow is consistent (not shifting)
- [ ] Any people in scene maintain identity and natural motion

If ANY check fails: reject, add stronger constraints, retry (max 2 per model-ceiling-detection.md).

## Known Kling v3 Truck Failure Modes

| Failure | Frequency | Fix |
|---------|-----------|-----|
| Forward creep (ghost driving) | ~60% without constraints | All 5 layers above |
| Text morphing on cargo box | ~40% | Remove text from hero frame, composite in post |
| Wheel rotation illusion | ~20% | Static mask covering wheels specifically |
| Cargo box geometry warp | ~15% | cfg_scale 0.7 + static mask |
| Reflection artifacts on cab | ~10% | Diffuse lighting in hero frame, avoid direct sun |

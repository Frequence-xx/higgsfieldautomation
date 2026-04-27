---
name: Generation — Hero Frames (Image)
description: Tier 1A hero frame generation via AIMLAPI. Covers Nano Banana Pro, Nano Banana Pro Edit, Flux Kontext Max, and Flux Pro. Native 9:16 parameters, reference image handling, model selection, and API call templates.
autoInvoke: true
triggers:
  - hero frame
  - image generation
  - generate image
  - Nano Banana Pro
  - NBP
  - Kontext Max
  - Flux Pro
  - still image
  - keyframe
negatives:
  - Do NOT invoke when animating an already-approved hero frame (use generation-video.md)
  - Do NOT invoke when performing QA or scoring (use video-qa-rubric.md)
  - Do NOT invoke when doing post-production, captions, or audio work
---

# Generation — Hero Frames (Image Models)

Tier 1A of the pipeline. Generate hero frames (still images) via AIMLAPI API. Every hero frame MUST pass QA before advancing to video animation.

## Critical Rules

1. **MUST generate natively in 9:16** for vertical platforms. NEVER crop, zoom, or pad a square image.
2. **MUST generate ONE image at a time.** Verify the output before generating the next.
3. **MUST use reference images** for any shot containing brand assets (truck, uniform, boxes).
4. **MUST run full QA** (8 dimensions + Shari'ah + cinematic quality) on every hero frame before sending to I2V.
5. **MUST send hero frames to owner for approval** before spending video credits on animation. MUST NOT animate without owner sign-off.

## Model Selection Matrix

| Model | AIMLAPI String | Best For | Max Refs | Cost (1K) | 9:16 Output |
|-------|---------------|----------|----------|-----------|-------------|
| Nano Banana 2 Edit (DRAFT) | `google/nano-banana-2` | Draft iterations before committing NBP Pro credits | 14* | ~$0.07* | 768x1344* |
| Nano Banana Pro | `google/nano-banana-pro` | Text-only scenes, B-roll, establishing shots | 0 | ~$0.13 | 768x1344 |
| Nano Banana Pro Edit | `google/nano-banana-pro-edit` | Brand asset compositing (truck + character + box) | 14 | ~$0.20 | 768x1344 |
| Flux Kontext Max | `flux/kontext-max/image-to-image` | Character identity lock across scenes | 8 | ~$0.10 | 752x1392 |
| Flux Kontext Max T2I | `flux/kontext-max/text-to-image` | Brand color stills without input ref | 0 | ~$0.08 | 768x1344 |
| Flux Pro v1.1 | `flux-pro/v1.1` | High detail hero shots | — | ~$0.05 | TBD |
| Flux Pro v1.1 Ultra | `flux-pro/v1.1-ultra` | Money shots, CTA cards | — | ~$0.10 | TBD |

*NB2 row marked with asterisk — CANARY TEST REQUIRED before production use. AIMLAPI pricing unverified. As of Feb 2026 launch, NB2 is reported to support 14 refs and 9:16; earlier April 16 audit noted a "5 refs / 5 ratio" limit that may refer to the older `google/nano-banana` (Gemini 2.5 Flash) model, not NB2. Verify in a $0 test before using on paid shots.

### Decision Flow

```
Shot has characters, need to iterate prompt? → NB2 Edit DRAFT first (if canary passes), then NBP Edit for final
Shot has characters (Karel/Mourad), final? → Nano Banana Pro Edit (existing refs as Image 1)
Shot has characters (new recurring)? → Create ref sheet first, then NBP Edit
Shot has brand assets but no people? → Nano Banana Pro Edit (truck/box refs)
Shot is pure scenery / B-roll? → Nano Banana Pro (text-only, cheapest)
Shot needs pixel-perfect text on truck? → Flux Kontext Max I2I (best text rendering)
Shot needs brand-color still without input? → Flux Kontext Max T2I
Shot is the money shot / CTA hero? → Flux Pro v1.1 Ultra
```

## API Call Templates

### Nano Banana 2 Edit (draft/iteration — CANARY VERIFY FIRST)

```python
# Use for prompt iteration before committing NBP Pro credits.
# Verify 9:16 support and pricing on AIMLAPI before first use.
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/nano-banana-2",
    "prompt": "Image 1: Mourad character reference sheet. DRAFT: Mourad standing next to the truck cab, three-quarter view. Keep facial features identical to Image 1. Golden hour warm backlight, 85mm portrait, shallow DOF, vertical composition.",
    "image_urls": [mourad_sheet_url],
    "aspect_ratio": "9:16",
    "resolution": "1K",
    "num_images": 1,
}, headers=headers, timeout=60)
hero_url = resp.json()["data"][0]["url"]
# If canary passes: use this model for prompt iteration drafts, NBP Pro for approved finals.
```

### Nano Banana Pro (text-to-image)

```python
import httpx, os

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/nano-banana-pro",
    "prompt": "<scene description in creative-director natural language>",
    "aspect_ratio": "9:16",
    "resolution": "1K",
    "num_images": 1,
}, headers=headers, timeout=60)

hero_url = resp.json()["data"][0]["url"]
```

### Nano Banana Pro Edit (reference-based, up to 14 images)

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/nano-banana-pro-edit",
    "prompt": "Image 1: Mourad character reference sheet. Image 2: Truck reference. Generate Mourad standing next to the truck cab, three-quarter view. Keep facial features exactly the same as Image 1. Golden hour warm backlight, 85mm portrait lens, shallow depth of field, cinematic color grading, vertical composition.",
    "image_urls": [mourad_sheet_url, truck_ref_url],
    "aspect_ratio": "9:16",
    "resolution": "1K",
    "num_images": 1,
}, headers=headers, timeout=60)

hero_url = resp.json()["data"][0]["url"]
```

### Flux Kontext Max (image-to-image, character lock)

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "flux/kontext-max/image-to-image",
    "prompt": "Place this exact person on a quiet Dutch residential street next to a white moving truck. Keep all clothing and facial features exactly the same. Golden hour warm sunlight, cinematic wide shot, vertical composition.",
    "image_url": [character_ref_url],
    "aspect_ratio": "9:16",
    "num_images": 1,
}, headers=headers, timeout=90)
# Response is SYNCHRONOUS — no polling needed
hero_url = resp.json()["data"][0]["url"]
```

## 9:16 Resolution Reference

| Resolution | Nano Banana Pro | Kontext Max | Cost |
|------------|-----------------|-------------|------|
| 1K | 768 x 1344 | 752 x 1392 | ~$0.10-0.20 |
| 2K | 1536 x 2688 | — | ~$0.13 |
| 4K | 3072 x 5376 | — | ~$0.24 |

## Prompting Rules for NBP (Gemini 3 Pro Image)

NBP is a "Thinking" model. Natural language outperforms tag soup.

### 6-Component Structure (2026-04-27)

Structure every NBP prompt using these six components — each adds ~15-20% more control:

1. **Subject** — who or what is the main focus ("Mourad, mid-30s man, warm olive skin, strong jawline, short black beard")
2. **Action** — what the subject is doing and pose ("standing at the rear of the truck, three-quarter left profile, lifting a box")
3. **Environment** — specific spatial placement ("positioned at the left third of the frame, next to the open truck on a quiet Dutch residential street")
4. **Art Style** — render approach ("cinematic photorealistic, golden hour color grading")
5. **Lighting** — direction and quality ("warm backlight from upper left, soft fill on face, shallow depth of field")
6. **Camera** — lens and framing ("85mm portrait lens, f/2.2, vertical composition, face occupying 30-40% of frame height")

### Spatial Reasoning — Be Precise (2026-04-27)

Use specific positional language rather than vague placement:

| WEAK | STRONG |
|------|--------|
| "Person standing near a window" | "Person standing at a floor-to-ceiling window, positioned at the left third of the frame, facing right, three-quarter profile view" |
| "Next to the truck" | "Standing at the rear left corner of the truck cab, facing camera, truck filling right 40% of frame" |
| "Holding a box" | "Both hands gripping the base of a white cardboard box at waist height, box tilted 15° toward camera" |

### Explicit Exclusions — Embed in Natural Language (2026-04-27)

No negative prompt parameter exists. Embed exclusions directly in the prompt:

```
"No side door on the cargo box — smooth sealed white panels only.
No additional people in the scene.
No text overlays or watermarks.
No extra props not listed above.
No hyper-saturation or heavy vignetting."
```

Place exclusions at the END of the prompt after the positive description.

### Visual Anchors — Multi-Shot Consistency (2026-04-27)

For productions requiring 4+ hero frames of the same character, define a Visual Anchors block at the START of every prompt. List 3-6 invariant traits that must stay constant across all shots:

```
VISUAL ANCHORS (maintain across all shots):
- Color palette: warm golden hour, Dutch soft light, #FC8434 brand orange
- Mourad: olive skin, strong jawline, dark brown eyes, short black beard, black crewneck, orange chest logo
- Truck: white cargo box, sealed panels (no side door), SNELVERHUIZEN text
- Environment: quiet Dutch residential street, red-brick facades, clean pavement
- Camera: 85mm portrait, shallow DOF, 9:16 vertical
```

This reduces iteration cycles from 15-20 to 3-5 attempts for multi-shot batches.

### Other Rules

- Wrap text in quotes: `displaying "SNELVERHUIZEN" in bold white sans-serif`
- Prompts over ~200 words trigger internal summarization — keep concise
- NO seed, guidance scale, or CFG parameters

### Reference Image Rules (NBP Edit)

- Label every image: "Image 1: Mourad character sheet. Image 2: Truck reference."
- Control via natural language: "Use Image 1 as a strict identity reference"
- **Identity lock formula:** "Maintain the exact same facial features as Image 1 — same eyes, nose shape, jawline contour, and skin texture." (more specific than generic "keep face the same")
- **Add text description of distinctive features** alongside the image ref: e.g., "Mourad: warm olive skin, strong jawline, dark brown eyes, short black beard" — text reinforces the visual anchor
- Explicitly remove objects from previous scenes ("No longer holding the clipboard")
- Character sheet MUST be Image 1 in every call for character shots
- **Max 14 images total, BUT only 5 can be human/person identity references.** Remaining 9 slots are for objects, vehicles, and scenes. Do NOT exceed 5 human refs or identity anchoring degrades. For strict structural accuracy, cap total uploads at 6 high-quality refs even if quota allows more.
- **Reference image quality spec (2026-04-21):** Minimum resolution 1024×1024. Face must occupy **30–50% of the frame area** — tighter crops produce better identity anchoring than full-body shots used as the sole reference. Sub-30% face coverage = identity drift; sub-1024px = detail loss in identity latent.
- First-pass consistency rates: character-sheet workflow = 85-90%; single hero image without sheet = 60-70%

### Multi-Reference Role Assignment (2026-04-27)

Assign a ROLE to each reference image, not just a name. The model reads role assignments and applies refs selectively:

```
Image 1: Mourad character reference sheet — use as strict IDENTITY reference.
  Maintain 100% of facial features, bone structure, skin tone.
Image 2: Lighting/color reference — use ONLY for lighting angle and color grading.
  Do NOT copy clothing or environment from this image.
Image 3: Truck brand reference — use for truck design, box color, and text styling.
  Do NOT use for character identity.
Image 4: Background environment reference — use for street architecture and pavement texture.
```

Role-assigned refs prevent bleed between identity and style references, which is the main cause of character drift when mixing person + vehicle + environment refs.

### 3-View Character Sheet Workflow (2026-04-23)

**Why:** A single composite sheet (frontal + 45° + 90° side) gives the model a 3D head structure map in one slot, using only 1 of the 5 human slots instead of 3. Achieves 90%+ consistency across multi-shot batches.

**How to build a character sheet from ONE approved hero frame:**

```
Step 1 — generate 3/4 left view:
  prompt: "Image 1: Mourad hero frame. Generate Mourad at a 45-degree left profile.
           Maintain the exact same facial features as Image 1 — same eyes, nose shape,
           jawline contour, and skin texture. Plain white background. Head and shoulders only.
           Same clothing as Image 1."
  model: google/nano-banana-pro-edit
  image_urls: [mourad_hero_url]

Step 2 — generate 3/4 right view:
  (same prompt with "45-degree right profile")

Step 3 — FFmpeg composite into one image:
  ffmpeg -i front.jpg -i left.jpg -i right.jpg \
    -filter_complex "[0][1][2]hstack=inputs=3" character_sheet_mourad.jpg

Step 4 — use character_sheet_mourad.jpg as Image 1 in all future NBP Edit calls
```

This single sheet costs ~$0.40 total (2× NBP Edit + free FFmpeg) and eliminates slot pressure.

## Prompting Rules for Flux Kontext Max

- 30-80 word sweet spot, maximum 512 tokens
- FLUX does NOT support CLIP-style weighting — `(keyword:1.5)` is silently ignored
- Token hierarchy: subject > action/pose > environment > lighting > style
- For SNELVERHUIZEN.NL text: always use quotation marks, ALL CAPS, specify "bold clean sans-serif". Text editing format: `Replace '[original text]' with '[new text]'`
- If text morphs: generate truck text-free, composite in post
- **ONE change per call** — progressive editing only. Change background first → then lighting → then details. Stacking multiple changes in one prompt degrades quality.
- Refer to subjects by description, not pronouns: "the man with the black crewneck" not "him"
- Character identity: uses AuraFace embeddings; maintains cosine similarity >0.92 across 6 successive edits (vs ~0.80 for competing models). This means ≤6 edits from original ref before restarting chain.
- `guidance_scale` range on AIMLAPI: 1–20. **Default is 3.5.** Optimal 2.5–3.5 for editing (higher = more prompt-literal, lower = more image-preserving). Do not exceed 5 for character editing — face structure distorts. Note: other platforms (Replicate, fal.ai) use a different guidance_scale range (1–50) — do not import their settings.
- `num_inference_steps`: not exposed on AIMLAPI I2I endpoint (handled server-side). For T2I endpoint: 20-50 steps; use 28 for drafts, 50 for production finals.

### Max vs Pro — When to Use Which (2026-04-27)

| Capability | Kontext Max | Kontext Pro |
|-----------|-------------|-------------|
| Typography / text rendering | **Max wins** — cleaner letterforms | Competent but slightly less refined |
| Style transfers (global) | **Max wins** — more believable | Sometimes inconsistent |
| Character identity across ≥4 chain edits | Pro more reliable | **Pro wins** — fewer subtle face drifts |
| Complex multi-attribute edits | **Max wins** — handles priority better | Sometimes deprioritizes elements |

**Pipeline routing:** Use Max for all text/typography shots (SNELVERHUIZEN.NL renders). For pure character edits requiring 4+ iterations from one ref, Kontext Pro may yield more stable face identity — but Max remains default on AIMLAPI per current model string.

### Chain Edit Checkpoint Workflow (2026-04-27)

After 6 successive edits, artifacts accumulate and identity drifts. Follow this workflow:

```
Edit 1 → Save intermediate (checkpoint A)
Edit 2 → Save intermediate (checkpoint B)
Edit 3 → SAVE CHECKPOINT — this is your recovery point
Edit 4 → ...
Edit 5 → ...
Edit 6 → Final. If quality insufficient, restart chain from checkpoint A or B (NOT from Edit 6).
```

- Save every intermediate URL to SQLite before the next edit call
- Never use the step-6 output as the input for a new chain — restart from original ref or checkpoint A
- Planning the edit order before starting reduces backtracking: background → lighting → costume details → text

## Post-Generation Checklist

After generating EACH hero frame:

- [ ] READ the generated image (visually inspect, not just check URL)
- [ ] Face matches reference? (if character shot)
- [ ] Truck branding correct? (SNELVERHUIZEN, orange #FC8434)
- [ ] No side door on cargo box?
- [ ] Clothing correct? (black crewneck, orange logo, blue jeans, white sneakers)
- [ ] No Shari'ah violations?
- [ ] Native 9:16 composition? (no black bars)
- [ ] Would a professional accept this?
- [ ] Send to owner for approval BEFORE animating

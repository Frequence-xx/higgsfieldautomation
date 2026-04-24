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

- Write 3-6 sentences in creative-director voice
- Include camera specs: "50mm f/2.8, shallow depth of field"
- Wrap text in quotes: `displaying "SNELVERHUIZEN" in bold white sans-serif`
- Use positive framing ("empty street" not "no cars")
- Prompts over ~200 words trigger internal summarization — keep concise
- NO negative prompt parameter — all control via natural language
- NO seed, guidance scale, or CFG parameters

### Reference Image Rules (NBP Edit)

- Label every image: "Image 1: Mourad character sheet. Image 2: Truck reference."
- Control via natural language: "Use Image 1 as a strict identity reference"
- **Identity lock formula:** "Maintain the exact same facial features as Image 1 — same eyes, nose shape, jawline contour, and skin texture." (more specific than generic "keep face the same")
- **Add text description of distinctive features** alongside the image ref: e.g., "Mourad: warm olive skin, strong jawline, dark brown eyes, short black beard" — text reinforces the visual anchor
- Explicitly remove objects from previous scenes ("No longer holding the clipboard")
- Character sheet MUST be Image 1 in every call for character shots
- **Max 14 images total, BUT only 5 can be human/person identity references.** Remaining 9 slots are for objects, vehicles, and scenes. Do NOT exceed 5 human refs or identity anchoring degrades.
- **Reference image quality spec (2026-04-21):** Minimum resolution 1024×1024. Face must occupy **30–50% of the frame area** — tighter crops produce better identity anchoring than full-body shots used as the sole reference. Sub-30% face coverage = identity drift; sub-1024px = detail loss in identity latent.
- First-pass consistency rates: character-sheet workflow = 85-90%; single hero image without sheet = 60-70%

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
- `guidance_scale` range on AIMLAPI: 1–20. **Default is 3.5.** Optimal 2.5–3.5 for editing (higher = more prompt-literal, lower = more image-preserving). Do not exceed 5 for character editing — face structure distorts.
- `num_inference_steps`: not exposed on AIMLAPI I2I endpoint (handled server-side). For T2I endpoint: 20-50 steps; use 28 for drafts, 50 for production finals.

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

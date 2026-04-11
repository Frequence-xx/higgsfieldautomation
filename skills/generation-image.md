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
5. **SHOULD send hero frames to owner for approval** before spending video credits on animation.

## Model Selection Matrix

| Model | AIMLAPI String | Best For | Max Refs | Cost (1K) | 9:16 Output |
|-------|---------------|----------|----------|-----------|-------------|
| Nano Banana Pro | `google/nano-banana-pro` | Text-only scenes, B-roll, establishing shots | 0 | ~$0.13 | 768x1344 |
| Nano Banana Pro Edit | `google/nano-banana-pro-edit` | Brand asset compositing (truck + character + box) | 14 | ~$0.20 | 768x1344 |
| Flux Kontext Max | `flux/kontext-max/image-to-image` | Character identity lock across scenes | 4 | ~$0.10 | 752x1392 |
| Flux Pro v1.1 | `flux-pro/v1.1` | High detail hero shots | — | ~$0.05 | TBD |
| Flux Pro v1.1 Ultra | `flux-pro/v1.1-ultra` | Money shots, CTA cards | — | ~$0.10 | TBD |

### Decision Flow

```
Shot has characters (Karel/Mourad)? → Nano Banana Pro Edit (existing refs as Image 1)
Shot has characters (new recurring)? → Create ref sheet first, then NBP Edit
Shot has brand assets but no people? → Nano Banana Pro Edit (truck/box refs)
Shot is pure scenery / B-roll? → Nano Banana Pro (text-only, cheapest)
Shot needs pixel-perfect text on truck? → Flux Kontext Max (best text rendering)
Shot is the money shot / CTA hero? → Flux Pro v1.1 Ultra
```

## API Call Templates

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
- Identity-locking phrases: "Keep facial features exactly the same as Image 1"
- Explicitly remove objects from previous scenes ("No longer holding the clipboard")
- Character sheet MUST be Image 1 in every call for character shots
- 6 references with high fidelity, up to 14 total

## Prompting Rules for Flux Kontext Max

- 30-80 word sweet spot, maximum 512 tokens
- FLUX does NOT support CLIP-style weighting — `(keyword:1.5)` is silently ignored
- Token hierarchy: subject > action/pose > environment > lighting > style
- For SNELVERHUIZEN.NL text: always use quotation marks, ALL CAPS, specify "bold clean sans-serif"
- If text morphs: generate truck text-free, composite in post

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

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

| Model | AIMLAPI String | Best For | Max Refs | Cost | 9:16 Output |
|-------|---------------|----------|----------|------|-------------|
| Imagen 4 Fast (DRAFT) | `google/imagen-4.0-fast-generate-001` | **⚠️ RETIRES 2026-06-24** — cheap prompt iteration, $0.02/img. Migrate to NBP now. | 0 | $0.02 | native |
| Imagen 4 | `google/imagen-4.0-generate-001` | **⚠️ RETIRES 2026-06-24** — use NBP Pro instead | 0 | ~$0.04 | native |
| Imagen 4 Ultra | `google/imagen-4.0-ultra-generate-001` | **⚠️ RETIRES 2026-06-24** — migrate to NBP Pro immediately | 0 | ~$0.06 | 2K native |
| Nano Banana 2 Edit | `google/nano-banana-2` | Draft iterations with refs; Pro-quality at Flash speed — use before NBP for prompt iteration | 14† | ~$0.07 | 768x1344 |
| Nano Banana Pro | `google/nano-banana-pro` | Text-only scenes, B-roll, establishing shots | 0 | ~$0.13 | 768x1344 |
| Nano Banana Pro Edit | `google/nano-banana-pro-edit` | Brand asset compositing (truck + character + box) — final quality | 14 | ~$0.20 | 768x1344 |
| Flux Kontext Max | `flux/kontext-max/image-to-image` | Character identity lock across scenes; text/typography edits | 8 | ~$0.10 | 752x1392 |
| Flux Kontext Pro | `flux/kontext-pro/image-to-image` | Character identity chain-editing (4+ iterations) — better face stability, lower cost than Max | 8 | ~$0.05 | 752x1392 |
| Flux Kontext Max T2I | `flux/kontext-max/text-to-image` | Brand color stills without input ref | 0 | ~$0.08 | 768x1344 |
| FLUX.2 Pro Edit | `blackforestlabs/flux-2-pro-edit` | Multi-ref brand asset compositing, up to 3 refs on AIMLAPI | 3 | ~$0.07 | native |
| GPT Image 2 | `gpt-image-2` | CTA cards requiring pixel-perfect Dutch text; 99% text accuracy, 2K | 0‡ | ~$0.07-0.35§ | 1K–2K |
| Flux Pro v1.1 | `flux-pro/v1.1` | High detail hero shots | — | ~$0.05 | TBD |
| Flux Pro v1.1 Ultra | `flux-pro/v1.1-ultra` | Money shots, CTA cards | — | ~$0.10 | TBD |

†NB2 (Gemini 3.1 Flash Image, launched Feb 26 2026) — **confirmed on AIMLAPI, $0.067/img at 1K**. Canary flag removed. Supports up to 14 reference images total (max 5 character identity refs, remainder for objects/vehicles/scenes). Context window 131K tokens (vs NBP's 65K) — handles more complex multi-ref prompts. **`thinking_level` is NOT a valid image generation API parameter** (2026-05-22 correction — previously documented incorrectly). Recommended for prompt iteration before final NBP Edit pass — saves ~$0.13/iteration.

**NB2 resolution tiers (Google official rates):** `"resolution": "512"` ($0.045/img, ~4-6s) → `"1K"` ($0.067/img) → `"2K"` ($0.101/img) → `"4K"` ($0.151/img). Use `"512"` for layout/composition checks before committing to 1K — saves ~33% per draft pass. Note: 512px is specified as `"512"` (no K suffix), not `"0.5K"`. AIMLAPI may map this to their own pricing tier — run a canary if using 512 for the first time.

**NB2 Image Search Grounding:** NB2 can pull real photos from Google Image Search before generating (e.g., Dutch residential streets, specific truck models). This uses a `google_search` tool with `search_types: ["image_search"]` in the native Gemini Interactions API format. **NOT available via AIMLAPI's OpenAI-compatible endpoint.** If you need real-world visual references, supply downloaded images as explicit refs instead.

‡GPT Image 2 supports up to **16 reference images** per call (every reference billed at high-fidelity input rate). Best use: CTA cards with complex Dutch text (e.g., phone numbers, URLs), text-heavy brand cards. AIMLAPI model string: `openai/gpt-image-2`. Confirmed `size` values: `1024x1536` (9:16 portrait), `1536x1024` (landscape), `1024x1024` (square). Quality tiers: `low`, `medium`, `high`. Run canary to verify AIMLAPI reference image support before using in production — OpenAI confirms it, AIMLAPI implementation unverified.

§GPT Image 2 uses token-based pricing on AIMLAPI — cost varies by resolution and prompt length. Run a $0.10 canary test to confirm exact cost before batch use. Use Imagen 4 Fast ($0.02) for iteration, GPT Image 2 only for finals requiring superior text accuracy.

**⚠️ IMAGEN 4 RETIREMENT — URGENT (2026-05-22):** All three Imagen 4 variants (`imagen-4.0-ultra-generate-001`, `imagen-4.0-generate-001`, `imagen-4.0-fast-generate-001`) retire **June 24, 2026 — 33 days away**. Google's official replacement: `gemini-3-pro-image-preview` = `google/nano-banana-pro` on AIMLAPI. Stop routing new jobs to Imagen 4 immediately. Migrate CTA/money-shot workflow to NBP Pro (`google/nano-banana-pro`, T2I) or NBP Edit (`google/nano-banana-pro-edit`, I2I with refs).

**Imagen 4 note (2026-05-08):** Imagen 4 is T2I only — no reference image input. Use for scenery, establishing shots, CTA cards, and text-heavy stills. For character or brand-asset shots requiring refs, use NBP Edit or Kontext Max. Imagen 4 Fast ($0.02) replaces NBP Pro as the cheapest non-ref draft tier. **[DEPRECATED — see retirement notice above]**

### Decision Flow

```
Shot has characters, need to iterate prompt? → NB2 Edit first ($0.07 at 1K, or $0.045 at 512px draft), then NBP Edit for approved final ($0.20)
Shot has characters (Karel/Mourad), final? → Nano Banana Pro Edit (existing refs as Image 1)
Shot has characters (new recurring)? → Create ref sheet first, then NBP Edit
Shot has brand assets but no people? → Nano Banana Pro Edit (truck/box refs) OR FLUX.2 Pro Edit (up to 3 refs on AIMLAPI)
Shot is pure scenery / B-roll? → Nano Banana Pro ($0.13) — Imagen 4 Fast RETIRING 2026-06-24
Shot needs pixel-perfect text on truck? → Flux Kontext Max I2I (best text rendering)
Shot needs brand-color still without input? → Flux Kontext Max T2I or Nano Banana Pro
Shot is the money shot / CTA hero? → Nano Banana Pro Edit (14 refs, T2I) — Imagen 4 Ultra RETIRING 2026-06-24
Shot needs flawless Dutch text (CTA card)? → GPT Image 2 (99% text accuracy) — run canary first
Need character chain-editing (4+ iterations)? → Kontext Pro ($0.052/img) over Kontext Max ($0.10) — better face stability, lower cost
```

## API Call Templates

### Nano Banana 2 Edit (draft/iteration — confirmed on AIMLAPI, ~$0.07/img)

Use NB2 for every prompt iteration pass before committing NBP Edit credits. Saves ~$0.13/pass.
**thinking_level is NOT a valid image API parameter** — do not add it to calls. (2026-05-22 correction)

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/nano-banana-2",
    "prompt": "Image 1: Mourad character reference sheet. Mourad-SV standing next to the truck cab, three-quarter view. Keep facial features identical to Image 1. Golden hour warm backlight, 85mm portrait, shallow DOF, vertical composition.",
    "image_urls": [mourad_sheet_url],
    "aspect_ratio": "9:16",
    "resolution": "1K",
    "num_images": 1,
    # NOTE: thinking_level is NOT a confirmed parameter for the image generation API endpoint.
    # It is a Gemini TEXT model parameter only. Do not add to image generation calls.
}, headers=headers, timeout=90)
hero_url = resp.json()["data"][0]["url"]
```

**thinking_level status (2026-05-22 UPDATE):**
- **NOT a confirmed API parameter for the image generation endpoint.** `thinking_level` applies to Gemini TEXT models only — the image generation API uses internal reasoning by default that cannot be controlled externally.
- Remove `thinking_level` from any image generation API calls. Model reasoning is handled server-side.
- Previous guidance (2026-05-16) was incorrect — it conflated text and image API parameters.

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

| Resolution | Nano Banana Pro | Kontext Max | Imagen 4 | Cost |
|------------|-----------------|-------------|----------|------|
| 1K | 768 x 1344 | 752 x 1392 | native 9:16 | ~$0.02-0.20 |
| 2K | 1536 x 2688 | — | Ultra only | ~$0.06 (Ultra confirmed) |
| 4K | 3072 x 5376 | — | — | ~$0.24 |

**Safe zone (2026-05-08):** On Instagram Reels / TikTok, platform UI (profile, caption, buttons) occludes the **top 14%** and **bottom 20%** of the frame. Keep all brand elements, faces, and text out of these zones. For a 768×1344 frame: top 107px and bottom 269px are danger zones. Compose the hero in the middle 66% of vertical height.

## Prompting Rules for NBP and NB2 (Gemini Image Models)

**NBP (Nano Banana Pro)** is the final-quality model. **NB2 (Nano Banana 2)** is the fast-iteration model — same prompting rules apply to both. Key difference: NB2 has a 131K token context window vs NBP's 65K, meaning NB2 can handle much longer multi-ref prompts without truncation risk. Use NB2 for all iteration passes; promote to NBP only when a composition is approved.

NBP/NB2 are "Thinking" models. Natural language outperforms tag soup.

### Face Identity Header Rule (2026-05-20)

**Gemini processes prompts sequentially — earlier text carries more weight.** For character shots, ALWAYS open with a compact identity header BEFORE the scene description:

```
IDENTITY LOCK — Mourad-SV: warm olive skin, strong jawline, dark brown eyes, short black beard, mid-30s.
Maintain exact facial structure from Image 1: same eye spacing, nose width, jaw contour, skin texture.
Do not modify facial proportions. Do not age or beautify. No freckles. No beard modifications.
[Scene description follows here...]
```

**Hard constraint format** (confirmed effective per Google AI Developers Forum):
- "Do not change facial proportions, eye spacing, nose width, jawline contour"
- "Do not age the character. No freckles. No beauty filter."

**Single-subject shots** preserve identity at acceptable rates (~85-90%). **Multi-person shots** have consistent identity preservation failures — never place Mourad AND Karel in the same NBP generation. Generate each character separately and composite in post.

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

### Strong Verb at Start (2026-05-12)

Google official guidance: **start every prompt with a strong verb** that tells the model the primary operation to perform. This improves prompt adherence.

```
✗ WEAK:  "Mourad standing next to the truck, golden hour..."
✓ STRONG: "Generate Mourad standing next to the truck, golden hour..."
✓ STRONG: "Create a cinematic hero frame of Mourad lifting a box..."
✓ STRONG: "Render a wide establishing shot of a Dutch residential street..."
```

### Positive Framing Rule (2026-05-12)

Google official guidance: **describe what you want, not what you don't want.** Use positive language where possible.

| Weak (negative) | Strong (positive) |
|----------------|-------------------|
| "no cars in the street" | "empty residential street, clear pavement" |
| "no blur" | "sharp focus, crisp detail" |
| "no yellow, no gold" | "bright orange #FC8434 only" |

**Exception:** For brand-critical structural elements where ambiguity could be costly, explicit exclusions remain appropriate alongside positive framing:
```
"White sealed cargo box with smooth flat panels [positive].
No side door or sliding panel cutout [explicit — brand binary]."
```

### Trait Locking — Verbatim Descriptor Reuse (2026-05-12)

For multi-shot productions: **use the exact same descriptor words verbatim in every prompt.** Swapping synonyms causes identity drift.

```
✗ DRIFT:  Prompt 1: "olive complexion, dark beard" | Prompt 2: "tan skin, black stubble"
✓ LOCKED: ALL prompts: "warm olive skin, short black beard, dark brown eyes, strong jawline"
```

Mourad canonical trait lock (copy verbatim into every prompt):
```
warm olive skin, strong jawline, dark brown eyes, short black beard, mid-30s
```

### Character Unique Tag (2026-05-12)

Give each recurring character a short unique tag and include it in every prompt. The model anchors on named identities.

```
"Mourad-SV [short tag]: warm olive skin, strong jawline, dark brown eyes, short black beard, black crewneck with orange chest logo, blue jeans, white sneakers."
```

Add the tag + one-line descriptor at the START of every character prompt, before the scene description.

### Font Specification for Typography in NBP (2026-05-12)

NBP (Gemini 3 Pro) supports named fonts directly in the prompt — more reliable than generic descriptions:

```
✓ "Display 'SNELVERHUIZEN.NL' in a bold, clean sans-serif font, white text, orange background #FC8434"
✓ "Render '085 3331133' in Century Gothic, 14px weight, left-aligned"
✓ "Large Impact-style headline 'VERHUIZEN ZONDER ZORGEN', orange #FC8434"
```

**Text-first hack:** For best NBP text rendering, converse with the model first to generate the text concepts, then request the image. (Google official tip, 2026.) Works well for CTA cards and label text.

**Note:** Despite NBP's strong text rendering, truck text (SNELVERHUIZEN.NL) is still safer as post-overlay due to garbling risk on curved/lit surfaces. Use NBP font naming for flat CTA card designs only.

### Other Rules

- Wrap text in quotes: `displaying "SNELVERHUIZEN" in bold white sans-serif`
- Prompts over ~200 words trigger internal summarization — keep concise
- NO seed, guidance scale, or CFG parameters (NBP is autoregressive, not diffusion — seed reproducibility does not apply)
- **safety_settings (2026-05-22):** Two distinct block behaviors: `blockReason: SAFETY` = pre-generation block (configurable via safety thresholds); `blockReason: IMAGE_SAFETY` = post-generation output block (also configurable). `blockReason: OTHER` is non-configurable. If a generation fails silently, check the response for blockReason field before retrying. For modest-dress character shots, IMAGE_SAFETY false-positives can occur — log the blockReason and escalate to owner rather than retrying blindly.
- **Gemini 3.5 Flash (2026-05-19):** Text-output-only model. Does NOT generate images. Not an upgrade path for hero frames. Image generation pipeline remains: NB2 (draft) → NBP Edit (final) → Imagen 4 Ultra (CTA/money shots).

### Reference Image Rules (NBP Edit)

- Label every image: "Image 1: Mourad character sheet. Image 2: Truck reference."
- Control via natural language: "Use Image 1 as a strict identity reference"
- **Identity lock formula:** "Maintain the exact same facial features as Image 1 — same eyes, nose shape, jawline contour, and skin texture." (more specific than generic "keep face the same")
- **Add text description of distinctive features** alongside the image ref: e.g., "Mourad: warm olive skin, strong jawline, dark brown eyes, short black beard" — text reinforces the visual anchor
- Explicitly remove objects from previous scenes ("No longer holding the clipboard")
- Character sheet MUST be Image 1 in every call for character shots
- **Max 14 images total, BUT only 5 can be human/person identity references.** Remaining 9 slots are for objects, vehicles, and scenes. Do NOT exceed 5 human refs or identity anchoring degrades. For strict structural accuracy, cap total uploads at 6 high-quality refs even if quota allows more. (Confirmed by community guides apiyi.com, laozhang.ai 2026 — going beyond 6 shows no quality gain and may introduce conflicting information.)
- **NB2 (Gemini 3.1 Flash Image) ref limits differ:** up to 10 object fidelity refs, but only 5 character consistency refs. Same 6-cap guidance applies.
- **Reference image quality spec (2026-04-21):** Minimum resolution 1024×1024. Face must occupy **30–50% of the frame area** — tighter crops produce better identity anchoring than full-body shots used as the sole reference. Sub-30% face coverage = identity drift; sub-1024px = detail loss in identity latent.
- First-pass consistency rates: character-sheet workflow = 85-90%; single hero image without sheet = 60-70%
- **Chain update technique (2026-05-08):** Include the PREVIOUS output as one of the reference images when making incremental edits. This reduces drift across multi-pass generation by giving the model a visual anchor of the last state. Remind it explicitly each call to preserve hair, clothing, and facial features.
- **Iterative refinement loop (2026-05-22):** After each generation pass, use the BEST output from that pass as an additional reference in the next call — alongside the original character sheet. Community-confirmed: achieves 90%+ consistency across 50+ image batches. Loop: generate batch → pick best → add as Image 2 alongside original sheet → generate next batch → repeat. Stop when identity is locked (face distance < 0.4 cosine).

### Multi-Reference Role Assignment (2026-04-27)

Assign a ROLE to each reference image, not just a name. The model reads role assignments and applies refs selectively. **Note (2026-05-08): There is NO structured `role` API field — this is prompt-level instruction only. Effectiveness is prompt-dependent, not guaranteed.** Still worth doing — community data shows it reduces bleed.

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

**Flux Kontext Max Multi (2026-05-22):** BFL released a multi-reference variant. On fal.ai: `fal-ai/flux-pro/kontext/max/multi`; on Replicate: `multi-image-kontext-max`. **NOT confirmed on AIMLAPI as of 2026-05-22.** AIMLAPI Kontext endpoints remain single-reference. Workaround: composite character + truck into one reference image (FFmpeg hstack) before calling the API, rather than passing two separate refs. Monitor `docs.aimlapi.com/api-references/image-models/flux` for a multi endpoint.

- 30-80 word sweet spot, maximum 512 tokens
- FLUX does NOT support CLIP-style weighting — `(keyword:1.5)` is silently ignored
- Token hierarchy: subject > action/pose > environment > lighting > style
- For SNELVERHUIZEN.NL text: always use quotation marks, ALL CAPS, specify "bold clean sans-serif". Text editing format: `Replace '[original text]' with '[new text]'`
- If text morphs: generate truck text-free, composite in post
- **ONE change per call** — progressive editing only. Change background first → then lighting → then details. Stacking multiple changes in one prompt degrades quality.
- Refer to subjects by description, not pronouns: "the man with the black crewneck" not "him"
- Character identity: uses AuraFace embeddings; maintains cosine similarity >0.92 across 6 successive edits (vs ~0.80 for competing models). This means ≤6 edits from original ref before restarting chain.
- `guidance_scale` range on AIMLAPI: 1–20. **Default is 3.5.** Two regimes: (1) character/face editing → use 2.0–2.5 (more image-preserving, prevents face warp; 2.0 is the confirmed lower bound for stable face output); (2) text/typography editing → use 3.5–4.0 (more prompt-literal for letter accuracy). Do not exceed 5 for character editing — face structure distorts. Note: other platforms (Replicate, fal.ai) use a different guidance_scale range (1–50) — do not import their settings.
- **`image_strength`** (0–1, default 0.1): Controls how much the reference image influences the output. **Status: UNVERIFIED on AIMLAPI Kontext endpoint** — may not be exposed. If available: increase to 0.3–0.5 for stronger face identity lock (higher = more reference-faithful, less prompt flexibility). Run canary to confirm parameter is accepted before relying on it.
- **Multi-image on AIMLAPI**: `image_url` accepts an array. AIMLAPI docs confirm **2 reference images** in examples. BFL-native supports up to 8-10, but higher counts on AIMLAPI are UNVERIFIED. Do not assume 8 slots — treat 2 as confirmed max until canary proves otherwise.
- `num_inference_steps`: not exposed on AIMLAPI I2I endpoint (handled server-side). For T2I endpoint: 20-50 steps; use 28 for drafts, 50 for production finals.
- **`prompt_upsampling`**: When `true`, an LLM rewrites the prompt for richer output — but results are NOT reproducible across calls. For character editing and brand-critical shots, set `prompt_upsampling: false` to maintain reproducibility. For T2I scenery shots where variation is acceptable, leaving it true may improve output. Status on AIMLAPI's Kontext endpoint: UNVERIFIED — may be handled server-side. Use `false` explicitly if the parameter is exposed.

### Max vs Pro — When to Use Which (2026-05-18)

| Capability | Kontext Max | Kontext Pro |
|-----------|-------------|-------------|
| Typography / text rendering | **Max wins** — cleaner letterforms | Competent but slightly less refined |
| Style transfers (global) | **Max wins** — more believable | Sometimes inconsistent |
| Character identity across ≥4 chain edits | Pro more reliable | **Pro wins** — fewer subtle face drifts |
| Complex multi-attribute edits | **Max wins** — handles priority better | Sometimes deprioritizes elements |

**Pipeline routing (2026-05-18):** Use **Max** for text/typography shots (SNELVERHUIZEN.NL renders), style transfers, and complex multi-attribute edits. Use **Pro** (`flux/kontext-pro/image-to-image`, $0.052 on AIMLAPI) for pure character chain-editing requiring 4+ sequential iterations — Pro delivers more stable face identity at half the cost. Both confirmed on AIMLAPI. For new characters: start with Pro to build identity chain, switch to Max only if you need text-on-image precision.

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

## Face Consistency QA Tools

Two scriptable options for automated face similarity checks between generated frames:

| Tool | GitHub | Method | Threshold |
|------|--------|--------|----------|
| **InsightFace** | `deepinsight/insightface` | ArcFace embeddings | cosine >0.6 = same person |
| **DeepFace** | `serengil/deepface` (2026-active) | Wraps ArcFace, FaceNet512, VGG-Face, GhostFaceNet | cosine >0.6 = same person |

DeepFace is a practical drop-in alternative to InsightFace — actively maintained, wider model choice, identical interface pattern. Use Facenet512 backend for best accuracy on cropped faces.

```python
from deepface import DeepFace
result = DeepFace.verify(img1_path="ref_face.jpg", img2_path="generated_frame.jpg",
                         model_name="Facenet512", distance_metric="cosine")
is_same = result["verified"]  # True if cosine distance < threshold
```

Run this check on every hero frame before sending to owner for approval. Rejection threshold: if cosine distance > 0.4 (i.e. similarity < 0.6), flag for regeneration.

## Imagen 4 API Templates (2026-05-08)

### Imagen 4 Fast — cheapest draft ($0.02)

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/imagen-4.0-fast-generate-001",
    "prompt": "A quiet Dutch residential street at golden hour. Red-brick facades, clean pavement. No people. Wide establishing shot, vertical composition.",
    "aspect_ratio": "9:16",
    "num_images": 1,
}, headers=headers, timeout=60)
hero_url = resp.json()["data"][0]["url"]
```

### Imagen 4 Ultra — money shots / CTA (max quality, 2K)

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/imagen-4.0-ultra-generate-001",
    "prompt": "CTA card: clean white background, large bold orange text 'SNELVERHUIZEN.NL', orange #FC8434, professional Dutch design, 9:16 vertical. No people. No additional text.",
    "aspect_ratio": "9:16",
    "num_images": 1,
    "enhance_prompt": False,      # FALSE for brand-critical prompts — prevents LLM rewriting HEX colors and exact text
    "person_generation": "allow_adult",  # Required for shots with Mourad/Karel; default is "allow_adult" but set explicitly
    # "seed": 12345,             # CANARY REQUIRED — seed may be supported on Imagen 4 (diffusion); NOT supported on NBP (autoregressive)
    # NOTE: add_watermark parameter does NOT exist. SynthID invisible watermark is embedded at pixel level and cannot be removed via API.
}, headers=headers, timeout=90)
hero_url = resp.json()["data"][0]["url"]
```

**`enhance_prompt` guidance (2026-05-20):**
- `True` (default): Gemini LLM rewrites the prompt to add richness — good for scenery and B-roll where variation is acceptable
- `False`: Prompt sent verbatim — **always use for brand-critical shots** (truck text, phone numbers, HEX colors, CTA cards). Prevents the model from substituting your exact #FC8434 or "085 3331133" with paraphrased equivalents.

**CANARY NOTE:** Imagen 4 pricing on AIMLAPI — run a $0.10 test before batch production use to verify exact cost per image and response structure. Model strings confirmed in AIMLAPI docs as of 2026-05.

### GPT Image 2 — CTA Cards with Dutch Text (2026-05-16)

Use ONLY for CTA cards and text-heavy brand stills. T2I only, no reference image support. Strength: 99% text accuracy in Dutch vs ~60% for older models. Token-based pricing — run canary before production.

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "gpt-image-2",
    "prompt": "Clean professional CTA card on white background. Large bold orange text reading 'SNELVERHUIZEN.NL' centered at top. Below it in smaller text: '085 3331133'. Below that: 'VERHUIZEN ZONDER ZORGEN' in bold. Orange is exactly #FC8434. 9:16 vertical format. Minimal design, no people, no decoration.",
    "size": "1024x1536",   # confirmed 9:16 portrait — values must be divisible by 16, ratio 1:3 to 3:1
    "quality": "high",
    "n": 1,
}, headers=headers, timeout=120)
hero_url = resp.json()["data"][0]["url"]
```

**CANARY REQUIRED:** GPT Image 2 uses token-based pricing on AIMLAPI. Run one test call and check actual cost before committing to a batch. Confirm `size` parameter values accepted by AIMLAPI. If cost exceeds $0.20/image, fall back to Imagen 4 Ultra for text stills.

## NBP → Veo Keyframe Bridge (2026-05-12)

Official Google workflow: generate hero keyframes with NBP, then use Veo to animate between them.

```
Step 1: Generate shot start frame with NBP Edit (approved, QA passed)
Step 2: Generate shot end frame with NBP Edit (approved, QA passed)
Step 3: Pass START frame as image_url to Veo I2V with motion prompt
        — Veo animates from that anchor toward the end state
```

Benefit: brand accuracy from the NBP hero-frame QA gate carries through to the animation. Reduces ghost-driving and off-brand drift compared to T2V. Best for predictable action pairs: Mourad lifts box → box loaded, door open → door closed.

---

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

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

## ⚠️ JUNE 25, 2026 — PREVIEW MODEL SHUTDOWN (11 days away as of 2026-06-14) — CANARY NOW URGENT

Google is retiring both Gemini image preview models on **June 25, 2026**:
- `gemini-3-pro-image-preview` → GA replacement: `gemini-3-pro-image`
- `gemini-3.1-flash-image-preview` → GA replacement: `gemini-3.1-flash-image`

**Google recommended migration deadline: June 20, 2026** — that is 6 days from today. After June 25, all calls to `-preview` native model IDs will fail. AIMLAPI's routing aliases should buffer this (see below), but run the canary NOW.

**AIMLAPI routing note:** AIMLAPI model strings `google/nano-banana-pro`, `google/nano-banana-pro-edit`, and `google/nano-banana-2` are AIMLAPI's OWN routing aliases — they do NOT pass the `-preview` suffix to Google. This means they should survive the June 25 shutdown IF AIMLAPI has already migrated their backend routing to the GA model IDs. AIMLAPI's doc URLs still reference `-preview` internally, but this is a documentation artifact, not the API string you pass. **Run a canary call on `google/nano-banana-pro-edit` BEFORE JUNE 20 to confirm.** If calls return 404/model-not-found after June 25, contact AIMLAPI support immediately — do NOT assume the pipeline is broken before checking.

## Critical Rules

1. **MUST generate natively in 9:16** for vertical platforms. NEVER crop, zoom, or pad a square image.
2. **MUST generate ONE image at a time.** Verify the output before generating the next.
3. **MUST use reference images** for any shot containing brand assets (truck, uniform, boxes).
4. **MUST run full QA** (8 dimensions + Shari'ah + cinematic quality) on every hero frame before sending to I2V.
5. **MUST send hero frames to owner for approval** before spending video credits on animation. MUST NOT animate without owner sign-off.

## Model Selection Matrix

| Model | AIMLAPI String | Best For | Max Refs | Cost | 9:16 Output |
|-------|---------------|----------|----------|------|-------------|
| Gemini 2.5 Flash Image | `google/gemini-2.5-flash-image`‖ | Ultra-cheap T2I layout/composition drafts (no refs, no reasoning). Use ONLY before NB2 pass when you need rough placement check — NOT for character or brand shots | 0 | ~$0.039 | native 9:16 |
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
| FLUX.2 Max | `blackforestlabs/flux-2-max`⁑ | Highest quality T2I, up to 10 refs — when Kontext Max 2-ref limit is insufficient | 10 | ~$0.09 | native |
| GPT Image 1.5 | `openai/gpt-image-1.5`✩ | Step-up from GPT Image 1; supports text-to-image, editing, and variations; better instruction following than GPT Image 1; 20% cheaper per-image I/O vs GPT Image 1 | 16 | ~$0.04-0.28 | 1K–2K |
| GPT Image 2 | `openai/gpt-image-2` | CTA cards requiring pixel-perfect Dutch text; 99% text accuracy, 2K; up to 16 refs | 16‡ | ~$0.07-0.35§ | 1K–2K–4K |
| Flux Pro v1.1 | `flux-pro/v1.1` | High detail hero shots | — | ~$0.05 | TBD |
| Flux Pro v1.1 Ultra | `flux-pro/v1.1-ultra` | Money shots, CTA cards | — | ~$0.10 | TBD |
| Grok Imagine Quality | `x-ai/grok-imagine-image-quality`† (**CANARY — Pro deprecated 2026-05-15**) | T2I + I2I scenery drafts; 3 refs; strong text | 3 | ~$0.055 (1K), ~$0.07 (2K) | 9:16 native |
| Qwen Image Edit | `alibaba/qwen-image-edit`✦ | Surgical text edits within existing images; background/object removal; fallback when NBP blockReason OTHER fires | 2–3 | ~$0.059 | native |
| Seedream 4.5 | `bytedance/seedream-4-5`✧ | T2I + I2I with up to 14 refs; portrait/character editing with strong face fidelity; fallback when NBP blockReason OTHER fires | 14 | $0.052 | 9:16 native |
| Seedream 5.0 Lite | `bytedance/seedream-5-0-lite-preview`✧ | T2I + I2I (image_urls supported); chain-of-thought reasoning; draft-tier, cheaper than NB2 | 14 | ~$0.035 | 9:16 (`"9:16"` in size param) |

‖**Gemini 2.5 Flash Image (2026-05-28):** The original "Nano Banana" (Gemini 2.5 Flash Image) is available on AIMLAPI at ~$0.039/img. T2I only, no reference images, no Gemini 3 reasoning. Use ONLY as a sub-NB2 draft tier for rough composition/layout checks before committing NB2 credits. Do NOT use for character or brand-critical shots — quality is significantly below NB2. **AIMLAPI model string `google/gemini-2.5-flash-image` — run canary to confirm before production use.** Native 9:16 output. Pricing: ~42% cheaper than NB2 ($0.039 vs $0.067 at 1K).

†NB2 (Gemini 3.1 Flash Image, **GA as of 2026-05-28**) — **confirmed on AIMLAPI, $0.067/img at 1K**. Canary flag removed. Native GA model ID: `gemini-3.1-flash-image` (no `-preview`). AIMLAPI model string: `google/nano-banana-2` (confirmed). Supports up to 14 reference images total (max 5 character identity refs, remainder for objects/vehicles/scenes). Context window 131K tokens (vs NBP's 65K) — handles more complex multi-ref prompts. **`thinking_level` on AIMLAPI: NOT exposed.** The GA release (May 28, 2026) added configurable thinking modes (Minimal/default, High) accessible via the native Google Interactions API / Python SDK `ThinkingConfig`. However, AIMLAPI's stateless `/v1/images/generations` endpoint does NOT expose `thinking_level` — it is absent from AIMLAPI's documented parameters for this model. Do not pass `thinking_level` via AIMLAPI calls. (Corrects the 2026-05-22 note: the parameter IS valid at the native Google API level, but NOT via AIMLAPI's proxy.) Recommended for prompt iteration before final NBP Edit pass — saves ~$0.13/iteration. **Video-to-image (Preview, 2026-06-10 update):** NB2 officially supports video files as input — pass a video file or public YouTube URL alongside a text prompt to generate thumbnails, keyframes, or stills from approved footage. Listed as a **video-to-image (Preview)** feature in the Google Cloud GA announcement blog (May 28, 2026). The model analyzes visual context, subjects, and actions within the video to generate context-aware images. **Not yet confirmed on AIMLAPI's `/v1/images/generations` endpoint** — AIMLAPI's stateless proxy may not expose the video input path; run a canary before relying on it in production.

**NB2 resolution tiers (Google official rates):** `"resolution": "512"` ($0.045/img, ~4-6s) → `"1K"` ($0.067/img) → `"2K"` ($0.101/img) → `"4K"` ($0.151/img). Use `"512"` for layout/composition checks before committing to 1K — saves ~33% per draft pass. Note: 512px is specified as `"512"` (no K suffix), not `"0.5K"`. AIMLAPI may map this to their own pricing tier — run a canary if using 512 for the first time.

**NBP (Nano Banana Pro) 2K = same price as 1K (2026-06-10 update — community confirmed):** Google's native API prices both `"1K"` and `"2K"` for NBP at **$0.134/image** — they consume the same token count (~1,120 output tokens). This means 2K (1536×2688px) is a free quality upgrade over 1K (768×1344px). Confirmed by multiple independent sources (laozhang.ai, aifreeapi.com, evolink.ai) as of June 2026. **AIMLAPI billing not independently verified — run one canary call with `"resolution": "2K"` before switching all production calls.** If AIMLAPI charges the same, update all NBP production calls from `"1K"` to `"2K"` — free resolution doubling.

**Google Batch API — 50% off NBP (native Google API only):** Google's Batch API gives 50% off all image generation: 2K drops from $0.134 → **$0.067**, 4K from $0.24 → $0.12. Async processing, typical turnaround 2-6h (target 24h). **NOT available via AIMLAPI** — AIMLAPI doesn't expose the Batch API endpoint. Relevant only if the AIMLAPI-only constraint is relaxed in the future.

**4K output — confirmed unstable, do NOT use in production (2026-06-12 update):** Google Cloud blog confirms 1K and 2K are GA-stable for both NBP and NB2. 4K output is still in Preview AND is confirmed unstable in practice: (a) 4K compute load is 256× that of 1K; (b) the January 21, 2026 NBP API outage was specifically 4K timeout failures; (c) 4K file sizes dropped from ~30MB to ~8MB in April 2026, indicating Google compute-throttling 4K output behind the scenes. Stability expected to improve by mid-2026 when TPU v7 ramp-up completes — reassess then. **Until confirmed stable: use 2K for all production hero frames.** 2K is a free quality upgrade from 1K for NBP (same token cost), so there is no reason to attempt 4K in production today.

**NB2 Image Search Grounding:** NB2 can pull real photos from Google Image Search before generating (e.g., Dutch residential streets, specific truck models). This uses a `google_search` tool with `search_types: ["image_search"]` in the native Gemini Interactions API format. **NOT available via AIMLAPI's OpenAI-compatible endpoint.** If you need real-world visual references, supply downloaded images as explicit refs instead.

‡GPT Image 2 (`openai/gpt-image-2`, released 2026-04-21) supports up to **16 reference images** per call (every reference billed at high-fidelity input rate). Best use: CTA cards with complex Dutch text (e.g., phone numbers, URLs), text-heavy brand cards. **⚠️ CRITICAL parameter notes:** (1) Do NOT pass `input_fidelity` — this parameter does not exist on GPT Image 2 and will cause the request to fail (exists on older models only; GPT Image 2 always processes at high fidelity). (2) `background: "transparent"` is NOT supported — requests with this param will fail. Size: custom dimensions, both edges multiples of 16, max 3840px per edge, ratio under 3:1, total pixels 655,360–8,294,400. Recommended 9:16 size: `1152x2048` (true 9:16, both divisible by 16). Quality tiers: `low`, `medium`, `high`. Output format: `png` (default), `jpeg`, `webp`. Run canary to verify AIMLAPI reference image support before using in production — OpenAI confirms it, AIMLAPI implementation unverified. 3–5 well-chosen refs outperform 16 mixed ones.

§GPT Image 2 uses token-based pricing on AIMLAPI — cost varies by resolution and prompt length. Run a $0.10 canary test to confirm exact cost before batch use. Use Gemini 2.5 Flash Image ($0.039) or NB2 ($0.045 at 512px) for cheap iteration drafts; GPT Image 2 only for finals requiring superior Dutch text accuracy. Imagen 4 Fast **retires June 24, 2026** — do not use as iteration fallback.

**GA model IDs clarification (2026-06-03):** Google's native GA model strings are `gemini-3-pro-image` (NBP) and `gemini-3.1-flash-image` (NB2). AIMLAPI wraps these under `google/nano-banana-pro`, `google/nano-banana-pro-edit`, and `google/nano-banana-2` — these AIMLAPI strings are unchanged and should continue working post-June-25 assuming AIMLAPI updates their backend routing. The `-preview` suffix is in AIMLAPI's internal doc URLs but NOT in the model strings you pass in API calls. Run a canary before June 22 to confirm.

⁑**FLUX.2 Max (2026-05-31):** BFL's highest-quality T2I/I2I model. Available on AIMLAPI as `blackforestlabs/flux-2-max` — **CANARY REQUIRED** to confirm exact model string and parameter support. Pricing: ~$0.091/megapixel at BFL-native; ~$0.09/img at 1K on AIMLAPI (slightly more than Kontext Max but similar). Supports up to **10 reference images** — the key advantage over Kontext Max's 2-ref AIMLAPI ceiling. Use case: brand compositing shots needing more than 2 refs (character + truck + boxes + background scene) without paying NBP Edit prices. Do NOT use for character chain-editing — Kontext Pro/Max is better for sequential face edits. Run canary before production use.

†**Grok Imagine Image Quality (2026-06-14 update):** xAI launched `grok-imagine-image-quality` on 2026-05-06 (consumer) / API available 2026-05-06. Predecessor `grok-imagine-image-pro` deprecated **2026-05-15** — do not use. Supports T2I and I2I editing with up to 3 reference images. 9:16 via `aspect_ratio: "9:16"`. Strong text rendering and photorealism. Practical use: cheap B-roll / environment drafts ($0.055 < NBP Pro's $0.13) when character accuracy isn't required. **AIMLAPI model string status (2026-06-14):** AIMLAPI docs confirm two separate xAI image model pages: `x-ai/grok-imagine-image` (base model, older) and `x-ai/grok-imagine-image-pro` (deprecated May 15). The Quality model's expected AIMLAPI string is **`x-ai/grok-imagine-image-quality`** (following AIMLAPI's x-ai/ naming convention) — **CANARY REQUIRED** to confirm this string is live. Prompt syntax and parameters are identical between Pro and Quality — no prompt changes needed when migrating. Do NOT use for character shots (no identity sheet support beyond 3 refs; no face adherence features).

✩**GPT Image 1.5 (2026-06-12):** Available on AIMLAPI as `openai/gpt-image-1.5`. Released December 2025 — sits between GPT Image 1 and GPT Image 2 in the OpenAI image generation family. Supports text-to-image generation, image editing, and variations. Key improvement over GPT Image 1: better instruction following on small details (changes what you ask for while keeping lighting, composition, and likeness stable across edits). Image I/O costs 20% cheaper than GPT Image 1. **For our pipeline:** Lower priority than GPT Image 2 for CTA cards (GPT Image 2 has better Dutch text accuracy at 99%). Consider as a cost-efficient alternative when GPT Image 2 pricing is prohibitive for draft-tier CTA cards. **CANARY REQUIRED** to verify exact AIMLAPI model string and parameter support — `openai/gpt-image-1.5` is the expected string based on AIMLAPI naming conventions for OpenAI models.

✦**Qwen Image Edit (2026-06-02):** Available on AIMLAPI as `alibaba/qwen-image-edit` at ~$0.059/img. Primary use case: surgical edits on existing images — text corrections within a generated frame, background replacement when NBP fires `blockReason: OTHER`, precise object removal/insertion. Supports 2-3 reference images. NOT a replacement for NBP Edit on multi-ref character compositing (no 14-ref support, no character-sheet identity anchoring). Use as a fallback when NBP Edit is blocked by the March 2026 policy tightening. AIMLAPI model string confirmed. **CANARY REQUIRED** to verify exact parameter names and response structure before production use. Qwen-Image-2.0 (Feb 2026, 2K native, professional typography) is available via Alibaba DashScope but NOT confirmed on AIMLAPI — do not route to it until canary confirms.

✧**Seedream 4.5 and 5.0 Lite Preview (2026-06-06, AIMLAPI docs confirmed):** ByteDance Seedream models confirmed on AIMLAPI with the following verified specs:

**Seedream 4.5** (`bytedance/seedream-4-5`, $0.052/img): T2I + I2I via `image_urls` array (min 1, max 14 images — same slot count as NBP Edit). `size` parameter accepts `2K`/`4K` presets or custom pixel dimensions; supports 9:16. `seed` parameter supported. Significantly improved editing consistency vs v4.0 (preserves subject details, lighting, colour tone). At $0.052 vs NBP Edit's $0.195, this is a 73% cost saving if quality is acceptable — CANARY REQUIRED before production use. Primary use case: blockReason OTHER fallback for character composites; secondary: cheaper prompt iteration with refs (vs NB2 at $0.067).

**Seedream 5.0 Lite Preview** (`bytedance/seedream-5-0-lite-preview`, ~$0.035/img — pricing unconfirmed on AIMLAPI pricing page directly): T2I + I2I via `image_urls`. Supports 9:16 via `size: "9:16"` literal string. Also accepts ratio strings (`"4:5"`, `"3:4"`) and pixel formats. Chain-of-thought reasoning enabled. Optional web search grounding add-on ($0.0069/call). Cheaper than NB2 at $0.067 if pricing confirms. CANARY REQUIRED.

**Both models:** Do NOT use as primary character model until canary confirms face adherence vs. NBP Edit baseline. Parameter names (other than `prompt`, `image_urls`, `size`, `seed`) may differ from NBP/Kontext — verify in canary.

**Ideogram 4.0 (2026-06-03, NOT yet on AIMLAPI — future candidate):** Released June 3, 2026 as an open-weight foundation model (9.3B parameters). Key specs: English OCR accuracy **0.97** (highest confirmed for any image model — surpasses GPT Image 2 for text accuracy), native 2K output, JSON structured prompting (specify bounding boxes, color palettes, layout zones via JSON), multilingual text, transparent background support. Weights are downloadable (self-hostable + fine-tunable). **Not confirmed on AIMLAPI** as of 2026-06-14 — available via Ideogram native API, Runware, and potentially others. If AIMLAPI adds it, expected string: `ideogram/ideogram-4.0`. **CTA card use case:** If confirmed on AIMLAPI, Ideogram 4.0 may displace GPT Image 2 for Dutch text accuracy on CTA cards given its 0.97 OCR score. Monitor AIMLAPI model additions; run canary when/if available.

**⚠️ IMAGEN 4 RETIREMENT — CRITICAL (2026-06-08 update):** All three Imagen 4 variants (`imagen-4.0-ultra-generate-001`, `imagen-4.0-generate-001`, `imagen-4.0-fast-generate-001`) retire **June 24, 2026 — 16 days away**. Google's official replacement: `gemini-3-pro-image` = `google/nano-banana-pro` on AIMLAPI. Stop routing new jobs to Imagen 4 immediately. Migrate CTA/money-shot workflow to NBP Pro (`google/nano-banana-pro`, T2I) or NBP Edit (`google/nano-banana-pro-edit`, I2I with refs). Gemini 2.5 Flash Image (`gemini-2.5-flash-image`) shuts down **October 2, 2026**.

**Imagen 4 note (2026-05-08):** Imagen 4 is T2I only — no reference image input. Use for scenery, establishing shots, CTA cards, and text-heavy stills. For character or brand-asset shots requiring refs, use NBP Edit or Kontext Max. Imagen 4 Fast ($0.02) replaces NBP Pro as the cheapest non-ref draft tier. **[DEPRECATED — see retirement notice above]**

### Decision Flow

```
Need ultra-cheap T2I layout/composition draft (no chars, no refs)? → Gemini 2.5 Flash Image ($0.039) — run canary first (model string unverified)
Shot has characters, need to iterate prompt? → NB2 Edit first ($0.07 at 1K, or $0.045 at 512px draft), then NBP Edit for approved final ($0.20)
Shot has characters (Karel/Mourad), final? → Nano Banana Pro Edit (existing refs as Image 1)
Shot has characters (new recurring)? → Create ref sheet first, then NBP Edit
Shot has brand assets but no people? → Nano Banana Pro Edit (truck/box refs) OR FLUX.2 Pro Edit (up to 3 refs on AIMLAPI) OR FLUX.2 Max (up to 10 refs, ~$0.09 — canary first)
Need 4+ brand refs without character? → FLUX.2 Max over FLUX.2 Pro Edit (10 refs vs 3)
Shot is pure scenery / B-roll? → Nano Banana Pro ($0.13) — Imagen 4 Fast RETIRING 2026-06-24
Shot needs pixel-perfect text on truck? → Flux Kontext Max I2I (best text rendering)
Shot needs brand-color still without input? → Flux Kontext Max T2I or Nano Banana Pro
Shot is the money shot / CTA hero? → Nano Banana Pro Edit (14 refs, T2I) — Imagen 4 Ultra RETIRING 2026-06-24
Shot needs flawless Dutch text (CTA card)? → GPT Image 2 (99% text accuracy) — run canary first
Budget CTA card draft (not final)? → GPT Image 1.5 (~$0.04-0.28, 20% cheaper per I/O than GPT Image 1, better instruction following) — CANARY REQUIRED before use
Need character chain-editing (4+ iterations)? → Kontext Pro ($0.052/img) over Kontext Max ($0.10) — better face stability, lower cost
Hero frame passed most QA but has 1 brand failure? → NBP Edit inpainting ($0.20) — fix only the failing element, not full regen
Need cheap B-roll scenery draft (no characters)? → Grok Imagine Quality ($0.055, `x-ai/grok-imagine-image-quality`) — CANARY REQUIRED (Pro deprecated May 15; Quality string unverified on AIMLAPI)
NBP Edit returns blockReason OTHER (March 2026 policy)? → (1) Use stylized ref + add "fictional, illustrated character" to prompt (60-70% block reduction); (2) if still blocked: Seedream 4.5 ($0.052, 14 refs, canary first) or Qwen Image Edit ($0.059) for I2I fallback; (3) T2I describe-the-scene fallback; (4) **Model-switch**: try NB2 Edit with the same refs and prompt — NB2 and NBP use separate enforcement paths, and a call blocked on NBP sometimes succeeds on NB2 (community report June 2026, unverified — treat as last resort before T2I fallback)
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
- **blockReason: OTHER — March 2026 policy tightening (CRITICAL, 2026-06-10 update):** Google significantly expanded `blockReason: OTHER` in March 2026 to cover person-related editing operations: uploading a reference photo of a person and asking to change their background, composite them into a new scene, or modify appearance now frequently returns `blockReason: OTHER`. This is a policy-level restriction — safety_settings adjustments have NO effect. **Our characters are AI-generated (not real people), but NBP cannot reliably distinguish them from real-person photos.** Five mitigations (in priority order): (1) **Use stylized/illustrated reference frames** — photorealistic character refs trigger the policy most often; slightly illustrated or rendered refs (even minor stylization) significantly reduce OTHER blocks. Add "fictional, illustrated character" to the prompt alongside a stylized ref for maximum reduction (confirmed community guidance 2026). (2) **T2I fallback**: Describe the scene in text with the character's features spelled out rather than uploading a reference photo — avoids the "editing real person photo" trigger entirely. (3) **Segmentation composite**: Use BiRefNet or rembg to extract the character silhouette from the approved hero frame, generate the new background separately with NBP T2I, composite in FFmpeg. (4) **Qwen Image Edit fallback** (`alibaba/qwen-image-edit`, $0.059) or **Seedream 4.5 Edit** (canary first) for surgical background replacement when NBP OTHER-blocks. (5) **Model-switch**: try the same call on NB2 Edit (`google/nano-banana-2`) — NBP and NB2 use separate enforcement paths; a call blocked on NBP sometimes passes on NB2 (community report June 2026, unverified — try before giving up on I2I). The OTHER block is NOT a failure of prompt quality — do not keep retrying the same call.
- **Gemini 3.5 Flash (2026-05-19):** Text-output-only model. Does NOT generate images. Not an upgrade path for hero frames. Image generation pipeline remains: NB2 (draft) → NBP Edit (final) → Imagen 4 Ultra (CTA/money shots).

### Camera Angle Variation Technique (2026-05-31)

Generate alternate camera angles from one approved hero frame — cheaper than full regen from scratch.

**Official Google formula (confirmed):**
```
[Reference images] + [Relationship instruction] + [New scenario/angle]
```

**Camera angle prompt template:**
```
Image 1: Mourad-SV approved hero frame (frontal close-up, golden hour).
Keep ALL of the following IDENTICAL: facial features, skin tone, short black beard,
black crewneck with orange chest logo, blue jeans, white sneakers, lighting direction.
Change ONLY the camera angle to a 45-degree left three-quarter profile view.
Same shallow depth of field (f/2.2). Same golden hour warm backlight.
No side door on the cargo box behind him. Vertical 9:16.
```

**Camera hardware naming for lens control** (more reliable than abstract lens specs):
- "Shot on Fujifilm X-T5, f/1.8, warm color science" → cinematic portrait
- "Shot on Sony A7R V, 85mm portrait lens, f/2.2" → sharp commercial
- "GoPro Hero 11 Wide" → immersive, slightly distorted action feel

**Use case — character sheet from one hero frame:**
Instead of generating three views from scratch, take one approved hero frame and use NBP Edit to generate 45° left and 45° right views. Each call costs $0.20. Total character sheet from one approved frame: $0.40 + FFmpeg (free).

**Critical:** When asking for an angle change, list EVERY preserved element explicitly. The model interprets ambiguity as permission to change. Leaving out "keep same lighting" = risk of lighting drift.

**Failure mode:** Full-body shots with angle changes fail more often than head-and-shoulders crops. If identity consistency is critical, crop to head-and-shoulders before requesting angle variation.

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
- **Reference image lighting consistency (2026-06-02):** All reference images for the same character MUST share identical lighting setup — even, front-facing diffused light, no strong directionality. Mixed lighting across refs (e.g., one studio-lit and one outdoor) introduces inconsistency that the model resolves by averaging, producing a face that matches neither. If you have refs with mixed lighting, pick only those shot in the same session or relight to match before uploading.
- **Input image size limit — 7MB per image (2026-06-12):** Each reference image passed to NBP Edit MUST be ≤7MB original file size. Google automatically compresses images above this limit, causing detail loss and identity drift. Base64 encoding adds ~33% overhead, so a 7MB original becomes ~9.3MB encoded — this is fine as long as the original file is ≤7MB. For refs that exceed 7MB: (a) compress/resize to fit under 7MB; (b) or pass via Cloud Storage URL (supports up to 30MB). Generated NBP outputs at 1K/2K typically land well under 7MB. 4K outputs may exceed this if used as refs in a subsequent call — downsize before reusing as input.
- First-pass consistency rates: character-sheet workflow = 85-90%; single hero image without sheet = 60-70%
- **Chain update technique (2026-05-08):** Include the PREVIOUS output as one of the reference images when making incremental edits. This reduces drift across multi-pass generation by giving the model a visual anchor of the last state. Remind it explicitly each call to preserve hair, clothing, and facial features.
- **Iterative refinement loop (2026-05-22):** After each generation pass, use the BEST output from that pass as an additional reference in the next call — alongside the original character sheet. Community-confirmed: achieves 90%+ consistency across 50+ image batches. Loop: generate batch → pick best → add as Image 2 alongside original sheet → generate next batch → repeat. Stop when identity is locked (face distance < 0.4 cosine).
- **NBP chain edit degrades at 3-4 passes (2026-06-12 — CRITICAL):** Unlike Flux Kontext (which maintains identity stability across 6+ edits via ArcFace), NBP/NB2 chain edits accumulate quality loss like repeated JPEG re-saves. After 3-4 chain edits: faces look older, skin textures turn plastic, colors shift. **Hard limit: restart the chain from the original refs after 3 edits on any NBP/NB2 composition.** Do NOT continue editing a 4th-pass output — degrade compounds. Recovery technique: when chain passes 3 but composition is not yet right, extract a structured text description of the conceptually-correct output from that pass (all visual elements, pose, lighting, props), then regenerate from scratch using the original refs + extracted description. A fresh generation from a good description outperforms salvaging a degraded chain.

### thoughtSignature — Multi-Turn Chain Editing (2026-06-03)

Gemini 3 image models (NBP and NB2) use **thought signatures** — encrypted reasoning-state tokens returned with every generation response. In multi-turn editing (e.g., asking the model to iteratively refine the same image across several calls), the `thoughtSignature` from each response MUST be passed back in the next turn. Missing signatures result in **400 errors** or the model "forgetting" earlier context (reverts to generating from scratch).

**For our AIMLAPI pipeline (httpx, not official Google SDK):**
- AIMLAPI proxies through the Gemini API — it may or may not surface `thoughtSignature` in the response JSON.
- Do NOT attempt to build native multi-turn Gemini sessions through AIMLAPI. AIMLAPI's `/v1/images/generations` endpoint is stateless by design — each call is independent.
- **Our existing substitute is correct**: include the PREVIOUS output image as Image 2 (alongside the original character sheet as Image 1) in every chain-edit call. This gives the model a visual anchor of prior state and is the AIMLAPI-safe equivalent of thoughtSignature continuity.
- If you need true thoughtSignature-based multi-turn editing, use the native Gemini Python SDK (`google-generativeai`) with a `chat` object — signatures are handled automatically. Only switch to native SDK if AIMLAPI's stateless proxy proves insufficient after ≥3 chain-edit failures.

**Why this matters:** The iterative refinement loop (chain update technique) documented above is our thoughtSignature substitute — it works precisely because passing the previous output preserves visual context. Continue using it; don't try to extract or pass `thoughtSignature` manually through AIMLAPI.

### NBP Semantic Inpainting — Fix Brand Failures Without Regenerating (2026-05-24)

NBP Edit supports mask-free localized editing: pass the hero frame as Image 1 and describe the change in natural language. The model identifies the target area automatically using scene understanding, not pixel masks. No inpainting mask parameter is needed.

**Use case:** A hero frame passes 7/8 QA checks but fails one brand binary item — use inpainting to fix that element at $0.20 instead of re-running the full generation loop (saves 2-5 iteration passes = ~$0.40-1.00).

**Common pipeline fixes:**

| Failure | Inpainting prompt |
|---------|-------------------|
| Truck side door visible | `"Image 1: hero frame. Remove the side door from the cargo box. Replace with a smooth flat white sealed panel. Keep everything else in the scene identical — do not change the character, lighting, background, or any other part of the truck."` |
| Uniform wrong color | `"Image 1: hero frame. Change the shirt color to black. Keep the orange logo on the left chest. Do not change anything else — face, background, truck, jeans."` |
| Logo color off (yellow instead of #FC8434) | `"Image 1: hero frame. Change all orange/yellow brand elements to exactly #FC8434 bright orange. Do not change any other part of the image."` |
| Box color wrong (brown kraft instead of white) | `"Image 1: hero frame. Change the moving box to white cardboard with #FC8434 orange text. Do not change the character, truck, or background."` |

**Rules:**
- Always pass the hero frame as Image 1 in the `image_urls` array
- Name the target area explicitly — "the cargo box", "the shirt", "the logo" — not "it" or "that"
- Explicitly state what NOT to change: "do not change the face, lighting, or background"
- If the fix fails after 2 attempts, regenerate from scratch rather than chaining fixes
- Log inpainting calls in cost tracking the same as any NBP Edit call ($0.20 each)

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

**Flux Kontext Max Multi (2026-05-28 UPDATE — CONFIRMED):** `image_url` on AIMLAPI's `flux/kontext-max/image-to-image` accepts an **array of URLs**. AIMLAPI docs show working 2-image examples (place object from image A onto image B). This was unverified as of 2026-05-22 — now confirmed operational. BFL-native supports up to 8-10 refs; AIMLAPI confirmed at 2 in docs, exact max unclear — treat 2 as the safe ceiling until you run a canary with 3+. Dedicated `/multi` endpoints exist on fal.ai (`fal-ai/flux-pro/kontext/max/multi`) and Replicate (`multi-image-kontext-max`) but still no separate `/multi` path on AIMLAPI — use the standard I2I endpoint with array input instead. The FFmpeg hstack composite workaround is no longer required for 2-ref calls.

- 30-80 word sweet spot, maximum 512 tokens
- FLUX does NOT support CLIP-style weighting — `(keyword:1.5)` is silently ignored
- Token hierarchy: subject > action/pose > environment > lighting > style
- For SNELVERHUIZEN.NL text: always use quotation marks, ALL CAPS, specify "bold clean sans-serif". Text editing format: `Replace '[original text]' with '[new text]'`
- If text morphs: generate truck text-free, composite in post
- **ONE change per call** — progressive editing only. Change background first → then lighting → then details. Stacking multiple changes in one prompt degrades quality.
- Refer to subjects by description, not pronouns: "the man with the black crewneck" not "him"
- Character identity: uses AuraFace embeddings; maintains cosine similarity >0.92 across 6 successive edits (vs ~0.80 for competing models). This means ≤6 edits from original ref before restarting chain.
- `guidance_scale` range on AIMLAPI: 1–20. **Default is 3.5.** Two regimes: (1) character/face editing → use 2.0–2.5 (more image-preserving, prevents face warp; 2.0 is the confirmed lower bound for stable face output); (2) text/typography editing → use 3.5–4.0 (more prompt-literal for letter accuracy). Do not exceed 5 for character editing — face structure distorts. Note: other platforms (Replicate, fal.ai) use a different guidance_scale range (1–50) — do not import their settings. **Kontext technical paper (BFL, arxiv.org/abs/2506.15742):** Published June 2026. Key finding: AuraFace cosine similarity averages ~0.908 across successive editing steps, confirming robust identity preservation. guidance_scale=2.5 is used in all BFL HF model card examples for editing tasks — this is the HF model card recommendation, not directly stated in the paper body. AIMLAPI guidance_scale has no documented default; use 2.0–2.5 for character editing per existing pipeline guidance.**
- **`image_strength` / `strength` — ⚠️ CORRECTION (2026-06-06):** AIMLAPI's `flux/kontext-max/image-to-image` endpoint does **NOT** expose a `strength` or `image_strength` parameter. The previous guidance ("default 0.1, increase to 0.3–0.5 for face lock") was sourced from **fal.ai's** Kontext Max endpoint, not AIMLAPI. On AIMLAPI, image influence is fixed server-side and cannot be controlled by the caller. Do NOT pass `image_strength` or `strength` in AIMLAPI Kontext calls — it will be silently ignored or may cause an error. If you need fine-grained strength control, fal.ai exposes this parameter (default 0.1, same range 0–1) — but fal.ai is outside the AIMLAPI-only architecture. For AIMLAPI: control identity lock via `guidance_scale` (2.0–2.5 for character editing) and prompt wording only. Reference for HF diffusers: default strength is 0.6 (meaning "allow 60% repaint") — also irrelevant to AIMLAPI calls.
- **`safety_tolerance`** (1–6, default 2): Controls content safety threshold. 1 = most strict, 5 = most permissive. **Confirmed on AIMLAPI Kontext.** Default 2 is appropriate for our modest-dress character shots — do NOT raise above 2 for character calls. If a character shot is unexpectedly blocked, log `blockReason` and escalate; do not loosen safety_tolerance.
- **Multi-image on AIMLAPI (confirmed 2026-05-28)**: `image_url` accepts an array. AIMLAPI docs confirm **2 reference images** in working examples. BFL-native supports up to 8-10, but counts above 2 on AIMLAPI are unverified — treat 2 as the safe max until canary confirms 3+.
- `num_inference_steps`: not exposed on AIMLAPI I2I endpoint (handled server-side). For T2I endpoint: 20-50 steps; use 28 for drafts, 50 for production finals.
- **`prompt_upsampling`**: When `true`, an LLM rewrites the prompt for richer output — but results are NOT reproducible across calls. For character editing and brand-critical shots, set `prompt_upsampling: false` to maintain reproducibility. For T2I scenery shots where variation is acceptable, leaving it true may improve output. Status on AIMLAPI's Kontext endpoint: UNVERIFIED — may be handled server-side. Use `false` explicitly if the parameter is exposed.

**Kontext Max speed upgrade (2026-03-03):** BFL doubled generation speed for both text-to-image and image-editing tasks with zero quality loss. Turnaround on AIMLAPI should be ~15-20s at current load.

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

## Background Segmentation Tools (for blockReason OTHER workaround)

When NBP Edit returns `blockReason: OTHER` on a person+scene composite call, the segmentation-composite workflow extracts the character silhouette from the approved hero frame, generates a new background with T2I, and composites in FFmpeg — without triggering person-editing policies.

| Tool | Install | Strength | Notes |
|------|---------|----------|-------|
| **BiRefNet** | `pip install birefnet` | Production-grade high-res segmentation; outperforms rembg on complex edges | Three-tier: Light (fast), Heavy (complex), Portrait (face-optimized) |
| **rembg** | `pip install rembg` | Simple, fast automatic foreground extraction | Adequate for clean-background refs; inferior to BiRefNet on natural scenes |
| **SAM2** | `pip install transformers` | Interactive segmentation (point/box prompt) | Slower; use when BiRefNet misses hair or fine details |

**Workflow (blockReason OTHER fallback):**
```
1. BiRefNet: extract character RGBA from approved hero frame
2. NBP T2I: generate new background scene (no person in prompt)
3. FFmpeg composite: overlay character RGBA onto new background
   ffmpeg -i background.jpg -i character_rgba.png \
     -filter_complex "[0][1]overlay=x=...:y=..." output.jpg
```

This produces the same scene change as an NBP Edit call but avoids all person-editing policy triggers.

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

### GPT Image 2 — CTA Cards with Dutch Text (2026-06-08 update)

Use for CTA cards and text-heavy brand stills. Supports up to 16 reference images (AIMLAPI unverified — canary required). Strength: 99% text accuracy in Dutch vs ~60% for older models. Token-based pricing — run canary before production.

**⚠️ BANNED PARAMS on GPT Image 2:** Do NOT include `input_fidelity` (breaks the call) or `background: "transparent"` (not supported — will fail).

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "openai/gpt-image-2",
    "prompt": "Clean professional CTA card on white background. Large bold orange text reading 'SNELVERHUIZEN.NL' centered at top. Below it in smaller text: '085 3331133'. Below that: 'VERHUIZEN ZONDER ZORGEN' in bold. Orange is exactly #FC8434. 9:16 vertical format. Minimal design, no people, no decoration.",
    "size": "1152x2048",   # true 9:16 portrait — multiples of 16, ratio < 3:1
    "quality": "high",
    "n": 1,
    # DO NOT add: input_fidelity (doesn't exist on gpt-image-2, breaks the call)
    # DO NOT add: background: "transparent" (not supported on gpt-image-2)
}, headers=headers, timeout=120)
hero_url = resp.json()["data"][0]["url"]
```

**CANARY REQUIRED:** GPT Image 2 uses token-based pricing on AIMLAPI. Run one test call and check actual cost before committing to a batch. Confirm `size: "1152x2048"` accepted by AIMLAPI. If cost exceeds $0.25/image, re-evaluate against NBP Edit. Imagen 4 Ultra fallback **retires June 24, 2026** — do not use as fallback.

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

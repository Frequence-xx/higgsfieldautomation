---
name: Character Consistency
description: Maintains visual consistency for recurring characters (crew, family archetypes) across multiple shots and videos using reference anchoring and prompt structure.
autoInvoke: true
triggers:
  - character
  - crew member
  - person
  - family
  - consistent
  - reference image
  - anchor
negatives:
  - Do NOT invoke when generating shots with no people (truck-only, B-roll, establishing shots)
  - Do NOT invoke when doing post-production or caption work
  - Do NOT invoke when the shot uses a Type C generic one-off person in a wide/silhouette framing
---

# Character Consistency System

## The Problem
AI models drift: a crew member's face, build, skin tone, and clothing change between shots. Without explicit anchoring, every generation treats characters as new.

## AIMLAPI Character Reference Models

| Stage | Model | Param | Max Refs | Use For |
|-------|-------|-------|----------|---------|
| Hero frame with character lock | `flux/kontext-max/image-to-image` | `image_url` (array) | 4 | Lock character identity across scenes |
| Hero frame — cheaper multi-ref | `klingai/image-o1` | `image_urls` (array) | **10** | $0.040/img — UNVERIFIED for production; test before adopting |
| Compositing character into scene | `google/nano-banana-pro-edit` | `image_urls` (array) | **14** | Place character into any background |
| Character-consistent video | `klingai/video-o1-reference-to-video` | `elements` + `image_list` | 4 elements, 7 total | Video with locked character identity |
| High-quality character video | `google/veo-3.1-reference-to-video` | `image_urls` (array) | ~3+ | Premium character video |

## Step-by-Step Workflow

### Step 1: Create Character Reference Sheet
For each recurring character, MUST generate 4 reference images using Nano Banana Pro.
Use 1:1 for reference sheets (consistency matching), 9:16 for final hero frames.

```python
# Generate 4 angles of the character via AIMLAPI
for angle in ["front view", "3/4 angle from left", "profile from right side", "full body standing"]:
    resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
        "model": "google/nano-banana-pro",
        "prompt": f"A 37-year-old Dutch man with short dark brown hair, medium olive skin, clean shaven, wearing a navy blue polo shirt with company logo on left chest and dark grey cargo trousers with black work boots, {angle}, professional photography, neutral background",
        "aspect_ratio": "1:1",
        "resolution": "1K",
    }, headers=headers, timeout=60)
```

Save to `/opt/pipeline/assets/characters/{name}/`.

### Step 2: Lock Character via Flux Kontext Max

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "flux/kontext-max/image-to-image",
    "prompt": "Place this person on a Dutch suburban street next to a white moving truck, golden hour lighting, cinematic vertical composition, 35mm lens",
    "image_url": [
        "https://cdn.example.com/characters/crew_lead/front.png",
        "https://cdn.example.com/characters/crew_lead/three_quarter.png"
    ],
    "aspect_ratio": "9:16",
    "num_images": 1,
}, headers=headers, timeout=90)
hero_frame_url = resp.json()["data"][0]["url"]
```

### Step 3: Animate with Character Reference (Kling O1)

```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "klingai/video-o1-reference-to-video",
    "prompt": "The person from @Element1 walks confidently towards the moving truck, picks up a box, golden hour light",
    "elements": [
        {
            "frontal_image_url": "https://cdn.example.com/characters/crew_lead/front.png",
            "reference_image_urls": [
                "https://cdn.example.com/characters/crew_lead/three_quarter.png",
                "https://cdn.example.com/characters/crew_lead/profile.png"
            ]
        }
    ],
    "duration": 5,
    "aspect_ratio": "16:9"
}, headers=headers)
```

**Important:** Elements extract face + posture + clothing together. **No face_weight API parameter exists on AIMLAPI.** "Subject Binding 80-90" in CLAUDE.md is a quality target, not a parameter.

### Step 3b: Multi-Character Scene

```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "klingai/video-o1-reference-to-video",
    "prompt": "@Element1 and @Element2 carry boxes together towards the truck, natural collaboration, golden hour",
    "elements": [
        {"frontal_image_url": "mourad/front.png", "reference_image_urls": ["mourad/three_quarter.png", "mourad/profile.png"]},
        {"frontal_image_url": "karel/front.png", "reference_image_urls": ["karel/three_quarter.png", "karel/profile.png"]}
    ],
    "generate_audio": False,
    "duration": 5,
    "aspect_ratio": "9:16"
}, headers=headers)
```

**Multi-character known failure mode:** Feature swapping when characters touch or overlap. Mitigation: keep characters spatially separated in prompt, run InsightFace QA on BOTH.

### Step 3c: Video-Based Element

```python
"elements": [{"video_url": "https://cdn.example.com/characters/mourad/reference_clip.mp4"}]
```

Best for carrying consistency forward from clip N to clip N+1.

### Step 4: Alternative — Nano Banana Pro Edit

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/nano-banana-pro-edit",
    "image_urls": ["crew_lead/front.png", "crew_lead/full_body.png", "dutch_street_golden_hour.png"],
    "prompt": "Place the person from the first two images into the street scene from the third image",
    "aspect_ratio": "9:16",
    "resolution": "1K",
}, headers=headers, timeout=60)
```

### Step 2b: Kling Image O1 — Cheaper Multi-Ref Hero Frame (UNVERIFIED — do not use in production until tested)

Kling Image O1 (`klingai/image-o1`) is an MVL-based image model on AIMLAPI that supports up to 10 reference images at **$0.040/image** — 5× cheaper than NBP Edit ($0.195) and 2.5× cheaper than Flux Kontext Max ($0.10). It uses the same `/v1/images/generations` endpoint.

**Before adopting:** run one draft hero frame, score with InsightFace buffalo_l, compare score vs NBP Edit baseline on the same refs. Only switch routing matrix entry after owner-reviewed output passes brand binary checklist.

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "klingai/image-o1",
    "prompt": "The man with short dark brown hair and medium olive skin, wearing a navy blue polo with company logo on left chest and dark grey cargo trousers, stands confidently on a Dutch suburban street next to a white moving truck, golden hour lighting, cinematic vertical composition, 35mm lens",
    "image_urls": [
        "https://cdn.example.com/characters/crew_lead/front.png",
        "https://cdn.example.com/characters/crew_lead/three_quarter.png",
        "https://cdn.example.com/characters/crew_lead/profile.png"
    ],
    "aspect_ratio": "9:16",
    "resolution": "1K",
}, headers=headers, timeout=90)
# Note: same noun-phrase prompt rule applies — no pronouns (see Step 4b below)
```

**Key parameter differences vs NBP Edit:**
- `image_urls` (not `image_url` singular) — array, same as NBP Edit
- `resolution`: `"1K"` or `"2K"` (not `"1024"` or numeric)
- `aspect_ratio`: same string format as other AIMLAPI models (`"9:16"`)
- **No `num_images` param** — generates 1 image per call

### Step 4b: Flux Kontext Max — Noun-Phrase Prompts (no pronouns)

When using `flux/kontext-max/image-to-image` for character hero frames, **always describe the character in the prompt with noun phrases, never pronouns**. The model treats each reference independently and has no pronoun resolution.

**DO:** `"The man with short dark brown hair and medium olive skin, wearing a navy blue polo, stands next to the truck"`
**DON'T:** `"He stands next to the truck"` — "he" is ignored, identity reverts to model default

Up to 10 reference images are technically supported; 3–5 covering distinct angles (front, 3/4, profile, full body) is the practical optimum. Beyond 5, references compete and consistency degrades.

### Step 5: Character Metadata (character.json)

```json
{
  "name": "Crew Lead",
  "gender": "male",
  "approximate_age": "35-40",
  "build": "medium athletic",
  "skin_tone": "medium olive",
  "hair": "short dark brown",
  "uniform": "navy blue polo with Snel Verhuizen logo on left chest, dark grey cargo trousers, black work boots",
  "distinguishing": "clean shaven, friendly expression",
  "prompt_snippet": "a 37-year-old man with short dark brown hair, medium olive skin, clean shaven, wearing a navy blue polo shirt with company logo and dark grey cargo trousers with black work boots",
  "reference_urls": {
    "front": "/assets/characters/crew_lead/front.png",
    "three_quarter": "/assets/characters/crew_lead/three_quarter.png",
    "profile": "/assets/characters/crew_lead/profile.png",
    "full_body": "/assets/characters/crew_lead/full_body.png"
  }
}
```

### Step 6: QA Check for Character Drift

**InsightFace install (pass 10 finding, 2026-05-25):** InsightFace 1.0.1 (released May 23, 2026) no longer builds the `face3d` Cython/C++ extension by default. Standard `pip install insightface` now works without a C++ compiler. Our QA pipeline uses only `FaceAnalysis` (detection + recognition) — no `face3d` needed. If face3d is ever required, opt in explicitly: `pip install "insightface[face3d]"` or set `INSIGHTFACE_WITH_FACE3D=1`.

```python
from insightface.app import FaceAnalysis
import cv2, numpy as np

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=-1, det_size=(640, 640))  # init once per session

def clip_qa(ref_path: str, frame_paths: list[str]) -> dict:
    ref_img = cv2.imread(ref_path)
    ref_faces = app.get(ref_img)
    if not ref_faces:
        return {"error": "no face in reference"}
    ref_emb = ref_faces[0].normed_embedding  # already L2-normalized

    results = {}
    labels = ["t0", "t2_5", "t5"]
    for label, path in zip(labels, frame_paths):
        img = cv2.imread(path)
        faces = app.get(img)
        if not faces:
            results[label] = 0.0
        else:
            emb = faces[0].normed_embedding
            results[label] = float(np.dot(ref_emb, emb))  # cosine sim (no division needed)
    return results

# PASS if all scores >= 0.68; note if 0.60-0.67; retry if < 0.60; reject if < 0.50
```

**Threshold guide (buffalo_l model):**

| Score | Meaning | Action |
|-------|---------|--------|
| ≥ 0.68 | Strong identity match | PASS |
| 0.60 – 0.67 | Acceptable drift | PASS with note |
| 0.50 – 0.59 | Marginal | RETRY |
| < 0.50 | Identity failure | REJECT — try FaceFusion fallback |

**Skin-tone bias correction (pass 4 finding):** buffalo_l was trained predominantly on lighter-skinned subjects. For olive/brown skin characters (Karel, Mourad), the model produces systematically lower cosine scores at the same identity. **Lower the RETRY threshold to 0.42–0.45 for these characters** to avoid false QA rejects. The REJECT floor stays at 0.40 (below which identity failure is genuine). Calibrate per character by scoring 4 approved reference images against each other — the lowest pair score is the effective floor.

```python
# Character-specific threshold example:
THRESHOLDS = {
    "karel":  {"pass": 0.62, "note": 0.55, "retry": 0.42, "reject": 0.40},
    "mourad": {"pass": 0.62, "note": 0.55, "retry": 0.42, "reject": 0.40},
    "generic_light_skin": {"pass": 0.68, "note": 0.60, "retry": 0.50, "reject": 0.50},
}
```

**buffalo_l vs antelopev2 (pass 5 finding):** antelopev2 uses an R100 backbone (vs buffalo_l's R50) and outperforms buffalo_l on IJB-C per InsightFace's own model table. Upgrade path:
```python
# Upgrade: R100 backbone, better identity accuracy on harder cases
app = FaceAnalysis(name='antelopev2')
app.prepare(ctx_id=-1, det_size=(640, 640))
# NOTE: antelopev2 produces lower raw cosine values than buffalo_l for the same identity.
# Confirmed threshold range for 1:1 verification: 0.30–0.45 cosine at FMR=1e-4 to 1e-5
# (pass 6 finding, 2026-05-17). Start retry threshold at 0.30, not 0.42–0.50.
# Requires manual model download: pip install insightface then run prepare() once to auto-fetch.
```
**Current production model stays buffalo_l** (auto-downloads, validated thresholds). Upgrade to antelopev2 only after re-calibrating thresholds on approved character sheets.

**AuraFace** (open-source, commercially licensed): ResNet100 + ArcFace, drop-in ONNX replacement for buffalo_l's recognition head. Key advantage: Apache 2.0 license (buffalo_l ONNX models carry non-commercial restriction). **LFW benchmark confirmed at 99.65%** (pass 6 finding, 2026-05-17). Multiple production teams have validated it. Recommended upgrade path from buffalo_l when licensing matters.

**AuraFace threshold regime (pass 13 finding, 2026-06-03):** AuraFace produces lower raw cosine scores than buffalo_l. Same-person comparison across different images typically yields ~0.55–0.65 cosine — noticeably lower than buffalo_l's ~0.75–0.90 range for the same identity. **Do NOT use buffalo_l thresholds (PASS≥0.68) with AuraFace** — they will produce systematic false rejects. Starting calibration range for AuraFace:

| Score | Action |
|-------|--------|
| ≥ 0.45 | PASS |
| 0.35 – 0.44 | PASS with note |
| 0.25 – 0.34 | RETRY |
| < 0.25 | REJECT |

These are starting estimates only — calibrate per character by scoring 4 approved reference images against each other (same procedure as buffalo_l skin-tone calibration). No per-demographic benchmark published yet for AuraFace; treat olive/brown skin characters same as generic until calibrated.

### FaceFusion Fallback (identity score < 0.50)

FaceFusion **v3.6.1** is the current stable release (April 19, 2026). v3.6.0 added the `fran` age modification processor (de-age / re-age faces) and new background remover models (`corridor_key_1024`, `corridor_key_2048`). No new face-swapper or expression-restorer features since v3.6.0.

FaceFusion v3.6.0+ uses a **job-based architecture** — `run` is replaced by `headless-run`. The old `python facefusion.py run --headless` syntax is broken in v3.

```bash
conda create -n facefusion python=3.12 -y && conda activate facefusion
git clone https://github.com/facefusion/facefusion && cd facefusion && python install.py

# v3.6.0+ syntax (headless-run, NOT run)
python facefusion.py headless-run \
  --source-paths /path/to/approved_character_front.png \
  --target-path /path/to/failed_clip.mp4 \
  --output-path /path/to/fixed_clip.mp4 \
  --processors face_swapper face_enhancer \
  --face-swapper-model inswapper_128_fp16 \
  --face-selector-mode reference \
  --reference-face-position 0 \
  --face-enhancer-model gfpgan_1.4 \
  --face-enhancer-blend 80
```

**v3 model change:** `hyperswap_1a_256` is the new default face swapper. Use `inswapper_128_fp16` explicitly for highest quality (especially for non-white skin fidelity).

**New parameters in v3.4.0–v3.5.0 (pass 6 findings, 2026-05-17):**

```bash
# --face-swapper-weight (v3.4.0+): source-target balance. Default 1.0 (full source identity).
# Use 0.8 for olive/brown skin to reduce over-swap artifacts and preserve skin tone nuance.
python facefusion.py headless-run \
  --source-paths /path/to/approved_character_front.png \
  --target-path /path/to/failed_clip.mp4 \
  --output-path /path/to/fixed_clip.mp4 \
  --processors face_swapper face_enhancer \
  --face-swapper-model inswapper_128_fp16 \
  --face-swapper-weight 0.8 \
  --face-selector-mode reference \
  --reference-face-position 0 \
  --face-enhancer-model gfpgan_1.4 \
  --face-enhancer-blend 80 \
  --output-video-encoder libx264rgb   # prevents RGB→YUV color shift on brown/olive skin

# face_dat_x4 frame processor (v3.5.0+): 4× face detail upscaler.
# Use instead of (or after) face_enhancer when GFPGAN over-smooths.
# Replace --processors face_swapper face_enhancer with:
#   --processors face_swapper face_dat_x4

# --face-detector-margin (v3.5.0+): extend detection box beyond frame edge.
# Add when character face is partially cropped at clip edge.

# expression_restorer processor (v3.6.0+, pass 7 finding, 2026-05-19):
# After face_swapper, faces can look stiff/frozen. expression_restorer (Live Portrait)
# re-injects natural expression motion. Add AFTER face_swapper and face_enhancer.
# --expression-restorer-factor 80: default. Range 0-100. Lower (60) for dark/olive skin
# to avoid over-driving expression artifacts. --expression-restorer-areas: all/upper-face/lower-face.
python facefusion.py headless-run \
  --source-paths /path/to/approved_character_front.png \
  --target-path /path/to/failed_clip.mp4 \
  --output-path /path/to/fixed_clip.mp4 \
  --processors face_swapper face_enhancer expression_restorer \
  --face-swapper-model inswapper_128_fp16 \
  --face-swapper-weight 0.8 \
  --face-selector-mode reference \
  --reference-face-position 0 \
  --face-enhancer-model gfpgan_1.4 \
  --face-enhancer-blend 80 \
  --expression-restorer-model live_portrait \
  --expression-restorer-factor 60 \
  --expression-restorer-areas all \
  --output-video-encoder libx264rgb
```

Re-run InsightFace QA after FaceFusion. Score should be ≥ 0.65.

**GSwap — Future Watch (research stage, March 2026):** 3D head swap using neural Gaussian portrait representation embedded in SMPL-X body surface. Models head, torso, and motion together (not just 2D face patch), with neural re-rendering for natural background integration. Addresses FaceFusion's known failure mode: detached/misaligned look under strong head motion. Not yet packaged as a tool. Monitor for open-source release — would replace FaceFusion for clips with large head rotation or motion blur.

**lip_syncer processor (pass 9 finding, 2026-05-23): sync mouth to voiceover**

When a clip needs Dutch/Arabic voiceover, add `lip_syncer` after `face_swapper` to synchronize mouth movements with the audio. Three model choices: `edtalk_256`, `wav2lip_96`, `wav2lip_gan_96` (default). `--lip-syncer-weight` 0.0–1.0 (default 0.5 — higher = stronger sync, lower = less geometry distortion risk).

```bash
python facefusion.py headless-run \
  --source-paths /path/to/voiceover.wav /path/to/approved_character_front.png \
  --target-path /path/to/clip.mp4 \
  --output-path /path/to/lipped_clip.mp4 \
  --processors face_swapper lip_syncer \
  --face-swapper-model inswapper_128_fp16 \
  --face-swapper-weight 0.8 \
  --lip-syncer-model wav2lip_gan_96 \
  --lip-syncer-weight 0.5 \
  --face-selector-mode reference \
  --reference-face-position 0 \
  --output-video-encoder libx264rgb
# edtalk_256: better for high-res output, less GAN artifacts
# wav2lip_gan_96: default, generally more natural-looking for talking head
# Order: pass source audio FIRST in --source-paths, then face reference image
```

**OmniHuman v1.5 — cloud-based alternative to FaceFusion lip_syncer (pass 11 finding, 2026-05-30):**

`bytedance/omnihuman/v1.5` on AIMLAPI generates full-body animated video from a character photo + audio. Unlike FaceFusion lip_syncer (lip sync only), OmniHuman animates the entire body with gesture and expression synchronized to the audio — no local compute needed.

When to use: FaceFusion not installed, or scene requires full-body expressiveness (gestures, posture) matching the voiceover rather than just mouth sync.

```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "bytedance/omnihuman/v1.5",
    "image_url": "https://cdn.example.com/characters/crew_lead/front.png",
    "audio_url": "https://cdn.example.com/voiceover/dutch_line.wav",
    "resolution": "720p",   # "720p" (faster, better quality) or "1080p"
    # Duration = audio length automatically; max 30s at 1080p, 60s at 720p
}, headers=headers, timeout=120)
# Response: result["video"]["url"], result["duration"] (seconds billed)
```

**Cost: ~$0.208/sec on AIMLAPI.** A 5s clip costs ~$1.04 — use sparingly; only when FaceFusion unavailable. FaceFusion lip_syncer (free, local) is the primary option for lip sync. QA note: run InsightFace identity check on OmniHuman output — full-body re-animation can alter facial geometry.

**CodeFormer alternative (better for olive/brown skin):** GFPGAN can whiten/flatten brown skin features at high fidelity. Use CodeFormer with `w=0.5–0.6` instead — lower w preserves skin tone accuracy.

```bash
# CodeFormer face restoration (better for non-white skin than GFPGAN)
python inference_codeformer.py \
  -w 0.6 \
  --input_path /path/to/failed_clip.mp4 \
  --output_path /path/to/fixed_clip.mp4 \
  --face_upsample \
  --bg_upsampler realesrgan
# w=0.5-0.6: preserve skin tone; w>0.7: over-smooth, whitens features
```

**ComfyUI InstantID + IP-Adapter + FaceDetailer stack (best quality, most effort):**
For clips where FaceFusion produces unnatural results (stiff face, wrong skin tone):
1. InstantID node: inject reference face identity
2. IP-Adapter node: match pose + lighting from reference
3. FaceDetailer node: CodeFormer polish (w=0.6)
Best for non-celebrity, non-white subjects. Setup time: ~2h first run.

## Model Selection for Character Shots

| Scenario | Image Model | Video Model | Cost Est. |
|----------|-------------|-------------|----------|
| Karel/Mourad alone | Nano Banana Pro Edit | Kling v3 Pro I2V (audio OFF) | ~$0.13 + $1.46/5s |
| Multiple characters | Nano Banana Pro Edit (14 refs) | Kling v3 Pro I2V (audio OFF) | ~$0.13 + $1.46/5s |
| Generic one-off person | Nano Banana Pro (no refs) | Kling v3 Pro I2V (audio OFF) | ~$0.13 + $1.46/5s |

## Character Types — Decision Tree

### Type A: Existing Characters (Karel & Mourad)
Ref sheets at `/opt/pipeline/assets/crew/`. Use Nano Banana Pro Edit with existing sheets.

### Type B: New Recurring Character
Generate 4-angle ref sheet via Nano Banana Pro. Owner approval required before use.

### Type C: Generic One-Off Person
Nano Banana Pro text-only. Not reusable. Best for wide shots, back-of-head, silhouettes.

## Reference Image Quality Requirements

- **Resolution:** 1024×1024 minimum
- **Background:** Pure flat white or green screen — MANDATORY for Kling Element binding
- **Lighting:** Soft, even, diffused. All 4 angles MUST be from the same lighting setup
- **Expression:** Neutral across ALL reference images
- **Ref count sweet spot:** 3–4 refs optimal; cap at 4 (Kling hard limit). More than 4 increases copy-paste artifact risk ("view-dependent copy-paste," per arXiv 2508.09476 Mixture of Facial Experts research).
- **Angular diversity > expression diversity:** front + 3/4 + profile is the minimal effective multi-view set (confirmed by Mv²ID and MoFE research). Do NOT replace an angle ref with an expression variant — cover angles first.
- **Array order does not matter for Kling elements binding.** No published evidence of order sensitivity. Focus on angle coverage.
- **Do NOT feed generated frames back as references.** Always re-anchor from original approved photos
- **Each clip in a video sequence MUST independently derive character identity** from original approved reference photos

## Multi-Shot Frame-Chaining

```python
# Extract last clean frame — prefer t=4.5s if t=5.0s has motion blur
# -sseof -0.5 = 0.5s before end; use -sseof -0.1 only for well-resolved final frames
os.system(f"ffmpeg -i {prev_clip} -vframes 1 -sseof -0.5 {last_frame_path}")
# If that frame has motion blur, fall back to t=4.5s absolute:
# os.system(f"ffmpeg -i {prev_clip} -ss 4.5 -vframes 1 {last_frame_path}")

resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "klingai/kling-video-v3-pro-image-to-video",
    "image_url": last_frame_path_or_url,   # Continuity anchor
    "elements": [{"frontal_image_url": "crew_lead/front.png", "reference_image_urls": ["crew_lead/three_quarter.png"]}],
    "prompt": "...",
    "generate_audio": False,
    "duration": 5,
    "aspect_ratio": "9:16"
}, headers=headers)
```

**Alternative: `klingai/video-o1-video-to-video-reference` (pass 10 finding, 2026-05-25):** Confirmed available on AIMLAPI. Instead of extracting a last frame (I2V), pass the entire previous clip as a video reference. Stronger continuity for character motion and scene lighting — the model reads temporal context from the full clip rather than a single frozen frame. Use when a character was in motion at clip end (motion-blur frame risk) or when scene lighting continuity matters more than exact pose match.

```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "klingai/video-o1-video-to-video-reference",
    "video_url": prev_clip_url,           # Full previous clip as continuity anchor
    "elements": [{"frontal_image_url": "crew_lead/front.png", "reference_image_urls": ["crew_lead/three_quarter.png"]}],
    "prompt": "...",
    "generate_audio": False,
    "duration": 5,
    "aspect_ratio": "9:16"
}, headers=headers)
# Cost: same as O1 reference-to-video ($1.46/5s Pro tier).
# Requires prev_clip uploaded to a CDN or public URL — not a local path.
# Fall back to I2V frame-chaining if prev_clip is not yet uploaded.
```

## InsightFace buffalo_l Benchmarks

| Model | Backbone | LFW | CFP-FP | AgeDB-30 | IJB-C(E4) | Size | FPS (RTX-3090, batch=1) | Notes |
|-------|----------|-----|--------|----------|-----------|------|------------------------|-------|
| buffalo_l | R50 / W600K (w600k_r50) | 99.83% | 99.33% | 98.23% | 97.25% | 326MB | 450 FPS | Production default |
| buffalo_m | R50 / W600K | same as buffalo_l | — | — | — | ~200MB | 900 FPS | Batch QA; identical accuracy |
| buffalo_s (CPU fallback) | R18 / W600K | 99.70% | 98.00% | — | — | 159MB | — | Edge/mobile only |
| antelopev2 | R100 / Glint360K (glintr100) | — | — | — | higher | 407MB | — | Better on harder cases; lower raw cosine range 0.30–0.45 at FMR 1e-4 |

**buffalo_m (pass 9 finding, 2026-05-23):** Identical accuracy to buffalo_l but 2× faster throughput (900 vs 450 FPS on RTX-3090). Use buffalo_m for batch QA pipelines (many frame extractions in one session) where speed matters. Use buffalo_l for per-clip evaluation where accuracy is paramount. Same threshold calibration as buffalo_l applies.

**Batch QA optimization (pass 14 finding, 2026-06-04):** When running QA across 5+ clips in one session (15+ frames total), collecting all extracted frames first and then running them through `app.get()` in rapid succession with `buffalo_m` is significantly faster than per-clip sequential processing. ONNX Runtime batch inference at batch=8 provides a **3.2× speed-up** vs batch=1 — but `FaceAnalysis.get()` is single-image-only; to exploit batch throughput, use the underlying `ArcFaceONNX` model directly on pre-aligned face crops. For most production sessions (3–5 clips), per-clip `buffalo_l` is fine. For high-volume batch sessions (10+ clips), switch to `buffalo_m` and pre-collect all frames.

**TensorRT FP16 (pass 14 finding, 2026-06-04):** Converting buffalo_l ONNX to FP16 via TensorRT gives an additional **1.8× FPS** boost with <0.05% accuracy drop. Practical only if TensorRT is installed in the environment. INT8 quantization is even smaller (4× model size reduction, 0.02% ArcFace embedding error increase) but requires calibration data. Not needed for our current clip volumes.

## Kling Element Library Auto-View Generation

Upload ONE good front-facing reference; enable "AI-generate additional views" in Kling web UI. Saves ~$0.39 vs 4 separate NBP calls. **Caveat:** web UI feature only — not exposed via AIMLAPI as of 2026-04.

## face_consistency Parameter (Kling v3 / O1 — Research 2026-05-04)

```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "klingai/video-o1-reference-to-video",
    "prompt": "...",
    "elements": [...],
    "face_consistency": True,   # Occlusion recovery — add when face may be partially hidden
    "generate_audio": False,
    "duration": 5,
    "aspect_ratio": "9:16"
}, headers=headers)
```

**When to set `face_consistency: True`:** Face partially covered — hands near face, carrying box, hat brim, strong shadows. **AIMLAPI passthrough unverified as of 2026-05-04.** Test on draft before Pro.

**Do NOT set for full clear face visibility** — adds latency with no benefit.

## Act-Two — Performance-Drive Animation Pathway (pass 11 finding, 2026-05-30)

`runway/act_two` on AIMLAPI transfers performance (facial expression, gesture, body movement) from a driving video onto a character reference image. **$0.065/sec** — 4.5× cheaper than Kling v3 Pro ($0.291/sec) for character shots.

**When to use:** You have a driving video of someone performing the action (e.g., owner Farouq records himself carrying a box, gesturing, or speaking). Act-Two maps that performance onto Karel/Mourad's reference image. The character's face and clothing come from the reference image — only the motion is transferred.

**When NOT to use:** You need a fully generative shot (no driving video available). Use Kling O1 reference-to-video instead.

```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "runway/act_two",
    "character": {
        "type": "image",
        "url": "https://cdn.example.com/characters/crew_lead/front.png"
    },
    "reference": {
        "type": "video",
        "url": "https://cdn.example.com/performance/owner_carrying_box.mp4"
    },
    "body_control": True,          # enable full body movement (not just face)
    "expression_intensity": 3,     # 1–5; default 3. Lower for subtle scenes.
    "width": 720,
    "height": 1280,
    # No generate_audio or audio params — Act-Two is video-only output
}, headers=headers, timeout=120)
# Response: result["video"]["url"]
```

**Key rules:**
- Driving video MUST have character facing same general direction as character reference
- Content policy: output face = character reference (halal-compliant if ref is compliant)
- Run InsightFace QA on output — misaligned driving/reference angles degrade identity
- Driving video does NOT need to be halal-compliant (it's never in the output); only the output is QA'd
- Act-Two generates no audio — add voiceover in post via FFmpeg, same as all other clips

## Veo 3.1 Reference-to-Video — BLOCKED for Character Shots

- **Cost: ~$0.788/sec → $6.30 per 5s clip** (vs Kling v3 Pro $0.291/sec → $1.46 per 5s clip)
- **4× more expensive** than Kling v3 Pro, no evidence of superior identity lock
- **DO NOT use for character shots.** Kling O1 reference-to-video remains correct model.

## Kling O3 — Future Watch for Character Consistency (NOT on AIMLAPI as of 2026-06-03)

Kling O3 (Omni, released Feb 2026) introduces major character consistency upgrades. **O3 is NOT on AIMLAPI.** AIMLAPI still serves only `klingai/video-o1-reference-to-video`. O3 is confirmed live on: Runware (`klingai:kling-video@o3-4k`, since April 23, 2026) and fal.ai (`fal-ai/kling-video/o3`). Per Farouq directive, AIMLAPI-only pipeline — do not use Runware/fal.ai until O3 lands on AIMLAPI. Monitor AIMLAPI changelog.

**O3 advantages for character shots:**
- Multi-shot: up to 6 shots in a single API call with consistent character across all shots (max 15s total, each shot ≥ 3s)
- `face_consistency: True` confirmed functional on fal.ai/Atlas Cloud — forces face reconstruction from image_reference even when occluded (hands, hat, shadows)
- `kling_elements` replaces O1's `elements` array — inline element definition with `name`+`description`+`element_input_urls` (2–4 images)
- Stronger element binding (3D Spacetime Joint Attention)

**O3 multi-shot `multi_prompt` parameter structure (for when O3 lands on AIMLAPI):**
```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "klingai/video-o3-reference-to-video",   # model ID TBC on AIMLAPI
    "image_url": last_frame_url,                       # renamed from start_image_url
    "kling_elements": [                                # replaces elements[] in O3 (pass 9 correction)
        {
            "name": "crew_lead",                       # referenced in prompt as @crew_lead
            "description": "moving company crew member, olive skin, navy polo, cargo trousers",
            "element_input_urls": [                    # 2-4 images: front + angles
                "https://cdn/crew_lead/front.png",
                "https://cdn/crew_lead/three_quarter.png",
                "https://cdn/crew_lead/profile.png",
                "https://cdn/crew_lead/full_body.png"
            ]
        }
    ],
    # max 3 kling_elements per task; each element 2–4 images in element_input_urls
    # prompt uses @crew_lead (not @Element1) — name must match exactly
    "multi_prompt": [                                  # multi-shot control (O3 only, requires multi_shot: true)
        {"prompt": "@crew_lead lifts a box from the truck, golden hour", "duration": 5},
        {"prompt": "@crew_lead carries box to doorway, focus pull", "duration": 5}
    ],
    "multi_shot": True,                               # required to activate multi_prompt (singular — NOT multi_shots)
    "face_consistency": True,
    "generate_audio": False,   # CRITICAL: O3 audio defaults ON — must set explicitly
    # Native Kling 3.0 API uses "sound" param; AIMLAPI likely remaps to "generate_audio" (consistent with V3)
    "negative_prompt": "ghost driving, blurry, distorted anatomy, extra limbs",  # still present in O3
    "cfg_scale": 0.5,          # still present in O3, default 0.5
    "aspect_ratio": "9:16"
}, headers=headers)
```

**O3 breaking changes vs O1 (confirmed across fal.ai/Runware/Atlas/Freepik/PiAPI — pass 12 correction):**
- `start_image_url` → renamed to `image_url`
- `elements` array → replaced by `kling_elements` array (max 3 elements, each with `name`+`description`+`element_input_urls` of 2–4 images) — **NOT `image_reference`**
- Prompt references elements by `@name` (element name field), not `@Element1`
- `multi_shot: True` required to activate `multi_prompt` (multi-shot control) — singular, NOT `multi_shots`
- `negative_prompt` **STILL PRESENT** — default "blur, distort, and low quality" (prior pass incorrectly said REMOVED)
- `cfg_scale` **STILL PRESENT** — default 0.5 range 0–1 (prior pass incorrectly said REMOVED)
- Audio: native Kling 3.0 API uses `sound` (bool); AIMLAPI likely remaps to `generate_audio` (consistent with how it handles V3). Always set to OFF explicitly regardless of param name.
- `generate_audio` defaults **ON** in O3 (was off by default in O1) — ALWAYS set `False` explicitly
- Text prompts capped at 2,500 characters; each @element reference consumes 37 characters
- New `shot_type` param: `"intelligent"` (auto scope selection) or `"customize"` (manual control)
- AIMLAPI endpoint pattern will shift from `/v3/` to `/o3/`

**Action on O3 landing on AIMLAPI:** Confirm `kling_elements` parameter passthrough with a draft test; update frame-chaining snippet (`start_image_url` → `image_url`). Do NOT remove `negative_prompt` or `cfg_scale` — they still work.

## Kling Image O3 — Future Watch for Hero Frames (NOT on AIMLAPI as of 2026-06-03)

Kling Image O3 (released Feb 2026, available on Runware) is a significant upgrade from Image O1 for character hero frame generation. Not yet on AIMLAPI.

**Key advantages over Kling Image O1 for hero frames:**
- **Native 4K output** — no upscaling needed, ready for commercial print
- **Up to 10 reference images** with `image_reference` array (vs O1's standard multi-ref)
- **@ tag syntax** in prompts: `@Character1 carries a box toward @Character2` — identity tagging prevents feature swapping in multi-character scenes
- **Reference Attention Mechanism** — locks face, build, clothing across different seeds and scenes
- **Visual Chain-of-Thought (vCoT)** — model "plans" before rendering; reduces anatomy errors and clothing drift

**When O3 image lands on AIMLAPI — routing matrix change:**
- Kling Image O3 would replace Kling Image O1 ($0.040/img) for production hero frames
- Check pricing: if ≤ $0.10/img → upgrade immediately; if > $0.195/img → keep NBP Edit

**Current hero frame routing stays unchanged until Kling Image O3 confirms on AIMLAPI.**

## Shari'ah-Specific Character Rules
- Male crew: long trousers, covered 'awrah, modest work clothing
- Female family members (if depicted): full hijab, loose-fitting garments
- MUST specify exact clothing in prompts — MUST NOT leave it to the model's default
- MUST include clothing description in EVERY prompt, even if character appeared in a previous shot
- Reference images themselves MUST be Shari'ah compliant — MUST run QA on character sheets before using

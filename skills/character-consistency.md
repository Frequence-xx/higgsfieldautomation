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
    "negative_prompt": "morphing, face morphing, shifting jawline, hairstyle change, outfit change, extra characters, age change, blurry, flickering, extra limbs",
    "generate_audio": False,
    "duration": 5,
    "aspect_ratio": "9:16"
}, headers=headers)
```

**Important:** Elements extract face + posture + clothing together. **No face_weight API parameter exists on AIMLAPI.** "Subject Binding 80-90" in CLAUDE.md is a quality target, not a parameter.

### Step 3a: Differential Prompt Rule — Action + Camera Only When Refs Are Provided (pass 24 finding, 2026-06-29; DomainShuttle validation pass 30, 2026-07-13)

When `elements` or `image_url` reference images are provided, describe **only what changes** from those references — NOT the character's static attributes. References already carry face, build, skin tone, and clothing; redundant description competes with the reference signal and can cause identity drift.

**DO (differential — action + camera only):**
```
@Element1 lifts a moving box from the truck, pivots left 30 degrees, eases to stop at the doorway
```

**DON'T (redundant character description competing with refs):**
```
The man with short dark brown hair and olive skin wearing a navy polo shirt and cargo trousers lifts a box and walks toward the door
```

**Seven elements framework (AnyID, arXiv 2603.25188):** shot type, hairstyle, clothes, accessory, expression, action, background. Only describe what **differs** from the reference. Action and camera move are almost always the only things that change — those are what the prompt should specify.

Independently confirmed by Atlas Cloud Kling 3.0 prompt guide: *"With image-to-video, the model already sees your starting frame, so repeating descriptions wastes characters… drop the Subject and Scene description that the image already supplies, and lead with Subject Movement plus Camera Language."*

**Exception:** If the scene places the character in a context NOT visible in any reference (new background, new lighting), briefly describe the new context. Do NOT re-describe attributes already shown in refs.

**DomainShuttle research validation (arXiv 2606.26058, June 2026):** DomainShuttle introduces Video-Reference DualRoPE — reference image tokens and video generation tokens are placed in **separate RoPE spaces**. This proves architecturally that identity description in the motion prompt competes directly with reference embeddings (same embedding space, interference guaranteed). The correct design isolates identity to the reference channel and text to action+camera only. No public code or AIMLAPI endpoint — research only, validates our existing differential prompt rule.

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
    "negative_prompt": "morphing, face morphing, shifting jawline, hairstyle change, outfit change, extra characters, age change, blurry, flickering, extra limbs, distorted anatomy",
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

**InsightFace install (pass 10 finding, 2026-05-25; pass 43 recheck, 2026-08-23 — v1.0.1 still latest):** InsightFace 1.0.1 (released May 23, 2026) no longer builds the `face3d` Cython/C++ extension by default. Standard `pip install insightface` now works without a C++ compiler. Our QA pipeline uses only `FaceAnalysis` (detection + recognition) — no `face3d` needed. If face3d is ever required, opt in explicitly: `pip install "insightface[face3d]"` or set `INSIGHTFACE_WITH_FACE3D=1`.

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

FaceFusion **v3.8.2** is the current stable release (August 10, 2026; pass 43 recheck, 2026-08-23 — still latest, no new version). Previously v3.7.1 (July 5, 2026).

**⚠️ CRITICAL — FFmpeg 9 Compatibility (pass 39 finding, 2026-08-16):** FFmpeg 9.0 (released Aug 4, 2026) **removed the `-vsync` flag** (use `-fps_mode` instead). FaceFusion 3.7.x and earlier use `-vsync` internally — **any FaceFusion version < 3.8.2 is broken with FFmpeg 9.0.1**, which is our pipeline's current FFmpeg version (documented SC256). **Upgrade to FaceFusion 3.8.2 before running any FaceFusion jobs.** Failure mode: silent pipeline error or crash at the FFmpeg compositing step.

**3.8.0 changes (pass 39 finding, 2026-08-16):**
- `--workflow-strategy` argument: `memory` (faster, higher RAM use) or `disk` (slower, RAM-efficient). Add `--workflow-strategy memory` for speed on high-RAM machines; use `disk` if OOM errors occur during batch processing.
- `--workflow-mode` argument: aligns with upcoming architecture changes (no production-visible effect yet).
- **AV1 support** via FFmpeg decoding and encoding. Use `--output-video-encoder libsvtav1` for better compression if needed (our default stays `libx264rgb` for skin-tone fidelity — do not change).
- `--temp-pixel-format`: alpha channel support for compositing workflows. Not relevant to our face-swap pipeline.

**3.8.2 fixes (pass 39 finding, 2026-08-16):**
- **Fixed broken pipeline with FFmpeg 9 after `-vsync` removal** — the primary reason to upgrade immediately.
- Fixed incorrect frame enhancer output for in-memory processing.
- Frame enhancer model now drives output scale in UI.

**3.7.1 changes (pass 27 finding, 2026-07-06):**
- **Frame distribution fix:** 3.7.0's multi-frame-aware architecture introduced a performance regression; 3.7.1 restores throughput to pre-3.7.0 levels.
- **2-processor bug fix:** Fixed image-to-image workflow when using exactly 2 processors. **Directly affects our pipeline** — `face_swapper + face_enhancer` and `face_swapper + expression_restorer` combos were broken in 3.7.0 on still-image inputs.

**3.7.0 changes (pass 25 finding, 2026-07-02):**
1. **Multi-frame aware processors:** Processors now consider neighboring frames simultaneously rather than processing each frame in isolation. This directly improves temporal consistency in video output — less flickering, morphing, and facial geometry shifts between frames. Benefit for our clips: expression_restorer and face_enhancer should produce smoother cross-frame results on 5s clips.
2. **Auto face selector mode:** New `--face-selector-mode auto` automatically matches the source face to the most similar target face. Useful for clips where the character's face may shift slightly across frames — removes need to manually set `--reference-face-position`. Use `reference` mode when target has multiple people; use `auto` for single-character clips.
3. **Breaking changes (install and args):** `--onnxruntime` is now a positional argument (not a named flag — update install scripts). `--system-memory-limit` argument **removed** (if set in any scripts, delete it).

FaceFusion v3.6.0+ uses a **job-based architecture** — `run` is replaced by `headless-run`. The old `python facefusion.py run --headless` syntax is broken in v3.

```bash
conda create -n facefusion python=3.12 -y && conda activate facefusion
git clone https://github.com/facefusion/facefusion && cd facefusion
# IMPORTANT: use v3.8.2+ — earlier versions break with FFmpeg 9 (see FFmpeg 9 warning above)
git checkout 3.8.2
# v3.7.0+: --onnxruntime is now positional (no flag name needed)
python install.py cpu  # or: python install.py cuda  (positional, not --onnxruntime cuda)

# v3.7.0 syntax (headless-run, NOT run)
python facefusion.py headless-run \
  --source-paths /path/to/approved_character_front.png \
  --target-path /path/to/failed_clip.mp4 \
  --output-path /path/to/fixed_clip.mp4 \
  --processors face_swapper face_enhancer \
  --face-swapper-model inswapper_128_fp16 \
  --face-selector-mode reference \  # use "auto" for single-character clips (v3.7.0+)
  --reference-face-position 0 \     # only needed with "reference" mode
  --face-enhancer-model gfpgan_1.4 \
  --face-enhancer-blend 80
# NOTE: --system-memory-limit is REMOVED in v3.7.0 — delete from any existing scripts
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

**LaVieID — Future Watch (arXiv 2508.07603, ACM MM 2025, code released, pass 40 finding, 2026-08-17; code status confirmed pass 41, 2026-08-19):** Local Autoregressive Diffusion Transformers for Identity-Preserving Video Creation. Code: github.com/ssugarwh/LaVieID. **Code IS released** (4 commits as of 2026-08-19). Tested environment: Python 3.12.4, PyTorch 2.1.0+, CUDA 12.8 (Python 3.10 recommended if xformers/diffusers compatibility issues arise). No formal release tags — clone from master. Key mechanisms: (1) **Local Router** — represents latent states as weighted combinations of fine-grained local facial structures, directly alleviating feature interference between identity cues and background/clothing content (the mechanism that causes our known identity drift under large head rotations); (2) **Temporal Autoregressive Module** — divides denoised latent tokens into temporal chunks and exploits long-range temporal dependencies to predict correction biases per chunk before video decoding, significantly improving inter-frame identity consistency over 5s clips. No AIMLAPI endpoint as of 2026-08-19. **Practical implication now:** The Local Router validates our 4-ref strategy — providing geometrically distinct face views gives the model distinct "local structures" to anchor against, reducing feature interference. The temporal chunk correction mechanism suggests that longer clips (10s+ at O3) benefit more from this architecture than short 5s clips; for our 5s standard, Kling O1 elements remain the correct choice until a LaVieID-based endpoint appears on AIMLAPI.

**Show and Polish — Future Watch (arXiv 2507.10293, MM 2025, July 2025):** Reference-Guided Identity Preservation in Face Video Restoration (IP-FVR). Accepted at ACM Multimedia 2025. Core mechanism: uses a high-quality reference face photo as a visual prompt injected via decoupled cross-attention during denoising, recovering identity-specific features in degraded/compressed face video. Also addresses intra-clip identity drift. **Practical implication for our pipeline (pass 38 finding, 2026-07-27):** Complements FaceFusion — where FaceFusion swaps/corrects identity post-generation, IP-FVR restores quality in degraded clips *while* using the reference to anchor identity. Useful when a clip passes InsightFace QA but has visible compression artifacts or low quality. No confirmed public code repo. Monitor for code release — if available as a REST endpoint, could replace the CodeFormer step in the FaceFusion pipeline for olive/brown-skin characters (CodeFormer can whiten skin; IP-FVR preserves reference appearance more faithfully).

**GSwap — Future Watch (research stage, no OSS code as of 2026-06-17):** 3D head swap using neural Gaussian portrait representation embedded in SMPL-X body surface (arXiv 2603.23168, IEEE TVCG, March 2026). Models head, torso, and motion together (not just 2D face patch), with neural re-rendering for natural background integration. Addresses FaceFusion's known failure mode: detached/misaligned look under strong head motion. Project page: ustc3dv.github.io/GSwap/ — no public code release confirmed. Monitor for open-source release — would replace FaceFusion for clips with large head rotation or motion blur.

**IMPORTANT CODE CONFUSION (pass 20 finding, 2026-06-17):** Search engines return `github.com/chiehwangs/gaussian-head` as a GSwap result — this is **NOT GSwap**. It is GaussianHead (TVCG 2025, "High-fidelity Head Avatars with Learnable Gaussian Derivation"), a completely different project by different authors. GSwap has no confirmed open-source GitHub repo as of 2026-06-17. Do NOT clone GaussianHead expecting GSwap functionality.

**ST-DRC — Future Watch (arXiv 2606.02441, June 1, 2026, research only):** Spatial-Temporal Decoupled Reference Conditioning for identity-preserving T2V generation. Backbone: LTX-2.3 (22B param, open-source). Key mechanisms: (1) **Latent in-context injection** — reference image encoded with video VAE and concatenated to noisy latents (no extra adapters needed); (2) **TASS-RoPE** (Temporal-Adjacent Spatial-Shifted RoPE) — places reference tokens adjacent to video in time but shifted in space, letting identity flow through spatio-temporal attention while blocking pixel-level copy-paste shortcuts (directly addresses our known copy-paste artifact failure mode in multi-ref generation); (3) **Three-stream CFG** — independently controls text adherence vs. reference fidelity at inference time. No public code or production API as of 2026-06-27. When LTX-2.3-based endpoints appear on AIMLAPI, ST-DRC-style models are worth testing for character identity. **Practical implication now:** TASS-RoPE validates our current mitigation — keep characters spatially separated in prompts and use tight face crop as 4th ref — both reduce the copy-paste risk TASS-RoPE solves architecturally.

**InfinityStory — Future Watch (arXiv 2603.03646, March 2026, Adobe Research / Meta AI / KAUST):** Unlimited video generation framework for long-form storytelling with multi-subject character-aware shot transitions. Key mechanisms: (1) **Background-Consistent Generation Pipeline** — maintains visual coherence across shots without re-generating backgrounds each cut; (2) **Character-Aware Shot Transition module** — explicitly models multi-subject identity during shot-to-shot transitions, preventing character swap at the cut point. On VBench: achieves highest Background Consistency (88.94) and Subject Consistency (82.11) scores, with best average rank (2.80) across all metrics. Scalable to hour-long narratives. **Practical implication for our pipeline (pass 36 finding, 2026-07-25):** The Character-Aware Transition module confirms that shot boundaries are the highest-risk point for identity loss — exactly why our policy (re-anchor every clip from original reference photos, never from prior clip's last frame for identity) is correct. InfinityStory's identity-at-transition design also validates re-anchoring via `elements` on every Kling call rather than relying on continuity from the prior clip's last frame alone. No public code or AIMLAPI endpoint — research only.

**ARGUS — Future Watch (arXiv 2606.11670, June 10, 2026, no public code):** Stacked Multi-View Identity Mosaic Injection (SMII) for subject-preserving video generation. Backbone: Wan-based. Key mechanism: converts MLLM-selected image/video identity evidence into a 3×3 stacked mosaic, synchronizes the mosaic with the diffusion timestep, and injects it as negative-time read-only memory in Wan's native token space — bypassing external adapters entirely. Addresses the same problem our Kling element binding partially solves: identity lock under large viewpoint changes, occlusion, and expression shifts. No public code or AIMLAPI endpoint as of 2026-07-04. **Practical implication now:** The 3×3 mosaic maps naturally to our existing 3–4 multi-view ref set (front + 3/4 + profile + face crop) — ARGUS validates this coverage strategy. When SMII-based Wan endpoints appear on AIMLAPI, test for Karel/Mourad identity stability vs Kling O1.

**EntityBench (arXiv 2605.15199, May 2026):** New benchmark measuring multi-shot character consistency. Key production finding: **cross-shot entity consistency degrades sharply with recurrence distance** — the more shots between appearances, the worse identity hold. Benchmark covers up to 50 shots with recurrence gaps spanning 48 shots. Validates our policy: every clip must independently anchor from original approved reference photos, not from the prior clip's last frame. "EntityMem" (paired method) improves long-range consistency by establishing visual identity once from a canonical source and reusing it — exactly our character.json + original photo anchoring workflow.

**GroundShot (arXiv 2606.20799, June 2026):** Training-free, model-agnostic framework for multi-shot entity consistency. **Key production implication: "the visual quality of the first appearance sets the consistency ceiling for all later appearances."** A weak hero frame produces weak identity lock across all subsequent clips — no amount of Subject Binding or InsightFace retry will recover from a poor reference. This validates prioritizing hero frame QA above all else (gate 2: "QA every hero frame against brand reference before animation"). GroundShot's quality-aware shot scheduling — generate reference-source shots before dependent shots — also validates our sequential one-clip-at-a-time approach rather than batching.

**FaithfulFaces — Research Validation (arXiv 2605.04702, May 2026):** Pose-faithful facial identity preservation for T2V generation. Core finding: identity features and pose features are entangled in face embeddings — injecting a single face embedding carries both, and when the output clip involves a pose angle not shown in the reference, identity distorts. FaithfulFaces introduces a "pose-shared identity aligner" that maps facial views into a global pose representation via explicit Euler angle embeddings and a pose-variation / identity-invariance constraint, so the identity features become pose-agnostic. **Practical implication for our pipeline (pass 28 finding, 2026-07-09):** This is the academic explanation for why our 3-angle ref strategy (front + 3/4 + profile) works — covering the major pose variants ensures the model sees identity cues at every angle the output clip might use. It also validates the tight face crop as 4th ref: a tight crop isolates the identity-invariant features (eye shape, bone structure, skin tone) with minimal pose ambiguity. No public model or AIMLAPI endpoint — research only, validates existing pipeline.

**Identity-Action Decoupling — IaD Framework (arXiv 2606.22347, June 2026):** Addresses a failure mode in inference-time identity injection (ConsisID, ID-Animator): injecting facial identity features also injects pose and expression info from the reference image, making the model generate monotonous or incorrect facial movements even when the prompt requests specific action. IaD introduces two loss functions — **Identity Decoupling Loss (L_ID)** separates identity features from pose/expression attributes; **Text Alignment Loss (L_TA)** ensures the decoupled action space follows the text prompt faithfully. Result: rich, controllable expressions and scene variations while maintaining cross-temporal identity consistency, without subject-specific fine-tuning. **Practical implication for our pipeline (pass 28 finding, 2026-07-09):** Provides the academic grounding for WHY our differential prompt rule (Step 3a) works — prompts that describe ONLY action + camera, letting references carry identity, avoid the identity/action entanglement problem IaD solves architecturally. When retrying a clip with wrong facial movement, check whether the motion prompt contains identity-descriptive words ("the friendly man", "the olive-skinned person") competing with the reference signal — strip these to action-only. No public code or AIMLAPI endpoint as of 2026-07-09 — research only.

**IPT2V Spatial-Temporal Decoupling — Research Validation (arXiv 2507.04705, ACM MM 2025, Tencent YouTu Lab; pass 41 finding, 2026-08-19):** "Identity-Preserving Text-to-Video Generation Guided by Simple yet Effective Spatial-Temporal Decoupled Representations." Key finding: identity-preserving video generation suffers a spatial-temporal trade-off — optimizing for spatially coherent character identity (staying in character) competes with temporally smooth motion dynamics (natural movement). The framework decouples spatial representations (layout, character identity) from temporal representations (motion dynamics) using a two-stage generation paradigm: first generate a spatially coherent keyframe with identity locked, then generate temporal motion separately. **Practical implication for our pipeline:** Validates our prompt structure of separating identity (carried by reference images) from motion (described in text prompt only). Do NOT describe motion and identity attributes simultaneously in the same prompt — they compete in the embedding space. The differential prompt rule (Step 3a) is architecturally justified by this paper. No AIMLAPI endpoint — research only, validates existing pipeline.

**Avatar V — Future Watch (arXiv 2606.13872, HeyGen, released April 8, 2026; pass 30 finding, 2026-07-13):** Video-reference avatar generation from HeyGen. Key mechanism: conditions on the **full token sequence of a reference VIDEO** (not just still images) at every transformer layer via Sparse Reference Attention (linear complexity vs reference length). Unlike our current still-image refs, Avatar V extracts "video-DNA" — talking rhythm, micro-expressions, gesture habits — from the reference clip. The identity-aware super-resolution refiner reuses the full reference conditioning for output upscaling. Available on HeyGen's API (`developers.heygen.com`). **NOT on AIMLAPI — AIMLAPI-only pipeline.** When Avatar V or equivalent appears on AIMLAPI, prioritize over still-image refs for characters.

**Practical implication NOW:** This validates our existing `klingai/video-o1-video-to-video-reference` pathway. A 15-second reference clip of Karel or Mourad working (carrying a box, walking purposefully) carries richer temporal identity than 4 still photos — the model sees actual motion, micro-expressions, and posture dynamics. When filming crew reference material: prioritize capturing a short reference clip (15–30s, even with phone, stable lighting) in addition to the 4 still reference photos. Use the clip as the `video_url` element for Kling O1 video-to-video-reference instead of still images when available.

**Avatar V — NOT for our pipeline today:** HeyGen's API requires avatar enrollment (user submits a 15s reference clip to create a persistent avatar object). This enrollment-then-animate workflow differs from our per-call element binding. Content-policy note: HeyGen's platform is not shariah-reviewed; AIMLAPI pipeline avoids these concerns.

**Aura — Future Watch (arXiv 2607.04311, July 7, 2026, code released):** Consistent multi-subject video generation via VLM-Grounded Semantic Alignment. Code: github.com/Camellia997/Aura. Two key innovations: (1) **AI director-level captions** — dense, structured descriptions of video content that capture scene dynamics and subject interactions rather than simple noun-phrase descriptions; (2) **VLM-Grounded Semantic Alignment** — two-stage alignment that progressively maps VLM features into the DiT feature space, bridging the gap between language understanding and visual generation. Directly improves multi-subject identity consistency where existing methods struggle. No AIMLAPI endpoint as of 2026-07-11. **Practical implication now:** The "AI director-level caption" concept validates writing prompts that describe inter-character dynamics explicitly ("Image1 hands the box to Image2, who turns left to carry it inside") rather than listing character actions independently. This gives the model richer relational context for multi-character shots. Monitor for hosted API — when Aura-based endpoints appear (likely as a Wan or CogVideo successor), test on Karel+Mourad two-person shots where feature swapping is a known failure mode.

**MAGREF — Future Watch (ICLR 2026, code released, FP8 available):** Multi-reference video generation with masked guidance and subject disentanglement (arXiv 2505.23742). Code: github.com/MAGREF-Video/MAGREF. Backbone: Wan2.1 14B. Addresses copy-paste artifacts and character entanglement in multi-reference generation — the core problem our Kling element binding partially solves.

**VRAM requirements (pass 17 update, 2026-06-11):**
- Full BF16/FP16: ~70 GB (single H100 required)
- FP8 quantized (ComfyUI): **~40–50 GB** — fits A100 40GB at 480p, H100 80GB at 720p
- **GGUF quantized: ~9–11 GB** — consumer GPU now feasible (see below)

**FP8 ComfyUI integration:** Kijai published `Wan2_1-Wan-I2V-MAGREF-14B_fp8_e4m3fn.safetensors` (Hugging Face: `Kijai/WanVideo_comfy`) with ComfyUI nodes at `kijai/ComfyUI-WanVideoWrapper`. FP8 reduces from 70GB to ~40-50GB.

**GGUF now available (pass 17 finding, 2026-06-11):** QuantStack released `QuantStack/MAGREF_Wan2.1_I2V_14B-GGUF` on Hugging Face — GGUF quantized versions using city96 conversion scripts, usable with `kijai/ComfyUI-GGUF` node. VRAM by quant level:

| Quant | VRAM | Notes |
|-------|------|-------|
| Q3_K_S | ~7 GB | 480p only; visible quality loss |
| Q4_K_M | ~9.65 GB | Fits 12–16 GB GPU; good quality floor |
| Q5_K_M | ~10.8 GB | Recommended: near-FP8 quality, fits 12 GB with margin |
| Q8_0 | ~15.4 GB | Effectively lossless vs FP16; needs 24 GB |

**Generation speed caveat:** Wan 2.1 14B at Q4 on a single consumer GPU generates a 5s clip in 4–15 minutes (vs seconds for cloud API). Impractical for production throughput — but now feasible for local QA testing and identity calibration runs. Do not use for production clips until cloud-hosted MAGREF API appears (no AIMLAPI endpoint as of 2026-06-17).

**Gloria — Future Watch (arXiv 2603.29931, March 2026):** Consistent character video generation via "content anchors" — a compact set of anchor frames covering multiple viewpoints AND expression variants. Key mechanisms: (1) **Superset Content Anchoring** — includes both intra-clip and extra-clip cues in the anchor set to prevent view-dependent copy-paste artifacts; (2) **RoPE as Weak Condition** — distinct positional encodings assigned to video vs. conditioning tokens, preventing multi-reference identity collapse. Research model; no public production code as of 2026-06-09.

**Practical implication for our pipeline:** Gloria validates the multi-view anchor strategy (front + 3/4 + profile + face-crop). It also suggests that adding one mild expression variant (e.g., a slight smile) alongside angle refs could further reduce identity collapse in clips that require the character to smile. However, Mv²ID (arXiv 2603.21299) established angular diversity > expression diversity in our current 4-ref cap. **Current policy unchanged.** If a clip drifts specifically on expression-heavy action (character smiling or laughing), test substituting the full-body ref with a smiling expression ref to see if it improves anchoring.

**AnyID — Future Watch (arXiv 2603.25188, March 26, 2026):** Ultra-fidelity identity-preserving video generation from any visual references (faces, portraits, videos). Key innovations: (1) **Omni-referenced architecture** — uses original VAE (not visual experts) to inject identity; unifies heterogeneous reference types (image + video) into one representation; (2) **Primary-referenced generation** — designates one reference as the canonical anchor for all static attributes; (3) **Differential prompt** — describes ONLY what changes from the primary reference (action, expression change, new background), while anything not mentioned stays consistent. No public code as of 2026-06-29; no AIMLAPI endpoint. **Practical implication now (already applied above in Step 3a):** The differential prompt principle is applicable to our Kling O1/O3 prompts today — describe only action + camera, let reference images carry identity.

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
- **Ref count sweet spot:** 3–4 refs optimal; cap at 4 (Kling hard limit). More than 4 increases copy-paste artifact risk ("view-dependent copy-paste," per arXiv 2508.09476 CoFE — paper retitled Dec 2025 from "MoFE" to "Collaborative Face Experts Fusion"; further confirmed by Mv²ID, arXiv 2603.21299, March 2026).
- **Angular diversity > expression diversity:** front + 3/4 + profile is the minimal effective multi-view set (confirmed by Mv²ID and MoFE research). Do NOT replace an angle ref with an expression variant — cover angles first.
- **Include a tight face crop as the 4th ref (pass 15 finding, 2026-06-07):** Within the 4-ref cap, replace the full-body standing ref with a tight face crop (eyes-to-chin, no hair, flat background). Mv²ID (arXiv 2603.21299) establishes that region-focused conditioning on the face area is the primary identity signal under large angle variations — simply adding more full-body refs exacerbates copy-paste without improving identity lock. Save as `assets/characters/{name}/face_crop.png` (crop from approved front-view photo). Include as ref 3 or 4. **Especially effective when the character appears in profile or 3/4 view in the generated clip** — the model can extract identity from the face-crop ref even when the full-body angle differs.
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

**InsightFace Server (released 2026-07-27, pass 40 finding):** New product from DeepInsight — self-hosted web UI + snake_case REST API + Python client for detection, comparison, registration, and person search. Runs in a single Linux x86_64 Docker container (CPU or NVIDIA GPU) using local ONNX Runtime. Key addition: **INT8 embedding quantization** — 0.02% ArcFace error increase at 4× smaller model size (validates INT8 quantization note in TensorRT section below). Scales to 50M+ image search on one RTX 5090. Relevant if QA pipeline is ever refactored to a persistent microservice instead of in-process calls; commercial license required. Not needed for current per-clip QA volume.

**buffalo_m (pass 9 finding, 2026-05-23):** Identical accuracy to buffalo_l but 2× faster throughput (900 vs 450 FPS on RTX-3090). Use buffalo_m for batch QA pipelines (many frame extractions in one session) where speed matters. Use buffalo_l for per-clip evaluation where accuracy is paramount. Same threshold calibration as buffalo_l applies.

**Batch QA optimization (pass 14 finding, 2026-06-04):** When running QA across 5+ clips in one session (15+ frames total), collecting all extracted frames first and then running them through `app.get()` in rapid succession with `buffalo_m` is significantly faster than per-clip sequential processing. ONNX Runtime batch inference at batch=8 provides a **3.2× speed-up** vs batch=1 — but `FaceAnalysis.get()` is single-image-only; to exploit batch throughput, use the underlying `ArcFaceONNX` model directly on pre-aligned face crops. For most production sessions (3–5 clips), per-clip `buffalo_l` is fine. For high-volume batch sessions (10+ clips), switch to `buffalo_m` and pre-collect all frames.

**TensorRT FP16 (pass 14 finding, 2026-06-04):** Converting buffalo_l ONNX to FP16 via TensorRT gives an additional **1.8× FPS** boost with <0.05% accuracy drop. Practical only if TensorRT is installed in the environment. INT8 quantization is even smaller (4× model size reduction, 0.02% ArcFace embedding error increase) but requires calibration data. Not needed for our current clip volumes.

**Face Consistency Benchmark — model selection validation (pass 22 finding, 2026-06-21):** Benchmark paper arXiv 2505.11425 (TCL Research, May 2025) measured face consistency scores across AI video generation models: **Kling AI 92%**, Luma Dream Machine 74%, Runway Gen-4.5 68%. Kling's lead is attributed to its multi-image reference support anchoring identity across 10-second sequences. Wan 2.x not in benchmark. This independently validates Kling as the correct primary model for character shots requiring identity lock — consistent with our routing matrix.

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

**FixTalk — Identity Leakage Risk in Performance-Driven Animation (arXiv 2507.01390, ICCV 2025):** Identity leakage (IL) is a confirmed failure mode in Act-Two and FaceFusion lip_syncer workflows: motion features extracted from the driving video carry the driver's identity information, which can bleed into the output and corrupt the target character's face (especially under extreme poses or large expressions). FixTalk (ICCV 2025) proves this architecturally — identity is embedded in motion features, not cleanly separable by default. Key mechanisms: **EMI (Enhanced Motion Indicator)** decouples identity information from motion features; **EDI (Enhanced Detail Indicator)** re-injects leaked identity features to fix rendering artifacts (rather than discarding them). **Practical implications for our pipeline:**
1. When recording driving videos for Act-Two, prefer drivers whose ethnic appearance and facial geometry is similar to Karel/Mourad — dissimilar drivers increase identity bleed risk.
2. If a clearly different driver is unavoidable, use `expression_intensity: 1–2` (lower end) to reduce motion magnitude and limit identity transfer.
3. Run InsightFace QA with strict threshold (≥0.68 vs the normal ≥0.62) on Act-Two output when the driver differs significantly from the target character.
4. Identity leakage shows up as a score drop below 0.60 — that is the diagnostic signal, not an animation quality issue.
No AIMLAPI endpoint — research only, validates existing QA step.

## Veo 3.1 Reference-to-Video — BLOCKED for Character Shots

- **Cost: ~$0.788/sec → $6.30 per 5s clip** (vs Kling v3 Pro $0.291/sec → $1.46 per 5s clip)
- **4× more expensive** than Kling v3 Pro, no evidence of superior identity lock
- **DO NOT use for character shots.** Kling O1 reference-to-video remains correct model.

## Happy Horse 1.1 — High-Ref Character Video (AIMLAPI blog-confirmed, canary required)

Alibaba ATH/Taotian Group model that generates character-consistent video from up to **9 reference images** in one call — the highest reference count of any model currently accessible. AIMLAPI has published a blog guide; docs.aimlapi.com page not confirmed as of 2026-08-17.

**Key specs:**
- References: up to 9 images (images, video clips, or audio — mixed). Prompt binding: `Image1`, `Image2`, `Video1` (positional, no @ prefix)
- Output: 720P or 1080P, 3–15s clips, 9 aspect ratios including 9:16
- Pricing (Atlas Cloud/EvoLink reference): **$0.14/sec at 720P → $0.70/5s; $0.28/sec at 1080P → $1.40/5s** — AIMLAPI pricing TBC on canary
- Joint audio-video generation in one pass (**audio ON by default — CRITICAL Shari'ah risk**)
- 7-language lip-sync: English, Mandarin, Cantonese, Japanese, Korean, German, French — **Dutch NOT supported**
- Model ID pattern (expect AIMLAPI): `alibaba/happyhorse-1.1` or `alibaba/happyhorse-1.1/reference-to-video`

**⚠️ MANDATORY audio mute** — Happy Horse generates audio by default. Always strip in post:
```bash
ffmpeg -i happyhorse_output.mp4 -an -c:v copy happyhorse_muted.mp4
```
Also attempt to set audio-disable param at API call (param name unconfirmed — use FFmpeg strip as the safety net regardless).

**When to evaluate vs Kling O1:**
- Happy Horse wins on **reference count** (9 vs O1's 4-image element limit) — useful when 4 refs aren't capturing a complex character
- Happy Horse 720P at $0.70/5s is slightly **more expensive** than Kling O3 ($0.5625/5s when it lands) and similar to Kling O1 at $1.46 (Pro). At 720P draft use only.
- Dutch lip-sync not supported → joint audio generation has no production use for our Dutch voiceovers; always mute
- Character identity quality vs Kling O1 for olive/brown-skin characters **unverified** — run InsightFace QA (PASS ≥ 0.62)

**Canary procedure:** 1 Karel/Mourad reference image at 720P, strip audio post, InsightFace score ≥ 0.62. Do NOT use in production without owner-reviewed output passing brand binary checklist. (pass 40 finding, 2026-08-17)

```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "alibaba/happyhorse-1.1",   # model ID TBC — verify on canary
    # Prompt syntax: reference images by [Image 1], [Image 2], ... (not @Image1 or Image1)
    "prompt": "[Image 1] lifts a moving box and walks toward the front door, golden hour light, 9:16",
    # Parameter name: "images_list" confirmed from Python wrapper (array of URLs, 1-9)
    # AIMLAPI adapter may use different name — canary-test both "images_list" and "reference_images"
    "images_list": [                    # confirmed param name from community wrapper; TBC on AIMLAPI
        "https://cdn.example.com/characters/crew_lead/front.png",
        "https://cdn.example.com/characters/crew_lead/three_quarter.png",
        "https://cdn.example.com/characters/crew_lead/profile.png",
        "https://cdn.example.com/characters/crew_lead/face_crop.png",
    ],
    # Mode auto-detected from image count: 0=T2V, 1=I2V, 2-9=R2V (no explicit mode param)
    "aspect_ratio": "9:16",
    "resolution": "720p",
    "duration": 5,
    # NO confirmed audio-disable param — no "mute" option documented on AIMLAPI.
    # FFmpeg strip is MANDATORY (not optional): ffmpeg -i output.mp4 -an -c:v copy muted.mp4
}, headers=headers, timeout=120)
# MANDATORY post-step regardless of API params:
# ffmpeg -i output.mp4 -an -c:v copy muted.mp4
```

## Kling 3.0 Turbo — Character Draft Iteration Model (on AIMLAPI as `v3-standard-turbo`)

Kling 3.0 Turbo officially launched June 17, 2026 as Kuaishou's speed-and-cost-optimized tier. AIMLAPI's `klingai/kling-video-v3-standard-turbo-image-to-video` (documented in cycle 142) is this same model. It is explicitly designed for "rapid creative iteration" / draft use — not final delivery.

**Key facts for character work:**
- Supports `kling_elements` character binding (confirmed for Kling 3.0 family — verify passthrough on AIMLAPI before production adoption)
- Cost: ¥0.8/sec (720P) ≈ **$0.11/sec → ~$0.55/5s clip** — 50% cheaper than Kling v3 Standard ($1.09/5s)
- Output: 720p maximum (vs Standard/Pro up to 1080p, vs Omni up to 4K)
- **Audio ON by default** — `generate_audio: false` is CRITICAL (same audio-default-on risk as O3)
- `cfg_scale` still supported (default 0.5)
- Multi-shot: holds character and setting consistency across up to 6 shots in a sequence

**When to use Turbo for character shots:**
- Use for ALL draft/prompt-iteration loops on character shots — saves $0.54 per iteration vs Standard
- Do NOT use for final delivery clips — quality ceiling is lower than Standard/Pro
- Once prompt is locked on Turbo, regenerate final with Kling v3 Pro I2V at $1.46/5s

**Unverified on AIMLAPI as of 2026-06-19:** `kling_elements` passthrough on v3-standard-turbo. Run one draft before relying on it for character binding. If elements are silently ignored, fall back to Kling O1 reference-to-video for drafts.

## Kling O3 — Character Consistency Upgrade (AIMLAPI model database — CANARY REQUIRED)

Kling O3 (= Kling Video 3.0 Omni, released Feb 2026) introduces major character consistency upgrades.

**⚠️ SC279 finding (2026-08-20): Kling O3 model strings NOW CONFIRMED in AIMLAPI model database** — `klingai/video-v3-omni-720p-image-to-video`, `klingai/video-v3-omni-1080p-image-to-video`, `klingai/video-v3-omni-720p-text-to-video`, `klingai/video-v3-omni-1080p-text-to-video` all found in the AIMLAPI model database. **No dedicated docs page yet (pass 43 recheck, 2026-08-23 confirmed — still database-only, no docs page).** Expected pricing: ~$1.09/5s (720p) / ~$1.46/5s (1080p) based on AIMLAPI's 2.6× markup over Kling list prices. **CANARY REQUIRED before production use** — `kling_elements` syntax and prompt reference syntax (`@element_name` vs `<<<element_1>>>`) unverified on this endpoint. Prior pass 41 recheck (2026-08-19) found nothing; SC279 (2026-08-20, Kling study) found model strings. O3 was previously confirmed live only on Atlas Cloud ($0.15/sec) and EvoLink ($0.1125/sec R2V).

**O3 canary checklist (run before production use):**
1. Call `klingai/video-v3-omni-720p-image-to-video` with Karel `front.png`, single-element `kling_elements` array, 5s, `generate_audio: false`
2. Confirm element syntax: try `@element_name` first; fall back to `<<<element_1>>>` if rejected
3. Score InsightFace (PASS ≥ 0.62 for Karel/Mourad) across t=0, t=2.5, t=5
4. Log cost per 5s clip — confirm pricing vs expected $1.09 (720p) or $1.46 (1080p)
5. Do NOT use in production without owner-reviewed output passing brand binary checklist

**June 17, 2026 Omni upgrade (pass 21 finding):** Kling 3.0 Omni received an editing pipeline extension — now supports 3–15s video input/output and 4K resolution for its video editing workflow. The reference-to-video character binding capabilities are unchanged.

**O3 pricing on official Kling API (pass 16 finding, 2026-06-09):** O3 reference-to-video = **$0.1125/sec = $0.5625/5s** — 2.6× cheaper than current O1 at $1.46/5s. When O3 lands on AIMLAPI, expect AIMLAPI pricing to be slightly higher but still significantly under $1.46. This is a major cost reduction for character shots.

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
    # element_input_video_urls: optional video URL (3–8s clip) for motion-DNA identity lock
    # element_input_audio_urls: optional audio URL (5–30s) for voice binding — DO NOT USE (Shari'ah)
    # ELEMENT REFERENCE SYNTAX (SC149+SC177 correction):
    # Native Kling API: <<<element_1>>>, <<<element_2>>> (triple brackets, positional)
    # fal.ai wrapper:   @Element1, @Element2 (same as v3 Pro)
    # Most wrappers:    @crew_lead (name-value matching "name" field) — SC177: try this first on AIMLAPI
    # AIMLAPI wrapper: canary-test on O3 landing — try @element_name first, fall back to <<<element_1>>>
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
- Prompt references elements: **native Kling API** = `<<<element_1>>>` triple-bracket positional; **fal.ai wrapper** = `@Element1` positional; **kie.ai and most third-party wrappers** = `@element_name` name-based (matching the `"name"` field in kling_elements — confirmed via kie.ai official docs with example `@element_dog` → `{"name": "element_dog", ...}`). When O3 lands on AIMLAPI, canary-test `@element_name` first (most wrappers use this); fall back to `<<<element_1>>>` if rejected. (pass 22 correction: earlier advice of "try `<<<element_1>>>` first" was incorrect for wrapper APIs)
- `multi_shot: True` required to activate `multi_prompt` (multi-shot control) — singular, NOT `multi_shots`
- `negative_prompt` **STILL PRESENT** — default "blur, distort, and low quality" (prior pass incorrectly said REMOVED)
- `cfg_scale` **STILL PRESENT** — default 0.5 range 0–1 (prior pass incorrectly said REMOVED)
- Audio: native Kling 3.0 API uses `sound` (bool); AIMLAPI likely remaps to `generate_audio` (consistent with how it handles V3). Always set to OFF explicitly regardless of param name.
- `generate_audio` defaults **ON** in O3 (was off by default in O1) — ALWAYS set `False` explicitly
- Text prompts capped at 2,500 characters; each @element reference consumes 37 characters
- New `shot_type` param: `"intelligent"` (auto scope selection) or `"customize"` (manual control)
- AIMLAPI endpoint pattern will shift from `/v3/` to `/o3/`

**Action on O3 landing on AIMLAPI:** Confirm `kling_elements` parameter passthrough with a draft test; update frame-chaining snippet (`start_image_url` → `image_url`). Do NOT remove `negative_prompt` or `cfg_scale` — they still work.

## Wan 2.7 R2V — Character Shots at Lower Cost (Coming Soon on AIMLAPI — NOT YET LIVE as of 2026-07-17)

`alibaba/wan-2-7-r2v` is the Reference-to-Video mode of Wan 2.7. **As of 2026-07-09 (pass 28), the model ID `alibaba/wan-2-7-r2v` appears in the AIMLAPI model database** — search results confirm it alongside `alibaba/wan-2-7-i2v` and `alibaba/wan-2-7-t2v`. However, no dedicated R2V docs page at `docs.aimlapi.com` has been confirmed yet (only the I2V page exists). Status upgrade: "Coming Soon" → "likely live — must canary-test before production adoption." AIMLAPI AIMLAPI has not published the R2V parameter schema yet; use Segmind/Replicate docs as reference for expected params. (previously NOT on AIMLAPI as of 2026-07-06, pass 27)

**Why it matters:** Official Wan 2.7 credit structure: **$0.125/sec → $0.625/5s at 720P**; $0.1875/sec → $0.9375/5s at 1080P. This is ~**2.3× cheaper** than Kling O1 at $1.46/5s at 720P (not 3× — earlier estimate of $0.50/5s was too low). Pricing above reflects Segmind/official Wan 2.7 rates; AIMLAPI pricing when R2V lands may differ. Use 720P for drafts, 1080P only for finals.

### AIMLAPI Wan 2.6 R2V — Correct Parameters (pass 19 finding, 2026-06-16)

AIMLAPI's Wan 2.6 R2V uses **`video_urls`** (not `reference_images`) and **"character1"/"character2"** prompt binding (NOT "Image1"). It accepts VIDEO references only — not static images. This makes it less useful for photo-based character sheets (use Kling O1 instead for image refs).

```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "alibaba/wan-2-6-r2v",
    "prompt": "Character1 carries a box confidently toward the moving truck, golden hour, no ghost driving",
    "video_urls": [
        "https://cdn.example.com/crew_lead/reference_clip.mp4",   # reference VIDEO clip
    ],
    # For 2 characters: video_urls=[clip1, clip2], prompt uses "Character1 and Character2 carry boxes"
    "duration": 5,
    "aspect_ratio": "9:16",
    "generate_audio": False,   # confirm param name — may be different
}, headers=headers, timeout=120)
```

**Critical constraints for Wan 2.6 R2V on AIMLAPI:**
- `video_urls` takes VIDEO clips, not static images — requires recording a short reference clip of the character
- Prompt binding: "character1", "character2" (lowercase c, by array order) — NOT "Image1"
- Each reference clip must contain only ONE character (group video = identity merge failure)
- Max 2 video references (Wan 2.6 limit, vs 5 in Wan 2.7)
- Character drifts by shot 2 in multi-shot sequences (Wan 2.7 holds 3+ shots)

### Wan 2.7 R2V — Key Improvements (for when it lands on AIMLAPI)

**Key parameters (Together AI/fal.ai format; AIMLAPI format expected similar):**
```python
resp = httpx.post("https://api.aimlapi.com/v2/video/generations", json={
    "model": "alibaba/wan-2-7-r2v",   # Coming Soon on AIMLAPI as of 2026-07-17 — NOT live yet
    "prompt": "Image1 carries a box confidently toward the moving truck, golden hour, no ghost driving",
    "reference_images": [              # confirmed param name for AIMLAPI-compatible wrappers (pass 31)
        "https://cdn.example.com/crew_lead/front.png",
        "https://cdn.example.com/crew_lead/three_quarter.png",
        "https://cdn.example.com/crew_lead/face_crop.png",
    ],
    # Wan 2.7 supports up to 5 total (images + videos + audio); AIMLAPI adapter may differ
    "resolution": "720p",         # "720p" or "1080p"; use 720p for drafts
    "aspect_ratio": "9:16",
    "duration": 5,
    "shot_type": "single",        # "single" or "multi" (multi-shot storyboard) — confirm passthrough on AIMLAPI
    # DO NOT use generate_audio: False — Wan 2.7 uses different audio param (unconfirmed on AIMLAPI)
    # MANDATORY: strip audio in post via FFmpeg (see audio control section below)
}, headers=headers, timeout=120)
```

**Prompt binding syntax (Wan 2.7):** "image1" / "Image1", "image2" / "Image2", "video1" (no @ prefix). Each identifier maps to its position in the reference array. Official Segmind examples use capital "Image1" — treat binding as case-insensitive but prefer capitalized form ("Image1 walks toward the truck") to match published examples. "Image1 and Image2 carry boxes together" for 2 characters.

**Wan 2.7 R2V improvements over 2.6:**
- Supports STATIC IMAGE references (not video-only like 2.6) — "image1" binding directly from character photo
- Up to 5 references total (images + videos + audio), vs 2 video-only in 2.6
- Character consistency holds across 3+ shots; 2.6 drifts at shot 2
- Voice cloning via audio reference (1–10s WAV/MP3, 15MB max)
- No `face_weight` dial — identity lock is architectural; cannot tune face adherence per-call

**Critical limitations vs Kling O1:**
- **No Subject Binding weight parameter** — no face_adherence dial. Cannot increase face adherence on retry.
- Face consistency quality vs Kling O1 unverified for olive/brown-skin characters (Karel, Mourad). Run InsightFace QA.
- No `face_consistency: True` equivalent for occlusion recovery.
- Single subject per reference — group photos cause identity merge failure.

**Wan 2.7 R2V status on AIMLAPI (pass 43 recheck, 2026-08-23):** Status unchanged. Model ID `alibaba/wan-2-7-r2v` still no dedicated R2V docs page at docs.aimlapi.com (Wan 2.7 I2V docs page exists at `docs.aimlapi.com/api-references/video-models/alibaba-cloud/wan-2.7-image-to-video`; R2V page still absent). AIMLAPI blog post `aimlapi.com/blog/wan-2-7-video-next-generation-ai-video-generation-model` confirms Wan 2.7 coverage but R2V endpoint not confirmed live. Status: **"AIMLAPI blog-confirmed available but docs-absent — canary-test is mandatory before any production use"**. If canary call to `alibaba/wan-2-7-r2v` returns 404/model-not-found, fall back to Wan 2.6 R2V or Kling O1. All third-party providers (Segmind, Replicate, Together AI, Kie.ai, EvoLink, inference.sh, WaveSpeedAI) have Wan 2.7 R2V confirmed live. Canary-test procedure: call `alibaba/wan-2-7-r2v` with Karel `front.png` in `reference_images`, 720p, strip audio in post (API audio param still unconfirmed on AIMLAPI — use FFmpeg strip as mandatory safety step), score with InsightFace (PASS ≥ 0.62). Do NOT promote to production without owner-reviewed output passing brand binary checklist.

**Parameter naming (pass 31 finding, 2026-07-15):** Third-party wrappers (Segmind and equivalent AIMLAPI-style endpoints) use **`reference_images`** as the parameter name for static photo references — consistent with the code example above. The official upstream Alibaba API uses `images` instead. AIMLAPI adapter likely follows `reference_images` (matching Segmind convention). The code example above uses `reference_images` — this is the correct target for AIMLAPI canary testing.

**`shot_type` parameter (pass 31 finding):** `"single"` or `"multi"` — controls whether the model runs a single continuous generation or a multi-shot storyboard sequence. Documented across multiple wrappers. Add to canary call to confirm passthrough.

**Canary procedure:** Karel/Mourad `front.png` as `reference_images[0]`, 720p, audio explicitly muted (see below). Score with InsightFace buffalo_l (PASS threshold 0.62). If identity score ≥ 0.62 across 3 runs → eligible for draft-tier use at ~$0.625/5s. Only promote to production finals after owner-reviewed output passes brand binary checklist. If canary returns model-not-found → fall back to Wan 2.6 R2V or Kling O1.

**CRITICAL — Wan 2.7 R2V audio control (pass 29 finding, updated pass 33 2026-07-18):** Wan 2.7 R2V does **NOT** use a `generate_audio: false` boolean like Kling. Audio mode values confirmed across 5+ independent wrappers (Segmind, Kie.ai, EvoLink, Apiframe, inference.sh): **`"mute"`** (silence output), `"auto"` (model decides), `"keep_original"` / `"origin"` (preserve source audio). Use `"mute"` for all production clips. The AIMLAPI adapter parameter name for this mode is **unconfirmed** — no R2V docs page at docs.aimlapi.com as of 2026-07-18. Additionally: `reference_voice` accepts a 1–10s audio URL for voice cloning; omit entirely (do NOT set) to suppress voice generation. **Safety protocol — mandatory:** Always strip audio in post regardless of API parameter state:

```bash
ffmpeg -i wan_r2v_output.mp4 -an -c:v copy wan_r2v_muted.mp4
```

Add this FFmpeg strip as a non-negotiable post-step in any Wan 2.7 R2V generation script — do NOT rely on an unverified API parameter to silence audio. Generating haram music is a Shari'ah production gate failure. When R2V docs appear on AIMLAPI, test and document the audio param name, then update this entry.

## Kling Image O3 — Future Watch for Hero Frames (NOT on AIMLAPI as of 2026-06-27)

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

**ConsID-Gen — Research Validation (arXiv 2602.10113, CVPR 2026, code released):** View-Consistent and Identity-Preserving I2V generation. Code: github.com/eBay/ConsID-Gen. Curated dataset: ConsIDVid (Hugging Face: `mingyang-wu/ConsIDVid`). Core mechanism: augments the generation's first frame with **unposed auxiliary views** (multi-angle renders of the subject), then fuses semantic identity cues + geometric/structural cues via a dual-stream visual-geometric encoder and text-visual connector into a DiT backbone. Outperforms Wan2.1 and HunyuanVideo on identity fidelity and temporal coherence under real-world viewpoint variation. Accepted CVPR 2026 + associated VGBE 2026 challenge winner.

**Production implication for our pipeline (pass 31 finding, 2026-07-15):** ConsID-Gen confirms architecturally WHY our multi-angle reference strategy (front + 3/4 + profile + face crop) works: these angles are exactly the "unposed auxiliary views" that provide geometric + structural cues at varied viewpoints. The "dual-stream" (semantic ID + geometric structure) parallels our combination of texture-preserving references (full-body front) and structure-isolating references (tight face crop). No AIMLAPI endpoint — research only. Monitor for hosted API — if a ConsID-Gen-based I2V endpoint appears, it would excel at identity lock through camera moves (pan + zoom shots) where single-angle Kling O1 tends to drift.

**Stand-In — Future Watch (arXiv 2508.07901, August 2025, code released):** Lightweight plug-and-play identity control for video generation. Code: github.com/cainstudios/stand-in. Weights: HuggingFace `BowenXue/Stand-In`. Backbone: **Wan2.1-14B-T2V**. Key innovation: adds only **1% additional parameters** to the base model via a conditional image branch + restricted self-attention with conditional position mapping. VRAM follows Wan2.1-14B requirements (~40–50 GB FP8, ~70 GB BF16).

**Practical implications for our pipeline (pass 34 finding, 2026-07-20):**
1. **Validates differential prompt rule:** Stand-In's own inference guide recommends using generic descriptors ("a man", "a woman") rather than character-specific text — avoid re-describing attributes already shown in the reference image. Identical to our existing Step 3a policy.
2. **Limitation: frontal + medium-to-close-up videos only.** Stand-In does not reliably preserve identity in wide shots or strong profile angles. Our multi-angle ref strategy via Kling O1 handles this — Stand-In would only replace it if its hosted API targets close-up character shots.
3. **Face swapping listed as experimental** — not a replacement for FaceFusion fallback in production.
4. No AIMLAPI endpoint. When Wan2.1-based endpoints expand on AIMLAPI, Stand-In-style adapters may appear as options.

**WildActor — Future Watch (arXiv 2603.00586, March 2026, code released):** Full-body identity consistency across unconstrained viewpoints and motions. Code: github.com/WildActor/WildActor. Dataset: Actor-18M (1.6M videos, 18M human images). Benchmark: Actor-Bench.

Key mechanism: **Asymmetric Identity-Preserving Attention (AIPA)** — video tokens query identity cues from reference tokens, but reference tokens remain isolated from noisy backbone features. This unidirectional flow preserves identity fidelity while allowing free motion generation. Coupled with **Viewpoint-Adaptive Monte Carlo Sampling** for handling large viewpoint transitions.

**Practical implications for our pipeline (pass 34 finding, 2026-07-20):**
1. **Validates differential prompt rule architecturally:** AIPA's unidirectional design (identity flows reference→video only, not bidirectionally) is the architectural proof that text prompts should contain ONLY action+camera, not character attributes — attributes in the text compete with the unidirectional identity flow.
2. **Handles full-body viewpoint transitions** — WildActor is explicitly designed for the failure mode (large viewpoint transitions, substantial body motion) where Kling O1 elements binding tends to drift. When a WildActor-based API endpoint appears, prioritize testing for wide-shot and walking-away shots of Karel/Mourad.
3. **No AIMLAPI endpoint** as of 2026-07-20. Monitor for hosted API — backbone is not Wan2.1 (uses its own dataset/model), so AIMLAPI adoption timeline is uncertain.

**Vera — Future Watch (arXiv 2607.20247, July 22, 2026, Kuaishou Technology + Tsinghua):** Unified human-centric subject-to-video (S2V) framework for single- and multi-person generation. From the same company as Kling — mechanisms may inform future Kling O3+ updates. Core problem addressed: identity-critical human details drift across frames, poses, and interactions; in multi-person scenarios, **incorrect identity-role binding** leads to subject confusion, attribute swapping, and excessive reference-image copying. Two key mechanisms:
1. **Identity-Focal Masked Supervision (IFMS)** — spatially focused supervision strengthens identity-aware learning while reducing interference from irrelevant background/clothing artifacts. Validates our tight face crop as 4th ref (isolates identity signal from irrelevant scene content).
2. **Reference-Aware Layer-wise Attention (RALA)** — regulates how video tokens interact with reference identity cues in the DiT backbone at each layer, preserving stable identity anchors and enhancing layer-aware identity readout. Validates the differential prompt rule: identity is injected via references, text only drives action.

**Practical implication for our pipeline (pass 42 finding, 2026-08-21):** Vera's identity-role binding problem is exactly our known multi-character failure mode ("feature swapping when characters touch or overlap" — Step 3b). IFMS+RALA validate our two existing mitigations: (1) keep characters spatially separated in prompts, and (2) run InsightFace QA on BOTH characters after generation. Since Vera is from Kuaishou, its mechanisms may inform future Kling element-binding improvements. No AIMLAPI endpoint — research only.

**ID-V2V — Future Watch (arXiv 2607.22830, July 24, 2026, Netflix + Eyeline Labs, SIGGRAPH Asia 2026, code released):** Identity-preserving video restylization. Code: github.com/Eyeline-Labs/ID-V2V. ComfyUI nodes available (ComfyUI-wiki confirmed July 29, 2026). Core mechanism: decouples source-grounded identity preservation from edit-driven video synthesis. Given a source clip + a stylized keyframe (+ optional text), generates a new clip matching the keyframe's scene/lighting/style while preserving the source subjects' **facial identity, expressions, eye gaze, and lip sync**. "Shoot first, restyle later" workflow — generate the character clip first, then apply a cinematic style via a keyframe.

**Practical implication for our pipeline (pass 42 finding, 2026-08-21):** Potential post-production tool for consistent lighting grade across clips. When multiple Karel/Mourad clips need a unified golden-hour look, ID-V2V could apply the grade from a single keyframe across all clips without corrupting InsightFace identity scores (unlike per-clip color grading which can shift skin tone). **Prerequisite: clips must first pass InsightFace QA.** Apply ID-V2V as final grade step, then run QA again (facial expressions and identity should be invariant). Requires local ComfyUI install + Wan2.1-14B base weights (~40–50 GB VRAM). Not usable in cloud-API-only pipeline. Monitor for AIMLAPI endpoint — if it appears, could replace per-clip FFmpeg color grade for character shots.

## Shari'ah-Specific Character Rules
- Male crew: long trousers, covered 'awrah, modest work clothing
- Female family members (if depicted): full hijab, loose-fitting garments
- MUST specify exact clothing in prompts — MUST NOT leave it to the model's default
- MUST include clothing description in EVERY prompt, even if character appeared in a previous shot
- Reference images themselves MUST be Shari'ah compliant — MUST run QA on character sheets before using

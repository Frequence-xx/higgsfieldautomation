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
---

# Character Consistency System

## The Problem
AI models drift: a crew member's face, build, skin tone, and clothing change between shots. Without explicit anchoring, every generation treats characters as new.

## AIMLAPI Character Reference Models

| Stage | Model | Param | Max Refs | Use For |
|-------|-------|-------|----------|---------|
| Hero frame with character lock | `flux/kontext-max/image-to-image` | `image_url` (array) | 4 | Lock character identity across scenes |
| Compositing character into scene | `google/nano-banana-pro-edit` | `image_urls` (array) | **14** | Place character into any background |
| Character-consistent video | `klingai/video-o1-reference-to-video` | `elements` + `image_list` | 4 elements, 7 total | Video with locked character identity |
| High-quality character video | `google/veo-3.1-reference-to-video` | `image_urls` (array) | ~3+ | Premium character video |

## Step-by-Step Workflow

### Step 1: Create Character Reference Sheet
For each recurring character, generate 4 reference images using Nano Banana Pro.
Use 1:1 for reference sheets (consistency matching), 9:16 for final hero frames.

```python
# Generate 4 angles of the character via AIMLAPI
# Use 1:1 for reference sheets — these are for identity matching, not final output
for angle in ["front view", "3/4 angle from left", "profile from right side", "full body standing"]:
    resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
        "model": "google/nano-banana-pro",
        "prompt": f"A 37-year-old Dutch man with short dark brown hair, medium olive skin, clean shaven, wearing a navy blue polo shirt with company logo on left chest and dark grey cargo trousers with black work boots, {angle}, professional photography, neutral background",
        "aspect_ratio": "1:1",    # 1:1 for ref sheets
        "resolution": "1K",
    }, headers=headers, timeout=60)
```

Save to `/opt/pipeline/assets/characters/{name}/`:
```
/assets/characters/
├── crew_lead/
│   ├── front.png          # Generated via Nano Banana Pro
│   ├── three_quarter.png  # Generated via Nano Banana Pro
│   ├── profile.png        # Generated via Nano Banana Pro
│   ├── full_body.png      # Generated via Nano Banana Pro
│   └── character.json     # Metadata (see below)
```

### Step 2: Lock Character via Flux Kontext Max
Use Kontext Max to place the character into each scene while preserving identity.
**Always use `aspect_ratio: "9:16"` for vertical hero frames.**

```python
# Generate hero frame with character locked into the scene — NATIVE 9:16
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "flux/kontext-max/image-to-image",
    "prompt": "Place this person on a Dutch suburban street next to a white moving truck, golden hour lighting, cinematic vertical composition, 35mm lens",
    "image_url": [
        "https://cdn.example.com/characters/crew_lead/front.png",
        "https://cdn.example.com/characters/crew_lead/three_quarter.png"
    ],
    "aspect_ratio": "9:16",   # VERIFIED: produces native ~752x1392 vertical output
    "num_images": 1,
}, headers=headers, timeout=90)
# Response is SYNCHRONOUS — no polling needed
hero_frame_url = resp.json()["data"][0]["url"]
```

### Step 3: Animate with Character Reference (Kling O1)
For video clips where character must stay consistent:

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
# ASYNC — poll for completion
```

### Step 4: Alternative — Nano Banana Pro Edit for Compositing
For placing a character into a specific background scene (max 14 reference images).
**Always use `aspect_ratio: "9:16"` for vertical hero frames.**

```python
resp = httpx.post("https://api.aimlapi.com/v1/images/generations", json={
    "model": "google/nano-banana-pro-edit",
    "image_urls": [
        "https://cdn.example.com/characters/crew_lead/front.png",
        "https://cdn.example.com/characters/crew_lead/full_body.png",
        "https://cdn.example.com/scenes/dutch_street_golden_hour.png"
    ],
    "prompt": "Place the person from the first two images into the street scene from the third image, maintaining their exact appearance and clothing, cinematic vertical composition",
    "aspect_ratio": "9:16",   # Native 9:16 output — no cropping needed
    "resolution": "1K",       # Options: 1K (768x1344), 2K (1536x2688), 4K (3072x5376)
}, headers=headers, timeout=60)
```

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
After generating a multi-shot sequence, compare:
- Face geometry: same jaw shape, nose, eye spacing
- Skin tone: no shifts between shots
- Clothing: same items, same colors, same fit
- Build/proportions: no height or weight changes

Score character consistency 1-10. Below 7 = reject and regenerate with stronger reference anchoring.

## Model Selection for Character Shots

| Scenario | Image Model | Video Model | Cost Est. |
|----------|-------------|-------------|-----------|
| Character alone (portrait/action) | Kontext Max (4 refs) | Kling O1 Reference (4 elements) | ~$0.05 + $0.84/5s |
| Character in specific scene | Nano Banana Pro Edit (14 refs) | Kling v3 Standard I2V | ~$0.05 + $0.42/5s |
| Multiple characters in one shot | Nano Banana Pro Edit (14 refs) | Kling O1 Reference (4 elements) | ~$0.05 + $0.84/5s |
| Character consistency is not critical | Nano Banana Pro (text-only) | Kling v3 Standard I2V | ~$0.05 + $0.42/5s |

## Shari'ah-Specific Character Rules
- Male crew: long trousers, covered 'awrah, modest work clothing
- Female family members (if depicted): full hijab, loose-fitting garments
- Always specify exact clothing in prompts — never leave it to the model's default
- Include clothing description in EVERY prompt, even if the character appeared in a previous shot
- Reference images themselves must be Shari'ah compliant — run QA on character sheets before using

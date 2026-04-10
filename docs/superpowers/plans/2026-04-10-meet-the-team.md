# "Meet the Team" Video Ad — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a 15-second 9:16 vertical video ad introducing the Snelverhuizen team (Mourad & Karel) with Willem voiceover, ambient SFX, and animated captions.

**Architecture:** AIMLAPI-first pipeline. Generate hero frames (Nano Banana Pro / Flux Kontext Max), QA each still, animate via Kling v3 Standard I2V, generate voiceover via ElevenLabs, add ambient SFX from Freesound, assemble with FFmpeg, add captions via Remotion, deliver via Telegram.

**Tech Stack:** AIMLAPI REST API (Python httpx), ElevenLabs API, Freesound API, FFmpeg, Remotion (React/TypeScript), SQLite, Telegram MCP

---

## Pre-flight

### Task 0: Environment Check & Brief Registration

**Files:**
- Read: `/opt/pipeline/.env` (API keys)
- Read: `/opt/pipeline/data/pipeline.db` (SQLite)

- [ ] **Step 1: Check disk space**

Run: `df -h /`
Expected: >20GB free (currently 356GB free — OK)

- [ ] **Step 2: Verify AIMLAPI key is set**

```bash
source /opt/pipeline/.env && echo "AIMLAPI key length: ${#AIMLAPI_API_KEY}"
```
Expected: Non-zero length

- [ ] **Step 3: Verify ElevenLabs key is set**

```bash
source /opt/pipeline/.env && echo "ElevenLabs key length: ${#ELEVENLABS_API_KEY}"
```
Expected: Non-zero length

- [ ] **Step 4: Register brief in SQLite**

```bash
sqlite3 /opt/pipeline/data/pipeline.db "INSERT INTO briefs (concept_text, shot_list_json, shariah_validated, status, current_step, created_at, updated_at) VALUES ('Maak kennis met het team achter Snelverhuizen — korte, warme kennismaking met Mourad en Karel bij de bus', '{\"shots\": 5, \"duration\": 15, \"format\": \"9:16\", \"spec\": \"docs/superpowers/specs/2026-04-10-meet-the-team-design.md\"}', 1, 'generating', 'shot_1_hero_frame', datetime('now'), datetime('now'));"
```

- [ ] **Step 5: Get the brief ID**

```bash
sqlite3 /opt/pipeline/data/pipeline.db "SELECT id FROM briefs ORDER BY id DESC LIMIT 1;"
```
Store as `$BRIEF_ID` for all subsequent tasks.

- [ ] **Step 6: Create output directories**

```bash
mkdir -p /opt/pipeline/output/meet-the-team/{hero_frames,videos,audio,qa_frames,final}
```

- [ ] **Step 7: Send Telegram update — generation starting**

Use Telegram MCP reply: "Shotlijst goedgekeurd. Ik begin nu met genereren. Shot 1/5: Truck establishing shot..."

---

## Phase 1: Hero Frame Generation & QA

### Task 1: Shot 1 — Truck Establishing Hero Frame

**Files:**
- Reference: `/opt/pipeline/assets/truck/truck_rightdiagnol_side_view.png`
- Reference: `/opt/pipeline/assets/color_ref_1.png`
- Output: `/opt/pipeline/output/meet-the-team/hero_frames/shot1_truck.png`

- [ ] **Step 1: Generate hero frame via AIMLAPI Nano Banana Pro**

```python
import httpx, os, base64, json

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

resp = httpx.post("https://api.aimlapi.com/v2/generate/image/google/generation", json={
    "model": "google/nano-banana-pro",
    "prompt": "White Mercedes Sprinter box truck with orange SNELVERHUIZEN branding band across lower half, parked on a quiet Dutch suburban street with brick houses and trees, golden hour warm light, cinematic color grading, slightly desaturated, lifted blacks, amber highlights, cool blue shadows, film grain, professional commercial look, shot on RED camera, 9:16 vertical composition, wide establishing shot, slight low angle, natural wear on truck, realistic fabric wrinkles on tarp, practical on-set lighting, subtle asymmetry",
    "aspect_ratio": "9:16",
}, headers=headers, timeout=60)

result = resp.json()
print(json.dumps(result, indent=2))
```

- [ ] **Step 2: Download and save the hero frame**

Download the image URL from the response to `/opt/pipeline/output/meet-the-team/hero_frames/shot1_truck.png`

- [ ] **Step 3: Visual QA on hero frame**

Read the saved image with the Read tool. Score on 8 dimensions:
1. hand_anatomy (N/A — no hands)
2. face_consistency_vs_reference (N/A — no faces)
3. physics_plausibility (truck, street, lighting)
4. brand_accuracy (orange band, SNELVERHUIZEN text, logo)
5. lighting_coherence (golden hour, consistent shadows)
6. ai_artifact_severity (textures, edges, text garbling)
7. shariah_compliance (must be 10/10 — no haram elements)
8. overall_realism (would pass as real footage)

Pass threshold: ALL applicable dimensions >= 7, shariah_compliance = 10.
If FAIL: adjust prompt, regenerate (max 3 attempts). Log to generation_history.

- [ ] **Step 4: Log generation to SQLite**

```bash
sqlite3 /opt/pipeline/data/pipeline.db "INSERT INTO generation_history (brief_id, shot_number, prompt, model, settings_json, qa_scores_json, pass_fail, retry_count, generation_method, created_at) VALUES ($BRIEF_ID, 1, '<prompt used>', 'google/nano-banana-pro', '{\"aspect_ratio\": \"9:16\"}', '<QA scores JSON>', 'pass', 0, 'api', datetime('now'));"
```

- [ ] **Step 5: Update brief current_step**

```bash
sqlite3 /opt/pipeline/data/pipeline.db "UPDATE briefs SET current_step = 'shot_2_hero_frame', updated_at = datetime('now') WHERE id = $BRIEF_ID;"
```

---

### Task 2: Shot 2 — Mourad Portrait Hero Frame

**Files:**
- Reference: `/opt/pipeline/assets/crew/mourad_reference_sheet.png`
- Reference: `/opt/pipeline/assets/crew/mourad_full_body.png`
- Output: `/opt/pipeline/output/meet-the-team/hero_frames/shot2_mourad.png`

- [ ] **Step 1: Generate hero frame via AIMLAPI with character reference**

For Mourad's portrait, use Flux Kontext Max or Nano Banana Pro with strong character description anchored to reference:

```python
import httpx, os, json

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

resp = httpx.post("https://api.aimlapi.com/v2/generate/image/google/generation", json={
    "model": "google/nano-banana-pro",
    "prompt": "Professional portrait of a bald clean-shaven man with medium olive skin tone, medium build, wearing a black crewneck sweatshirt with small orange SNELVERHUIZEN logo on left chest and blue jeans, standing next to a white Mercedes Sprinter truck with orange branding, half-body shot looking at camera with a slight warm smile, 85mm portrait lens, shallow depth of field, beautiful golden hour backlight, cinematic bokeh, warm amber highlights, cool blue shadows, film grain, professional commercial photography, 9:16 vertical composition, natural skin texture, realistic fabric wrinkles on sweatshirt, practical on-set lighting, subtle asymmetry",
    "aspect_ratio": "9:16",
}, headers=headers, timeout=60)

result = resp.json()
print(json.dumps(result, indent=2))
```

- [ ] **Step 2: Download and save the hero frame**

Download to `/opt/pipeline/output/meet-the-team/hero_frames/shot2_mourad.png`

- [ ] **Step 3: Visual QA — compare face to reference**

Read both the generated image and `/opt/pipeline/assets/crew/mourad_reference_sheet.png`.
Score all 8 dimensions. Pay special attention to:
- face_consistency_vs_reference: Must match Mourad's features (bald, olive skin, clean-shaven)
- brand_accuracy: Orange logo on black crewneck
- shariah_compliance: Modest dress (10/10 required)

If FAIL on face: adjust prompt with stronger character descriptors, regenerate (max 3 attempts).

- [ ] **Step 4: Log generation to SQLite**

```bash
sqlite3 /opt/pipeline/data/pipeline.db "INSERT INTO generation_history (brief_id, shot_number, prompt, model, settings_json, qa_scores_json, pass_fail, retry_count, generation_method, created_at) VALUES ($BRIEF_ID, 2, '<prompt used>', 'google/nano-banana-pro', '{\"aspect_ratio\": \"9:16\"}', '<QA scores JSON>', 'pass', 0, 'api', datetime('now'));"
```

- [ ] **Step 5: Update brief current_step**

```bash
sqlite3 /opt/pipeline/data/pipeline.db "UPDATE briefs SET current_step = 'shot_3_hero_frame', updated_at = datetime('now') WHERE id = $BRIEF_ID;"
```

---

### Task 3: Shot 3 — Karel Portrait Hero Frame

**Files:**
- Reference: `/opt/pipeline/assets/crew/karel_character_sheet.png`
- Reference: `/opt/pipeline/assets/crew/karel_full_body_outside_with_box.png`
- Output: `/opt/pipeline/output/meet-the-team/hero_frames/shot3_karel.png`

- [ ] **Step 1: Generate hero frame via AIMLAPI**

```python
import httpx, os, json

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

resp = httpx.post("https://api.aimlapi.com/v2/generate/image/google/generation", json={
    "model": "google/nano-banana-pro",
    "prompt": "Professional portrait of a large stocky bald man with light beard and fair skin, wearing a black crewneck sweatshirt with small orange SNELVERHUIZEN logo on left chest and blue jeans with white sneakers, standing at the hydraulic liftgate of a white Mercedes Sprinter truck, holding a cardboard moving box with handle cutouts, half-body shot looking at camera with a warm friendly smile, 85mm portrait lens, shallow depth of field, golden hour backlight, cinematic bokeh, warm amber highlights, cool blue shadows, film grain, professional commercial photography, 9:16 vertical composition, natural skin texture, realistic fabric wrinkles, practical on-set lighting, subtle asymmetry",
    "aspect_ratio": "9:16",
}, headers=headers, timeout=60)

result = resp.json()
print(json.dumps(result, indent=2))
```

- [ ] **Step 2: Download and save the hero frame**

Download to `/opt/pipeline/output/meet-the-team/hero_frames/shot3_karel.png`

- [ ] **Step 3: Visual QA — compare face to reference**

Read both the generated image and `/opt/pipeline/assets/crew/karel_character_sheet.png`.
Score all 8 dimensions. Pay special attention to:
- face_consistency_vs_reference: Must match Karel's features (large build, bald, light beard, fair skin)
- hand_anatomy: Holding box — check finger count and grip
- brand_accuracy: Orange logo on black crewneck, correct box design
- shariah_compliance: 10/10 required

If FAIL: adjust prompt, regenerate (max 3 attempts).

- [ ] **Step 4: Log generation to SQLite**

```bash
sqlite3 /opt/pipeline/data/pipeline.db "INSERT INTO generation_history (brief_id, shot_number, prompt, model, settings_json, qa_scores_json, pass_fail, retry_count, generation_method, created_at) VALUES ($BRIEF_ID, 3, '<prompt used>', 'google/nano-banana-pro', '{\"aspect_ratio\": \"9:16\"}', '<QA scores JSON>', 'pass', 0, 'api', datetime('now'));"
```

- [ ] **Step 5: Update brief current_step**

```bash
sqlite3 /opt/pipeline/data/pipeline.db "UPDATE briefs SET current_step = 'shot_4_hero_frame', updated_at = datetime('now') WHERE id = $BRIEF_ID;"
```

---

### Task 4: Shot 4 — Team Together Hero Frame

**Files:**
- Reference: `/opt/pipeline/assets/crew/mourad_and_karel_together.png`
- Reference: `/opt/pipeline/assets/truck/truck_right_side_view.png`
- Output: `/opt/pipeline/output/meet-the-team/hero_frames/shot4_team.png`

- [ ] **Step 1: Generate hero frame via AIMLAPI**

```python
import httpx, os, json

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

resp = httpx.post("https://api.aimlapi.com/v2/generate/image/google/generation", json={
    "model": "google/nano-banana-pro",
    "prompt": "Two professional movers standing side by side next to a white Mercedes Sprinter box truck with orange SNELVERHUIZEN branding. Left man: bald clean-shaven medium olive skin medium build. Right man: large stocky bald light beard fair skin. Both wearing black crewneck sweatshirts with small orange SNELVERHUIZEN logo on left chest and blue jeans. Confident professional posture, arms at their sides, warm expressions. Medium wide shot, 35mm lens, both fully in frame, golden hour warm light, quiet Dutch suburban street background, cinematic color grading, warm amber highlights, cool blue shadows, film grain, professional commercial photography, 9:16 vertical composition, practical on-set lighting, subtle asymmetry, natural wear",
    "aspect_ratio": "9:16",
}, headers=headers, timeout=60)

result = resp.json()
print(json.dumps(result, indent=2))
```

- [ ] **Step 2: Download and save the hero frame**

Download to `/opt/pipeline/output/meet-the-team/hero_frames/shot4_team.png`

- [ ] **Step 3: Visual QA — compare both characters to references**

Read the generated image and compare to `/opt/pipeline/assets/crew/mourad_and_karel_together.png`.
Score all 8 dimensions. Critical checks:
- face_consistency_vs_reference: Both must be recognizable (Mourad left, Karel right)
- brand_accuracy: Both wearing correct uniform, truck branding visible
- shariah_compliance: 10/10 required

If FAIL: This is the hardest shot (2 characters). Try up to 3 times. If all fail, escalate to owner via Telegram with frames and failure codes.

- [ ] **Step 4: Log generation to SQLite**

Same pattern as previous tasks.

- [ ] **Step 5: Update brief current_step**

```bash
sqlite3 /opt/pipeline/data/pipeline.db "UPDATE briefs SET current_step = 'video_animation', updated_at = datetime('now') WHERE id = $BRIEF_ID;"
```

- [ ] **Step 6: Send Telegram update — hero frames complete**

Use Telegram MCP reply: "Alle 4 hero frames zijn gegenereerd en door QA gekomen. Ik ga nu de video-animaties starten..."

Send all 4 hero frames as attachments for owner review.

---

## Phase 2: Video Animation

### Task 5: Animate Shot 1 — Truck Establishing

**Files:**
- Input: `/opt/pipeline/output/meet-the-team/hero_frames/shot1_truck.png`
- Output: `/opt/pipeline/output/meet-the-team/videos/shot1_truck.mp4`

- [ ] **Step 1: Upload hero frame and get CDN URL**

If AIMLAPI requires a URL (not base64), first upload the hero frame to a temporary hosting or use a data URL. Check the API docs — if `image_url` accepts base64, encode the image:

```python
import base64
with open("/opt/pipeline/output/meet-the-team/hero_frames/shot1_truck.png", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()
image_url = f"data:image/png;base64,{image_b64}"
```

- [ ] **Step 2: Submit Kling v3 Standard I2V animation**

```python
import httpx, os, json

API_KEY = os.environ['AIMLAPI_API_KEY']
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

resp = httpx.post("https://api.aimlapi.com/v2/generate/video/kling/generation", json={
    "model": "kling-video/v3/standard/image-to-video",
    "image_url": image_url,
    "prompt": "Slow gentle camera push-in toward the truck, leaves rustling in golden hour breeze, subtle light flares, cinematic movement, steady smooth dolly shot",
    "duration": "5",
    "aspect_ratio": "9:16"
}, headers=headers, timeout=60)

task_id = resp.json()["id"]
print(f"Task ID: {task_id}")
```

- [ ] **Step 3: Poll for completion (every 10s, max 5 min)**

```python
import time
for i in range(30):
    time.sleep(10)
    sr = httpx.get("https://api.aimlapi.com/v2/generate/video/kling/generation",
                   params={"generation_id": task_id}, headers=headers, timeout=30)
    status = sr.json().get("status")
    print(f"Poll {i+1}: {status}")
    if status == "completed":
        video_url = sr.json()["video"]["url"]
        print(f"Video URL: {video_url}")
        break
    elif status == "failed":
        print("GENERATION FAILED")
        print(json.dumps(sr.json(), indent=2))
        break
```

- [ ] **Step 4: Download video**

```python
video_resp = httpx.get(video_url, timeout=120)
with open("/opt/pipeline/output/meet-the-team/videos/shot1_truck.mp4", "wb") as f:
    f.write(video_resp.content)
```

- [ ] **Step 5: QA the video clip**

Extract frames: `ffmpeg -i /opt/pipeline/output/meet-the-team/videos/shot1_truck.mp4 -vf "select=not(mod(n\,4))" -vsync vfr /opt/pipeline/output/meet-the-team/qa_frames/shot1_%03d.png`

Read a sample of extracted frames. Score on 8 dimensions + cinematic quality (temporal coherence, camera movement smoothness). Pass threshold: all >= 7, shariah = 10.

- [ ] **Step 6: Log to SQLite and clean up QA frames (if passed)**

```bash
# After QA pass, delete QA frames
rm /opt/pipeline/output/meet-the-team/qa_frames/shot1_*.png
```

---

### Task 6: Animate Shot 2 — Mourad Portrait

**Files:**
- Input: `/opt/pipeline/output/meet-the-team/hero_frames/shot2_mourad.png`
- Output: `/opt/pipeline/output/meet-the-team/videos/shot2_mourad.mp4`

- [ ] **Step 1: Submit Kling v3 Standard I2V animation**

Same pattern as Task 5. Prompt:

```
"Man standing next to truck turns head slightly toward camera, subtle warm smile, shallow depth of field bokeh shifts gently, golden hour light plays on face, very subtle natural movement, cinematic portrait, minimal motion"
```

- [ ] **Step 2: Poll for completion (every 10s, max 5 min)**

Same polling pattern as Task 5.

- [ ] **Step 3: Download video**

Save to `/opt/pipeline/output/meet-the-team/videos/shot2_mourad.mp4`

- [ ] **Step 4: QA the video clip**

Extract frames, score. Pay attention to face consistency across frames (temporal coherence of facial features). If face drifts mid-clip, FAIL.

- [ ] **Step 5: Log to SQLite, clean QA frames**

---

### Task 7: Animate Shot 3 — Karel Portrait

**Files:**
- Input: `/opt/pipeline/output/meet-the-team/hero_frames/shot3_karel.png`
- Output: `/opt/pipeline/output/meet-the-team/videos/shot3_karel.mp4`

- [ ] **Step 1: Submit Kling v3 Standard I2V animation**

Prompt:

```
"Large man holding moving box shifts weight slightly, warm friendly smile, subtle natural breathing movement, golden hour light, cinematic portrait, shallow depth of field, minimal motion, steady composition"
```

- [ ] **Step 2: Poll for completion**

Same pattern.

- [ ] **Step 3: Download video**

Save to `/opt/pipeline/output/meet-the-team/videos/shot3_karel.mp4`

- [ ] **Step 4: QA the video clip**

Critical: hand_anatomy while holding box, face consistency, temporal coherence.

- [ ] **Step 5: Log to SQLite, clean QA frames**

---

### Task 8: Animate Shot 4 — Team Together

**Files:**
- Input: `/opt/pipeline/output/meet-the-team/hero_frames/shot4_team.png`
- Output: `/opt/pipeline/output/meet-the-team/videos/shot4_team.mp4`

- [ ] **Step 1: Submit Kling v3 Standard I2V animation**

Prompt:

```
"Two men standing confidently next to truck, very subtle natural movement, slight breeze, golden hour light shifts gently, cinematic medium wide shot, steady camera, professional commercial feel, minimal motion"
```

- [ ] **Step 2: Poll for completion**

Same pattern.

- [ ] **Step 3: Download video**

Save to `/opt/pipeline/output/meet-the-team/videos/shot4_team.mp4`

- [ ] **Step 4: QA the video clip**

Critical: Both faces must remain consistent, no morphing between characters. Check temporal coherence across all frames.

- [ ] **Step 5: Log to SQLite, clean QA frames**

- [ ] **Step 6: Update brief status and send Telegram update**

```bash
sqlite3 /opt/pipeline/data/pipeline.db "UPDATE briefs SET current_step = 'voiceover', status = 'post_production', updated_at = datetime('now') WHERE id = $BRIEF_ID;"
```

Telegram: "Alle 4 video clips zijn geanimeerd en door QA. Nu voiceover en audio..."

---

## Phase 3: Audio Production

### Task 9: Generate Voiceover via ElevenLabs

**Files:**
- Output audio: `/opt/pipeline/output/meet-the-team/audio/voiceover.mp3`
- Output timestamps: `/opt/pipeline/output/meet-the-team/audio/voiceover_timestamps.json`

- [ ] **Step 1: Generate voiceover with word-level timestamps**

Use ElevenLabs MCP `text_to_speech` tool:
- Voice ID: `yBtEjlHaWNu9xrYohjbA` (Willem)
- Model: `eleven_multilingual_v2`
- Text: `"Dit is het team achter Snelverhuizen. Mourad en Karel. Uw verhuizing is bij ons in goede handen."`
- Settings: stability 0.55, similarity_boost 0.75, style 0.35

If MCP tool supports `output_format` with timestamps, request word-level alignment data.

- [ ] **Step 2: Save audio file**

Save the generated audio to `/opt/pipeline/output/meet-the-team/audio/voiceover.mp3`

- [ ] **Step 3: Get voiceover duration**

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /opt/pipeline/output/meet-the-team/audio/voiceover.mp3
```

Verify it's approximately 5-7 seconds (fits within 15s video).

- [ ] **Step 4: Extract word-level timestamps**

If ElevenLabs returned timestamps, save to `/opt/pipeline/output/meet-the-team/audio/voiceover_timestamps.json`.

If not, use the `speech_to_text` MCP tool on the generated audio to get word timestamps, or manually estimate based on duration:

```json
[
  {"text": "Dit", "start": 0.0, "end": 0.3},
  {"text": "is", "start": 0.3, "end": 0.5},
  {"text": "het", "start": 0.5, "end": 0.7},
  {"text": "team", "start": 0.7, "end": 1.0},
  {"text": "achter", "start": 1.0, "end": 1.4},
  {"text": "Snelverhuizen.", "start": 1.4, "end": 2.2},
  {"text": "Mourad", "start": 2.5, "end": 3.0},
  {"text": "en", "start": 3.0, "end": 3.2},
  {"text": "Karel.", "start": 3.2, "end": 3.8},
  {"text": "Uw", "start": 4.1, "end": 4.3},
  {"text": "verhuizing", "start": 4.3, "end": 4.9},
  {"text": "is", "start": 4.9, "end": 5.1},
  {"text": "bij", "start": 5.1, "end": 5.3},
  {"text": "ons", "start": 5.3, "end": 5.5},
  {"text": "in", "start": 5.5, "end": 5.7},
  {"text": "goede", "start": 5.7, "end": 6.0},
  {"text": "handen.", "start": 6.0, "end": 6.5}
]
```

These will be refined after actual generation.

---

### Task 10: Download Ambient SFX from Freesound

**Files:**
- Output: `/opt/pipeline/output/meet-the-team/audio/ambient_sfx.mp3`

- [ ] **Step 1: Search Freesound for quiet street ambiance**

```bash
source /opt/pipeline/.env && curl -s "https://freesound.org/apiv2/search/text/?query=quiet+dutch+street+ambiance+birds&filter=duration:[10 TO 30]&fields=id,name,previews,license,duration&token=$FREESOUND_API_KEY" | python3 -m json.tool | head -40
```

Look for a CC-licensed clip of ~15-20 seconds with: birds, light wind, quiet residential street.

- [ ] **Step 2: Download the best matching clip**

```bash
source /opt/pipeline/.env && curl -L -o /opt/pipeline/output/meet-the-team/audio/ambient_sfx_raw.mp3 "<preview_url>"
```

- [ ] **Step 3: Trim and normalize the ambient SFX**

```bash
ffmpeg -i /opt/pipeline/output/meet-the-team/audio/ambient_sfx_raw.mp3 -t 15 -af "afade=in:st=0:d=1,afade=out:st=13:d=2,volume=0.3" /opt/pipeline/output/meet-the-team/audio/ambient_sfx.mp3
```

This trims to 15s, fades in over 1s, fades out over last 2s, and reduces volume to 30% (background level).

---

## Phase 4: Assembly

### Task 11: FFmpeg Video Assembly

**Files:**
- Input: 4 video clips in `/opt/pipeline/output/meet-the-team/videos/`
- Input: `/opt/pipeline/output/meet-the-team/audio/voiceover.mp3`
- Input: `/opt/pipeline/output/meet-the-team/audio/ambient_sfx.mp3`
- Input: `/opt/pipeline/assets/logo-snelverhuizen.png`
- Output: `/opt/pipeline/output/meet-the-team/final/meet_the_team_raw.mp4`

- [ ] **Step 1: Verify all input clips exist and get durations**

```bash
for f in /opt/pipeline/output/meet-the-team/videos/shot{1,2,3,4}_*.mp4; do
  echo "$f: $(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f")s"
done
echo "voiceover: $(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /opt/pipeline/output/meet-the-team/audio/voiceover.mp3)s"
```

- [ ] **Step 2: Create Shot 5 logo card (3 seconds) via FFmpeg**

```bash
ffmpeg -loop 1 -i /opt/pipeline/assets/logo-snelverhuizen.png -f lavfi -i color=c=black:s=1080x1920:d=3 -filter_complex "[1:v][0:v]overlay=(W-w)/2:(H-h)/2:enable='between(t,0,3)',drawtext=text='snelverhuizen.nl':fontfile=/usr/share/fonts/truetype/montserrat/Montserrat-Black.ttf:fontsize=36:fontcolor=white:x=(w-text_w)/2:y=(h/2)+200:enable='between(t,0.5,3)'" -t 3 -r 30 -pix_fmt yuv420p /opt/pipeline/output/meet-the-team/videos/shot5_logo.mp4
```

- [ ] **Step 3: Normalize all clips to same format**

```bash
for i in 1 2 3 4; do
  ffmpeg -i /opt/pipeline/output/meet-the-team/videos/shot${i}_*.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30" -c:v libx264 -preset medium -crf 18 -an -pix_fmt yuv420p /opt/pipeline/output/meet-the-team/videos/shot${i}_norm.mp4
done
```

- [ ] **Step 4: Trim each clip to target duration**

Based on the 15s budget:
- Shot 1 (truck): 3s
- Shot 2 (Mourad): 3s
- Shot 3 (Karel): 3s
- Shot 4 (team): 3s
- Shot 5 (logo): 3s

```bash
ffmpeg -i /opt/pipeline/output/meet-the-team/videos/shot1_norm.mp4 -t 3 -c copy /opt/pipeline/output/meet-the-team/videos/shot1_trim.mp4
ffmpeg -i /opt/pipeline/output/meet-the-team/videos/shot2_norm.mp4 -t 3 -c copy /opt/pipeline/output/meet-the-team/videos/shot2_trim.mp4
ffmpeg -i /opt/pipeline/output/meet-the-team/videos/shot3_norm.mp4 -t 3 -c copy /opt/pipeline/output/meet-the-team/videos/shot3_trim.mp4
ffmpeg -i /opt/pipeline/output/meet-the-team/videos/shot4_norm.mp4 -t 3 -c copy /opt/pipeline/output/meet-the-team/videos/shot4_trim.mp4
```

- [ ] **Step 5: Create concat list and join all clips**

```bash
cat > /opt/pipeline/output/meet-the-team/videos/concat.txt << 'EOF'
file 'shot1_trim.mp4'
file 'shot2_trim.mp4'
file 'shot3_trim.mp4'
file 'shot4_trim.mp4'
file 'shot5_logo.mp4'
EOF

ffmpeg -f concat -safe 0 -i /opt/pipeline/output/meet-the-team/videos/concat.txt -c copy /opt/pipeline/output/meet-the-team/final/video_only.mp4
```

- [ ] **Step 6: Mix voiceover + ambient SFX and add to video**

```bash
ffmpeg -i /opt/pipeline/output/meet-the-team/final/video_only.mp4 \
  -i /opt/pipeline/output/meet-the-team/audio/voiceover.mp3 \
  -i /opt/pipeline/output/meet-the-team/audio/ambient_sfx.mp3 \
  -filter_complex "[1:a]adelay=500|500,volume=1.0[vo];[2:a]volume=0.25[sfx];[vo][sfx]amix=inputs=2:duration=longest[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest \
  /opt/pipeline/output/meet-the-team/final/meet_the_team_raw.mp4
```

The voiceover starts 0.5s in (after the first frame of the truck establishes), ambient SFX at 25% volume.

- [ ] **Step 7: Verify the assembled video**

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /opt/pipeline/output/meet-the-team/final/meet_the_team_raw.mp4
```

Expected: ~15 seconds.

---

### Task 12: Add Animated Captions via Remotion

**Files:**
- Modify: `/opt/pipeline/captions/src/Root.tsx`
- Modify: `/opt/pipeline/captions/src/CaptionComposition.tsx`
- Input: `/opt/pipeline/output/meet-the-team/audio/voiceover_timestamps.json`
- Output: Transparent caption overlay video

- [ ] **Step 1: Convert word timestamps to frame numbers**

At 30fps, convert each word's start/end seconds to frame numbers:

```python
import json

with open("/opt/pipeline/output/meet-the-team/audio/voiceover_timestamps.json") as f:
    words = json.load(f)

fps = 30
# Voiceover starts at 0.5s in the final video (500ms delay)
vo_offset = 0.5

remotion_words = []
for w in words:
    remotion_words.append({
        "text": w["text"],
        "startFrame": round((w["start"] + vo_offset) * fps),
        "endFrame": round((w["end"] + vo_offset) * fps)
    })

print(json.dumps(remotion_words, indent=2))
```

Save this output — it will be used as props for the Remotion composition.

- [ ] **Step 2: Update Root.tsx with meet-the-team composition**

Add a new `<Composition>` to `/opt/pipeline/captions/src/Root.tsx` with:
- id: `MeetTheTeamCaptions`
- width: 1080, height: 1920 (9:16)
- durationInFrames: 450 (15s × 30fps)
- fps: 30
- words: the converted word array from step 1
- style: Montserrat Black, ALL CAPS, white, gold highlight, center position at 60% height
- platformFormat: '9:16'

Update the style to use Montserrat Black per brand specs:
```typescript
const meetTheTeamStyle = {
    fontFamily: 'Montserrat, sans-serif',
    fontSize: 56,
    color: '#FFFFFF',
    highlightColor: '#FFD700',
    position: 'center' as const,
    animation: 'spring' as const,
};
```

- [ ] **Step 3: Add name card overlays for Mourad and Karel**

The name cards "MOURAD" (shot 2, ~3-6s = frames 90-180) and "KAREL" (shot 3, ~6-9s = frames 180-270) need to be separate text elements, not part of voiceover captions. Add these as additional elements in the CaptionComposition or create a wrapper composition that layers captions + name cards.

- [ ] **Step 4: Render caption overlay to transparent video**

```bash
cd /opt/pipeline/captions && npx remotion render MeetTheTeamCaptions --codec=vp9 --image-format=png --pixel-format=yuva420p /opt/pipeline/output/meet-the-team/final/captions_overlay.webm
```

This renders captions with transparency.

- [ ] **Step 5: Composite captions onto the assembled video**

```bash
ffmpeg -i /opt/pipeline/output/meet-the-team/final/meet_the_team_raw.mp4 \
  -i /opt/pipeline/output/meet-the-team/final/captions_overlay.webm \
  -filter_complex "[0:v][1:v]overlay=0:0:shortest=1" \
  -map 0:a -c:a copy -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  /opt/pipeline/output/meet-the-team/final/meet_the_team_captioned.mp4
```

---

## Phase 5: Final QA & Delivery

### Task 13: Final Brand Compliance Check

**Files:**
- Input: `/opt/pipeline/output/meet-the-team/final/meet_the_team_captioned.mp4`

- [ ] **Step 1: Extract sample frames from final video**

```bash
ffmpeg -i /opt/pipeline/output/meet-the-team/final/meet_the_team_captioned.mp4 -vf "select=not(mod(n\,30))" -vsync vfr /opt/pipeline/output/meet-the-team/qa_frames/final_%03d.png
```

This extracts one frame per second (every 30th frame at 30fps).

- [ ] **Step 2: Review each sampled frame**

Read each extracted frame. Check:
- Brand accuracy: Logo visible in closing, truck branding correct, uniforms correct
- Caption readability: Text visible, within safe zones, not overlapping faces
- Color grading: Warm cinematic look consistent across shots
- Shari'ah compliance: Final 10/10 check on all frames
- Transition quality: Clean cuts between shots

- [ ] **Step 3: Listen check on audio**

Play or analyze the audio track:
```bash
ffprobe -v error -show_entries stream=codec_type,codec_name,duration,sample_rate -of default /opt/pipeline/output/meet-the-team/final/meet_the_team_captioned.mp4
```

Verify: voiceover audible, ambient SFX present but subtle, NO music.

- [ ] **Step 4: Clean up QA frames**

```bash
rm /opt/pipeline/output/meet-the-team/qa_frames/final_*.png
```

- [ ] **Step 5: Update brief status**

```bash
sqlite3 /opt/pipeline/data/pipeline.db "UPDATE briefs SET status = 'complete', current_step = 'delivery', updated_at = datetime('now') WHERE id = $BRIEF_ID;"
```

---

### Task 14: Deliver via Telegram

- [ ] **Step 1: Send final video to owner**

Use Telegram MCP reply with file attachment:
- chat_id: owner's chat
- text: "Hier is de video: 'Maak kennis met het team achter Snelverhuizen' — 15 seconden, 9:16 verticaal. Bekijk en laat weten of je tevreden bent!"
- files: ["/opt/pipeline/output/meet-the-team/final/meet_the_team_captioned.mp4"]

- [ ] **Step 2: Wait for owner feedback**

If approved:
```bash
sqlite3 /opt/pipeline/data/pipeline.db "UPDATE briefs SET status = 'approved', updated_at = datetime('now') WHERE id = $BRIEF_ID;"
sqlite3 /opt/pipeline/data/pipeline.db "INSERT INTO feedback_log (video_id, owner_feedback, sentiment, created_at) VALUES ($BRIEF_ID, '<feedback text>', 'approved', datetime('now'));"
```

If rejected: log feedback, identify which shots need rework, and repeat from the relevant task.

- [ ] **Step 3: Clean up intermediate files (after approval)**

```bash
# Keep final video, delete intermediates
rm -rf /opt/pipeline/output/meet-the-team/hero_frames/
rm -rf /opt/pipeline/output/meet-the-team/videos/shot*_norm.mp4
rm -rf /opt/pipeline/output/meet-the-team/videos/shot*_trim.mp4
rm -rf /opt/pipeline/output/meet-the-team/videos/concat.txt
rm -rf /opt/pipeline/output/meet-the-team/final/video_only.mp4
rm -rf /opt/pipeline/output/meet-the-team/final/captions_overlay.webm
rm -rf /opt/pipeline/output/meet-the-team/final/meet_the_team_raw.mp4
```

Keep: final captioned video, voiceover audio, ambient SFX, timestamps JSON.

---

## Summary

| Task | Description | Est. Cost |
|------|-------------|-----------|
| 0 | Environment check & brief registration | $0 |
| 1-4 | Hero frame generation + QA (4 shots) | ~$0.30-0.50 |
| 5-8 | Video animation + QA (4 clips × $0.42) | ~$1.68 |
| 9 | Voiceover generation | ~$0.05 |
| 10 | Ambient SFX download | Free |
| 11 | FFmpeg assembly | Free |
| 12 | Remotion captions | Free |
| 13 | Final QA | Free |
| 14 | Delivery | Free |
| **Total** | | **~$2-3** |

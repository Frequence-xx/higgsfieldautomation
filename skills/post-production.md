---
name: Post-Production
description: Final post-production pipeline for Snelverhuizen video ads — color grading with LUTs, frame interpolation, assembly order, and platform delivery export settings. Covers FFmpeg commands ready to copy-paste.
autoInvoke: true
triggers:
  - color grade
  - color grading
  - LUT
  - frame interpolation
  - RIFE
  - export
  - delivery
  - compression
  - H.264
  - post-production
  - assembly
negatives:
  - Do NOT invoke for caption/text overlay work (use captions-and-titles.md)
  - Do NOT invoke for audio mixing or voiceover (use halal-audio.md)
  - Do NOT invoke for hero frame generation or video generation (those are upstream)
---

# Post-Production Pipeline

Post-production order for every video:
1. **Assembly** — concatenate approved clips
2. **Color grade** — apply warm LUT per scene mood
3. **Frame interpolation** (optional) — smooth choppy motion clips only
4. **Text overlays** — via text-overlay-compositing.md workflow
5. **Audio mix** — via halal-audio.md workflow
6. **Loudness normalize** — -14 LUFS before delivery
7. **Delivery export** — H.264 + AAC, platform-specific settings

---

## 1. Assembly — Concatenating Clips

Use FFmpeg concat demuxer (no re-encode):

```bash
# Create concat list
cat > concat.txt << 'EOF'
file 'clip1.mp4'
file 'clip2.mp4'
file 'clip3.mp4'
EOF

ffmpeg -f concat -safe 0 -i concat.txt -c copy assembled.mp4
```

**Note:** All clips MUST have identical codec, resolution, frame rate, and pixel format before concat. If not, re-encode to a common spec first.

Normalize all clips to common spec before assembly:

```bash
ffmpeg -i clip.mp4 -vf "scale=1080:1920,fps=30" \
  -c:v libx264 -crf 18 -preset slow \
  -pix_fmt yuv420p -c:a aac -ar 48000 -ac 2 \
  clip_normalized.mp4
```

### 1a. AI Video Input — FFmpeg Colorspace Fix

**Problem:** Kling (and most AI video models) output H.264 with no explicit colorspace metadata. FFmpeg 7.x changed its default behavior (carried into 8.x) — it no longer assumes BT.709 when metadata is missing, causing a visible color shift (greens shift, contrast change) when re-encoding.

**Diagnosis:** Run ffprobe first:
```bash
ffprobe -v quiet -select_streams v:0 -show_entries \
  stream=color_space,color_primaries,color_transfer \
  -of default=noprint_wrappers=1 input_clip.mp4
```
If output shows `color_space=unknown` or is empty → apply the fix.

**Fix — inject BT.709 metadata at input (zero re-encode quality cost):**
```bash
ffmpeg -i input_clip.mp4 \
  -bsf:v h264_metadata=matrix_coefficients=1 \
  -c copy \
  clip_tagged.mp4
```
`matrix_coefficients=1` = BT.709. Apply once after download, before any normalization or grading. This tags the stream without re-encoding.

**Alternative (re-encode path, e.g. when also normalizing):**
```bash
ffmpeg -i input_clip.mp4 \
  -vf "scale=1080:1920,fps=30" \
  -c:v libx264 -crf 18 -preset slow \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -pix_fmt yuv420p -c:a aac -ar 48000 -ac 2 \
  clip_normalized.mp4
```

---

## 2. Color Grading

### 2a. LUT Application (Preferred — .cube files)

```bash
ffmpeg -i assembled.mp4 \
  -vf "lut3d=file=/opt/pipeline/luts/warm_cinematic.cube" \
  -c:v libx264 -crf 18 -preset slow \
  -pix_fmt yuv420p -c:a copy \
  graded.mp4
```

### 2b. Hald-CLUT Application (.png format LUTs)

```bash
ffmpeg -i assembled.mp4 -i /opt/pipeline/luts/warm_hald.png \
  -filter_complex "haldclut" \
  -c:v libx264 -crf 18 -preset slow \
  -pix_fmt yuv420p -c:a copy \
  graded.mp4
```

### 2c. FFmpeg eq Filter (No LUT — quick adjustments only)

Use when no LUT is available or for targeted correction:

```bash
ffmpeg -i assembled.mp4 \
  -vf "eq=brightness=0.03:contrast=1.05:saturation=1.15:gamma=0.95" \
  -c:v libx264 -crf 18 -preset slow \
  -pix_fmt yuv420p -c:a copy \
  graded.mp4
```

| Parameter | Range | Snelverhuizen default |
|-----------|-------|----------------------|
| brightness | -1.0 to 1.0 | +0.03 (slight lift) |
| contrast | 0 to 2 | 1.05 (slight punch) |
| saturation | 0 to 3 | 1.15 (warm vibrancy) |
| gamma | 0.1 to 10 | 0.95 (slight lift in shadows) |

### 2d. Banding Prevention (Sky / Gradient Backgrounds)

AI-generated video often has smooth gradient skies or walls. Compressing these to 8-bit yuv420p can produce visible color banding. Apply `zscale` dithering whenever the clip contains large gradient areas (sky, white wall, sunset):

```bash
ffmpeg -i graded.mp4 \
  -vf "zscale=t=linear:npl=100,format=gbrpf32le,\
zscale=p=bt709,tonemap=hable,\
zscale=t=bt709:m=bt709:r=tv,\
dither=error_diffusion,format=yuv420p" \
  -c:v libx264 -crf 18 -preset slow \
  -c:a copy \
  graded_nodither.mp4
```

**Quick version (when you just need dither on 8-bit yuv input, no HDR):**
```bash
ffmpeg -i graded.mp4 \
  -vf "zscale=dither=error_diffusion,format=yuv420p" \
  -c:v libx264 -crf 18 -preset slow \
  -c:a copy \
  graded_dithered.mp4
```

When to use: moving truck/van clips against sky, interior close-ups with white walls, wide establishing shots. Skip for close-up face shots (unnecessary and slightly slower).

### 2f. LUT Presets by Scene Mood

From cinematic-standards.md:

| Scene | Look | LUT/Treatment |
|-------|------|--------------|
| Family / arrival | Warm golden, amber highlights | Warm cinematic LUT (Kodak 2393 style) |
| Professional service | Neutral, clean whites | Skip LUT — eq saturation=1.05 only |
| Moving day / stress | Cool desaturated, blue shadows | Cool/teal LUT OR eq saturation=0.85 |
| Hero/reveal moment | High contrast warm, deep blacks | Warm high-contrast LUT |

### 2g. Free LUT Sources (No Cost)

| Source | Notes |
|--------|-------|
| Lutify.me/free-luts | Film emulation, Kodak 2393-based, require free account |
| FilterGrade free cinematic | Clean warm options, direct download |
| SmallHD free pack | Designed for monitoring, good for social media |
| ON1 free LUTs | Cinematic, portrait, B&W packs |

Store downloaded LUTs at `/opt/pipeline/luts/`. File format: `.cube` preferred (lut3d filter).

---

## 3. Frame Interpolation (Optional)

**When to use:** Only on character or truck clips that look choppy at playback speed. Most AI-generated clips at 24fps already have a cinematic feel — do NOT interpolate unless the clip looks unacceptably choppy.

**When NOT to use:**
- Fast-action clips (interpolation artifacts on fast motion)
- Clips with hard cuts within them
- Kling v3 Pro clips at 1080p — quality is typically fine

### 3a. REAL Video Enhancer — ARCHIVED (2026-07-13) — Use CLI Instead

**⚠️ SC207 (2026-07-13) — TNTwise REAL Video Enhancer ARCHIVED:** The GitHub repository (`TNTwise/REAL-Video-Enhancer`) was archived by the owner on **2026-07-13** and is now read-only. Last stable release was v2.4.1 (2026-01-02). No further development or updates will occur. Do NOT rely on this GUI tool going forward.

**Pipeline impact: NONE for headless use.** The `rife-ncnn-vulkan` CLI binary (separate repository: `TNTwise/rife-ncnn-vulkan`, v20250112) is **NOT archived** and remains the correct tool for our scripted pipeline. The GUI wrapper is gone; the CLI binary is fine.

**Action:** Use the rife-ncnn-vulkan CLI directly (§3b) — this was always the recommended path for server/headless use. The RVE GUI was only relevant for desktop manual use. Skip any GUI-based RVE workflow.

**Model currency check (2026-07-04):** No new Practical-RIFE models since v4.26 / v4.26.heavy (2024-09-21). **v4.22 is no longer the recommended model.** Practical-RIFE README recommends v4.25 as the default for most scenes and explicitly states v4.24+ is best for diffusion-generated video — use v4.25 as pipeline default. **SC182 (2026-07-04):** `rife-v4.25.heavy` confirmed supported by TNTwise binary v20250112 (bundled since v20241030 release) — documented below as high-quality middle tier.

Model selection for live-action / AI-generated video:
- **rife-v4.25** — **best for diffusion-generated video (Kling, Veo output) and general default.** Practical-RIFE project explicitly states v4.24+ is suitable for diffusion model video post-processing; v4.25 is the maintainer's recommended default for most scenes. Use this as our pipeline default.
- **rife-v4.25.lite** — lower-cost variant of v4.25 (2024-10-20). Use on server/headless environments with limited VRAM where full v4.25 OOMs. CLI: `-m rife-v4.25.lite` with the TNTwise binary. Quality is slightly below v4.25 full.
- **rife-v4.25.heavy** — higher-quality variant of v4.25 (2024-10-30). Supported by TNTwise rife-ncnn-vulkan v20250112. Use as a middle tier between v4.25 default and v4.26.heavy when a clip needs extra polish without the full GPU cost of v4.26.heavy. CLI: `-m rife-v4.25.heavy`. Not in RVE GUI — CLI only.
- **rife-v4.26.heavy** — highest quality variant of v4.26, significantly more GPU-intensive. Reserve for final delivery polish on important clips only (character close-ups, hero moments). Not in RVE GUI — CLI only via rife-ncnn-vulkan binary.
- **rife-v4.26** — latest standard model (2024-09-21). Similar quality to v4.25 on most content; use if v4.25 produces artifacts on a specific clip.
- **rife-v4.22** — prior recommendation (superseded). v4.24+ is the current guidance for diffusion video; retain only as legacy fallback.
- **rife-v4.6** — legacy fallback only (nihui original binary)

**CORRECTION from SC21:** Prior note that v4.26 is "anime-only" was incorrect. v4.26 is a general improvement. There is a separate `rife-v4.6-anime` variant for anime, which is unrelated.

### 3b. rife-ncnn-vulkan CLI (Headless / Scripted)

For scripted pipeline use (no GUI):

```bash
# TNTwise fork: https://github.com/TNTwise/rife-ncnn-vulkan/releases
# Latest binary release: v20250112 (Jan 12, 2025) — supports models through v4.26/v4.26.heavy and v4.25.heavy
# Download the Linux binary
unzip rife-ncnn-vulkan-linux.zip

# Extract frames
ffmpeg -i clip.mp4 -r 24 frames/%08d.png

# Interpolate with v4.25 (best for diffusion/AI-generated video — see §3a)
# No -x TTA flag — deprecated in v4.22+
./rife-ncnn-vulkan -i frames/ -o interp_frames/ -m rife-v4.25 -j 1:2:2
# Middle-tier quality: ./rife-ncnn-vulkan -i frames/ -o interp_frames/ -m rife-v4.25.heavy -j 1:2:2

# Reassemble at target fps
ffmpeg -r 48 -i interp_frames/%08d.png -i clip.mp4 \
  -map 0:v -map 1:a \
  -c:v libx264 -crf 18 -preset slow \
  -pix_fmt yuv420p -c:a copy \
  -r 30 clip_smooth.mp4
```

**Note:** Using nihui's binary (v4.6)? Keep `-x` flag. Using TNTwise binary with v4.22+? Drop it — TTA deprecated. **nihui/rife-ncnn-vulkan** has not released a new binary since October 2022 (max bundled model: v4.6). Use TNTwise fork for v4.25.

### 3c. Expected Quality Risks

- **Ghost artifacts** on complex motion — if seen, discard and use original
- **Face warping** on close-up character shots — high risk, skip interpolation for these
- **Blended frames** at hard cuts within a clip — ALWAYS split at scene changes before interpolating (§3d)

### 3d. Scene Change Detection Before RIFE (Mandatory Pre-Step)

RIFE blends across hard cuts, producing ghost frames. Detect and split clips at scene boundaries before interpolating each segment separately.

**Option A — PySceneDetect (recommended, handles splitting automatically):**
```bash
# Install (v0.7, requires Python 3.10+):
# Server/headless environments (our pipeline): pip install scenedetect-headless
# Desktop with GUI libraries:                  pip install scenedetect
# NOTE: The [opencv] extra no longer exists in v0.7 — opencv is now a core dependency.
#       Use scenedetect-headless on servers to avoid pulling in GUI libs (opencv-python-headless).

# Detect content-aware cuts and auto-split to segment_XXX.mp4 files
scenedetect -i clip.mp4 detect-content --threshold 27 split-video
# Lower threshold = more sensitive (catch subtle cuts); default 27 is safe for AI video
```
**v0.7 release notes (2026-05-03):**
- Frame numbers are now 1-based (was 0-based). The `detect-content --threshold` and `split-video` command syntax is unchanged — only affects scripts that reference specific frame numbers. Our pipeline command above is unaffected.
- **VFR (variable framerate) video support:** v0.7 properly handles VFR input — relevant because some AI model outputs (particularly Veo) may have slightly irregular frame timing. PySceneDetect 0.7 now reads actual frame timestamps instead of assuming constant framerate, so scene boundaries are more accurate on VFR clips.
- New `save-fcp` command exports scene list in Final Cut Pro XML format — not relevant to our FFmpeg pipeline but useful if editing in FCP.
- New `save-qp` command writes a QP keyframe file for x264/x265 — lets you force keyframes at scene boundaries during re-encode instead of splitting. Not needed for our RIFE pre-step (we split), but useful if re-encoding a long clip that contains multiple scenes.
- **install change**: `pip install scenedetect[opencv]` is invalid in v0.7 — opencv-python is now a core dep. Use `scenedetect-headless` on servers (see install command above).

**Option B — FFmpeg scdet (no install, timestamps only):**
```bash
# Get scene change timestamps (threshold 10 = ~10% luma change between frames)
ffmpeg -i clip.mp4 -vf "scdet=t=10" -f null - 2>&1 | grep "Parsed_scdet"

# Then split using those timestamps (replace 2.5,8.1 with actual values):
ffmpeg -i clip.mp4 -c copy \
  -f segment -segment_times "2.5,8.1" \
  -reset_timestamps 1 segment_%03d.mp4
```

**For Kling/Veo clips that are a single continuous shot (no cuts):** scene detection step can be skipped — single-shot AI clips typically have no internal cuts.

**PySceneDetect v0.7.1 RELEASED (2026-07-21, now stable).** All features previously listed as "coming" are now confirmed shipped:

- **`--expand` flag for `split-video`:** When detecting within a time window (`-s`/`-e`), the first output clip is extended back to video start and the last clip is extended to video end — no footage lost at boundaries. Use with our standard split command: `scenedetect -i clip.mp4 detect-content --threshold 27 split-video --expand`
- **`expand_scenes_to_bounds()` API helper:** Extends a scene list to fill the full video bounds programmatically. Use in scripted pipelines when processing a time-windowed sub-range.
- **`backend` keyword arg for `scenedetect.detect()`:** Accepts `"opencv"` (default), `"pyav"`, or `"moviepy"` — selectable programmatically without config. Use `backend="pyav"` in headless/server pipelines for the most VFR-accurate results.

**New in v0.7.1 (not previously documented):**

- **`VideoStreamConcat`:** Processes multiple video files as a single continuous stream with a unified monotonic timeline. Useful for running scene detection across a batch of clips (e.g., all shots in a session) without re-splitting each one. Use: `open_video([clip1.mp4, clip2.mp4, ...])` or pass a list to `detect()`.
- **`VideoStream.decode_failures` property:** Public counter of frames skipped during decoding. Use to flag AI-generated clips (Kling/Veo) with frame-level corruption — any clip with `decode_failures > 0` should be flagged for manual review before RIFE interpolation.
- **PyAV backend tolerates up to 8 consecutive corrupt frames** (previously failed hard on first corrupt frame). More robust for AI-generated clips that can have occasional frame decode issues.
- **PyAV presentation time normalization:** Fixes delayed-start file issues where PTS timestamps don't start at 0. Improves scene boundary accuracy on VFR AI-generated outputs.
- **`FrameTimecode` VFR fix:** Comparisons now use exact `pts` values instead of rounded frame numbers for VFR videos — more accurate split points on Veo clips (which may have slightly irregular frame timing).
- **Official Docker image** published to GitHub Container Registry — use for containerized pipeline deployments.
- **Windows distribution bundles OpenCV 5.0, PyAV 18, FFmpeg 8.1.2, Pillow 12.3.0.**

Install command unchanged: `pip install scenedetect-headless` (no `[opencv]` extra — still a core dep in v0.7.1).

**Practical pipeline update:** Replace bare `split-video` with `split-video --expand` in the standard scene-detect command to ensure no footage is trimmed at the beginning/end of the clip. This is especially relevant when detecting short sub-ranges within a longer AI-generated clip.

---

## 4. Loudness Normalize Before Delivery

Cross-reference: detailed mixing in `halal-audio.md`. Final step before export:

```bash
# Two-pass loudnorm for social media delivery (-14 LUFS target)
# Pass 1: measure
ffmpeg -i mixed.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json \
  -f null /dev/null 2>&1 | grep -A 10 "input_i"

# Pass 2: apply (replace measured values)
ffmpeg -i mixed.mp4 \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=-24.3:measured_TP=-2.1:measured_LRA=6.4:linear=true" \
  -c:v copy -c:a aac -ar 48000 -b:a 256k \
  normalized.mp4
```

**Loudness targets by platform:**

| Platform | Target LUFS | True Peak | Notes |
|----------|-------------|-----------|-------|
| Instagram Reels | -14 LUFS | -1.5 dBTP | Platform normalizes to ~-14 |
| TikTok | -14 LUFS | -1.5 dBTP | Same normalization |
| YouTube / Shorts | -14 LUFS | -1.0 dBTP | YouTube normalizes to -14 |
| WhatsApp / Telegram | -16 LUFS | -2.0 dBTP | Lower target, device speakers vary |

---

## 5. Delivery Export

### 5a. Master Export (High Quality, For Archive + Editing)

```bash
ffmpeg -i normalized.mp4 \
  -c:v libx264 -crf 18 -preset slow \
  -profile:v high -level:v 4.1 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -c:a aac -ar 48000 -b:a 256k -ac 2 \
  delivery_master.mp4
```

### 5b. Social Media Upload (Optimized Bitrate)

For Instagram Reels (10–20 Mbps recommended upload — Instagram recompresses anyway, upload high):

```bash
ffmpeg -i normalized.mp4 \
  -c:v libx264 -b:v 15000k -maxrate 20000k -bufsize 20000k \
  -preset slow -profile:v high -level:v 4.1 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -c:a aac -ar 48000 -b:a 256k -ac 2 \
  upload_reels.mp4
```

For TikTok (8–15 Mbps — below 5 Mbps triggers quality downgrade flag):

```bash
ffmpeg -i normalized.mp4 \
  -c:v libx264 -b:v 10000k -maxrate 15000k -bufsize 15000k \
  -preset slow -profile:v high -level:v 4.1 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -c:a aac -ar 48000 -b:a 256k -ac 2 \
  upload_tiktok.mp4
```

**TikTok 60fps option (high-motion clips):** TikTok supports and recommends 60fps for fast-moving content (truck reveal, panning shots, fast camera moves). For 60fps export, add `-r 60` and raise maxrate: `-b:v 15000k -maxrate 20000k -bufsize 20000k`. Our moving ads are typically 24–30fps from Kling/Veo — only upconvert to 60fps if the source is 60fps or if RIFE frame interpolation was applied.

**Note:** Both platforms transcode H.264 to AV1 internally for delivery — that is Meta/TikTok's pipeline, not ours. Upload H.264; uploading AV1 causes a double-transcode with quality loss.

**TikTok "Upload HD" creator toggle (2026):** When the owner uploads directly via the TikTok app, advise them to enable "Upload HD" on the posting screen (tap "More options" → toggle "Upload HD") before submitting. This sends the file at higher quality before TikTok's compression pass. For Desktop/Studio uploads, high-quality mode is applied automatically — no toggle needed.

### 5c. Platform Specs Reference (2026)

| Platform | Resolution | FPS | Codec | Audio | Max File | Max Length |
|----------|-----------|-----|-------|-------|---------|------------|
| Instagram Reels | 1080×1920 | 30 | H.264 | AAC 256k 48kHz | 4 GB | **15 min** (upload) / 20 min (in-app) |
| TikTok | 1080×1920 | 30 | H.264 | AAC 192k 44.1kHz | 287.6 MB (mobile) / 10 GB (Studio) | 10 min |
| YouTube Shorts | 1080×1920 | 30 | H.264 | AAC 256k 48kHz | — | 3 min |
| WhatsApp Status | 1080×1920 | 30 | H.264 | AAC 128k | **16 MB** (video message) | 60s |

**Instagram Reels max length note:** Any video under 15 minutes uploaded from gallery is auto-classified as a Reel; in-app recording cap is 20 minutes (rolling out — not universal). **Algorithm discovery threshold:** under 90 seconds = widest non-follower reach; over 3 minutes = algorithm stops recommending to non-followers entirely. The 3-minute cutoff is the hard penalty — content above it surfaces mainly to existing followers. Our ads are 30–60s — well within all limits.

**TikTok upload:** Mobile app cap is 287.6 MB (iOS) / 72 MB (Android). Always upload via TikTok Studio (desktop) for master-quality files — supports up to 10 GB with no in-app compression.

**-pix_fmt yuv420p is MANDATORY** for all platform uploads. Without it, Instagram and some players reject the file silently.

**-movflags +faststart** moves the moov atom to the front — required for web streaming and Instagram playback.

**H.265/HEVC:** TikTok accepts HEVC but H.264 re-compresses it anyway. Instagram does NOT reliably accept H.265. Use H.264 for all platforms.

**WhatsApp delivery to owner:** Regular video message = 16 MB limit (lossy auto-compression). To send the full-quality master file: use **Document share** (paperclip → Document) — supports up to **2 GB** with no recompression. Always deliver the master via document share, not as a video message.

### 5f. Instagram Reels Safe Zone (Text / Logo Placement)

Instagram Reels UI elements overlay the video. Critical danger zones to avoid for text and logos:

| Zone | Pixels from edge | What occupies it |
|------|-----------------|------------------|
| Bottom danger zone | Bottom **320px** (organic) / 370px (ads) | Caption bar, audio attribution, engagement buttons |
| Right danger zone | Right **120px** | Like / comment / share / save buttons |
| Top danger zone | Top **108px** | Notch / dynamic island on device |
| Left danger zone | Left **60px** | Profile overlay elements |

**Effective safe content area: ~900 × 1492px, centered.**

**Hook text position:** Center horizontally, place between y=200px and y=600px from top — safe across all devices and notch sizes.

**CTA pill / URL:** Place between y=1200px and y=1600px from top — below center, above the 320px bottom danger zone.

This directly governs `drawtext` y-coordinates in text-overlay-compositing.md. When calculating `y=` values in FFmpeg `drawtext`, measure from top edge.

**Meta March 2026 — Unified Stories + Reels safe zone (paid ads only):** Meta unified Instagram Stories and Instagram Reels into a single 9:16 safe zone for paid ad creatives. One asset now works across both placements without re-cropping. The unified **ad** safe zone is more conservative than organic Reels: top 14% (~269px), bottom 20–35% (~384–672px depending on format), sides 6% each (~65px). **For our organic delivery (no paid boost), the existing organic safe zone values above remain correct.** If Farouq ever boosts a Reel as a paid ad, apply the stricter unified margins: keep all text and logos within a ~950 × 1267px center area (y=269 to y=1536, x=65 to x=1015).

### 5g. TikTok Safe Zone (Text / Logo Placement)

TikTok's right-side dead zone is significantly wider than Instagram's — this is the most common placement mistake when repurposing Reels assets for TikTok.

| Zone | Pixels from edge | What occupies it |
|------|-----------------|------------------|
| Bottom danger zone | Bottom **324px** (organic) / **370px** (ads/branded) | Caption, sound attribution, engagement buttons |
| Right danger zone | Right **~184px** | Like, Comment, Share, Bookmark, "Add to Playlist" — right column expanded ~+20px in Jan 2026 (from 164px base) |
| Top danger zone | Top **130px** | Back button, overflow menu |
| Left danger zone | Left **60px** | Profile avatar |

**Effective safe content area: ~836 × 1466px, centered.** (1080 − 60 left − 184 right = 836px; 1920 − 130 top − 324 bottom = 1466px. Right margin corrected from prior ~180px estimate: sources confirm Add to Playlist button added ~20px, not ~16px, making right margin ~184px. SC133 correction 2026-06-16.)

**Key difference vs Instagram:** TikTok's right dead zone is ~184px vs Instagram's 120px. When reusing an asset designed for Instagram, any element within the right 184px may be hidden on TikTok. Re-check placement of logos, phone numbers, and CTAs before cross-posting.

**Upload bitrate guidance:** Upload at 8–15 Mbps for 1080p/30fps. Below 5 Mbps triggers TikTok's quality downgrade flag. Desktop upload via TikTok Studio supports up to **10 GB** — always upload via desktop for master-quality delivery, not mobile (mobile cap is 287 MB iOS / 72 MB Android).

### 5e. File-Size-Constrained Export (WhatsApp 16 MB video message)

Use only when the owner specifically wants a standard video message (not document). Two-pass encoding for exact file size target:

```bash
# Formula: target_bitrate_kbps = (target_MB × 8 × 1024 / duration_sec) - audio_kbps
# For 30s video → 15MB target (leaving 1MB headroom): (15 × 8 × 1024 / 30) - 128 = 3966 kbps ≈ 3900k

# Pass 1 (analysis only)
ffmpeg -i normalized.mp4 \
  -c:v libx264 -b:v 3900k -pass 1 -an -f null /dev/null

# Pass 2 (encode)
ffmpeg -i normalized.mp4 \
  -c:v libx264 -b:v 3900k -pass 2 \
  -c:a aac -b:a 128k -ar 44100 \
  -vf scale=1080:1920 -pix_fmt yuv420p -movflags +faststart \
  upload_whatsapp_video.mp4
```

### 5h. AV1 Archive Encoding (Internal Storage Only — NOT for Platform Upload)

SVT-AV1 v4.2.0 (2026-07-13) + FFmpeg 8.x libsvtav1 offers 30–50% smaller files vs H.264 at equivalent quality. Use for internal archive masters to save disk space.

```bash
# Check SVT-AV1 availability
ffmpeg -encoders 2>/dev/null | grep svtav1

# Archive encode (internal storage only)
ffmpeg -i normalized.mp4 \
  -c:v libsvtav1 -crf 30 -preset 6 \
  -svtav1-params tune=0 \
  -pix_fmt yuv420p \
  -c:a aac -ar 48000 -b:a 256k \
  archive_av1.mp4
```

| CRF | Quality | Use case |
|-----|---------|---------|
| 22–25 | Near-transparent | Long-term production archive |
| 28–32 | High | Review copies, reference cache |
| 35+ | Acceptable | Low-priority storage |

**SVT-AV1 4.0+ `tune` options (set via `-svtav1-params tune=N`):**
| Value | Name | When to use |
|-------|------|------------|
| `0` | VQ | Psycho-visual / perceptual quality. **Use this for our video archive.** |
| `1` | PSNR (default) | Max PSNR for metrics; not perceptual; encoder default |
| `2` | SSIM | SSIM-optimized; good for detailed textures |
| `3` | IQ (Image Quality) | **Still image / AVIF ONLY** — added in SVT-AV1 4.0 for static frames, not video |
| `4` | MS-SSIM Still | **Still image / AVIF ONLY** — added in SVT-AV1 4.0, not intended for video |

Use `tune=0` (VQ) for all Snelverhuizen archive video encodes — it is the psycho-visual mode. **Do NOT use tune=3**: tune=3 (IQ) and tune=4 (MS-SSIM) were added in SVT-AV1 4.0 specifically for still image / AVIF encoding and should not be applied to video. SVT-AV1 4.0 also extended CRF range to 70 with quarter-step granularity — CRF 22–32 range remains our sweet spot.

**CRITICAL:** Do NOT upload AV1 to Instagram (rejected) or TikTok (triggers double-transcode). AV1 archive is for internal reference only — always deliver H.264 to platforms and owners.

**Preset guide (SVT-AV1):** Preset 0–4 = slow, highest quality. Preset 6 = good balance. Preset 8–12 = fast/realtime. Default `preset 6` is right for our archive use case.

**SVT-AV1-PSY archived (Feb 12, 2026):** The SVT-AV1-PSY psychovisual fork was officially archived — its perceptual features (including tune=0 as default) are being merged into mainline SVT-AV1. Our pipeline already uses mainline SVT-AV1 with `-svtav1-params tune=0` (VQ), so there is no change required. An active community fork (`svt-av1-psyex` by BlueSwordM, latest 3.0.2-B) exists if more aggressive psychovisual options are ever needed, but mainline SVT-AV1 4.1 with tune=0 is the correct choice for our archive encodes.

---

### 5d. Quality Check After Export

Before marking delivery complete:

```bash
# Inspect output
ffprobe -v quiet -print_format json -show_streams delivery_master.mp4 | \
  python3 -c "import json,sys; s=json.load(sys.stdin)['streams']; \
  [print(f\"{x['codec_type']}: {x.get('codec_name','-')} {x.get('width','-')}x{x.get('height','-')} {x.get('avg_frame_rate','-')} {x.get('bit_rate','-')}bps\") for x in s]"
```

Expected output for a valid delivery file:
```
video: h264 1080x1920 30/1 ~4000000bps
audio: aac - - 256000bps
```

---

## 6. FFmpeg 8.0 Native Whisper Filter (Quick Segment-Level SRT)

**FFmpeg 8.0 "Huffman"** (released 2025-08-22) and **8.1 "Hoare"** (released 2026-03-17) introduced a built-in `whisper` audio filter (`af_whisper`). **Current stable: 9.0.1 "Lei"** (released 2026-08-12, confirmed current 2026-08-29) — the `whisper` filter is confirmed present in 9.0.x. All pipeline-relevant filters (drawvg, normalize, zscale, hqdn3d) are stable and unchanged through 9.0.1. — powered by whisper.cpp — that can generate SRT/VTT subtitles in one command without a separate tool.

**Check availability:**
```bash
ffmpeg -version 2>&1 | grep -i "whisper\|version"
# Also: ffmpeg -filters 2>/dev/null | grep whisper
```

**Basic usage — Dutch SRT generation:**
```bash
# Requires FFmpeg built with --enable-whisper (and ggml model downloaded)
ffmpeg -i voiceover.mp4 -vn \
  -af "whisper=model=/opt/pipeline/models/ggml-medium.bin:language=nl:destination=output.srt:format=srt" \
  -f null -
```

**With Voice Activity Detection (reduces hallucinations on silence):**
```bash
ffmpeg -i voiceover.mp4 -vn \
  -af "whisper=model=/opt/pipeline/models/ggml-medium.bin:language=nl:format=srt:destination=output.srt:vad_model=/opt/pipeline/models/silero-v5.1.2-ggml.bin:vad_threshold=0.6" \
  -f null -
```

**Key parameters:**
| Parameter | Value | Notes |
|-----------|-------|-------|
| `model` | path to ggml-*.bin | medium or large-v3 for Dutch accuracy |
| `language` | `nl` | Force Dutch — do NOT use `auto` on short Dutch clips (misdetects) |
| `format` | `srt` or `vtt` or `json` | json for downstream processing |
| `destination` | output path | Required; omit to get stdout |
| `vad_threshold` | 0.6 | 0.5–0.7 range; higher = more aggressive silence removal |

**IMPORTANT CAVEAT — word-level timestamps:**
The FFmpeg native Whisper filter emits **segment-level** timestamps only (full sentence blocks). It does NOT yet expose `word_timestamps` / per-token timing that our orange-highlight karaoke caption pipeline requires. For word-level timestamps on Dutch voiceover, continue using **WhisperX** or **whisper.cpp CLI with `--word-timestamps true`** (documented in `captions-and-titles.md`). Use the FFmpeg filter only for quick rough-cut SRT review during production, not for final caption output.

**Model download (ggml format):**
```bash
# Medium — best accuracy/speed balance for Dutch
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin \
  -O /opt/pipeline/models/ggml-medium.bin

# Large-v3 — highest Dutch accuracy (slower)
wget https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin \
  -O /opt/pipeline/models/ggml-large-v3.bin
```

---

## 7. VMAF Quality Scoring (Optional QA)

Objective quality scoring of the exported file vs. the assembled pre-export reference. Requires FFmpeg built with `--enable-libvmaf` (check: `ffmpeg -filters 2>/dev/null | grep vmaf`).

```bash
# Score encoded output against pre-export reference
# n_subsample=5 = analyze 1 in 5 frames → ~4x faster, negligible score difference
ffmpeg -i assembled_pre_export.mp4 -i delivery_master.mp4 \
  -lavfi "libvmaf=log_fmt=json:log_path=vmaf_score.json:n_subsample=5" \
  -f null -
```

**VMAF model note:** Default model `vmaf_v0.6.1` is the standard. Versions v0.6.2 and v0.6.3 exist in the Netflix/vmaf repo but have "no material differences" compared to v0.6.1 per official docs — no need to override the model. The default FFmpeg libvmaf build uses v0.6.1, which is correct for our 1080p social-media delivery scoring.

VMAF score interpretation:

| Score | Quality |
|-------|--------|
| ≥ 95 | Excellent — imperceptible loss |
| 85–94 | Good — minor compression visible only on close inspection |
| 70–84 | Acceptable — visible compression, borderline for delivery |
| < 70 | Reject — re-export at higher bitrate |

**Snelverhuizen threshold: ≥ 90 required before delivery.** If score < 90, increase CRF by -2 (lower = better) and re-export.

---

## 8. Hardware-Accelerated Export (Speed Optimization)

For faster export on long or repeated encodes. Output quality matches libx264 at equivalent settings.

### 8a. NVIDIA NVENC (NVIDIA GPU)

```bash
# Check availability
ffmpeg -encoders 2>/dev/null | grep nvenc

# Encode (equivalent to libx264 CRF 18 quality)
ffmpeg -i normalized.mp4 \
  -c:v h264_nvenc -preset p7 -tune hq -cq 20 \
  -profile:v high -level:v 4.1 \
  -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -ar 48000 -b:a 256k -ac 2 \
  delivery_fast.mp4
```

Speed: ~3-5x faster than `libx264 -preset slow`.

### 8b. VAAPI (Intel/AMD GPU, Linux)

```bash
# Check device
ls /dev/dri/renderD*

# Encode
ffmpeg -vaapi_device /dev/dri/renderD128 \
  -i normalized.mp4 \
  -vf 'format=nv12,hwupload' \
  -c:v h264_vaapi -qp 19 \
  -movflags +faststart \
  -c:a aac -ar 48000 -b:a 256k -ac 2 \
  delivery_fast.mp4
```

**Note:** Hardware encoders are for speed only. For archive master use `libx264 -preset slow -crf 18` — it produces better quality/size ratio. Use NVENC/VAAPI for review copies or when time is tight.

---

## 9. AI Video Artifact Correction (Conditional — Only When Visible Problems Present)

Kling and Veo clips occasionally show two specific issues. Only apply these fixes when the artifact is visible — running them unconditionally degrades clean clips.

### 9a. Temporal Brightness Flicker

**Symptom:** Clip brightness pulses or flickers between frames — visible as a rapid "flash" or inconsistent exposure. Most common on dark interior shots or clips with moving shadows.

**Cause:** Diffusion model inconsistency in per-frame brightness values.

**Fix — FFmpeg `normalize` with temporal smoothing:**
```bash
# smoothing=15 = rolling average over 15 frames (0.5s at 30fps)
# For severe flicker, increase to smoothing=30
ffmpeg -i clip.mp4 \
  -vf "normalize=blackpt=black:whitept=white:smoothing=15:strength=0.7" \
  -c:v libx264 -crf 18 -preset slow \
  -pix_fmt yuv420p -c:a copy \
  clip_deflickered.mp4
```

**Parameter guide:**
- `smoothing` — number of previous frames in rolling average. 15 (0.5s) for mild flicker, 30 (1s) for severe. Higher values = more lag in tracking true exposure changes.
- `strength` — 0.0 to 1.0. Start at 0.7; reduce if the filter over-normalizes skin tones.
- `independence=0.0` — linked mode (preserves color balance). Default is 1.0 (independent per-channel, causes color shifts). Add `:independence=0.0` for skin tones.

**Full form for character close-ups (preserves skin tone):**
```bash
-vf "normalize=blackpt=black:whitept=white:smoothing=15:strength=0.7:independence=0.0"
```

### 9b. Blocking / Compression Artifacts (Light Denoise + Sharpen)

**Symptom:** Visible macroblock edges or mosquito noise, typically on backgrounds or smooth gradient areas. Distinct from temporal flicker — it's spatial, not temporal.

**Fix — hqdn3d denoise followed by unsharp:**
```bash
# Light: preserves detail, removes mosquito noise
ffmpeg -i clip.mp4 \
  -vf "hqdn3d=4:4:3:3,unsharp=5:5:0.8:5:5:0.4" \
  -c:v libx264 -crf 18 -preset slow \
  -pix_fmt yuv420p -c:a copy \
  clip_cleaned.mp4

# Moderate: more aggressive denoise (use only on backgrounds, not faces)
ffmpeg -i clip.mp4 \
  -vf "hqdn3d=8:6:6:6,unsharp=5:5:1.0:5:5:0.4" \
  -c:v libx264 -crf 18 -preset slow \
  -pix_fmt yuv420p -c:a copy \
  clip_cleaned_moderate.mp4
```

**hqdn3d parameter order:** `luma_spatial:chroma_spatial:luma_temporal:chroma_temporal`
- Light (4:4:3:3): safe for all shots including faces
- Moderate (8:6:6:6): backgrounds and truck shots only — can soften faces

**unsharp parameter order:** `luma_msize_x:luma_msize_y:luma_amount:chroma_msize_x:chroma_msize_y:chroma_amount`
- `0.8` luma amount = gentle sharpening to recover edge detail lost to denoise
- Do NOT increase above 1.5 — produces ringing halos on AI-generated faces

**Warning:** Never apply both flicker fix (§9a) and denoise (§9b) in a single command to a clip that doesn't need both. Chain them only if needed: `"normalize=...,hqdn3d=...,unsharp=..."`

---

## 10. drawvg Vector Graphics Filter (FFmpeg 8.1+)

**Available since FFmpeg 8.1 "Hoare" (2026-03-16).** `drawvg` renders vector graphics on video frames using a scripting language (VGS — Vector Graphics Script) powered by the Cairo library. Unlike `drawtext`, it supports full vector shapes: rounded rectangles, arcs, paths, and arbitrary fill colors with exact HEX values.

**Why this matters for Snelverhuizen:**
- Draws the orange #FC8434 pill badge / CTA overlay natively in FFmpeg (no Remotion/AE required for simple shapes)
- Coordinates computed dynamically from frame dimensions — works correctly at any resolution
- Avoids font-rendering inconsistencies of `drawtext` for complex badge shapes

**Check availability:**
```bash
ffmpeg -version 2>&1 | grep -i "version"
ffmpeg -filters 2>/dev/null | grep drawvg
```

**Basic rounded-rectangle brand badge (orange pill with text):**
```bash
# badge.vgs — save this file first
cat > /opt/pipeline/overlays/brand_badge.vgs << 'EOF'
# Orange pill CTA badge — bottom-center placement
# Frame: 1080x1920. Badge: 600px wide, 80px tall, centered x=(1080-600)/2=240, top-y=1510
setcolor #FC8434
roundedrect 240 1510 600 80 40
fill
EOF

ffmpeg -i graded.mp4 \
  -vf "drawvg=file=/opt/pipeline/overlays/brand_badge.vgs" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy \
  with_badge.mp4
```

**VGS command reference (correct names — the prior `set_source_rgb` / `rectangle` were wrong):**

| Purpose | Correct VGS command | Notes |
|---------|--------------------|----|
| Set fill color (float) | `setrgba r g b a` | All values 0–1; alpha=1 for opaque |
| Set fill color (hex, direct) | `setcolor #FC8434` | **Preferred** — direct hex syntax, FFmpeg 8.1.x+ |
| Set fill color with alpha | `setcolor #FC8434@@0.5` | `@@N` suffix sets alpha (0–1); `@@1` = opaque |
| Set fill color via variable | `setvar c #FC8434` then `setcolor c` | For reusable color constants in longer scripts — direct `#rrggbb` syntax now works correctly in variables (PR #21128, ~Dec 2025) |
| Rounded rectangle | `roundedrect x y w h radius` | `radius = h/2` for perfect pill |
| Plain rectangle | `rect x y w h` | NOT `rectangle` |
| Arc | `arc xc yc radius angle1 angle2` | Angles in radians; counterclockwise |
| Fill path | `fill` | Fills closed path with current color |

**Practical workflow — badge shape + drawtext layer:**
For our typical branded overlay (orange pill + white text), layer `drawvg` (shape) then `drawtext` (text) in the same `-vf` chain:
```bash
ffmpeg -i graded.mp4 \
  -vf "drawvg=file=/opt/pipeline/overlays/brand_badge.vgs, \
       drawtext=text='SNELVERHUIZEN.NL':fontfile=/opt/pipeline/fonts/Montserrat-Bold.ttf:\
       fontsize=42:fontcolor=white:x=(w-text_w)/2:y=1535" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy \
  with_overlay.mp4
```

**Post-8.1 patch (PR #21128, ~Dec 2025):** Improved color handling when colors are passed via `setvar`/`call` variables. The old workaround of encoding colors as `0xRRGGBBAA` integer arguments is no longer needed — use direct `#rrggbb` hex throughout. If any VGS scripts use `0xRRGGBBAA` encoding, migrate to `setcolor #FC8434` style.

**Limitation:** VGS is NOT SVG — it uses its own language. Static SVG files cannot be directly imported. Use for programmatically-defined shapes (rectangles, arcs, lines) where dynamic coordinates or exact brand colors matter. For complex imported vector art, continue using the PNG overlay workflow.

**Documentation:** https://ffmpeg.org/drawvg-reference.html

---

## 11. Tool Version Status (confirmed 2026-07-04, SC182)

All post-production tools confirmed as of study cycle 182 (2026-07-04):

| Tool | Confirmed current version | Status |
|------|--------------------------|--------|
| FFmpeg stable | **9.0.1 (released 2026-08-12)** | **⚠️ MAJOR VERSION:** FFmpeg 9.0 "Lei" released Aug 4, 2026 (9.0.1 patch Aug 12). Named in tribute to Lei Xiaohua. **All pipeline filter commands remain backward compatible** — `drawvg`, `normalize`, `zscale`, `hqdn3d`, `loudnorm`, `whisper`, `h264_metadata` BSF, `lut3d`, `haldclut`, `eq`, `libsvtav1`, `libvmaf` all confirmed present in 9.0. Library version bumps (libavcodec → 63.x, libavformat → 63.x) are C API changes only — no CLI impact. **Breaking change: `tls_verify` now defaults to 1** — FFmpeg 9.0 enforces HTTPS certificate verification for input URLs (prior default was 0 = no verification). AIMLAPI CDN URLs use valid CA-signed certs so no pipeline impact expected. If `ffmpeg -i <cdn_url>` fails with "certificate verify failed" on 9.0, the CDN cert is invalid — investigate rather than disabling verification. New 9.0 features not relevant to current pipeline: native animated WebP decode, ONNX Runtime DNN backend for GPU inference, Vulkan for APV codec, `v360_vulkan` (360° GPU projection), `vf_frc_amf` (AMD AMF frame interpolation — AMD-only), `vf_vqe_amf` (AMD video quality enhancer), `transpose_cuda` (NVIDIA-only), `afreqshift`/`asoftclip` (music audio effects). See SC256 and SC291 notes. |
| Practical-RIFE | v4.26 / v4.26.heavy (2024-09-21) | No v4.27 as of 2026-06-30 — v4.25 remains pipeline default for diffusion video |
| TNTwise REAL Video Enhancer | ~~v2.4.1~~ **ARCHIVED 2026-07-13** | GUI repo archived — do NOT use for new work. Use rife-ncnn-vulkan CLI (§3b) directly. |
| TNTwise rife-ncnn-vulkan CLI | v20250112 (2025-01-12) | **Primary interpolation tool** — separate repo, NOT archived, unaffected by RVE archival. |
| PySceneDetect | **v0.7.1 (2026-07-21)** | **NOW STABLE.** Replaces v0.7.0. All documented v0.7.1 features confirmed: `--expand` flag (use `split-video --expand`), `backend` kwarg, `expand_scenes_to_bounds()`. NEW: `VideoStreamConcat`, `VideoStream.decode_failures`, PyAV corrupt-frame tolerance (8 frames), PyAV PTS normalization. See §3d for full details. Install: `pip install scenedetect-headless`. |
| SVT-AV1 | **v4.2.0 (2026-07-13)** | New: `--tune-vmaf` (~15% VMAF BD-rate gain for VOD/archive); CBR Kalman-filter rate control; ARM NEON/SVE2 kernels. Pipeline commands (§5h) unchanged — `-svtav1-params tune=0` (VQ) remains correct. See SC221 update. |
| Remotion | **v4.0.518 (released 2026-08-26)** | `@remotion/effects` now has **60+ effects** since launch at v4.0.465 (May 22, 2026). Pipeline-documented: `colorKey()`, `linearProgressiveBlur()`, `checkerboard()`, `emboss()`, `gridlines()`, **`zoomBlur()`** (v4.0.481 — §11h), `radialProgressiveBlur()` (SC161 — §11a), `cornerPin()`, `lightTrail()` (§11c), `linearGradient()` (SC168 — §11d), `venetianBlinds()` (SC189 — §11f), `paper()`, `roughenEdges()` (SC195 — §11g), `thermalVision()`, `pixelate()` (v4.0.479 — §11i), `glow()`, `duotone()`, `dropShadow()`, `brightness()` (v4.0.466–468 — §11j), **`linearProgressivePixelate()`** (v4.0.490 — §11k), **`liquidContours()`**, **`skew()`** (v4.0.491 — §11l), **`wave()`**, **`noiseDisplacement()`** (SC235 — §11m), **`regionblur()`** (v4.0.507), **`exposure()`** **`whiteBalance()`** **`vibrance()`** **`levels()`** **`shadowsHighlights()`** (v4.0.508), **`colorCorrection()`** (v4.0.509) — all documented in §11n (SC263). **`tile()`** (v4.0.513 — §11o, SC277). **`outline()`** (v4.0.515 — §11p, SC284). New package: **`@remotion/rough-notation`** (v4.0.490 — sketch/annotation overlays). **New package: `@remotion/mac-cursors`** (v4.0.513 — macOS cursor animation; pipeline relevance: none for moving ads). `@remotion/media` now **stable**. ProRes support in `@remotion/media` (Mediabunny 1.50.8). NVENC H.264/H.265 encoding on Linux/Windows. **v4.0.513 `@remotion/media` audio fix:** non-standard sample rates (e.g., 22050 Hz source audio) now correctly resampled to 48000 Hz — previously caused distorted or sped-up audio in compositions mixing voiceover and SFX at different sample rates. v4.0.488 fixes looped audio dropout. **Bundled FFmpeg binary: `--enable-nonfree` removed** (libfdk_aac removed from Remotion's compositor binary — no pipeline impact, we use system FFmpeg). **v4.0.492:** `muted` prop on `<Video>`; negative sequence offset. **v4.0.494:** Sequence opacity preservation fix. **v4.0.496–499 (2026-07-21–24):** Studio-only / opacity-leak fix / Zod upgrade — see SC249 note. **v4.0.507 (2026-08-07): `regionblur()` added to @remotion/effects.** **v4.0.508 (2026-08-11): `exposure()`, `whiteBalance()`, `vibrance()`, `levels()`, `shadowsHighlights()` added.** **v4.0.509 (2026-08-12): `colorCorrection()` added.** **v4.0.510 (2026-08-14): `@remotion/elements` introduced** — data visualization / UI components: animated line chart, vertical bar chart, animated pie chart, spinning text wheel, product discount callout. These are a NEW PACKAGE separate from `@remotion/effects` (visual filter effects). Install: `npm install @remotion/elements` (package name unconfirmed from available docs — verify with `npm view @remotion/elements version`). No new @remotion/effects in v4.0.510. v4.0.511 (2026-08-14): Interactivity regression fix from v4.0.510. v4.0.512 (2026-08-14): Republish of v4.0.511 to fix npm staging delays. **v4.0.513 (2026-08-18): `tile()` added to @remotion/effects; `@remotion/mac-cursors` new package; `@remotion/media` audio sample-rate conversion fix.** **v4.0.516 (2026-08-24): Studio-only (rulers/guides toolbar, asset drag-and-drop, timeline optimizations) — no new @remotion/effects, no pipeline impact.** **v4.0.517 (2026-08-25): `@remotion/gsap` new package (GSAP animation integration); `fisheye()` behavior fix (pixels outside fisheye radius now preserved instead of clipped — no impact if fisheye unused); Studio enhancements; security dep updates.** **v4.0.518 (2026-08-26): `@remotion/whisper-webgpu` new package (browser/WebGPU Whisper transcription — browser-only, NOT applicable to our server-side whisper.cpp pipeline); `@remotion/captions` adds forced page breaks (explicit pagination control — useful for Dutch voiceover with irregular natural breaks); Social Safe Zones overlay element in Studio (visual guide, no render impact); audio visualization elements (mirrored audio spectrum, audio oscilloscope).** **⚠️ v5.0 migration docs live but not yet released — see §11b.** |
| Instagram safe zones | unchanged | 320px bottom (organic), 120px right, 108px top, 60px left — re-confirmed SC147 via multiple 2026 sources |
| TikTok safe zones | unchanged from SC133 | ~184px right (164px base + ~20px Add to Playlist Jan 2026), 324px bottom, 130px top, 60px left — effective safe area 836×1466px |

**SC305 update (2026-08-29):** Post-production topic (pass 42). **All tools confirmed unchanged.** FFmpeg 9.0.1 (2026-08-12) remains current stable — no 9.0.2 as of Aug 29. SVT-AV1 v4.2.0 (2026-07-13) unchanged — no v4.3 found (GitLab releases confirmed). Remotion v4.0.518 (2026-08-26) unchanged — npm confirms last published 3 days ago. PySceneDetect v0.7.1 unchanged. rife-ncnn-vulkan CLI v20250112 unchanged. **whisper.cpp: v1.9.3 CONFIRMED still pre-release as of 2026-08-29** (GitHub releases page: v1.9.2 = latest stable; v1.9.3 = pre-release with security fixes + GGML 0.19→0.20.2 performance updates but no word-timestamp changes — consistent with SC301 finding). Stay on v1.9.2 for production. **Section 6 corrected:** FFmpeg version reference in §6 body updated from stale "Current stable: 8.1.1" to "9.0.1 'Lei'" (SC305).

**SC298 update (2026-08-27):** **Remotion advanced to v4.0.518 (2026-08-26)** — three releases since SC291. (1) **v4.0.516 (Aug 24):** Studio-only (rulers/guides toolbar, local asset drag-and-drop onto canvas, agent context from inspector, timeline auto-scroll) — no new `@remotion/effects`, no pipeline impact. (2) **v4.0.517 (Aug 25):** New `@remotion/gsap` package integrates GSAP (GreenSock Animation Platform) for complex declarative animations — low priority for current moving ads but available for branded motion graphics. `fisheye()` behavior fix: pixels outside the fisheye radius are now preserved instead of clipped (no impact for our pipeline — we do not use fisheye). Security dep updates (fast-xml-parser CVE-2026-25896, loader-utils CVE-2022-37601, protobufjs CVE-2026-41242, websocket-driver CVE-2026-54466) — update `remotion` dep if running Studio. (3) **v4.0.518 (Aug 26):** **`@remotion/whisper-webgpu` new package** — browser/WebGPU-accelerated Whisper transcription. **NOT applicable to our server-side pipeline** (we use `whisper.cpp` CLI via `@remotion/install-whisper-cpp` for word-level timestamps); this package is for browser-embedded transcription only. **`@remotion/captions` adds forced page breaks** — explicit control over caption page splits, useful when `createTikTokStyleCaptions()` auto-pagination produces bad breaks mid-sentence in Dutch voiceover. Use this when a caption page break lands in an awkward semantic position. Studio adds Social Safe Zones overlay (visual guide — no render impact) and audio visualization elements (mirrored audio spectrum, audio oscilloscope — not relevant to our halal audio pipeline). **No new `@remotion/effects` in any of v4.0.516–518.** **All other tools confirmed unchanged (Aug 27 check):** FFmpeg 9.0.1 (no 9.0.2), SVT-AV1 v4.2.0 (no v4.3), rife-ncnn-vulkan CLI v20250112 (no new binary), PySceneDetect v0.7.1 (no v0.7.2), Practical-RIFE v4.26 (no v4.27, v4.25 remains pipeline default for diffusion video).

**SC291 update (2026-08-23):** All post-production tools confirmed unchanged (pass 40 recheck, 1 day since SC284). **Remotion v4.0.515 still current** — no v4.0.516 published in 24h since SC284; GitHub releases page confirms 515 as latest. Remotion v5.0 still NOT released (no date announced). **FFmpeg 9.0.1 still current** — no 9.0.2. **SVT-AV1 v4.2.0 still current** — no v4.3. **rife-ncnn-vulkan CLI v20250112 still current** — no new binary (confirmed GitHub releases: most recent is 20250112, Jan 2025). **Practical-RIFE v4.26 still latest** — no v4.27 (confirmed GitHub; v4.25 remains pipeline default for diffusion video). **PySceneDetect v0.7.1 still current** — no v0.7.2 (confirmed GitHub releases page). **FFmpeg 9.0 new filter inventory (SC291 — not previously documented):** Two new audio filters confirmed in 9.0 — `afreqshift` (frequency shift) and `asoftclip` (audio soft clip) — both are music/production effects with no role in video post-production pipeline; do NOT use in loudnorm/mixing chain. New video filters: `v360_vulkan` (360° projection remapping via GPU compute shaders — not relevant, no 360° content), `vf_frc_amf` (AMD AMF hardware frame rate interpolation — AMD GPU only; RIFE via rife-ncnn-vulkan is preferred for our cloud pipeline), `transpose_cuda` (CUDA GPU transpose — NVIDIA only; existing `transpose` filter sufficient). None of these change existing pipeline commands. **SVT-AV1 `--tune-vmaf` via libsvtav1 FFmpeg plugin status:** Confirmed still NOT exposed (SC291 recheck) — `tune=0` (VQ) via `-svtav1-params tune=0` remains the correct perceptual quality mode; the standalone `SvtAv1EncApp --tune-vmaf` flag is for binary-only use outside FFmpeg.

**SC284 update (2026-08-22):** **Remotion advanced to v4.0.515 (2026-08-21).** Two releases since SC277. (1) **v4.0.514 (2026-08-20, already documented in captions-and-titles.md SC280):** `@remotion/captions` — `silenceGapMs` parameter added to `createTikTokStyleCaptions()`, caption pagination edge-case fixes; Mediabunny upgraded to 1.55.1; no new `@remotion/effects`. (2) **v4.0.515 (2026-08-21):** **`outline()` added to `@remotion/effects`** (§11p — WebGL2 stroke/border effect around alpha channel; params: `width` default 8px, `color` default #ffffff, `opacity` default 1, `edgeSimplification` default 0, `outlineOnly` default false); `@remotion/captions` now exports ESM modules; backpressure applied during frame encoding (prevents buffer overflow on long renders); Lambda streams render chunks to disk instead of buffering in memory (lower peak memory for Lambda renders); video looping: silent tails now preserved, deadlock fix when loops begin with silence; SVG gradient strokes preserved during rendering; Lambda render cancellation support added. **All other tools confirmed unchanged (2026-08-22 check):** FFmpeg 9.0.1 (no 9.0.2), SVT-AV1 v4.2.0 (no v4.3), rife-ncnn-vulkan CLI v20250112 (no new binary), PySceneDetect v0.7.1 stable (no v0.7.2), Practical-RIFE v4.26 (no v4.27).

**SC277 update (2026-08-20):** **Remotion advanced to v4.0.513 (2026-08-18).** Three changes: (1) **`tile()` added to `@remotion/effects`** — WebGL2 effect that creates a repeated tile pattern from its child composition. Full parameters documented in new §11o. Pipeline relevance: title card pattern backgrounds, repeating brand-asset texture treatments — never on character or truck shots. (2) **`@remotion/mac-cursors` new package** — renders macOS-style animated cursor graphics; useful for screen recording/tutorial content. **Pipeline relevance for Snelverhuizen: none** — no screen recording in moving-ad briefs. Document only for future reference. (3) **`@remotion/media` audio sample-rate conversion fix** — compositions that mix audio files at different sample rates (e.g., a voiceover at 44100 Hz + SFX at 22050 Hz) previously produced distorted or sped-up audio; now correctly resampled to 48000 Hz inside the Remotion compositor. **Pipeline action:** If any Remotion composition mixes audio sources with different sample rates, upgrade to ≥ v4.0.513 and test playback. Our standard pipeline encodes all audio at 48000 Hz via system FFmpeg, so this fix only matters for audio embedded in Remotion `<Audio>` components. **All other tools confirmed unchanged (Aug 20 check):** FFmpeg 9.0.1 (no 9.0.2 or 9.1), SVT-AV1 v4.2.0 (no v4.3), rife-ncnn-vulkan CLI v20250112 (no new binary; AUR package confirms 20250112 is current), PySceneDetect v0.7.1 stable (no v0.7.2), Practical-RIFE v4.26 (no v4.27).

**SC270 update (2026-08-18):** **SC263 PARTIAL CORRECTION — v4.0.510 added `@remotion/elements` data visualization package (missed in SC263).** SC263 stated "v4.0.510 Studio enhancements only — no new effects" — correct for `@remotion/effects`, but missed the new `@remotion/elements` package. GitHub release notes for v4.0.510 confirm: animated line chart, vertical bar chart, animated pie chart, spinning text wheel, and product discount callout components added. These are separate from `@remotion/effects` (visual filter effects) — standalone composable chart/UI elements. Exact npm package name not confirmable via available sources (remotion.dev blocked, no package.json found) — verify with `npm view @remotion/elements version` before use. **Pipeline relevance: LOW for current ads (no data viz in current briefs), but product discount callout potentially useful for promotional price-comparison moving ads.** **All other tools confirmed unchanged (Aug 18 check):** FFmpeg 9.0.1 (no 9.0.2), SVT-AV1 v4.2.0 (no v4.3), rife-ncnn-vulkan CLI v20250112 (no new binary), PySceneDetect v0.7.1 stable (no v0.7.2), Practical-RIFE v4.26 (no v4.27, no GitHub releases page — models in repo as code).

**SC263 update (2026-08-16):** **SC256 CORRECTION — Remotion @remotion/effects additions in v4.0.507–509 were missed.** SC256 stated "no new `@remotion/effects` additions in v4.0.501–509" — this was INCORRECT. GitHub release history confirms: v4.0.507 (Aug 7) added `regionblur()`; v4.0.508 (Aug 11) added `exposure()`, `whiteBalance()`, `vibrance()`, `levels()`, `shadowsHighlights()`; v4.0.509 (Aug 12) added `colorCorrection()`. Seven new color correction / selective blur effects, all with full parameters confirmed from source. All documented in §11n. **Current Remotion: v4.0.512 (Aug 14, 2026).** v4.0.510 added Studio enhancements (easing icons) but no new @remotion/effects. v4.0.511 fixed an interactivity regression from v4.0.510. v4.0.512 was a npm republish of v4.0.511 to fix staging delays — no code changes. **All other tools unchanged:** FFmpeg 9.0.1 current (no 9.0.2), SVT-AV1 v4.2.0 (no v4.3), rife-ncnn-vulkan CLI v20250112 (no new binary), PySceneDetect v0.7.1 stable (no v0.7.2), Practical-RIFE v4.26 (no v4.27).

**SC256 update (2026-08-14):** Two substantive changes this cycle. (1) **FFmpeg 9.0 "Lei" released 2026-08-04 — major version bump.** Patch 9.0.1 released 2026-08-12 (current stable). Named in tribute to Lei Xiaohua. **Pipeline impact for CLI users: minimal.** All existing FFmpeg filter commands (drawvg, h264_metadata BSF, loudnorm, zscale, hqdn3d, normalize, lut3d, haldclut, eq, libsvtav1, libvmaf, whisper, scdet) remain valid — 9.0 does not break filter syntax. Key behavioral change: **`tls_verify` defaults to 1** — HTTPS certificate verification is now ON by default. Previous 8.x behavior was to skip cert verification. For our pipeline, AIMLAPI CDN URLs are on CA-signed certs so no issue expected. If any `ffmpeg -i <https_url>` call starts failing with "certificate verify failed" after upgrading to 9.0, treat it as a CDN cert problem, not a reason to add `-tls_verify 0`. Library version bumps (libavcodec → 63.x series) are C API-level only — no impact on our shell-command pipeline. New 9.0 additions not currently used by our pipeline: native animated WebP decode, ONNX Runtime DNN GPU inference backend, `v360_vulkan` filter, Vulkan acceleration for APV codec. Upgrade path: replace `ffmpeg 8.1.2` with `ffmpeg 9.0.1` on pipeline machines; run `ffmpeg -version` to confirm; all existing FFmpeg commands can be re-run unchanged. (2) **Remotion: v4.0.500 changes: `remotion` re-checks audio resume success before reporting failure; `@remotion/player` adds `_experimentalKeepAudioContextAlive` prop; Studio adds copy-properties-between-components and GitHub.com "Open in" menu.** ⚠️ Note: SC256 incorrectly stated "no new @remotion/effects in v4.0.501–509" — see SC263 correction above. **All other tools unchanged:** SVT-AV1 v4.2.0 (no new release), rife-ncnn-vulkan CLI v20250112 (no new binary), PySceneDetect v0.7.1 stable (no new release), Practical-RIFE v4.26 (no v4.27).

**SC249 update (2026-07-25):** Remotion advanced to **v4.0.499** (July 24, 2026) — two releases since SC242. (1) **v4.0.498 (July 23):** No new `@remotion/effects`. `getVideoMetadata()` deprecated — if any pipeline script calls `getVideoMetadata()`, migrate before upgrading to v4.0.498. v5 preparation: ANGLE+SwiftShader fallback is now the default v5 renderer setting; Node.js and ESLint minimum requirements raised for v5 compatibility; Webpack and Rspack config overrides are now separate APIs; buffering defaults enabled for v5. Improved handling of long variable-duration frames in media playback. Studio: batch easing changes for keyframes, dynamic config option updates, license configuration in Studio. (2) **v4.0.499 (July 24):** No new `@remotion/effects`. **Opacity leaking between layers in web-renderer fixed** — upgrade to ≥ v4.0.499 if any Remotion composition stacks multiple layers with non-100% opacity (e.g., caption overlays over brand layers, badge compositions). Zod upgraded to 4.4.3 (no pipeline-visible change). New `@remotion/drag-and-drop` package adds drag-and-drop payload support + Studio "Install in Studio interface" — no pipeline impact. Studio: sidebar clamping, visibility toggle debounce, text input for InputDragger, ruler full-canvas span. **All other tools unchanged:** FFmpeg 8.1.2 (no 8.2 release), SVT-AV1 v4.2.0 (confirmed on GitLab — SC221 was correct), Practical-RIFE v4.26 (no v4.27), rife-ncnn-vulkan CLI v20250112, PySceneDetect v0.7.1 stable.

**SC242 update (2026-07-23):** Three changes this cycle. (1) **PySceneDetect v0.7.1 released 2026-07-21 — now stable.** Previously documented as "in development." All v0.7.1 features confirmed: `--expand` flag for `split-video` (extend clips to video boundaries — use in all pipeline scene detection commands going forward), `backend` kwarg for `detect()`, `expand_scenes_to_bounds()` helper. NEW additions not previously documented: `VideoStreamConcat` for multi-clip unified detection, `VideoStream.decode_failures` property for corruption flagging, PyAV corrupt-frame tolerance (8 frames — more robust on AI-generated clips), PyAV PTS normalization (fixes delayed-start file bugs), VFR FrameTimecode PTS-based comparison. Full details in §3d. PySceneDetect v0.7.1 Windows release bundles FFmpeg 8.1.2 — this independently **confirms FFmpeg 8.1.2 is still the current stable** (see note below). (2) **Remotion v4.0.496–497 released.** v4.0.496 (July 21): Studio-only, no pipeline impact. v4.0.497 (July 23, today): Direct premounting for `<Img>`, `<AnimatedImage>`, `<CanvasImage>`, `<Gif>` (frame-accurate preload); animated image decoder race condition fix; AudioContext audio-tag stability fix; no new @remotion/effects. (3) **FFmpeg 9.0 claim in halal-audio.md (SC239) is INCORRECT.** GitHub tag history confirms no n9.x FFmpeg release exists as of 2026-07-23. Latest stable is **n8.1.2 (June 17, 2026)**, independently confirmed by PySceneDetect v0.7.1 bundling FFmpeg 8.1.2. The "FFmpeg 9.0 confirmed stable" note in halal-audio.md is a research error and has been corrected in that skill file. Post-production pipeline commands are unaffected — all FFmpeg 8.1.x commands remain valid.

**SC235 update (2026-07-21):** **Remotion advanced to v4.0.495 (released 2026-07-20).** Four releases since SC228 (v4.0.491). (1) **v4.0.492:** `muted` prop added to `<Video>` schema — use `muted` on embedded video clips to silence source audio when layering independent SFX/voiceover in Remotion compositions; negative video offset support in `<Sequence>` containers (allows offsetting a clip start time behind frame 0 for pre-roll/crossfade effects). (2) **v4.0.493:** Studio-only (composition inspector metadata editing, keyframe copy/paste, single-node drag) — no pipeline impact. (3) **v4.0.494:** **Sequence opacity preservation fix** — prior bug where `<Sequence>` opacity did not correctly persist while the sequence was active; now fixed. **Pipeline impact:** If any caption overlay or branded layer composition uses `opacity` on a `<Sequence>` wrapper for fade-in/fade-out, upgrade to ≥ v4.0.494. AnimatedImage component now supports WebP animated files (auto-inserted by Studio; can be used for simple animated brand elements). (4) **v4.0.495:** Studio improvements (Figma paste, SVG drag-and-drop, composition inspector) — no pipeline impact. **Previously undocumented effects** confirmed in package: `wave()` (sine-wave distortion) and `noiseDisplacement()` (localized noise-based pixel displacement) — documented in new §11m below. **All other tools unchanged:** FFmpeg 8.1.2, SVT-AV1 v4.2.0, rife-ncnn-vulkan v20250112, PySceneDetect v0.7.0 stable (v0.7.1.dev0 pre-release, not stable).

**SC228 update (2026-07-19):** **Remotion v4.0.491 released 2026-07-18.** Three pipeline-relevant changes: (1) Two new `@remotion/effects` additions — `liquidContours()` (WebGL2 procedural organic/fluid contour pattern; see §11l) and `skew()` (perspective skew transform; see §11l). (2) `@remotion/media` marked **stable** — was previously experimental/alpha; our pipeline was already using it as the recommended path, no code change needed. (3) **Remotion's bundled FFmpeg binary removes `--enable-nonfree`** — drops `libfdk_aac` AAC encoder from Remotion's own compositor binary. **Pipeline impact: zero** — our pipeline uses system FFmpeg (CLI), not Remotion's bundled binary, for all audio encoding. We use the built-in `aac` encoder (`-c:a aac`), which does not require `--enable-nonfree`. If any Remotion composition outputs audio via Remotion's compositor (not our FFmpeg post-step), it was already using the built-in aac encoder anyway. No action required. All other tools unchanged: FFmpeg 8.1.2, SVT-AV1 v4.2.0, rife-ncnn-vulkan v20250112, PySceneDetect v0.7.0 stable (v0.7.1 still in dev).

**SC221 update (2026-07-17):** Two substantive changes this cycle. (1) **SVT-AV1 v4.2.0 released 2026-07-13** — new `--tune-vmaf` flag targeting ~15% VMAF BD-rate improvement for VOD/archive encodes; CBR Kalman-filter rate control added (RTC/low-latency use); ARM NEON forward-transform kernels + SVE2 VMAF kernels. Our pipeline commands in §5h are unchanged — `-svtav1-params tune=0` (VQ/perceptual) remains the correct archive setting. The `--tune-vmaf` flag is not exposed via `libsvtav1` FFmpeg plugin as of this writing — relevant when using the standalone `SvtAv1EncApp` binary, not our FFmpeg-based pipeline. (2) **Remotion v4.0.490 released 2026-07-16** — new `linearProgressivePixelate()` effect in `@remotion/effects` (pixelation intensity gradient, analogous to `linearProgressiveBlur()` but for pixelation — see §11k); new `@remotion/rough-notation` package (sketch/handdrawn annotation overlays, wraps the rough-notation library); `interpolate()` gains `output: "perceptual-scale"` for Studio keyframes (no pipeline impact for code-driven renders). All other tools unchanged: FFmpeg 8.1.2, rife-ncnn-vulkan 20250112, PySceneDetect v0.7.0 stable (v0.7.1-dev0 pre-release from Jul 6 — not a stable release), Practical-RIFE v4.26 (v4.26.heavy not found in upstream hzwer README — supported by TNTwise binary only).

**SC214 update (2026-07-15):** All tool versions confirmed unchanged. No FFmpeg 8.1.3, no SVT-AV1 v4.2, no Practical-RIFE v4.27, no rife-ncnn-vulkan CLI newer than v20250112, no PySceneDetect v0.7.1 stable (still in dev). Remotion remains at v4.0.489. **SC140 documentation gap corrected:** v4.0.479 (Jun 17, 2026) also added `thermalVision()`, `pixelate()`, `shrinkwrap()`, and `burlap()` to @remotion/effects — these were omitted from SC140's notes. Documented in §11i below. **@remotion/effects library scope corrected:** The package has shipped 50+ effects since its launch at v4.0.465 (May 22, 2026). Effects added in v4.0.465–478 (May–June 2026) were never documented in this skill — the most pipeline-relevant are `glow()` and `duotone()`. Documented in §11j below.

**SC207 update (2026-07-13):** Remotion advanced to **v4.0.489** (released 2026-07-12) — studio-only patch (runtime config, element install-target request, file-source origin security fix); no effects, codec, or pipeline-relevant changes. **TNTwise REAL Video Enhancer GUI repo (`TNTwise/REAL-Video-Enhancer`) ARCHIVED 2026-07-13 by owner — read-only, no further development.** Pipeline impact: none for headless use — the `rife-ncnn-vulkan` CLI binary repo (`TNTwise/rife-ncnn-vulkan`, v20250112) is a separate repository and is NOT archived. All pipeline interpolation work continues via CLI (§3b). No other tool changes: FFmpeg 8.1.2 unchanged, PySceneDetect v0.7.1 still in dev (not released), SVT-AV1 v4.1.0 unchanged, Practical-RIFE v4.26 unchanged (v4.25 remains pipeline default for diffusion video).

**SC200 update (2026-07-11):** Remotion advanced to **v4.0.488** (released today). No new `@remotion/effects` additions. Key changes: (1) `@remotion/media` — looped audio dropout after multiple iterations now fixed — relevant if any Remotion composition loops ambient SFX; (2) Mediabunny upgraded to 1.50.8; (3) `@remotion/lambda` gains S3 output provider CLI option; (4) Studio: security hardening — origin-less requests now rejected. Four previously-undocumented `@remotion/effects` from v4.0.481 now documented in §11h: `checkerboard()`, `emboss()`, `gridlines()`, `zoomBlur()` plus a vignette fix. **v5.0 license change noted:** Automators-tier v5 will require mandatory telemetry via `licenseKey`; Creators tier keeps it optional. No release date for v5.0 announced — see §11b. All other tools unchanged: no FFmpeg 8.1.3, no SVT-AV1 v4.2, no Practical-RIFE v4.27, no RVE v2.4.2 stable, PySceneDetect v0.7.1 still in dev.

**SC195 update (2026-07-10):** Remotion advanced to v4.0.487 (released July 9). Two new `@remotion/effects` additions: `paper()` (v4.0.486, July 7 — WebGL2 procedural paper texture, `seed` parameter for randomization; see §11g) and `roughenEdges()` (v4.0.487 — WebGL2 noise-driven edge roughening, params: `border` default 26.5, `scale` default 0.07, `seed` default 231.2; see §11g). Also in v4.0.486: `@remotion/paths` adds `centerPath()` utility. ProRes support added to `@remotion/media` (Mediabunny 1.50.7). `@remotion/web-renderer` gains page responsiveness option. **TNTwise REAL Video Enhancer v2-main branch is "under a massive refactor" — current stable (v2.4.1) will not be updated for a while; see §3a note.** All other tools unchanged: no FFmpeg 8.1.3, no SVT-AV1 v4.2, no Practical-RIFE v4.27, no RVE v2.4.2 stable, PySceneDetect v0.7.1 still in dev.

**SC189 update (2026-07-06):** Remotion advanced to v4.0.485 (released today). New `venetianBlinds()` effect added to `@remotion/effects` — see §11f. Bug fixes: media playbackRate duration in loops corrected; preview frame accuracy improved; `@remotion/web-renderer` gains dotted/dashed/double text-decoration styles. PySceneDetect 0.7.1.dev0 uploaded to PyPI today — still not a stable release (noted in §3d). All other tools unchanged: no FFmpeg 8.1.3, no SVT-AV1 v4.2, no Practical-RIFE v4.27, no RVE v2.4.2 stable.

**SC182 update (2026-07-04):** All tool versions unchanged from SC175. No FFmpeg 8.1.3, no Remotion v4.0.485+, no PySceneDetect v0.7.1, no RVE v2.4.2 stable, no SVT-AV1 v4.2. Remotion v5.0 still not released. New additions this cycle: (1) `rife-v4.25.heavy` documented in §3a as a supported middle-tier model (TNTwise binary v20250112 bundles it since Oct 2024 release — was omitted from prior docs); (2) CVE-2026-8461 (PixelSmash) security note added to FFmpeg row — fixed in 8.1.2, our pipeline already patched.

**SC175 update (2026-07-03):** All tool versions unchanged from SC168. No FFmpeg 8.1.3, no Remotion v4.0.485+, no SVT-AV1 v4.2, no Practical-RIFE v4.27, no RVE v2.4.2 stable, no PySceneDetect v0.7.1. Remotion v5.0 confirmed NOT yet released — migration docs live at `remotion.dev/docs/5-0-migration` but no release date announced. Minor date correction: Remotion v4.0.484 was released 2026-06-26 (not ~2026-06-29 as previously noted). FFmpeg 6.1.6 and 7.0.3 received maintenance patches on older branches — not relevant to our 8.1.x pipeline.

**SC168 update (2026-06-30):** Remotion advanced to v4.0.484. New `linearGradient()` added to `@remotion/effects` (WebGL2 linear color gradient overlay — see §11d). NVENC H.264/H.265 hardware encoding confirmed for Linux/Windows via `hardwareAcceleration` option in `renderMedia()` — use `videoBitrate` instead of CRF when enabling. All other tools unchanged: no FFmpeg 8.1.3, no Practical-RIFE v4.27, no RVE v2.4.2 stable, no PySceneDetect v0.7.1, no SVT-AV1 v4.2.

**SC154 → SC161 updates:** Remotion advanced from v4.0.481 to v4.0.483 across two releases. v4.0.482 (June 22) added `cornerPin()` and `lightTrail()` to `@remotion/effects`. v4.0.483 (June 28, today) added `radialProgressiveBlur()` and spring easing tail support, and fixed an audio-freeze bug during scrubbing. All other tools unchanged.

**SC133 correction (2026-06-16):** TikTok right dead zone updated to ~184px (from ~180px) — prior estimate of +16px for Add to Playlist was wrong; multiple 2026 sources confirm +20px expansion. Effective safe content area corrected from "~900 × 1466px" to "~836 × 1466px" (1080 − 60 − 184 = 836px). The "900px" figure was a carry-over error from before the right-column expansion — it only held when right margin was 120px (matching Instagram), which TikTok never was.

**SC140 confirmation (2026-06-18):** Remotion updated to v4.0.479 (released June 17, 2026). All other tool versions unchanged. TikTok/Instagram safe zones confirmed unchanged. TNTwise rife-ncnn-vulkan CLI binary confirmed at v20250112 (Jan 2025) supporting models through v4.26.

**SC147 update (2026-06-20):** FFmpeg updated to 8.1.2 (released June 17, 2026 — maintenance patch, no pipeline filter changes). Remotion updated to v4.0.481 (released June 18, 2026 — new visual effects, no caption/text pipeline impact). Instagram 320px bottom safe zone re-confirmed by multiple independent 2026 sources (no change). All other tools confirmed unchanged.

**SC154 confirmation (2026-06-22):** All tool versions unchanged. No FFmpeg 8.1.3, no Practical-RIFE v4.27, no RVE v2.4.2 stable, no PySceneDetect v0.7.1, no SVT-AV1 v4.2. Remotion confirmed at v4.0.481 as most recent stable (published 3 days ago). New `@remotion/effects` entries documented (§11a). Remotion v5 forward-warning documented (§11b).

---

### 11a. `@remotion/effects` — Progressive Blur Effects (v4.0.481–483)

Three blur/key effects are now available in `@remotion/effects`. Install once:
```bash
npm install @remotion/effects
```

---

**`linearProgressiveBlur()`** (since v4.0.481) — gradient-controlled linear blur. Applies variable blur in one direction, strongest at one edge, tapering to zero. Practical use: blur the bottom of a frame behind the caption row to improve text readability on light backgrounds. Our orange #FC8434 highlight captions usually sit on dark backgrounds, but a progressive blur underneath is a clean fallback.

```tsx
import { linearProgressiveBlur } from "@remotion/effects";

// blur increases from 0 at y=1400 (above captions) to 8px at bottom edge
<AbsoluteFill style={{
  filter: linearProgressiveBlur({
    direction: "to bottom",
    blurAmountAtEnd: 8,
    from: 1400 / 1920,  // fraction of frame height where blur starts
    to: 1,              // bottom edge
  }),
}} />
```

---

**`radialProgressiveBlur()`** (added v4.0.483, 2026-06-28) — ellipse-controlled blur. Applies blur radially outward from a center point, sharpest at center and softest at the ellipse boundary. Backend: WebGL2.

Parameters:
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `center` | `[number, number]` | `[0.5, 0.5]` | UV coordinate (0–1 range); `[0.5, 0.5]` = frame center |
| `width` | `number` | `1` | Ellipse width (UV scale) |
| `height` | `number` | `1` | Ellipse height (UV scale) |
| `rotation` | `number` | `0` | Degrees |
| `start` | `number` | `0` | Where sharp zone ends (0 = starts at center) |
| `startBlur` | `number` | `0` | Blur amount at `start` edge (px) |
| `endBlur` | `number` | `50` | Blur amount at ellipse boundary (px) |

**Practical uses for Snelverhuizen:**
- **Cinematic DOF vignette on character close-ups:** center on face, endBlur=20–30px. Draws eye to subject while softening background edges.
- **Spotlight/focus pull:** combine with a character shot where background is white/neutral wall — looks like professional rack-focus.
- **Caption background softening:** center=[0.5, 0.8], height=0.4, endBlur=15 blurs the lower-third behind captions without visible hard line.

```tsx
import { radialProgressiveBlur } from "@remotion/effects";

// Cinematic vignette — face sharp, edges blur to 25px
<AbsoluteFill style={{
  filter: radialProgressiveBlur({
    center: [0.5, 0.4],  // slightly above center where face appears
    width: 0.7,
    height: 0.9,
    startBlur: 0,
    endBlur: 25,
  }),
}} />
```

**Note:** Requires WebGL2 in the render environment. The Remotion renderer supports WebGL2 — no extra config needed.

---

**`colorKey()`** (since v4.0.481) — removes a chroma key color (green screen). Not applicable to our current pipeline (no green screen shoots). Document only for future reference if client ever provides keyed footage.

---

**When to use linear vs radial progressive blur:**
- `linearProgressiveBlur`: directional (top→bottom, left→right) — best for caption bars and edge vignettes
- `radialProgressiveBlur`: elliptical spotlight — best for subject focus and character close-ups

---

### 11b. Remotion v5.0 — Forward-Compatibility Warning (Not Yet Released)

Remotion v5.0 migration docs are live at `remotion.dev/docs/5-0-migration` but v5.0 has NOT been released as of 2026-06-22. Document the upcoming breaking changes now so upgrade prep is clear:

| Breaking change | v4 behavior | v5 behavior | Impact on our pipeline |
|----------------|-------------|-------------|----------------------|
| `<Audio>` `optimizeFor` default | `"accuracy"` | `"speed"` | LOW — our pipeline uses FFmpeg, not Remotion's `<Audio>`, for audio mixing. If any Remotion composition includes `<Audio>`, add explicit `optimizeFor="accuracy"` before upgrading. |
| `inputProps` in `selectComposition()` / `getCompositions()` | Optional | Required | LOW — if any script calls these without `inputProps`, pass `{}` after upgrading. |
| Node.js minimum | varies | **18.0.0** | Verify server Node version before upgrading. |
| Bun minimum | varies | **1.1.3** | Only relevant if running Remotion via Bun. |

**Action required before upgrading to v5 (when released):**
1. Audit all Remotion compositions for `<Audio>` components — add explicit `optimizeFor="accuracy"` if audio sync precision matters
2. Audit scripts calling `selectComposition()` / `getCompositions()` — add `inputProps: {}` argument
3. Confirm server runs Node.js ≥ 18.0.0

**v5.0 license change (SC200 — confirmed 2026-07-11):** v5.0 will require mandatory telemetry via a `licenseKey` for the **Automators tier** (programmatic/server-side rendering). The **Creators tier** (GUI/template use) keeps telemetry optional. An Enterprise License will allow opting out of telemetry in exchange for monthly usage reports. Our pipeline uses Remotion programmatically (server-side caption/overlay rendering) — when v5.0 ships, obtain a licenseKey before upgrading. No action needed now.

**No action needed now** — v5 is not released and no date announced. Monitor `remotion.dev/changelog` for release announcement.

---

### 11c. `@remotion/effects` — `cornerPin` and `lightTrail` (v4.0.482)

**`cornerPin()`** (added v4.0.482, 2026-06-22) — WebGL2 perspective transform. Remaps the four corners of a composition to new UV coordinates, enabling perspective-correct overlays on non-flat surfaces.

Parameters — all UV coordinates in 0–1 range (0 = left/top edge, 1 = right/bottom edge):
| Parameter | Default | Notes |
|-----------|---------|-------|
| `topLeft` | `[0, 0]` | Top-left corner destination |
| `topRight` | `[1, 0]` | Top-right corner destination |
| `bottomRight` | `[1, 1]` | Bottom-right corner destination |
| `bottomLeft` | `[0, 1]` | Bottom-left corner destination |

**Snelverhuizen pipeline use case:** Overlay the SNELVERHUIZEN.NL URL or phone number onto the truck side in perspective, tracking the surface across frames. Advanced use — requires manually measuring the four corner UV positions per shot. For standard flat-plane overlays (caption bars, bottom-of-frame badges), `drawvg` + `drawtext` (§10) is simpler and does not require Remotion.

```tsx
import { cornerPin } from "@remotion/effects";

// Example: pin a logo layer to a truck side panel in perspective
// UV coords measured from the clip frame for each corner of the panel
<AbsoluteFill style={{
  filter: cornerPin({
    topLeft:     [0.12, 0.30],
    topRight:    [0.85, 0.25],
    bottomRight: [0.88, 0.72],
    bottomLeft:  [0.10, 0.75],
  }),
}}>
  <Img src={logoAsset} style={{ width: "100%", height: "100%" }} />
</AbsoluteFill>
```

**`lightTrail()`** (added v4.0.482) — motion-based light streak animation. Decorative effect for transitions or logo reveals. Not part of the standard ad pipeline — document for future branded motion-graphics use only.

---

### 11d. `@remotion/effects` — `linearGradient()` (v4.0.484)

**`linearGradient()`** (added v4.0.484, ~2026-06-29) — WebGL2-rendered linear color gradient overlay. Covers the entire frame with a smooth gradient from `startColor` to `endColor` between two UV points. Different from `linearProgressiveBlur()` (which blurs pixels) — this draws a color gradient layer.

Parameters:
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `start` | `[number, number]` | `[0, 0.5]` | UV coordinate where `startColor` is full-strength (0–1 range) |
| `end` | `[number, number]` | `[1, 0.5]` | UV coordinate where `endColor` is full-strength (0–1 range) |
| `startColor` | `string` | `'#000000'` | Hex color at `start` position |
| `endColor` | `string` | `'#ffffff'` | Hex color at `end` position |

UV coordinates: `[0, 0]` = top-left, `[1, 1]` = bottom-right, `[0.5, 0]` = top-center, `[0.5, 1]` = bottom-center.

**Practical uses for Snelverhuizen:**

**1. Dark scrim behind captions (most common use):** Overlay a transparent-to-black gradient in the lower third so caption text reads on any background without a hard box.
```tsx
import { linearGradient } from "@remotion/effects";

// transparent at y=0.6 (60% down frame), fades to semi-black at bottom
<AbsoluteFill style={{
  filter: linearGradient({
    start: [0.5, 0.65],
    end:   [0.5, 1.0],
    startColor: '#00000000',  // transparent black
    endColor:   '#000000CC',  // ~80% black
  }),
}} />
```

**2. Brand orange gradient accent (bottom corner):**
```tsx
// Subtle #FC8434 sweep from bottom-left to transparent — brand touch on reveal frame
<AbsoluteFill style={{
  filter: linearGradient({
    start: [0, 1],
    end:   [0.5, 0.7],
    startColor: '#FC843488',  // #FC8434 at 53% alpha
    endColor:   '#FC843400',  // fully transparent
  }),
}} />
```

**Note:** Requires WebGL2. The Remotion renderer supports WebGL2 — no extra config needed.

**When to use `linearGradient` vs alternatives:**
- `linearGradient()` — full-frame color gradient overlay (WebGL2). Best for dark scrims and brand color washes.
- `linearProgressiveBlur()` — directional blur (no color change). Best for blurring background behind text.
- CSS `background: linear-gradient(...)` on a `<div>` — simpler, no WebGL2, but cannot be used as a `filter`. Use for background fills within a div.

---

### 11e. Remotion NVENC Hardware Encoding (v4.0.484, Linux/Windows)

Remotion v4.0.484 confirmed NVENC H.264/H.265 hardware encoding support on Linux/Windows via the `hardwareAcceleration` parameter in `renderMedia()`.

**Key constraints (different from FFmpeg NVENC):**
- **CRF is NOT available** when `hardwareAcceleration` is enabled — Remotion removes this option automatically.
- Use `videoBitrate` to control file size: `--video-bitrate=8M` produces similar output size to software encode at CRF 18.
- Speed improvement: approximately 3–5× faster render than software encode.

**When to use Remotion NVENC vs FFmpeg NVENC (§8a):**
- Use **FFmpeg NVENC** (§8a) when encoding pre-assembled video files (post-production encode step).
- Use **Remotion NVENC** when rendering Remotion compositions directly (caption overlays, branded sequences) — avoids the FFmpeg post-step.
- Both target NVIDIA GPU; VAAPI (§8b) remains the Linux AMD/Intel alternative.

**CLI usage:**
```bash
npx remotion render MyComp out.mp4 --hardware-acceleration=if-possible --video-bitrate=8M
```

**`renderMedia()` API:**
```typescript
await renderMedia({
  composition,
  serveUrl,
  codec: 'h264',
  outputLocation: 'out.mp4',
  hardwareAcceleration: 'if-possible',  // 'disable' | 'if-possible' | 'required'
  videoBitrate: '8M',
  // Do NOT set crf when hardwareAcceleration is enabled
});
```

`hardwareAcceleration: 'if-possible'` falls back to software encode gracefully if no NVIDIA GPU is detected — safe default for our pipeline environment.

---

### 11g. `@remotion/effects` — `paper()` and `roughenEdges()` (v4.0.486–487)

**`paper()`** (added v4.0.486, 2026-07-07) — WebGL2 procedural paper texture overlay. Renders a realistic fiber-paper grain on the frame using a shader adapted from Paper Shaders (open-source). Gives compositions an organic, handcrafted look.

```typescript
import { paper } from "@remotion/effects";

// Paper texture overlay on a title card
<AbsoluteFill style={{
  filter: paper({ seed: 42 }),
}} />
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `seed` | `number` | — | Randomization seed for reproducible texture. Different values = different paper grain patterns. |

**Snelverhuizen use case:** Subtle paper texture on the SNELVERHUIZEN.NL title card or end frame — adds artisanal, hand-crafted warmth without music. Useful at low opacity (wrap in a `<div>` with `opacity: 0.15–0.3`). Do NOT apply to character close-ups or truck shots — leave video frames clean.

---

**`roughenEdges()`** (added v4.0.487, 2026-07-09) — WebGL2 noise-driven edge roughening. Creates torn/ragged edges on a composition layer, like a hand-torn paper or worn graphic. Built on the same Paper Shaders noise helpers as `paper()`.

```typescript
import { roughenEdges } from "@remotion/effects";

// Roughen the edge of a brand badge overlay
<AbsoluteFill style={{
  filter: roughenEdges({ border: 20, scale: 0.08, seed: 100 }),
}} />
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `border` | `number` | 26.5 | Width of the roughened edge region (px). Lower = finer tear; higher = more dramatic. |
| `scale` | `number` | 0.07 | Noise frequency. Higher = tighter/smaller tears; lower = broader, rounder edge variation. |
| `seed` | `number` | 231.2 | Randomization seed for reproducible edge patterns. |

**Snelverhuizen use case:** Roughen edges of the orange #FC8434 pill badge for an organic look on a hero-frame title card. Also works as a stylized frame border for the arrival reveal shot. Use `border: 15–25` for subtle effect; `border: 40+` for dramatic torn look. Do NOT apply to character faces or any shot requiring clean edges.

**Note:** Both `paper()` and `roughenEdges()` require WebGL2 — same requirement as the other `@remotion/effects` effects. No extra config needed in Remotion renderer.

**When to use which texture effect:**
- `paper()` — flat texture across the whole layer (grain / film-stock feel)
- `roughenEdges()` — only affects the layer boundary (torn/worn edge look)

---

### 11f. `@remotion/effects` — `venetianBlinds()` (v4.0.485)

**`venetianBlinds()`** (added v4.0.485, 2026-07-06) — WebGL2 venetian-blinds reveal animation. Divides the frame into horizontal or vertical slats and reveals them progressively, like opening window blinds.

**API:**
```typescript
import { venetianBlinds } from "@remotion/effects";

type VenetianBlindsParams = {
  progress?: number;               // 0–1, how far the reveal has progressed; default 0.5
  direction?: 'vertical' | 'horizontal';  // slat orientation; default 'vertical'
  slats?: number;                  // number of divisions, 1–100; default 12
};
```

**Practical uses for Snelverhuizen:**
- **Truck reveal transition:** Horizontal blinds (direction `'horizontal'`) opening to reveal the truck side panel — matches a "curtain lifts" cinematic feel.
- **Scene transition between shots:** Drive `progress` from 0→1 over ~12 frames (0.4s at 30fps) for a snappy reveal cut.
- **Hero frame intro:** Reveal a family arrival shot with vertical slats at `slats: 8` for a bold, stylized look.

**Example — truck reveal opening (horizontal, 8 slats, 12-frame reveal):**
```tsx
import { venetianBlinds } from "@remotion/effects";
import { useCurrentFrame, interpolate, AbsoluteFill } from "remotion";

// Truck reveal: blinds open from frame 0 to frame 12
const frame = useCurrentFrame();
const progress = interpolate(frame, [0, 12], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});

<AbsoluteFill style={{
  filter: venetianBlinds({ progress, direction: 'horizontal', slats: 8 }),
}}>
  {/* truck shot here */}
</AbsoluteFill>
```

**Note:** Uses WebGL2 — same requirement as `radialProgressiveBlur()`, `cornerPin()`, and `linearGradient()`. Remotion renderer supports WebGL2 — no extra config needed. Pair with a `linearGradient()` dark scrim underneath for legible captions on a bright truck reveal.

---

### 11h. `@remotion/effects` — Previously Undocumented Effects (v4.0.481)

Four effects were added in v4.0.481 alongside `linearProgressiveBlur()` and `colorKey()` but were not previously documented in this skill file. Documented SC200 (2026-07-11).

**`zoomBlur()`** — radial motion blur simulating a rapid zoom or push-in. Most relevant to our pipeline: can be used for impact transitions or a quick truck-reveal punch-in.

```tsx
import { zoomBlur } from "@remotion/effects";

// Impact zoom blur on a truck reveal — drives from 0 to 1 over ~6 frames
<AbsoluteFill style={{
  filter: zoomBlur({ strength: 0.8 }),
}} />
```

**Snelverhuizen use case:** Apply at the cut point of a truck reveal — drive `strength` from ~0.8 to 0 over 6 frames (eases in, then sharpens) for a cinematic "camera slam" feel. Alternative: use in reverse as a scene exit (strength 0→0.6, then hard cut). Keep `strength` below 1.0; above that, too much subject detail is lost.

---

**`emboss()`** — applies an embossed relief texture appearance. Low relevance to our ad pipeline — stylistic only.

**`gridlines()`** — adds a grid overlay. Not applicable to ad production.

**`checkerboard()`** — checkerboard pattern overlay. Not applicable to ad production.

**Vignette fix (v4.0.481):** The existing `vignette()` effect (previously available) was fixed for transparent source layers — no parameter changes required.

**When to use from this set:** Only `zoomBlur()` has practical ad use. Emboss/gridlines/checkerboard are decorative — skip unless a future brief specifically calls for graphic-art styling.

---

### 11i. `@remotion/effects` — v4.0.479 Gap: `thermalVision()` and `pixelate()` (SC140 missed)

Four effects were added in v4.0.479 (June 17, 2026) but were not documented in SC140's update note. Two are pipeline-relevant:

**`thermalVision()`** — maps frame luminance to a customizable thermal heat-map color ramp using WebGL2. Low practical relevance for moving company ads (gimmicky), but useful for dramatic impact cuts or stylized freeze-frame reveals.

```tsx
import { thermalVision } from "@remotion/effects";

// Full thermal effect — replace entirely with heat palette
<AbsoluteFill style={{
  filter: thermalVision({ amount: 1 }),
}} />

// Blended thermal — 30% thermal overlay on normal footage
<AbsoluteFill style={{
  filter: thermalVision({ amount: 0.3 }),
}} />
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `amount` | `number` | `1` | Blend 0–1. `1` = full thermal; `0.3` = subtle overlay on source. |
| `palette` | `string[]` | Blue→green→yellow→red→white | Minimum 2 colors required. Custom ramp possible — e.g., `['#1a1a2e', '#FC8434', '#ffffff']` for brand-orange ramp. |

**Snelverhuizen use case:** Apply with `amount: 0.3` + brand-orange palette for a stylized title card look. Skip for character/truck shots — the effect makes faces unrecognizable.

---

**`pixelate()`** — applies a mosaic pixel-block effect. Not useful for final delivery; use only for deliberate stylized transitions or a "loading/reveal" animation where footage pixelates in.

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `blockSize` | `number` | `20` | 1–200 | Larger = more pixelated. Animate from high→low over ~8 frames for a "sharpen-in" reveal. |

```tsx
import { pixelate } from "@remotion/effects";
import { interpolate, useCurrentFrame } from "remotion";

// Sharpen-in reveal: starts fully pixelated, clears over 12 frames
const frame = useCurrentFrame();
const blockSize = interpolate(frame, [0, 12], [60, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});

<AbsoluteFill style={{
  filter: pixelate({ blockSize }),
}} />
```

**`shrinkwrap()`** and **`burlap()`** — also added in v4.0.479. `burlap()` renders a woven textile/fabric texture (similar to `paper()` but coarser, burlap-style). `shrinkwrap()` creates a plastic-wrap/shrink-film distortion effect. Neither has a defined use in our current ad pipeline. Skip unless a future brief calls for a specific material texture.

---

### 11j. `@remotion/effects` — Pipeline-Relevant Older Effects (v4.0.465–478, May–June 2026)

The @remotion/effects package launched at v4.0.465 (May 22, 2026) and shipped 30+ effects before SC140 (the first version our skill started tracking). These were never documented. The two highest-value effects for Snelverhuizen production are `glow()` and `duotone()`.

---

**`glow()`** (added v4.0.468, May 27, 2026) — WebGL2 luminous blur that adds a soft halo around bright areas. The most directly useful of the undocumented effects: adds warm light bloom to orange #FC8434 elements or character highlights.

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `radius` | `number` | `20` | 0–100 px | Spread of the glow bloom |
| `intensity` | `number` | `1` | 0–5 | Brightness multiplier; `1.5–2` for visible glow |
| `threshold` | `number` | `0` | 0–1 | Luminance threshold — only pixels above this brightness receive the glow. `0` = all pixels, `0.7` = bright-only |
| `color` | `string` | `'#ffffff'` | any hex/css | Glow color — set to `'#FC8434'` for brand orange bloom |

**Snelverhuizen use cases:**
```tsx
import { glow } from "@remotion/effects";

// Warm white glow on hero frame — adds cinematic halo to highlights
<AbsoluteFill style={{
  filter: glow({ radius: 25, intensity: 1.5, threshold: 0.6 }),
}} />

// Brand orange glow on title card text or badge
<AbsoluteFill style={{
  filter: glow({ radius: 15, intensity: 2, threshold: 0.5, color: '#FC8434' }),
}} />
```

**When to use:** Apply to a `<Sequence>` wrapping the orange badge or CTA pill for a warm brand-color bloom. Also effective on the hero frame arrival reveal to add cinematic warmth. **Do NOT apply to character faces at intensity > 1.5** — the face loses detail.

**When NOT to use:** Truck shots (glow may bleed onto surrounding frame and look unrealistic), or any shot requiring clean, crisp edges.

---

**`duotone()`** (added v4.0.468, May 27, 2026) — WebGL2 two-color treatment. Converts frame to a two-tone image based on luminance threshold. Very useful for stylized intro/outro frames and brand-color title cards.

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `darkColor` | `string` | `'#000000'` | Color for shadows/dark pixels |
| `lightColor` | `string` | `'#ffffff'` | Color for highlights/bright pixels |
| `threshold` | `number` | `0.5` | Luminance split point (0–1) |

**Snelverhuizen use cases:**
```tsx
import { duotone } from "@remotion/effects";

// Brand duotone: deep navy shadows, orange highlights — cinematic brand frame
<AbsoluteFill style={{
  filter: duotone({
    darkColor: '#1a1a2e',    // deep navy
    lightColor: '#FC8434',  // brand orange
    threshold: 0.45,
  }),
}} />

// Black + orange — high contrast logo reveal or end frame
<AbsoluteFill style={{
  filter: duotone({
    darkColor: '#000000',
    lightColor: '#FC8434',
    threshold: 0.5,
  }),
}} />
```

**When to use:** End frame / logo reveal shots. Transition frames between scenes. Hero frame title card (static or near-static). **Do NOT apply to the main character or truck action shots** — duotone makes faces unnatural and is inappropriate for a sincere moving company ad. Reserve for stylized graphic frames (0–2s duration).

---

**Other notable undocumented effects (v4.0.465–478) — low priority for our pipeline:**

| Effect | Added | Use case | Priority |
|--------|-------|----------|----------|
| `brightness()` | v4.0.466 | Single param `amount` (-1 to 1). Quick in-Remotion brightness tweak on a layer. | Low — use FFmpeg eq filter for video, or CSS `filter: brightness()` for static layers |
| `dropShadow()` | v4.0.469 | Params: `radius` (12), `offsetX` (8), `offsetY` (8), `opacity` (0.5), `color` ('#000000'). Shadow under brand badge or text overlay in Remotion. | Medium — useful if building badge overlays in Remotion rather than FFmpeg drawvg |
| `chromaticAberration()` | v4.0.467 | Cinematic lens color split for impact transitions | Low — stylistic only, not appropriate for straightforward ad |
| `halftone()` | v4.0.466 | Print-dot pattern effect | Low — decorative only |
| `scanlines()` | v4.0.470 | Retro CRT TV effect | Low — not on-brand |
| `vignette()` | v4.0.468 | Darkens frame edges — was fixed in v4.0.481 for transparent layers | Documented separately in §11h fix note |

**Note on `noise()`:** The package includes `noise.ts` in source, but it was not identified as exported in the main API timeline. This may be an internal utility or a future public effect. Do not use until confirmed in a changelog entry.

---

### 11k. `@remotion/effects` — `linearProgressivePixelate()` and `@remotion/rough-notation` (v4.0.490)

**`linearProgressivePixelate()`** (added v4.0.490, 2026-07-16) — applies a pixelation (mosaic) effect that varies in intensity across the frame in one direction, analogous to `linearProgressiveBlur()` but using pixel-block size instead of blur radius. Strong pixelation at one edge fades to no pixelation at the other.

```tsx
import { linearProgressivePixelate } from "@remotion/effects";

// Pixelation increases from 0 at top (y=0) to blockSize=40 at bottom (y=1)
// Use for a stylized reveal where the frame "clarifies" from bottom-to-top
<AbsoluteFill style={{
  filter: linearProgressivePixelate({
    direction: "to top",
    blockSizeAtEnd: 40,
    from: 0,
    to: 1,
  }),
}} />
```

**Parameters** (mirroring `linearProgressiveBlur` API):
| Parameter | Type | Notes |
|-----------|------|-------|
| `direction` | `string` | `"to bottom"`, `"to top"`, `"to left"`, `"to right"` |
| `blockSizeAtEnd` | `number` | Pixelation (block size, px) at the strong end. 0 at the other end. |
| `from` | `number` | UV fraction (0–1) where pixelation starts |
| `to` | `number` | UV fraction (0–1) where pixelation reaches full `blockSizeAtEnd` |

**Snelverhuizen use cases:**
- **Stylized intro reveal:** Animate `blockSizeAtEnd` from 40→0 over ~15 frames with `direction: "to top"` — the frame de-pixelates upward, like a cinematic scan-reveal.
- **Title card texture:** Static `blockSizeAtEnd=20` over the lower third behind captions for a graphic-art look. Combine with `linearGradient()` dark scrim for legibility.
- **Cross-shot transition:** Apply at the end of one clip (blockSize 0→30) and start of the next (30→0) — creates a pixelate/de-pixelate cut-through effect. Keep transition under 8 frames to avoid looking gimmicky.

**When to use vs `pixelate()`:**
- `pixelate()` (§11i) — uniform pixelation across the entire frame; useful for animate-in/animate-out reveals
- `linearProgressivePixelate()` — graduated pixelation in one direction; useful for partial-frame graphic treatments and directional reveals

**Note:** API name `linearProgressivePixelate` inferred from Remotion's naming convention (`linearProgressiveBlur` → `linearProgressivePixelate`). Verify against the published `@remotion/effects` package before use in production.

---

**`@remotion/rough-notation`** (new package, v4.0.490) — wraps the [rough-notation](https://roughnotation.com/) library to render sketch/handdrawn annotation overlays on Remotion compositions. Supported annotation types: underline, box, circle, highlight, strike-through, crossed-off, bracket.

**Snelverhuizen use case:** Handdrawn circle or underline around the SNELVERHUIZEN.NL URL or phone number in a title-card frame for an organic, personal-touch feel. Use with the brand orange `#FC8434` color (`color: "#FC8434"`). Appropriate for still or near-still frames only — rough-notation animations do not synchronize frame-accurately to Remotion's frame clock without custom integration.

```tsx
// Install: npm install @remotion/rough-notation rough-notation
import { RoughNotation } from "@remotion/rough-notation";

// Orange underline under a URL text element
<RoughNotation type="underline" color="#FC8434" strokeWidth={3} show={true}>
  <span>SNELVERHUIZEN.NL</span>
</RoughNotation>
```

**Limitation:** rough-notation drives animations via a JS animation loop that is not frame-clock-aligned. For static (non-animating) annotations, `show={true}` renders immediately — safe. For animated strokes, the timing is wall-clock-based, not Remotion-frame-based, meaning render consistency may vary. Only use with `show={true}` (no animation) for reliable render output.

---

### 11l. `@remotion/effects` — `liquidContours()` and `skew()` (v4.0.491)

**`liquidContours()`** (added v4.0.491, 2026-07-18) — WebGL2 procedural fluid/organic contour pattern generator. Renders alternating color bands shaped by a Perlin-style noise field, producing a liquid topographic-map look. Also available as a `<LiquidContours>` React Element component (renders as a full composition layer, not a CSS filter).

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `firstColor` | `string` | `'#ff1a0a'` | First alternating band color |
| `secondColor` | `string` | `'#050505'` | Second alternating band color |
| `spacing` | `number` | `62` | Width of a band pair in pixels; lower = tighter bands |
| `scale` | `number` | `300` | Size of generated shapes in pixels; lower = smaller features |
| `complexity` | `number` | `0` | Small-scale detail amount, 0–1; higher = more noise |
| `smoothness` | `number` | `1` | Edge softness, 0–1; lower = sharper, rougher bands |
| `seed` | `number` | `4` | Deterministic seed — same seed = same pattern every render |
| `offsetX` | `number` | `13.4` | Horizontal pattern offset in pixels |
| `offsetY` | `number` | `0` | Vertical pattern offset in pixels |
| `phase` | `number` | `3.23` | Shifts the alternating bands across the pattern |

**Snelverhuizen use cases:**

```tsx
import { liquidContours } from "@remotion/effects";
// Or as a layer component:
import { LiquidContours } from "@remotion/effects";

// Brand-orange + dark navy end-frame background
// firstColor = brand orange, secondColor = deep navy
<AbsoluteFill style={{
  filter: liquidContours({
    firstColor: '#FC8434',
    secondColor: '#1a1a2e',
    spacing: 80,
    scale: 350,
    complexity: 0.3,
    smoothness: 0.8,
    seed: 42,
  }),
}} />

// As a full layer (fills the frame with the pattern — no host content visible):
<LiquidContours
  firstColor="#FC8434"
  secondColor="#1a1a2e"
  spacing={80}
  scale={350}
  complexity={0.3}
  seed={42}
/>
```

**Key distinction — filter vs Element:**
- `liquidContours()` as a CSS `filter`: renders the pattern as a tint/overlay over content beneath it (like other `@remotion/effects` functions)
- `<LiquidContours>` as a component: fills the frame with the pattern as a standalone layer (use as a background layer with content composited above)

**When to use:**
- **End frame / title card background** — drives `seed` from a fixed value + animates `offsetX`/`offsetY` slowly for a subtle moving background. Avoid fast animation; the effect should feel ambient.
- **Intro frame** — brand-orange (#FC8434) bands on deep navy backdrop before cutting to character reveal.
- **NOT for character or truck shots** — the pattern would obscure subjects.

**Animation recipe — slowly drifting brand background:**
```tsx
import { useCurrentFrame, interpolate } from "remotion";

const frame = useCurrentFrame();
const offsetX = interpolate(frame, [0, 90], [0, 30]); // drifts 30px over 3s
<LiquidContours firstColor="#FC8434" secondColor="#1a1a2e" offsetX={offsetX} seed={7} />
```

---

**`skew()`** (added v4.0.491, 2026-07-18) — WebGL2 perspective skew transform. Slants the frame content diagonally, like a CSS `skewX()`/`skewY()` but with WebGL2 precision and a configurable UV origin point.

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `x` | `number` | `20` | -80 to 80 | Horizontal skew angle in degrees; positive = leans right |
| `y` | `number` | `0` | -80 to 80 | Vertical skew angle in degrees |
| `origin` | `[number, number]` | `[0.5, 0.5]` | 0–1 per axis | UV coordinate of skew anchor; [0.5, 0.5] = center |

```tsx
import { skew } from "@remotion/effects";

// Subtle forward-lean on a truck badge or title — feels dynamic/in-motion
<AbsoluteFill style={{
  filter: skew({ x: 12, y: 0, origin: [0.5, 0.5] }),
}} />

// CTA pill text slanted slightly right (x: 8) anchored at left edge
<AbsoluteFill style={{
  filter: skew({ x: 8, origin: [0, 0.5] }),
}} />
```

**Snelverhuizen use cases:**
- **Brand badge / CTA pill** — apply `x: 8–15` for a forward-lean kinetic look on the SNELVERHUIZEN.NL pill badge. Makes static text look like it's "in motion" — appropriate for a moving company.
- **Headline text layer** — `x: 10` gives Dutch headline text a confident, forward-motion slant. Pair with `roughenEdges()` for a hand-made feel.
- **Transition frame** — animate `x` from `15→0` over ~8 frames as a clip enters: text "straightens up" from a skewed intro position. Dynamic opener for reveal frames.
- **NOT for face/character layers** — skewing faces looks unnatural; apply only to text and badge layers.

**When NOT to use:** Absolute angle ≥ 89° throws an error (hard limit). Keep `x` between -20 and +20 for any ad-appropriate skew; beyond ±30 the effect becomes jarring.

---

**Note:** Requires WebGL2 — same as all other `@remotion/effects` functions. Remotion renderer supports WebGL2 natively.

---

### 11m. `@remotion/effects` — `wave()` and `noiseDisplacement()` (SC235 — Previously Undocumented)

These effects ship in the `@remotion/effects` package (available since launch at v4.0.464) but were never documented in this skill. Confirmed present in v4.0.495.

---

**`wave()`** — applies a sine-wave distortion to the frame, bending content as if seen through rippling water or a warped lens. Useful for stylized intro/outro transitions or to add organic motion to otherwise static title cards.

```tsx
import { wave } from "@remotion/effects";

// Subtle horizontal wave on a title card — organic, handcrafted feel
<AbsoluteFill style={{
  filter: wave({ amplitude: 10, wavelength: 80, speed: 0 }),
}} />

// Animated wave — drive speed with frame counter for flowing motion
import { useCurrentFrame } from "remotion";
const frame = useCurrentFrame();
<AbsoluteFill style={{
  filter: wave({ amplitude: 8, wavelength: 60, speed: frame * 0.05 }),
}} />
```

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `amplitude` | `number` | — | Vertical displacement in pixels; higher = more dramatic wave |
| `wavelength` | `number` | — | Horizontal period of the wave in pixels; higher = broader, slower undulation |
| `speed` | `number` | `0` | Phase offset — animate by multiplying `useCurrentFrame()` for flowing wave |

**Snelverhuizen use cases:**
- Static `speed: 0` on an end-frame title card for an organic, non-flat look (pair with `paper()` for handcrafted feel)
- Animated wave intro (speed = frame × 0.05) on the opening brand-color background (`<LiquidContours>`) for ambient motion — avoid on character/truck shots
- **NOT for any shot showing faces, the truck, or boxes** — wave distortion on subjects looks like a technical defect

---

**`noiseDisplacement()`** — displaces pixels based on a Perlin noise field, creating an irregular, organic shimmering/trembling effect. Different from `wave()` (regular sine pattern) — `noiseDisplacement()` is irregular and randomized per pixel.

```tsx
import { noiseDisplacement } from "@remotion/effects";

// Subtle shimmer on a branded title card — feels alive without obvious motion
<AbsoluteFill style={{
  filter: noiseDisplacement({ strength: 5, scale: 0.01, seed: 42 }),
}} />
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `strength` | `number` | Displacement intensity in pixels. 3–8 = subtle shimmer; 15+ = visibly distorted |
| `scale` | `number` | Noise frequency. Lower = larger, broader displacement blobs; higher = tighter, grainier |
| `seed` | `number` | Deterministic seed — same seed produces same pattern; vary per composition to avoid identical looks |

**Snelverhuizen use cases:**
- `strength: 4, scale: 0.008` on a title-card background layer for a barely-visible living texture — heat-haze effect on end frame
- `strength: 8` on an intro freeze-frame (static frame held 0.5s) to add organic life before cut to action
- **NOT on character close-ups or truck shots** — irregular pixel displacement reads as video compression corruption

**When to use `wave()` vs `noiseDisplacement()`:**
- `wave()` — regular, rhythmic undulation; use for cinematic ripple or flowing reveal
- `noiseDisplacement()` — irregular, random; use for organic "living" texture or heat-distortion on still frames

**Note:** Both require WebGL2. Remotion renderer supports WebGL2 natively — no extra config needed.

---

### 11n. `@remotion/effects` — Color Correction Suite (v4.0.507–509, Aug 2026)

**⚠️ SC256 CORRECTION:** SC256 (2026-08-14) incorrectly stated "no new `@remotion/effects` additions in v4.0.501–509." Confirmed via GitHub release history: v4.0.507 added `regionblur()`, v4.0.508 added five grading effects, v4.0.509 added `colorCorrection()`. Seven effects total were missed. Documented SC263 (2026-08-16).

These are the most pipeline-relevant effects yet for Snelverhuizen — they address AI-generated video color correction directly in Remotion, avoiding an extra FFmpeg pass when doing caption/overlay compositions.

---

**`regionblur()`** (v4.0.507, Aug 7, 2026) — Gaussian blur applied only within a defined rectangular region. Does NOT blur the entire frame — only the specified area. Backend: WebGL2.

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `topLeft` | `[number, number]` | Required | UV coordinate (0–1) of region top-left corner |
| `bottomRight` | `[number, number]` | Required | UV coordinate (0–1) of region bottom-right corner |
| `blurRadius` | `number` | `40` | Gaussian blur radius in pixels |
| `feather` | `number` | `0` | Soft edge width in pixels — feathers the blur boundary |
| `roundness` | `number` | `0` | 0 = rectangular region, 1 = fully pill-shaped/rounded |

```tsx
import { regionblur } from "@remotion/effects";

// Blur lower-right background area — e.g. hide distraction behind character
<AbsoluteFill style={{
  filter: regionblur({
    topLeft:     [0.55, 0.60],
    bottomRight: [1.00, 1.00],
    blurRadius:  25,
    feather:     20,
    roundness:   0.3,
  }),
}} />
```

**Snelverhuizen use cases:**
- Blur a distracting background region (e.g. car parked behind character) without re-generating the clip
- Privacy-blur an incidental bystander in the background (feather=20 for natural transition)
- Soft focus effect on lower-third background to improve caption readability — alternative to `linearProgressiveBlur()` when blur should not extend past a vertical boundary

**When to use vs `linearProgressiveBlur()`:**
- `regionblur()` — blurs a defined rectangular/rounded area; cleanest for isolated region correction
- `linearProgressiveBlur()` — blurs in a gradient from one edge; better for full-frame directional softening behind caption rows

---

**`exposure()`** (v4.0.508, Aug 11, 2026) — single-parameter exposure correction in stops (±5 stop range). Applies a perceptual exposure multiplier — emulates how a camera sensor responds to light, not just a linear brightness shift. Backend: WebGL2.

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `stops` | `number` | `0` | -5 to +5 | Exposure adjustment in stops. +1 = one stop brighter (doubles luminance); -1 = one stop darker |

```tsx
import { exposure } from "@remotion/effects";

// Lift a slightly underexposed Kling clip by 0.5 stops
<AbsoluteFill style={{
  filter: exposure({ stops: 0.5 }),
}} />
```

**Snelverhuizen use case:** Kling v3 Pro I2V clips occasionally render 0.3–0.5 stops underexposed, especially on interior shots (moving boxes in hallway) and overcast exterior shots. Apply `exposure({ stops: 0.3–0.5 })` in the Remotion composition before the `colorCorrection()` step to lift the base exposure without affecting the color grade.

**Prefer `colorCorrection()` (below) when making multiple adjustments** — one WebGL2 pass is more efficient than chaining separate effects.

---

**`whiteBalance()`** (v4.0.508, Aug 11, 2026) — corrects color temperature (warm/cool) and tint (green/magenta) independently. Critical for AI-generated video: Kling and Veo outputs frequently have a slight cool or magenta cast compared to real-world footage.

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `temperature` | `number` | `0` | -1 to +1 | Blue-to-amber. Negative = cooler (more blue); positive = warmer (more amber) |
| `tint` | `number` | `0` | -1 to +1 | Green-to-magenta. Negative = greener; positive = more magenta |

```tsx
import { whiteBalance } from "@remotion/effects";

// Warm up a cool AI-generated exterior shot
<AbsoluteFill style={{
  filter: whiteBalance({ temperature: 0.08, tint: -0.02 }),
}} />
```

**Snelverhuizen use case:** Kling v3 Pro clips with outdoor Dutch scenes commonly show a cool-gray cast from overcast sky color contamination. Warm with `temperature: 0.05–0.15` to match the golden/warm look of our brand identity. Check against the approved V2-Proces reference frame before applying — if the AI clip matches the reference, skip.

---

**`vibrance()`** (v4.0.508, Aug 11, 2026) — intelligent saturation boost that protects skin tones. Unlike `saturation` in `colorCorrection()` (which boosts all colors equally), `vibrance` boosts desaturated colors more and leaves already-vivid colors (especially skin tones) largely untouched.

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `amount` | `number` | `0` | -1 to +1 | +0.1 to +0.3 = subtle boost; +0.5+ = strong vivid pop; negative = desaturate muted tones |

```tsx
import { vibrance } from "@remotion/effects";

// Subtle vibrance boost on a wide establishing shot — pops the orange truck
// without blowing out skin tones on the character
<AbsoluteFill style={{
  filter: vibrance({ amount: 0.2 }),
}} />
```

**Snelverhuizen use case:** Apply on wide shots (truck + character in frame) where the orange #FC8434 looks slightly muted due to AI-generated lighting. `amount: 0.15–0.25` boosts the truck's orange without making skin tones look oversaturated.

---

**`levels()`** (v4.0.508, Aug 11, 2026) — Photoshop-style input levels. Maps a custom input shadow/highlight range to full output black-to-white, then applies a midtone gamma correction. Use to set black point (clip shadows), white point (clip highlights), and lift/lower midtones.

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `blackPoint` | `number` | `0` | 0–1 | Input value mapped to black output; raise to crush shadows (0.05–0.15 typical) |
| `whitePoint` | `number` | `1` | 0–1 | Input value mapped to white output; lower to clip highlights (0.85–0.95 typical) |
| `gamma` | `number` | `1` | 0.01–10 | Midtone lift/lower. < 1 = lift mids (brighter); > 1 = lower mids (darker); 0.85–0.90 for cinematic look |

```tsx
import { levels } from "@remotion/effects";

// Cinematic levels — crush blacks slightly, clip highlights, lift mids
<AbsoluteFill style={{
  filter: levels({ blackPoint: 0.05, whitePoint: 0.92, gamma: 0.90 }),
}} />
```

**Snelverhuizen use case:** AI-generated Kling clips tend to have "milky" shadows (elevated black floor) because diffusion models never produce true black. Apply `blackPoint: 0.04–0.08` to crush shadows to true black and add cinematic punch. Do NOT crush more than 0.10 — the correction looks posterized on smooth gradient areas.

---

**`shadowsHighlights()`** (v4.0.508, Aug 11, 2026) — recovers detail in shadow and highlight areas independently. Like the Adobe Camera Raw Shadows/Highlights sliders.

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `shadows` | `number` | `0` | -1 to +1 | Positive = lift shadows (recover dark detail); negative = crush shadows |
| `highlights` | `number` | `0` | -1 to +1 | Positive = recover blown highlights; negative = darken bright areas |

```tsx
import { shadowsHighlights } from "@remotion/effects";

// Recover shadow detail in a dark hallway moving scene
<AbsoluteFill style={{
  filter: shadowsHighlights({ shadows: 0.25, highlights: -0.10 }),
}} />
```

**Snelverhuizen use case:** Interior moving scenes (stairway, hallway shots) where subject faces are dark against a bright window. `shadows: 0.2–0.35` lifts faces without over-exposing the window. Pair with `highlights: -0.1` to pull back blown-out areas.

---

**`colorCorrection()`** (v4.0.509, Aug 12, 2026) — **single combined color correction effect** that chains all the above adjustments in one WebGL2 pass. The recommended approach when applying ≥2 color adjustments to a clip — more efficient than stacking multiple separate effects.

| Parameter | Type | Default | Range | Notes |
|-----------|------|---------|-------|-------|
| `exposure` | `number` | `0` | -5 to +5 | Same as standalone `exposure()` |
| `contrast` | `number` | `1` | 0–3 | Contrast multiplier around `pivot`. 1 = unchanged; 1.1 = slight contrast boost |
| `pivot` | `number` | `0.5` | 0–1 | Contrast center point (luminance). 0.5 = neutral midpoint; lower = protects shadows |
| `shadows` | `number` | `0` | -1 to +1 | Same as `shadowsHighlights().shadows` |
| `highlights` | `number` | `0` | -1 to +1 | Same as `shadowsHighlights().highlights` |
| `whites` | `number` | `0` | -1 to +1 | Fine-tune extreme highlights (above whitePoint); positive = expand whites |
| `blacks` | `number` | `0` | -1 to +1 | Fine-tune extreme shadows (below blackPoint); negative = crush blacks |
| `temperature` | `number` | `0` | -1 to +1 | Same as `whiteBalance().temperature` |
| `tint` | `number` | `0` | -1 to +1 | Same as `whiteBalance().tint` |
| `saturation` | `number` | `1` | 0–3 | Uniform saturation. 1 = unchanged; 1.1 = slight boost; 0.85 = slight desaturate |
| `vibrance` | `number` | `0` | -1 to +1 | Same as standalone `vibrance()` |

**Standard Snelverhuizen AI clip color pass:**
```tsx
import { colorCorrection } from "@remotion/effects";

// Standard grade for Kling exterior shot (overcast Dutch sky)
<AbsoluteFill style={{
  filter: colorCorrection({
    exposure:     0.3,      // lift 0.3 stops — Kling outdoor shots run slightly dark
    contrast:     1.05,     // subtle punch
    pivot:        0.45,     // protect shadows while adding contrast
    blacks:      -0.06,     // crush black floor (Kling milky shadows)
    temperature:  0.08,     // warm from cool AI cast
    tint:        -0.02,     // slight green correction (Veo/Kling magenta cast)
    vibrance:     0.15,     // pop the orange truck without harming skin tones
  }),
}} />

// Interior moving scene (hallway, stairway)
<AbsoluteFill style={{
  filter: colorCorrection({
    exposure:    0.4,
    contrast:    1.03,
    shadows:     0.20,       // lift faces vs bright window
    highlights: -0.10,       // pull back blown windows
    blacks:     -0.05,
    temperature: 0.05,
  }),
}} />
```

**When to use `colorCorrection()` vs individual effects:**
- **≥2 adjustments needed:** Always use `colorCorrection()` — one WebGL2 pass vs multiple
- **Single adjustment only:** Use the standalone effect (`exposure()`, `whiteBalance()`, etc.) — cleaner code
- **FFmpeg color grade (§2c eq filter):** Still preferred for video-only encode pipelines. Use `colorCorrection()` when the clip is already inside a Remotion composition (e.g., for caption overlay renders — avoids an extra FFmpeg transcode step)

---

**Note on import paths (all effects above):**
```bash
npm install @remotion/effects
```
```tsx
import {
  regionblur, exposure, whiteBalance, vibrance,
  levels, shadowsHighlights, colorCorrection
} from "@remotion/effects";
```

All require WebGL2. Remotion renderer supports WebGL2 natively — no extra config needed.

---

### 11o. `@remotion/effects` — `tile()` (v4.0.513, SC277)

**`tile()`** (added v4.0.513, 2026-08-18) — WebGL2 effect that repeats its child composition as a tiled grid pattern across the frame. Creates a seamless mosaic/wallpaper treatment from any Remotion composition layer.

Parameters:
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `columns` | `number` | `2` | Number of tile columns (horizontal repeat count) |
| `rows` | `number` | `2` | Number of tile rows (vertical repeat count) |
| `phase` | `[number, number]` | `[0, 0]` | UV offset for the tile grid — animate to scroll the pattern |
| `flipAlternating` | `boolean` | `false` | Mirror every other tile — creates a symmetric reflect pattern; good for abstract brand treatments |

**Practical uses for Snelverhuizen:**

**1. Repeating logo/box pattern for title card backgrounds:**
```tsx
import { tile } from "@remotion/effects";

// 4×6 tiled grid of the moving-box asset as a title card background
// Set opacity low so it reads as texture behind the headline
<AbsoluteFill style={{ filter: tile({ columns: 4, rows: 6 }), opacity: 0.12 }}>
  <MovingBoxAsset />
</AbsoluteFill>
```

**2. Animated scrolling brand tile (ambient drift on end cards):**
```tsx
import { tile } from "@remotion/effects";
import { interpolate, useCurrentFrame } from "remotion";

const frame = useCurrentFrame();
// Slowly drift the tile grid — full scroll cycle over 90 frames
const phaseX = interpolate(frame, [0, 90], [0, 1]);

<AbsoluteFill style={{ filter: tile({ columns: 3, rows: 5, phase: [phaseX, 0] }), opacity: 0.08 }}>
  <OrangeBrandPattern />  {/* solid #FC8434 or logo lockup */}
</AbsoluteFill>
```

**3. Mirror-reflect tile for abstract end frame texture:**
```tsx
<AbsoluteFill style={{ filter: tile({ columns: 4, rows: 4, flipAlternating: true }), opacity: 0.10 }}>
  <TruckSilhouette />
</AbsoluteFill>
```

**When to use:**
- Title cards, end frames, and interstitials with abstract brand texture
- Low-opacity background layer only — never in the foreground
- Brand pattern backgrounds replacing solid color fills

**When NOT to use:**
- Character shots (any face in frame)
- Truck exterior or cargo shots
- Any clip that will be animated — tile is designed for static composition layers used as background texture

**Import:**
```tsx
import { tile } from "@remotion/effects";
// Part of @remotion/effects — already installed with other effects
```

---

### 11p. `@remotion/effects` — `outline()` (v4.0.515, SC284)

**`outline()`** (added v4.0.515, 2026-08-21) — WebGL2 effect that renders a colored stroke/border around the alpha channel of its input layer. Detects transparent-to-opaque edges and draws a configurable outline around them. Backend: WebGL2.

Parameters:
| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `width` | `number` | `8` | Outline stroke width in pixels |
| `edgeSimplification` | `number` | `0` | Pixel tolerance for simplifying the alpha contour into straight edges — higher = more blocky/geometric outline |
| `color` | `string` | `'#ffffff'` | Outline color (hex or CSS color) |
| `opacity` | `number` | `1` | Outline opacity 0–1 |
| `outlineOnly` | `boolean` | `false` | When `true`, replaces source content with just the filled outline mask (removes interior, keeps only the stroke border) |

**Practical uses for Snelverhuizen:**

**1. Brand-orange outline on caption text (most useful — improves legibility on busy backgrounds):**
```tsx
import { outline } from "@remotion/effects";

// Stack: video → text layer with orange outline → text layer (opaque white)
<AbsoluteFill style={{ filter: outline({ width: 4, color: '#FC8434', opacity: 0.9 }) }}>
  <CaptionTextLayer />  {/* white text, transparent background */}
</AbsoluteFill>
```

**2. White outline around logo lockup on dark or mixed backgrounds:**
```tsx
<AbsoluteFill style={{ filter: outline({ width: 6, color: '#ffffff', opacity: 0.7 }) }}>
  <SnelverhuizenLogoLayer />
</AbsoluteFill>
```

**3. Silhouette border for decorative brand shape (outlineOnly=true):**
```tsx
// Creates just the stroke with transparent interior — for layered badge animations
<AbsoluteFill style={{ filter: outline({ width: 12, color: '#FC8434', outlineOnly: true }) }}>
  <TruckSilhouette />
</AbsoluteFill>
```

**When to use:**
- Caption text legibility on complex backgrounds — orange outline at `width` 3–6 is sharper than a text shadow
- Logo or badge overlays needing clean separation from background
- Decorative border animations on title cards and end frames

**When NOT to use:**
- As a substitute for `drawtext` `borderw` param — if it's a pure text-only FFmpeg overlay, `drawtext` is simpler and requires no Remotion
- On character or face layers — outline on face shapes produces visible artifacts
- On truck/vehicle shots

**Comparison with `glow()` (§11j):** `glow()` creates a diffuse bloom around bright pixels; `outline()` creates a hard-edged stroke around the alpha boundary. For caption text: `outline()` is sharper and more legible; `glow()` is softer and more decorative. Use `outline()` for legibility; `glow()` for badge warmth.

**Import:**
```tsx
import { outline } from "@remotion/effects";
```

---

## Post-Production Checklist

Before marking video as delivered:

- [ ] ffprobe colorspace check on each AI clip (see §1a) — tag BT.709 if metadata missing
- [ ] Check for temporal brightness flicker (pulsing exposure) — if present, apply §9a normalize filter (smoothing=15, strength=0.7, independence=0.0 for faces)
- [ ] Check for blocking/mosquito noise artifacts — if present, apply §9b hqdn3d=4:4:3:3 + unsharp (light mode for faces, moderate for backgrounds)
- [ ] All clips have identical resolution (1080×1920) and frame rate (30fps) before assembly
- [ ] LUT applied matching the scene mood (warm/neutral/cool — see table above)
- [ ] Dither applied (zscale dither=error_diffusion) on clips with gradient skies/walls
- [ ] Frame interpolation: run scene detection (§3d) first with **PySceneDetect v0.7.1** (now stable, released 2026-07-21; install as `scenedetect-headless`; handles VFR AI clips correctly); use `split-video --expand` flag to preserve footage at boundaries; check `VideoStream.decode_failures > 0` on AI clips before RIFE; interpolate per-segment with rife-v4.25 (pipeline default for diffusion video) or rife-v4.25.heavy (middle-tier quality, same TNTwise binary) or rife-v4.26.heavy (highest quality, CLI only); use TNTwise rife-ncnn-vulkan CLI fork v20250112 (`TNTwise/rife-ncnn-vulkan` — NOT archived, separate repo) — supports v4.25/v4.25.heavy/v4.26/v4.26.heavy; nihui binary tops out at v4.6. **Do NOT use RVE GUI — repo archived 2026-07-13.** Check ghost artifacts.
- [ ] Instagram algorithm: our 30–60s ads are well under the 90s sweet spot and far under the 3-min non-follower cutoff — no action needed, but flag if a future brief pushes past 3 minutes
- [ ] Text overlays respect Instagram safe zone: bottom 320px, right 120px clear — see §5f
- [ ] TikTok repurpose: re-check right ~184px dead zone (wider than Instagram; Add to Playlist +20px Jan 2026, effective safe area ~836 × 1466px) — see §5g
- [ ] All text overlays composited (see text-overlay-compositing.md)
- [ ] Audio mixed per halal-audio.md — voiceover + SFX only, no instruments
- [ ] Final mix loudness: -14 LUFS ±1.0, true peak ≤ -1.5 dBTP
- [ ] Export: H.264, -pix_fmt yuv420p, -movflags +faststart, AAC 48kHz 256kbps
- [ ] ffprobe check passes (correct codec, resolution, fps confirmed)
- [ ] VMAF score ≥ 90 vs pre-export reference (if libvmaf available) — see §7
- [ ] AV1 archive: use SVT-AV1 v4.2.0 (released 2026-07-14) — `-svtav1-params tune=0` (VQ, perceptual) — NOT tune=3 (AVIF/still-image only). New in v4.2: `--tune-vmaf` flag (~15% VMAF BD-rate gain) but only via standalone binary, not FFmpeg libsvtav1 — pipeline commands unchanged. SVT-AV1-PSY fork archived Feb 2026; mainline SVT-AV1 4.2 + tune=0 is correct path. See §5h.
- [ ] Brand badge overlays: prefer `drawvg` (§10) + `drawtext` chain in FFmpeg 8.1+ for exact #FC8434 pill shapes without Remotion — use `setcolor #FC8434` (direct hex, preferred) or `setrgba`, then `roundedrect`/`fill` (NOT `set_source_rgb`/`rectangle`)
- [ ] Remotion v4.0.491 effect options: use `radialProgressiveBlur()` for cinematic DOF vignette on character close-ups (center on face, endBlur=20–30px); use `linearProgressiveBlur()` for caption-bar blur on light backgrounds; use `linearGradient()` for dark scrim behind captions or #FC8434 brand accent (startColor/endColor with alpha); use `cornerPin()` for perspective overlays on truck surfaces (UV coords 0–1 range); use `venetianBlinds()` for truck/scene reveal transitions (direction='horizontal', slats=8, drive progress 0→1 over ~12 frames); use `paper()` for organic film-grain texture on title cards (seed param, apply at low opacity); use `roughenEdges()` for torn-edge badge/overlay looks (border 15–25 subtle, 40+ dramatic); use `zoomBlur()` for impact/reveal transition punch-ins (strength 0.6–0.8, drive to 0 over ~6 frames); use `glow()` for warm brand-color bloom on orange badge/CTA elements (radius=15–25, intensity=1.5–2, threshold=0.5–0.7, color='#FC8434'); use `duotone()` for stylized brand-color end/title frames only (darkColor='#1a1a2e', lightColor='#FC8434', threshold=0.45) — NOT on character/truck shots; use `pixelate()` animated sharpen-in reveal (blockSize 60→1 over 12 frames); use `linearProgressivePixelate()` (v4.0.490, §11k) for directional pixelation reveals (blockSizeAtEnd=30–40, 15-frame animate-in) or partial-frame graphic treatments; use `@remotion/rough-notation` for static sketch-style annotations on title cards (color='#FC8434', show={true} only — no animation); use `<LiquidContours>` / `liquidContours()` (v4.0.491, §11l) for branded organic-pattern title card backgrounds (firstColor='#FC8434', secondColor='#1a1a2e' — animate offsetX slowly for ambient drift, never on character/truck shots); use `skew()` (v4.0.491, §11l) for kinetic forward-lean on CTA pills and headline text layers (x: 8–15°, keep under ±30 — never on face/character layers); use `wave()` (§11m) for sine-wave distortion on title card backgrounds (static speed=0 for organic texture, animated for flowing ripple — never on faces/truck); use `noiseDisplacement()` (§11m) for irregular living texture on freeze-frame or end-frame backgrounds (strength 3–8 subtle, 15+ distorted — never on character shots) — see §11a, §11c, §11d, §11f, §11g, §11h, §11i, §11j, §11k, §11l, §11m
- [ ] Remotion looped audio: if any Remotion composition loops ambient SFX via `<Audio>`, test for dropout — v4.0.488 fixed a looped audio dropout bug after multiple iterations; upgrade to ≥ v4.0.488 if affected
- [ ] Remotion Sequence opacity: if any `<Sequence>` wrapper uses `opacity` for fade-in/fade-out on caption overlays or branded layers, upgrade to ≥ v4.0.494 (fixed Sequence opacity preservation while active — prior versions did not maintain opacity correctly)
- [ ] Remotion layer opacity leak (v4.0.499): if any composition stacks multiple layers with non-100% opacity (brand badge over video, caption over scrim), upgrade to ≥ v4.0.499 — v4.0.499 fixes opacity leaking between stacked layers in web-renderer
- [ ] Remotion color correction (§11n, SC263): if clip is inside a Remotion composition and shows AI color cast → apply `colorCorrection()` in one WebGL2 pass instead of chaining multiple effects. Standard exterior Kling pass: exposure=0.3, contrast=1.05, pivot=0.45, blacks=-0.06, temperature=0.08, tint=-0.02, vibrance=0.15. Interior (dark hallway): exposure=0.4, shadows=0.20, highlights=-0.10, blacks=-0.05, temperature=0.05. Single adjustments: use standalone `exposure()`, `whiteBalance()`, `vibrance()`, `levels()`, `shadowsHighlights()`, or `regionblur()` (selective area blur, topLeft/bottomRight UV coords required)
- [ ] Remotion outline effect (§11p, SC284, v4.0.515+): for caption text legibility on busy backgrounds, use `outline()` from `@remotion/effects` — stack a text layer with `filter: outline({ width: 4, color: '#FC8434', opacity: 0.9 })` below the opaque white text layer; also for logo overlays needing clean edge separation (`width` 4–8, `color` white or #FC8434); use `outlineOnly: true` for decorative silhouette border animations. **Never on character face layers or truck shots.**
- [ ] Remotion tile pattern backgrounds (§11o, SC277, v4.0.513+): for title cards and end frames needing brand texture backgrounds, use `tile()` from `@remotion/effects` — apply at opacity 0.08–0.12 as a low background layer. Parameters: columns/rows (repeat count), phase ([x,y] offset, animate for slow drift), flipAlternating (mirror every other tile). **Never on character/truck shots.** Also: `@remotion/media` audio sample-rate fix in v4.0.513 — if any Remotion composition mixes audio at different sample rates (e.g., voiceover 44100 Hz + SFX 22050 Hz), upgrade to ≥ v4.0.513 to fix distorted/sped-up audio
- [ ] Remotion Video muted prop (v4.0.492+): when embedding video clips in Remotion compositions, use `<Video muted>` to silence source audio when layering independent SFX/voiceover above
- [ ] `getVideoMetadata()` deprecated (v4.0.498): if any pipeline script calls Remotion's `getVideoMetadata()`, flag for migration before upgrading past v4.0.497. **v5 confirmed removal** (GitHub #3310): migrate to **Mediabunny** — `@remotion/renderer` no longer exports `getVideoMetadata()` in v5; use the Mediabunny API (`import { getVideoMetadata } from "@remotion/mediabunny"`) as the replacement.
- [ ] Remotion compositions: if any `<Audio>` component used, add explicit `optimizeFor="accuracy"` — v5 **confirmed breaking change** (GitHub #3310): default switches to `"speed"` (slightly different audio visualization); `optimizeFor="accuracy"` preserves current behavior. Also confirmed v5 package deprecations: `@remotion/media-parser` and `@remotion/webcodecs` will not be published in v5 (replace with Mediabunny); `@remotion/light-leaks` and `@remotion/starburst` also removed. If pipeline uses any of these, flag for migration. v5 Automators tier will require mandatory telemetry (`licenseKey`) — see §11b (forward-compat guard, low priority until v5 releases)
- [ ] Remotion version recheck (SC330, 2026-09-06): latest is **v4.0.521** (released Sept 5, 2026). Changes in v4.0.521: Studio UI / stability fixes — playback rate reset fix, video rendering stall fix on Windows (not our pipeline), caption import in Studio (import Remotion caption JSON for review), caption editing fix in Elements, OPFS fallback for web rendering (not our pipeline), bundler incremental chunk graph builds (faster Remotion bundling — passive benefit for our compositing step), composition reordering. **No new production effects. No server-side rendering changes. No audio or caption format changes.** For server-side (our path): no action required beyond upgrading. Prior v4.0.520 changes still apply (SC316): Studio UI, `playbackStore`/`usePlaying()`, `@remotion/whisper-webgpu` (browser-WASM only, not our pipeline), `@remotion/gsap`, social safe-zone overlay (Studio only). Upgrade to v4.0.521 when next touching Remotion compositions.
- [ ] Delivery to owner: WhatsApp **Document** share (not video message) for lossless 2GB delivery
- [ ] Final video watched end-to-end before delivery (MANDATORY per CLAUDE.md)

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

### 3a. REAL Video Enhancer (Preferred — GUI, scene-detection, multi-backend)

**TNTwise REAL Video Enhancer v2.4.1** (stable, 2026-01-02) is the recommended tool. Also available on Steam (released 2026-02-11) for easier Windows/Mac install. It wraps RIFE with scene change detection (prevents blending artifacts at cuts), and supports TensorRT (NVIDIA RTX, fastest), PyTorch CUDA/ROCm (AMD), and NCNN Vulkan (any modern GPU).

**v2.4.2 pre-release note (2026-01-09, still pre-release as of June 2026):** Fixes a conflict between PySceneDetect and restoration models (upscaling/denoising) when both are enabled simultaneously — if your pipeline uses RVE's built-in scene detection alongside a restoration model, upgrading to 2.4.2 once stable resolves random crashes. Also adds decimal frame timestep support, input folder structure for output files, and fixes FFmpeg reading stopping randomly. **Current stable: 2.4.1.** Monitor releases at https://github.com/TNTwise/REAL-Video-Enhancer/releases.

Download: https://github.com/TNTwise/REAL-Video-Enhancer/releases

**Model currency check (2026-06-05):** No new Practical-RIFE models since v4.26 / v4.26.heavy (2024-09-21). **v4.22 is no longer the recommended model.** Practical-RIFE README recommends v4.25 as the default for most scenes and explicitly states v4.24+ is best for diffusion-generated video — use v4.25 as pipeline default.

Model selection for live-action / AI-generated video:
- **rife-v4.25** — **best for diffusion-generated video (Kling, Veo output) and general default.** Practical-RIFE project explicitly states v4.24+ is suitable for diffusion model video post-processing; v4.25 is the maintainer's recommended default for most scenes. Use this as our pipeline default.
- **rife-v4.25.lite** — lower-cost variant of v4.25 (2024-10-20). Use on server/headless environments with limited VRAM where full v4.25 OOMs. CLI: `-m rife-v4.25.lite` with the TNTwise binary. Quality is slightly below v4.25 full.
- **rife-v4.26.heavy** — highest quality variant of v4.26, significantly more GPU-intensive. Reserve for final delivery polish on important clips only (character close-ups, hero moments). Not in RVE GUI — CLI only via rife-ncnn-vulkan binary.
- **rife-v4.26** — latest standard model (2024-09-21). Similar quality to v4.25 on most content; use if v4.25 produces artifacts on a specific clip.
- **rife-v4.22** — prior recommendation (superseded). v4.24+ is the current guidance for diffusion video; retain only as legacy fallback.
- **rife-v4.6** — legacy fallback only (nihui original binary)

**CORRECTION from SC21:** Prior note that v4.26 is "anime-only" was incorrect. v4.26 is a general improvement. There is a separate `rife-v4.6-anime` variant for anime, which is unrelated.

### 3b. rife-ncnn-vulkan CLI (Headless / Scripted)

For scripted pipeline use (no GUI):

```bash
# TNTwise fork: https://github.com/TNTwise/rife-ncnn-vulkan/releases
# Latest binary release: v20250112 (Jan 12, 2025) — supports models through v4.26/v4.26.heavy
# Download the Linux binary
unzip rife-ncnn-vulkan-linux.zip

# Extract frames
ffmpeg -i clip.mp4 -r 24 frames/%08d.png

# Interpolate with v4.25 (best for diffusion/AI-generated video — see §3a)
# No -x TTA flag — deprecated in v4.22+
./rife-ncnn-vulkan -i frames/ -o interp_frames/ -m rife-v4.25 -j 1:2:2

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

**PySceneDetect v0.7.1 (in development, not yet released as of 2026-06-14, date TBD):** Will add:
- `--expand` flag to `split-video` (extends first/last clip to video boundaries — no footage lost)
- `expand_scenes_to_bounds()` API helper in scene manager module
- `backend` keyword argument for `scenedetect.detect()` — accepts `"opencv"` (default), `"pyav"`, or `"moviepy"` to select the video backend programmatically (useful in headless/server pipelines)

Monitor: https://github.com/Breakthrough/PySceneDetect/blob/main/website/pages/changelog.md

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

SVT-AV1 v4.1 (2026-03-23, confirmed current 2026-06-05) + FFmpeg 8.x libsvtav1 offers 30–50% smaller files vs H.264 at equivalent quality. Use for internal archive masters to save disk space.

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

**FFmpeg 8.0 "Huffman"** (released 2025-08-22) and **8.1 "Hoare"** (released 2026-03-17) include a built-in `whisper` audio filter (`af_whisper`). **Current stable: 8.1.1** (released 2026-05-04, confirmed current 2026-06-03) — maintenance patch fixing ALS/USAC decoder bugs; no new filters. All pipeline-relevant filters (drawvg, normalize, zscale, hqdn3d) are stable and unchanged in 8.1.1. — powered by whisper.cpp — that can generate SRT/VTT subtitles in one command without a separate tool.

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

## 11. Tool Version Status (confirmed 2026-06-30, SC168)

All post-production tools confirmed as of study cycle 168 (2026-06-30):

| Tool | Confirmed current version | Status |
|------|--------------------------|--------|
| FFmpeg stable | **8.1.2 (released 2026-06-17)** | No 8.1.3 as of 2026-06-30. All pipeline filters (drawvg, normalize, zscale, hqdn3d, loudnorm, whisper) stable and unchanged. |
| Practical-RIFE | v4.26 / v4.26.heavy (2024-09-21) | No v4.27 as of 2026-06-30 — v4.25 remains pipeline default for diffusion video |
| TNTwise REAL Video Enhancer | v2.4.1 stable (2026-01-02), v2.4.2 pre-release | v2.4.2 still pre-release as of 2026-06-30 — no new stable |
| TNTwise rife-ncnn-vulkan CLI | v20250112 (2025-01-12) | Latest binary release; supports models through v4.26/v4.26.heavy |
| PySceneDetect | v0.7.0 (2026-05-03) | v0.7.1 still in development — not released as of 2026-06-30 |
| SVT-AV1 | v4.1.0 (2026-03-23) | No v4.2 as of 2026-06-30 — current pipeline commands unchanged |
| Remotion | **v4.0.484 (released ~2026-06-29)** | `@remotion/effects` now includes `colorKey()`, `linearProgressiveBlur()`, `radialProgressiveBlur()` (SC161 — see §11a), `cornerPin()`, `lightTrail()` (see §11c), and **`linearGradient()`** (SC168 — see §11d). NVENC H.264/H.265 encoding on Linux/Windows added. **⚠️ v5.0 migration docs live but not yet released — see §11b.** |
| Instagram safe zones | unchanged | 320px bottom (organic), 120px right, 108px top, 60px left — re-confirmed SC147 via multiple 2026 sources |
| TikTok safe zones | unchanged from SC133 | ~184px right (164px base + ~20px Add to Playlist Jan 2026), 324px bottom, 130px top, 60px left — effective safe area 836×1466px |

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

**No action needed now** — v5 is not released. Monitor `remotion.dev/changelog` for release announcement.

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

## Post-Production Checklist

Before marking video as delivered:

- [ ] ffprobe colorspace check on each AI clip (see §1a) — tag BT.709 if metadata missing
- [ ] Check for temporal brightness flicker (pulsing exposure) — if present, apply §9a normalize filter (smoothing=15, strength=0.7, independence=0.0 for faces)
- [ ] Check for blocking/mosquito noise artifacts — if present, apply §9b hqdn3d=4:4:3:3 + unsharp (light mode for faces, moderate for backgrounds)
- [ ] All clips have identical resolution (1080×1920) and frame rate (30fps) before assembly
- [ ] LUT applied matching the scene mood (warm/neutral/cool — see table above)
- [ ] Dither applied (zscale dither=error_diffusion) on clips with gradient skies/walls
- [ ] Frame interpolation: run scene detection (§3d) first with PySceneDetect 0.7 (handles VFR AI clips correctly; install as `scenedetect-headless` on server), interpolate per-segment with rife-v4.25 (best for diffusion video; use TNTwise rife-ncnn-vulkan CLI fork v20250112 — supports v4.26; nihui binary tops out at v4.6), check ghost artifacts
- [ ] Instagram algorithm: our 30–60s ads are well under the 90s sweet spot and far under the 3-min non-follower cutoff — no action needed, but flag if a future brief pushes past 3 minutes
- [ ] Text overlays respect Instagram safe zone: bottom 320px, right 120px clear — see §5f
- [ ] TikTok repurpose: re-check right ~184px dead zone (wider than Instagram; Add to Playlist +20px Jan 2026, effective safe area ~836 × 1466px) — see §5g
- [ ] All text overlays composited (see text-overlay-compositing.md)
- [ ] Audio mixed per halal-audio.md — voiceover + SFX only, no instruments
- [ ] Final mix loudness: -14 LUFS ±1.0, true peak ≤ -1.5 dBTP
- [ ] Export: H.264, -pix_fmt yuv420p, -movflags +faststart, AAC 48kHz 256kbps
- [ ] ffprobe check passes (correct codec, resolution, fps confirmed)
- [ ] VMAF score ≥ 90 vs pre-export reference (if libvmaf available) — see §7
- [ ] AV1 archive: use `-svtav1-params tune=0` (VQ, perceptual) — NOT tune=3 (AVIF/still-image only) — see §5h. SVT-AV1-PSY fork archived Feb 2026; mainline SVT-AV1 4.1 + tune=0 is correct path.
- [ ] Brand badge overlays: prefer `drawvg` (§10) + `drawtext` chain in FFmpeg 8.1+ for exact #FC8434 pill shapes without Remotion — use `setcolor #FC8434` (direct hex, preferred) or `setrgba`, then `roundedrect`/`fill` (NOT `set_source_rgb`/`rectangle`)
- [ ] Remotion v4.0.484 effect options: use `radialProgressiveBlur()` for cinematic DOF vignette on character close-ups (center on face, endBlur=20–30px); use `linearProgressiveBlur()` for caption-bar blur on light backgrounds; use `linearGradient()` for dark scrim behind captions or #FC8434 brand accent (startColor/endColor with alpha); use `cornerPin()` for perspective overlays on truck surfaces (UV coords 0–1 range) — see §11a, §11c, §11d
- [ ] Remotion compositions: if any `<Audio>` component used, add explicit `optimizeFor="accuracy"` — v5 will change default to `"speed"` (§11b, forward-compat guard, low priority until v5 releases)
- [ ] Delivery to owner: WhatsApp **Document** share (not video message) for lossless 2GB delivery
- [ ] Final video watched end-to-end before delivery (MANDATORY per CLAUDE.md)

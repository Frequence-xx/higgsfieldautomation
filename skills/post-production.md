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

Download: https://github.com/TNTwise/REAL-Video-Enhancer/releases

Model selection for live-action / AI-generated video:
- **rife-v4.22** — **best for diffusion-generated video (Kling, Veo output)**. Maintainer explicitly notes this version for diffusion post-processing. Use this as default for our pipeline.
- **rife-v4.26.heavy** — highest quality variant of v4.26, significantly more GPU-intensive. Reserve for final delivery polish on important clips only (character close-ups, hero moments). Not in RVE GUI — CLI only via rife-ncnn-vulkan binary.
- **rife-v4.26** — latest standard model (2024-09-21), officially recommended for general use. Good fallback if v4.22 produces artifacts on a specific clip.
- **rife-v4.25** — previous recommended; community finds it matches v4.26 on real footage when bidirectional + dynamic optical flow enabled. No longer the first choice.
- **rife-v4.6** — legacy fallback only (nihui original binary)

**CORRECTION from SC21:** Prior note that v4.26 is "anime-only" was incorrect. v4.26 is a general improvement. There is a separate `rife-v4.6-anime` variant for anime, which is unrelated.

### 3b. rife-ncnn-vulkan CLI (Headless / Scripted)

For scripted pipeline use (no GUI):

```bash
# TNTwise fork: https://github.com/TNTwise/rife-ncnn-vulkan/releases
# Download the Linux binary
unzip rife-ncnn-vulkan-linux.zip

# Extract frames
ffmpeg -i clip.mp4 -r 24 frames/%08d.png

# Interpolate with v4.22 (best for diffusion/AI-generated video — see §3a)
# No -x TTA flag — deprecated in v4.22+
./rife-ncnn-vulkan -i frames/ -o interp_frames/ -m rife-v4.22 -j 1:2:2

# Reassemble at target fps
ffmpeg -r 48 -i interp_frames/%08d.png -i clip.mp4 \
  -map 0:v -map 1:a \
  -c:v libx264 -crf 18 -preset slow \
  -pix_fmt yuv420p -c:a copy \
  -r 30 clip_smooth.mp4
```

**Note:** Using nihui's binary (v4.6)? Keep `-x` flag. Using TNTwise binary with v4.22+? Drop it — TTA deprecated.

### 3c. Expected Quality Risks

- **Ghost artifacts** on complex motion — if seen, discard and use original
- **Face warping** on close-up character shots — high risk, skip interpolation for these
- **Blended frames** at hard cuts within a clip — ALWAYS split at scene changes before interpolating (§3d)

### 3d. Scene Change Detection Before RIFE (Mandatory Pre-Step)

RIFE blends across hard cuts, producing ghost frames. Detect and split clips at scene boundaries before interpolating each segment separately.

**Option A — PySceneDetect (recommended, handles splitting automatically):**
```bash
# Install: pip install scenedetect[opencv]
# Detect content-aware cuts and auto-split to segment_XXX.mp4 files
scenedetect -i clip.mp4 detect-content --threshold 27 split-video
# Lower threshold = more sensitive (catch subtle cuts); default 27 is safe for AI video
```

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

**Note:** Both platforms transcode H.264 to AV1 internally for delivery — that is Meta/TikTok's pipeline, not ours. Upload H.264; uploading AV1 causes a double-transcode with quality loss.

### 5c. Platform Specs Reference (2026)

| Platform | Resolution | FPS | Codec | Audio | Max File |
|----------|-----------|-----|-------|-------|---------|
| Instagram Reels | 1080×1920 | 30 | H.264 | AAC 256k 48kHz | 4 GB |
| TikTok | 1080×1920 | 30 | H.264 | AAC 192k 44.1kHz | 287.6 MB |
| YouTube Shorts | 1080×1920 | 30 | H.264 | AAC 256k 48kHz | 15 min |
| WhatsApp Status | 1080×1920 | 30 | H.264 | AAC 128k | **16 MB** (video message) |

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

### 5g. TikTok Safe Zone (Text / Logo Placement)

TikTok's right-side dead zone is significantly wider than Instagram's — this is the most common placement mistake when repurposing Reels assets for TikTok.

| Zone | Pixels from edge | What occupies it |
|------|-----------------|------------------|
| Bottom danger zone | Bottom **324px** (organic) / **370px** (ads/branded) | Caption, sound attribution, engagement buttons |
| Right danger zone | Right **164px** | Like, Comment, Share, Bookmark + "Add to Playlist" (added Jan 2026) |
| Top danger zone | Top **130px** | Back button, overflow menu |
| Left danger zone | Left **60px** | Profile avatar |

**Effective safe content area: ~916 × 1466px, centered.**

**Key difference vs Instagram:** TikTok's right dead zone is 164px vs Instagram's 120px. When reusing an asset designed for Instagram, any element within the right 164px may be hidden on TikTok. Re-check placement of logos, phone numbers, and CTAs before cross-posting.

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

SVT-AV1 v4.1 (2026-03-16) + FFmpeg 8.x libsvtav1 offers 30–50% smaller files vs H.264 at equivalent quality. Use for internal archive masters to save disk space.

```bash
# Check SVT-AV1 availability
ffmpeg -encoders 2>/dev/null | grep svtav1

# Archive encode (internal storage only)
ffmpeg -i normalized.mp4 \
  -c:v libsvtav1 -crf 30 -preset 6 \
  -svtav1-params tune=3 \
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
| `0` | VQ (default) | General video quality — PSNR-optimized |
| `1` | PSNR | Max PSNR for metrics; not perceptual |
| `2` | SSIM | SSIM-optimized; good for detailed textures |
| `3` | IQ (Image Quality) | Best perceptual quality, psychovisual. **Use this for our archive.**|
| `4` | MS-SSIM | Multi-scale SSIM; alternative to IQ for stills |

Use `tune=3` (IQ) for all Snelverhuizen archive encodes. SVT-AV1 4.0 also extended CRF range to 70 with quarter-step granularity — CRF 22–32 range remains our sweet spot.

**CRITICAL:** Do NOT upload AV1 to Instagram (rejected) or TikTok (triggers double-transcode). AV1 archive is for internal reference only — always deliver H.264 to platforms and owners.

**Preset guide (SVT-AV1):** Preset 0–4 = slow, highest quality. Preset 6 = good balance. Preset 8–12 = fast/realtime. Default `preset 6` is right for our archive use case.

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

**FFmpeg 8.0 "Huffman"** (released 2025-08-22) and **8.1 "Hoare"** (released 2026-03-17) include a built-in `whisper` audio filter (`af_whisper`) — powered by whisper.cpp — that can generate SRT/VTT subtitles in one command without a separate tool.

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
# Frame: 1080x1920. Badge: 600px wide, 80px tall, centered at y=1550
set_source_rgb 0.988 0.518 0.204   # #FC8434
arc  240 1550 40 1.5708 -1.5708    # left cap
rectangle 240 1510 600 80          # body
arc  840 1550 40 -1.5708 1.5708    # right cap
fill
# Text uses cairo pango layout — requires drawtext for actual text layer
EOF

ffmpeg -i graded.mp4 \
  -vf "drawvg=file=/opt/pipeline/overlays/brand_badge.vgs" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy \
  with_badge.mp4
```

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

**Limitation:** VGS is NOT SVG — it uses its own language. Static SVG files cannot be directly imported. Use for programmatically-defined shapes (rectangles, arcs, lines) where dynamic coordinates or exact brand colors matter. For complex imported vector art, continue using the PNG overlay workflow.

**Documentation:** https://ffmpeg.org/drawvg-reference.html

---

## Post-Production Checklist

Before marking video as delivered:

- [ ] ffprobe colorspace check on each AI clip (see §1a) — tag BT.709 if metadata missing
- [ ] Check for temporal brightness flicker (pulsing exposure) — if present, apply §9a normalize filter (smoothing=15, strength=0.7, independence=0.0 for faces)
- [ ] Check for blocking/mosquito noise artifacts — if present, apply §9b hqdn3d=4:4:3:3 + unsharp (light mode for faces, moderate for backgrounds)
- [ ] All clips have identical resolution (1080×1920) and frame rate (30fps) before assembly
- [ ] LUT applied matching the scene mood (warm/neutral/cool — see table above)
- [ ] Dither applied (zscale dither=error_diffusion) on clips with gradient skies/walls
- [ ] Frame interpolation: run scene detection (§3d) first, interpolate per-segment with rife-v4.22, check ghost artifacts
- [ ] Text overlays respect Instagram safe zone: bottom 320px, right 120px clear — see §5f
- [ ] TikTok repurpose: re-check right 164px dead zone (wider than Instagram) — see §5g
- [ ] All text overlays composited (see text-overlay-compositing.md)
- [ ] Audio mixed per halal-audio.md — voiceover + SFX only, no instruments
- [ ] Final mix loudness: -14 LUFS ±1.0, true peak ≤ -1.5 dBTP
- [ ] Export: H.264, -pix_fmt yuv420p, -movflags +faststart, AAC 48kHz 256kbps
- [ ] ffprobe check passes (correct codec, resolution, fps confirmed)
- [ ] VMAF score ≥ 90 vs pre-export reference (if libvmaf available) — see §7
- [ ] AV1 archive: use `-svtav1-params tune=3` (IQ) for perceptual quality — see §5h
- [ ] Brand badge overlays: prefer `drawvg` (§10) + `drawtext` chain in FFmpeg 8.1+ for exact #FC8434 pill shapes without Remotion
- [ ] Delivery to owner: WhatsApp **Document** share (not video message) for lossless 2GB delivery
- [ ] Final video watched end-to-end before delivery (MANDATORY per CLAUDE.md)

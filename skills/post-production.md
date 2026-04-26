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

### 2d. LUT Presets by Scene Mood

From cinematic-standards.md:

| Scene | Look | LUT/Treatment |
|-------|------|--------------|
| Family / arrival | Warm golden, amber highlights | Warm cinematic LUT (Kodak 2393 style) |
| Professional service | Neutral, clean whites | Skip LUT — eq saturation=1.05 only |
| Moving day / stress | Cool desaturated, blue shadows | Cool/teal LUT OR eq saturation=0.85 |
| Hero/reveal moment | High contrast warm, deep blacks | Warm high-contrast LUT |

### 2e. Free LUT Sources (No Cost)

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

### 3a. rife-ncnn-vulkan (Linux, free, GPU-accelerated)

**Use TNTwise fork** — supports up to rife-v4.25 (original nihui repo capped at v4.6):

```bash
# TNTwise fork: https://github.com/TNTwise/rife-ncnn-vulkan/releases
# Download the Linux binary from releases page
wget <latest-release-linux.zip-from-TNTwise-releases>
unzip rife-ncnn-vulkan-linux.zip
```

Model selection:
- **rife-v4.25** — latest, best quality, TTA mode deprecated (no longer needed)
- **rife-v4.6** — still fine if using nihui's original binary

Usage — 24fps to 30fps (1.25x speed):
```bash
# Extract frames
ffmpeg -i clip.mp4 -r 24 frames/%08d.png

# Interpolate with v4.25 (no -x TTA flag — deprecated in v4.25)
./rife-ncnn-vulkan -i frames/ -o interp_frames/ -m rife-v4.25 -j 1:2:2

# Reassemble at target fps
ffmpeg -r 48 -i interp_frames/%08d.png -i clip.mp4 \
  -map 0:v -map 1:a \
  -c:v libx264 -crf 18 -preset slow \
  -pix_fmt yuv420p -c:a copy \
  -r 30 clip_smooth.mp4
```

**Note:** Using nihui's binary (v4.6)? Keep `-x` flag. Using TNTwise binary with v4.25? Drop it.

### 3b. Expected Quality Risks

- **Ghost artifacts** on complex motion — if seen, discard and use original
- **Face warping** on close-up character shots — high risk, skip interpolation for these
- **Blended frames** at hard cuts within a clip — always trim clips cleanly before interpolating

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

For Instagram Reels (3,500–4,500 kbps target):

```bash
ffmpeg -i normalized.mp4 \
  -c:v libx264 -b:v 4000k -maxrate 4500k -bufsize 4500k \
  -preset slow -profile:v high -level:v 4.1 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -c:a aac -ar 48000 -b:a 256k -ac 2 \
  upload_reels.mp4
```

For TikTok (2,000–3,500 kbps acceptable):

```bash
ffmpeg -i normalized.mp4 \
  -c:v libx264 -b:v 3000k -maxrate 3500k -bufsize 3500k \
  -preset slow -profile:v main -level:v 3.1 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -c:a aac -ar 48000 -b:a 192k -ac 2 \
  upload_tiktok.mp4
```

### 5c. Platform Specs Reference (2026)

| Platform | Resolution | FPS | Codec | Audio | Max File |
|----------|-----------|-----|-------|-------|---------|
| Instagram Reels | 1080×1920 | 30 | H.264 | AAC 256k 48kHz | 1 GB |
| TikTok | 1080×1920 | 30 | H.264 | AAC 192k 44.1kHz | 287.6 MB |
| YouTube Shorts | 1080×1920 | 30 | H.264 | AAC 256k 48kHz | 15 min |
| WhatsApp Status | 1080×1920 | 30 | H.264 | AAC 128k | **16 MB** (video message) |

**-pix_fmt yuv420p is MANDATORY** for all platform uploads. Without it, Instagram and some players reject the file silently.

**-movflags +faststart** moves the moov atom to the front — required for web streaming and Instagram playback.

**H.265/HEVC:** TikTok accepts HEVC but H.264 re-compresses it anyway. Instagram does NOT reliably accept H.265. Use H.264 for all platforms.

**WhatsApp delivery to owner:** Regular video message = 16 MB limit (lossy auto-compression). To send the full-quality master file: use **Document share** (paperclip → Document) — supports up to **2 GB** with no recompression. Always deliver the master via document share, not as a video message.

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

## 6. VMAF Quality Scoring (Optional QA)

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
|-------|---------|
| ≥ 95 | Excellent — imperceptible loss |
| 85–94 | Good — minor compression visible only on close inspection |
| 70–84 | Acceptable — visible compression, borderline for delivery |
| < 70 | Reject — re-export at higher bitrate |

**Snelverhuizen threshold: ≥ 90 required before delivery.** If score < 90, increase CRF by -2 (lower = better) and re-export.

---

## 7. Hardware-Accelerated Export (Speed Optimization)

For faster export on long or repeated encodes. Output quality matches libx264 at equivalent settings.

### 7a. NVIDIA NVENC (NVIDIA GPU)

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

### 7b. VAAPI (Intel/AMD GPU, Linux)

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

## Post-Production Checklist

Before marking video as delivered:

- [ ] All clips have identical resolution (1080×1920) and frame rate (30fps) before assembly
- [ ] LUT applied matching the scene mood (warm/neutral/cool — see table above)
- [ ] Frame interpolation applied only if clip was visually choppy AND passed ghost-artifact check
- [ ] All text overlays composited (see text-overlay-compositing.md)
- [ ] Audio mixed per halal-audio.md — voiceover + SFX only, no instruments
- [ ] Final mix loudness: -14 LUFS ±1.0, true peak ≤ -1.5 dBTP
- [ ] Export: H.264, -pix_fmt yuv420p, -movflags +faststart, AAC 48kHz 256kbps
- [ ] ffprobe check passes (correct codec, resolution, fps confirmed)
- [ ] VMAF score ≥ 90 vs pre-export reference (if libvmaf available)
- [ ] Delivery to owner: WhatsApp **Document** share (not video message) for lossless 2GB delivery
- [ ] Final video watched end-to-end before delivery (MANDATORY per CLAUDE.md)

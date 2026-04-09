---
name: Captions and Titles
description: Remotion-based cinematic caption workflow — word-by-word animated captions synced to voiceover, title cards, lower-thirds, and platform-specific formatting.
autoInvoke: true
triggers:
  - captions
  - titles
  - lower third
  - text overlay
  - Remotion
  - subtitle
---

# Captions and Titles

Every video gets cinematic animated captions. No exceptions. No generic AI caption styling.

## Caption Workflow (Data Flow)

1. **ElevenLabs generates voiceover** with word-level timestamps
2. **Parse timestamps** into frame-number arrays:
   ```
   word_timestamps → [{text: "Your", start_ms: 0, end_ms: 500}, ...]
   frame_data → [{text: "Your", startFrame: 0, endFrame: 15}, ...]  // at 30fps
   ```
3. **Generate Remotion composition** with `CaptionComposition` component in `/opt/pipeline/captions/`
4. **Render to transparent video** (WebM with alpha or ProRes 4444):
   ```bash
   npx remotion render Captions --props='{"words": [...], "style": {...}}' --codec=vp8 --image-format=png
   ```
5. **Composite over main video** via FFmpeg:
   ```bash
   ffmpeg -i main.mp4 -i captions.webm -filter_complex "[0:v][1:v]overlay=0:0" -c:a copy output.mp4
   ```

## Typography Standards

- **Primary font:** Playfair Display (cinematic serif, free from Google Fonts)
- **Secondary font:** Cormorant Garamond (elegant alternative)
- **Weight:** Bold (700) for captions, Regular (400) for subtitles
- **Size:** 64px for 1080p master, scale proportionally for other formats
- **Color:** White (#FFFFFF) with active-word highlight (gold #FFD700 or brand accent)
- **Shadow:** `2px 2px 8px rgba(0,0,0,0.7)` — always. Text must be readable over any background.
- **Letter spacing:** 0.02em — slightly open for cinematic feel
- **Kerning:** Optical (not metric)

## Animation Styles

- **Word-by-word spring reveal** (default): Each word springs in as its voiceover moment arrives. Active word highlighted. Used for standard narration.
- **Fade reveal**: Words fade in smoothly. Used for quiet/emotional moments.
- **Block reveal**: Entire phrase appears at once with a subtle scale animation. Used for CTA text and key messages.

## Title Cards

- **Opening title:** Brand name + tagline, 2-3 second animated reveal. Cinematic serif font, centered, with subtle light leak or particle effect.
- **Closing title:** Brand name + contact info + CTA, 3-4 seconds. Same typography as opening for consistency.
- **Section titles** (if needed): Lower-third with brand accent color bar.

## Lower-Third Overlays

- **CTA text:** Phone number, website, "Call now" — positioned bottom-left with brand color bar
- **Service description:** Brief text describing the service shown — bottom-left, smaller font
- **Always composited, never AI-generated** — text must be pixel-perfect

## Platform-Specific Safe Zones

### 16:9 (YouTube, landscape)
- Captions: bottom 15% of frame, centered
- Title cards: center of frame
- Lower-thirds: bottom-left, 10% margin from edges

### 9:16 (Reels, TikTok, vertical)
- Captions: lower 30% of frame (above platform UI elements)
- AVOID: bottom 10% (navigation bar), top 15% (username/caption overlay)
- Title cards: center, slightly above midpoint
- Lower-thirds: avoid — use centered text instead

### 1:1 (Feed, square)
- Captions: bottom 20% of frame, centered
- Title cards: center
- Lower-thirds: bottom-left, similar to 16:9

## On-Screen Text Cards (Separate from Captions)

Some briefs specify on-screen text that is NOT voiceover captions — these are designed text elements with their own timing (e.g., "BINNEN MINUTEN DUIDELIJKHEID" during a hook shot).

**Rules for on-screen text cards:**
- Same Montserrat Black, ALL CAPS styling as captions
- Positioned **center of frame** (not lower-third like captions)
- Larger font size: 72px for hero text, 48px for secondary
- Animated entrance: scale-up spring or fade-in from below
- Animated exit: fade-out
- Can appear simultaneously with voiceover captions (text card at center, captions at 60% height)
- Rendered via Remotion as a separate overlay, composited in FFmpeg

**Timing:** On-screen text cards follow the shot list timing, NOT the voiceover timing. They are independent elements.

## Consistency Rules

- Same font, same weight, same animation style across ALL 50 videos in a month
- Same highlight color across all videos
- Same title card template across all videos
- The only things that change are the words and timing

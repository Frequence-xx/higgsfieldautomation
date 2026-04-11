---
name: Text Overlay Compositing
description: When and how to composite text overlays onto video — static drawtext, planar tracking for moving surfaces, Remotion for animated captions, and word-level timestamp requirements.
autoInvoke: true
triggers:
  - text overlay
  - compositing
  - drawtext
  - planar tracking
  - tracked text
  - branding overlay
  - truck text
  - logo overlay
negatives:
  - Do NOT invoke when generating hero frames or video clips (text goes on AFTER generation)
  - Do NOT invoke when doing caption/subtitle work only (use captions-and-titles.md for voiceover captions)
  - Do NOT invoke when the shot has no text or branding requirements
---

# Text Overlay Compositing

AI video models CANNOT reliably render text. "SNELVERHUIZEN.NL" becomes "www.sedeerhuiren.nl" in 40%+ of generations. ALL text and branding MUST be composited in post-production.

## Decision Matrix: When to Use Which Method

| Scenario | Method | Tool | Complexity |
|----------|--------|------|------------|
| Static camera, text in fixed position | Static overlay | FFmpeg drawtext | Low |
| Camera moves, text anchored to screen | Static screen overlay | FFmpeg drawtext | Low |
| Camera moves, text anchored to surface (truck panel) | Tracked overlay | Mocha AE planar tracking | High |
| Voiceover captions synced to speech | Animated captions | Remotion @remotion/captions | Medium |
| Animated title cards, name cards, CTAs | Animated overlay | Remotion composition | Medium |
| Logo watermark (corner, persistent) | Static overlay | FFmpeg overlay filter | Low |

## Method 1: FFmpeg Static Drawtext

Use when the camera is STATIC (locked tripod, no movement) and text should appear at a fixed screen position.

### Basic Drawtext Command

```bash
ffmpeg -i input.mp4 -vf "drawtext=\
fontfile=/usr/share/fonts/truetype/montserrat/Montserrat-Black.ttf:\
text='SNELVERHUIZEN.NL':\
fontcolor=white:\
fontsize=72:\
borderw=6:\
bordercolor=black:\
shadowcolor=black@0.7:\
shadowx=2:\
shadowy=2:\
x=(w-text_w)/2:\
y=h*0.6:\
enable='between(t,2,8)'" \
-c:a copy output.mp4
```

### Drawtext with Fade In/Out

```bash
ffmpeg -i input.mp4 -vf "drawtext=\
fontfile=/usr/share/fonts/truetype/montserrat/Montserrat-Black.ttf:\
text='SNELVERHUIZEN.NL':\
fontcolor=white@%{eif\\:if(lt(t-2,0.3),(t-2)/0.3,if(lt(8-t,0.3),(8-t)/0.3,1))\\:d\\:2}:\
fontsize=72:\
borderw=6:\
bordercolor=black@%{eif\\:if(lt(t-2,0.3),(t-2)/0.3,if(lt(8-t,0.3),(8-t)/0.3,1))\\:d\\:2}:\
x=(w-text_w)/2:\
y=h*0.6:\
enable='between(t,2,8)'" \
-c:a copy output.mp4
```

### Brand Logo Overlay (Corner Watermark)

```bash
ffmpeg -i input.mp4 -i /opt/pipeline/assets/logo-snelverhuizen.png \
-filter_complex "[1:v]scale=iw*0.08:-1[logo];[0:v][logo]overlay=W-w-20:H-h-20" \
-c:a copy output.mp4
```

### When FFmpeg Drawtext is Sufficient

- Camera is completely static (locked tripod)
- Camera pans but text is a screen-space overlay (lower-third, corner logo)
- Text does not need to "stick" to a physical surface in the scene
- No perspective change needed

## Method 2: Mocha AE Planar Tracking (Moving Surfaces)

Use when text MUST appear to be physically painted/printed on a moving surface (e.g., truck side panel during a camera orbit).

### Workflow

1. **Generate hero frame WITHOUT text** on the target surface (solid #FC8434 panel, no text)
2. **Animate via I2V** — focus on motion, include "no text, no logos" in negative prompt
3. **Import clip into After Effects** (or Natron/Blender for free alternative)
4. **Launch Mocha AE** (bundled with After Effects) on the clip
5. **Draw planar tracking spline** around the flat surface where text will go (truck side panel)
6. **Track forward** — Mocha tracks the plane's perspective changes across all frames
7. **Export corner-pin tracking data** to After Effects
8. **Create text layer** with exact brand typography:
   - Font: Montserrat Black, ALL CAPS
   - Color: White (#FFFFFF) on orange (#FC8434) background
   - Size: Proportional to surface area
9. **Apply corner-pin tracking data** to the text layer
10. **Match the scene:**
    - Add film grain matching the clip
    - Apply motion blur matching camera movement
    - Adjust opacity/blend for natural integration
    - Color-correct to match the lighting on the surface
11. **Export** with matching codec and resolution

### When Planar Tracking is Required

- Camera orbits around the truck and branding must appear on the cargo box
- Camera dollies past the truck and text must stay anchored to the panel
- Any shot where the branded surface undergoes perspective change

### Free Alternatives to After Effects + Mocha AE

- **Blender Motion Tracking:** Built-in planar tracker, free, steep learning curve
- **Natron:** Open-source compositing, has a planar tracker node
- **HitFilm (free tier):** Has point tracking, limited planar

### When to Skip Tracking Entirely

If the truck surface is visible but the camera is static or barely moving:
- Use FFmpeg drawtext positioned to match the surface
- Accept that it will look like a screen overlay, not a physical label
- For social media (9:16 vertical, viewed on phone), this is often acceptable

## Method 3: Remotion for Animated Captions

Use for voiceover captions synced to speech timing. See `captions-and-titles.md` for full specification.

### Word-Level Timestamps Requirement

**MUST obtain word-level timestamps from actual transcription.** NEVER estimate or calculate timestamps manually.

Sources for word-level timestamps:
1. **ElevenLabs API** — returns word-level timing with voiceover generation (preferred)
2. **Whisper transcription** — run on generated audio file for word-level alignment
3. **@remotion/install-whisper-cpp** — local whisper for offline timestamp extraction

### Remotion Caption Rendering Pipeline

```
1. Generate voiceover (ElevenLabs) → get word timestamps
2. Convert timestamps to frame numbers (at 30fps)
3. Create Remotion composition with @remotion/captions
4. Render to transparent WebM (VP8 with alpha)
5. Composite over main video via FFmpeg overlay filter
```

### Animated Title Cards and CTAs via Remotion

For non-caption text elements (title cards, name cards, CTAs), render as separate Remotion compositions:

```bash
npx remotion render TitleCard --props='{"text":"SNELVERHUIZEN","subtitle":"Betaalbaar & Betrouwbaar"}' \
  --codec=vp8 --image-format=png --output=title.webm
```

Then composite:

```bash
ffmpeg -i main.mp4 -i title.webm \
  -filter_complex "[0:v][1:v]overlay=0:0:enable='between(t,0,3)'" \
  -c:a copy output.mp4
```

## Method 4: Static Screen Overlay (Simplest for Branding)

When the truck drives through frame or the camera moves, and tracking is not worth the effort:

- Place "SNELVERHUIZEN.NL" as a persistent lower-third or title card
- The text lives in screen space, not world space
- Professional and clean for social media content
- Use FFmpeg drawtext or Remotion overlay

## Compositing Quality Checklist

After compositing any text overlay:

- [ ] Text is pixel-sharp (no blur from scaling)
- [ ] Font matches brand spec (Montserrat Black, ALL CAPS)
- [ ] Colors match brand spec (white text, #FC8434 orange if on brand surface)
- [ ] Text does not overlap with subject's face or important visual elements
- [ ] Tracked text follows the surface naturally (if using planar tracking)
- [ ] Film grain and motion blur match the underlying clip
- [ ] Text appears and disappears cleanly (fade in/out, not hard cut)
- [ ] Text is within platform safe zones (see captions-and-titles.md)
- [ ] No encoding artifacts around text edges

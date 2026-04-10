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

- **Primary font:** Montserrat (bold sans-serif, free from Google Fonts) — industry standard for short-form video captions. 31% higher mobile readability than serif fonts.
- **Secondary font:** Anton (ultra-heavy, free from Google Fonts) — alternative for extra-bold headlines
- **Weights:** Black (900) for titles/hooks/names, Bold (700) for voiceover captions, SemiBold (600) for name card subtitles
- **Size:** 55–75px for voiceover captions, 80–100px for title/hook text, 48–64px for name cards (on 1080x1920 canvas)
- **Color:** White (#FFFFFF) with active-word highlight (yellow #F7C204 or brand accent)
- **Outline:** `-webkit-text-stroke: 6px black; paint-order: stroke fill;` — ALWAYS. Outline is more reliable than shadow alone for readability on any background.
- **Shadow:** `2px 2px 8px rgba(0,0,0,0.7)` — in addition to outline, for depth.
- **Letter spacing:** 0.02em — slightly open for cinematic feel
- **Text transform:** ALL CAPS for titles, names, and voiceover captions
- **Max words per block:** 4–6 words across 1–2 lines (max 42 characters per line)

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

### 9:16 (Reels, TikTok, vertical) — UPDATED WITH PIXEL VALUES

**Universal cross-platform safe zone (TikTok + Reels + Shorts):**
- Safe area: 840 x 1280 pixels, centered in 1080x1920 frame
- Top margin: 320px (avoids username, sound label, subscribe button)
- Bottom margin: 320px (avoids caption bar, CTA, navigation, playback bar)
- Side margins: 120px each (avoids engagement buttons on right)

**Voiceover captions:** Zone C — 1150–1350px from top (above bottom danger zone)
**Name cards:** Zone B — 800–1050px from top (center-lower)
**Title/hook text:** Zone A — 480–720px from top (center)
**AVOID:** Bottom 320px (platform UI), top 320px (platform UI), right 120px (buttons)

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

## Name Card Design Rules (Person Introductions)

Name cards are separate from voiceover captions. They identify a person on screen and have their own timing, animation, and positioning.

### Anatomy

```
┌─────────────────────────────────┐
│  ■ FAROUQ AL-RASHID             │  <- Name: Montserrat Black (900), 56px
│    Oprichter, Snel Verhuizen    │  <- Title: Montserrat SemiBold (600), 36px, 80% opacity
└─────────────────────────────────┘
     ^
     Accent bar (brand color, 4px wide, left edge)
```

### Specifications

| Element | Value |
|---------|-------|
| Name font | Montserrat Black (900), 48–64px, white (#FFFFFF) |
| Title/role font | Montserrat SemiBold (600), 32–40px, white at 80% opacity |
| Background | Semi-transparent black: rgba(0,0,0,0.6) with 8px border-radius |
| Accent bar | 4px wide brand color bar on left edge (optional) |
| Padding | 16px horizontal, 12px vertical |
| Max width | 80% of frame width |
| Shadow | Text: 2px 2px 6px rgba(0,0,0,0.8). Box: 0 4px 12px rgba(0,0,0,0.3) |

### Positioning (9:16 / 1080x1920)

- **Vertical zone:** 800–1050px from top (center-lower area)
- **Horizontal:** Centered, or left-aligned with 120px left margin
- **NEVER** in the same vertical zone as voiceover captions

### Timing

| Parameter | Value |
|-----------|-------|
| Appear | 0.5–1.0s after person first appears on screen |
| Duration | 3–5 seconds |
| Fade-in | 200–300ms (slide-up + opacity) |
| Fade-out | 200–300ms |
| Buffer after exit | 500ms minimum before any other text in same zone |

### When to Show

- First appearance of a person in the video
- When switching between speakers
- NOT needed if only one person and already introduced in the hook
- In a 15–30 second ad: show once, 3–5 seconds, in the first 5–10 seconds

### Animation

Default: **Slide-up reveal** — text slides up 20px from below final position while fading in (200–300ms). Exit: fade out over 200ms.

---

## Timing Rules to Prevent Overlap

### The 2-Layer Maximum Rule

**NEVER show more than 2 text layers simultaneously.** This is the single most important rule for professional-looking captions.

### Vertical Zone System (9:16 / 1080x1920)

Three mutually exclusive vertical zones prevent spatial overlap:

```
┌──────────────────────────┐  0px
│   PLATFORM UI (avoid)    │
├──────────────────────────┤  320px
│                          │
│   ZONE A: Title/Hook     │
│   (480–720px from top)   │
│                          │
│   ZONE B: Name Cards     │
│   (800–1050px from top)  │
│                          │
├──────────────────────────┤  1150px
│   ZONE C: Voiceover      │
│   Captions               │
│   (1150–1350px from top) │
├──────────────────────────┤  1400px
│   PLATFORM UI (avoid)    │
└──────────────────────────┘  1920px
```

### Conflict Resolution

| Scenario | Solution |
|----------|----------|
| Name card + voiceover caption at same time | Name in Zone B, caption in Zone C |
| Title + voiceover caption | Title in Zone A, caption in Zone C |
| Title + name card | Show sequentially (title first, then name card) |
| All three needed at once | NEVER — redesign the timing |

### Caption Sync Timing

| Parameter | Value |
|-----------|-------|
| Pre-roll | 50–100ms before spoken word |
| Post-hold | 50–100ms after word ends |
| Gap between blocks | 150–250ms (minimum 2 frames at 30fps) |
| Display duration | 0.3s per word + 0.5s buffer (minimum) |
| Maximum display | 6 seconds per block |
| Ideal display | 2–3 seconds per block |

### Choreography Template (15–30s Ad)

```
0.0s — Hook title appears (Zone A, center)
1.5s — Hook title fades out
2.0s — Name card slides in (Zone B) + voiceover captions begin (Zone C)
5.0s — Name card fades out
5.5s — Voiceover captions continue alone (Zone C)
...
25.0s — Voiceover ends
25.5s — CTA appears (Zone A, center)
28.0s — CTA fades out
30.0s — End
```

---

## Professional Animation Patterns

### Word-by-Word Highlight (Default for Voiceover Captions)

The standard for professional short-form video in 2026. Active word changes color as it is spoken.

- All words visible in white (#FFFFFF) with black outline (6px)
- Active word turns yellow (#F7C204) or brand accent color
- Active word may scale to 1.05x (subtle)
- Word highlights 50–100ms BEFORE it is spoken
- Each word stays highlighted for full spoken duration + 50–100ms
- Spring config: damping 12, stiffness 200, mass 1.0

**Performance data:** +15% engagement lift for business/educational content. 70% of top creators use a variation.

### Spring Pop (For Name Cards and Title Text)

- Text enters with spring animation: scale 0 -> 1.0 with slight overshoot
- Spring config: damping 10, mass 0.5, stiffness 150
- Duration to settle: ~300ms
- Exit: fade out over 200ms

### Slide-Up Reveal (For Name Cards)

- Text slides up from 20px below final position
- Opacity: 0 -> 1 during slide
- Duration: 200–300ms
- Optional: accent bar slides in from left simultaneously

### Block Reveal (For Hook Text / CTA)

- Entire phrase appears at once
- Scale: 0.95 -> 1.0 with spring
- Optional: background box fades in 100ms before text
- Duration: 200ms

### AVOID (Amateur Patterns)

- Typewriter effects (dated)
- Spinning or rotating text
- Neon glow effects
- Flashy color-cycling
- Excessive bounce/wobble
- Multiple simultaneous animation types

---

## Typography Hierarchy

Four distinct text roles, each with its own visual weight. Never mix them up.

| Role | Font | Weight | Size (px) | Color | Outline | ALL CAPS |
|------|------|--------|-----------|-------|---------|----------|
| **Title/Hook** | Montserrat | Black (900) | 80–100 | White | 6–8px black | YES |
| **Name (card)** | Montserrat | Black (900) | 48–64 | White | 6px black | YES |
| **Name title** | Montserrat | SemiBold (600) | 32–40 | White 80% | 4px black | No |
| **Voiceover Caption** | Montserrat | Bold (700) | 55–75 | White (highlight: #F7C204) | 6px black | YES |
| **CTA** | Montserrat | Bold (700) | 48–64 | White or brand | 6px black | YES |

### Why Montserrat (Not Playfair Display)

Research finding: Bold sans-serif fonts score 31% higher on mobile readability tests than serif fonts. For fast-scrolling 9:16 video viewed at arm's length on a phone, Montserrat Black is the industry standard. Playfair Display (serif) is elegant but harder to read at speed. **Switch primary font to Montserrat for all caption roles.**

### Outline vs Shadow

**Use BOTH.** The outline ensures readability on any background. The shadow adds depth.

```css
/* Recommended text treatment */
-webkit-text-stroke: 6px black;
paint-order: stroke fill;
text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
```

If the Remotion paint-order approach does not work, render text twice: first pass with large black shadow/stroke, second pass with white fill on top.

---

## @remotion/captions Integration

### Preferred Implementation (Replaces Custom CaptionComposition)

Use the official `@remotion/captions` package with `createTikTokStyleCaptions()` for word-level highlighting.

```bash
npx remotion add @remotion/captions
```

```tsx
import { createTikTokStyleCaptions, parseSrt } from '@remotion/captions';

// Create word-level pages
const { pages } = createTikTokStyleCaptions({
  captions,
  combineTokensWithinMilliseconds: 500, // Word-by-word
});

// Render with highlight
{currentPage?.tokens.map((token, i) => {
  const isActive = currentTimeMs >= token.fromMs && currentTimeMs < token.toMs;
  return (
    <span style={{
      color: isActive ? '#F7C204' : '#FFFFFF',
      transform: `scale(${isActive ? 1.05 : 1})`,
      WebkitTextStroke: '6px black',
      paintOrder: 'stroke fill',
      textShadow: '2px 2px 8px rgba(0,0,0,0.7)',
      whiteSpace: 'pre',
    }}>
      {token.text}
    </span>
  );
})}
```

### Key Parameter: combineTokensWithinMilliseconds

- `500` — Word-by-word (recommended for business/ad content)
- `1200` — Phrase-by-phrase (calmer, educational content)
- `2000` — Sentence-level (subtitle-style)

### Critical: whiteSpace: 'pre'

Always set `whiteSpace: 'pre'` on the caption container. Spaces are used as delimiters and omitting this causes words to collapse.

---

## Consistency Rules

- Same font, same weight, same animation style across ALL 50 videos in a month
- Same highlight color across all videos
- Same title card template across all videos
- Same name card template across all videos
- The only things that change are the words and timing

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
negatives:
  - Do NOT invoke when generating hero frames or animating video clips (no text at generation stage)
  - Do NOT invoke when performing visual QA on raw clips before post-production
  - Do NOT invoke when doing brief intake or shot list planning
---

# Captions and Titles

Every video gets cinematic animated captions. No exceptions. No generic AI caption styling.

## Caption Workflow (Data Flow)

1. **Extract word-level timestamps** — three options in priority order:

   **Option A: ElevenLabs Forced Alignment (primary, paid)** — TWO endpoints exist, only ONE is fully verified for word-level timestamps:
   - ✅ **CORRECT: `POST /v1/forced-alignment`** — returns word AND character-level timestamps (submit audio + transcript after TTS generation). Supports Dutch natively (150+ languages, introduced 2025-04). Works with both `eleven_multilingual_v2` and `eleven_v3`.
   - ⚠️ **CONDITIONAL: `POST /v1/text-to-speech/{voice_id}/with-timestamps`** — returns only CHARACTER-level timestamps with `eleven_multilingual_v2` (root cause of V2 caption sync issues 2026-04-09/10). With `eleven_v3` (launched Feb 2026), this endpoint appears to return per-character AND per-word timestamps — but this is **unverified in production**. Do NOT rely on it for word-by-word highlighting until tested; fall back to `/v1/forced-alignment`.
   - Recommended Dutch voices (verified 2026-04-16): male warm 30-40 = `hLnc7y4d152WGG2BQlAY` (Jaimie Amsterdam), female warm 30-40 = `DiUBVrSFwkMaPz4XqWvR` (Jolanda)
   - **Recommended model: `eleven_v3`** (launched 2026-02-12, new flagship — 70+ languages, higher emotional range, audio-tag emotion control via `[whispers]`/`[excited]` tags). Replaces `eleven_multilingual_v2` as primary recommendation. `eleven_multilingual_v2` remains valid fallback if `eleven_v3` produces English-accented Dutch on a specific voice.

   **Option B: WhisperX (free, $0, use when ElevenLabs credits are low)**
   Dutch (`nl`) supported via wav2vec2 forced alignment. **Version requirement: `>=3.8.5`** — v3.8.2 fixed a wildcard alignment bug; v3.8.4 fixed blank_id for HuggingFace models and restored digit/symbol timestamps ("085 3331133", "4,9 ster"); v3.8.5 (April 2026) pins torchvision/torchcodec for torch 2.8 compatibility + includes PR #1347 fix (SRT/ASS subtitle cue timestamps now derived from word-level data, not VAD segment boundaries — previously caused premature cue display). Older versions silently produce wrong timestamps.

   **Dependency requirement (v3.8.5+):** `faster-whisper>=1.2.0` is required. Install both:
   ```bash
   pip install "faster-whisper>=1.2.0" "whisperx>=3.8.5"
   ```
   **Model recommendation for Dutch:** Use `large-v3-turbo` instead of `large-v2` — performs identically to large-v2 on Dutch (v3 pure has Dutch regression; turbo reverts to v2-level accuracy) but transcribes ~3–4x faster on CPU. Pass `--model large-v3-turbo` in the CLI.

   ```bash
   # CPU usage — always specify --device cpu explicitly
   # large-v3-turbo: same Dutch accuracy as v2, ~3x faster on CPU (via faster-whisper)
   # Add --max_line_width 40 --max_line_count 2 to enforce 42-char line limit in ASS/SRT output
   whisperx voiceover.wav --model large-v3-turbo --language nl --batch_size 4 --compute_type int8 --device cpu \
     --max_line_width 40 --max_line_count 2
   # Fallback if turbo produces hallucinations on this recording: --model large-v2
   # Output: voiceover.json → segments[].words → [{word, start, end, score}]
   ```

   **⚠️ Dutch last-word timestamp bug (WhisperX issue #749 — open, unfixed):** For Dutch (`nl`), wav2vec2 alignment extends the `end` of the final word (and sometimes mid-segment words) into trailing silence — overestimating duration by 4–5 seconds. This is a known unfixed issue with the Dutch alignment model. **Always run this post-processing fix before converting to Remotion format:**

   ```python
   import json, subprocess

   def _audio_duration(path):
       r = subprocess.run(
           ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", path],
           capture_output=True, text=True
       )
       for s in json.loads(r.stdout)["streams"]:
           if s["codec_type"] == "audio":
               return float(s["duration"])
       return None

   def fix_dutch_whisperx_timestamps(words, audio_path):
       """Cap last-word end to audio duration; enforce monotonic ordering."""
       duration = _audio_duration(audio_path)
       fixed = [dict(w) for w in words]
       if duration:
           for w in fixed:
               if "end" in w:
                   w["end"] = min(w["end"], duration)
       for i in range(len(fixed) - 1):
           if "end" in fixed[i] and "start" in fixed[i + 1]:
               fixed[i]["end"] = min(fixed[i]["end"], fixed[i + 1]["start"])
       return fixed
   ```

   Call this on the flat word list BEFORE the Remotion converter below.

   Convert to Remotion Caption format (use startMs/endMs, not frame numbers):
   ```python
   import json
   result = json.load(open("voiceover.json"))
   words = [w for seg in result["segments"] for w in seg.get("words", [])]
   words = fix_dutch_whisperx_timestamps(words, "voiceover.wav")  # Dutch bug fix
   captions = [
       {"text": w["word"], "startMs": int(w["start"] * 1000), "endMs": int(w["end"] * 1000),
        "timestampMs": int((w["start"] + w["end"]) / 2 * 1000), "confidence": w.get("score", 1)}
       for w in words if "start" in w
   ]
   ```

   **WhisperX hallucination prevention (automatic):**
   - VAD pre-processing enabled by default — strips silence, eliminates phantom hallucinations
   - `condition_on_prev_text=False` by default — prevents context bleeding between segments
   - Use `large-v3-turbo` (preferred) or `large-v2` for Dutch. Do NOT use `large-v3` — it regresses on Dutch vs v2. Turbo is based on v3 architecture but with 4 decoder layers (vs 32 in v3/v2) and reverts to v2-level accuracy while being ~3x faster.

   **Option C: @remotion/install-whisper-cpp with DTW (free, Remotion-native, no Python needed)**
   Uses whisper.cpp with Dynamic Time Warping on attention weights — no separate language model. Works for Dutch without a wav2vec2 model. Integrates directly with `toCaptions()`.

   **Version requirements for large-v3-turbo:** Remotion v4.0.229+ AND whisper.cpp v1.8.x+. Do NOT use `version: '1.5.5'` with turbo — it silently fails.

   ```typescript
   import { installWhisperCpp, transcribe, toCaptions } from '@remotion/install-whisper-cpp';
   await installWhisperCpp({ version: '1.8.4', printOutput: false }); // once; v1.8.4 required for large-v3-turbo
   const result = await transcribe({
     inputPath: 'voiceover.wav',
     model: 'large-v3-turbo',    // ~3x faster than large-v2, same Dutch accuracy (Remotion v4.0.229+)
     language: 'nl',
     tokenLevelTimestamps: true,  // enables --dtw for word-level accuracy
     flashAttention: false,       // keep false on CPU; set true only with CUDA GPU
   });
   const { captions } = toCaptions({ whisperCppOutput: result });
   // captions → Caption[] ready for createTikTokStyleCaptions()
   // timestampMs field uses t_dtw (DTW-derived) when tokenLevelTimestamps: true —
   // this is the most accurate single-point timestamp available from whisper.cpp.
   // Without tokenLevelTimestamps, timestampMs falls back to (startMs + endMs) / 2.
   ```

   **`additionalArgs` escape hatch:** Pass custom whisper.cpp CLI flags via `additionalArgs: ['--no-prints', '--print-special']` (string[] or key-value pair arrays). Only needed for non-standard whisper.cpp builds.

   Choose Option C when: no Python env available, CPU-only server (avoids loading second neural network), or pure TypeScript pipeline.

   **Option D: @remotion/whisper-web (browser/WASM, free, NOT for Dutch production)**
   Browser-side transcription via WebAssembly. No Node.js or Python required. Uses whisper.cpp compiled to WASM.

   **⚠️ HARD LIMIT — do NOT use for Snel Verhuizen Dutch voiceovers:** Supported models are `tiny`, `tiny.en`, `base`, `base.en`, `small`, `small.en` only. No `large-v3-turbo` in WASM. Small models produce significantly worse Dutch accuracy than large-v3-turbo. Word alignment will drift and caption sync will be poor.

   ```typescript
   import { transcribe, toCaptions, canUseWhisperWeb } from '@remotion/whisper-web';
   // Requires: cross-origin isolation headers (COOP + COEP) for SharedArrayBuffer
   const check = await canUseWhisperWeb();
   if (check.supported) {
     const result = await transcribe({ audioData: float32Array, model: 'small', language: 'nl' });
     const { captions } = toCaptions({ whisperWebOutput: result });
   }
   ```

   Version: 4.0.448 (May 2026). Only use Option D for: browser-only apps with no server component, rapid prototyping, or languages where small models are sufficient (English/Spanish).

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
- **Color:** White (#FFFFFF) with active-word highlight (brand orange #FC8434)
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

**MUST NOT show more than 2 text layers simultaneously.** This is the single most important rule for professional-looking captions.

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
|----------|---------|
| Name card + voiceover caption at same time | Name in Zone B, caption in Zone C |
| Title + voiceover caption | Title in Zone A, caption in Zone C |
| Title + name card | Show sequentially (title first, then name card) |
| All three needed at once | NEVER — redesign the timing |

### Caption Sync Timing

| Parameter | Value |
|-----------|-------|
| Pre-roll | MUST appear 50–100ms before spoken word |
| Post-hold | MUST hold 50–100ms after word ends |
| Gap between blocks | MUST be 150–250ms (minimum 2 frames at 30fps) |
| Display duration | MUST be 0.3s per word + 0.5s buffer (minimum) |
| Maximum display | MUST NOT exceed 6 seconds per block |
| Ideal display | 2–3 seconds per block |

**WhisperX drift:** wav2vec2 alignment has inherent ±50–100ms timing drift. The 50ms pre-roll in this table exists specifically to compensate. Do not reduce it. With whisper.cpp Option C + `tokenLevelTimestamps: true`, drift is lower because `t_dtw` is used directly — but keep 50ms pre-roll as minimum regardless.

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
- Active word turns brand orange (#FC8434)
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
| **Voiceover Caption** | Montserrat | Bold (700) | 55–75 | White (highlight: #FC8434) | 6px black | YES |
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

### Full API (v4.0.447+)

| Export | Purpose |
|--------|---------|
| `createTikTokStyleCaptions()` | Groups `Caption[]` into pages with per-token timing for word highlight |
| `parseSrt()` | Parses SRT → `Caption[]` — **block-level only, NO word timestamps** |
| `serializeSrt()` | Serializes `Caption[]` back to SRT string (round-trip) |
| `CaptionsInternals.ensureMaxCharactersPerLine()` | Splits `Caption[]` into line segments with max char limit + orphan prevention |
| `Caption` | Type: `{ text, startMs, endMs, timestampMs, confidence }` |

No `parseWebVtt()` exists in this package. No `convertToCaptions()` either — that was deprecated at v4.0.216; use `toCaptions()` from `@remotion/install-whisper-cpp` instead.

### CRITICAL: parseSrt() does NOT give word-level timestamps

`parseSrt()` returns one `Caption` per SRT block with a single `startMs`/`endMs` for the entire phrase. If you feed WhisperX `--output_format srt` through `parseSrt()`, word-by-word highlighting will NOT work — every word in the block gets the same timing and the orange highlight stays stuck.

**For word-by-word highlight, use WhisperX JSON or whisper.cpp output (Options B/C above).** Use `parseSrt()` only for subtitle-style display where you show one phrase at a time with no per-word highlight.

### Preferred Implementation

```bash
npx remotion add @remotion/captions
```

```tsx
import { createTikTokStyleCaptions } from '@remotion/captions';

// captions = Caption[] from WhisperX JSON, whisper.cpp toCaptions(), or ElevenLabs
const { pages } = createTikTokStyleCaptions({
  captions,
  combineTokensWithinMilliseconds: 500, // word-by-word
});

{currentPage?.tokens.map((token, i) => {
  const isActive = currentTimeMs >= token.fromMs && currentTimeMs < token.toMs;
  return (
    <span key={i} style={{
      color: isActive ? '#FC8434' : '#FFFFFF',
      transform: `scale(${isActive ? 1.05 : 1})`,
      WebkitTextStroke: '6px black',
      paintOrder: 'stroke fill',
      textShadow: '2px 2px 8px rgba(0,0,0,0.7)',
      whiteSpace: 'pre',
      display: 'inline-block',
    }}>
      {token.text}
    </span>
  );
})}
```

### Enforcing 42-char Line Limit with ensureMaxCharactersPerLine

The skill file specifies max 42 characters per line. Enforce this automatically with the built-in utility — do not hand-count:

```typescript
import { CaptionsInternals } from '@remotion/captions';

const { segments } = CaptionsInternals.ensureMaxCharactersPerLine({
  captions,          // Caption[] from WhisperX JSON or toCaptions()
  maxCharsPerLine: 42,
});

// segments: Caption[][] — each inner array is one display line
// Orphan prevention built-in: if <4 words remain and line is >50% full,
// forces an early break to avoid stranded 1-2 word tails.
// Feed each segment into createTikTokStyleCaptions() as its own Caption[].
```

Use this BEFORE `createTikTokStyleCaptions()` when you have long Dutch phrases that would otherwise overflow the 1080px canvas width.

### Key Parameter: combineTokensWithinMilliseconds

- `500` — Word-by-word (recommended for business/ad content)
- `1200` — Phrase-by-phrase (calmer, educational content)
- `2000` — Sentence-level (subtitle-style, matches parseSrt() input)

### Critical: whiteSpace: 'pre'

Always set `whiteSpace: 'pre'` on the caption container. Spaces are used as delimiters and omitting this causes words to collapse.

### Rounded Corner Caption Backgrounds — Remotion Only

**FFmpeg `drawtext`/`drawbox` cannot produce rounded corners.** The `box=1` parameter draws a hard rectangle only. Neither ASS subtitle format nor any FFmpeg filter supports border-radius natively.

**The ONLY correct path for rounded caption pill/background is Remotion CSS:**

```tsx
// Caption background pill with rounded corners
<div style={{
  backgroundColor: 'rgba(0, 0, 0, 0.72)',
  borderRadius: 12,
  padding: '8px 20px',
  display: 'inline-block',
}}>
  {currentPage?.tokens.map((token, i) => {
    const isActive = currentTimeMs >= token.fromMs && currentTimeMs < token.toMs;
    return (
      <span key={i} style={{
        color: isActive ? '#FC8434' : '#FFFFFF',
        WebkitTextStroke: '3px black',
        paintOrder: 'stroke fill',
        whiteSpace: 'pre',
        fontFamily: 'Montserrat',
        fontWeight: 700,
        fontSize: 64,
        transform: `scale(${isActive ? 1.05 : 1})`,
        display: 'inline-block',
      }}>
        {token.text}
      </span>
    );
  })}
</div>
```

**`borderRadius` values by use case:**
- Voiceover caption pill: `borderRadius: 12` (subtle rounding, feels native)
- Name card box: `borderRadius: 8` (already specified above — matches the spec)
- CTA button style: `borderRadius: 24` (fully rounded, pill shape)

If FFmpeg compositing is required without Remotion, generate a rounded-rect PNG background per phrase at pre-render time (ImageMagick or Pillow), then overlay it on video with `ffmpeg -i video -i pill.png -filter_complex [0][1]overlay=...`.

### ASS Karaoke — FFmpeg-Native Fallback (No Remotion)

When Remotion is unavailable, WhisperX can generate ASS subtitle files with word-level karaoke timing in a single CLI call:

```bash
whisperx voiceover.wav \
  --model large-v3-turbo \
  --language nl \
  --device cpu --compute_type int8 --batch_size 4 \
  --highlight_words True \
  --output_format ass \
  --max_line_width 40 \
  --max_line_count 2 \
  --output_dir .
# Output: voiceover.ass — contains \k tags with per-word timing
# Fallback: --model large-v2 if turbo hallucinates on this recording
```

Burn subtitles into video:
```bash
ffmpeg -i main.mp4 -vf "ass=voiceover.ass" -c:a copy output_captioned.mp4
```

**ASS color format is BGR, NOT RGB** — this is the #1 mistake:
- Brand orange `#FC8434` in ASS hex = `&H003484FC` (bytes reversed: R→FC, G→84, B→34 → write as BB GG RR → 34 84 FC)
- Writing `&H00FC8434` renders as BLUE, not orange
- White (pre-highlight) = `&H00FFFFFF` | Black outline = `&H00000000`

**`\k` vs `\kf` in ASS karaoke:**
- `\k` — instant color switch at word start (correct for speech ads)
- `\kf` — left-to-right sweep (traditional karaoke look, odd for voiceover)
- WhisperX generates `\k` by default — do not change it

**Style override to match brand:** Edit the `[V4+ Styles]` section of the generated `.ass` file:
```
Style: Default,Montserrat Bold,55,&H00FFFFFF,&H003484FC,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,2,2,10,10,40,1
```
Fields: Name, Font, Size, PrimaryColour (white), SecondaryColour (orange `&H003484FC`=highlight), OutlineColour (black), BackColour (semi-transparent black), Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding.

**Limitations of ASS/FFmpeg vs Remotion:**
- No rounded corners (libass rectangle only)
- No spring/scale animation on active word
- No per-frame CSS control
- ASS is correct fallback when: Remotion not installed, pure server-side pipeline, or quick prototype

---

## Consistency Rules

- MUST use same font, same weight, same animation style across ALL 50 videos in a month
- MUST use same highlight color across all videos
- MUST use same title card template across all videos
- MUST use same name card template across all videos
- The only things that change are the words and timing

---
name: Halal Audio
description: End-to-end halal audio pipeline — ElevenLabs Dutch voiceover, nasheed sourcing, ambient SFX retrieval, FFmpeg mixing commands, LUFS normalization for Snelverhuizen video ads. No music or instruments ever.
autoInvoke: true
triggers:
  - audio
  - audio mixing
  - voiceover
  - nasheed
  - SFX
  - sound effects
  - ambient audio
  - LUFS
  - ElevenLabs
negatives:
  - Do NOT invoke for purely visual tasks (image/video generation, hero frames)
  - Do NOT invoke for caption/text overlay work (use captions-and-titles.md)
---

# Halal Audio Pipeline

No music. No instruments. Ever. Audio is restricted to:
1. Voiceover (ElevenLabs, voice: Willem, model: `eleven_v3` for production / `eleven_flash_v2_5` for drafts)
2. Natural ambient SFX (Pixabay CC0 primary; Freesound CC0 fallback)
3. Vocal nasheeds without instruments (owner approval required before use)

## Audio Layer Hierarchy

| Layer | Source | Volume | Notes |
|-------|--------|--------|-------|
| Voiceover | ElevenLabs (Willem) | 100% / 0 dB | Primary. Always present. |
| Ambient SFX | Pixabay CC0 / Freesound CC0 | 25–30% | Background texture. Never music. |
| Vocal Nasheed | NoCopyrightNasheeds / Internet Archive | 15–20% | Optional. Owner approval required per brief. |

---

## 0. ElevenLabs Dutch Voiceover Settings

### Model Selection

| Model | Model ID | Dutch? | Cost/1K chars | Use case |
|-------|----------|--------|---------------|----------|
| **Eleven v3** | `eleven_v3` | ✓ (70+ lang) | ~$0.12/1K chars | **Production** — most expressive, audio tag support. NOT real-time capable (larger codec). |
| Multilingual v2 | `eleven_multilingual_v2` | ✓ | ~$0.12/1K chars | Fallback if v3 unavailable (same cost tier) |
| Flash v2.5 | `eleven_flash_v2_5` | ✓ (32 lang) | ~$0.06/1K chars | **Draft/iteration** — 75ms latency, 50% cheaper |

**Upgrade path:** Use `eleven_flash_v2_5` for script testing/iteration, then `eleven_v3` for the final production take. Never use `eleven_monolingual_v1` for Dutch.

### Voice Parameters (all models)

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Stability | 60 | Consistent delivery; >65 → monotone on longer passages |
| Similarity Boost | 72 | >80 introduces artifacts in Dutch |
| Style Exaggeration | 15 | Slight energy; 0 = flat, >30 = over-dramatic |
| Speaker Boost | true | Improves clarity on mobile speakers |

**eleven_v3 + audio tags**: lower stability to **50–55** when the script uses `[tag]` markers. Stability ≥60 suppresses the headroom the model needs to act on tags — they will be ignored or weakened. For plain prose with no tags, keep at 60.

### eleven_v3 Audio Tags

Audio tags are inline `[tag]` markers in the text that direct delivery. They are voice- and context-dependent — test on the actual voice first.

eleven_v3 has a community-documented library of ~1806 tags across 15 categories (emotions, delivery styles, accents, pacing, reactions, etc.). The tags below are the verified useful subset for Snelverhuizen brand ads. Anything in brackets is interpreted as a tag, not spoken — so typos or unknown tags silently fail.

**Appropriate for Snelverhuizen ads:**
- `[sincere]` — honest, direct delivery; use for brand promise lines
- `[warm]` — approachable, friendly; use for customer-benefit lines
- `[confident]` — authoritative, trust-building; use for CTA
- `[calm]` — composed, professional; use for contact info
- `[conversational]` — natural, unhurried pace; use for longer copy
- `[newsreader]` — clean broadcast delivery; use for factual claims
- `[professional]` — neutral authority; safe default for any line
- `[direct]` — punchy, no-nonsense; use for price/offer lines

**Avoid for Snelverhuizen brand:**
- `[excited]`, `[shouts]` — sensationalist, not aligned with sincere brand voice
- `[mischievously]`, `[laughs]`, `[crying]` — unprofessional
- `[whispers]` — inaudible on phone speakers
- `[sings]`, `[strong X accent]` — experimental; output is unreliable

**Tag persistence (v3 behaviour):** a tag affects ALL text from that point forward until a new tag appears. Explicitly reset after expressive sections — append `[professional]` before the CTA so it doesn't carry unwanted emotion.

**Usage in text (eleven_v3 only):**
```
[sincere] Verhuizen zonder zorgen? [warm] Snel Verhuizen regelt alles. [professional] Bel nu: 085 333 11 33.
```

**Note:** Audio tags and `<prosody rate="95%">` SSML can be used together in eleven_v3.

### SSML for natural Dutch pacing (all models)
```xml
<speak>
  <prosody rate="95%">
    Verhuizen zonder zorgen? <break time="400ms"/>
    <emphasis level="moderate">Snel Verhuizen</emphasis> regelt alles.
    <break time="300ms"/>
    Bel nu: 085 333 11 33.
  </prosody>
</speak>
```

ElevenLabs exports at ~-24 LUFS — always normalize before mixing (see 4a).

---

## 1. Nasheed Sources (Vocals-Only)

Use ONLY with owner Telegram approval before adding to any video.

| Source | License | Commercial? | Attribution? | Download |
|--------|---------|-------------|--------------|----------|
| **NoCopyrightNasheeds (NCN)** — nocopyrightnasheeds.com | NCN Custom | YouTube: free with credit. Outside YouTube: paid license required. | Yes (description) | YouTube DL via yt-dlp |
| **Internet Archive — Mix Vocal Only Nasheeds** — archive.org/details/mixvocalonlynasheeds | Varies per track | Check per track | Check per track | Direct download |
| **Internet Archive — Background Nasheed Collection** — archive.org/details/background-nasheed-collection | Varies per track | Check per track | Check per track | Direct download |
| **Halal Tones** — halaltones.com | Pro Plan | Yes, up to 100k views/platform | No | WAV download |
| **Halal Beats** — halalbeats.com | Custom | Check plan | Check plan | WAV download |

**Practical rule:** For YouTube-distributed ads, use NCN with credit in description. For paid/boosted ads (Instagram, TikTok, paid reach), confirm licensing before use or use CC0 from Internet Archive only.

**Halal Sounds (SoundCloud):** Channel `soundcloud.com/hasib-mahfin-777406511` — explicit "No Copyright Vocals Only Background Nasheed" tracks (Destiny, Grateful, Lost In Dreams, Beauty Of Creation). SoundCloud's ToS permits streaming only; verify license in track description before downloading for commercial use.

**Finding vocals-only tracks on NCN:** Search for "acapella", "vocals only", or "no instrument" in the track title on the NCN channel page.

**yt-dlp to extract audio from NCN YouTube video (free, no API cost):**
```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 \
  -o "/opt/pipeline/sfx/nasheeds/%(title)s.%(ext)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

---

## 2. SFX Libraries

### Tier 1: Pixabay SFX (Primary — No Attribution Required)

- **URL:** `pixabay.com/sound-effects/`
- **License:** Pixabay License — free for commercial use, no attribution required
- Preferred over Freesound: no API key needed, direct browser/curl download

**Search terms by scene:**

| Scene | Pixabay search term | Duration target |
|-------|---------------------|-----------------|
| Truck arriving | `truck engine idle` | 10–30s loop |
| Boxes being moved | `cardboard boxes moving` | 3–8s |
| Door open/close | `door open creak` | 2–4s |
| Footsteps on floor | `footsteps indoor` | 5–15s |
| Quiet street ambient | `street ambience birds morning` | 30–60s loop |
| Tape being applied | `tape roll dispenser` | 2–4s |
| Furniture settling | `furniture drag wood floor` | 3–6s |
| Family arrival warmth | `birds chirping morning quiet` | 30–60s loop |

### Tier 2: Freesound (API, CC0 Filter Only)

Use when Pixabay returns nothing suitable. Requires free API key from `freesound.org/apiv2/apply`.

### License Priority: CC0 > CC-BY > CC-BY-NC (never use NC for commercial ads)

**API search pattern (filter CC0 only):**
```python
import freesound
client = freesound.FreesoundClient()
client.set_token(FREESOUND_API_KEY)
results = client.text_search(
    query="quiet residential street birds",
    filter='license:"Creative Commons 0" duration:[10.0 TO 60.0]',
    fields="id,name,duration,license,previews"
)
```

### Curated Freesound Sounds (verified useful, check license at download)

| Use case | Creator / ID | Search terms |
|----------|-------------|--------------|
| Quiet residential street + birds | Robinhood76 — pack 3668 | `birds ambient` |
| Street ambience | DarkProductions_2016 — #334054 | `quiet street` |
| Furniture moving/bumping | William020304 — #593619 | `furniture moving` |
| Traffic ambience (distant) | Robinhood76 — pack 4036 | `traffic ambience` |
| Footsteps on concrete | InspectorJ — #336598 | `footsteps concrete` (CC-BY) |
| Outdoor nature birds | Luftrum — pack 3069 | `ambient nature garden birds` |

**Default ambient for any brief without specified audio:**
Search: `quiet residential street birds` — duration 20-60s — CC0 preferred
Volume in mix: 25-30% of voiceover

### Tier 3: Zapsplat (Free with Attribution)

- **URL:** `zapsplat.com/sound-effect-category/trucks/`
- **License:** Free tier requires Zapsplat credit in video description. Paid tier removes requirement.
- **Good for:** Professional diesel truck sounds, loading dock, hydraulic lift — more variety than Pixabay for vehicle audio.

### Standard SFX Kit for Snelverhuizen Videos

Quick reference for recurring scenes:

| Scene | SFX | Source | Search Term |
|-------|-----|--------|-------------|
| Truck exterior | Diesel engine idle | Pixabay | "truck engine idle" |
| Loading / boxes | Cardboard handling, tape pull | Pixabay | "cardboard box", "packing tape" |
| Door transition | Front door open/close | Pixabay | "door open close" |
| Neighborhood establishing | Birdsong, distant street | Pixabay | "birds ambient residential" |
| Arrival / unloading | Footsteps on wood | Freesound CC0 | "footsteps wood floor" |
| Handshake / close shot | Subtle wind or silence | — | (silence is fine) |

---

## 3. Mixing Levels

| Layer | dB Peak | LUFS Integrated | Notes |
|-------|---------|-----------------|-------|
| Voiceover (ElevenLabs) | -6 to -10 dBFS | -14 LUFS | Normalize first. Always loudest. |
| Ambient SFX bed | -25 to -30 dBFS | -35 LUFS | 25-30% of VO level |
| Nasheed (if approved) | -20 to -22 dBFS | -28 LUFS | Never louder than ambient bed |
| Mixed master output | -3 dBFS peak | -14 to -16 LUFS | Instagram/TikTok target |

**Platform loudness targets:**
- Instagram Reels / TikTok: -16 LUFS integrated, -1 dBTP true peak
- YouTube: -14 LUFS integrated
- ElevenLabs output default: ~-24 LUFS (always normalize before mixing)

---

## 4. FFmpeg Commands

### 4a. Normalize ElevenLabs voiceover to -14 LUFS
```bash
ffmpeg -i voiceover_raw.mp3 \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 \
  voiceover_normalized.mp3
```

### 4b. Simple mix: voiceover + ambient bed (no ducking)

Use `aloop=loop=-1` to loop ambient to match video length without gaps:
```bash
ffmpeg -i video_silent.mp4 -i voiceover_normalized.mp3 -i ambient.wav \
  -filter_complex \
    "[1:a]volume=1.0[vo]; \
     [2:a]volume=0.27,aloop=loop=-1:size=2e+09[amb]; \
     [vo][amb]amix=inputs=2:duration=first:normalize=0[audio_mixed]; \
     [audio_mixed]loudnorm=I=-14:TP=-1.5:LRA=11[out]" \
  -map 0:v -map "[out]" -c:v copy -c:a aac -b:a 192k \
  output_with_audio.mp4
```

### 4b2. Mix with nasheed (owner approval required)
```bash
ffmpeg -i video_silent.mp4 -i voiceover_normalized.mp3 -i ambient.wav -i nasheed.mp3 \
  -filter_complex \
    "[1:a]volume=1.0[vo]; \
     [2:a]volume=0.20,aloop=loop=-1:size=2e+09[amb]; \
     [3:a]volume=0.18,aloop=loop=-1:size=2e+09[nash]; \
     [vo][amb][nash]amix=inputs=3:duration=first:normalize=0[audio_mixed]; \
     [audio_mixed]loudnorm=I=-14:TP=-1.5:LRA=11[out]" \
  -map 0:v -map "[out]" -c:v copy -c:a aac -b:a 192k \
  output_with_nasheed.mp4
```

### 4b3. Add fade in/out to ambient or nasheed tracks

Replace `DURATION` with total video length in seconds:
```bash
# In filter_complex, replace the ambient line with:
[2:a]afade=t=in:st=0:d=1.5,afade=t=out:st=DURATION-2:d=2.0,volume=0.27,aloop=loop=-1:size=2e+09[amb];
```

### 4c. Auto-ducking: ambient ducks when voiceover is active
```bash
ffmpeg -i voiceover_normalized.mp3 -i ambient.wav \
  -filter_complex \
    "[0:a]asplit=2[narr][sc]; \
     [1:a][sc]sidechaincompress=threshold=0.02:ratio=10:attack=50:release=500[ducked]; \
     [narr][ducked]amix=inputs=2:duration=first:normalize=0[out]" \
  -map "[out]" -c:a aac -b:a 192k \
  audio_ducked.aac
```
- `threshold=0.02` triggers when VO is present
- `attack=50ms` — quick duck on speech start
- `release=500ms` — smooth fade-back after speech

### 4d. Attach audio to video (preserving video stream)
```bash
ffmpeg -i video_silent.mp4 -i audio_mixed.aac \
  -c:v copy -c:a aac -b:a 192k \
  -shortest \
  final_output.mp4
```

### 4e. Phone speaker voice optimization chain (for Reels / TikTok mobile delivery)

Phone speakers roll off below ~150 Hz and above ~8 kHz. ElevenLabs VO is produced stereo at -24 LUFS. This chain prepares it for maximum intelligibility on a phone speaker before mixing:

```bash
# Apply AFTER loudnorm (4a) and BEFORE the mix commands (4b / 4b2)
ffmpeg -i voiceover_normalized.mp3 \
  -af "highpass=f=80, \
       equalizer=f=2500:t=q:w=1.2:g=3, \
       equalizer=f=4000:t=q:w=1.5:g=2, \
       acompressor=threshold=-20dB:ratio=3:attack=5:release=100:makeup=2dB, \
       aformat=channel_layouts=mono, \
       aresample=48000" \
  voiceover_phone.mp3
```

What each stage does:
- `highpass=f=80` — removes sub-bass rumble phone can't reproduce
- `equalizer f=2500 +3dB` — presence peak; Dutch consonants land here
- `equalizer f=4000 +2dB` — articulation boost; improves "s", "t", "k" clarity
- `acompressor ratio=3` — tightens dynamic range so quiet syllables aren't lost
- `aformat=mono` — phone is mono; avoids stereo cancellation artifacts
- `aresample=48000` — ensures consistent sample rate into the mix

**When to use:** Any deliverable going to Instagram Reels, TikTok, or WhatsApp. Skip for YouTube (stereo plays through TV/laptop).

### 4e. Pre-process ambient SFX for seamless looping (eliminates audible click)

`aloop` wraps the file abruptly — if start and end don't match in level/tone, you hear a click. Pre-process the raw SFX file ONCE to create a crossfaded loop version:

```bash
# Feed the file to itself twice; acrossfade blends the end of pass 0 into the start of pass 1
# d=1.5 = 1.5-second crossfade zone; output is ~1.5s shorter than original
# c1/c2=exp = exponential curve (sounds more natural than linear)
ffmpeg -i ambient_raw.wav -i ambient_raw.wav \
  -filter_complex "[0][1]acrossfade=d=1.5:c1=exp:c2=exp" \
  ambient_seamless.wav
```

Then use `ambient_seamless.wav` in all mix commands (4b / 4b2 / 4b3) with `aloop=loop=-1:size=2e+09` — it loops without audible clicks.

**Curve options:** `exp` (default, natural), `tri` (linear), `nofade` (hard cut — use to test if click is really there).

### 4g. Phone-speaker pre-processing (run ONCE on raw ambient/nasheed files)

Phone speakers (including most mobile social-media playback) roll off below ~150 Hz and can distort on sub-bass content. Pre-processing prevents muddy/buzzy playback and saves headroom in the mix.

**Step 1 — Highpass ambient bed at 100 Hz (removes rumble, frees headroom):**
```bash
ffmpeg -i ambient_seamless.wav \
  -af "highpass=f=100:width_type=q:width=0.707" \
  ambient_seamless_hp.wav
```

**Step 2 — Optional: presence boost on voiceover for small-speaker clarity (+2 dB at 2.5 kHz):**
```bash
ffmpeg -i voiceover_normalized.mp3 \
  -af "equalizer=f=2500:width_type=q:width=1.5:g=2.0" \
  voiceover_mobile.mp3
```

**Step 3 — Verify mono compatibility (phase cancellation check):**
```bash
ffmpeg -i output_with_audio.mp4 \
  -af "aformat=channel_layouts=mono,astats" \
  -f null - 2>&1 | grep "RMS level"
```
If mono RMS is >3 dB lower than stereo RMS, there is phase cancellation — check ambient SFX source for stereo-widening processing and downmix to mono before using.

---

### 4f. Normalize final mix master to -14 LUFS (social media master)

**Single-pass (fast):**
```bash
ffmpeg -i final_output.mp4 \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 \
  -c:v copy \
  final_output_normalized.mp4
```

**Two-pass (accurate — required before delivery):**
```bash
# Pass 1: measure
ffmpeg -i final_output.mp4 \
  -af loudnorm=I=-14:LRA=11:TP=-1.5:print_format=json \
  -f null - 2>&1 | tail -20
# Copy JSON values (input_i, input_lra, input_tp, input_thresh, target_offset), then Pass 2:
ffmpeg -i final_output.mp4 \
  -af "loudnorm=I=-14:LRA=11:TP=-1.5:measured_I=<input_i>:measured_LRA=<input_lra>:measured_TP=<input_tp>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true" \
  -c:v copy -c:a aac -b:a 192k \
  final_output_normalized.mp4
```

**Or use ffmpeg-normalize (pip install ffmpeg-normalize):**
```bash
ffmpeg-normalize final_output.mp4 -t -14 --true-peak -1.5 -c:a aac -b:a 192k -o final_output_normalized.mp4
```

---

## 5. Audio QA Checklist

Before delivery, confirm all items:

- [ ] No musical instruments (clap, synth, drum, etc.) anywhere in the audio
- [ ] Voiceover is loudest element — peaks at -6 to -10 dBFS
- [ ] Ambient SFX at 25-30% of VO level
- [ ] Nasheed (if used): owner approval confirmed via Telegram
- [ ] Master normalized to -14 to -16 LUFS integrated
- [ ] True peak does not exceed -1 dBTP
- [ ] No clipping anywhere (check with `ffmpeg -i output.mp4 -af astats -f null -`)
- [ ] Freesound sounds are CC0 or CC-BY (not CC-BY-NC for commercial ads)
- [ ] Attribution logged for any CC-BY sounds used
- [ ] Audio plays correctly on phone speaker (test mono compatibility)

### Check for clipping / audio stats:
```bash
ffmpeg -i output.mp4 -af "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.Peak_level" -f null -
```

---

## 6. Shariah Compliance Cross-Check

The audio QA must also pass shariah-compliance.md hard gate:
- `shariah_compliance = 10/10` required on audio track
- Any nasheed with any instrument (even subtle beat or clap rhythm): REJECT
- Any ambient SFX with background music (check carefully): REJECT, find alternative
- Voiceover tone: professional, sincere — never sensationalist or manipulative

---

## 7. Platform Loudness Standards

| Platform | Target LUFS | True Peak | Notes |
|----------|-------------|-----------|-------|
| Instagram Reels | -14 LUFS | -1.5 dBTP | Platform normalizes louder content down |
| TikTok | -14 LUFS | -1.5 dBTP | Same normalization behavior |
| YouTube Shorts | -14 LUFS | -1.0 dBTP | YouTube target |
| WhatsApp / Telegram | -16 LUFS | -1.0 dBTP | Voice-first, slightly lower |

**Rule:** Always export at -14 LUFS. Platforms normalize louder content DOWN (losing dynamics). Do not push louder to "cut through" — it triggers more limiting and sounds worse.

---

## 9. Nasheed Instrument Screening

Use before submitting any nasheed to owner for approval. Catches nasheeds that have instruments disguised under the mix.

### 9a. Sub-bass energy check (FFmpeg — fast, no install)

Vocal-only nasheeds have negligible energy below 80 Hz. Any track with significant sub-bass content almost certainly contains a bass guitar, kick drum, or synthesizer.

```bash
# Measure RMS level of sub-80Hz content only
ffmpeg -i nasheed.mp3 \
  -af "lowpass=f=80,astats=metadata=1,ametadata=print:key=lavfi.astats.Overall.RMS_level" \
  -f null - 2>&1 | grep RMS
```

**Interpretation:**
- RMS < -45 dBFS → likely vocals-only (no bass instrument)
- RMS −30 to −45 dBFS → borderline; check carefully at 1.5x speed
- RMS > −30 dBFS → bass instrument present → **REJECT**

### 9b. Onset density check (Python + librosa — detects percussion/claps)

Consistent rhythmic onsets indicate a beat track or percussion (even hand claps at regular BPM suggest instrumented production).

```python
import librosa
import numpy as np

y, sr = librosa.load("nasheed.mp3", mono=True)
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

print(f"Detected tempo: {tempo:.1f} BPM")
print(f"Beat confidence: {np.mean(onset_env[beats]):.3f}")

# If tempo > 60 BPM AND beat confidence > 0.5 → likely has rhythmic percussion
```

**Interpretation:**
- Detected tempo 0-40 BPM and beat confidence < 0.3 → probably vocals-only speech rhythm
- Detected tempo 60-130 BPM and beat confidence ≥ 0.5 → likely has a beat track → listen carefully or **REJECT**

### 9c. Essentia voice_instrumental classifier (optional, more accurate)

Pre-trained model available at `https://essentia.upf.edu/models/classification-heads/voice_instrumental/`. Install: `pip install essentia-tensorflow`. Best architecture for general audio: `voice_instrumental-discogs-effnet-1`.

**Note:** this model classifies "voice" (vocals present) vs "instrumental" (no vocals). It will not flag a nasheed with instruments PLUS vocals as "instrumental". Use §9a and §9b for instrument presence checks; use this model if you need to confirm that vocals ARE present in a suspected all-instrumental track.

---

## 8. Known Issues and Solutions

| Problem | Cause | Fix |
|---------|-------|-----|
| Ambient loops with audible click | No crossfade at loop point | Pre-process with `acrossfade` (see §4f) then re-use with `aloop` |
| VO sounds robotic | Stability too high (>70) | Set stability to 55–60 |
| Dutch phonemes sound off | Wrong model | Must use `eleven_multilingual_v2` |
| Nasheed copyright claim on YouTube | Not checking each video's description | Always verify specific NCN video description before use |
| Audio out of sync with video | Different sample rates | Resample all inputs to 48000 Hz before mixing |
| Mobile speakers sound muddy | Stereo ambient on mono speaker | Downmix ambient: `aformat=channel_layouts=mono` |
| SFX cuts off before video ends | `duration=first` uses shortest input | Use `aloop=loop=-1:size=2e+09` on all SFX inputs |
| Audio tags ignored / flat delivery with tags | Stability ≥60 suppresses tag headroom | Lower stability to 50–55 when script uses `[tag]` markers (see §0) |
| Tag emotion bleeds into CTA line | Tags persist until next tag | Explicitly add `[professional]` before CTA line to reset (see §0) |
| Mobile ambient sounds buzzy/distorted | Sub-bass in ambient SFX hitting phone speaker | Highpass ambient at 100 Hz (see §4g) |
| Dutch phonemes sound off | Wrong model | Use `eleven_v3` (production) or `eleven_multilingual_v2` (fallback). Never monolingual v1. |

---

## 9. Nasheed Instrument Detection Script

Before using any nasheed download, run this script to flag hidden instruments (subtle percussion, synth pads, clap tracks). Pure vocal nasheeds produce high spectral flatness + weak beat confidence; instruments produce low flatness + strong beat periodicity.

```python
#!/usr/bin/env python3
"""
nasheed_check.py — detects likely instruments in a nasheed file.
Install once: pip install librosa numpy
Usage: python nasheed_check.py path/to/nasheed.mp3
Exit 0 = likely vocal-only (PASS). Exit 1 = instruments detected (FAIL — review manually).
"""
import sys
import numpy as np
import librosa

def check_nasheed(path: str) -> dict:
    y, sr = librosa.load(path, mono=True, duration=60)  # analyse first 60s

    # 1. Spectral flatness: pure tones → near 0; pure noise/vocals → near 1
    flatness = librosa.feature.spectral_flatness(y=y)
    flatness_mean = float(np.mean(flatness))

    # 2. Beat tracking: strong periodic rhythm → instruments likely
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    beat_strength = float(np.mean(onset_env[beat_frames])) if len(beat_frames) > 0 else 0.0

    # 3. Spectral contrast: music has high contrast between peaks/valleys
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    contrast_mean = float(np.mean(contrast))

    # Heuristic thresholds (empirical — adjust after testing on known-good nasheeds)
    has_instruments = (
        flatness_mean < 0.08          # very tonal = likely instruments
        and beat_strength > 2.5       # strong periodic beats
        and contrast_mean > 18        # high spectral contrast = music
    )

    return {
        "spectral_flatness": round(flatness_mean, 4),
        "beat_strength": round(beat_strength, 2),
        "spectral_contrast": round(contrast_mean, 2),
        "tempo_bpm": round(float(tempo), 1),
        "verdict": "FAIL — instruments likely" if has_instruments else "PASS — likely vocal-only",
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python nasheed_check.py <audio_file>")
        sys.exit(2)
    result = check_nasheed(sys.argv[1])
    for k, v in result.items():
        print(f"  {k}: {v}")
    sys.exit(1 if "FAIL" in result["verdict"] else 0)
```

**Thresholds explained:**
- `flatness < 0.08` — pure tonal energy (instruments have sustained pitches); pure voice/ambient scores ~0.15–0.30
- `beat_strength > 2.5` — strong onset periodicity; free-verse vocals typically score < 1.5
- `contrast > 18` — high peak-valley difference typical of music mixing

**Practical workflow:**
1. Download nasheed: `yt-dlp -x --audio-format mp3 -o nasheed.mp3 "URL"`
2. Run check: `python nasheed_check.py nasheed.mp3`
3. FAIL → do NOT use without owner manual review; PASS → proceed, still listen once yourself
4. PASS does not guarantee halal compliance — always listen to confirm NO instruments, NO beat patterns

**Limitations:** A cappella groups with hand-clap percussion (allowed by some scholars, not by Snelverhuizen policy) may score PASS. Always confirm by ear.

---

## 10. SFX Noise Reduction (arnndn)

ElevenLabs voiceover is already clean — skip for VO. Use this to remove background hiss, HVAC hum, or room noise from Pixabay/Freesound SFX files before mixing.

**One-time setup — download model files:**
```bash
git clone https://github.com/richardpl/arnndn-models /opt/pipeline/models/arnndn-models
# Primary model: std.rnnn — general speech/ambient
```

**Denoise a SFX file:**
```bash
ffmpeg -i sfx_noisy.wav \
  -af "arnndn=m=/opt/pipeline/models/arnndn-models/std.rnnn:mix=0.8" \
  sfx_clean.wav
```

**mix parameter:** `0.8` = good balance (removes hiss, keeps room character). `1.0` = maximum (may flatten ambience texture). `0.5` = light touch for subtle noise.

**Workflow:** Pre-process once, save as `_clean.wav` in the SFX library for reuse.

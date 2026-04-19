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
1. Voiceover (ElevenLabs, voice: Willem, model: `eleven_multilingual_v2`)
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

**Model:** `eleven_multilingual_v2` — mandatory for Dutch. Never use `eleven_monolingual_v1` for Dutch.

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Stability | 60 | Consistent delivery; >65 → monotone on longer passages |
| Similarity Boost | 72 | >80 introduces artifacts in Dutch |
| Style Exaggeration | 15 | Slight energy; 0 = flat, >30 = over-dramatic |
| Speaker Boost | true | Improves clarity on mobile speakers |

**SSML for natural Dutch pacing:**
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

**yt-dlp to extract audio from NCN YouTube video (free, no API cost):**
```bash
yt-dlp -x --audio-format mp3 -o "nasheed_%(title)s.%(ext)s" "https://www.youtube.com/watch?v=VIDEO_ID"
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

### 4e. Normalize final mix master to -16 LUFS (social media master)
```bash
ffmpeg -i final_output.mp4 \
  -af loudnorm=I=-16:TP=-1.0:LRA=11 \
  -c:v copy \
  final_output_normalized.mp4
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

## 8. Known Issues and Solutions

| Problem | Cause | Fix |
|---------|-------|-----|
| Ambient loops with audible click | No crossfade at loop point | Find seamless loop file or use `acrossfade` |
| VO sounds robotic | Stability too high (>70) | Set stability to 55–60 |
| Dutch phonemes sound off | Wrong model | Must use `eleven_multilingual_v2` |
| Nasheed copyright claim on YouTube | Not checking each video's description | Always verify specific NCN video description before use |
| Audio out of sync with video | Different sample rates | Resample all inputs to 48000 Hz before mixing |
| Mobile speakers sound muddy | Stereo ambient on mono speaker | Downmix ambient: `aformat=channel_layouts=mono` |
| SFX cuts off before video ends | `duration=first` uses shortest input | Use `aloop=loop=-1:size=2e+09` on all SFX inputs |

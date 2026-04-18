---
name: Halal Audio
description: End-to-end halal audio pipeline — nasheed sourcing, ambient SFX retrieval, mixing levels, FFmpeg commands, and LUFS normalization for Snelverhuizen video ads. No music or instruments ever.
autoInvoke: false
triggers:
  - audio mixing
  - voiceover
  - nasheed
  - SFX
  - sound effects
  - ambient audio
  - ElevenLabs
---

# Halal Audio Pipeline

No music. No instruments. Ever. Audio is restricted to:
1. Voiceover (ElevenLabs, voice: Willem)
2. Natural ambient SFX (Freesound, CC0 or CC-BY only)
3. Vocal nasheeds without instruments (owner approval required before use)

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

## 2. Freesound SFX — Curated Sounds for Moving Company Ads

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
```bash
ffmpeg -i voiceover_normalized.mp3 -i ambient.wav \
  -filter_complex \
    "[0:a]volume=1.0[vo]; \
     [1:a]volume=0.27[amb]; \
     [vo][amb]amix=inputs=2:duration=first:normalize=0[out]" \
  -map "[out]" -c:a aac -b:a 192k \
  audio_mixed.aac
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

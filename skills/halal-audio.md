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
| **Eleven v3** | `eleven_v3` | ✓ (74 lang) | ~$0.12/1K chars | **Production** — most expressive, audio tag support. GA since March 14, 2026. NOT real-time capable (use `eleven_v3_conversational` for agents only). |
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
| **language_code** | **"nl"** | Always set explicitly for Dutch scripts. Ensures Dutch text normalisation rules apply (numbers, dates, phone numbers). Without this, "085 3331133" may be pronounced with English digit names. |
| **apply_text_normalization** | **"on"** | Force Dutch text normalisation ON (not "auto"). Spells out numbers and phone numbers in Dutch. Critical for scripts containing "085 3331133". |

**Willem voice_id**: The `voice_id` string for Willem is not published in any SDK reference or public list — it is a Voice Library community voice. Retrieve it once and store in project config. As of the April 7, 2026 API update, the voice response also includes `recording_quality` and `labelling_status` — check these when first retrieving:
```python
import requests
r = requests.get("https://api.elevenlabs.io/v1/voices",
                 headers={"xi-api-key": ELEVENLABS_API_KEY},
                 params={"search": "Willem"})
voice = r.json()["voices"][0]
VOICE_ID = voice["voice_id"]
# April 7, 2026: recording_quality enum: "studio" | "good" | "ok" | "poor" | "bad"
# labelling_status enum: "in_review" | "review_complete"
print(f"Willem quality: {voice.get('recording_quality', 'unknown')}")
print(f"Review status: {voice.get('labelling_status', 'unknown')}")
```
Only proceed to production if `recording_quality` is `"studio"` or `"good"`. If `"ok"` or worse, or `labelling_status` is `"in_review"`, consider switching to a different Dutch voice. Alternatively: elevenlabs.io → Voices → search "Willem" → three-dot menu → Copy voice ID. **Voice Library community voices are NOT subject to the Dec 31, 2026 ElevenLabs default-voice expiry** (that applies only to the original 38 pre-made English defaults). Willem will persist unless its creator removes it — save the ID to project config as a precaution.

**PVC note (April 2026):** Professional Voice Clones (PVCs) are not yet fully optimized for eleven_v3 — they may show reduced responsiveness to audio tags compared to Instant Voice Clones (IVCs) and Voice Library voices. Willem (a Voice Library voice) is not affected. Do NOT create a PVC for production unless testing confirms tags work as expected.

**eleven_v3 + audio tags**: lower stability to **50–55** when the script uses `[tag]` markers. Stability ≥60 suppresses the headroom the model needs to act on tags — they will be ignored or weakened. For plain prose with no tags, keep at 60.

### eleven_v3 Audio Tags

Audio tags are inline `[tag]` markers in the text that direct delivery. They are voice- and context-dependent — test on the actual voice first.

eleven_v3 has a community-documented library of ~1806 tags across 15 categories (emotions, delivery styles, accents, pacing, reactions, etc.). The tags below are the verified useful subset for Snelverhuizen brand ads. Anything in brackets is interpreted as a tag, not spoken — so typos or unknown tags silently fail.

**ElevenLabs does NOT publish an exhaustive official tag list.** Tags are voice- and context-dependent. The list below distinguishes confirmed (verified in official ElevenLabs blog posts/docs) from unconfirmed (appear in third-party summaries, may work but test first).

**Confirmed in official ElevenLabs sources:**
- `[calm]` — composed, professional; use for contact info
- `[pause]` — brief natural pause; eleven_v3-native pacing tool (replaces SSML `<break>` which v3 ignores). **Note:** official ElevenLabs blogs use `[pause]` (no 's'). Previous docs had `[pauses]` — both may work, but `[pause]` is the documented canonical form. Test on Willem if migrating scripts.
- `[matter-of-fact]` — neutral, direct delivery; good safe fallback for any ad line
- `[drawn out]` — slows and stretches the next phrase for emphasis; use on key brand claims
- `[hesitates]` — momentary stammer before the next phrase; use sparingly for natural delivery feel (confirmed in ElevenLabs "story beats" category)
- `[deliberate]` — precise, measured pacing with careful articulation; **best professional substitute for unconfirmed `[confident]` / `[direct]`**; use for brand claims and CTA lines
- `[understated]` — calm, controlled understatement; anti-sensationalist; ideal for Snelverhuizen brand (sincere, not hype)
- `[serious tone]` — professional authority for factual/pricing lines; use where `[matter-of-fact]` is too flat
- `[slows down]` — reduces pace on following phrase; use to land the brand name or phone number with weight
- `[emphasized]` — adds vocal emphasis to the following phrase; use for key brand promise lines ("verhuizen zonder zorgen"). Confirmed in ElevenLabs precision delivery control docs.
- `[stress on next word]` — focuses emphasis on the immediately following word only; more targeted than `[emphasized]`. Confirmed in ElevenLabs precision delivery control docs. Example: `[stress on next word] SNELVERHUIZEN.NL`

**Unconfirmed (test on Willem voice before production — may be silently ignored):**
- `[sincere]` — honest, direct delivery; use for brand promise lines
- `[warm]` — approachable, friendly; use for customer-benefit lines
- `[confident]` — authoritative, trust-building; use for CTA (use confirmed `[deliberate]` as a reliable alternative)
- `[conversational]` — natural, unhurried pace; use for longer copy
- `[newsreader]` — clean broadcast delivery; use for factual claims
- `[professional]` — neutral authority; safe default for any line
- `[direct]` — punchy, no-nonsense; use for price/offer lines (use confirmed `[deliberate]` as a reliable alternative)

**Test protocol for unconfirmed tags:** generate one sentence with and without the tag using Willem + `eleven_v3`; if delivery is identical, the tag is not working on this voice — switch to `[matter-of-fact]` or `[calm]` instead.

**Avoid for Snelverhuizen brand:**
- `[excited]`, `[shouts]` — sensationalist, not aligned with sincere brand voice
- `[mischievously]`, `[laughs]`, `[crying]` — unprofessional
- `[whispers]` — inaudible on phone speakers
- `[sings]`, `[strong X accent]` — experimental; output is unreliable
- `[breathes]` — **confirmed working** but adds audible breath sounds; violates same policy as "breathing" ban in video motion prompts; never use in Snelverhuizen ads
- `[sarcastic tone]`, `[resigned]`, `[wistful]` — confirmed working but tone is wrong for brand (sarcasm, defeat, nostalgia — none appropriate for a professional moving company ad)
- `[rushed]`, `[rapid-fire]` — confirmed official speed tags; too fast for a professional brand; never use for Snelverhuizen ad copy

**Tag persistence (v3 behaviour):** a tag affects ALL text from that point forward until a new tag appears. Explicitly reset after expressive sections — append `[professional]` before the CTA so it doesn't carry unwanted emotion.

**Minimum prompt length for reliable tag response:** audio tags work best in prompts over ~250 characters. In shorter prompts the model may ignore or weakly apply tags — use the full script (including VO context) rather than testing on a single isolated line.

**Usage in text (eleven_v3 only):**
```
[sincere] Verhuizen zonder zorgen? [warm] Snel Verhuizen regelt alles. [professional] Bel nu: 085 333 11 33.
```

**SSML in eleven_v3:** eleven_v3 does NOT support SSML `<break>` tags. Use audio tags for pacing control instead (`[calm]`, `[conversational]`, `[professional]`). Limited `<prosody rate="...%">` wrapping may still apply, but test each script — break tags will be silently ignored or spoken as text. The SSML section below (§SSML) applies to `eleven_multilingual_v2` and Flash only, NOT v3.

### eleven_v3 Character Limit and Multi-Chunk Continuity

**Character limit:** eleven_v3 caps at **5,000 characters per request** (versus 40,000 for Flash/Turbo). Scripts longer than ~750 Dutch words must be split.

**`previous_request_ids` — preserves prosody continuity across chunks:**
When splitting a long script, pass the prior call's request ID in the next call so the model maintains natural flow across the join point. Max 3 IDs. Pass them in chronological order.

```python
# Chunk 1 — no previous context
r1 = client.text_to_speech.convert(
    voice_id=VOICE_ID,
    text=chunk_1_text,
    model_id="eleven_v3",
    language_code="nl",
    apply_text_normalization="on",
)
request_id_1 = r1.request_id  # save for next call

# Chunk 2 — references chunk 1 for prosody continuity
r2 = client.text_to_speech.convert(
    voice_id=VOICE_ID,
    text=chunk_2_text,
    model_id="eleven_v3",
    language_code="nl",
    apply_text_normalization="on",
    previous_request_ids=[request_id_1],
)
```

**Split rule:** Break at sentence boundaries (full stop + capital). Never split mid-sentence. Crossfade the joined audio clips by 5–10 ms in FFmpeg to eliminate any click at the join point.

### SSML for natural Dutch pacing (eleven_multilingual_v2 and Flash v2.5 ONLY — NOT v3)

**eleven_v3 does not support `<break>` tags.** For v3, use audio tags (`[calm]`, `[conversational]`) for pacing and pauses.

For multilingual_v2 / Flash v2.5:
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
| **NoCopyrightNasheeds (NCN)** — nocopyrightnasheeds.com | NCN Custom | YouTube: free with credit. Outside YouTube: paid license required. Tiers: Forever $99.99 (one-time) · Monthly $19.99/mo · Mujahideen $11.99/mo — all tiers: outside-YouTube commercial use, no attribution. | Yes on free tier (YouTube only) | YouTube DL via yt-dlp |
| **Internet Archive — Mix Vocal Only Nasheeds** — archive.org/details/mixvocalonlynasheeds | Varies per track | Check per track | Check per track | Direct download |
| **Internet Archive — Background Nasheed Collection** — archive.org/details/background-nasheed-collection | Varies per track | Check per track | Check per track | Direct download |
| **Halal Tones** — halaltones.com | Pro Plan | Yes, up to 100k views/platform | No | WAV download |
| **Halal Beats** — halalbeats.com | Custom | Check plan | Check plan | WAV download — **REJECT for Snelverhuizen**: platform explicitly uses daf (frame drum) on tracks. Daf is percussion; Snelverhuizen policy prohibits all instruments. Do not use. |
| **Halal Soundtracks** — halalsoundtracks.com | Royalty-free library | Yes, commercial | Check terms | WAV download — **MUST select "Vocals Only" version** (each track is released in two variants: "Vocals Only" and "Vocals + Daf" — always confirm you have the vocals-only file) |
| **Internet Archive — The Ultimate Nasheed Collection** — archive.org/details/nasheedplaylist | Varies per track | Check per track (CC0 tracks safe; verify others) | Check per track | Direct download — uploaded by TheNasheedMaster; "NO MUSIC" in title; Arabic, Urdu, Bangla nasheeds. Run nasheed_check.py before use — not all tracks in the collection are confirmed instruments-free by ear. |
| **Nasheed Station** — nasheedstation.com | Unknown | **Unconfirmed** — verify before commercial use | Check per track | Stream/download |
| **Riad Nasheeds** — youtube.com/channel/UC9NUIlplMU9CztLIIy8nbEA | Custom | **Unconfirmed for commercial use** — email riadnasheeds@gmail.com before use | Check per track | yt-dlp (see below) |

**Practical rule:** For YouTube-distributed ads, use NCN with credit in description. For paid/boosted ads (Instagram, TikTok, paid reach), use Halal Soundtracks (royalty-free commercial license) or confirm licensing per track for all other sources. Internet Archive CC0 tracks are always safe for commercial use.

**Riad Nasheeds:** YouTube channel specialising in 100% vocal-only humming nasheeds — no instruments, no lyrics (pure melodic humming). Tracks are labelled "No Copyright Nasheed" on their YouTube titles. Before any commercial use (including boosted/paid social ads), email riadnasheeds@gmail.com to confirm commercial terms. For YouTube-only distribution, check individual video description for permission statement. Use yt-dlp to download (same command as NCN below).

**Islamic Audio Library:** `islamicaudiolibrary.com` / YouTube `youtube.com/c/IslamicAudioLibrary-Free` — channel explicitly labelled "Free To Use / No Copyright". Covers background nasheeds, vocal nasheeds, and halal SFX. Verify license per track in video description before commercial use; no blanket CC license stated. Use yt-dlp command below to extract.

**Halal Sounds (SoundCloud):** Channel `soundcloud.com/hasib-mahfin-777406511` — explicit "No Copyright Vocals Only Background Nasheed" tracks (Destiny, Grateful, Lost In Dreams, Beauty Of Creation). SoundCloud's ToS permits streaming only; verify license in track description before downloading for commercial use.

**Finding vocals-only tracks on NCN:** Search for "acapella", "vocals only", or "no instrument" in the track title on the NCN channel page.

**Pixabay Islamic Nasheed category:** Pixabay (Tier 1b SFX library, §2) also has a dedicated Islamic nasheed music category — royalty-free, no attribution, commercial OK. Search `pixabay.com/music/search/islamic%20nasheed/`. Useful when Pixabay is already open for SFX and a light background track is needed. Always screen with nasheed_check.py (§9) before use.

**yt-dlp to extract audio from NCN YouTube video (free, no API cost):**
```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 \
  -o "/opt/pipeline/sfx/nasheeds/%(title)s.%(ext)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"
```

---

## 2. SFX Libraries

### Tier 1a: Mixkit SFX (Primary — Fastest, No Sign-Up)

- **URL:** `mixkit.co/free-sound-effects/`
- **License:** Mixkit Sound Effects Free License — free for commercial use, no attribution required, no registration
- **Best for:** Quick one-off sounds; smaller library than Pixabay but zero friction (no account, direct download)
- Categories useful for Snelverhuizen: "city", "ambience", "home", "household"

### Tier 1b: Pixabay SFX (Primary — Larger Catalogue)

- **URL:** `pixabay.com/sound-effects/`
- **License:** Pixabay License — free for commercial use, no attribution required
- Preferred for broader search coverage; no API key needed, direct browser/curl download

**Search terms by scene:**

| Scene | Pixabay search term | Duration target |
|-------|---------------------|------------------|
| Truck arriving | `truck engine idle` | 10–30s loop |
| Boxes being moved | `cardboard boxes moving` | 3–8s |
| Door open/close | `door open creak` | 2–4s |
| Footsteps on floor | `footsteps indoor` | 5–15s |
| Quiet street ambient | `street ambience birds morning` | 30–60s loop |
| Tape being applied | `tape roll dispenser` | 2–4s |
| Furniture settling | `furniture drag wood floor` | 3–6s |
| Family arrival warmth | `birds chirping morning quiet` | 30–60s loop |

### Tier 1c: ElevenLabs SFX v2 (Generated — Use When Pixabay/Mixkit Come Up Empty)

Model `eleven_text_to_sound_v2` generates custom ambient sounds from a text prompt. Use when Pixabay/Mixkit don't return a suitable match for a specific scene — this lets you specify exactly what the scene needs.

**Halal advantage over library search:** you control the prompt, so you can explicitly exclude music descriptors → zero risk of hidden instruments in the ambient bed.

**Key parameters:**

| Parameter | Type | Range | Notes |
|-----------|------|-------|-------|
| `text` | str | — | Scene description; avoid music words |
| `duration_seconds` | float | 0.5–30 | Set explicitly for ambient loops; leave None for short one-shots |
| `loop` | bool | — | `True` = seamless loop output (no acrossfade post-processing needed) |
| `prompt_influence` | float | 0–1 | Default 0.3; raise to 0.6+ if output drifts from description |
| `model_id` | str | — | `"eleven_text_to_sound_v2"` |
| `output_format` | str | see below | Default is MP3 22kHz/32kbps. **Always override for pipeline use.** |

**`output_format` values for SFX v2** (format: `codec_samplerate_bitrate`):

| Format string | Quality | Plan required | Use case |
|---------------|---------|---------------|----------|
| `mp3_44100_128` | Good — CD-rate MP3 | Free+ | **Pipeline default** — best quality without plan restriction |
| `mp3_44100_192` | Better | Creator+ | Higher fidelity if on Creator plan |
| `wav_44100` | Lossless | Pro+ | Lossless SFX master for long-term library storage |
| `mp3_22050_32` | Low | Free | Not suitable for mixing — leave as fallback only |

**Always request `mp3_44100_128` or better for pipeline SFX.** The default 22kHz/32kbps output introduces noticeable artifacts at the top of the frequency range, which are amplified after the highpass filter (§4g) and loudnorm stages.

**Cost:** 200 credits (auto-duration) or 40 credits/second (custom). Uses the same ElevenLabs credit pool as TTS — not an additional subscription. Free plan: ~10,000 credits/month (~50 auto-gen or ~12 × 20s custom SFX free/month).

**Prompt patterns for Snelverhuizen scenes:**

| Scene | SFX v2 prompt |
|-------|---------------|
| Neighborhood establishing | `quiet Dutch residential street, birds chirping softly, distant light traffic, calm morning ambience, no music` |
| Truck exterior | `diesel truck engine idling at low rpm, steady rumble, outdoor ambience, no music` |
| Loading / boxes | `cardboard box being placed on wooden floor, single thud, no music` |
| Front door | `wooden front door opening slowly, quiet house interior, no music` |
| Tape being applied | `packing tape pulled from dispenser, sticky tear sound, no music` |

**Python SDK example:**
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

audio = b"".join(client.text_to_sound_effects.convert(
    text="quiet Dutch residential street, birds chirping, distant light traffic, no music",
    model_id="eleven_text_to_sound_v2",
    duration_seconds=20.0,   # 20-second ambient bed: 800 credits
    loop=True,               # native seamless loop — skip acrossfade post-processing
    prompt_influence=0.4,    # slightly higher adherence for descriptive prompts
    output_format="mp3_44100_128",  # always override default (22kHz/32kbps is too low for mixing)
))

with open("/opt/pipeline/sfx/street_ambient.mp3", "wb") as f:
    f.write(audio)
```

**When `loop=True` is used:** the output is already seamlessly looped — do NOT additionally run the `acrossfade` command from §4e. Use directly with `aloop=loop=-1:size=2e+09` in the mix commands.

### ⚠ ElevenLabs Music API — DO NOT USE for halal ambient SFX

ElevenLabs added a Music API with `generation_mode: "ambience"` (May 2026, SDK v2.49.0). Despite the name "ambience", this is a **music generation API** — it generates AI-composed music with instrumentation. Even in `ambience` mode, output is likely to contain musical elements (tonal pads, harmonics, rhythmic content).

**Rule: never use ElevenLabs Music API in this pipeline.** The SFX v2 API (`eleven_text_to_sound_v2`) is the correct tool for instrument-free ambient beds. The Music API exists for background music use cases — incompatible with Snelverhuizen halal audio policy. If an ambient SFX v2 generation sounds musical, that is a prompt issue (include "no music, no instruments, no melody" in the text prompt) — it is NOT a reason to switch to the Music API.

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
| Mixed master output | -3 dBFS peak | **-16 LUFS** | TikTok official spec; safe floor for all social platforms |

**Platform loudness targets:**
- Instagram Reels: -14 to -16 LUFS integrated, -1.5 dBTP true peak (Meta uses xHE-AAC; target -16 to be safe)
- TikTok: -16 LUFS integrated, -1 dBTP true peak (official TikTok spec)
- YouTube: -14 LUFS integrated
- ElevenLabs output default: ~-24 LUFS (always normalize before mixing)
- **Safe universal master for all platforms:** -16 LUFS integrated, -1 dBTP (prevents downward normalization on any platform)

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

**Standard (natural ducking):**
```bash
ffmpeg -i voiceover_normalized.mp3 -i ambient.wav \
  -filter_complex \
    "[1:a]aformat=channel_layouts=stereo[amb]; \
     [0:a]asplit=2[narr][sc]; \
     [amb][sc]sidechaincompress=threshold=0.02:ratio=10:attack=50:release=500:knee=2.82843[ducked]; \
     [narr][ducked]amix=inputs=2:duration=first:normalize=0[out]" \
  -map "[out]" -c:a aac -b:a 192k \
  audio_ducked.aac
```

**Aggressive (ads — VO must dominate completely):**
```bash
ffmpeg -i voiceover_normalized.mp3 -i ambient.wav \
  -filter_complex \
    "[1:a]aformat=channel_layouts=stereo[amb]; \
     [0:a]asplit=2[narr][sc]; \
     [amb][sc]sidechaincompress=threshold=0.015:ratio=15:attack=30:release=800:makeup=1:knee=6[ducked]; \
     [narr][ducked]amix=inputs=2:duration=first:normalize=0[out]" \
  -map "[out]" -c:a aac -b:a 192k \
  audio_ducked.aac
```

- `aformat=channel_layouts=stereo` on ambient — required before sidechain to avoid channel-layout errors in FFmpeg 7+
- `threshold=0.02` / `0.015` — triggers when VO signal is present
- `attack=30–50ms` — quick duck at speech start; faster = less music surge on pauses
- `release=500–800ms` — smooth fade-back; shorter = pumping artifact risk; longer = more natural
- `knee=2.82843` (standard) / `knee=6` (aggressive) — soft knee smooths the compression onset
- Use aggressive variant for social ads where ambient must not compete with VO

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

### 4i. De-esser for Dutch ElevenLabs VO (removes sibilance before mixing)

Dutch has heavy /s/ consonants. ElevenLabs VO is often sibilant in the 5–8 kHz range — audible as harshness on phone speakers. Run this ONCE after the dynaudnorm stage (§4h stage 1) and BEFORE loudnorm.

**Basic de-ess (start here):**
```bash
ffmpeg -i voiceover_dynorm.mp3 \
  -af "deesser=i=0.5:m=0.6:f=0.4" \
  voiceover_deessed.mp3
```

Parameters:
- `i=0.5` — intensity (0–1): how readily sibilance triggers reduction; start here, raise to 0.7 if still harsh
- `m=0.6` — max reduction (0–1): amount of treble cut applied; 0.6 is audible but not lispy
- `f=0.4` — frequency keep (0–1): lower = more high-freq removed; 0.4 good for Dutch /s/

**If deesser alone is insufficient — chain with 7 kHz shelf cut:**
```bash
ffmpeg -i voiceover_dynorm.mp3 \
  -af "deesser=i=0.5:m=0.6:f=0.4,equalizer=f=7000:width_type=o:width=2:g=-3" \
  voiceover_deessed.mp3
```

**Caution:** Do NOT use `i=1.0` — creates a dull, lispy result. Always A/B test against the unprocessed VO before committing.

**Full chain order for VO processing:** raw → dynaudnorm → deesser → dialoguenhance (optional, see below) → phone EQ (§4e) → loudnorm → mix

**Optional: `dialoguenhance` for stereo VO clarity (FFmpeg 5.1+):**
Lifts dialogue presence in stereo field. Use before loudnorm on stereo VO; skip for mono VO.
```bash
ffmpeg -i voiceover_deessed.mp3 \
  -af "dialoguenhance=original=0.5:enhance=3:voice=5" \
  voiceover_enhanced.mp3
```
- `original=0.5` — weight of original signal (0.0–1.0)
- `enhance=3` — enhancement factor (1–3 is subtle; 5+ is aggressive)
- `voice=5` — voice band sensitivity (1–3 is conservative)

---

### 4h. Two-stage voiceover normalization (preferred over single loudnorm pass)

**Why two stages?**  
`loudnorm` measures at the clip level and applies a static gain — it does not even out sentence-to-sentence volume variation within the clip.  
`dynaudnorm` operates on sliding 200 ms frames and actively boosts quiet syllables, making the voice consistently audible across the clip before the loudness standard is applied.

**Stage 1 — `dynaudnorm` on raw ElevenLabs output (evens out intra-clip dynamics):**
```bash
ffmpeg -i voiceover_raw.mp3 \
  -af "dynaudnorm=framelen=200:gausssize=11:maxgain=30:peak=0.95" \
  voiceover_dynorm.mp3
```
- `framelen=200` — 200 ms analysis frames; responsive to speech without over-pumping
- `gausssize=11` — smooth gain transitions between frames
- `maxgain=30` — sufficient boost for very quiet passages
- `peak=0.95` — 5% headroom, matches loudnorm default

**Stage 2 — `loudnorm` on dynaudnorm output (EBU R128 broadcast compliance):**
```bash
ffmpeg -i voiceover_dynorm.mp3 \
  -af loudnorm=I=-14:TP=-1.5:LRA=11 \
  voiceover_normalized.mp3
```

Then feed `voiceover_normalized.mp3` into the mix commands (§4b / §4b2).

**Use single `loudnorm` (§4a) ONLY** when the script is already dynamically even (short sentences, consistent delivery). For longer Dutch VO scripts with varied sentence energy, always use the two-stage chain.

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
- [ ] Freesound/Mixkit sounds are CC0 or CC-BY (not CC-BY-NC for commercial ads)
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
| Instagram Reels | -14 to -16 LUFS | -1.5 dBTP | Meta xHE-AAC; exact target not published; -16 is safe floor |
| TikTok | **-14 to -16 LUFS** | -1.0 dBTP | TikTok does NOT apply in-feed loudness normalization — audio plays at delivered level. Target -14 to -16 LUFS to prevent clipping/distortion on phone speakers, not because TikTok normalises down. Going louder (e.g. -10 LUFS) will play louder; going quieter will play quieter. |
| YouTube Shorts | -14 LUFS | -1.0 dBTP | YouTube target |
| WhatsApp / Telegram | -16 LUFS | -1.0 dBTP | Voice-first, slightly lower |

**Rule:** Master to **-16 LUFS / -1 dBTP** for all social media deliverables — this satisfies TikTok's official target AND avoids Instagram downward normalization. Do NOT push louder to "cut through" — triggers limiting and sounds worse. YouTube can accept -14 LUFS if delivering there exclusively.

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
| VO sounds harsh/hissy on phone (Dutch /s/) | ElevenLabs sibilance in 5–8 kHz range | Run `deesser=i=0.5:m=0.6:f=0.4` before loudnorm (see §4i) |
| sidechaincompress errors in FFmpeg 7+ | Channel layout mismatch on ambient input | Add `aformat=channel_layouts=stereo` before sidechain (see §4c) |
| SFX library requires sign-up | Pixabay/Freesound account friction slows workflow | Use Mixkit (mixkit.co) — no account, CC0 commercial, instant download (see §2 Tier 1a) |
| Dutch phonemes sound off | Wrong model | Use `eleven_v3` (production) or `eleven_multilingual_v2` (fallback). Never monolingual v1. |
| Phone number "085 3331133" spoken in English | `language_code` not set / text normalisation off | Set `language_code="nl"` and `apply_text_normalization="on"` in every API call (see §0) |
| Draft VO (Flash v2.5) mispronounces "085 3331133" despite `apply_text_normalization="on"` | `apply_text_normalization` is **Enterprise-only for Flash v2.5** — ignored on standard plans | On non-Enterprise plans, Flash v2.5 always outputs unnormalized phone numbers. Do NOT use Flash v2.5 to QA Dutch phone number pronunciation — use eleven_v3 for that verification step only. |
| VO sounds uneven — loud on some sentences, quiet on others | Single loudnorm pass doesn't equalise intra-clip dynamics | Use two-stage chain: dynaudnorm first, then loudnorm (see §4h) |
| Prosody break / unnatural join between VO chunks | Script split across multiple API calls without continuity hint | Pass `previous_request_ids=[prior_request_id]` in each subsequent call (see §0, multi-chunk section) |
| Pixabay/Mixkit return no suitable SFX for a specific scene | Limited library coverage for niche or locale-specific sounds | Generate with ElevenLabs SFX v2 (`eleven_text_to_sound_v2`, `loop=True`) — see §2 Tier 1c |
| Ambient SFX has click at loop point despite acrossfade | Pre-processing acrossfade not applied, or file too short | Use ElevenLabs SFX v2 with `loop=True` instead — output is natively seamless, no post-processing needed |
| Audio tags work weakly or inconsistently | Prompt too short (< ~250 chars) | Tags need enough context — test with the full production script (≥250 chars), not an isolated sentence |
| Tags `[rushed]` / `[rapid-fire]` accidentally in script | Speed tags sound unprofessional for moving company brand | Add both to pre-generation script review checklist; never use in Snelverhuizen copy |
| SFX has distracting room tone or crowd noise that arnndn can't fully clean | arnndn is for broadband hiss; mixed source noise requires source separation | Use ElevenLabs Voice Isolator (`client.audio_isolation.convert()`) — AI source separation; costs 1000 credits/minute (see §10 Option C) |
| Willem voice_id unknown / not in SDK reference | Voice Library community voices have no public ID list | Fetch once via `GET /v1/voices?search=Willem` and store in project config (see §0) |
| ElevenLabs default voice expiry Dec 31, 2026 | ElevenLabs retiring original 38 pre-made defaults | Willem is a Voice Library voice (NOT a default) — not affected. If you switch to a new ElevenLabs default voice, check expiry at elevenlabs.io/docs |
| FFmpeg 8.x whisper filter — NOT a speech enhancer | whisper filter does ASR transcription only (outputs SRT/JSON) | Do not use as audio enhancement. For voiceover post-processing, continue with arnndn/afwtdn/dynaudnorm/loudnorm/deesser as documented. No new speech enhancement filters added in FFmpeg 8.0 or 8.1. |
| Want instrument-free ambient bed but consider using ElevenLabs Music API `ambience` mode | Music API generates AI music (even in ambience mode) — contains instrumentation | Use ElevenLabs SFX v2 (`eleven_text_to_sound_v2`) instead. Add "no music, no instruments, no melody" to the SFX v2 prompt. Music API is banned in this pipeline. |
| SFX v2 output sounds thin or artifacts after loudnorm | Default SFX v2 output is 22kHz/32kbps MP3 — too low for mixing | Add `output_format="mp3_44100_128"` to every SFX v2 API call. For Pro plan: use `wav_44100` for lossless SFX library masters. |
| TikTok video sounds quieter than expected or louder than other platforms | TikTok does not apply in-feed loudness normalization | Content plays at delivered level. Master to -14 to -16 LUFS for clean phone playback. Do not over-compress to get louder — will sound distorted on mobile. |
| PVC audio tags weak or ignored in eleven_v3 | PVCs not fully optimized for v3 as of April 2026 | Switch to a Voice Library voice (e.g. Willem) or an IVC. Do not use PVCs for eleven_v3 tag-dependent scripts until ElevenLabs confirms full PVC compatibility. |
| Need to verify Willem voice quality before production | No UI check in pipeline | Call GET /v1/voices?search=Willem — check `recording_quality` field. Proceed only if "studio" or "good". If "in_review" labelling_status, hold and re-check next session. |
| Scribe v2 cost over-estimated | Old skill docs said "~1 credit/character" (wrong billing model) | Scribe v2 is billed per audio hour ($0.22/hour batch), not per character. A 30s VO QA call costs ~$0.002. Always cheap — budget is not a constraint for VO QA. |
| VO transcript can't be verified against script | No cheap Dutch STT tool in pipeline | Run Scribe v2 (`model_id="scribe_v2"`, `language_code="nld"`, `timestamps_granularity="word"`) after every generation — see §11 |
| `[pauses]` tag in old scripts not working | Official ElevenLabs form is `[pause]` (no 's') — `[pauses]` may be silently ignored | Update scripts to use `[pause]` (confirmed canonical form from official ElevenLabs blog posts). Both may work but test on Willem to confirm. |
| `[confident]` / `[direct]` ignored on Willem | These are unconfirmed tags; Willem may not respond | Substitute with confirmed `[deliberate]` — same professional pacing effect, confirmed in official ElevenLabs delivery control category. |

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

## 11. Dutch VO Transcription QA (Scribe v2)

Use ElevenLabs Scribe v2 to verify that a generated voiceover matches the intended script and to extract word-level timestamps for caption alignment. Scribe v2 achieves ≤5% WER on Dutch — significantly more accurate than Whisper base on Dutch. GA since March 11, 2026: 99 languages, 98% speaker label accuracy.

**When to run:** after every `eleven_v3` generation before mixing, to catch mispronounced proper nouns (SNELVERHUIZEN, 085 3331133) and confirm Dutch text normalisation applied correctly.

**API call:**
```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Brand-specific keyterms: bias Scribe toward Snelverhuizen proper nouns
BRAND_KEYTERMS = [
    "SNELVERHUIZEN",
    "SNELVERHUIZEN.NL",
    "085 3331133",
    "VERHUIZEN ZONDER ZORGEN",
]

with open("voiceover_raw.mp3", "rb") as f:
    result = client.speech_to_text.convert(
        file=f,
        model_id="scribe_v2",
        language_code="nld",            # Dutch
        timestamps_granularity="word",  # word-level start/end times
        keyterms=BRAND_KEYTERMS,        # biases model toward brand names (see note below)
        no_verbatim=True,               # strips filler words for clean script comparison
    )

# Check transcript against script
print(result.text)

# Word-level timestamps (for caption alignment)
for word in result.words:
    print(f"{word.text:20s}  {word.start:.3f}s → {word.end:.3f}s")
```

**`keyterms` (Scribe v2 batch — confirmed 2026):**
- Biases the model toward recognising the listed terms. Up to 1000 keyterms per call; each ≤50 characters and ≤5 words.
- **+$0.050/hr flat surcharge** applies when `keyterms` is set (base $0.22/hr → $0.27/hr total, ≈23% increase). Not "+20%" — the surcharge is a flat additive rate per audio hour, not a percentage of base.
- Characters not supported in keyterms: `< > { } [ ] \`
- Realtime (WebSocket) variant supports max 50 keyterms at ≤20 chars each — different limits from batch.
- **May 2026 realtime update:** Scribe v2 realtime WebSocket now also accepts `no_verbatim` (removes filler words) and native mute/unmute. These are realtime-only additions; the batch API (used for VO QA) is unchanged.

**`entity_detection` (Scribe v2 — new in 2026):**
Detects PII, PHI, PCI, and offensive language with timestamps. Not needed for VO QA, but useful for compliance screening of user-submitted audio.
- `entity_detection="all"` → detect all 56 entity categories across pii/phi/pci/other/offensive_language
- **+30% cost surcharge** applies when set (already negligible at $0.22/hour base)
- Returns entities in `result.entities` with text, type, and character positions
- Skip for Snelverhuizen VO QA — irrelevant for brand voiceover scripts

**`no_verbatim=True`:** removes filler words, false starts, and disfluencies from the transcript — makes script diff cleaner. Use for VO QA (comparing against intended script). Omit for caption timing use (fillers shift word timestamps).

**Output fields per word:** `text`, `start` (seconds), `end` (seconds), `type` (`word` | `spacing` | `audio_event`).

**Cost:** Scribe v2 is billed **per audio hour**, NOT per character. Batch rate: **$0.22/hour** base (reduced from $0.40/hour — 45% cut, announced May 7, 2026). Keyterm surcharge: +$0.050/hr flat → $0.27/hr total with keyterms. Entity detection: +$0.070/hr. Realtime: $0.39/hour. A 30-second VO costs ~$0.0018 base + $0.000417 keyterm surcharge = **~$0.0022 total** — essentially free for VO QA use. Do NOT budget Scribe as if it were TTS credits.

**QA checklist:**
- [ ] Transcript contains "SNELVERHUIZEN" (not garbled)
- [ ] Phone number "085 3331133" transcribed in Dutch digit form ("nul-acht-vijf...")
- [ ] No extra/dropped words vs. approved script
- [ ] Total duration within ±0.5 s of target video slot length — use `result.audio_duration_secs` (added April 7, 2026; no ffprobe needed)

**`result.audio_duration_secs` (added April 7, 2026):** The response now includes total audio duration as a float. Use this for the ±0.5 s duration check instead of `ffprobe` — saves a subprocess call:
```python
print(f"VO duration: {result.audio_duration_secs:.2f}s")  # compare against target slot
```

**Caption reuse:** the word timestamps from Scribe v2 can be passed directly to `captions-and-titles.md` §2 pipeline (whisper → timecode → Remotion). No separate Whisper run needed.

---

## 10. SFX Noise Reduction

ElevenLabs voiceover is already clean — skip for VO. Use these filters to remove background hiss, HVAC hum, or room noise from Pixabay/Freesound SFX files before mixing.

### Option A: arnndn (neural network — best for preserving ambient texture)

Requires a one-time model file download. Better at retaining room character while removing hiss.

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

### Option B: afwtdn (wavelet-based — no model download, good for tonal/HVAC noise)

Pure FFmpeg, no external model file. Works on broadband and tonal periodic noise (HVAC hum, room modes). Simpler to deploy in environments where model files aren't available.

```bash
ffmpeg -i sfx_noisy.wav \
  -af "afwtdn=sigma=-45dB:nb=10:percent=85" \
  sfx_clean.wav
```

**Parameters:**
- `sigma` — noise level in dB (set to match noise floor; `-45dB` is typical for light hiss; `-35dB` for louder HVAC hum). Default 0 = no denoising — must set explicitly.
- `nb` — wavelet decomposition levels (1–12, default 10). Higher = more thorough but slower.
- `percent` — percent of full denoising applied (0–100, default 85). 85 is a safe partial denoise that retains room character.

**When to use afwtdn vs arnndn:**
- **afwtdn**: HVAC/room hum, mains hum (50/60 Hz); no model download needed; first choice on fresh deployment
- **arnndn**: broadband digital hiss, microphone noise; better speech/voice preservation if any voice content is present in the SFX

**Workflow:** Pre-process once, save as `_clean.wav` in the SFX library for reuse.

### Option C: ElevenLabs Voice Isolator (AI-powered — best for SFX with mixed voice/noise)

Deep-learning model that separates vocal signal from background noise. Useful for cleaning ambient SFX files that contain unwanted room tone, crowd noise, or bleed. Also useful for extracting a clean vocal track from a nasheed that has recording artifacts (room reverb, hiss) — but NOT as a substitute for rejecting a nasheed with actual instruments (policy: reject those outright, do not strip them).

**Cost:** 1000 characters per minute of audio (uses same ElevenLabs credit pool as TTS). A 30-second SFX file costs ~500 credits (~$0.06 at Creator plan rates). Use sparingly — only when arnndn/afwtdn insufficient.

**Supports:** WAV, MP3, FLAC, OGG, AAC (input); up to 500MB / 1 hour. (Note: STT/Scribe accepts up to 5.0GB — the 500MB limit here applies to Voice Isolator specifically.)

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

with open("sfx_noisy.mp3", "rb") as f:
    cleaned = b"".join(client.audio_isolation.convert(audio=f))

with open("sfx_clean.mp3", "wb") as f:
    f.write(cleaned)
```

**When to use vs arnndn/afwtdn:**
- **Voice Isolator**: AI-powered, no local model download; best when SFX contains room tone + voice-like content (e.g., ambient crowd); high-quality result
- **arnndn**: broadband digital hiss from microphone; best for pure noise reduction without isolating a specific source
- **afwtdn**: HVAC/mains hum; no credits consumed

---

## 12. Text to Dialogue API (future use — multi-speaker ads)

ElevenLabs launched a dedicated Text to Dialogue endpoint alongside eleven_v3 GA (March 2026). Generates a single audio file containing multiple speakers in natural conversation. Not needed for current Snelverhuizen single-VO format, but relevant if a future brief calls for two characters (e.g., customer + crew dialogue scene).

**Endpoint:** `client.text_to_speech.text_to_dialogue.convert()` (Python SDK v2.42+)

**Key parameters:**
- `inputs` — array of `{text, voice_id}` objects; each object is one dialogue turn
- Max **10 unique voice IDs** per request
- Max **2,000 characters total** across all `inputs[].text` values (hard limit — split longer dialogues)
- `model_id` — must be `"eleven_v3"` (only model supporting dialogue mode)
- `language_code` — set `"nl"` for Dutch
- `text_normalization` — `"on"` to force Dutch number normalisation (same as TTS `apply_text_normalization`)
- `seed` — optional int for reproducibility (model is nondeterministic)

**Billing:** same per-character rate as TTS. Not a separate credit pool.

**Halal note:** each `voice_id` must be a male voice consistent with modest Islamic advertising standards. Owner approval required before using two-voice format in any production.

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

audio = b"".join(client.text_to_speech.text_to_dialogue.convert(
    inputs=[
        {"text": "[calm] Verhuizen zonder zorgen?", "voice_id": VOICE_ID_CREW},
        {"text": "[warm] Snel Verhuizen regelt alles.", "voice_id": VOICE_ID_NARRATOR},
    ],
    model_id="eleven_v3",
    language_code="nl",
    text_normalization="on",
))

with open("dialogue_output.mp3", "wb") as f:
    f.write(audio)
```

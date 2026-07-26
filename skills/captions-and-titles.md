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

   **Option A: ElevenLabs Forced Alignment (primary, paid)** — TWO endpoints exist, only ONE is verified for word-level timestamps:
   - ✅ **CORRECT: `POST /v1/forced-alignment`** — returns word AND character-level timestamps (submit audio + transcript after TTS generation). Supports **150+ languages including Dutch** (introduced 2025-04; **auto-detects language — no `language` parameter needed**; exceeds eleven_v3's 70+ language set — Python client params are `file` + `text` only, confirmed from SDK 2026-07-18). Works with both `eleven_multilingual_v2` and `eleven_v3`.

     **Response schema (confirmed from Python SDK `ForcedAlignmentResponseModel` — 2026-05-23):**
     ```python
     # response.words → List[ForcedAlignmentWordResponseModel]
     # Each word: .text (str), .start (float, seconds), .end (float, seconds), .loss (float)
     # response.characters → List[ForcedAlignmentCharacterResponseModel]
     # Each char: .text (str), .start (float, seconds), .end (float, seconds)
     # response.loss → float (overall alignment confidence, lower is better)

     # Convert to Remotion Caption format:
     # ⚠️ SPACE CONVENTION: createTikTokStyleCaptions() uses text.startsWith(' ') to detect
     # page boundaries. ElevenLabs returns clean words WITHOUT leading spaces. You MUST add
     # a leading space to every word except the first — otherwise all words land in one page
     # and word-by-word highlighting never fires.
     captions = [
         {
             "text": ("" if i == 0 else " ") + w.text,
             "startMs": int(w.start * 1000),
             "endMs": int(w.end * 1000),
             "timestampMs": int((w.start + w.end) / 2 * 1000),
             "confidence": 1 - w.loss,  # loss → confidence inversion
         }
         for i, w in enumerate(response.words)
     ]
     ```

     **⚠️ Dashboard enablement:** Some users report forced alignment must be enabled in ElevenLabs account settings before the endpoint accepts requests. If you receive a 403 or feature-not-enabled error, check the API features section of your dashboard.

   - ❌ **WRONG for word-level: `POST /v1/text-to-speech/{voice_id}/with-timestamps`** — returns **CHARACTER-ONLY** timestamps regardless of model. The Python SDK `Alignment` type confirms this: fields are `char_start_times_ms`, `char_durations_ms`, `chars` — no word-level fields exist (confirmed 2026-05-23 via SDK inspection). Root cause of V2 caption sync issues 2026-04-09/10. **Do NOT use this endpoint for word-by-word highlighting — use `/v1/forced-alignment` instead.**

     **`alignment` vs `normalized_alignment` in the response:** The `with-timestamps` response contains two character-level alignment objects. `alignment` timestamps map to original input characters (e.g., "0", "8", "5" for the input "085"). `normalized_alignment` timestamps map to characters as spoken after text normalization (e.g., "n","u","l"," ","a","c","h","t"," ","v","i","j","f" for Dutch "085" → "nul acht vijf"). For Dutch ads with phone numbers ("085 3331133") or numerals, `normalized_alignment` matches actual pronunciation and is the correct field to use when grouping characters into word-level boundaries. Still character-level only — group by whitespace to reconstruct words. **Fastest correct path remains `/v1/forced-alignment` which returns true word-level timestamps directly.**
   - Recommended Dutch voices (verified 2026-04-16): male warm 30-40 = `hLnc7y4d152WGG2BQlAY` (Jaimie Amsterdam), female warm 30-40 = `DiUBVrSFwkMaPz4XqWvR` (Jolanda)
   - **Recommended model: `eleven_v3`** (launched 2026-02-12, new flagship — 70+ languages, higher emotional range, audio-tag emotion control via `[whispers]`/`[excited]` tags). Replaces `eleven_multilingual_v2` as primary recommendation. `eleven_multilingual_v2` remains valid fallback if `eleven_v3` produces English-accented Dutch on a specific voice.

   **Dutch pronunciation dictionary with `eleven_v3` (IPA, free to create once):**
   `eleven_v3` is the only ElevenLabs model that supports IPA phoneme rules for non-English languages. Create a pronunciation dictionary once to prevent mispronunciation of Dutch brand terms:

   ```python
   from elevenlabs import ElevenLabs

   client = ElevenLabs()

   # Create once; store the returned dictionary_id in your .env
   response = client.pronunciation_dictionary.create_from_rules(
       rules=[
           # IPA for "SNELVERHUIZEN": /snɛlvərˈhœy̯zə(n)/ — stress on 2nd syllable
           {
               "type": "phoneme",
               "string_to_replace": "SNELVERHUIZEN",
               "phoneme": "snɛlvərˈhœy̯zən",
               "alphabet": "ipa",
               "case_sensitive": True,
           },
           # Alias rule: ensure "VERHUIZEN ZONDER ZORGEN" is read as separate words
           {
               "type": "alias",
               "string_to_replace": "SNELVERHUIZEN.NL",
               "alias": "snel verhuizen punt nl",
               "case_sensitive": False,
           },
       ],
       name="snelverhuizen-nl",
   )
   DICT_ID = response.id  # save this

   # Pass dict when generating TTS:
   audio = client.text_to_speech.convert(
       voice_id="hLnc7y4d152WGG2BQlAY",  # Jaimie Amsterdam
       model_id="eleven_v3",
       text="Bel SNELVERHUIZEN nu!",
       pronunciation_dictionary_locators=[{"pronunciation_dictionary_id": DICT_ID}],
   )
   ```

   **IPA achieves 80–90% consistency** on eleven_v3 (not 100% — re-test if a specific phrase still sounds off). Only `eleven_v3` and `eleven_flash_v2` support phoneme rules; `eleven_multilingual_v2` does not. Alias rules (string substitution) work on all models.

   **Option A2: ElevenLabs Scribe v2 (paid, use for non-TTS / client-provided audio)**
   **⛔ `scribe_v1` was REMOVED on July 9, 2026 (confirmed). Any code using `scribe_v1` will throw 404 — use `scribe_v2` only.**

   **⛔ Also removed July 9, 2026: `eleven_monolingual_v1` and `eleven_multilingual_v1` (legacy v1 TTS models — confirmed removed).** Our pipeline uses `eleven_v3` (primary) and `eleven_multilingual_v2` (fallback) — no migration needed.
   When the audio is NOT ElevenLabs TTS (e.g. client testimonial, on-site recording, phone call), forced alignment is unavailable. Scribe v2 is the best alternative within the ElevenLabs ecosystem — no Python or Node.js model download required.

   - **Dutch supported** (`language: "nl"` or leave null for auto-detect)
   - **Word-level timestamps** returned in response: `words[].text`, `words[].start` (seconds), `words[].end` (seconds)
   - **Pricing:** $0.22/hour of audio — a 30-second voiceover costs ~$0.002. Negligible.
   - **File size limit:** Up to 5.0GB per submission (increased from 3.0GB in June 2026). Our 30-60s WAV files (~5–20MB) are far below this.
   - **Keyterm biasing** (`+$0.05/hr`): pass up to **1,000 keyterms** (50 characters each, expanded April 2026 — was 100). Use for Dutch brand names that would otherwise be mangled. **⚠️ Billing note:** requests with >100 keyterms incur a minimum billable unit of 20 seconds. For our short 30-60s voiceovers this has no practical impact.
     ```python
     keyterms = ["SNELVERHUIZEN", "snelverhuizen.nl", "085 3331133", "VERHUIZEN ZONDER ZORGEN"]
     ```
   - **`no_verbatim: True`** — strips filler words ("uh", "uhm") from transcription output; leave False for voiceovers (TTS never produces fillers).
   - **`tag_audio_events` (default: `True`) — ⚠️ ALWAYS set `False` for TTS voiceover audio.** Scribe v2 defaults to tagging non-speech events (`[laughter]`, `[music]`, `[footsteps]`, etc.) in the transcript word list. For clean TTS audio these tags never occur naturally, but if present they add spurious tokens with their own timestamps that pollute the word list and cause off-by-one errors when converting to Remotion captions. Explicitly set `tag_audio_events=False` for all voiceover audio. Only set `True` when processing client-recorded field audio where ambient events are meaningful.
   - **`additional_formats`** — Scribe v2 can emit SRT/TXT/DOCX in the same response. Pass `additional_formats=["srt"]` to receive a ready-made SRT string alongside the JSON transcript. Useful shortcut for the ASS/FFmpeg fallback path (Option B in ASS Karaoke section below) — no need to post-process JSON to SRT manually.
   - **`seed`** — pass any integer (e.g. `seed=42`) for deterministic output across re-runs. Useful when the pipeline retries transcription after a failure and needs identical timestamps.
   - **`entity_detection` (default: `False`) — detects and tags up to 56 entity categories** (names, dates, locations, credit card numbers, SSNs, etc.) with their timestamps. Adds cost. **ALWAYS leave `False` for TTS brand-ad voiceovers** — there is no PII in "Bel SNELVERHUIZEN nu!" and the extra tags pollute the word list. Only relevant for client-provided testimonial recordings where PII might appear.
   - **`redact_pii` (default: `False`) — automatically removes PII from the returned transcript.** Three output modes: complete → `[REDACTED]`; categorized → `[CREDIT_CARD]`; enumerated → `[CREDIT_CARD_1]`. **ALWAYS leave `False` for TTS voiceover** — brand ad scripts contain no PII. Setting this on a clean voiceover transcript achieves nothing and risks mangling brand names. Only use for client-provided recordings with real personal data.
   - **Mixed language support (automatic, no config needed):** Scribe v2 auto-transcribes English words embedded in Dutch audio correctly — e.g. "call us" spoken in English within a Dutch voiceover stays as "call us" rather than being force-normalized to Dutch. This requires no parameter; it is on by default. Relevant for ads that mix Dutch narration with English brand phrases.
   - **Dutch accuracy (Scribe v2 benchmark):** WER ≤5% — Excellent tier on ElevenLabs' internal multilingual benchmark. In practice: brand names and phone numbers may still need keyterm biasing; normal narration transcribes correctly without it.

   ```python
   from elevenlabs import ElevenLabs
   import json

   client = ElevenLabs()  # uses ELEVENLABS_API_KEY env var

   with open("voiceover.wav", "rb") as f:
       result = client.speech_to_text.convert(
           file=f,
           model_id="scribe_v2",         # scribe_v1 removed July 9, 2026 (confirmed). scribe_v2 only.
           language_code="nl",           # Dutch; omit for auto-detect
           timestamps_granularity="word", # required for word-level timestamps
           tag_audio_events=False,       # ⚠️ REQUIRED for TTS audio — default True adds spurious event tokens
           keyterms=["SNELVERHUIZEN", "snelverhuizen.nl", "085 3331133"],  # optional
           no_verbatim=False,            # keep False for TTS audio
           entity_detection=False,       # keep False for TTS voiceover — adds cost, no PII in brand ads
           redact_pii=False,             # keep False for TTS voiceover — no PII to redact in brand ads
           seed=42,                      # optional: deterministic output for reproducibility
       )

   # Convert to Remotion Caption format:
   # ⚠️ SPACE CONVENTION: same as forced alignment — Scribe v2 returns clean words.
   # Add leading space to every word except the first so createTikTokStyleCaptions()
   # can detect page-break boundaries via text.startsWith(' ').
   word_tokens = [w for w in result.words if w.type == "word"]  # filter out spacing tokens
   captions = [
       {
           "text": ("" if i == 0 else " ") + w.text,
           "startMs": int(w.start * 1000),
           "endMs": int(w.end * 1000),
           "timestampMs": int((w.start + w.end) / 2 * 1000),
           "confidence": 1.0,
       }
       for i, w in enumerate(word_tokens)
   ]
   ```

   **When NOT to use Scribe:** For ElevenLabs TTS voiceovers where you have both audio + transcript, always prefer `/v1/forced-alignment` (Option A) — it gives exact timestamps by aligning the known transcript, whereas Scribe transcribes and may produce slightly different wording. Scribe is for **unknown audio** only.

   **Scribe v2 Realtime (WebSocket mode — NOT for this pipeline):** Launched January 6, 2026. 150ms latency over WebSocket for live speech. As of June 2026, accepts `keyterms` (array, max 50 entries × 20 chars each) and `no_verbatim` params — both echoed back in `session_started` event. Key limit vs batch: keyterms capped at **50 terms, 20 chars each** (vs batch Scribe: **1,000 terms, 50 chars each** — expanded April 2026). Use case is live agent calls / real-time transcription — our pipeline uses pre-recorded voiceover so batch mode is always correct.

   **Option B: WhisperX (free, $0, use when ElevenLabs credits are low)**
   Dutch (`nl`) supported via wav2vec2 forced alignment. **Version requirement: `>=3.8.6`** — v3.8.7rc1 released June 26, 2026 is a pre-release (Windows CUDA fix + huggingface-hub pin relax only — no timestamp changes). **Stay on stable 3.8.6** for production. — v3.8.2 fixed a wildcard alignment bug; v3.8.4 fixed blank_id for HuggingFace models and restored digit/symbol timestamps ("085 3331133", "4,9 ster"); v3.8.5 (April 2026) pins torchvision/torchcodec for torch 2.8 compatibility + includes PR #1347 fix (SRT/ASS subtitle cue timestamps now derived from word-level data, not VAD segment boundaries — previously caused premature cue display); v3.8.6 (May 25, 2026) fixes handling of the 'ignore' interpolation method in `interpolate_nans` — when Dutch wav2vec2 alignment fails on unusual tokens (foreign proper nouns, special characters), the code falls back to interpolation; the bug caused incorrect timestamps in those edge cases. Older versions silently produce wrong timestamps.

   **Dependency requirement (v3.8.6+):** `faster-whisper>=1.2.0` is required. Install both:
   ```bash
   pip install "faster-whisper>=1.2.0" "whisperx>=3.8.6"
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

   **Qwen3-ForcedAligner (free, watch item — Dutch NOT yet supported as of 2026-07-18):**
   Released January 2026 by Alibaba Cloud. The 0.6B model achieves ~42.9ms average alignment shift (AAS) vs WhisperX wav2vec2's ~133.2ms on MFA-labeled data (Qwen3-ASR technical report) — a 67-77% error reduction. Its 11 supported languages are: Chinese, English, Cantonese, French, German, Italian, Japanese, Korean, Portuguese, Russian, Spanish. **Dutch (nl) is not in the supported set.** Qwen3-ASR (the companion transcription model) does support Dutch, but without Dutch ForcedAligner support, it cannot improve our timestamp accuracy over wav2vec2. The current WhisperX + wav2vec2 + Dutch last-word fix (Option B above) remains the correct free path. Monitor `Qwen/Qwen3-ForcedAligner-0.6B` on HuggingFace for Dutch addition — if added, it would be a meaningful accuracy upgrade.

   **Option C: @remotion/install-whisper-cpp with DTW (free, Remotion-native, no Python needed)**
   Uses whisper.cpp with Dynamic Time Warping on attention weights — no separate language model. Works for Dutch without a wav2vec2 model. Integrates directly with `toCaptions()`.

   **Version requirements for large-v3-turbo:** Remotion v4.0.229+ AND whisper.cpp v1.8.x+. Do NOT use `version: '1.5.5'` with turbo — it silently fails.

   **⚠️ Minimum recommended: whisper.cpp v1.8.5.** v1.8.5 (May 29, 2026) includes PR #2279 — fixes incorrect segment-start timestamps near silence gaps. Root cause: the model produces extra consecutive timestamp tokens between segments that the library was ignoring; when there is a pause between phrases, the next segment's `startMs` was placed at the end of the previous segment instead of after the actual gap. For Dutch voiceovers with natural pauses between phrases ("Bel ons nu... 085 3331133"), this caused captions to appear mid-silence before the word was spoken. v1.8.6 (June 2, 2026) adds no timestamp changes. v1.8.7 (June 16, 2026) — maintenance only: library path fixes, UTF-8 token merge in server, C++ exception handling in `whisper_init`, CoreML quantize/ANE fixes, `--version` CLI flag. No DTW or timestamp changes. v1.9.0 (June 17, 2026) — adds NVIDIA Parakeet model support (new architecture, separate from Whisper models) and Ruby bindings for Parakeet. No DTW or timestamp changes. **v1.9.1 (June 19, 2026) is the current latest** — CI build fixes for Windows BLAS only (GGML_NATIVE=OFF, GGML_BMI2=OFF). **No DTW, timestamp, or Parakeet changes** — all timing behavior identical to v1.8.5+. Upgrade is safe and recommended: Remotion's `installWhisperCpp()` accepts any semantic version string. Use `WHISPER_VERSION = '1.9.1'` for new installs.

   **⚠️ REQUIRED PARAMETERS (confirmed from source, v4.0.469):** Both `installWhisperCpp()` and `transcribe()` have mandatory parameters that must be supplied explicitly — there are no defaults:
   - `installWhisperCpp()` requires `to: string` — the directory where whisper.cpp will be installed
   - `transcribe()` requires `whisperPath: string` — same path passed to `installWhisperCpp(to:)`
   - `transcribe()` requires `whisperCppVersion: string` — must match the version string used in `installWhisperCpp(version:)`

   Omitting any of these will cause a TypeScript compile error (they have no `?` in the interface).

   **Two transcription modes — pick one:**

   **Mode A (DTW, recommended):** `tokenLevelTimestamps: true` adds `--dtw` to whisper.cpp. Produces the most accurate single-point timestamp per word (`t_dtw`). `tokensPerItem` and `splitOnWord` have **no effect** in DTW mode.

   ```typescript
   import { installWhisperCpp, transcribe, toCaptions } from '@remotion/install-whisper-cpp';

   const WHISPER_PATH = './whisper-cpp';   // installation directory
   const WHISPER_VERSION = '1.9.1';        // v1.8.5+ for PR #2279 silence-gap fix; 1.9.1 is current latest (June 19, 2026 — confirmed 2026-07-26, no newer release)

   await installWhisperCpp({
     version: WHISPER_VERSION,
     to: WHISPER_PATH,       // REQUIRED — no default
     printOutput: false,
   });

   const result = await transcribe({
     inputPath: 'voiceover.wav',
     whisperPath: WHISPER_PATH,          // REQUIRED — path from installWhisperCpp(to:)
     whisperCppVersion: WHISPER_VERSION, // REQUIRED — must match install version
     model: 'large-v3-turbo',           // ~3x faster than large-v2, same Dutch accuracy (Remotion v4.0.229+)
     language: 'nl',
     tokenLevelTimestamps: true,        // enables --dtw; tokensPerItem/splitOnWord ignored in this mode
     flashAttention: false,             // keep false on CPU; set true only with CUDA GPU
     modelFolder: './whisper-models',   // optional: custom model folder (see caching note below)
     printOutput: false,                // default is true — suppress console noise in production
   });
   const { captions } = toCaptions({ whisperCppOutput: result });
   // captions → Caption[] ready for createTikTokStyleCaptions()
   // timestampMs field uses t_dtw (DTW-derived) when tokenLevelTimestamps: true —
   // most accurate single-point timestamp available from whisper.cpp.
   // Without tokenLevelTimestamps, timestampMs falls back to (startMs + endMs) / 2.
   //
   // ⚠️ timestampMs CAN BE NULL: when whisper.cpp DTW fails for a token (t_dtw === -1),
   // toCaptions() sets timestampMs = null. Always null-check before using:
   //   const activeMs = caption.timestampMs ?? caption.startMs;
   // confidence is also number | null — null-safe default to 1.0.
   ```

   **Mode B (non-DTW, one-word-per-segment):** Use when DTW produces errors or you need strict 1-word-per-Caption output. `tokensPerItem: 1` sets `--max-len 1` (one word per segment); `splitOnWord: true` adds `--split-on-word` to prevent a word being split across two segments at the `max-len` boundary. **Only works with `tokenLevelTimestamps: false`.**

   ```typescript
   const result = await transcribe({
     inputPath: 'voiceover.wav',
     whisperPath: WHISPER_PATH,          // REQUIRED
     whisperCppVersion: WHISPER_VERSION, // REQUIRED
     model: 'large-v3-turbo',
     language: 'nl',
     tokenLevelTimestamps: false, // DTW off; enables tokensPerItem + splitOnWord
     tokensPerItem: 1,            // --max-len 1 → one word per Caption
     splitOnWord: true,           // --split-on-word → no mid-word segment breaks
     flashAttention: false,
     modelFolder: './whisper-models',  // optional: point to shared model cache
     printOutput: false,               // suppress console noise in production
   });
   const { captions } = toCaptions({ whisperCppOutput: result });
   // Each Caption covers exactly one word — good for createTikTokStyleCaptions()
   // timestampMs = (startMs + endMs) / 2 (no DTW), timing slightly less accurate
   ```

   **Optional parameters worth knowing:**
   - `onProgress?: (progress: number) => void` — callback receiving 0–1 progress updates during transcription (useful for long voiceovers)
   - `signal?: AbortSignal` — cancel an in-progress transcription via `AbortController`
   - `modelFolder?: string` — if specified, `transcribe()` looks for `ggml-{model}.bin` in this folder instead of the default `{whisperPath}/models/` path. Use when model is stored separately from the whisper.cpp binary (e.g. a persistent Docker volume or S3-backed cache).
   - `printOutput?: boolean` — defaults to `true`. Set `false` in production to suppress whisper.cpp CLI output from stdout. Already shown in examples above.
   - `translateToEnglish?: boolean` — **defaults to `false`. NEVER set to `true` for Dutch voiceovers** — it translates the transcript to English, producing English captions over Dutch audio. Also: do NOT use a `*.en` model (e.g. `base.en`) when this is `true`, as `.en` models cannot translate non-English audio. For this pipeline: always omit or explicitly pass `translateToEnglish: false`.

   **Model caching pattern (important for cloud/containerized pipeline):**
   `ggml-large-v3-turbo.bin` is ~820MB. In ephemeral containers it re-downloads every session without a cache. Avoid this with `downloadWhisperModel()`:

   ```typescript
   import { downloadWhisperModel, installWhisperCpp, transcribe, toCaptions } from '@remotion/install-whisper-cpp';

   const WHISPER_PATH = './whisper-cpp';
   const MODEL_FOLDER = './whisper-models'; // persistent volume or pre-provisioned dir
   const WHISPER_VERSION = '1.9.1';

   await installWhisperCpp({ version: WHISPER_VERSION, to: WHISPER_PATH, printOutput: false });

   const { alreadyExisted } = await downloadWhisperModel({
     model: 'large-v3-turbo',
     folder: MODEL_FOLDER,  // downloads to MODEL_FOLDER/ggml-large-v3-turbo.bin
     printOutput: false,    // suppress download progress messages
     onProgress: (p) => process.stderr.write(`\rModel download: ${Math.round(p * 100)}%`),
   });
   if (alreadyExisted) console.log('Using cached model — no download needed');

   const result = await transcribe({
     inputPath: 'voiceover.wav',
     whisperPath: WHISPER_PATH,
     whisperCppVersion: WHISPER_VERSION,
     model: 'large-v3-turbo',
     modelFolder: MODEL_FOLDER, // transcribe() finds the bin file here
     language: 'nl',
     tokenLevelTimestamps: true,
     flashAttention: false,
     printOutput: false,
   });
   const { captions } = toCaptions({ whisperCppOutput: result });
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

   Version: 4.0.498 (confirmed July 24, 2026 — synced with main Remotion package). Only use Option D for: browser-only apps with no server component, rapid prototyping, or languages where small models are sufficient (English/Spanish).

   **Option E: @remotion/openai-whisper (paid OpenAI API — NOT for this pipeline)**
   Package converts OpenAI Whisper API output directly into `Caption[]` compatible with `createTikTokStyleCaptions()`. Requires `timestamp_granularities: ['word']` in the OpenAI transcription call. Dutch is supported. **Do not use** — OpenAI API is paid and our pipeline is AIMLAPI-only per Farouq directive 2026-04-16. Use Options B or C instead. Documented here for awareness only.

   ```typescript
   import { openAiWhisperApiToCaptions } from '@remotion/openai-whisper';
   // transcription = OpenAI API response with timestamp_granularities: ['word']
   const { captions } = openAiWhisperApiToCaptions({ transcription });
   // → Caption[] compatible with createTikTokStyleCaptions()
   ```

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

**`Easing.spring` (new in Remotion v4.0.476) — inline spring for `interpolate()`:**

Previously, scaling an active word required calling the standalone `spring()` function (needs `frame`, `fps`, `config`). With `Easing.spring`, you can pass spring physics directly to `interpolate()` without a separate hook — cleaner for per-token animations inside a `.map()`:

```tsx
import { interpolate, Easing } from 'remotion';

// In a token map — no useCurrentFrame() needed per-token
const progress = interpolate(
  isActive ? 1 : 0,  // binary: active or not
  [0, 1],
  [1, 1.05],
  { easing: Easing.spring({ damping: 12, stiffness: 200, mass: 1.0 }), extrapolateRight: 'clamp' }
);
// → scale value that springs to 1.05 when active, springs back to 1.0 when not active
```

`Easing.spring` config (v4.0.483+ full signature):
```typescript
type EasingSpringConfig = Partial<{
  damping: number;        // default 10
  mass: number;           // default 1
  stiffness: number;      // default 100
  overshootClamping: boolean; // default false — clamps OUTPUT value at 1
}> & {
  allowTail?: boolean;            // default false (new v4.0.483)
  durationRestThreshold?: number; // default undefined (new v4.0.483)
};
```
- `overshootClamping: true` — output value never exceeds 1 (good for opacity animations)
- `allowTail: true` — allows the spring to continue past `t=1` and oscillate naturally past the end point. **Do NOT use for caption word-highlight scale** — it causes each word to over-bounce, which distracts from readability. USE for title/name card spring entrances where a natural overshoot "pop" is desired.
- `durationRestThreshold` — controls when the spring is considered "settled" (rest threshold). Lower value = spring must settle more completely before stopping; affects how the easing duration is measured internally.

Internal simulation runs at 30fps.

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

**Remotion v4.0.499 (July 24, 2026):**
- Zod bumped to 4.4.3; Studio sidebar clamping, visibility toggle, keyframe selection improvements; `@remotion/drag-and-drop` new payload package; `@remotion/web-renderer` opacity rendering fix; template dependency updates (PostCSS, React Router).
- **No changes to `@remotion/captions` API.**
- `npm install remotion@4.0.499`.

**Remotion v4.0.498 (July 23, 2026):**
- Core: SwiftShader fallback (v5.0 preview); `trimBefore` sequence freeze interaction fix; `@remotion/paths` and Next.js template updates; `@remotion/media` and `@remotion/renderer` changes.
- **No changes to `@remotion/captions` API.**

**Remotion v4.0.497 (July 23, 2026):**
- Studio: background color editing, direct premounting for image components, timeline asset-drop support; `@remotion/transitions`, `@remotion/gif`, and `@remotion/cli` changes.
- **No changes to `@remotion/captions` API.**

**Remotion v4.0.496 (July 21, 2026):**
- Studio layout refinements; asset opening in new windows; HtmlInCanvas fallback rendering fixes in web-renderer; prevent parentheses around wrapped assets in studio-server.
- **No changes to `@remotion/captions` API.**

**Remotion v4.0.495 (July 20, 2026):**
- Studio: Figma paste/SVG paste support; composition inspector actions; nested sequence reordering fix; image metadata in asset inspector; split-clip action; open existing render output. Direct premounting for Video/Audio; seek when adjusting trim points.
- **No changes to `@remotion/captions` API.**

**Remotion v4.0.494 (July 19, 2026):**
- **Fixed "Preserve Sequence opacity while active"** — Previously, opacity applied at the `<Sequence>` level was not reliably preserved while the sequence was playing. This affected caption fade-out animations where opacity was set directly on `<Sequence style={{ opacity: ... }}>` rather than on the inner component. If you use opacity on `<Sequence>` for caption page fades, upgrade to 4.0.494. Workaround for older versions: apply opacity inside the child component instead.
- Fix AnimatedImage playback rate; Keep interactive components visible with negative offsets (Studio only).
- **No changes to `@remotion/captions` API.**

**Remotion v4.0.493 (July 19, 2026):**
- Composition metadata editing in inspector; connected composition navigation; keyframe copy/paste (Studio only).
- Internal: "Add animated captions tester" — a Studio dev tool for testing animated captions; not a user-facing API change.
- **No changes to `@remotion/captions` API.**

**Remotion v4.0.492 (July 19, 2026):**
- "Negative Video offsets in sequences fixed" — edge case where `<Video>` with a negative `startFrom` inside a `<Sequence>` rendered incorrectly. Unlikely to affect caption-only compositions.
- Flannel visual effect added.
- **No changes to `@remotion/captions` API.**

**Remotion v4.0.491 (July 18, 2026):**
- **Client-side rendering (CSR) launched** (`renderMediaOnWeb()` / `@remotion/web-renderer`). **Caption CSS warning for CSR:** CSR emulates CSS via `getBoundingClientRect()` and canvas drawing — it does NOT support all CSS properties. The following caption styles may NOT render in CSR: `-webkit-text-stroke`, `paint-order: stroke fill`, `borderRadius` on arbitrary elements, complex `text-shadow`. To get correct caption rendering in CSR, enable **HTML-in-canvas mode (requires Chrome 152+)** — this takes a full screenshot instead of emulating CSS and supports all styling. **Our Node.js server-side render pipeline (`npx remotion render`) is NOT affected** — this warning applies only if you ever switch to `renderMediaOnWeb()`.
- `@remotion/media` marked stable and recommended; `liquidContours` and `skew()` effects added.
- **No changes to `@remotion/captions` API.**

**Remotion v4.0.490 (July 16, 2026):**
- New package: `@remotion/rough-notation` (hand-drawn annotation animations — not relevant for caption pipeline).
- `remotion`: New `output: "perceptual-scale"` option for `interpolate()` — maps values through a sqrt transform so scale animations feel more natural to human perception (uses `sign(x) * x²` → interpolate → `sign(x) * √|x|`). Studio now defaults scale keyframes to perceptual output. **Not needed for caption word-scale (1.0 → 1.05 range is too small for perceptual nonlinearity to matter; keep linear or `Easing.spring`).** Useful for wider-range scale transitions (0 → 1.5+).
- `@remotion/effects`: Progressive pixelation effect added.
- **No changes to `@remotion/captions` API** — caption pipeline is unaffected. `npm install remotion@4.0.490`.

**Remotion v4.0.489 (July 12, 2026):**
- `@remotion/studio`: Request element install targets on demand; use runtime Studio config.
- `@remotion/studio-server`: Fix file source origin check; reject origin-less requests.
- `remotion`: Fix image loading during premount transitions.
- **No changes to `@remotion/captions` API** — caption pipeline is unaffected.

**Remotion v4.0.488 (July 11, 2026):**
- **Fixed looped audio dropping out after multiple iterations.** If your caption composition includes a looped ambient audio layer (e.g., background ambience looped for the full video duration), it previously cut out silently after repeating several times. Now fixed. Safe to upgrade.
- ProRes decoder support added to `@remotion/media`. Mediabunny upgraded to 1.50.8.
- **No changes to `@remotion/captions` API** — caption pipeline is unaffected.

**Remotion v4.0.487 (July 9, 2026):**
- ProRes support added to `@remotion/media`. Easing.cubic support in interactivity.
- **No changes to `@remotion/captions` API** — caption pipeline is unaffected.

**Remotion v4.0.486 (July 7, 2026):**
- **Fixed WebM tail frame extraction following the last keyframe.** If you load a rendered caption WebM inside a Remotion composition via `<OffthreadVideo>`, frames past the last keyframe previously returned garbage/black. Affects pipelines that composite captions inside Remotion (not FFmpeg-only pipelines).
- Delayed CanvasImage rendering until canvas presentation — affects `<OffthreadVideo>` with canvas-based rendering.
- New docs: official Sequence freeze recommendations published (the `freeze` prop pattern documented below is now officially documented).

**Remotion v4.0.485 (July 6, 2026):**
- **Fixed `media playbackRate` duration calculation in loops.** If your caption composition includes looped ambient audio/video, its duration was calculated incorrectly at non-1x playback rates. Now fixed — verify any looped audio layer timing after upgrading.
- Preview frame accuracy improved (Studio only).

### Full API (v4.0.499 — confirmed current as of 2026-07-26; no caption API changes in 4.0.485–4.0.499)

| Export | Purpose |
|--------|---------|
| `createTikTokStyleCaptions()` | Groups `Caption[]` into pages with per-token timing for word highlight |
| `parseSrt()` | Parses SRT → `Caption[]` — input: `{ input: string }` object. **Block-level only, NO word timestamps** |
| `serializeSrt()` | Serializes `Caption[]` back to SRT string (round-trip) |
| `CaptionsInternals.ensureMaxCharactersPerLine()` | Splits `Caption[]` into line segments with max char limit + orphan prevention |
| `Caption` | Type: `{ text: string, startMs: number, endMs: number, timestampMs: number \| null, confidence: number \| null }` |
| `TikTokPage` | Type: `{ text, startMs, durationMs, tokens: TikTokToken[] }` — `durationMs` added v4.0.261 |
| `TikTokToken` | Type: `{ text, fromMs, toMs }` — named export for TypeScript typing |
| `EnsureMaxCharactersPerLineInput` | Direct named type export (TypeScript only) — input type for `CaptionsInternals.ensureMaxCharactersPerLine` |
| `EnsureMaxCharactersPerLineOutput` | Direct named type export (TypeScript only) — output type for `CaptionsInternals.ensureMaxCharactersPerLine` |
| `ParseSrtInput`, `ParseSrtOutput` | Direct named type exports for `parseSrt()` |
| `SerializeSrtInput` | Direct named type export for `serializeSrt()` |
| `CreateTikTokStyleCaptionsInput`, `CreateTikTokStyleCaptionsOutput` | Direct named type exports for `createTikTokStyleCaptions()` |

No `parseWebVtt()` exists in this package. No `convertToCaptions()` either — that was deprecated at v4.0.216; use `toCaptions()` from `@remotion/install-whisper-cpp` instead.

### CRITICAL: parseSrt() does NOT give word-level timestamps

`parseSrt()` returns one `Caption` per SRT block with a single `startMs`/`endMs` for the entire phrase. If you feed WhisperX `--output_format srt` through `parseSrt()`, word-by-word highlighting will NOT work — every word in the block gets the same timing and the orange highlight stays stuck.

**For word-by-word highlight, use WhisperX JSON or whisper.cpp output (Options B/C above).** Use `parseSrt()` only for subtitle-style display where you show one phrase at a time with no per-word highlight.

### Preferred Implementation

```bash
npx remotion add @remotion/captions
```

#### Production Pattern: useDelayRender() for async caption loading

**Required** when fetching captions from a JSON file at render time. Without it, Remotion renders frames before caption data loads — frames come out with no captions.

```tsx
import { delayRender, continueRender, useCurrentFrame, useVideoConfig } from 'remotion';
import { createTikTokStyleCaptions } from '@remotion/captions';
import { useState, useEffect } from 'react';

export const CaptionComposition = () => {
  const [captions, setCaptions] = useState(null);
  const [handle] = useState(() => delayRender()); // suspend rendering
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTimeMs = (frame / fps) * 1000;

  useEffect(() => {
    fetch('/captions.json')
      .then(r => r.json())
      .then(data => {
        setCaptions(data);
        continueRender(handle); // resume rendering
      })
      .catch(e => {
        console.error(e);
        continueRender(handle); // MUST always call even on error
      });
  }, [handle]);

  if (!captions) return null;
  // ... render captions
};
```

#### Page rendering with <Sequence> (recommended for performance)

Each caption page as its own `<Sequence>` lets Remotion skip inactive pages during render.

**New in v4.0.477 — `freeze` prop on `<Sequence>`:** You can now pass `freeze?: number | null` directly on `<Sequence>` instead of wrapping it in a separate `<Freeze>` component. When set, the sequence content freezes at that frame number. Useful for holding a caption page visible on screen after the audio ends — set `freeze={durationInFrames - 1}` to pin the last frame:

```tsx
import { Sequence } from 'remotion';

const { pages } = createTikTokStyleCaptions({ captions, combineTokensWithinMilliseconds: 500 });

{pages.map((page, i) => (
  <Sequence
    key={i}
    from={Math.round(page.startMs / 1000 * fps)}
    durationInFrames={Math.round(page.durationMs / 1000 * fps)}
  >
    <CaptionPage page={page} fps={fps} />
  </Sequence>
))}

// Inside CaptionPage: useCurrentFrame() returns frames RELATIVE to sequence start
// → const relativeMs = (useCurrentFrame() / fps) * 1000;
// → const isActive = relativeMs >= (token.fromMs - page.startMs) && relativeMs < (token.toMs - page.startMs);
```

**`freeze` prop example — hold last caption frame:**
```tsx
// Before v4.0.477: had to wrap in <Freeze>
// After v4.0.477: pass freeze directly on <Sequence>
{pages.map((page, i) => {
  const durationFrames = Math.round(page.durationMs / 1000 * fps);
  return (
    <Sequence
      key={i}
      from={Math.round(page.startMs / 1000 * fps)}
      durationInFrames={durationFrames}
      freeze={i === pages.length - 1 ? durationFrames - 1 : undefined}
      // ↑ last page only: freeze on final frame so caption persists until next scene cut
    >
      <CaptionPage page={page} fps={fps} />
    </Sequence>
  );
})}
```

**New in v4.0.482 — `trimBefore` prop on `<Sequence>`:** You can now trim the beginning of a `<Sequence>`'s child timeline without affecting its `from`/`durationInFrames` visibility window. Child content starts rendering from frame `trimBefore` onward — frames before that are skipped as if fast-forwarded. Useful for caption pages when a scene cut lands mid-entrance-animation and you want to skip the first N frames of the spring-in so the word appears already visible rather than mid-bounce:

```tsx
// Scene cut arrives 8 frames into a caption page's spring entrance animation
// trimBefore={8} makes the caption start from frame 8 of its animation —
// word is already in final position when it first appears, no half-finished spring
<Sequence
  from={Math.round(page.startMs / 1000 * fps)}
  durationInFrames={Math.round(page.durationMs / 1000 * fps)}
  trimBefore={8}  // skip first 8 frames of CaptionPage's entrance animation
>
  <CaptionPage page={page} fps={fps} />
</Sequence>
```

Unlike `trimBefore` on `<Audio>`/`<Video>` (which skips media file playback), `trimBefore` on `<Sequence>` propagates an offset through the child timing context — `useCurrentFrame()` inside the child sees `trimBefore` as frame 0.

#### Inline conditional (simpler, same result):

```tsx
import { createTikTokStyleCaptions } from '@remotion/captions';

// captions = Caption[] from WhisperX JSON, whisper.cpp toCaptions(), or ElevenLabs
const { pages } = createTikTokStyleCaptions({
  captions,
  combineTokensWithinMilliseconds: 500, // word-by-word
});
// Each page: { text: string, startMs: number, durationMs: number, tokens: TikTokToken[] }
// durationMs is available from v4.0.261 — use it to advance pages:
// const currentPage = pages.find(p => currentTimeMs >= p.startMs && currentTimeMs < p.startMs + p.durationMs);

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

**Simpler alternative for basic line-wrapping:** Set `maxWidth: '80%'` (or a pixel value like `maxWidth: 840`) directly on the caption container `<div>`. This lets the browser/Remotion renderer wrap naturally without needing pre-processing. Use `ensureMaxCharactersPerLine` when you need precise control over per-word line breaks (e.g. preventing orphan 1-word tail); use `maxWidth` CSS when simple visual wrapping is enough.

### CRITICAL: Leading-Space Convention for Page Breaks

`createTikTokStyleCaptions()` detects page boundaries by checking `text.startsWith(' ')` in each `Caption`. A new page is started **only** when a caption whose text begins with a space arrives after `combineTokensWithinMilliseconds` have elapsed.

**Source behavior by provider:**
- ✅ **whisper.cpp / `toCaptions()`** — already adds leading spaces; works out of the box
- ✅ **WhisperX** — wav2vec2 BPE tokens naturally carry leading spaces; works out of the box
- ❌ **ElevenLabs forced alignment** — returns clean words (no spaces); MUST add manually (see fix above)
- ❌ **ElevenLabs Scribe v2** — same; MUST add manually (see fix above)

**Failure mode if missing:** Every word is appended to the FIRST page; `createTikTokStyleCaptions` never breaks; the orange highlight advances but the same block of text stays on screen for the entire voiceover.

### Key Parameter: combineTokensWithinMilliseconds

- `500` — Word-by-word (classic TikTok style, fastest pace)
- `600`–`800` — **Premium pace for business/service ad content** (2-3 word chunks held 600–900ms — 2026 industry shift: premium short-form video is slowing down from rapid word-by-word toward more deliberate chunk timing; increases comprehension without losing energy)
- `1200` — Phrase-by-phrase (calmer, educational content)
- `2000` — Sentence-level (subtitle-style, matches parseSrt() input)

**Snel Verhuizen recommendation:** Use `700` (or `combineTokensWithinMilliseconds: 700`) for voiceover captions. Dutch is spoken at moderate pace; 700ms gives 2-3 word chunks that feel cinematic without rushing. Use `500` only if voiceover is fast-paced (>160 wpm).

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

### FFmpeg 8.0 Built-in Whisper Filter — NOT for word-level captions

FFmpeg 8.0 "Huffman" (August 2025, current stable: 8.1.2 released June 17, 2026) added a native `whisper` audio filter that performs ASR transcription inside FFmpeg itself using whisper.cpp. **Do NOT use this for Snel Verhuizen caption pipeline.** Reason: it outputs segment-level SRT/JSON only — no word-level timestamps, no word-by-word highlighting. Suitable only for basic subtitle overlays without per-word orange highlight. Our pipeline requires word-level timestamps from Options A/B/C above.

```bash
# What FFmpeg 8.0 whisper filter does (context only — not for our pipeline):
# ffmpeg -i voiceover.wav -af "whisper=model=path/to/ggml-large-v3-turbo.bin:language=nl" output.srt
# → produces segment-level SRT, timestamps at phrase level, not word level
# → word-by-word orange highlight is impossible with this output
```

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

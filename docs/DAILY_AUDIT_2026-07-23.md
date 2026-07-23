# Daily Audit — 2026-07-23

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-07-22 | Operator 2.54/5.0 · Skills 87.5% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-07-22 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **2.85 / 5.0** | ↑ +0.31 | ↓ −1.00 |
| Skill Library & Policy | **88.1%** (141/160) | ↑ +0.6% | ↓ −3.4% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Two study cycles (SC239–SC240) since the 2026-07-22 audit.** Operator score rebounds +0.31 — the single strongest one-window gain since SC tracking began. The driver is protocol recovery: SC239 is a clean pair (0% bundling vs 75% last window) and SC240 is a clean content commit. D2 Execution and D4 Reliability both rise sharply. The ROOT-clean streak extends to 3 consecutive windows. **CLAUDE.md remains frozen for the 27th consecutive audit.**

**SC240's highest-value finding:** Wan 2.7 R2V status upgraded from "not live" to **canary-test recommended** — AIMLAPI published a blog post covering R2V as a Wan 2.7 mode. Endpoint `alibaba/wan-2-7-r2v` may now be callable; canary documented with Karel `front.png`, 720p, muted audio, InsightFace ≥ 0.62 gate. All third-party providers confirmed live; AIMLAPI docs still have no dedicated R2V page. This is the first new character model canary opportunity since Turbo Pro reached HIGH confidence in SC237.

**90 days without approved creative output.** 3 canaries outstanding (Wan 2.2 Animate Replace $0.06, Wan 2.7 R2V, Kling Turbo Pro). 23 days to LTXV Aug-15 deadline with no CLAUDE.md routing alert. 14 days past ElevenLabs v1 retirement with no CLAUDE.md fix.

---

## CHANGES SINCE 2026-07-22 AUDIT

Git commits since `8662076` (July 22 audit):

| Hash | Commit | Files changed | DB path | Protocol |
|------|--------|---------------|---------|---------|
| 6419ee3 | SC239: Halal audio (pass 36) — FFmpeg 9.0 confirmed stable, 3 missing AllowedOutputFormats entries | `skills/halal-audio.md` only | — | ✓ CLEAN CONTENT |
| 25e0be3 | SC239 log: record study cycle 239 commit hash in pipeline.db | `data/pipeline.db` only | `data/` ✓ | ✓ CLEAN LOG |
| 329b9e6 | SC240: Character consistency (pass 35) — Kling O3 still not on AIMLAPI, Wan 2.7 R2V canary-test recommended, FixTalk EMI/EDI mechanism names added | `skills/character-consistency.md` only | — | ✓ CLEAN CONTENT (no log yet) |

**Protocol compliance this window:**
- Clean pairs: **SC239 = 1/1 (100%)** — full recovery from last window's 0/4 (0%) worst-ever record
- Bundled commits: **0/2 (0%)** — complete reversal of last window's 75% bundling regression
- SC240 dedicated log: **ABSENT** — content committed at 00:09 today; audit runs before log commit was made (not retroactively missing; expected to be committed after this audit)
- ROOT pipeline.db path errors: **0/2** — ROOT-clean streak extends to 3 consecutive windows ✓

**DB integrity note:** `study_log` table still stuck at cycle 234 (id=39) — SC235–SC240 absent (10 consecutive missing). Study cycles table has SC239 (id=118) and SC240 (id=119) present. Production sessions querying `study_log` continue to miss intelligence from the last 6 study cycles. This is the 10th consecutive cycle missing from `study_log`.

---

## SC CONTENT NOTES

**SC239** — `halal-audio.md` (6419ee3, Wed Jul 22 06:08:58) — +4/−1 lines (net +5):
- **FFmpeg 9.0 confirmed current stable as of July 2026.** All pipeline audio filter commands (loudnorm, dynaudnorm, sidechaincompress, arnndn, afwtdn, deesser, dialoguenhance) unchanged through 8.1 and 9.0.
- **3 undocumented AllowedOutputFormats entries added:** `mp3_44100_32`, `mp3_44100_64`, `mp3_44100_96`. All three categorized as "too lossy for production" — `mp3_44100_128` remains the minimum acceptable MP3 format. Completes the format table.
- **FFmpeg whisper filter note extended:** Entry updated from "8.x" to "8.x/9.x" — confirms no word-level timestamps in FFmpeg 9.0 either; prevents future misuse.
- Commit body: ✓ Detailed with specific per-finding breakdown and policy guidance.
- Protocol: ✓ CLEAN CONTENT (skill only) + ✓ CLEAN LOG (25e0be3, DB only) = **CLEAN PAIR**.

**SC240** — `character-consistency.md` (329b9e6, Thu Jul 23 00:09:47) — +3/−3 lines (net 0):
- **Wan 2.7 R2V: "not live" → "canary-test recommended".** AIMLAPI blog post covers R2V as a Wan 2.7 mode. Endpoint `alibaba/wan-2-7-r2v` may be callable; no dedicated docs.aimlapi.com page yet. Canary sequence: Karel `front.png` + 720p + muted audio + InsightFace ≥ 0.62. If `model-not-found` → fall back to `wan-2.6-reference-to-video` or Kling O1. All third-party providers confirmed live (Segmind, Replicate, Together AI, Kie.ai, EvoLink, inference.sh, WaveSpeedAI).
- **Kling O3 recheck (pass 35, 2026-07-23):** docs.aimlapi.com confirms only v3-standard, v3-standard-turbo, v2.6-motion-control, v2-master — O3 still NOT listed. Still not on AIMLAPI; per Farouq directive, continue Kling O1 until O3 lands.
- **FixTalk EMI/EDI mechanism names added:** EMI (Enhanced Motion Indicator) decouples identity from motion features; EDI (Enhanced Detail Indicator) re-injects leaked identity features to fix rendering artifacts. Precision improvement to existing entry (arXiv 2507.01390, ICCV 2025).
- Commit body: ✓ 5 specific bullets with sources, dates, and production guidance.
- Protocol: ✓ CLEAN CONTENT (skill only); dedicated log commit pending.

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 3.0/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC240: Wan 2.7 R2V status upgrade | Upgraded from "not live" to "canary-test recommended" based on AIMLAPI blog post — single-source evidence, correctly scoped to canary (not production) with explicit fallback if model-not-found | Strong positive |
| SC240: Kling O3 recheck with docs confirmation | Uses docs.aimlapi.com endpoint list (v3-standard/turbo, v2.6, v2-master) as authoritative verification — recheck dated correctly, conclusion unchanged | Strong positive |
| SC239: FFmpeg 9.0 pipeline-impact assessment | "All existing audio filter commands unchanged through 9.0" — correct non-action verdict; prevents unnecessary pipeline disruption | Positive |
| SC239: AllowedOutputFormats analysis | 3 undocumented formats correctly categorized: too lossy for production, but completeness value noted | Positive |
| SC240: FixTalk EMI/EDI naming | Precision improvement — mechanism names added without changing the practical advice already in place | Positive |
| **CLAUDE.md Pre-Gen Check #5 still wrong (27th audit)** | "15-40 words" → 2.3 rerolls per character shot (Kling v3 requires 40–120w I2V) | Critical negative |
| **ElevenLabs v1 retirement still absent (27th flag, 14 days past)** | Guaranteed 404 at next voiceover session | Critical negative |
| **LTXV Aug-15 — 23 days, 8th audit without CLAUDE.md alert** | B-roll routing still includes LTXV with no deprecation warning | Negative |
| **SC166 absent (22nd audit)** | Differential prompt rule validated by 2 papers; still not in model-prompting-guide.md Part 4 | Negative |

**Score: 3.0/5.0** (↑ +0.1 — SC240's Wan 2.7 R2V upgrade is a well-calibrated judgment from incomplete evidence with appropriate caution; SC239 FFmpeg 9.0 assessment is correct non-action reasoning; persistent CLAUDE.md non-propagation is the structural floor)

---

### D2 — Execution Accuracy (20%) → 2.3/5.0 (↑ +0.6)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC239 content commit | skills/halal-audio.md only — no DB in content commit | ✓ CLEAN |
| SC239 log commit | data/pipeline.db only (25e0be3) — separate, dedicated | ✓ CLEAN LOG |
| SC239 = CLEAN PAIR | Content-only commit + dedicated log = textbook clean pair | ✓ Strong positive |
| SC240 content commit | skills/character-consistency.md only — no DB in content commit | ✓ CLEAN |
| SC240 log | Not yet committed (SC240 at 00:09, audit before log) | → Pending |
| Bundling rate | **0/2 (0%)** — full reversal of last window's 75% regression | ✓ Critical improvement |
| ROOT DB errors | **0/2** — ROOT-clean streak: 3 consecutive windows | ✓ Sustained improvement |
| CLAUDE.md frozen | **27th consecutive audit** — zero structural updates | ❌ Critical structural |

**Score: 2.3/5.0** (↑ +0.6 — SC239 is a textbook clean pair; 0% bundling reverses last window's worst-ever regression; ROOT-clean streak at 3 windows; CLAUDE.md still frozen for 27th consecutive audit)

---

### D3 — Memory & Continuity (15%) → 2.4/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC240: Wan 2.7 R2V — single-source signal handled correctly | Correctly tagged as "canary-test recommended" not "confirmed" — single blog post without dedicated docs page = appropriate caution | Positive |
| SC240: Kling O3 recheck using docs.aimlapi.com endpoint list | Consistent pass-35 recheck with stronger source (endpoint docs vs. general statements) — no premature upgrade | Strong positive |
| SC239: FFmpeg filter versions tracked longitudinally | Entry extended from 8.x to 8.x/9.x — consistent maintenance without false new discoveries | Positive |
| study_cycles table: SC239–240 present (id 118–119) | ✓ study_cycles current and complete | Positive |
| **study_log: stuck at cycle 234 — SC235–240 ABSENT (10th cycle)** | Production sessions querying study_log miss 6 cycles of intelligence including camera_control fix, fal.ai elements cap, Turbo Pro HIGH, wave()/noiseDisplacement(), Wan 2.7 R2V canary | Critical negative |
| **SC166 absent (22nd audit)** | Differential prompt rule never formalized | Negative |
| Camera_control correction still not in CLAUDE.md | SC237 finding is in skill; CLAUDE.md routing matrix has no camera_control section | Negative |

**Score: 2.4/5.0** (↑ +0.1 — Kling O3 recheck with docs-confirmation is stronger evidence than prior passes; Wan 2.7 R2V upgrade is correctly scoped; study_log fragmentation (10 consecutive missing cycles) is the persistent structural ceiling)

---

### D4 — Reliability & Consistency (20%) → 2.2/5.0 (↑ +0.7)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC239 = CLEAN PAIR | First clean pair after 3/4 bundled last window — protocol behavior normalized | ✓ Strong positive |
| SC240 = CLEAN CONTENT | Second clean content commit in a row | ✓ Positive |
| 0/2 bundled | Complete reversal of last window's 75% regression | ✓ Critical improvement |
| ROOT DB error streak: 3 windows clean | Was 7 consecutive ROOT-error windows; now 3 consecutive clean | ✓ Sustained structural improvement |
| No false retroactive fill claims | Consistent with prior clean window | Positive |
| CLAUDE.md frozen 27th audit | Zero structural updates in 27 days | ❌ Critical structural |
| 90 days without approved output | Production reliability = 0 | Negative |

**Score: 2.2/5.0** (↑ +0.7 — SC239 clean pair + SC240 clean content + 0% bundling + 3-window ROOT-clean streak together represent the strongest protocol signal in 6+ audit windows; CLAUDE.md still frozen for 27th consecutive audit is the non-negotiable ceiling)

---

### D5 — Tool/Model Integration (15%) → 4.2/5.0 (→ 0.0)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC240: Wan 2.7 R2V canary documented | Endpoint `alibaba/wan-2-7-r2v` + Karel front.png + 720p + muted audio + InsightFace ≥ 0.62 + fallback to wan-2.6-r2v | Strong positive |
| SC240: Kling O3 docs endpoint list | v3-standard/turbo, v2.6-motion-control, v2-master — definitive negative confirmation for O3 | Positive |
| SC239: AllowedOutputFormats table complete | 3 undocumented formats documented with production guidance | Positive |
| SC239: FFmpeg 9.0 pipeline stability confirmed | Prevents unnecessary pipeline migration effort | Positive |
| **CLAUDE.md routing matrix: LTXV still active (23 days to Aug-15)** | B-roll I2V routing would hit a deprecated model | Critical negative |
| **CLAUDE.md Check #5 wrong prompt length (27th audit)** | Active wrong guidance at point of generation | Critical negative |
| **CLAUDE.md Check #7: ElevenLabs v1 retirement absent (27th flag)** | 404 at next voiceover session | Critical negative |
| Wan 2.2 Animate Replace canary still unrun (SC234, 10+ days) | Parameters confirmed; $0.06/gen; 24× cheaper than Kling Pro | Negative |
| Wan 2.7 R2V canary now recommended (SC240) | Third outstanding canary — highest potential ROI if confirmed | Negative |

**Score: 4.2/5.0** (→ 0.0 — SC240's Wan 2.7 R2V canary documentation adds a new actionable test with well-specified parameters; SC239's FFmpeg 9.0 stability confirmation prevents pipeline disruption; CLAUDE.md divergence pattern unchanged)

---

### D6 — Communication & Social (10%) → 3.6/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC239 commit body | Detailed: per-finding breakdown (FFmpeg 9.0, 3 formats, whisper filter extension), explicit "nothing dramatically new since SC232" qualification — models intellectual honesty | ✓ Strong |
| SC240 commit body | 5 specific bullets with pass numbers, recheck dates, and production guidance (Wan 2.7 R2V canary sequence, O3 docs confirmation, FixTalk mechanism names) | ✓ Strong |
| SC239: "nothing dramatically new" qualifier | Explicitly states lack of major finds rather than inflating minor maintenance as discovery | ✓ Anti-sycophancy positive |
| 2/2 commit bodies this window | Both substantive, with sources and dates | ✓ Consistent quality |

**Score: 3.6/5.0** (↑ +0.1 — SC239's "nothing dramatically new since SC232" qualifier demonstrates appropriate hedging; SC240's 5-bullet body with specific canary sequence and docs verification is strong; consistent quality across both cycles)

---

### D1–D6 Weighted Score

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|-------------|
| D1 Reasoning | 3.0 | 20% | 0.600 |
| D2 Execution | 2.3 | 20% | 0.460 |
| D3 Memory | 2.4 | 15% | 0.360 |
| D4 Reliability | 2.2 | 20% | 0.440 |
| D5 Integration | 4.2 | 15% | 0.630 |
| D6 Social | 3.6 | 10% | 0.360 |
| **Total** | — | 100% | **2.85 / 5.0** |

**Delta vs 2026-07-22: +0.31** — SC239 clean pair + SC240 clean content + 0% bundling rate + 3-window ROOT-clean streak together produce the strongest protocol signal in 6+ audit windows. This is the largest single-window gain in recorded session history.

**Failure classification:**
- DISCIPLINE: CLAUDE.md frozen (27th audit), ElevenLabs v1 not fixed, LTXV Aug-15 not in CLAUDE.md, SC166 absent, Wan 2.2 canary unrun, Wan 2.7 R2V canary unrun
- ARCHITECTURAL: study_log not receiving SC log entries (write mechanism uses study_cycles table only; study_log stuck at cycle 234)
- MODEL CAPABILITY CEILING: none this window

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

**20 skills × 8 criteria = 160 total points maximum**

Skills assessed: anti-sycophancy, brand-identity, brief-intake, captions-and-titles, character-consistency, cinematic-standards, credit-efficiency, generation-image, generation-video, halal-audio, higgsfield-generation, kling-truck-prompting, model-ceiling-detection, model-prompting-guide, post-production, production-checklist, shariah-compliance, text-overlay-compositing, video-qa-rubric, viral-research.

**Previous: 140/160 = 87.5%**

### Changes this window (SC239–SC240)

**halal-audio.md (SC239):**
- Accuracy: +0.5 (FFmpeg whisper filter note extended to 8.x/9.x; FFmpeg 9.0 pipeline stability confirmed; AllowedOutputFormats table now complete)
- Coverage: +0.5 (3 undocumented MP3 formats added with production guidance)
- Net: **+1.0 point** (skill was already strong; these fill genuine gaps)

**character-consistency.md (SC240):**
- Accuracy: +0.5 (Kling O3 dated 2026-07-23 with docs.aimlapi.com endpoint confirmation; Wan 2.7 R2V status upgrade with correct source qualification)
- Coverage: +0.5 (Wan 2.7 R2V canary sequence added with endpoint/params/fallback; FixTalk EMI/EDI mechanism names)
- Net: **+0.5 points** (existing skill was current; SC240 adds one new canary entry; awarding conservatively)

**Total new points this window: +1.5 → applying conservatively as +1.0 net**

**Persistent deductions (unchanged from previous audit):**
- model-ceiling-detection.md: C8 wrong (Veo 3.1 Lite I2V in escalation path) — 22nd audit, −1
- model-prompting-guide.md Part 4: SC166 differential prompt rule absent — 22nd audit, −1
- CLAUDE.md meta-compliance: Pre-Gen Check #5 wrong prompt length, ElevenLabs v1 absent, LTXV Aug-15 absent, Wan 2.2 Animate Replace absent — continuing deductions
- Wan 2.7 R2V now "canary-test recommended" per SC240 but absent from CLAUDE.md routing matrix

**Score: 141/160 = 88.1%** (↑ +0.6% — halal-audio.md AllowedOutputFormats completion and character-consistency.md Wan 2.7 R2V canary documentation are the meaningful gains; structural skill gaps unchanged)

### CLAUDE.md Structural Audit

| Component | Status |
|-----------|--------|
| THREE-AGENT PATTERN | ✓ Present |
| PRE-GENERATION CHECKS (10 items) | ❌ Check #5 wrong ("15-40 words" → should be I2V 40-120 / T2V 80-150); Check #7 ElevenLabs v1 IDs absent (retired July 9, 14 days overdue); Check #9 syntax stale (`face adherence 80-90` → `face_consistency: true`) |
| PRODUCTION GATES (10 items) | ✓ Present and accurate |
| MODEL ROUTING MATRIX | ❌ LTXV row missing deprecation warning (23 days to Aug-15 deadline); Wan 2.2 Animate Replace absent; Wan 2.7 R2V canary-test recommended (SC240) but absent; Turbo Pro not reflected as HIGH-quality confirmed |
| BRAND BINARY CHECKLIST | ✓ Present |
| BANNED WORDS IN MOTION PROMPTS | ✓ Present |
| SHARI'AH COMPLIANCE | ✓ Present |
| ANTI-SYCOPHANCY | ✓ Present |
| FAMILY LOCK-IN | ✓ Present |
| SNORKEL TRIAGE | ✓ Present |

**CLAUDE.md structural score: 7/10 components fully correct** (3 components with active errors/omissions — unchanged from previous 5 audits)

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved video:** V3-Tarik-v2-couple (2026-04-26) — **90 days ago.** No new creative output this window.

**Family lock status:** `testimonial` family, 3/6 videos approved. 3 more required before family unlock (lock_until: 6).

**Cost metric:** Credits per approved video = MATHEMATICALLY UNDEFINED (zero new output, day 90).

### Four-Tier Rubric (carried forward from 2026-04-26 output)

**Tier 1 — Technical Gate (binary pass/fail)**
- Resolution ≥1080p: ✓
- Frame rate 24-30fps: ✓
- Correct duration and aspect ratio: ✓
- No corruption: ✓
- Audio: intentionally silent at generation (halal compliance) ✓
- Watermarks: none ✓
- **Tier 1 result: PASS**

**Tier 2 — Visual Quality (1–5, target ≥3.5)**

| Dimension | Score |
|-----------|-------|
| hand_anatomy | 3.5 |
| face_consistency_vs_reference | 4.2 |
| physics_plausibility | 4.0 |
| ai_artifact_severity | 3.8 |
| lighting_coherence | 4.1 |
| **Tier 2 average** | **3.9** |

**Tier 3 — Brand Accuracy (1–5, target ≥4.0)**

| Element | Score |
|---------|-------|
| Logo color #FC8434 | 4.5 |
| Truck cargo box (no side door) | 4.0 |
| Crew uniform | 4.0 |
| Truck text legibility | 3.8 |
| Box design | 4.5 |
| **Tier 3 average** | **4.2** |

**Tier 4 — Ad Effectiveness (1–5, target ≥3.5)**

| Dimension | Score |
|-----------|-------|
| Cinematic composition | 4.2 |
| Narrative clarity | 4.1 |
| Brand recall likelihood | 4.0 |
| CTA clarity | 4.0 |
| **Tier 4 average** | **4.1** |

### New Production Intelligence (SC239–SC240)

**Halal audio (SC239):**
- FFmpeg 9.0 is current stable — no pipeline changes needed. All audio filter commands remain valid.
- ElevenLabs AllowedOutputFormats table now complete. `mp3_44100_128` remains minimum acceptable format for production mixing.
- FFmpeg 8.x/9.x whisper filter: segment-level only — confirmed not suitable for word-level captions through FFmpeg 9.0.

**Character consistency (SC240):**
- **NEW CANARY OPPORTUNITY:** Wan 2.7 R2V recommended for canary test — `alibaba/wan-2-7-r2v` + Karel `front.png` + 720p + `generate_audio: false` + InsightFace ≥ 0.62. If confirmed, adds a third character animation option alongside Kling O1 and Wan 2.6 R2V.
- Kling O3: still NOT on AIMLAPI as of 2026-07-23. docs.aimlapi.com confirms no O3 endpoint. Expected cost when it arrives: $0.5625/5s (vs $1.46 for O1) — continue planning for migration.
- FixTalk: EMI/EDI mechanism names now documented — useful when briefing vendors on identity-leakage mitigation for Act-Two workflows.

### Ralph Loop

*"What would a senior creative director still reject?"*

1. **Three canaries outstanding for 90 days of no output, all documented and ready to run.**
   - Wan 2.2 Animate Replace ($0.06/gen, 24× cheaper than Kling Pro) — SC234, 10+ days outstanding.
   - Wan 2.7 R2V (SC240 — just upgraded to canary-test recommended; endpoint documented).
   - Kling Turbo Pro (HIGH quality confidence, SC237; only AIMLAPI cost/audio confirmation needed).
   Any one of these could unlock a cost tier that accelerates production. All are blocked purely by "no production session was run." A senior creative director would consider this a planning failure, not a capability gap.

2. **ElevenLabs v1 retirement: 14 days past. CLAUDE.md still silent.** Next voiceover session hits 404 on `eleven_monolingual_v1` / `eleven_multilingual_v1` / `scribe_v1`. The operator knows this (SC halal-audio.md has the fix); the policy document does not. A 5-minute CLAUDE.md edit would eliminate a guaranteed debugging session.

3. **LTXV Aug-15 deadline: 23 days.** CLAUDE.md routing matrix lists B-roll I2V without a deprecation warning. Replacement documented in `credit-efficiency.md` (`minimax/hailuo-2.3-fast`, $0.0416/sec) but not in CLAUDE.md. A production session today following CLAUDE.md routing could route B-roll to `ltxv/ltxv-2-fast` — a model that will return errors in 23 days.

4. **study_log fragmentation: 10 consecutive missing cycles (SC235–SC240).** Production sessions using `study_log` for pre-production intelligence will miss the camera_control API correction (SC237), fal.ai elements cap (SC237), Turbo Pro HIGH confidence (SC237), wave()/noiseDisplacement() effects (SC235), FFmpeg whisper filter scope (SC238), and Wan 2.7 R2V canary recommendation (SC240). This is not a study cycle quality issue — it is a retrieval failure that makes all those findings effectively invisible at the decision point.

**Overall Creative: (3.9 + 4.2 + 4.1) / 3 = 4.07 / 5.0** (→ unchanged, day 90 of production stagnation)

CREATIVE_AUDIT_COMPLETE

---

## ACTION ITEMS

### [P0 — CRITICAL — 27th audit — CLAUDE.md: 3 fixes needed in one edit session]

**1. Fix Pre-Gen Check #5: prompt length**
```
Current:  Motion prompt: 15-40 words, motion ONLY, defined endpoint ("eases to stop")
Correct:  Motion prompt: I2V 40-120 words / T2V 80-150 words (Kling v3, July 2026).
          Motion ONLY — action arc + camera move + defined endpoint. (15-40w was Kling v1/v2.)
```

**2. Fix Pre-Gen Check #7: ElevenLabs v1 retirement (14 DAYS OVERDUE)**
```
⚠️ RETIRED JULY 9, 2026: eleven_monolingual_v1 / eleven_multilingual_v1 / scribe_v1 → 404 NOW.
Use: eleven_v3 (TTS production) / eleven_flash_v2_5 (TTS draft) / scribe_v2 (captions).
NOTE: language_code NOT supported on eleven_multilingual_v2 (silently ignored, June 29, 2026).
grep -r "monolingual_v1\|scribe_v1" scripts/ before voiceover work.
```

**3. Routing matrix: LTXV alert + Wan 2.2 Animate Replace + Turbo Pro + Wan 2.7 R2V**
```
⚠️ LTXV DEADLINE Aug 15 (23 days): ltxv/ltxv-2-fast WILL ERROR after Aug 15.
  → Use minimax/hailuo-2.3-fast ($0.0416/sec) for non-char I2V.

Add row: Character animation canary | Wan 2.2 Animate Replace | $0.06/gen
  (alibaba/wan2.2-14b-animate-replace; video_url + image_url + resolution: "720p")

Add row: Character animation canary | Wan 2.7 R2V | TBD
  (alibaba/wan-2-7-r2v; reference_images + 720p + generate_audio: false; InsightFace ≥ 0.62)

Update: Kling Turbo Pro character consistency: HIGH confidence (multi-source July 2026).
  Canary required for AIMLAPI cost/audio only — run 3s reference before locking finals.
```

---

### [P0 — BEFORE NEXT PRODUCTION SESSION — 3 canaries outstanding]

**4. Wan 2.7 R2V canary (SC240, NEW):**
- Call `alibaba/wan-2-7-r2v` with Karel `front.png` + simple 5s reference clip + 720p + `generate_audio: false`
- If `model-not-found` → fall back to `wan-2.6-reference-to-video` or Kling O1; update status to "confirmed not live"
- If output received: score with InsightFace (PASS ≥ 0.62) + brand binary checklist + owner review
- If confirmed: adds a 3rd character animation tier with unknown cost (likely lower than Kling O1)

**5. Wan 2.2 Animate Replace canary (SC234, 10+ days outstanding):**
- Step 1: Pass NBP Edit hero frame as `image_url` + simple 5s drive video as `video_url`, mode: Move
- Step 2: Verify output quality + confirm $0.06 billing in AIMLAPI credit log
- Step 3 (if Move passes): Run Replace mode with B-roll + hero frame reference
- If confirmed: adds $0.06/gen character animation tier (24× cheaper than Kling Pro $1.46)

**6. Kling Turbo Pro canary (SC237, 11+ days outstanding):**
- Quality confidence: HIGH (multi-source confirmed). Remaining unknowns: AIMLAPI cost/sec, audio default.
- Canary: `klingai/video-v3-turbo-pro` + `generate_audio: false` + 3s reference clip + confirm billing.
- If confirmed: Turbo Pro becomes draft character animation tier, replacing Standard.

---

### [P0 — DATA INTEGRITY — study_log missing SC235–SC240 (10 cycles)]

**7. Investigate study_log write mechanism and backfill:**
- `study_cycles` table (data/pipeline.db): SC235–240 present (id 114–119) — SC log commits write here.
- `study_log` table: stuck at cycle 234 (id=39) — 10 consecutive cycles missing.
- Production sessions querying `study_log` miss: camera_control API correction, fal.ai elements cap, Turbo Pro HIGH, wave()/noiseDisplacement(), FFmpeg whisper filter scope, Wan 2.7 R2V canary.
- Action: Determine whether study_log is legacy or active; if active, identify why SC log commits write to study_cycles but not study_log. Backfill SC235–240.

---

### [P0 — OPERATIONAL — model-ceiling-detection.md C8 — 22nd consecutive audit]

**8. Remove Veo 3.1 Lite I2V from escalation path** (one-line removal — Veo 3.1 Lite is T2V only)

---

### [P0 — BEFORE NEXT CHARACTER SESSION — SC166 — 22nd audit]

**9. model-prompting-guide.md Part 4 — add SC166 differential prompt rule:**
```
On facial-movement retries: use action-only prompts; strip identity-descriptive words.
(Validated by Stand-In (arXiv 2508.07901) + WildActor (arXiv 2603.00586) — both confirm
character attributes in text compete with identity flow. Text = action+camera ONLY.)
```

---

### [P1 — COMMIT PROTOCOL]

**10. SC240 dedicated log commit:** SC240 content was committed at 00:09 2026-07-23 without a DB log entry. A dedicated SC240 log commit (data/pipeline.db only) is pending. Commit after this audit.

---

### [P1 — BEFORE NEXT B-ROLL SESSION]

**11. Upgrade Remotion to ≥4.0.496** (SC235/SC238): Fixes Sequence opacity bug (4.0.494) and adds muted prop (4.0.492). Both affect caption overlay sequences. `npm install remotion@4.0.496`.

**12. ffmpeg-normalize update (SC232):** `pip install ffmpeg-normalize --upgrade` to get v1.41.1. Add `--threshold 1.0`; remove `-c:a aac` flag (v1.41.0 infers from container).

---

## TELEGRAM REPORT STATUS

Telegram delivery attempted. No TELEGRAM_BOT_TOKEN found at `~/.claude/channels/telegram/.env` or in environment. Telegram report NOT sent.

Report text (for manual resend if needed):
```
📊 Daily Audit 2026-07-23 — Snelverhuizen Pipeline

Operator: 2.85/5.0 (+0.31) ↑ — best 1-window gain in history
Skills:   88.1% (+0.6%)
Creative: 4.07/5.0 (→) — day 90, no new output

Protocol breakthrough: SC239 = clean pair, 0% bundled (was 75% last window).
ROOT-clean: 3 consecutive windows.
CLAUDE.md still frozen (27th audit).

TOP 3 ACTION ITEMS:
1. CLAUDE.md edit: fix Check #5 prompt length, add ElevenLabs v1 warning (14d overdue), add LTXV Aug-15 alert (23d)
2. Run Wan 2.7 R2V canary (SC240 new: alibaba/wan-2-7-r2v, Karel front.png, 720p)
3. Run Wan 2.2 Animate Replace canary ($0.06/gen, 10+ days outstanding)
```

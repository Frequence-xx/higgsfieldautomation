# Daily Audit — 2026-07-25

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-07-24 | Operator 3.03/5.0 · Skills 88.8% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-07-24 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **2.92 / 5.0** | ↓ −0.11 | ↓ −0.93 |
| Skill Library & Policy | **89.5%** (143.25/160) | ↑ +0.7% | ↓ −2.0% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Four study cycles (SC244–SC247) since the 2026-07-24 audit. SC247 arrived during this audit run.** Operator score falls to 2.92/5.0 (−0.11) — first regression after two consecutive windows of gains. The primary driver is a ROOT DB error recurrence: **SC245 and SC246** log commits wrote to `pipeline.db` (repository root, 61 440 B) instead of `data/pipeline.db` (155 648 B), breaking the 4-window ROOT-clean streak. SC247 immediately corrects course — clean pair + study_log write — providing partial recovery but not reversing the window-level regression.

**Skill content quality is high across all four cycles:** SC244's Kling v3 parameter-trap documentation (legacy faceStrength/subjectStrength dropped; reference_strength is a UI slider not a raw API param) is the window's strongest technical contribution. SC247's Wan 2.7 R2V status upgrade from "canary-test recommended" to **"AIMLAPI blog-confirmed available"** is the highest-value intelligence addition — the R2V canary is now unblocked and should be run immediately.

**Persistent structural blockers:** CLAUDE.md frozen for the 29th consecutive audit. ElevenLabs v1 model IDs are now 16 days past retirement (404 guaranteed). LTXV Aug-15 deadline is 21 days away with no alert in the routing matrix. study_cycles id=118 still contains "FFmpeg 9.0 confirmed as current stable" (false) — P0 from July 24 audit, unaddressed. study_log partial recovery: SC247 wrote id=41 (cycle=247) but SC244/245/246 absent (gap: 10 cycles). Creative output: day 92 with no approved video.

---

## CHANGES SINCE 2026-07-24 AUDIT

Git commits since `acd03df` (July 24 audit):

| Hash | Commit | Files changed | DB path | Protocol |
|------|--------|---------------|---------|----------|
| 5a3cc19 | SC244: Kling v3 Pro parameters (pass 32) — dropped v1/v2 face params, reference_strength clarification, multi-shot min duration discrepancy, status dates July 24 | `skills/generation-video.md` only | — | ✓ CLEAN CONTENT |
| d9096c8 | SC244 log: record study cycle 244 commit hash in pipeline.db | `data/pipeline.db` only | `data/` ✓ | ✓ CLEAN LOG |
| 2370803 | SC245: Caption pipeline (pass 37) — Remotion 4.0.498, FFmpeg 8.1.2, whisper.cpp/WhisperX unchanged | `skills/captions-and-titles.md` only | — | ✓ CLEAN CONTENT |
| 8e0d69e | SC245 log: record study cycle 245 commit hash in pipeline.db | `pipeline.db` (ROOT) ❌ | ROOT ❌ | ❌ ROOT DB ERROR |
| 4d14ab2 | SC246: Halal audio (pass 37) — SDK v2.59.0 confirmed, PCM low-rate formats added to table | `skills/halal-audio.md` only | — | ✓ CLEAN CONTENT |
| 650b262 | SC246 log: record study cycle 246 commit hash in pipeline.db | `pipeline.db` (ROOT) ❌ | ROOT ❌ | ❌ ROOT DB ERROR |
| 519c566 | SC247: Character consistency (pass 36) — Wan 2.7 R2V AIMLAPI blog-confirmed available, Kling O3 still not on AIMLAPI (2026-07-25 recheck), InfinityStory future watch added | `skills/character-consistency.md` only | — | ✓ CLEAN CONTENT |
| 27035c2 | SC247 log: record study cycle 247 commit hash in pipeline.db | `data/pipeline.db` only | `data/` ✓ | ✓ CLEAN LOG |

**Protocol compliance this window (SC244–SC247):**
- Clean pairs: **SC244 = ✓, SC247 = ✓** (2/4 = 50% strict)
- ROOT DB errors: **SC245 = ❌ ROOT, SC246 = ❌ ROOT** — 2/4 cycles ROOT-broken
- ROOT-clean streak: **BROKEN** — was 4 consecutive clean windows (per July 24 audit); SC247 returns to clean but the window-level streak is still broken
- Bundling: all four cycles single-skill content — no bundling issues
- study_log: **1/4 new entries** — SC247 wrote id=41 (cycle=247) to data/pipeline.db; SC244/245/246 absent

**ROOT DB divergence state (after SC247 rebase):**
- `pipeline.db` (root, 61 440 B): 64 study_cycles rows, no study_log table; SC245/246 present here
- `data/pipeline.db` (155 648 B): 122 study_cycles rows (SC244 + SC247), 41 study_log rows
- SC245/246 exist ONLY in root DB; not in `data/pipeline.db`
- A production session with working directory at repository root queries the 64-row DB and misses SC244, SC247, and 57 other entries

---

## SC CONTENT NOTES

**SC244** — `skills/generation-video.md` (5a3cc19, Fri Jul 24 06:14:02) — +7/−3 lines:
- **v3 dropped legacy face parameters:** `faceStrength`, `subjectStrength`, `faceNo`, `imageReference`, `reference` from v1/v2 do NOT exist in v3. Do not copy v1/v2 API examples. Clear warning added with SC244 date stamp.
- **reference_strength / motion_strength are UI sliders, not raw API params:** Community tutorials cite "reference strength at 0.35/0.65/0.85" and "motion strength at 0.55" for Kling 3.0 — these are kling.ai web UI abstractions or third-party wrapper params (e.g., Flixly). Raw AIMLAPI uses `face_consistency: true` + `elements` + `cfg_scale` only.
- **Multi-shot minimum duration discrepancy documented:** Magnific API (v3 wrapper) confirms 3s minimum; fal.ai docs say 1s. AIMLAPI minimum unconfirmed — conservative 3s default maintained until canary.
- **Status dates updated:** Kling O3 and v3 Motion Control both "NOT on AIMLAPI as of July 24, 2026" — accurate negative recheck.
- Protocol: ✓ CLEAN PAIR (skill-only content + `data/` log).

**SC245** — `skills/captions-and-titles.md` (2370803, Fri Jul 24 12:07:11) — +13/−5 lines:
- **Remotion v4.0.498 documented (July 23, 2026):** SwiftShader fallback (v5.0 preview), `trimBefore` sequence freeze interaction fix. No changes to `@remotion/captions` API. `npm install remotion@4.0.498`.
- **Remotion v4.0.497 also documented:** Studio background color editing, direct premounting for image components, timeline asset-drop. No captions API changes.
- **API table header updated:** "Full API (v4.0.498 — confirmed current as of 2026-07-24; no caption API changes in 4.0.485–4.0.498)"
- **FFmpeg 8.1.2 confirmed:** Caption pipeline reference updated from 8.1.1 to 8.1.2 current stable — consistent with SC242/SC244 confirmations.
- **whisper.cpp 1.9.1 unchanged:** Confirmation date updated to July 24, 2026.
- Protocol: ✓ CLEAN CONTENT / ❌ ROOT LOG — content commit single-skill; log commit wrote to root `pipeline.db` instead of `data/pipeline.db`.

**SC246** — `skills/halal-audio.md` (4d14ab2, Fri Jul 24 18:07:37) — +8/−1 lines:
- **ElevenLabs SDK v2.59.0 (July 22, 2026):** Only HMAC-signed post-call webhook config added — zero changes to TTS, SFX, VoiceSettings, AllowedOutputFormats, or any audio pipeline parameters. Confirmed in §12 (Text to Dialogue) as well.
- **VoiceSettings speed note:** SDK version reference updated v2.58.0 → v2.59.0 (July 22, 2026).
- **5 PCM low-rate output_format entries added to SFX v2 table:** `pcm_8000`, `pcm_16000`, `pcm_22050`, `pcm_24000`, `pcm_32000` — all confirmed in AllowedOutputFormats SDK type (v2.59.0 verified). All marked telephony/streaming only — not suitable for production video mixing. Prevents accidental use of low-quality PCM formats.
- **FFmpeg n8.1.2 still current (July 24, 2026):** No n8.1.3 or n8.2 tag on GitHub. ffmpeg-normalize v1.41.1 unchanged.
- Protocol: ✓ CLEAN CONTENT / ❌ ROOT LOG — same ROOT DB error as SC245.

**SC247** — `skills/character-consistency.md` (519c566, Sat Jul 25 06:07:52) — +4/−2 lines:
- **Wan 2.7 R2V status upgraded: AIMLAPI blog-confirmed available.** AIMLAPI blog post (`aimlapi.com/blog/wan-2-7-video-next-generation-ai-video-generation-model`) explicitly confirms "The R2V mode is available via the AI/ML API platform." Status upgraded from "canary-test recommended" to **"AIMLAPI blog-confirmed — canary before production"**. docs.aimlapi.com still has no dedicated R2V page, but blog + inference.sh listing (`alibaba/wan-2-7-r2v`) are consistent. Canary: `reference_images` param, Karel `front.png`, 720p, strip audio. **The Wan 2.7 R2V canary is now unblocked by evidence — run at next opportunity.**
- **InfinityStory future watch added (Adobe Research / Meta AI / KAUST, arXiv 2603.03646):** Character-Aware Shot Transition module + Background-Consistent Generation Pipeline. Best VBench scores: Background Consistency 88.94, Subject Consistency 82.11. Confirms shot boundaries as highest identity-loss risk — validates our re-anchor-per-clip policy. Research only, no AIMLAPI endpoint.
- **Kling O3 not on AIMLAPI as of 2026-07-25 (pass 36 recheck):** Date-stamp updated; confirmed O3 on fal.ai/Atlas Cloud/Krea/Runware but not AIMLAPI. Farouq AIMLAPI-only directive stands.
- Protocol: ✓ CLEAN PAIR (skill-only content + `data/` log). study_log: **id=41 written** (cycle=247, 2026-07-25) — second write in 4 days after 10-cycle gap.

**study_log gap (cycle 235–241 + 244–246 = 10 absent cycles; SC247 wrote successfully):**
Current state: study_log has **41** rows; most recent is id=41, cycle=247 (2026-07-25). SC244/245/246 still absent. Root causes: (1) SC245/246 log commits targeted root DB which has no study_log table; (2) SC244 used correct data/ path but still no study_log entry — trigger gap independent of DB path. SC247 wrote successfully (same data/ path as SC244) — the trigger condition differs between SC244 and SC247, unclear why. Seven prior absent cycles (235–241) remain unaddressed. Total absent: 10 cycles.

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 3.1/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC244: v3 parameter trap identification | Documented that community tutorials cite UI wrapper params, not raw API params — prevents generation API errors. Multi-source discrepancy (Magnific 3s vs fal.ai 1s) handled conservatively with explicit canary recommendation | Strong positive |
| SC244: negative recheck accuracy | Kling O3 and v3 Motion Control date-stamped July 24 — disciplined "not yet" maintenance | Positive |
| SC245: version accuracy | Remotion 4.0.498 changelog entries (SwiftShader, trimBefore fix) documented correctly — not just version number | Positive |
| SC246: SDK scope accuracy | v2.59.0 correctly characterized as HMAC webhook-only, no audio impact — prevents false "major SDK change" alarm | Positive |
| **CLAUDE.md Pre-Gen Check #5 wrong (29th audit)** | "15-40 words" still wrong at point of generation | Critical negative |
| **ElevenLabs v1 retirement absent from CLAUDE.md (29th flag, 16 days overdue)** | Guaranteed 404 at next voiceover session | Critical negative |
| **LTXV Aug-15 — 21 days, 10th audit without CLAUDE.md alert** | Routing matrix at point of use still lists LTXV with no warning | Negative |
| **SC166 absent (24th audit)** | Differential prompt rule still not in model-prompting-guide.md Part 4 | Negative |
| ROOT DB error recurrence: SC245/246 | After 4-window clean streak, two consecutive log commits went to root DB — reasoning gap: why did the commit path revert? | Negative |

**Score: 3.1/5.0** (→ unchanged — SC244's API trap research is the strongest reasoning contribution; the ROOT DB recurrence adds a reasoning question that prevents improvement; CLAUDE.md non-propagation remains the structural floor)

---

### D2 — Execution Accuracy (20%) → 2.2/5.0 (↓ −0.3)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC244 content commit | skills/generation-video.md only — no DB | ✓ CLEAN |
| SC244 log commit | data/pipeline.db only (d9096c8) — correct path, separate commit | ✓ CLEAN LOG |
| SC244 = CLEAN PAIR | Third clean pair after SC241 and SC243 | ✓ Positive |
| **SC245 log commit (8e0d69e)** | Commit says "pipeline.db" — root path. `git show 8e0d69e --stat` confirms `pipeline.db | Bin 61440 -> 61440 bytes` (root, not `data/`). study_cycles cycle=245 absent from `data/pipeline.db` | ❌ ROOT DB ERROR |
| **SC246 log commit (650b262)** | Same: `pipeline.db | Bin 61440 -> 61440 bytes` (root). study_cycles cycle=246 absent from `data/pipeline.db` | ❌ ROOT DB ERROR |
| ROOT DB streak **BROKEN** | 4 consecutive clean windows achieved (per July 24 audit); this window: 2/3 ROOT errors | ❌ Critical regression |
| ROOT DB divergence | root `pipeline.db`: 64 rows; `data/pipeline.db`: 121 rows — a production session in the repo root misses 57 entries of pipeline intelligence | ❌ Structural risk |
| CLAUDE.md frozen | 29th consecutive audit — zero structural updates | ❌ Critical structural |

**Score: 2.3/5.0** (↓ −0.2 — SC244 and SC247 clean pairs are genuine positives; SC245 and SC246 ROOT DB errors break the 4-window streak; SC247's immediate return to correct `data/` path suggests an intermittent/session-specific failure rather than a full architectural regression; ROOT DB divergence for SC245/246 remains a production risk)

**Failure classification: OPERATIONAL** — SC244 and SC247 both used correct `data/` path; SC245 and SC246 reverted to root. The failure is operational (working directory or log script path inconsistency in SC245/246 sessions), not architectural.

---

### D3 — Memory & Continuity (15%) → 2.3/5.0 (↓ −0.2)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC244 cross-skill coherence | v3 parameters build on SC237/SC216 baseline — no contradictions introduced | Positive |
| SC245 version continuity | Caption skill version chain (4.0.495 → 4.0.496 → 4.0.497 → 4.0.498) maintained accurately | Positive |
| SC246 SDK version continuity | v2.58.0 → v2.59.0 correctly stepped; prior v2.58.0 content undisturbed | Positive |
| **study_log gap expanded: 7 → 10+ absent cycles** | SC244/245/246 all absent from study_log (id=40, cycle=242 still most recent). Root cause SC245/246: log commits targeted root DB which has no study_log table. SC244: log wrote to data/ but still no study_log entry — the study_log trigger gap persists | Critical negative |
| **study_cycles id=118: "FFmpeg 9.0" stale entry UNADDRESSED** | P0 from July 24 audit — study_cycles row for SC239/halal-audio still reads "FFmpeg 9.0 confirmed as current stable." Any session querying study_cycles for halal-audio intelligence will get incorrect FFmpeg version. 1-window since P0 raised, zero action | Critical negative |
| study_log: 0/3 new writes this window | Even SC244 (correct data/ path) did not write to study_log. Write trigger gap now confirmed as persistent structural issue, not random failure | Structural negative |

**Score: 2.4/5.0** (↓ −0.1 — skill content continuity is good; SC247 wrote study_log id=41 (partial recovery); study_log gap is 10 cycles (235-241, 244-246); study_cycles SC239 stale data unaddressed; SC245/246's root DB routing means their study_cycles entries exist only in root DB)

---

### D4 — Reliability & Consistency (20%) → 2.2/5.0 (↓ −0.4)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC244 = CLEAN PAIR | Content + correct data/ log = textbook clean | ✓ Positive |
| SC244 content: accurate negative rechecks | O3 and v3 Motion Control "NOT on AIMLAPI" maintained with fresh date stamps | ✓ Positive |
| **ROOT-clean streak BROKEN** | 4 consecutive windows (the only sustained positive in recent D4 history) → 0. Two ROOT errors in one window reverse the progress. The clean streak was the signal that the protocol had stabilized. | ❌ Critical regression |
| **CLAUDE.md frozen: 29th audit** | Zero structural updates — the consistent floor on all reliability-related scores | ❌ Critical |
| 92 days without approved creative output | Production reliability = 0 | Negative |
| study_log gap expanding | SC244 log wrote to correct path but still no study_log entry — write trigger gap now at 10+ cycles | Structural concern |
| No P0 action items from July 24 audit addressed | study_cycles id=118 backfill: not done. CLAUDE.md 3 fixes: not done. Canaries: not run | Negative |

**Score: 2.3/5.0** (↓ −0.3 — SC244 and SC247 clean pairs are genuine positives; SC245/246 ROOT errors break the 4-window streak; SC247's immediate correction suggests intermittent failure rather than full regression; CLAUDE.md frozen 29th audit and no P0 items addressed are the non-negotiable floor)

---

### D5 — Tool/Model Integration (15%) → 4.3/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC244: v3 API parameter traps | `faceStrength`/`subjectStrength`/`faceNo` documented as v3-absent; `reference_strength`/`motion_strength` documented as UI slider vs raw API distinction — directly prevents wrong API calls | Strong positive |
| SC244: multi-shot duration discrepancy | Flagged Magnific (3s) vs fal.ai (1s) discrepancy; AIMLAPI unconfirmed; conservative 3s default maintained with canary recommendation — correct calibration under uncertainty | Positive |
| SC245: Remotion 4.0.498 full changelog | Two new releases (4.0.497, 4.0.498) accurately documented with production-relevant details (SwiftShader, premounting, trimBefore fix) | Positive |
| SC246: ElevenLabs PCM completeness | 5 telephony PCM formats added to AllowedOutputFormats table with explicit "NOT for video mixing" guidance | Positive |
| SC246: v2.59.0 scope accuracy | Confirmed HMAC webhook-only change — prevents unnecessary audit of audio parameters | Positive |
| **SC247: Wan 2.7 R2V AIMLAPI blog-confirmed** | Blog post confirmation upgrades status from "canary-test recommended" to "AIMLAPI blog-confirmed available" — the R2V canary is now unblocked by evidence | Strong positive |
| SC247: InfinityStory future watch | Research paper finding validating per-clip re-anchoring policy + shot boundary as identity risk point | Positive |
| **CLAUDE.md routing matrix: LTXV active (21 days to Aug-15)** | At production generation time, routing matrix still has no deprecation warning | Critical negative |
| **CLAUDE.md Check #5 wrong prompt length (29th audit)** | Wrong guidance at point of generation | Critical negative |
| ROOT DB split: dual study_cycles | root (64 rows) vs data/ (121 rows) — a production session querying root DB gets stale/incomplete model landscape | Negative |
| Three canaries unrun (13/12/5 days outstanding) | Wan 2.2 Animate Replace (13 days), Kling Turbo Pro (13 days), Wan 2.7 R2V (5 days) | Negative |

**Score: 4.3/5.0** (→ unchanged — SC244's parameter traps and SC247's Wan 2.7 R2V blog-confirmation are the window's strongest contributions; CLAUDE.md divergence and ROOT DB split are persistent but D5 credit stays with skill content quality)

---

### D6 — Communication & Social (10%) → 3.7/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC244 commit body | 5-bullet body with ⚠️ warnings, explicit "do NOT copy v1/v2 API examples," multi-source discrepancy noted with date sources — high clarity | ✓ Strong |
| SC245 commit body | Concise and accurate: Remotion version, FFmpeg confirmation, whisper.cpp/WhisperX unchanged — no overclaiming | ✓ Solid |
| SC246 commit body | 5-bullet body with SDK version, HMAC-only scope, PCM format list with tier notes — complete | ✓ Solid |
| 3/3 commit bodies substantive | Consistent quality across the window | ✓ Positive |

**Score: 3.7/5.0** (→ unchanged — consistent commit body quality; SC244's ⚠️ framing on parameter traps is the standout; no communication regressions)

---

### D1–D6 Weighted Score

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|-------------|
| D1 Reasoning | 3.1 | 20% | 0.620 |
| D2 Execution | 2.3 | 20% | 0.460 |
| D3 Memory | 2.4 | 15% | 0.360 |
| D4 Reliability | 2.3 | 20% | 0.460 |
| D5 Integration | 4.3 | 15% | 0.645 |
| D6 Social | 3.7 | 10% | 0.370 |
| **Total** | — | 100% | **2.92 / 5.0** |

**Delta vs 2026-07-24: −0.11** — First regression after two consecutive windows of gains. SC245 and SC246 ROOT DB errors break the 4-window streak; SC247's immediate return to correct `data/` path + study_log write provides partial recovery. SC244 and SC247 both clean pairs. Skill content quality (D5) remains the pipeline's consistent strength.

**Failure classification:**
- OPERATIONAL: ROOT DB path recurrence (SC245/246) — SC244 used correct `data/` path; SC245/246 reverted to root. Working directory or log script path inconsistency.
- ARCHITECTURAL: study_log write trigger gap (10+ cycles absent; write mechanism confirmed alive SC243, but SC244 with correct data/ path also missed study_log — implies the trigger gap is independent of the DB path issue)
- DISCIPLINE: CLAUDE.md frozen (29th audit), ElevenLabs v1 not fixed (16 days overdue), LTXV Aug-15 not in CLAUDE.md (21 days), SC166 absent, 3 canaries unrun, study_cycles id=118 not backfilled
- MODEL CAPABILITY CEILING: none this window

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

**20 skills × 8 criteria = 160 total points maximum**

Skills assessed: anti-sycophancy, brand-identity, brief-intake, captions-and-titles, character-consistency, cinematic-standards, credit-efficiency, generation-image, generation-video, halal-audio, higgsfield-generation, kling-truck-prompting, model-ceiling-detection, model-prompting-guide, post-production, production-checklist, shariah-compliance, text-overlay-compositing, video-qa-rubric, viral-research.

**Previous: 142/160 = 88.8%**

### Changes this window (SC244–SC247)

**generation-video.md (SC244):**
- Accuracy: +1.0 (two critical parameter warnings added: v3 dropped legacy params; reference_strength/motion_strength are UI slider abstractions not raw API params — these prevent real API call errors)
- Coverage: +0.25 (multi-shot minimum duration discrepancy documented with sources and conservative default)
- Net: **+0.75 points** (meaningful accuracy improvement with direct production risk mitigation)

**captions-and-titles.md (SC245):**
- Accuracy: +0.5 (Remotion 4.0.498 documented correctly with two-release changelog; FFmpeg 8.1.2 reference updated from 8.1.1)
- Net: **+0.25 points** (incremental version accuracy; skill was already well-maintained)

**halal-audio.md (SC246):**
- Accuracy: +0.25 (SDK v2.59.0 scope correctly limited to HMAC webhook; speed param note updated)
- Coverage: +0.25 (5 PCM low-rate formats added to AllowedOutputFormats table with explicit telephony-only guidance)
- Net: **+0.25 points** (completion of PCM format table; scope accuracy prevents false alarm)

**character-consistency.md (SC247):**
- Accuracy: +0.5 (Wan 2.7 R2V status upgraded to blog-confirmed — the key routing decision for next character session; Kling O3 recheck date updated)
- Coverage: +0.25 (InfinityStory future watch adds validated research support for per-clip re-anchoring policy)
- Net: **+0.25 points** (meaningful R2V intelligence upgrade; InfinityStory adds research depth to existing policy)

**Total new points this window: applying as +1.25 net (conservative — persistent deductions unchanged)**

**Persistent deductions (unchanged from previous audit):**
- model-ceiling-detection.md: C8 wrong (Veo 3.1 Lite I2V in video escalation path — T2V only) — 24th audit, −1
- model-prompting-guide.md Part 4: SC166 differential prompt rule absent — 24th audit, −1
- CLAUDE.md meta-compliance: Pre-Gen Check #5 wrong, ElevenLabs v1 absent, LTXV matrix warning absent, Wan 2.7 R2V absent — continuing deductions (unchanged 7th consecutive)

**Score: 143.25/160 = 89.5%** (↑ +0.7% — generation-video.md SC244 parameter trap documentation and character-consistency.md SC247 Wan 2.7 R2V upgrade are the meaningful gains; structural deductions unchanged)

### CLAUDE.md Structural Audit

| Component | Status |
|-----------|--------|
| THREE-AGENT PATTERN | ✓ Present |
| PRE-GENERATION CHECKS (10 items) | ❌ Check #5 wrong ("15-40 words" → should be I2V 40-120 / T2V 80-150); Check #7 ElevenLabs v1 IDs absent (retired July 9, **16 days overdue**, guaranteed 404) |
| PRODUCTION GATES (10 items) | ✓ Present and accurate |
| MODEL ROUTING MATRIX | ❌ LTXV row missing deprecation warning (**21 days to Aug-15**); Wan 2.2 Animate Replace absent; Wan 2.7 R2V absent; Turbo Pro confidence status not reflected |
| BRAND BINARY CHECKLIST | ✓ Present |
| BANNED WORDS IN MOTION PROMPTS | ✓ Present |
| SHARI'AH COMPLIANCE | ✓ Present |
| ANTI-SYCOPHANCY | ✓ Present |
| FAMILY LOCK-IN | ✓ Present |
| SNORKEL TRIAGE | ✓ Present |

**CLAUDE.md structural score: 7/10 components fully correct** (3 components with active errors/omissions — unchanged for 7 consecutive audits; same 3 components)

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved video:** V3-Tarik-v2-couple (2026-04-26) — **92 days ago.** No new creative output this window.

**Family lock status:** `testimonial` family, 3/6 videos approved. 3 more required before family unlock (lock_until: 6).

**Cost metric:** Credits per approved video = MATHEMATICALLY UNDEFINED (zero new output, day 92).

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

### New Production Intelligence (SC244–SC246)

**Kling v3 Pro generation (SC244):**
- **CRITICAL parameter trap:** Do NOT use `faceStrength`, `subjectStrength`, `faceNo`, `imageReference`, `reference` in v3 calls — these are v1/v2 params, silently ignored or error in v3. Character consistency in v3 = `face_consistency: true` + `elements` only.
- **UI slider trap:** "reference_strength 0.35/0.65/0.85" and "motion_strength 0.55" in tutorials are kling.ai UI sliders or wrapper params. Do NOT copy to AIMLAPI JSON.
- **Multi-shot safe default:** 3s per shot until AIMLAPI minimum is confirmed (Magnific says 3s, fal.ai says 1s — AIMLAPI unconfirmed).

**Caption pipeline (SC245):**
- Remotion 4.0.498: SwiftShader fallback and trimBefore freeze fix. No caption API changes. Use `npm install remotion@4.0.498`.
- `@remotion/captions` API unchanged since 4.0.485.

**Halal audio (SC246):**
- ElevenLabs SDK v2.59.0: HMAC webhook only — all TTS/SFX/VoiceSettings unchanged.
- PCM table now complete (pcm_8000/16000/22050/24000/32000 marked telephony-only).
- FFmpeg n8.1.2 still current stable (triple-confirmed: SC242/245/246).

**Character consistency (SC247):**
- **Wan 2.7 R2V NOW CONFIRMED: AIMLAPI blog-confirmed available.** Call `alibaba/wan-2-7-r2v`, `reference_images` param, Karel `front.png`, 720p, strip audio post. InsightFace gate ≥ 0.62.
- O3 not on AIMLAPI as of July 25, 2026 — continue with Kling O1 for character shots.
- InfinityStory confirms: shot boundaries are highest identity-loss risk → re-anchor every clip from original reference photos (not from prior clip's last frame).

### Ralph Loop

*"What would a senior creative director still reject?"*

1. **ROOT pipeline.db split is now a production risk.** The root `pipeline.db` (64 rows) diverges from `data/pipeline.db` (122 rows). Any pre-production intelligence check from the repo root queries half the pipeline's accumulated knowledge. SC244 (Kling v3 API traps) and SC247 (Wan 2.7 R2V blog-confirmation) exist only in `data/`; SC245/246 exist only in root. A production session relying on study_cycles pre-brief could get contradictory information depending on working directory. A senior creative director would call this a single point of failure in the pipeline's memory system.

2. **LTXV expiry is 21 days away with no action plan.** CLAUDE.md routing matrix still lists LTXV for B-roll I2V with no deprecation warning. The replacement (`minimax/hailuo-2.3-fast`) was identified in SC234, documented in credit-efficiency.md, and has been in the audit's P0 list for 10 consecutive audits. No canary has been run. At the current rate (zero canaries per day), the LTXV route will fail in production with no validated replacement.

3. **Three canaries outstanding — Wan 2.7 R2V is now AIMLAPI blog-confirmed.** Wan 2.7 R2V (SC247 today: blog-confirmed available on AIMLAPI — the blocker "not confirmed" is resolved), Wan 2.2 Animate Replace ($0.06/gen, 13+ days), Kling Turbo Pro (13+ days). There is no longer any "not confirmed available" excuse for the Wan 2.7 R2V canary. The Animate Replace canary costs less than a cup of coffee. Running zero canaries while accumulating 4+ cycles of intelligence about them is research without production benefit.

4. **study_log gap is now 10 cycles.** SC235–241 (7 cycles) + SC244 (1 cycle, log wrote to correct data/ path but no study_log entry) + SC245 (root DB, no study_log table) + SC246 (root DB, no study_log table) = 10 absent cycles in study_log. A pre-production brief via study_log misses: fal.ai elements cap (SC237), camera_control 6-type API confirmation (SC237), Kling Turbo Pro HIGH quality confirmation (SC237), PySceneDetect v0.7.1 stable (SC235/242), Wan 2.7 R2V canary recommendation (SC240), LTXV 21-day warning (SC241), Kling v3 API traps (SC244), Remotion 4.0.498 (SC245), SDK v2.59.0 scope (SC246).

**Overall Creative: (3.9 + 4.2 + 4.1) / 3 = 4.07 / 5.0** (→ unchanged, day 92 of production stagnation)

CREATIVE_AUDIT_COMPLETE

---

## ACTION ITEMS

### [P0 — CRITICAL — NEW THIS AUDIT — ROOT DB SPLIT]

**1. Fix ROOT DB split (IMMEDIATE):**

`data/pipeline.db` is the authoritative DB. SC245 and SC246 log commits wrote to root `pipeline.db` instead. Two actions required:

**1a. Add SC245 and SC246 entries to `data/pipeline.db`:**
```python
# SC245
INSERT INTO study_cycles (cycle, topic, date, summary, git_commit)
VALUES (245, 'Caption pipeline',  '2026-07-24',
  'Remotion 4.0.498 (2x new releases, no caption API changes); FFmpeg 8.1.2; whisper.cpp 1.9.1 and WhisperX 3.8.6 unchanged',
  '2370803');
# SC246
INSERT INTO study_cycles (cycle, topic, date, summary, git_commit)
VALUES (246, 'Halal audio', '2026-07-24',
  'SDK v2.59.0: HMAC webhook only, zero audio API changes. VoiceSettings speed confirmed v2.59.0. Added pcm_8000/16000/22050/24000/32000 to AllowedOutputFormats table (telephony-only). FFmpeg n8.1.2 still current. Commit: 4d14ab26.',
  '4d14ab2');
```

**1b. Fix log script path:** The script writing study_cycles log entries must target `data/pipeline.db` not `pipeline.db`. Verify with `grep -r "pipeline.db" scripts/` — the path reference that SC245 and SC246 used must be corrected to `data/pipeline.db`. SC244 used the correct path (d9096c8 shows `data/pipeline.db`) — compare SC244's script invocation vs SC245's.

---

### [P0 — CRITICAL — 29th audit — CLAUDE.md: 3 fixes needed in one edit session]

**2. Fix Pre-Gen Check #5: prompt length**
```
Current:  Motion prompt: 15-40 words, motion ONLY, defined endpoint ("eases to stop")
Correct:  Motion prompt: I2V 40-120 words / T2V 80-150 words (Kling v3, July 2026).
          Motion ONLY — action arc + camera move + defined endpoint. (15-40w was Kling v1/v2.)
```

**3. Fix Pre-Gen Check #7: ElevenLabs v1 retirement (16 DAYS OVERDUE)**
```
⚠️ RETIRED JULY 9, 2026: eleven_monolingual_v1 / eleven_multilingual_v1 / scribe_v1 → 404 NOW.
Use: eleven_v3 (TTS production) / eleven_flash_v2_5 (TTS draft) / scribe_v2 (captions).
NOTE: language_code NOT supported on eleven_multilingual_v2 (silently ignored, June 29, 2026).
grep -r "monolingual_v1\|scribe_v1" scripts/ before voiceover work.
```

**4. Routing matrix: LTXV alert + Wan 2.2 Animate Replace + Turbo Pro + Wan 2.7 R2V**
```
⚠️ LTXV DEADLINE Aug 15 (21 days): ltxv/ltxv-2-fast WILL ERROR after Aug 15.
  → Use minimax/hailuo-2.3-fast ($0.0416/sec) for non-char I2V.

Add row: Character animation canary | Wan 2.2 Animate Replace | $0.06/gen
  (alibaba/wan2.2-14b-animate-replace; video_url + image_url + resolution: "720p")

Add row: Character animation canary | Wan 2.7 R2V | TBD
  (alibaba/wan-2-7-r2v; reference_images + 720p + generate_audio: false; InsightFace ≥ 0.62)

Update: Kling Turbo Pro character consistency: HIGH confidence (multi-source July 2026).
  Canary required for AIMLAPI cost/audio only — run 3s reference before locking finals.
```

---

### [P0 — DATA INTEGRITY — study_cycles id=118 stale FFmpeg version (2nd consecutive audit)]

**5. Backfill study_cycles id=118 summary (SC239 / halal-audio):**
```
study_cycles row: id=118, cycle=239, topic='Halal audio (pass 36)', date='2026-07-22'
Current: "FFmpeg 9.0 confirmed as current stable (July 2026)" — FALSE
Correct: "FFmpeg 8.1.2 (n8.1.2, June 17 2026) is current stable — no n9.x release exists.
          SC239 error. Corrected in SC242 (halal-audio.md). DB summary not updated at correction time."
```

---

### [P0 — BEFORE NEXT PRODUCTION SESSION — 3 canaries outstanding]

**6. Wan 2.7 R2V canary (SC247: AIMLAPI BLOG-CONFIRMED, 5 days outstanding):**
- AIMLAPI blog post: "The R2V mode is available via the AI/ML API platform" — confirmed today (SC247)
- Call `alibaba/wan-2-7-r2v` with Karel `front.png` in `reference_images` + 720p + strip audio post
- If `model-not-found` → fall back to `wan-2.6-reference-to-video`; update status to "blog says available but endpoint not live"
- If output received: InsightFace ≥ 0.62 gate + brand binary + owner review; update CLAUDE.md routing matrix

**7. Wan 2.2 Animate Replace canary (SC234, 13+ days outstanding):**
- Step 1: NBP Edit hero frame as `image_url` + 5s drive video as `video_url`, mode: Move, $0.06
- Step 2: Verify quality + confirm billing in credit log
- If Move passes: Replace mode with B-roll + hero frame reference

**8. Kling Turbo Pro canary (SC237, 13+ days outstanding):**
- `klingai/video-v3-turbo-pro` + `generate_audio: false` + 3s reference clip + confirm billing
- Quality confidence: HIGH (multi-source). Only AIMLAPI cost/audio unknown.

---

### [P0 — DATA INTEGRITY — study_log gap investigation (7 → 10 cycles)]

**9. Investigate study_log gaps SC235–241 + SC244–246:**
- study_log trigger fires independently of DB path — SC244 used correct `data/` path but still no study_log entry
- SC245/246: root DB has no study_log table → root DB commits cannot write study_log
- Backfill: write study_log entries for SC235–241 from study_cycles summaries; verify SC244 trigger conditions

---

### [P0 — BEFORE NEXT B-ROLL SESSION — LTXV deadline approaching]

**10. Verify `minimax/hailuo-2.3-fast` endpoint on AIMLAPI before Aug-15:**
- Run a canary: 5s scenery clip (no character), 9:16, `generate_audio: false`
- Confirm `$0.0416/sec` billing vs LTXV's `$0.052/sec`
- Update CLAUDE.md routing matrix once confirmed

---

### [P0 — OPERATIONAL — model-ceiling-detection.md C8 — 24th consecutive audit]

**11. Remove Veo 3.1 Lite I2V from video escalation path** — Veo 3.1 Lite is T2V only (one-line removal)

---

### [P0 — BEFORE NEXT CHARACTER SESSION — SC166 — 24th audit]

**12. model-prompting-guide.md Part 4 — add SC166 differential prompt rule:**
```
On facial-movement retries: use action-only prompts; strip identity-descriptive words.
(Validated by Stand-In (arXiv 2508.07901) + WildActor (arXiv 2603.00586) — both confirm
character attributes in text compete with identity flow. Text = action+camera ONLY.)
```

---

## TELEGRAM REPORT STATUS

No TELEGRAM_BOT_TOKEN found in environment or .env files. Telegram report NOT sent.

Report text (for manual resend if needed):
```
📊 Daily Audit 2026-07-25 — Snelverhuizen Pipeline

Operator: 2.92/5.0 (↓ -0.11) — SC245/246 ROOT DB broke 4-win streak
Skills:   89.5% (+0.7%) — SC244 v3 traps + SC247 Wan R2V confirmed
Creative: 4.07/5.0 (→) — day 92, no new output

🆕 SC247: Wan 2.7 R2V AIMLAPI blog-confirmed available — run canary NOW
⚠️ SC245+246 log commits wrote to ROOT pipeline.db (not data/):
  data/ (122 rows) vs root (64 rows) — SC245/246 missing from authoritative DB
  Fix: insert SC245/246 into data/pipeline.db; fix log script path
⚠️ LTXV Aug-15: 21 days. No CLAUDE.md alert. No replacement canary yet.

TOP 3 ACTION ITEMS:
1. Fix ROOT DB split: insert SC245/246 into data/pipeline.db + fix log path
2. Wan 2.7 R2V canary: alibaba/wan-2-7-r2v (blog-confirmed — no more waiting)
3. CLAUDE.md: ElevenLabs v1 (16d overdue, 404 now) + LTXV Aug-15 (21 days)
```

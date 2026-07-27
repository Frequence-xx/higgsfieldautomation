# Daily Audit — 2026-07-27

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-07-26 | Operator 2.86/5.0 · Skills 90.3% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-07-26 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **3.05 / 5.0** | ↑ +0.19 | ↓ −0.80 |
| Skill Library & Policy | **91.4%** (146.25/160) | ↑ +1.1% | ↓ −0.1% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Four study cycles (SC251–SC254) since the 2026-07-26 audit.** Operator score recovers to 3.05/5.0 (+0.19). Primary driver: first four-pair clean window since the mid-July ROOT DB regression streak — SC251, SC252, SC253, and SC254 all went to `data/pipeline.db`. This is the cleanest execution window in at least 10 cycles. DB inspection confirms all four are correctly in `data/pipeline.db`: cycle 251 (Kling v3 Pro), 252 (Caption pipeline), 253 (Halal audio), 254 (Character consistency).

**Skills score climbs to 91.4% (+1.1%)** — strongest window since the current regression began. SC253's halal-audio.md logprob addition is the quality standout: catching silent brand-name garbling via `logprob < -2.0` is a genuine production gate upgrade. SC251's shot_type parameter documentation fills a real multi-shot gap. SC252 propagates Remotion v4.0.499 to captions-and-titles.md within 2 days.

**One naming inconsistency this window:** SC253+1 content commit (19b7b98) is titled "Study cycle 253+1" while the paired log commit (6f351e1) says "SC254 log". DB is internally consistent (cycle 254 in study_cycles), so data integrity is preserved — the inconsistency is in the git commit message only.

**Persistent structural blockers unchanged:** CLAUDE.md frozen for the 31st consecutive audit. ElevenLabs v1 model IDs now 18 days past retirement. LTXV Aug-15 deadline is **19 days away** — not in CLAUDE.md routing matrix. SC245/246/249 still missing from `data/pipeline.db` (3rd audit unaddressed). Day 94 without approved creative output. Three canaries outstanding (Wan 2.7 R2V: 7 days, Wan 2.2 Animate Replace: 15 days, Kling Turbo Pro: 15 days).

---

## CHANGES SINCE 2026-07-26 AUDIT

Git commits since `29c470d` (July 26 audit):

| Hash | Commit | Files changed | DB path | Protocol |
|------|--------|---------------|---------|----------|
| 4961e3f | SC251: Kling v3 Pro parameters (pass 33) — shot_type parameter, per-shot 512-char limit, O3/Motion Control recheck Jul 26 (both absent) | `skills/generation-video.md` only | — | ✓ CLEAN CONTENT |
| bedf0f9 | SC251 log: record study cycle 251 commit hash in pipeline.db | `data/pipeline.db` only | `data/` ✓ | ✓ CLEAN LOG |
| e2b848b | SC252: Caption pipeline (pass 38) — Remotion v4.0.499 added; whisper.cpp v1.9.1, WhisperX v3.8.6, ElevenLabs SDK v2.59.0 confirmed current | `skills/captions-and-titles.md` only | — | ✓ CLEAN CONTENT |
| 2845208 | SC252 log: record study cycle 252 commit hash in pipeline.db | `data/pipeline.db` only | `data/` ✓ | ✓ CLEAN LOG |
| fec24de | SC253: Halal audio (pass 38) — Scribe v2 logprob + character granularity documented; SDK v2.59.0 + ffmpeg-normalize v1.41.1 confirmed | `skills/halal-audio.md` only | — | ✓ CLEAN CONTENT |
| e6a230d | SC253 log: record study cycle 253 commit hash in pipeline.db | `data/pipeline.db` only (155648→159744 B) | `data/` ✓ | ✓ CLEAN LOG |
| 19b7b98 | SC253+1: Character consistency (pass 38) — Kling O3 absent (07-27 recheck); Wan 2.7 R2V downgraded to blog-confirmed/docs-absent; FaceFusion v3.7.1 current; Show and Polish IP-FVR added | `skills/character-consistency.md` only | — | ✓ CLEAN CONTENT |
| 6f351e1 | SC254 log: record study cycle 254 commit hash in pipeline.db | `data/pipeline.db` only (159744→159744 B) | `data/` ✓ | ✓ CLEAN LOG ⚠️ NAMING |

**Protocol compliance this window (SC251–SC254):**
- Clean pairs: **ALL 4 = ✓** — first four-pair clean window since the ROOT DB regression began (SC245, SC246, SC249 all went to root in prior windows)
- ROOT DB errors: ZERO this window
- Bundled commits: ZERO this window
- Naming inconsistency: SC253+1 content (19b7b98) vs SC254 log (6f351e1) — git commit message mismatch. DB cycle=254 is internally consistent; only the commit subject line diverges.
- SC252 log DB size unchanged (155648→155648 B): suspicious, but `data/pipeline.db` query confirms cycle=252 IS in the DB — SQLite's write-ahead log or page reuse produced same file size.

**ROOT DB divergence state (after SC254):**
- `data/pipeline.db` (159744 B): cycles 247, 248, 250, 251, 252, 253, 254 present. Still missing: **245, 246, 249** (3rd consecutive audit unaddressed)
- `pipeline.db` (root, 61440 B): stale copy; has cycle 249 only from the ROOT errors; out of sync

---

## SC CONTENT NOTES

**SC251** — `skills/generation-video.md` (4961e3f, Sun Jul 26 06:13:30) — +18/−5 lines:
- **`shot_type` parameter added to multi-shot section (CANARY on AIMLAPI).** Native Kling v3 API requires `shot_type` alongside `multi_shot: true`. Two values: `"customize"` (uses `multi_prompt` array — our current approach) and `"intelligence"` (AI auto-segments a single `prompt` string into shots). Native API uses camelCase `shotType`; AIMLAPI likely uses `shot_type` (consistent with snake_case convention). CANARY required: add `"shot_type": "customize"` to an existing multi_prompt call.
- **Per-shot prompt character limit: 512 chars** (native Kling API docs; keep ≤400 on AIMLAPI for safety). Main `prompt` field stays 2500 chars for intelligence mode.
- **`intelligence` mode use-case boundary:** Do NOT use when character element binding (@Element1) is needed per shot — use `"customize"` + `multi_prompt` for that.
- **`index` field clarification:** `index` in multi_prompt entries is a native API requirement; AIMLAPI wrapper handles automatically.
- O3 and v3 Motion Control recheck dates updated Jul 24→Jul 26: both still absent from AIMLAPI.
- Protocol: ✓ CLEAN PAIR

**SC252** — `skills/captions-and-titles.md` (e2b848b, Sun Jul 26 12:08:40) — +7/−3 lines:
- **Remotion v4.0.499 propagated from SC249 post-production update** — opacity leak fix now in captions skill (2 days after SC249 first documented it). Correct cross-skill propagation.
- **whisper.cpp v1.9.1 confirmed current** (CI build fixes only — no DTW/timestamp changes from v1.8.5+).
- **WhisperX v3.8.6 confirmed current** (v3.8.7rc1 is pre-release Windows fix; stay on stable 3.8.6).
- **ElevenLabs SDK v2.59.0 confirmed current** (no new release since July 22).
- Protocol: ✓ CLEAN PAIR (DB size unchanged but cycle=252 confirmed in data/pipeline.db)

**SC253** — `skills/halal-audio.md` (fec24de, Sun Jul 26 18:10:52) — +14/−2 lines:
- **`logprob` field documented for brand name QA.** `logprob` is the log probability of each transcribed word; `logprob < -2.0` flags low confidence. Production code example added. Specifically targets SNELVERHUIZEN and 085 3331133 as highest-risk words. This closes a silent failure mode: a garbled brand name can look plausible in the transcript but be phonetically wrong.
- **`timestamps_granularity="character"` confirmed in SDK v2.59.0.** Correctly scoped to "karaoke-style animation only" — standard pipeline uses `"word"`. Each word object gains a `characters` array when this is set. No change to current workflow required.
- **`characters` field in word response documented** (populated only when `timestamps_granularity="character"`).
- **Logprob check added to §11 QA checklist and Known Issues table.**
- **SDK v2.59.0 and ffmpeg-normalize v1.41.1 confirmed current** (no changes).
- Protocol: ✓ CLEAN PAIR (DB grew 155648→159744 B, consistent with study_cycles row insertion)

**SC253+1 / SC254** — `skills/character-consistency.md` (19b7b98, Mon Jul 27 00:11:28) — +5/−3 lines:
- **Kling O3 recheck: still absent from AIMLAPI as of 2026-07-27.** No AIMLAPI endpoint found. Confirmed on fal.ai, Atlas Cloud, Krea, Runware — but per Farouq directive, AIMLAPI-only. Recheck date updated.
- **Wan 2.7 R2V status DOWNGRADED: "AIMLAPI blog-confirmed available but docs-absent — canary mandatory."** Previous SC247 said "blog-confirmed available." SC253+1 correctly notes that the AIMLAPI docs page for R2V is still absent and search results describe it as "Coming Soon." Anti-sycophantic correction: does not inflate the status based on the blog post alone.
- **FaceFusion v3.7.1 confirmed current** (July 5, 2026; 2-processor bug fix confirmed relevant to our pipeline — `face_swapper + face_enhancer` combos were broken on still-image inputs in v3.7.0).
- **Show and Polish (arXiv 2507.10293, MM 2025) added as IP-FVR future watch.** Reference-Guided Identity Preservation in Face Video Restoration. Practical implication: complements FaceFusion by restoring quality in degraded clips while anchoring identity to the reference. Flagged as CodeFormer replacement candidate for olive/brown-skin characters (CodeFormer can whiten skin; IP-FVR preserves reference appearance more faithfully). No confirmed public code — monitor for release.
- Naming inconsistency: content commit titled "253+1" but log commit (6f351e1) titled "SC254". DB is consistent (cycle=254). Only the git message diverges.
- Protocol: ✓ CLEAN PAIR (naming inconsistency in commit message only)

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 3.1/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC251: shot_type "customize" vs "intelligence" boundary | Correctly identifies that `intelligence` mode is incompatible with character element binding (@Element1) per shot — actionable use-case separation | Strong positive |
| SC251: AIMLAPI canary guidance | "CANARY REQUIRED: try adding `shot_type: "customize"` to an existing multi_prompt call" — specific test protocol, not just a flag | Positive |
| SC253: logprob < -2.0 threshold for brand QA | Non-obvious production improvement — silent garbling of brand names is the exact failure mode that causes owner rejects. Correct threshold with code example | Strong positive |
| SC253: timestamps_granularity scoping | "word" for standard use, "character" only for karaoke — prevents unnecessary complexity creep | Positive |
| SC253+1: Wan 2.7 R2V status downgrade | Correctly refuses to promote from "blog-confirmed" to "live" without docs or a canary test — anti-sycophantic | Strong positive |
| SC253+1: Show and Polish scoping | "No confirmed public code — monitor for release" — appropriate future-watch classification | Positive |
| **CLAUDE.md Pre-Gen Check #5 wrong (31st audit)** | "15-40 words" still wrong at point of generation | Critical negative |
| **ElevenLabs v1 retirement absent from CLAUDE.md (18 days overdue)** | halal-audio.md has it; CLAUDE.md does not — propagation gap persists | Critical negative |
| **LTXV Aug-15 — 19 days, 12th audit without CLAUDE.md alert** | credit-efficiency.md has the warning; routing matrix (point of generation) does not | Critical negative |
| **SC253+1 naming inconsistency** | Content commit says "253+1", log says "254" — ambiguous cycle numbering in git history (DB is correct) | Minor negative |
| **SC166 absent (26th audit)** | Differential prompt rule still not in model-prompting-guide.md Part 4 (though character-consistency.md Step 3a has the equivalent) | Negative |

**Score: 3.1/5.0** (→ unchanged — SC253's logprob gate and SC253+1's Wan 2.7 R2V downgrade are the reasoning window highlights; CLAUDE.md non-propagation and LTXV inaction remain the floor)

---

### D2 — Execution Accuracy (20%) → 2.8/5.0 (↑ +0.6)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC251 = CLEAN PAIR | generation-video.md + data/pipeline.db log — textbook clean | ✓ |
| SC252 = CLEAN PAIR | captions-and-titles.md + data/pipeline.db log (size unchanged but cycle=252 confirmed in DB) | ✓ |
| SC253 = CLEAN PAIR | halal-audio.md + data/pipeline.db log (DB grew 155648→159744 B — row added) | ✓ |
| SC254 = CLEAN PAIR | character-consistency.md + data/pipeline.db log | ✓ |
| **Four-pair clean window** | Zero ROOT DB errors, zero bundled commits — best execution window since SC244 (July 24 clean pair) | ✓ Strong positive |
| SC253+1 naming mismatch | Content "253+1" vs log "SC254" — data integrity preserved, git message inconsistent | ⚠️ Minor |
| **P0 actions from July 26 audit** | ROOT DB fix (SC245/246/249 inserts into data/): NOT done. CLAUDE.md 3 fixes: NOT done. SC166: NOT done. model-ceiling-detection C8: NOT done. Canaries (3): NOT run. study_cycles id=118 fix: NOT done | ❌ Critical |
| **CLAUDE.md frozen** | 31st consecutive audit — zero structural updates | ❌ Critical structural |

**Score: 2.8/5.0** (↑ +0.6 — four-pair clean window is the first in this regression period; naming inconsistency and zero P0 actions cap the ceiling. Previous 2.2 reflected SC249 ROOT error; this window's clean record merits meaningful recovery.)

**Failure classification:**
- OPERATIONAL: SC253+1 naming inconsistency — session named the commit "253+1" instead of "254"; DB cycle number (254) is correct, only the git commit subject diverges. The log script wrote to correct path — execution correct, commit message discipline slightly off.
- ARCHITECTURAL: study_log gaps — trigger fires inconsistently across sessions (independent of DB path choice). 43 study_log rows vs ~30+ study_cycles rows suggests partial coverage.
- DISCIPLINE: CLAUDE.md frozen (31st audit), ElevenLabs v1 absent from CLAUDE.md (18 days overdue), LTXV Aug-15 not in routing matrix (19 days), SC166 absent, 3 canaries unrun, SC245/246/249 not backfilled, study_cycles id=118 stale — all P0 items from July 26 audit unaddressed for second consecutive audit
- MODEL CAPABILITY CEILING: none this window

OPERATOR_AUDIT_COMPLETE

---

### D3 — Memory & Continuity (15%) → 2.4/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC252: cross-skill Remotion v4.0.499 propagation | SC249 (post-production, Jul 25) documented opacity fix → SC252 (captions, Jul 26) added it 2 days later — correct inter-skill memory | Strong positive |
| SC253+1: Wan 2.7 R2V downgrade tracks SC247 | SC247 said "blog-confirmed available"; SC253+1 rechecks Jul 27 and correctly downgrades to "blog-confirmed/docs-absent" — active status tracking | Positive |
| SC253+1: FaceFusion v3.7.1 recheck | "confirmed current pass 38, 2026-07-27" — version tracking maintained | Positive |
| **SC245/246/249 still missing from data/pipeline.db** | 3rd consecutive audit: SC245 (Caption pipeline, Jul 24), SC246 (Halal audio, Jul 24), SC249 (Post-production, Jul 25) absent. Study queries miss these cycles | Critical negative (P0 unaddressed) |
| **study_log: 43 rows, gaps likely** | SC253 log likely wrote study_log (DB grew). SC254 log size unchanged — study_log entry for SC254 uncertain | Minor negative |
| **study_cycles id=118 stale FFmpeg data (4th consecutive audit)** | id=118 still reports "FFmpeg 9.0 confirmed" — demonstrably false (8.1.2 is current since SC239 correction) | Critical negative (P0 unaddressed) |

**Score: 2.4/5.0** (↑ +0.1 — SC252's Remotion propagation and SC253+1's status downgrade are genuine memory positives; SC245/246/249 gap and stale id=118 persist for 3+ audits)

---

### D4 — Reliability & Consistency (20%) → 2.4/5.0 (↑ +0.2)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC251–SC254 all CLEAN PAIRS | Zero ROOT DB errors in this window; first clean four-pair streak since the ROOT regressions began | ✓ Strong positive |
| SC253+1 Wan 2.7 R2V not over-promoted | Status downgraded, not inflated — consistent with evidence | ✓ Positive |
| **CLAUDE.md frozen: 31st consecutive audit** | Zero structural updates — ceiling on all reliability-related improvements | ❌ Critical |
| **Zero P0 items addressed from July 26 audit** | All action items outstanding: 3 CLAUDE.md fixes, 3 canaries, 3 DB inserts, SC166, id=118, model-ceiling-detection C8 | ❌ Critical |
| **LTXV countdown: 19 days to Aug-15** | Routing matrix in CLAUDE.md still has LTXV as active B-roll I2V route with no warning. A production session following CLAUDE.md would still route to LTXV and 404 on Aug 16 | ❌ Critical (escalating) |
| **Day 94: no approved creative output** | Production reliability = 0 for 94 consecutive days | Negative |
| **Canaries: 3 outstanding** | Wan 2.7 R2V (7 days), Wan 2.2 Animate Replace (15 days), Kling Turbo Pro (15 days) | Negative |

**Score: 2.4/5.0** (↑ +0.2 — clean execution streak is meaningful; LTXV now 19 days from production failure, day 94 stagnation, and zero P0 action prevent higher score)

---

### D5 — Tool/Model Integration (15%) → 4.3/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC251: shot_type AIMLAPI canary guidance | "CANARY on AIMLAPI — add and test; may be implicit when multi_prompt is present" — prevents premature assumption of parameter compatibility | Strong positive |
| SC251: per-shot 512-char limit with AIMLAPI safety margin | "keep ≤400 chars for safety on AIMLAPI" — practical production constraint applied correctly | Positive |
| SC253: logprob threshold with code example | Code pattern ready for drop-in use in production scripts; brand-specific guidance (SNELVERHUIZEN and phone number flagged explicitly) | Strong positive |
| SC253: timestamps_granularity confirmed from SDK v2.59.0 | API accuracy via SDK source inspection (not just docs) | Positive |
| SC253+1: FaceFusion v3.7.1 2-processor bug documented | "v4.0.499 upgrade before next Remotion session" equivalent — concrete pre-session action | Positive |
| SC253+1: Show and Polish CodeFormer comparison | Correctly identifies why IP-FVR could be superior for olive/brown skin (CodeFormer whitening vs reference preservation) — useful production context | Positive |
| **CLAUDE.md routing matrix: LTXV active (19 days to Aug-15)** | credit-efficiency.md has the warning; CLAUDE.md (point of generation) does not | Critical negative |
| **CLAUDE.md Check #5 wrong prompt length (31st audit)** | Wrong guidance at point of generation | Critical negative |
| **Three canaries unrun (15/15/7 days)** | Wan 2.2 Animate Replace, Kling Turbo Pro, Wan 2.7 R2V — intelligence accumulated; not validated | Negative |
| **model-ceiling-detection.md C8: Veo 3.1 Lite in I2V path (26th audit)** | One-line removal unaddressed | Negative |

**Score: 4.3/5.0** (→ unchanged — SC253's logprob gate and SC251's shot_type canary guidance are the window's strongest contributions; CLAUDE.md divergence and canary backlog persist)

---

### D6 — Communication & Social (10%) → 3.8/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC253 commit body | 7-bullet breakdown: specific changes (logprob, character granularity, characters field, QA checklist, Known Issues), SDK recheck, ffmpeg-normalize confirm, unchanged tools listed | ✓ Outstanding |
| SC253+1 commit body | Explicitly annotates "Wan 2.7 R2V AIMLAPI status downgraded" — acknowledges status correction, not just a recheck | ✓ Strong |
| SC251 commit body | Multi-bullet: shot_type, per-shot limit, index field, O3/Motion Control recheck — complete and actionable | ✓ Solid |
| SC252 commit body | Terse but accurate ("Remotion v4.0.499 added (July 24, no captions API changes)") — all confirmed current tools listed | ✓ Solid |
| **SC253+1 naming mismatch** | "Study cycle 253+1" in content commit vs "SC254 log" in log commit — creates ambiguity in git log history | ⚠️ Minor |

**Score: 3.8/5.0** (↑ +0.1 — SC253's 7-bullet commit body is the window's standout; SC253+1's naming mismatch is the only deduction)

---

### D1–D6 Weighted Score

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|-------------|
| D1 Reasoning | 3.1 | 20% | 0.620 |
| D2 Execution | 2.8 | 20% | 0.560 |
| D3 Memory | 2.4 | 15% | 0.360 |
| D4 Reliability | 2.4 | 20% | 0.480 |
| D5 Integration | 4.3 | 15% | 0.645 |
| D6 Social | 3.8 | 10% | 0.380 |
| **Total** | — | 100% | **3.05 / 5.0** |

**Delta vs 2026-07-26: +0.19** — Recovery driven by clean execution (D2: +0.6) and modest improvements across D3/D4/D6. The four-pair clean window breaks the ROOT DB regression that had been costing 0.5–0.7 points in D2 alone. P0 items remain unaddressed for a second consecutive audit; if another window passes without LTXV fix and canary runs, the reliability floor will prevent further recovery.

**Failure classification:**
- OPERATIONAL: SC253+1 naming inconsistency (commit subject "253+1" vs DB cycle 254)
- ARCHITECTURAL: study_log write trigger gap (43 rows; SC254's DB size unchanged suggests SC254 may have no study_log entry)
- DISCIPLINE: CLAUDE.md frozen (31st), ElevenLabs v1 absent from CLAUDE.md (18 days overdue), LTXV Aug-15 not in CLAUDE.md (19 days), SC166 absent, 3 canaries unrun, SC245/246/249 not backfilled, study_cycles id=118 not corrected — all from July 26 audit, none addressed
- MODEL CAPABILITY CEILING: none this window

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

**20 skills × 8 criteria = 160 total points maximum**

Skills assessed: anti-sycophancy, brand-identity, brief-intake, captions-and-titles, character-consistency, cinematic-standards, credit-efficiency, generation-image, generation-video, halal-audio, higgsfield-generation, kling-truck-prompting, model-ceiling-detection, model-prompting-guide, post-production, production-checklist, shariah-compliance, text-overlay-compositing, video-qa-rubric, viral-research.

**Previous: 144.50/160 = 90.3%**

### Changes this window (SC251–SC254)

**generation-video.md (SC251):**
- Coverage: +0.25 (shot_type "customize"/"intelligence" distinction documented; per-shot 512-char limit; AIMLAPI canary guidance — fills genuine multi-shot gap)
- Net: **+0.25 points**

**captions-and-titles.md (SC252):**
- Accuracy: +0.25 (Remotion v4.0.499 propagated; whisper.cpp v1.9.1 and WhisperX v3.8.6 confirmed current — 2-day cross-skill propagation is faster than previous windows)
- Net: **+0.25 points**

**halal-audio.md (SC253):**
- Coverage: +0.50 (logprob brand name QA — production-critical silent failure gate; timestamps_granularity="character" correctly scoped to karaoke-only)
- Accuracy: +0.25 (SDK v2.59.0 + ffmpeg-normalize v1.41.1 confirmed; logprob documented from SDK source, not just changelog)
- Net: **+0.75 points**

**character-consistency.md (SC253+1 / SC254):**
- Accuracy: +0.25 (Kling O3 Jul 27 recheck confirmed absent; Wan 2.7 R2V correctly nuanced; FaceFusion v3.7.1 confirmed with 2-processor bug context)
- Coverage: +0.25 (Show and Polish IP-FVR added with CodeFormer comparison — relevant future watch for olive-skin fidelity)
- Net: **+0.50 points**

**Total new points this window: +1.75**

**Persistent deductions (unchanged from previous audit):**
- model-ceiling-detection.md C8: Veo 3.1 Lite still in I2V video escalation path (T2V only, not I2V) — 26th consecutive audit, −1
- model-prompting-guide.md Part 4: SC166 differential prompt rule absent (though character-consistency.md Step 3a has equivalent) — 26th consecutive audit, −1
- CLAUDE.md meta-compliance: Pre-Gen Check #5 wrong, ElevenLabs v1 retirement absent, LTXV routing matrix warning absent, Wan 2.7 R2V absent from routing matrix — 9th consecutive window with same deductions

**Score: 146.25/160 = 91.4%** (↑ +1.1% — halal-audio.md logprob addition and cross-skill Remotion propagation are the quality drivers; structural deductions unchanged)

### CLAUDE.md Structural Audit

| Component | Status |
|-----------|--------|
| THREE-AGENT PATTERN | ✓ Present |
| PRE-GENERATION CHECKS (10 items) | ❌ Check #5 wrong ("15-40 words" → should be I2V 40-120 / T2V 80-150); Check #7 ElevenLabs v1 IDs absent (retired July 9, **18 days overdue**, guaranteed 404) |
| PRODUCTION GATES (10 items) | ✓ Present and accurate |
| MODEL ROUTING MATRIX | ❌ LTXV row missing deprecation warning (**19 days to Aug-15**); Wan 2.2 Animate Replace absent; Wan 2.7 R2V absent; Kling Turbo Pro confidence status not reflected |
| BRAND BINARY CHECKLIST | ✓ Present |
| BANNED WORDS IN MOTION PROMPTS | ✓ Present |
| SHARI'AH COMPLIANCE | ✓ Present |
| ANTI-SYCOPHANCY | ✓ Present |
| FAMILY LOCK-IN | ✓ Present |
| SNORKEL TRIAGE | ✓ Present |

**CLAUDE.md structural score: 7/10 components fully correct** (3 components with active errors/omissions — unchanged for 9 consecutive audits)

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved video:** V3-Tarik-v2-couple (2026-04-26) — **94 days ago.** No new creative output this window.

**Family lock status:** `testimonial` family, 3/6 videos approved. 3 more required before family unlock (lock_until: 6).

**Cost metric:** Credits per approved video = MATHEMATICALLY UNDEFINED (zero new output, day 94).

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

### New Production Intelligence (SC251–SC254)

**Multi-shot (SC251):**
- **shot_type: "customize" is required for character element binding in multi-shot.** If `shot_type: "intelligence"` is used, no @Element references are possible — the model auto-segments a single prompt. Add `"shot_type": "customize"` to all existing multi_prompt calls (CANARY on AIMLAPI first).
- **Per-shot prompt: keep ≤400 chars on AIMLAPI** (native limit 512 chars; safety margin for AIMLAPI parameter handling).

**Captions (SC252):**
- **Upgrade Remotion to ≥v4.0.499 before next caption compositing session.** Opacity leak between stacked layers was fixed in v4.0.499 — affects caption overlays over brand layers.

**Halal audio / VO QA (SC253):**
- **Add logprob check to every Scribe v2 post-processing call.** Flag `logprob < -2.0` on SNELVERHUIZEN and 085 3331133 specifically — these are highest-risk for silent garbling. See SC253 code example in halal-audio.md §11.
- **`timestamps_granularity="character"` available but not needed for standard VO QA.** Only use if karaoke-style per-character subtitle animation is required.

**Character consistency / FaceFusion (SC253+1):**
- **FaceFusion: upgrade to v3.7.1 before any image-to-image FaceFusion job.** v3.7.0 broke `face_swapper + face_enhancer` and `face_swapper + expression_restorer` combos on still-image inputs — v3.7.1 patches this.
- **Wan 2.7 R2V: canary still mandatory.** Blog-confirmed but docs-absent — call `alibaba/wan-2-7-r2v` with Karel `front.png`, 720p, audio FFmpeg-stripped, InsightFace ≥ 0.62. Do NOT route production shots until canary passes.
- **Kling O3: still not on AIMLAPI (Jul 27 confirmed).** Continue using Kling O1 for character shots.

### Ralph Loop

*"What would a senior creative director still reject?"*

1. **LTXV Aug-15 is now 19 days from a production failure.** CLAUDE.md routing matrix actively lists LTXV as a B-roll I2V option with no warning. A production session that opens CLAUDE.md today and follows it would route non-character I2V to LTXV — a model that will return 404 on August 16. The skill (`credit-efficiency.md`) has the warning and the fallback (`minimax/hailuo-2.3-fast`, $0.0416/sec). This gap has been flagged for 12 consecutive audits. Fix CLAUDE.md before ANY B-roll production session.

2. **Day 94 with no output and three canaries unrun.** The cheapest canary (Wan 2.2 Animate Replace) costs $0.06 flat — less than a coffee. The Wan 2.7 R2V canary uses a reference image you already have (Karel `front.png`). Kling Turbo Pro requires a 3s clip you've produced before. Collectively under $2. Running these three canaries could unlock a new draft-tier character motion model (Wan 2.7 R2V at ~$0.63/5s vs $1.09/5s Kling Standard) and validate the Turbo Pro cost structure. A senior creative director would not accept "we didn't have bandwidth for $2 of test calls" on day 94 of production stagnation.

3. **SC253's logprob brand QA is documented but not implemented in scripts.** halal-audio.md §11 has the code pattern. But `scripts/gen_*.py` still calls ElevenLabs without a post-generation Scribe v2 logprob check. The QA gate is in the skill doc — it needs to land in the actual generation scripts before the next voiceover session. Find any gen script that calls ElevenLabs and add the logprob check loop from §11.

**Overall Creative: (3.9 + 4.2 + 4.1) / 3 = 4.07 / 5.0** (→ unchanged, day 94 of production stagnation)

CREATIVE_AUDIT_COMPLETE

---

## ACTION ITEMS

### [P0 — CRITICAL — DEADLINE 19 DAYS — LTXV Aug-15]

**1. CLAUDE.md routing matrix: add LTXV deprecation alert NOW**
```
⚠️ LTXV DEADLINE Aug 15 (19 days): ltxv/ltxv-2-fast WILL 404 after Aug 15.
  → Use minimax/hailuo-2.3-fast ($0.0416/sec) for non-char I2V.
  → Check AIMLAPI docs by Aug 1 for new ltxv/ltxv-2-3-fast string.
  → If absent by Aug 10: notify owner, route ALL non-char I2V to Hailuo 2.3 Fast.
```

---

### [P0 — CRITICAL — 31st audit — CLAUDE.md: 3 fixes in one edit session]

**2. Fix Pre-Gen Check #5: prompt length (31st flag)**
```
Current:  Motion prompt: 15-40 words, motion ONLY, defined endpoint ("eases to stop")
Correct:  Motion prompt: I2V 40-120 words / T2V 80-150 words (Kling v3, July 2026).
          Motion ONLY — action arc + camera move + defined endpoint. (15-40w was Kling v1/v2.)
```

**3. Fix Pre-Gen Check #7: ElevenLabs v1 retirement (18 DAYS OVERDUE)**
```
⚠️ RETIRED JULY 9, 2026: eleven_monolingual_v1 / eleven_multilingual_v1 / scribe_v1 → 404 NOW.
Use: eleven_v3 (TTS production) / eleven_flash_v2_5 (TTS draft) / scribe_v2 (captions).
NOTE: language_code NOT supported on eleven_multilingual_v2 (silently ignored, June 29, 2026).
grep -r "monolingual_v1\|scribe_v1" scripts/ before voiceover work.
```

**4. Routing matrix: full update (LTXV + Wan 2.7 R2V + Wan 2.2 Animate Replace + Kling Turbo Pro)**
(See item #1 for LTXV. Also add:)
```
Add row: Character animation canary | Wan 2.2 Animate Replace | $0.06/gen flat
  (alibaba/wan2.2-14b-animate-replace; video_url + image_url + resolution: "720p")

Add row: Character motion (R2V draft) | Wan 2.7 R2V | ~$0.63/5s est
  (alibaba/wan-2-7-r2v; reference_images + 720p + FFmpeg audio strip; InsightFace ≥ 0.62)
  Status: AIMLAPI blog-confirmed / docs-absent — CANARY REQUIRED before production

Update: Kling Turbo Pro — "HIGH confidence July 2026 (multi-source). CANARY for AIMLAPI cost/audio."
```

---

### [P0 — CRITICAL — ROOT DB SPLIT — 3rd consecutive audit unaddressed]

**5. Insert SC245/246/249 entries into data/pipeline.db**

Three cycles still absent from `data/pipeline.db`:

```sql
-- SC245 (absent from data/)
INSERT INTO study_cycles (cycle, topic, date, summary, git_commit)
VALUES (245, 'Caption pipeline', '2026-07-24',
  'Remotion 4.0.498 (2x new releases, no caption API changes); FFmpeg 8.1.2; whisper.cpp 1.9.1 unchanged',
  '2370803');

-- SC246 (absent from data/)
INSERT INTO study_cycles (cycle, topic, date, summary, git_commit)
VALUES (246, 'Halal audio', '2026-07-24',
  'SDK v2.59.0: HMAC webhook only, zero audio API changes. Added pcm_8000/16000/22050/24000/32000 (telephony-only). FFmpeg n8.1.2 current.',
  '4d14ab2');

-- SC249 (absent from data/)
INSERT INTO study_cycles (cycle, topic, date, summary, git_commit)
VALUES (249, 'Post-production', '2026-07-25',
  'Remotion v4.0.499: opacity leaking between layers FIXED (upgrade if using opacity on stacked layers). getVideoMetadata() deprecated. v4.0.498: v5 prep (SwiftShader default, Node/ESLint raised, Webpack/Rspack split). FFmpeg 8.1.2 confirmed.',
  '4a8c33a');
```

---

### [P0 — DATA INTEGRITY — study_cycles id=118 stale FFmpeg version (4th consecutive audit)]

**6. Correct study_cycles id=118 summary:**
```sql
UPDATE study_cycles SET summary =
  'FFmpeg 8.1.2 (n8.1.2, June 17 2026) is current stable. SC239 error; corrected SC242.'
WHERE id = 118;
```

---

### [P0 — BEFORE NEXT PRODUCTION SESSION — 3 canaries outstanding]

**7. Wan 2.7 R2V canary (SC247: AIMLAPI blog-confirmed, 7 days outstanding):**
- Model: `alibaba/wan-2-7-r2v`; Karel `front.png` in `reference_images`; `aspect_ratio: "9:16"`; `duration: 5`; audio FFmpeg-stripped as mandatory safety step
- If `model-not-found` → fall back to `alibaba/wan-2-6-r2v`; update status to "blog says available but endpoint not live"
- If output received: InsightFace ≥ 0.62 gate + brand binary + owner review; update CLAUDE.md routing matrix

**8. Wan 2.2 Animate Replace canary (SC234, 15 days outstanding):**
- Cost: $0.06 flat. Model: `alibaba/wan2.2-14b-animate-replace`
- Step 1: NBP Edit hero frame as `image_url` + 5s drive video as `video_url`, mode: Move
- Step 2: Verify quality + confirm $0.06 billing in credit log

**9. Kling Turbo Pro canary (SC237, 15 days outstanding):**
- Model: `klingai/video-v3-turbo-pro-image-to-video` + `generate_audio: false` + 3s reference clip
- Confirm billing ($0.91/5s claimed) and audio behavior

---

### [P0 — BEFORE NEXT REMOTION SESSION — opacity leak bug]

**10. Upgrade Remotion to ≥v4.0.499 before next composition session:**
- `npm install remotion@4.0.499`
- Audit any composition using non-100% opacity on stacked layers for pre-v4.0.499 artifacts
- Migrate any script using `getVideoMetadata()` (deprecated in v4.0.498)

---

### [P0 — BEFORE NEXT VO SESSION — logprob QA implementation]

**11. Add Scribe v2 logprob check to production scripts:**
- Add the §11 logprob loop from `skills/halal-audio.md` to any `scripts/gen_*.py` that calls ElevenLabs TTS
- Flag words with `logprob < -2.0` — especially "SNELVERHUIZEN" and "085 3331133"

---

### [P0 — OPERATIONAL — model-ceiling-detection.md C8 — 26th consecutive audit]

**12. Remove Veo 3.1 Lite from I2V video escalation path** — Veo 3.1 Lite is T2V only (one-line removal in model-ceiling-detection.md C8)

---

### [P0 — BEFORE NEXT CHARACTER SESSION — SC166 — 26th audit]

**13. model-prompting-guide.md Part 4 — add SC166 differential prompt rule:**
```
On facial-movement retries: use action-only prompts; strip identity-descriptive words.
(Validated by DomainShuttle arXiv 2606.26058 + AnyID arXiv 2603.25188 — both confirm
character attributes in text compete with identity flow. Text = action+camera ONLY.)
```

---

### [NEW — NAMING — SC253+1 commit history note]

**14. Note for future cycles:** Content commits should use the same cycle number as the corresponding log commit. SC253+1 content (19b7b98) vs SC254 log (6f351e1) creates ambiguity in git log. DB is internally consistent (cycle=254). For future cycles: if the session labels a cycle "253+1" in the commit message, the log should also say "SC253+1 log" for consistency, or the content commit should say "Study cycle 254".

---

## TELEGRAM REPORT STATUS

Telegram env not found at `$HOME/.claude/channels/telegram/`. Telegram report NOT sent.

Report text (max 15 lines — for manual resend if needed):
```
📊 Daily Audit 2026-07-27 — Snelverhuizen Pipeline

Operator: 3.05/5.0 (↑ +0.19) — 4 CLEAN PAIRS, best execution in 10+ cycles
Skills:   91.4% (+1.1%) — halal-audio logprob gate + cross-skill Remotion propagation
Creative: 4.07/5.0 (→) — day 94, no new output, 3 canaries still unrun

⚠️ LTXV Aug-15: 19 days. CLAUDE.md routing matrix still has NO alert
⚠️ ElevenLabs v1: 18 days past retirement — absent from CLAUDE.md Pre-Gen Check #7
⚠️ SC245/246/249 still missing from data/pipeline.db (3rd audit unaddressed)

TOP 3 ACTION ITEMS:
1. Fix CLAUDE.md now: LTXV deprecation + prompt length + ElevenLabs v1 (one edit session)
2. Run Wan 2.7 R2V canary — blog-confirmed 7 days, costs under $1, unlocks ~$0.43/shot savings
3. Add logprob Scribe v2 check to gen scripts (SC253 pattern in halal-audio.md §11 — copy/paste)
```

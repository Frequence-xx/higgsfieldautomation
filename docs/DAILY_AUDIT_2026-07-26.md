# Daily Audit — 2026-07-26

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-07-25 | Operator 2.92/5.0 · Skills 89.5% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-07-25 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **2.86 / 5.0** | ↓ −0.06 | ↓ −0.99 |
| Skill Library & Policy | **90.3%** (144.50/160) | ↑ +0.8% | ↓ −1.2% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Three study cycles (SC248–SC250) since the 2026-07-25 audit.** Operator score falls to 2.86/5.0 (−0.06). Primary driver: SC249 log commit (d01f2a2) targeted root `pipeline.db` instead of `data/pipeline.db` — the third ROOT DB failure in six cycles, breaking any hope of re-establishing a clean streak. SC248 introduced a bundling violation (content commit included both `skills/credit-efficiency.md` and `data/pipeline.db`). SC250 is a CLEAN PAIR recovering the pattern.

**Skill content quality remains the window's strength:** SC249's Remotion v4.0.499 opacity-leak fix is production-critical (any composition with stacked opacity layers must upgrade before next Remotion session). SC248 corrects a six-week pricing error (Krea WAN 14B V2V was $0.026/sec in SC234, confirmed $0.033/sec — prevents wrong cost projections). SC250 correctly classifies Qwen-Image-3.0 as not available on AIMLAPI.

**Persistent structural blockers:** CLAUDE.md frozen for the 30th consecutive audit. ElevenLabs v1 model IDs now 17 days past retirement (404 guaranteed). LTXV Aug-15 deadline is now **20 days away** — credit-efficiency.md has the warning, CLAUDE.md routing matrix does not. Zero canaries run (Wan 2.7 R2V blog-confirmed 6 days ago, Wan 2.2 Animate Replace 14 days outstanding, Kling Turbo Pro 14 days outstanding). study_cycles id=118 stale FFmpeg data unaddressed (3rd consecutive audit). Day 93 without approved creative output.

---

## CHANGES SINCE 2026-07-25 AUDIT

Git commits since `14f64d2` (July 25 audit):

| Hash | Commit | Files changed | DB path | Protocol |
|------|--------|---------------|---------|----------|
| 6992395 | SC248: Cost optimization (pass 34) — Krea V2V corrected $0.026→$0.033/sec, LTXV 21d deadline, no new AIMLAPI video models July 22-25 | `skills/credit-efficiency.md` + `data/pipeline.db` (BUNDLED) | `data/` ✓ path | ⚠️ BUNDLED COMMIT |
| 32aaa35 | SC248 log: record study cycle 248 commit hash in pipeline.db | `data/pipeline.db` only | `data/` ✓ | ✓ CLEAN LOG |
| 4a8c33a | SC249: Post-production (pass 34) — Remotion v4.0.499, opacity leak fix, getVideoMetadata() deprecated | `skills/post-production.md` only | — | ✓ CLEAN CONTENT |
| d01f2a2 | SC249 log: record study cycle 249 commit hash in pipeline.db | `pipeline.db` (ROOT) ❌ | ROOT ❌ | ❌ ROOT DB ERROR |
| d5eb3a5 | SC250: Hero frame generation (pass 37) — Qwen-Image-3.0 watch item added, FLUX.2 Max/Edit recheck dates 07-23→07-26 | `skills/generation-image.md` only | — | ✓ CLEAN CONTENT |
| df9e679 | SC250 log: record study cycle 250 commit hash in pipeline.db | `data/pipeline.db` only | `data/` ✓ | ✓ CLEAN LOG |

**Protocol compliance this window (SC248–SC250):**
- Clean pairs: **SC250 = ✓** (1/3 strict)
- Bundled commits: **SC248 = ⚠️** — content commit 6992395 included both `skills/credit-efficiency.md` and `data/pipeline.db`; log commit 32aaa35 then also wrote `data/pipeline.db`. Two DB writes per cycle (content + log) diverges from the single-content / single-log protocol. DB path is correct (`data/`), so data integrity preserved, but the bundling pattern violates separation of concerns.
- ROOT DB errors: **SC249 = ❌ ROOT** — log commit d01f2a2 shows `pipeline.db | Bin 61440 -> 61440 bytes` (root). study_cycles cycle=249 absent from `data/pipeline.db`.
- ROOT-clean potential: SC250 is clean but SC249 breaks any 2-cycle streak. No streak to report.
- study_log: Uncertain for SC248/249/250. SC249 log targeted root DB (no study_log table → no entry). SC248 bundled content+DB in single commit (study_log write timing unclear). SC250 used correct `data/` path like SC247 which did write study_log — tentatively ≥1 new entry.

**ROOT DB divergence state (after SC250):**
- `pipeline.db` (root, 61 440 B): 65 study_cycles rows (added SC249 this window); no study_log table
- `data/pipeline.db` (155 648 B): ~124 study_cycles rows (added SC248, SC250; SC249 absent); ≥41 study_log rows
- SC249 exists ONLY in root DB; SC248/SC250 exist in `data/pipeline.db`

---

## SC CONTENT NOTES

**SC248** — `skills/credit-efficiency.md` (6992395, Sat Jul 25 12:10:06) — +12/−5 lines:
- **Krea WAN 14B V2V price CORRECTED: $0.026→$0.033/sec.** SC234 Rule 39 stated V2V at $0.026/sec. AIMLAPI pricing page confirms BOTH T2V and V2V at $0.033/sec. Correction applied in Rules 39, 49, 52, and canary checklist. Prevents wrong cost projections; V2V remains cheapest restyling option but gap vs T2V is now zero (same price).
- **LTXV Aug-15 deadline — 21 days documented (SC248).** Action plan: check AIMLAPI docs by Aug 1; if no new string by Aug 10, escalate to owner. Hailuo 2.3 Fast ($0.0416/sec) confirmed fallback.
- **No new AIMLAPI video models July 22-25.** GitHub api-docs commits in window: Anthropic Claude Opus 5, Alibaba Qwen-Image-3.0/Edit (VLMs), Poolside Laguna (code-gen). Zero video additions. All routing decisions current.
- **Wan 2.7 R2V — no dedicated docs page found (SC248, July 25).** SC241/247 raised to "canary-test recommended" / "blog-confirmed." credit-efficiency still shows unconfirmed status as of SC248 (before SC247 blog-confirmation propagated to this skill).
- Protocol: ⚠️ BUNDLED — content commit (6992395) included both `skills/credit-efficiency.md` AND `data/pipeline.db`. Log commit (32aaa35) then also wrote `data/pipeline.db`. Separation of concerns violated; data integrity preserved (both to `data/`).

**SC249** — `skills/post-production.md` (4a8c33a, Sat Jul 25 18:08:01) — +6/−1 lines:
- **Remotion v4.0.499 (July 24, 2026):** Two releases since SC245's v4.0.497 documentation.
  - **v4.0.498 (July 23):** `getVideoMetadata()` deprecated — migrate any pipeline script using this before upgrading. v5 preparation: ANGLE+SwiftShader as default, Node.js/ESLint requirements raised, Webpack/Rspack config overrides split into separate APIs, buffering defaults enabled. No new `@remotion/effects`.
  - **v4.0.499 (July 24):** **Opacity leaking between layers in web-renderer FIXED.** Upgrade to ≥v4.0.499 if any Remotion composition uses non-100% opacity on stacked layers (e.g., caption overlays over brand layers). Zod 4.4.3. New `@remotion/drag-and-drop` package (Studio only). No new `@remotion/effects`.
- **Two new production checklist items added:** Layer opacity leak check (use ≥v4.0.499) and getVideoMetadata() deprecation check.
- **All other tools confirmed unchanged:** FFmpeg 8.1.2, SVT-AV1 v4.2.0, Practical-RIFE v4.26, rife-ncnn-vulkan v20250112, PySceneDetect v0.7.1.
- Protocol: ✓ CLEAN CONTENT / ❌ ROOT LOG — content commit single-skill; log commit (d01f2a2) wrote to root `pipeline.db`.

**SC250** — `skills/generation-image.md` (d5eb3a5, Sun Jul 26 00:10:54) — +6/−3 lines:
- **Qwen-Image-3.0 added as watch item:** Alibaba released 2026-07-21. Features: 4.5K token input, sub-10px text legibility, 12 languages (incl. Dutch), complex layout, character appearance maintenance. Available ONLY on Qwen Chat/Studio and Alibaba API — **NOT on AIMLAPI.** Correctly classified as `NO API ON AIMLAPI YET⊘`. Monitor for AIMLAPI addition.
- **FLUX.2 Max recheck date updated 07-23→07-26:** Dedicated docs page at docs.aimlapi.com STILL NOT PUBLISHED (unchanged from July 16). Product landing page confirmed. CANARY REQUIRED before production.
- **FLUX.2 Max Edit recheck date updated 07-23→07-26:** docs.aimlapi.com STILL NOT PUBLISHED. Parameters partially confirmed via third-party aggregators (SC248 batch). CANARY REQUIRED.
- **Gemini Omni Flash recheck dates updated 07-23→07-26:** Status unchanged.
- Protocol: ✓ CLEAN PAIR — content commit single-skill; log commit (df9e679) to `data/pipeline.db` only.

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 3.1/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC248: Krea V2V cross-source correction | AIMLAPI pricing page cross-referenced vs SC234 stated $0.026/sec. Correction applied in 3 independent rules + canary checklist — thorough propagation. | Strong positive |
| SC248: LTXV action plan specificity | Deadline documented as "21 days" with calendar checkpoints (Aug 1, Aug 10 escalate to owner) — concrete, not just a flag | Positive |
| SC249: Two-release changelog accuracy | v4.0.498 and v4.0.499 both documented with production-relevant detail (opacity leak ≥v4.0.499, getVideoMetadata deprecation) | Positive |
| SC250: Qwen-Image-3.0 scope gatekeeping | Correctly classified as not-on-AIMLAPI at release with "Monitor for AIMLAPI addition" — no premature routing recommendation | Positive |
| **CLAUDE.md Pre-Gen Check #5 wrong (30th audit)** | "15-40 words" still wrong at point of generation | Critical negative |
| **ElevenLabs v1 retirement absent from CLAUDE.md (30th flag, 17 days overdue)** | Guaranteed 404 at next voiceover session | Critical negative |
| **LTXV Aug-15 — 20 days, 11th audit without CLAUDE.md alert** | credit-efficiency.md has the warning; CLAUDE.md routing matrix does not | Negative |
| **SC249 ROOT DB error** | After SC247 clean recovery, SC249 immediately reverts to root — reasoning gap: why did the path reset again? | Negative |
| **SC166 absent (25th audit)** | Differential prompt rule still not in model-prompting-guide.md Part 4 | Negative |

**Score: 3.1/5.0** (→ unchanged — SC248 price correction and LTXV action plan are the window's reasoning highlights; ROOT DB recurrence and CLAUDE.md non-propagation remain the floor)

---

### D2 — Execution Accuracy (20%) → 2.2/5.0 (↓ −0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC248 content commit | credit-efficiency.md + data/pipeline.db in single commit — both files bundled | ⚠️ BUNDLED |
| SC248 log commit | data/pipeline.db only (32aaa35) — correct path, but DB already written in content commit | ⚠️ Double DB write |
| SC250 = CLEAN PAIR | skills/generation-image.md + data/pipeline.db only — textbook clean | ✓ Positive |
| **SC249 log commit (d01f2a2)** | `pipeline.db | Bin 61440 → 61440 bytes` (root). study_cycles cycle=249 absent from `data/pipeline.db` | ❌ ROOT DB ERROR |
| ROOT DB pattern | SC245 ROOT, SC246 ROOT, SC249 ROOT — 3 of 8 cycles since the 4-window clean streak now ROOT-broken | ❌ Structural |
| ROOT DB divergence growing | root (65 rows, SC249 added this window) vs data/ (~124 rows, SC249 missing) | ❌ Production risk |
| P0 actions from July 25 audit | ROOT DB fix (SC245/246 inserts into data/): NOT done. CLAUDE.md 3 fixes: NOT done. SC166: NOT done. model-ceiling-detection C8: NOT done. Canaries (3): NOT run | ❌ Critical |
| CLAUDE.md frozen | 30th consecutive audit — zero structural updates | ❌ Critical structural |

**Score: 2.2/5.0** (↓ −0.1 — SC249 ROOT DB error, SC248 bundling violation; SC250 clean pair is genuine positive; no P0 items addressed this window; ROOT DB pattern worsening — 3 of last 8 cycles broken)

**Failure classification: OPERATIONAL** — SC248 and SC250 used correct `data/` path. SC249 reverted to root. The alternating pattern (clean → ROOT → clean) suggests a session-specific working directory or script path inconsistency rather than a full architectural regression. However, 3 occurrences in 8 cycles means the operational fix has not been systematically applied.

---

### D3 — Memory & Continuity (15%) → 2.3/5.0 (↓ −0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC248: cross-cycle correction from SC234 | Krea V2V V2V price error dated to SC234 (6 weeks prior), corrected in SC248 with explicit cross-reference | Strong positive |
| SC249: Remotion version chain maintained | 4.0.495→496→497→498→499 chain documented accurately across SC235/242/245/249 | Positive |
| SC250: FLUX.2 status tracking continuity | "STILL NOT PUBLISHED" consistent pattern since July 16 — correct incremental tracking | Positive |
| **SC249 study_cycles in root DB only** | Log commit d01f2a2 wrote to root (no study_log table) → cycle=249 absent from data/; any pre-production brief misses SC249's Remotion v4.0.499 opacity fix | Critical negative |
| **study_log gap: 10+ cycles absent** | Gap from July 25 audit (SC235–241, SC244–246 = 10 cycles) plus SC249 (root → no study_log entry possible). SC250 potentially wrote study_log (same data/ path as SC247 which did) — gap minimum 11 cycles | Critical negative |
| **study_cycles id=118 stale: "FFmpeg 9.0" (3rd consecutive audit)** | Halal-audio intelligence row still reports "FFmpeg 9.0 confirmed as current stable" — demonstrably false. Any session querying study_cycles for halal-audio gets incorrect FFmpeg version | Critical negative (P0 unaddressed) |
| SC248: Krea V2V blog-confirmed status vs SC247 | SC247 upgraded Wan 2.7 R2V to "blog-confirmed" but SC248's credit-efficiency update still showed "unconfirmed status" — cross-skill propagation lag | Minor negative |

**Score: 2.3/5.0** (↓ −0.1 — SC249's study_cycles in root only means production sessions miss the opacity leak fix; study_log gap expanding; stale SC239 data unaddressed for 3 audits)

---

### D4 — Reliability & Consistency (20%) → 2.2/5.0 (↓ −0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC250 = CLEAN PAIR | Recovery to correct data/ path after SC249 ROOT error | ✓ Positive |
| SC249 content accurate | post-production.md content correct — Remotion changelog, FFmpeg confirmation unchanged | ✓ Positive |
| **SC249 ROOT DB error** | Third ROOT error in 8 cycles; SC247 clean recovery was immediately followed by SC249 ROOT | ❌ Critical |
| **CLAUDE.md frozen: 30th consecutive audit** | Zero structural updates — ceiling on all reliability-related scores | ❌ Critical |
| **Zero P0 items addressed from July 25 audit** | All 12 action items outstanding: ROOT DB SC245/246 inserts, CLAUDE.md 3 fixes, study_cycles id=118, 3 canaries, SC166, model-ceiling-detection C8 | ❌ Critical |
| **Day 93: no approved creative output** | Production reliability = 0 for 93 consecutive days | Negative |
| **LTXV countdown: 20 days to Aug-15** | Routing matrix in CLAUDE.md has no warning. A production session following CLAUDE.md would still route non-char I2V to LTXV and hit 404 on Aug 16 | Negative |
| **Canaries: 3 outstanding (14/14/6 days)** | Wan 2.2 Animate Replace (14 days), Kling Turbo Pro (14 days), Wan 2.7 R2V (6 days) | Negative |

**Score: 2.2/5.0** (↓ −0.1 — SC250 clean pair; but SC249 ROOT, 30th CLAUDE.md freeze, zero P0 actions, and 20-day LTXV clock collectively prevent stability. LTXV now within single sprint of breaking production.)

---

### D5 — Tool/Model Integration (15%) → 4.3/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC248: Krea V2V price correction propagated to 3 rules | Rules 39, 49, 52 all corrected — thorough; prevents systematic cost undercounting | Strong positive |
| SC248: LTXV action plan in credit-efficiency | "Aug 1 check / Aug 10 escalate" — specific dates with fallback model named ($0.0416/sec Hailuo 2.3 Fast) | Strong positive |
| SC249: opacity leak fix documented with upgrade gate | "upgrade to ≥v4.0.499 if any Remotion composition uses non-100% opacity on stacked layers" — correct production gate | Strong positive |
| SC249: getVideoMetadata() deprecation flagged | Explicit: "migrate any pipeline script using this before upgrading" — prevents silent breakage on v5 upgrade path | Positive |
| SC250: Qwen-Image-3.0 correctly scoped | "Alibaba-only, NOT on AIMLAPI" — prevents premature API call attempts | Positive |
| SC250: FLUX.2 Max/Edit recheck discipline | Third consecutive "still not published" recheck (July 16 → 23 → 26) — accurate status maintenance | Positive |
| **CLAUDE.md routing matrix: LTXV active (20 days to Aug-15)** | credit-efficiency.md has the warning; CLAUDE.md (point-of-generation) does not — a production session following CLAUDE.md would still use LTXV | Critical negative |
| **CLAUDE.md Check #5 wrong prompt length (30th audit)** | Wrong guidance at point of generation | Critical negative |
| **Three canaries unrun (14/14/6 days)** | Wan 2.2 Animate Replace, Kling Turbo Pro, Wan 2.7 R2V — intelligence accumulated; not tested | Negative |
| **ROOT DB split: SC249 missing from data/** | A production session querying study_cycles for post-production intelligence misses SC249's opacity fix | Negative |

**Score: 4.3/5.0** (→ unchanged — Krea V2V correction, LTXV action plan, Remotion opacity gate are the window's strongest contributions; CLAUDE.md divergence and canary backlog persist)

---

### D6 — Communication & Social (10%) → 3.7/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC248 commit body | Krea V2V correction explicitly annotated "CORRECTED SC248: was $0.026/sec (SC234 error)" — acknowledges prior error, names source. Applied to 3 rules. | ✓ Strong |
| SC249 commit body | 5-bullet summary: version chain, two specific changes (opacity, getVideoMetadata), confirmed unchanged tools — complete and scannable | ✓ Solid |
| SC250 commit body | Clear negative markers ("NOT on AIMLAPI," recheck date pattern), specific release date (2026-07-21) | ✓ Solid |
| 3/3 commit bodies substantive | Consistent standard across window | ✓ Positive |

**Score: 3.7/5.0** (→ unchanged — consistent commit body quality; SC248's acknowledgment of SC234 error is the standout)

---

### D1–D6 Weighted Score

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|-------------|
| D1 Reasoning | 3.1 | 20% | 0.620 |
| D2 Execution | 2.2 | 20% | 0.440 |
| D3 Memory | 2.3 | 15% | 0.345 |
| D4 Reliability | 2.2 | 20% | 0.440 |
| D5 Integration | 4.3 | 15% | 0.645 |
| D6 Social | 3.7 | 10% | 0.370 |
| **Total** | — | 100% | **2.86 / 5.0** |

**Delta vs 2026-07-25: −0.06** — Continued gradual regression. SC248 bundling + SC249 ROOT error are the execution failures. SC250 clean pair prevents steeper decline. No P0 items from the previous audit were addressed.

**Failure classification:**
- OPERATIONAL: ROOT DB path recurrence (SC249) — SC248/250 used correct `data/` path; SC249 reverted to root. Alternating pattern suggests session-specific working directory inconsistency — not architectural, but also not resolved.
- ARCHITECTURAL: study_log write trigger gap (11+ cycles absent; trigger fires in some sessions, not others, independently of DB path choice)
- DISCIPLINE: CLAUDE.md frozen (30th audit), ElevenLabs v1 not fixed (17 days overdue), LTXV Aug-15 not in CLAUDE.md (20 days), SC166 absent, 3 canaries unrun, study_cycles id=118 not backfilled — all P0 items from July 25 audit unaddressed
- MODEL CAPABILITY CEILING: none this window

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

**20 skills × 8 criteria = 160 total points maximum**

Skills assessed: anti-sycophancy, brand-identity, brief-intake, captions-and-titles, character-consistency, cinematic-standards, credit-efficiency, generation-image, generation-video, halal-audio, higgsfield-generation, kling-truck-prompting, model-ceiling-detection, model-prompting-guide, post-production, production-checklist, shariah-compliance, text-overlay-compositing, video-qa-rubric, viral-research.

**Previous: 143.25/160 = 89.5%**

### Changes this window (SC248–SC250)

**credit-efficiency.md (SC248):**
- Accuracy: +0.50 (Krea V2V price correction propagated to 3 independent rules — prevents systematic cost undercounting; LTXV Aug-15 action plan now concrete)
- Net: **+0.50 points**

**post-production.md (SC249):**
- Accuracy: +0.50 (Remotion v4.0.499 opacity-leak fix and getVideoMetadata() deprecation both production-critical; documented with upgrade gate language)
- Coverage: +0.25 (two new checklist items added; v4.0.498 changelog separate from v4.0.499 — version boundary correctly maintained)
- Net: **+0.75 points**

**generation-image.md (SC250):**
- Coverage: +0.25 (Qwen-Image-3.0 watch item added with correct AIMLAPI scoping; recheck discipline maintained for FLUX.2 Max/Edit)
- Net: **+0.25 points**

**Total new points this window: +1.25 (conservative — persistent deductions unchanged)**

**Persistent deductions (unchanged from previous audit):**
- model-ceiling-detection.md C8: Veo 3.1 Lite listed in video escalation path (T2V only, not I2V) — 25th consecutive audit, −1
- model-prompting-guide.md Part 4: SC166 differential prompt rule absent — 25th consecutive audit, −1
- CLAUDE.md meta-compliance: Pre-Gen Check #5 wrong, ElevenLabs v1 absent, LTXV matrix warning absent, Wan 2.7 R2V absent — continuing deductions (unchanged, 8th consecutive)

**Score: 144.50/160 = 90.3%** (↑ +0.8% — Remotion v4.0.499 opacity fix in post-production.md and Krea V2V price correction in credit-efficiency.md are meaningful accuracy gains; structural deductions unchanged)

### CLAUDE.md Structural Audit

| Component | Status |
|-----------|--------|
| THREE-AGENT PATTERN | ✓ Present |
| PRE-GENERATION CHECKS (10 items) | ❌ Check #5 wrong ("15-40 words" → should be I2V 40-120 / T2V 80-150); Check #7 ElevenLabs v1 IDs absent (retired July 9, **17 days overdue**, guaranteed 404) |
| PRODUCTION GATES (10 items) | ✓ Present and accurate |
| MODEL ROUTING MATRIX | ❌ LTXV row missing deprecation warning (**20 days to Aug-15**); Wan 2.2 Animate Replace absent; Wan 2.7 R2V absent; Turbo Pro confidence status not reflected |
| BRAND BINARY CHECKLIST | ✓ Present |
| BANNED WORDS IN MOTION PROMPTS | ✓ Present |
| SHARI'AH COMPLIANCE | ✓ Present |
| ANTI-SYCOPHANCY | ✓ Present |
| FAMILY LOCK-IN | ✓ Present |
| SNORKEL TRIAGE | ✓ Present |

**CLAUDE.md structural score: 7/10 components fully correct** (3 components with active errors/omissions — unchanged for 8 consecutive audits)

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved video:** V3-Tarik-v2-couple (2026-04-26) — **93 days ago.** No new creative output this window.

**Family lock status:** `testimonial` family, 3/6 videos approved. 3 more required before family unlock (lock_until: 6).

**Cost metric:** Credits per approved video = MATHEMATICALLY UNDEFINED (zero new output, day 93).

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

### New Production Intelligence (SC248–SC250)

**Cost optimization (SC248):**
- **Krea V2V corrected: $0.033/sec (NOT $0.026/sec).** Affects B-roll restyling cost calculations. At $0.033/sec, 5s restyle = $0.165 (previously miscalculated as $0.13). V2V still cheapest restyling on AIMLAPI — but no longer cheaper than T2V (same rate).
- **LTXV: DO NOT ROUTE NEW PRODUCTION SHOTS.** Use Hailuo 2.3 Fast (`minimax/hailuo-2.3-fast`, $0.0416/sec) for all non-character I2V. LTXV string will 404 after Aug 15.

**Post-production (SC249):**
- **⚠️ UPGRADE REMOTION TO ≥v4.0.499 BEFORE NEXT COMPOSITION SESSION.** Opacity leaking between stacked layers was a web-renderer bug (pre-v4.0.499). Caption overlays over brand layers, badge compositions, any multi-layer opacity work is affected. Upgrade first.
- **Migrate any script using `getVideoMetadata()`** before upgrading to v4.0.498+. This API is deprecated; v5 will remove it.

**Hero frame generation (SC250):**
- **Qwen-Image-3.0:** Not on AIMLAPI at launch (2026-07-21). Sub-10px text legibility and 12-language support make it a future watch for box text shots — but no AIMLAPI endpoint yet. Do NOT attempt API call.
- **FLUX.2 Max/Edit:** Product pages live but docs still absent. Canary required before any production use.

### Ralph Loop

*"What would a senior creative director still reject?"*

1. **LTXV Aug-15 is a production landmine now 20 days out.** CLAUDE.md routing matrix still lists LTXV as an active B-roll I2V route with no warning. A production session in the next 20 days that opens CLAUDE.md and follows the routing matrix would route non-character I2V to LTXV — a model that will 404 on August 16. The credit-efficiency.md skill has the warning and the fallback (`minimax/hailuo-2.3-fast`). The gap between skill (correct) and CLAUDE.md (missing) is a production accident waiting to happen. Fix CLAUDE.md routing matrix before any B-roll production session.

2. **The Remotion opacity leak is a silent quality bug that has been in production compositions.** If any caption overlay or brand badge was composited using opacity on stacked layers in Remotion before v4.0.499, those files have visible quality defects. The pipeline should audit existing compositions built on v4.0.495–4.0.498 for this bug and re-render with v4.0.499 if affected.

3. **Day 93 with no canaries run and no new output.** Wan 2.7 R2V is AIMLAPI blog-confirmed (SC247, July 25). Wan 2.2 Animate Replace costs $0.06 flat — less than a coffee. Kling Turbo Pro requires a 3s reference clip. Three canaries, collectively under $0.50, could unlock new routing options and new character motion capabilities. Fourteen days of outstanding canary recommendations have produced zero test runs. A senior creative director would not accept "we didn't have time to run a $0.06 test" on day 93 of production stagnation.

**Overall Creative: (3.9 + 4.2 + 4.1) / 3 = 4.07 / 5.0** (→ unchanged, day 93 of production stagnation)

CREATIVE_AUDIT_COMPLETE

---

## ACTION ITEMS

### [P0 — CRITICAL — DEADLINE 20 DAYS — LTXV Aug-15]

**1. CLAUDE.md routing matrix: add LTXV deprecation alert NOW**

```
⚠️ LTXV DEADLINE Aug 15 (20 days): ltxv/ltxv-2-fast WILL ERROR after Aug 15.
  → Use minimax/hailuo-2.3-fast ($0.0416/sec) for non-char I2V.
  → Check AIMLAPI docs by Aug 1 for new ltxv/ltxv-2-3-fast string.
  → If absent by Aug 10: notify owner, route ALL non-char I2V to Hailuo 2.3 Fast.
```

---

### [P0 — CRITICAL — 30th audit — CLAUDE.md: 3 fixes needed in one edit session]

**2. Fix Pre-Gen Check #5: prompt length (30th flag)**
```
Current:  Motion prompt: 15-40 words, motion ONLY, defined endpoint ("eases to stop")
Correct:  Motion prompt: I2V 40-120 words / T2V 80-150 words (Kling v3, July 2026).
          Motion ONLY — action arc + camera move + defined endpoint. (15-40w was Kling v1/v2.)
```

**3. Fix Pre-Gen Check #7: ElevenLabs v1 retirement (17 DAYS OVERDUE)**
```
⚠️ RETIRED JULY 9, 2026: eleven_monolingual_v1 / eleven_multilingual_v1 / scribe_v1 → 404 NOW.
Use: eleven_v3 (TTS production) / eleven_flash_v2_5 (TTS draft) / scribe_v2 (captions).
NOTE: language_code NOT supported on eleven_multilingual_v2 (silently ignored, June 29, 2026).
grep -r "monolingual_v1\|scribe_v1" scripts/ before voiceover work.
```

**4. Routing matrix: full update (LTXV + Wan 2.2 Animate Replace + Turbo Pro + Wan 2.7 R2V)**
See item #1 above for LTXV block. Also add:
```
Add row: Character animation canary | Wan 2.2 Animate Replace | $0.06/gen flat
  (alibaba/wan2.2-14b-animate-replace; video_url + image_url + resolution: "720p")

Add row: Character motion (R2V) | Wan 2.7 R2V | TBD ($0.033/sec est)
  (alibaba/wan-2-7-r2v; reference_images + 720p + generate_audio: false; InsightFace ≥ 0.62)
  Status: AIMLAPI blog-confirmed available as of SC247 (2026-07-25)

Update: Kling Turbo Pro — "HIGH confidence multi-source July 2026. Canary for AIMLAPI cost/audio."
```

---

### [P0 — CRITICAL — ROOT DB SPLIT — 2nd consecutive audit unaddressed]

**5. Insert SC245/246/249 entries into data/pipeline.db**

SC245 and SC246 log commits went to root DB (July 24 audit, still unaddressed). SC249 added this window. Three cycles now absent from `data/pipeline.db`:

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

**6. Fix log script path for SC249 sessions:**
Investigate why SC249 wrote to root `pipeline.db` instead of `data/pipeline.db`. Check working directory at log script invocation. Compare SC249's script invocation vs SC250's (SC250 used correct data/ path). Apply the same fix that made SC250 clean.

---

### [P0 — DATA INTEGRITY — study_cycles id=118 stale FFmpeg version (3rd consecutive audit)]

**7. Backfill study_cycles id=118 summary (SC239 / halal-audio):**
```
study_cycles row: id=118, cycle=239, topic='Halal audio (pass 36)', date='2026-07-22'
Current: "FFmpeg 9.0 confirmed as current stable" — FALSE
Correct: "FFmpeg 8.1.2 (n8.1.2, June 17 2026) is current stable. SC239 error; corrected SC242."
```

---

### [P0 — BEFORE NEXT PRODUCTION SESSION — 3 canaries outstanding]

**8. Wan 2.7 R2V canary (SC247: AIMLAPI BLOG-CONFIRMED, 6 days outstanding):**
- Model: `alibaba/wan-2-7-r2v`; Karel `front.png` in `reference_images`; `aspect_ratio: "9:16"`; `duration: 5`; `audio_mode: "mute"`
- If `model-not-found` → fall back to `alibaba/wan-2-6-r2v`; update status to "blog says available but endpoint not live"
- If output received: InsightFace ≥ 0.62 gate + brand binary + owner review; update CLAUDE.md routing matrix

**9. Wan 2.2 Animate Replace canary (SC234, 14 days outstanding):**
- Step 1: NBP Edit hero frame as `image_url` + 5s drive video as `video_url`, mode: Move, $0.06 flat
- Step 2: Verify quality + confirm $0.06 billing in credit log
- If Move passes: Replace mode with B-roll + hero frame reference

**10. Kling Turbo Pro canary (SC237, 14 days outstanding):**
- `klingai/video-v3-turbo-pro` + `generate_audio: false` + 3s reference clip + confirm billing
- Quality confidence: HIGH (multi-source). Only AIMLAPI cost/audio unknown.

---

### [P0 — BEFORE NEXT REMOTION SESSION — opacity leak bug]

**11. Upgrade Remotion to ≥v4.0.499 before next composition session:**
- `npm install remotion@4.0.499`
- Audit existing compositions using opacity on stacked layers for pre-v4.0.499 artifacts
- Run `getVideoMetadata()` migration scan if any pipeline scripts use this call

---

### [P0 — DATA INTEGRITY — study_log gap investigation]

**12. Investigate study_log gaps SC235–241 + SC244–246 + SC249:**
- study_log has ≥41 rows (SC247 wrote id=41 on 2026-07-25)
- SC249: root DB log commit → no study_log entry possible
- SC248: content commit bundled DB write → study_log write timing unclear
- SC250: used correct data/ path like SC247 → likely wrote study_log
- Backfill: write study_log entries for missing cycles from study_cycles summaries

---

### [P0 — OPERATIONAL — model-ceiling-detection.md C8 — 25th consecutive audit]

**13. Remove Veo 3.1 Lite I2V from video escalation path** — Veo 3.1 Lite is T2V only (one-line removal)

---

### [P0 — BEFORE NEXT CHARACTER SESSION — SC166 — 25th audit]

**14. model-prompting-guide.md Part 4 — add SC166 differential prompt rule:**
```
On facial-movement retries: use action-only prompts; strip identity-descriptive words.
(Validated by Stand-In (arXiv 2508.07901) + WildActor (arXiv 2603.00586) — both confirm
character attributes in text compete with identity flow. Text = action+camera ONLY.)
```

---

## TELEGRAM REPORT STATUS

Telegram env not found at `$HOME/.claude/channels/telegram/.env`. Telegram report NOT sent.

Report text (for manual resend if needed):
```
📊 Daily Audit 2026-07-26 — Snelverhuizen Pipeline

Operator: 2.86/5.0 (↓ -0.06) — SC249 ROOT DB + SC248 bundled commit
Skills:   90.3% (+0.8%) — Remotion opacity fix + Krea V2V price correction
Creative: 4.07/5.0 (→) — day 93, no new output

⚠️ LTXV Aug-15: 20 days. CLAUDE.md has NO alert — fix before any B-roll session
⚠️ Remotion ≥v4.0.499 REQUIRED: opacity leak in web-renderer fixed; upgrade now
⚠️ SC249 log went to ROOT db: cycle=249 missing from data/pipeline.db

TOP 3 ACTION ITEMS:
1. Fix CLAUDE.md routing matrix: LTXV deprecation + ElevenLabs v1 + prompt length
2. Run Wan 2.7 R2V canary (blog-confirmed 6 days ago, $0 cost on first 3s clip)
3. Insert SC245/246/249 into data/pipeline.db (fix ROOT DB split — now 3 cycles missing)
```

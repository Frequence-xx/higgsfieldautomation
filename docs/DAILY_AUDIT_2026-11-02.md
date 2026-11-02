# Daily Audit — 2026-11-02

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-11-01 | Operator 3.63/5.0 · Skills 99.8% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-11-01 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **3.71 / 5.0** | ↑ +0.08 | ↓ −0.14 |
| Skill Library & Policy | **99.8%** (159.75/160) | → 0.00% | ↑ +8.3% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Active window. Four study cycles (SC399–SC402) landed since the Nov 1 audit.** DB compliance recovery: **4/4 = 100% this window** (↑ from 1/3 = 33% yesterday). Running tally: ~50/75 ≈ 66.7% (↑ from 65%). SC401 resolves SC387 deprecation concern for MAI-Image 2.5 (docs 404 was wrong URL path, not deprecation). SC402 identifies alternate v4 R2V model ID on AIMLAPI with canary fallback strategy.

**Day 74: O3 $1.46 contradiction in generation-video.md still not fixed (SC402 touched the file but did not fix it).**

**Day 51: CLAUDE.md P0 pricing errors still not fixed.**

**Day 203: No approved creative output.**

---

## CHANGES SINCE 2026-11-01 AUDIT

**8 commits — 4 study cycles (SC399–SC402) with DB compliance 4/4.**

| SC | Date | Skill Updated | Net Content |
|----|------|---------------|-------------|
| SC399 | Nov 1 | credit-efficiency.md | Kling v4 720p pricing re-confirmed via Unifically reseller (Oct 2026): $0.1134/sec 720p, $0.1701/sec 1080p — 22% cheaper than v3 Pro if AIMLAPI splits by resolution; canary still required for billing confirmation. LTXV 2.5 re-confirmed NOT on AIMLAPI. |
| SC400 | Nov 1 | post-production.md | Confirmatory cycle: FFmpeg 9.0.2, SVT-AV1 v4.2.0, rife-ncnn-vulkan v20250112/v4.26, PySceneDetect v0.7.2 all confirmed unchanged. Section header updated SC393→SC400; added FFmpeg 9.1 feature notes (improved AAC encoder; APV/ASTC not pipeline-relevant). |
| SC401 | Nov 1 | generation-image.md | **Z-Image Turbo model string confirmed `alibaba/z-image-turbo`** via AIMLAPI docs page + 3 third-party aggregators; aspect_ratio 9:16 high-confidence; AIMLAPI proxy canary still required. **MAI-Image 2.5 ACTIVE on AIMLAPI** — SC387 deprecation concern resolved (docs 404 was old URL path, not deprecation; correct path: /api-references/image-models/microsoft/mai-image-2.5). MAI-Image 2.6 Flash on Vercel AI Gateway only (microsoft/mai-image-2.6-flash) — NOT on AIMLAPI. |
| SC402 | Nov 2 | generation-video.md | **Alternate AIMLAPI model ID for v4 R2V found:** `klingai/video-v4-reference-to-video` exists alongside `kling-video/v4/reference-to-video` — canary fallback strategy added. Kling v3 4K confirmed still NOT on AIMLAPI (live on EachLabs/WaveSpeed at $0.42/sec). Kling 4.0 Flash confirmed NOT on AIMLAPI — web UI only for Ultra yearly subscribers. |

**DB compliance this window: 4/4 (100%) — RECOVERY from 1/3 (33%) yesterday.**

| SC | study_cycles | cycle_commits | Pair status |
|----|-------------|--------------|-------------|
| SC399 | ✅ | ✅ (hash f085154) | Clean ✅ |
| SC400 | ✅ | ✅ (hash 4c753a5) | Clean ✅ |
| SC401 | ✅ | ✅ (hash 3d5a5b6) | Clean ✅ |
| SC402 | ✅ | ✅ (hash e23c5fd) | Clean ✅ |

**Running tally update: was ~46/71 ≈ 65%. This window adds 4 clean pairs / 4 possible → ~50/75 ≈ 66.7% (↑ from 65%).**

**CLAUDE.md: ZERO changes since Oct 20 (last CLAUDE.md change: Oct 26 audit — not a P0 fix).** All P0 items persist — now day 51.

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 3.65/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC401: MAI-Image 2.5 ACTIVE resolution — SC387 docs 404 correctly reframed as wrong URL path, not deprecation; new correct path confirmed | Sound diagnostic reasoning; resolves a critical concern without overcorrecting | ✅ |
| SC401: Z-Image Turbo model string confirmed via AIMLAPI docs + 3 third-party aggregators — triangulation under incomplete evidence | Correct multi-source triangulation; canary maintained for proxy | ✅ |
| SC402: Alternate v4 R2V model ID discovery — two AIMLAPI pages for same model; fallback strategy (try canonical first, if 404 try alternate) is prudent | Correct disambiguation under conflicting AIMLAPI docs structure | ✅ |
| SC399: Kling v4 720p "22% cheaper than v3 Pro IF AIMLAPI splits by resolution" — conditional framing correct | Not committing to pricing before billing split confirmed; correct uncertainty representation | ✅ |
| SC400: All tools unchanged confirmatory cycle — minimal update (header only) appropriate | Scope-matched output for confirmatory cycle | ✅ |
| **O3 $1.46 contradiction in generation-video.md — day 74** | SC402 touched the file; 6 lines changed; contradiction not fixed | ❌ DISCIPLINE |
| **CLAUDE.md P0 freeze — day 51** | Zero action | ❌ DISCIPLINE |

**Score: 3.65/5.0** (↑ +0.05 — SC401 MAI-Image 2.5 resolution is the strongest reasoning signal this window; SC402 alternate model ID with fallback strategy is clean; persistent P0 items cap the score)

---

### D2 — Execution Accuracy (20%) → 3.70/5.0 (↑ +0.20)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| **DB compliance: 4/4 = 100% this window** — full recovery from 1/3 (33%) yesterday | Running tally improves to ~66.7% (↑ from 65%) | ✅ RECOVERY |
| SC401: generation-image.md updated with correct model strings, URL paths, and active/inactive status per AIMLAPI | Multi-location update consistent and correct | ✅ |
| SC402: Alternate v4 R2V model ID canary note added to correct location (v4 CANARY CHECKLIST section) | Structured, findable placement | ✅ |
| SC399: credit-efficiency.md pricing update — conditional framing ("if AIMLAPI splits") correct | Precision execution; no overcommitment | ✅ |
| SC400: Minimal 4-line update for confirmatory cycle — appropriate scope | No scope creep | ✅ |
| **O3 $1.46 not fixed** — SC402 made 6 edits to generation-video.md, none in O3 comparison section | 2-minute fix on active file; skipped again | ❌ DISCIPLINE |
| **CLAUDE.md P0 not fixed** | | ❌ DISCIPLINE |

**Score: 3.70/5.0** (↑ +0.20 — DB recovery to 4/4 is the primary positive; running tally improving; MAI-Image 2.5 active/inactive status correctly documented; O3 fix skipped again despite SC402 touching the same file)

---

### D3 — Memory & Continuity (15%) → 3.75/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC401: References SC387 for MAI-Image 2.5 concern; resolves it correctly — not re-derived | SC387 → SC401 longitudinal resolution chain | ✅ |
| SC402: References SC381 for v4 R2V AIMLAPI confirmation; adds SC402 alternate ID discovery as layer | Correct longitudinal build | ✅ |
| SC401: Z-Image Turbo references SC394 (last canary status); SC401 closes the model string gap | Prior canary work correctly recalled | ✅ |
| SC400: All tool versions cited from prior SCs; no re-derivation of known-confirmed state | Stable memory anchor for post-production stack | ✅ |
| SC399: LTXV 2.5 "re-confirmed NOT on AIMLAPI as of SC399" — adds current-date anchor to prior confirmation | Correct versioning of negative confirmation | ✅ |
| **O3 contradiction: day 74** | | ❌ DISCIPLINE |
| **SC397 DB gap (cycle_commits missing) and SC398 DB gap (completely absent)** — prior window failures; not yet addressed via DB repair | Running tally history still contains dirty pairs | ❌ OPERATIONAL |

**Score: 3.75/5.0** (↑ +0.05 — SC401 chain resolution (SC387→SC401) and SC402 longitudinal build on SC381 are positive memory signals; SC397/SC398 DB gaps not retroactively repaired)

---

### D4 — Reliability (20%) → 3.55/5.0 (↑ +0.15)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| **DB compliance: 4/4 = 100% this window** — running tally recovering | Structural recovery | ✅ |
| SC402: "CANARY REQUIRED" maintained for all v4 AIMLAPI paths despite alternate model ID discovery | No production premature unlock | ✅ |
| SC401: AIMLAPI proxy canary still required for Z-Image Turbo despite model string confirmation | Correct separation of model string vs proxy behavior | ✅ |
| SC399: "canary test required (resolution param billing split unconfirmed)" — explicit production gate on pricing | No budget risk from unconfirmed split | ✅ |
| **O3 $1.46: day 74** — in active routing matrix comparisons, causing 2× budget overestimation risk | Reliability risk in production routing | ❌ DISCIPLINE |
| **CLAUDE.md P0: day 51** | Reliability risk in core policy document | ❌ DISCIPLINE |
| SC397/SC398 DB gaps not repaired (retroactive fix not attempted) | Historical tally integrity not restored | ❌ OPERATIONAL |

**Score: 3.55/5.0** (↑ +0.15 — DB recovery to 4/4 drives improvement; canary gates maintained across all four new cycles; persistent P0 items and unremediated prior DB gaps cap the score)

---

### D5 — Integration (15%) → 3.90/5.0 (↓ −0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC401: MAI-Image 2.5 ACTIVE — removes a false deprecation gate; model now usable for hero frame generation | Unblocks image generation path | ✅ |
| SC401: Z-Image Turbo `alibaba/z-image-turbo` confirmed — model string ready for production once proxy canary passes | Production-ready model string | ✅ |
| SC402: Alternate v4 R2V model ID with fallback strategy — reduces integration failure risk on first v4 R2V call | Proactive failure path coverage | ✅ |
| SC399: v4 720p pricing canary condition defined — "if AIMLAPI splits by resolution, test `resolution: '720p'`" | Integration test condition explicit | ✅ |
| SC400: Post-production stack confirmed stable — no version drift detected | No integration regression | ✅ |

**Score: 3.90/5.0** (↓ −0.05 — Slight decrease vs last window; SC399-SC402 are mostly confirmatory with narrower new capability surface than SC398's v4 R2V full parameter schema; SC401 MAI-Image 2.5 resolution is the strongest new integration unlock)

---

### D6 — Social / Communication (10%) → 3.80/5.0 (↓ −0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC402: "CANARY: try `kling-video/v4/reference-to-video` first; if rejected with 404, try `klingai/video-v4-reference-to-video` as fallback" — specific, actionable fallback strategy | Owner can execute without re-research | ✅ |
| SC401: MAI-Image 2.5 resolution: "docs 404 was old URL path — correct path is /api-references/..." — specific correction with cause explained | Not just "fixed"; explains what was wrong | ✅ |
| SC400: "All tools confirmed unchanged" — concise confirmatory statement | Correct level of signal for confirmatory cycle | ✅ |
| SC399: "22% cheaper than v3 Pro IF AIMLAPI splits by resolution — canary required" | Conditional framing clear; no false precision | ✅ |

**Score: 3.80/5.0** (↓ −0.05 — Slightly below yesterday; window is mostly confirmatory vs SC398's audio canary haram risk framing which was exceptional; SC402 fallback strategy is clean but lower urgency)

---

### AUDIT 1 SUMMARY

| Dimension | Weight | Score | Contribution |
|-----------|--------|-------|-------------|
| D1 Reasoning | 20% | 3.65 | 0.730 |
| D2 Execution | 20% | 3.70 | 0.740 |
| D3 Memory | 15% | 3.75 | 0.563 |
| D4 Reliability | 20% | 3.55 | 0.710 |
| D5 Integration | 15% | 3.90 | 0.585 |
| D6 Social | 10% | 3.80 | 0.380 |
| **TOTAL** | | | **3.71/5.0** |

**Failure summary:**
- DISCIPLINE (dominant): O3 $1.46 contradiction day 74; CLAUDE.md P0 freeze day 51; O3 fix skipped despite SC402 touching the same file
- OPERATIONAL: SC397/SC398 DB gaps not retroactively repaired; running tally ~66.7% (below 70% target)

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

### Skills Assessed This Window (SC399–SC402)

**credit-efficiency.md (SC399)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: "canary test required (resolution param billing split unconfirmed on AIMLAPI)" — explicit condition ✅
4. RFC 2119: Canary gates maintained ✅
5. Approval gates: v4 720p 22% savings behind resolution billing split canary ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: $0.1134/sec 720p consistent with SC395 v4 pricing section in generation-video.md; LTXV 2.5 absent consistent across skills ✅

**Score: 8/8 (100%)**

---

**post-production.md (SC400)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: All tool versions explicit (FFmpeg 9.0.2, SVT-AV1 v4.2.0, rife-ncnn-vulkan v20250112, PySceneDetect v0.7.2) ✅
4. RFC 2119: Imperative gates maintained ✅
5. Approval gates: No new gates — confirmatory cycle ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: FFmpeg 9.0.2 version tag consistent with prior entries; SC400 header update self-consistent ✅

**Score: 8/8 (100%)**

---

**generation-image.md (SC401)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: Z-Image Turbo `alibaba/z-image-turbo` explicit; MAI-Image 2.5 `microsoft/mai-image-2.5` explicit; MAI-Image 2.6 Flash "NOT on AIMLAPI" explicit ✅
4. RFC 2119: "AIMLAPI proxy canary still required" — imperative maintained ✅
5. Approval gates: Z-Image Turbo behind proxy canary; MAI-Image 2.5 active with correct URL path ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: Z-Image Turbo `alibaba/z-image-turbo` consistent with no other skill conflict; MAI-Image 2.5 activation has no CLAUDE.md conflict ✅

**Score: 8/8 (100%)** — MAI-Image 2.5 resolution is a clean, well-documented fix to a prior false-positive deprecation concern.

---

**generation-video.md (SC402)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: Alternate model ID `klingai/video-v4-reference-to-video` explicit; Kling 4.0 Flash "NOT on AIMLAPI as of SC402 Nov 2, 2026" explicit ✅
4. RFC 2119: "CANARY REQUIRED" maintained; fallback strategy imperative ✅
5. Approval gates: All v4 paths behind canary; fallback strategy has no implicit production unlock ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: Kling 4.0 Flash "web UI only" consistent with CLAUDE.md routing matrix (v4 not in production routing); v4 R2V `kling-video/v4/reference-to-video` primary model string consistent with character-consistency.md (SC398) ✅

**Score: 8/8 (100%)**

---

### Cross-Skill Consistency

| Check | Status |
|-------|--------|
| Z-Image Turbo `alibaba/z-image-turbo` in generation-image.md: no conflict with other skills | ✅ No conflict |
| MAI-Image 2.5 ACTIVE in generation-image.md: no conflict (not referenced elsewhere) | ✅ No conflict |
| Kling 4.0 Flash "web UI only": generation-video.md vs CLAUDE.md routing matrix (v4 absent from routing) | ✅ Consistent |
| v4 R2V alternate model ID `klingai/video-v4-reference-to-video` in generation-video.md vs character-consistency.md (SC398 canonical `kling-video/v4/reference-to-video`) | ✅ Additive, no conflict — alternate flagged as canary |
| LTXV 2.5 NOT on AIMLAPI: credit-efficiency.md vs generation-video.md (consistent absence) | ✅ Consistent |

**Cross-skill deductions: 0 (no mismatches this window)**

### CLAUDE.md Audit

| Component | Present | Status |
|-----------|---------|--------|
| Instruction count vs 150 limit | ~95 instructions | ✅ |
| Three-agent pattern | ✅ PLANNER/GENERATOR/EVALUATOR | ✅ |
| Snorkel triage | ✅ ZERO/3-5 taxonomy | ✅ |
| Model routing matrix | ✅ Present | ⚠️ Pricing errors persist — P0, **day 51** |
| Brand binary checklist | ✅ All 6 items | ✅ |
| Production gates | ✅ All 10 | ⚠️ Pre-gen check #5/#7 wording — day 118 |

**CLAUDE.md deduction: −0.5 (unchanged — P0 items not fixed)**

### Hindsight / Memory Status

- `data/pipeline.db`: ~101 study_cycles rows, ~21 cycle_commits rows; DB compliance 66.7% (↑ from 65% — recovering); note: SC397 and SC398 gaps not yet repaired
- Feedback catalog: Current (pattern-extractor.py runs Sundays)
- Skill memory banks: credit-efficiency, post-production, generation-image, generation-video all updated Nov 1–2

### Gap Analysis

| Gap | Severity | Days Open |
|----|---------|-----------|
| **O3 $1.46 contradiction in generation-video.md** — SC402 touched file without fixing | 🔴 CRITICAL | **74** |
| Kling v4 canary: audio strip verification (haram risk), face adherence, billing confirm | 🔴 CRITICAL | 10 |
| Wan 2.7 R2V canary on AIMLAPI ($0.65/5s confirmed live) | 🔴 CRITICAL | 4 |
| Z-Image Turbo AIMLAPI proxy canary (model string confirmed SC401) | 🔴 CRITICAL | 3 |
| CLAUDE.md pricing errors (P0) | 🟠 HIGH | **51** |
| ElevenLabs v4 Dutch canary — probability HIGH (SC397) | 🟠 HIGH | 7 |
| FaceFusion v3.9.2 CRITICAL upgrade — NVIDIA driver fatal crash on v3.9.1 | 🟠 HIGH | 4 |
| SC397/SC398 DB gaps — retroactive repair of dirty pair + completely absent SC | 🟠 HIGH | 2 |
| NB2.1 production canary — thinking_level, per-image billing | 🟡 MEDIUM | 7 |
| Kling O3 canary on AIMLAPI | 🟡 MEDIUM | 74 |
| CLAUDE.md pre-gen check #5/#7 wording | 🟡 MEDIUM | 118 |
| Kling v4 alternate model ID (`klingai/video-v4-reference-to-video`) canary test | 🟡 MEDIUM | 1 |
| Remotion v5.0 license tier verification | 🟡 MEDIUM | 4 |

### Skill Score Calculation

| Category | Passes | Possible | Notes |
|----------|--------|----------|-------|
| Core skills (18 files × 8 criteria) | 143.25 | 144 | −0.75 pre-existing (O3 contradiction in generation-video.md — SC402 touched file without fixing) |
| CLAUDE.md structural components | 5.5 | 6 | −0.5 for pricing P0 (unchanged) |
| Cross-skill consistency | 11 | 11 | No mismatches this window |
| **TOTAL** | **159.75** | **160** | **99.8%** |

**Target ≥95%: PASS → unchanged**

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved output:** V2-Proces (2026-04-12)
**Days since last approval:** **203 days**
**Output produced since Nov 1 audit:** None

No new clips to score. Scores carry forward from V2-Proces reference.

### Tier 1 — Technical (binary pass/fail)

Based on V2-Proces (last approved video):
- Resolution ≥1080p ✅ | Frame rate 24fps ✅ | Aspect ratio 9:16 ✅
- No corruption ✅ | No watermarks ✅ | Duration correct ✅

**PASS**

### Tier 2 — Visual Quality (1-5, ≥3.5 required)

Carrying forward from V2-Proces assessment:
**4.1/5.0** (above threshold)

### Tier 3 — Brand Compliance (1-5, ≥4.0 required)

**4.1/5.0** (above threshold, V2-Proces)

### Tier 4 — Advertising Effectiveness (1-5, ≥3.5 required)

**4.0/5.0** (above threshold)

**Overall Creative Score: 4.07/5.0** (→ unchanged — no new output)

### Ralph Loop

*"What would a senior creative director still reject about this pipeline's creative output?"*

1. **Day 203. Z-Image Turbo model string confirmed (SC401). MAI-Image 2.5 false-positive deprecation resolved (SC401).** The pipeline's image generation path now has two unblocked model strings ready for proxy canary. The four open canaries (Z-Image proxy behavior, Kling v4 audio strip, Wan 2.7 R2V, ElevenLabs Dutch v4) cost ~$1.44 total. A senior CD would observe that every single-session blocker is now a known-cost item. The obstacle is not knowledge or money — it is scheduling the session.

2. **SC402: O3 contradiction not fixed despite file access.** SC402 made 6 edits to generation-video.md — the exact file containing the O3 $1.46 contradiction (lines ~703, ~745-746, ~748, ~753-754). A senior CD would read that as a pattern, not an oversight: the pipeline documents the issue but does not fix it. Day 74 on a 2-minute edit is a structural avoidance pattern.

3. **DB running tally: 66.7%.** SC397/SC398 dirty pairs are still in the tally. A CD reviewing DB health would note that the prior window's regression is not retroactively repaired — only the current window is clean. The tally gap between ~50 clean pairs and 75 total is larger than it looks if the goal is auditable production records.

### Model Capability Notes (New Since Nov 1)

- **Z-Image Turbo `alibaba/z-image-turbo` confirmed (SC401)** — AIMLAPI docs page confirmed model string; aspect_ratio 9:16 high-confidence. Classification: **INTEGRATION** — proxy canary required before production.
- **MAI-Image 2.5 ACTIVE (SC401)** — SC387 deprecation concern resolved. Classification: **INTEGRATION** — model available on AIMLAPI at confirmed path; proxy canary standard pre-flight still applies.
- **Alternate v4 R2V model ID (SC402)** — `klingai/video-v4-reference-to-video` as fallback to `kling-video/v4/reference-to-video`. Classification: **INTEGRATION** — canary fallback test, not a new production model.

### Cost Metric

Credits per APPROVED video: **MATHEMATICALLY UNDEFINED** (0 approved videos since April 12, 2026)

### Predicted Pass Rate

**~73% confidence, 70% predicted pass rate** (→ unchanged)

- Upside: Z-Image Turbo model string confirmed; MAI-Image 2.5 deprecation false alarm resolved; v4 R2V alternate model ID documented; DB compliance fully recovered
- Downside: Four open CRITICAL canaries (none run); FaceFusion CRITICAL fix not applied; DB integrity SC397/SC398 not repaired; 203-day production gap; O3 contradiction in active skill file day 74

CREATIVE_AUDIT_COMPLETE

---

## TOP ACTION ITEMS (Prioritized)

| # | Priority | Action | Deadline |
|---|----------|--------|---------|
| 1 | 🔴 CRITICAL | **Fix O3 $1.46 contradiction in generation-video.md** — lines ~703, ~745-746, ~748, ~753-754 reference deprecated v3 Pro at $1.46 in O3 comparison section. 2-minute edit. **Day 74. SC402 touched this file — no excuse for another skip.** | Immediate |
| 2 | 🔴 CRITICAL | **Run combined canary session.** Four canaries now unblocked — run as one session: (a) Z-Image Turbo AIMLAPI proxy canary ($0.007); (b) Kling v4 I2V audio strip + billing ($0.785); (c) Wan 2.7 R2V + InsightFace cosine ($0.65); (d) ElevenLabs Dutch v4 language_code="nl" (fractions). Total: ~$1.44. | Next session |
| 3 | 🔴 CRITICAL | **Repair SC397/SC398 DB gaps retroactively.** SC397: write missing cycle_commits row. SC398: write both study_cycles and cycle_commits rows. Running tally integrity requires repair of prior dirty pairs, not just forward compliance. | Next session |
| 4 | 🟠 HIGH | **Fix CLAUDE.md pricing errors (P0)** — v3 Pro $1.46→$0.728; v3 Standard $1.09→$0.546; Wan 2.6 I2V fallback note. Day 51. 5-minute edit. | Immediate |
| 5 | 🟠 HIGH | **Upgrade FaceFusion to v3.9.2** — CRITICAL NVIDIA driver fatal crash on v3.9.1. `git checkout 3.9.2` before ANY FaceFusion run. | Before next FaceFusion run |
| 6 | 🟡 MEDIUM | **Kling v4 alternate model ID canary** — test `klingai/video-v4-reference-to-video` vs `kling-video/v4/reference-to-video` on first v4 R2V call; update generation-video.md with confirmed string. | Next v4 R2V session |

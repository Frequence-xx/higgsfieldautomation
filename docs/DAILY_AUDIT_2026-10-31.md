# Daily Audit — 2026-10-31

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-10-30 | Operator 3.64/5.0 · Skills 99.8% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-10-30 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **3.65 / 5.0** | ↑ +0.01 | ↓ −0.20 |
| Skill Library & Policy | **99.8%** (159.75/160) | → 0.00% | ↑ +8.3% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Active window. Four study cycles (SC392–SC395) landed after the Oct 30 audit.** SC392: Wan 2.6 I2V price CORRECTED from $0.65/5s to $0.525/5s (I2V 720p = $0.105/sec — AIMLAPI model page; prior $0.13/sec was T2V rate); Kling v4 API status nuanced (Kling's own developer page says "preview purposes only" — canary mandatory). SC393: PySceneDetect v0.7.2 documented — detector defaults changed for histogram/hash (detect-content pipeline command UNCHANGED), scenedetect-core package yanked (install path unchanged). SC394: Z-Image Turbo CONFIRMED on AIMLAPI — cheapest T2I at $0.007/img at 9:16, 6× below NB2 Lite; T2I only, not character shots; canary required. SC395: **Kling v4 pricing CONFIRMED from AIMLAPI model pages** — 720p $0.785/5s, 1080p $1.175/5s. v4 is MORE EXPENSIVE than v3 Pro ($0.728/5s). v3 Pro remains production default. v4 Video Edit model string added (`kling-video/v4/video-to-video/edit`). All 4 SCs have clean DB log pairs (4/4 = 100%). Running tally: ~45/68 ≈ 66% (↑ from 64%).

**Kling v4 pricing confirmed (SC395): v4 720p = $0.785/5s (7.8% above v3 Pro), v4 1080p = $1.175/5s (61% above v3 Pro).** The $0.06 placeholder that would have caused 13× budget underestimation is removed. v3 Pro at $0.728/5s remains the correct production default.

**Wan 2.6 I2V price corrected (SC392): $0.65/5s → $0.525/5s.** Prior rate was the T2V rate, not I2V. All budget tables updated.

**SC395 modified generation-video.md without fixing the O3 $1.46 contradiction.** The file was IN HAND; the O3 comparison tables (lines ~703, ~745-746) still reference the deprecated $1.46 pricing. Now day 72. This is the sharpest discipline signal in the window.

**Day 201 without approved creative output.**

CLAUDE.md P0 freeze continues — day 49. O3 contradiction in generation-video.md — day 72 (SC395 touched the file without fixing it).

---

## CHANGES SINCE 2026-10-30 AUDIT

**8 commits — 4 study cycles (SC392–SC395) with 4 clean DB log pairs.**

| SC | Date | Skill Updated | Net Content |
|----|------|---------------|-------------|
| SC392 | Oct 30 | credit-efficiency.md | Wan 2.6 I2V price CORRECTED: $0.105/sec I2V 720p (was $0.13/sec — that was T2V; AIMLAPI model page); Kling v4 developer API status nuanced: Kling's own pricing page says "preview purposes only" / "not yet available" — canary AND API readiness both uncertain; LTX-2.5 and Seedance 2.5 confirmed still absent from AIMLAPI |
| SC393 | Oct 30 | post-production.md | PySceneDetect v0.7.2 (~Oct 12 2026): HistogramDetector/HashDetector defaults changed (detect-content UNCHANGED); scenedetect-core package yanked from PyPI (headless install unchanged); fade-out < 0.1s now ignored by detect-threshold; save-keyframes command added (not needed); FFmpeg 9.1 branch confirmed Oct 23 on Phoronix but not tagged/released; SVT-AV1 still v4.2.0 |
| SC394 | Oct 30 | generation-image.md | **Z-Image Turbo CONFIRMED ON AIMLAPI** — dedicated product page; pricing $0.0065/MP (~$0.007/img at 9:16); cheapest T2I on AIMLAPI (6× below NB2 Lite); T2I ONLY, no I2I; NOT for character shots; LoRA variant also on AIMLAPI; Decision Flow updated; model string CANARY REQUIRED; MAI-Image 2.6 still NOT on AIMLAPI (confirmed Oct 30) |
| SC395 | Oct 31 | generation-video.md | **Kling v4 pricing CONFIRMED from AIMLAPI model pages**: 720p $0.157/sec ($0.785/5s), 1080p $0.235/sec ($1.175/5s) — v4 MORE EXPENSIVE than v3 Pro ($0.728/5s); v3 Pro remains production default; v4 Video Edit model string added (`kling-video/v4/video-to-video/edit`); Reference-to-Video: 10 refs + 7 elements confirmed; v4 section expanded with cost/5s column |

**DB compliance this window: 4/4 (100%). Running tally: ~45/68 ≈ 66% (↑ from 64%).**

**CLAUDE.md: ZERO changes since Oct 20.** All P0 items persist — now day 49.

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 3.55/5.0 (↓ −0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC395: v4 pricing confirmed AND correctly interpreted: "v4 is MORE EXPENSIVE than v3 Pro — v3 Pro remains production default" | Removes misleading $0.06 placeholder; routing verdict stated without hedging | ✅ |
| SC392: Wan 2.6 I2V price corrected by identifying ROOT CAUSE: "prior $0.13/sec was T2V rate, not I2V" | Correct causal reasoning — not just a number change, identifies why the error existed | ✅ |
| SC392: Kling v4 API status correctly nuanced: AIMLAPI docs vs Kling's own developer page ("preview purposes only") | Appropriate skepticism of reseller claims; canary AND API readiness both flagged | ✅ |
| SC394: Z-Image Turbo correctly positioned as B-roll T2I only, NOT character shots, canary behind production gate | Model capability limits correctly identified and documented | ✅ |
| SC393: PySceneDetect v0.7.2 — correctly identifies detector default changes that do NOT affect our detect-content command | Saves unnecessary pipeline audit work; no false alarm | ✅ |
| **SC395 modified generation-video.md without fixing O3 $1.46 contradiction** | File was in hand; O3 comparison tables at lines ~703, ~745-746 still reference deprecated price; now day 72. This is the clearest possible discipline signal — it went past the broken section and updated adjacent content. | ❌ DISCIPLINE |
| **CLAUDE.md P0 freeze: day 49** | Zero action | ❌ DISCIPLINE |

**Score: 3.55/5.0** (↓ −0.05 — SC395 correctly confirmed v4 pricing but passed over the O3 contradiction in the same file. The proximity makes this a sharper reasoning failure than simply skipping an unrelated file.)

---

### D2 — Execution Accuracy (20%) → 3.70/5.0 (↓ −0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| 4/4 DB clean pairs | SC392–SC395 all log correctly | ✅ |
| SC395: v4 pricing table updated, v4 Video Edit row added, CANARY CHECKLIST updated | Comprehensive v4 section update; no partial updates | ✅ |
| SC392: Wan 2.6 I2V price corrected in TWO places (table row + note) | Consistent multi-location update | ✅ |
| SC394: Z-Image Turbo added to model matrix table AND Decision Flow in generation-image.md | Skill file and decision flow updated together | ✅ |
| SC393: Post-production.md received scenedetect v0.7.2 upgrade command + pipeline-action note | Actionable command delivered in the skill file | ✅ |
| **SC395 modified generation-video.md — O3 section not fixed** | File touched, contradiction passed over | ❌ DISCIPLINE |
| **CLAUDE.md P0: day 49** | | ❌ DISCIPLINE |

**Score: 3.70/5.0** (↓ −0.05 — Execution quality is consistent on the new content; SC395 modifying the file without fixing the O3 section is a worse signal than not touching it.)

---

### D3 — Memory & Continuity (15%) → 3.70/5.0 (→ 0.00)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC392: Historical pricing note preserved: "prior $0.13/sec was T2V rate, not I2V" — reason for correction documented | Longitudinal context maintained; reader can understand why the number changed | ✅ |
| SC395: Old $0.06 placeholder removed with source noted (AIMLAPI model page SC395 Oct 31 2026) | Correct sourced replacement; history of the placeholder acknowledged in canary checklist update | ✅ |
| SC392: LTX-2.5 and Seedance 2.5 NOT on AIMLAPI — monitoring items tracked and reconfirmed | Continuous negative-confirmation tracking | ✅ |
| SC394: MAI-Image 2.6 still NOT on AIMLAPI reconfirmed (tracked from SC387) | Long-running monitoring item maintained | ✅ |
| SC393: FFmpeg 9.1 status updated — branch confirmed Oct 23 (Phoronix) but not tagged/released; SVT-AV1 v4.2.0 | Longitudinal tool version tracking | ✅ |
| **O3 contradiction: day 72** | | ❌ DISCIPLINE |

**Score: 3.70/5.0** (→ unchanged — Pricing history preservation (SC392, SC395) and long-running monitoring items (SC392, SC394) are strong continuity signals; no regression.)

---

### D4 — Reliability (20%) → 3.50/5.0 (↑ +0.10)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC395: Removes $0.06 v4 placeholder — prevents 13× budget underestimation if v4 was used | **Highest-value reliability fix this window** — the placeholder would cause catastrophic budget overrun on any v4 call | ✅ |
| SC392: Wan 2.6 I2V price corrected — prevents ~24% budget underestimation on fallback path | Corrects a routing cost error that would silently inflate actual vs predicted costs | ✅ |
| SC392: Kling v4 API "preview purposes only" caveat added — prevents production calls to an unready API | Prevents wasted credits on an API that may return errors | ✅ |
| SC393: PySceneDetect v0.7.2 scenedetect-core yanked — documents correct install path to prevent install failure | Catches a dependency removal before it affects any pipeline setup | ✅ |
| DB compliance: 4/4 this window (100%); running tally: ~45/68 ≈ 66% (↑ from 64%) | Improving trend | ✅ |
| **CLAUDE.md P0 freeze: day 49** | | ❌ DISCIPLINE |
| **O3 contradiction: day 72, file touched** | | ❌ DISCIPLINE |

**Score: 3.50/5.0** (↑ +0.10 — SC395 removing the $0.06 v4 placeholder is the highest single reliability gain in recent windows; SC392 Wan 2.6 I2V correction closes a budget accuracy gap; DB tally continues improving.)

---

### D5 — Integration (15%) → 3.80/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC395: v4 Video Edit model string added (`kling-video/v4/video-to-video/edit`) — previously undocumented | New integration path available in skill file | ✅ |
| SC395: Cost/5s column added to v4 model table — routing cost data now directly comparable | Integration-ready cost data format | ✅ |
| SC392: Wan 2.6 I2V budget table updated to $0.525/5s — routing cost data correct | Direct cost routing accuracy improved | ✅ |
| SC394: Z-Image Turbo integration context: product page confirmed, pricing formula ($0.0065/MP), Decision Flow updated | Pre-canary integration framing complete | ✅ |
| SC393: PySceneDetect upgrade command provided (`pip install --upgrade scenedetect-headless`) | Integration action directly executable | ✅ |

**Score: 3.80/5.0** (↑ +0.05 — v4 Video Edit model string is a new integration deliverable; SC392 corrected routing cost data improves budget accuracy.)

---

### D6 — Social / Communication (10%) → 3.75/5.0 (→ 0.00)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC395: "v4 is MORE EXPENSIVE than v3 Pro — v3 Pro remains the production default for all standard shots" — commit message line 2 | Unambiguous routing verdict; owner can act on this sentence alone | ✅ |
| SC392: "Canary is mandatory AND the official API may not be live yet" — correct escalation of Kling v4 API uncertainty | Not over-confident; two-part warning (canary + API readiness) is the complete picture | ✅ |
| SC394: "cheapest T2I confirmed on AIMLAPI (6× below NB2 Lite $0.044)" — concrete comparative framing | Actionable comparison; not just a price but a relative positioning | ✅ |
| SC393: "Pipeline action: pip install --upgrade scenedetect-headless" — direct | Command-ready; no ambiguity | ✅ |

**Score: 3.75/5.0** (→ unchanged — Consistent quality; SC395 routing verdict and SC392 dual-caveat are the strongest communication deliverables.)

---

### AUDIT 1 SUMMARY

| Dimension | Weight | Score | Contribution |
|-----------|--------|-------|-------------|
| D1 Reasoning | 20% | 3.55 | 0.710 |
| D2 Execution | 20% | 3.70 | 0.740 |
| D3 Memory | 15% | 3.70 | 0.555 |
| D4 Reliability | 20% | 3.50 | 0.700 |
| D5 Integration | 15% | 3.80 | 0.570 |
| D6 Social | 10% | 3.75 | 0.375 |
| **TOTAL** | | | **3.65/5.0** |

**Failure summary:**
- DISCIPLINE (dominant): O3 $1.46 contradiction in generation-video.md day 72 (file touched by SC395 without fixing it); CLAUDE.md P0 freeze day 49; pre-gen check wording day 117

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

### Skills Assessed This Window (SC392–SC395)

**credit-efficiency.md (SC392)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: Wan 2.6 I2V corrected in table AND footnote; "Kling's own pricing page says preview purposes only" caveat added ✅
4. RFC 2119: Canary requirements maintained; "NOT live yet" note appropriately imperative ✅
5. Approval gates: v4 canary required with API readiness caveat ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: Wan 2.6 I2V $0.525/5s consistent with AIMLAPI model page source; no CLAUDE.md routing conflict ✅

**Score: 8/8 (100%)** — Pricing correction with root-cause note and v4 API status nuance are both production-safety improvements.

---

**post-production.md (SC393)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: detect-content command confirmed unchanged; "Pipeline action: pip install --upgrade scenedetect-headless" provided ✅
4. RFC 2119: "Pipeline action:" language is imperative ✅
5. Approval gates: Upgrade is non-destructive; no new gated actions ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: v0.7.2 changelog consistent with FFmpeg 9.x notes; no CLAUDE.md conflict ✅

**Score: 8/8 (100%)** — Proactive documentation of detector default changes and correct install path prevents false pipeline audits.

---

**generation-image.md (SC394)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: "T2I ONLY — no I2I" and "NOT for character shots" both explicit; canary gates clear ✅
4. RFC 2119: "CANARY REQUIRED" maintained throughout; capability boundaries explicit ✅
5. Approval gates: Z-Image Turbo staged behind model-string canary; Decision Flow updated to reflect pre-canary status ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: AIMLAPI-only policy respected; pricing formula ($0.0065/MP) documented with source; no routing matrix conflict ✅

**Score: 8/8 (100%)** — Z-Image Turbo confirmation with correct model positioning is a clean addition.

---

**generation-video.md (SC395)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: v4 pricing confirmed; v3 Pro as production default made explicit ✅
4. RFC 2119: "CRITICAL: No generate_audio parameter" / "strip immediately" — imperative ✅
5. Approval gates: v4 canary required ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: **⚠️ PARTIAL** — v4 section updated correctly; BUT O3 comparison table (~lines 703, 745-746) still references v3 Pro at $1.46. File touched; contradiction not fixed. Pre-existing -0.75 deduction maintained.

**Score: 7.25/8 (−0.75 pre-existing O3 deduction, unchanged)**

---

### Cross-Skill Consistency

| Check | Status |
|-------|--------|
| Wan 2.6 I2V $0.525/5s: credit-efficiency.md vs CLAUDE.md (routing matrix lists Wan 2.6 I2V as fallback, no pricing) | ✅ No conflict |
| Kling v4 $0.785/5s 720p: generation-video.md vs CLAUDE.md routing matrix (CLAUDE.md still outdated — P0 issue already captured) | ✅ No new conflict created |
| Z-Image Turbo: generation-image.md vs CLAUDE.md routing matrix (not in CLAUDE.md — additive) | ✅ No conflict |
| PySceneDetect v0.7.2: post-production.md vs no other skill reference | ✅ No conflict |
| v4 Video Edit model string: generation-video.md (new) vs credit-efficiency.md (not listed — additive) | ✅ No conflict |

**Cross-skill deductions: 0 (no mismatches this window)**

### CLAUDE.md Audit

| Component | Present | Status |
|-----------|---------|--------|
| Instruction count vs 150 limit | ~95 instructions | ✅ |
| Three-agent pattern | ✅ PLANNER/GENERATOR/EVALUATOR | ✅ |
| Snorkel triage | ✅ ZERO/3-5 taxonomy | ✅ |
| Model routing matrix | ✅ Present | ⚠️ Pricing errors persist — P0, day 49 |
| Brand binary checklist | ✅ All 6 items | ✅ |
| Production gates | ✅ All 10 | ⚠️ Pre-gen check #5/#7 wording — day 117 |

**CLAUDE.md deduction: −0.5 (unchanged — P0 items not fixed)**

### Hindsight / Memory Status

- `data/pipeline.db`: 221 rows total; 68 tracked study cycles; DB compliance 66% (↑ from 64% per Oct 30 audit)
- Feedback catalog: Current (pattern-extractor.py runs Sundays)
- Skill memory banks: credit-efficiency, post-production, generation-image, generation-video all updated Oct 30-31

### Gap Analysis

| Gap | Severity | Days Open |
|----|---------|-----------|
| **O3 $1.46 contradiction in generation-video.md** — SC395 modified file WITHOUT fixing it | 🔴 CRITICAL | 72 — ESCALATED (file was touched) |
| Kling v4 canary: audio strip verification, face adherence vs v3 Pro baseline, billing confirm ($0.785/5s → actual invoice), API readiness (Kling dev page "preview purposes only") | 🔴 CRITICAL | 8 |
| Wan 2.7 R2V canary on AIMLAPI — CONFIRMED LIVE ($0.65/5s); model string, binding syntax, param schema | 🔴 CRITICAL | 2 (from SC391) |
| Z-Image Turbo canary on AIMLAPI — CONFIRMED ON AIMLAPI; model string + aspect_ratio + quality baseline | 🔴 CRITICAL | NEW (SC394 — cheapest T2I path, canary is now urgent) |
| CLAUDE.md pricing errors (P0) | 🟠 HIGH | 49 |
| ElevenLabs v4 Dutch canary — cost barrier removed (SC390) | 🟠 HIGH | 5 |
| FaceFusion v3.9.2 CRITICAL upgrade — NVIDIA driver fatal crash on v3.9.1 | 🟠 HIGH | 2 (from SC391) |
| NB2.1 production canary — thinking_level, per-image billing at 1K/2K | 🟡 MEDIUM | 5 |
| Kling O3 canary on AIMLAPI | 🟡 MEDIUM | 72 |
| CLAUDE.md pre-gen check #5/#7 wording | 🟡 MEDIUM | 117 |
| Remotion v5.0 license tier verification (Farouq) | 🟡 MEDIUM | 2 |
| Kling v4 prompt length: 8k tokens vs 2500 chars AIMLAPI | 🟡 MEDIUM | 2 |

### Skill Score Calculation

| Category | Passes | Possible | Notes |
|----------|--------|----------|-------|
| Core skills (18 files × 8 criteria) | 143.25 | 144 | −0.75 pre-existing (O3 contradiction in generation-video.md — SC395 touched file without fixing) |
| CLAUDE.md structural components | 5.5 | 6 | −0.5 for pricing P0 (unchanged) |
| Cross-skill consistency | 11 | 11 | No mismatches this window |
| **TOTAL** | **159.75** | **160** | **99.8%** |

**Target ≥95%: PASS → unchanged**

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved output:** V2-Proces (2026-04-12)
**Days since last approval:** **201 days**
**Output produced since Oct 30 audit:** None

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

1. **Day 201. The routing decision is now as clear as it will ever be.** v4 pricing confirmed today (SC395): v3 Pro is cheaper AND has more ghost-driving controls. The cheapest B-roll still image path is now confirmed (SC394: Z-Image Turbo $0.007/img). A CD reviewing today's SCs would say: you've removed the last knowledge gap blocking a production brief. The only remaining gaps are canaries — and canaries are run IN production, not before it. The obstacle to starting is not knowledge.

2. **SC395 went INTO generation-video.md and came out without fixing the O3 $1.46 contradiction.** A CD would not read this as forgetfulness. At 72 days, this is a systemic behavior: the study cycle engine is optimized for adding new facts, not correcting old ones. The correction takes 2 minutes. It has been 72 days.

3. **Four CRITICAL canaries are open simultaneously.** Wan 2.7 R2V, Kling v4 audio/billing, Z-Image Turbo model string, and the O3 section fix all sit at CRITICAL. A CD would not run four separate research sessions. They would book one 30-minute canary session: one Z-Image Turbo call ($0.007), one v4 I2V call ($0.785), one Wan 2.7 R2V call ($0.65). Total canary cost: $1.44. Under the $15/video ceiling by 90%. The canaries ARE the production brief.

### Model Capability Notes (New Since Oct 30)

- **Kling v4 pricing confirmed (SC395)** — $0.785/5s at 720p, $1.175/5s at 1080p. v4 more expensive than v3 Pro ($0.728). v3 Pro confirmed as production default. Classification: **INTEGRATION** — pricing is now known; remaining gaps are audio behavior and face adherence canary.
- **Wan 2.6 I2V price corrected (SC392)** — $0.525/5s (not $0.65). Budget accuracy classification: **OPERATIONAL** — incorrect data in skill file; now corrected.
- **Z-Image Turbo AIMLAPI confirmed (SC394)** — cheapest T2I at $0.007/img. Classification: **INTEGRATION** — model string and aspect_ratio param unverified; canary determines production viability.

### Cost Metric

Credits per APPROVED video: **MATHEMATICALLY UNDEFINED** (0 approved videos since April 12, 2026)

### Predicted Pass Rate

**~73% confidence, 70% predicted pass rate** (→ unchanged)

- Upside: SC395 confirms v3 Pro routing is correct and cheaper than v4; Z-Image Turbo reduces B-roll cost if canary passes; Wan 2.7 R2V confirmed live at 2.2× cheaper than Kling O1
- Downside: Four open CRITICAL canaries; FaceFusion CRITICAL fix not applied; ElevenLabs v4 Dutch canary pending; 201-day production gap; O3 contradiction in active skill file

CREATIVE_AUDIT_COMPLETE

---

## TOP ACTION ITEMS (Prioritized)

| # | Priority | Action | Deadline |
|---|----------|--------|---------|
| 1 | 🔴 CRITICAL | **Fix O3 $1.46 contradiction in generation-video.md** — lines ~703, ~745-746 still reference deprecated v3 Pro pricing. SC395 modified the same file today without fixing it. Day 72. 2-minute edit. | Immediate |
| 2 | 🔴 CRITICAL | **Run Z-Image Turbo canary on AIMLAPI.** Confirmed on AIMLAPI product page (SC394). Canary: (a) model string (`alibaba/z-image-turbo` expected — unconfirmed), (b) aspect_ratio param name on AIMLAPI proxy, (c) actual per-image cost at 9:16, (d) quality baseline vs NB2 Lite. Cost: ~$0.007 per test image. | Next session |
| 3 | 🔴 CRITICAL | **Run Kling v4 full canary.** Confirm: (a) audio behavior — strip `ffmpeg -i input.mp4 -an -c:v copy output_silent.mp4` and verify no audio pass-through; (b) billing confirm ($0.785/5s 720p → actual invoice); (c) face adherence vs v3 Pro Subject Binding baseline; (d) API availability (Kling dev page says "preview purposes only"). | Next session |
| 4 | 🔴 CRITICAL | **Run Wan 2.7 R2V canary on AIMLAPI.** Confirmed live ($0.65/5s). Test: `image_urls: [hero_frame]`, `aspect_ratio: "9:16"`, `duration: 5`, `audio_mode: "mute"`. Run InsightFace cosine vs v3 Pro baseline. If PASS ≥ 0.62: update routing matrix — 2.2× cost reduction on B-roll character shots. | Next session |
| 5 | 🟠 HIGH | **Fix CLAUDE.md pricing errors (P0)** — v3 Pro $1.46→$0.728; v3 Standard $1.09→$0.546; Wan 2.6 I2V fallback. Acknowledged 5-min edit, day 49. | Immediate |
| 6 | 🟠 HIGH | **Upgrade FaceFusion to v3.9.2** — CRITICAL NVIDIA driver fatal crash on v3.9.1. `git checkout 3.9.2` in facefusion dir before ANY FaceFusion run. | Before next FaceFusion run |

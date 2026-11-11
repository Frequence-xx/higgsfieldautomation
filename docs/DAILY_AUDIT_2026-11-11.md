# Daily Audit — 2026-11-11

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-11-10 | Operator 3.87/5.0 · Skills 99.2% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-11-10 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **3.90 / 5.0** | ↑ +0.03 | ↑ +0.05 |
| Skill Library & Policy | **99.2%** (158.75/160) | → 0.00 | ↑ +7.7% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Active window. Three study cycles (SC433–SC435) since Nov 10 audit.** Highlights: SC433 adds Keyframe-Anchored Identity Preservation (arXiv 2607.17985) validating defined-endpoint policy; SC434 confirms Gemini Omni 1.2 Flash aspect_ratio as snake_case and finds MiniMax H3 Highspeed + H3 Lite on AIMLAPI (H3 Lite CANARY PRIORITY HIGH — cheapest B-roll candidate at $0.025/sec); SC435 updates post-production.md for Remotion v4.0.542, **closing the Day 1 Remotion version drift gap**.

**DB compliance this window: 3/3 (100%) — fourth consecutive full-compliance window.**
**Running DB tally: ~73/100 = 73.0% (↑ from 70.0%). Third consecutive above-70% window.**

**Day 84: O3 $1.46 contradiction in generation-video.md not fixed.**
**Day 61: CLAUDE.md P0 pricing errors not fixed.**
**Day 3: CLAUDE.md routing matrix lists retired Veo 3.1 Lite model (P0).**
**Day 212: No approved creative output.**

---

## CHANGES SINCE 2026-11-10 AUDIT

**6 commits — 3 study cycles (SC433–SC435), DB compliance 3/3 (100%) this window.**

| SC | Date | File(s) Updated | Net Content |
|----|------|-----------------|-------------|
| SC433 | Nov 10 | character-consistency.md | Keyframe-Anchored Identity Preservation (arXiv 2607.17985) added to Future Watch section. 3rd-place Track 2 at ACM MM 2026 IPVG Challenge (official results pending Nov 14). Three key findings: (1) terminal-state endpoint prompts = identity preservation technique — **validates CLAUDE.md defined-endpoint policy**; (2) multi-reference guidance is single strongest lever for consistency — first retry action: add more refs BEFORE changing prompts; (3) FaceFusion v3.9.2 + InsightFace v2.1 confirmed unchanged. Chronos check deferred to Nov 15. **Has DB log commit ✅** |
| SC434 | Nov 10 | credit-efficiency.md | (1) Gemini Omni 1.2 Flash `aspect_ratio` CONFIRMED snake_case from Google native API, Krea, fal.ai — resolves CANARY uncertainty. Default "16:9", target `"9:16"`. (2) MiniMax H3 Highspeed CONFIRMED ON AIMLAPI: $0.04/sec · 5s=$0.20, 768p, first/last frame, audio always ON — strip required. CANARY required. (3) MiniMax H3 Lite CONFIRMED ON AIMLAPI: $0.025/sec · 5s=$0.125, 480p/768p, 4–15s, first/last frame, audio always ON. **CANARY PRIORITY HIGH**: 40% cheaper than Hailuo 2.3 Fast ($0.0416→$0.025/sec). Non-char routing section updated. **Has DB log commit ✅** |
| SC435 | Nov 11 | post-production.md | (1) Remotion v4.0.542: magnify() — HIGH relevance for brand callouts (truck logo, box text, phone number); lightning() — LOW relevance (Snelverhuizen tone). renderMediaOnLambdaAndStream(), --chunks Lambda flag, Studio: OpenTimelineIO + high contrast + inline ChatGPT composer. §11s added. Tool table + checklist updated v4.0.541 → v4.0.542. **Closes Day 1 version drift vs captions-and-titles.md ✅** (2) FFmpeg 9.1 still NOT released — SC435 added to §3e confirmation list. All tools confirmed unchanged. **Has DB log commit ✅** |

**Gaps closed this window:** Remotion version drift (post-production.md v4.0.541 vs captions-and-titles.md v4.0.542) — CLOSED by SC435. Gemini Omni 1.2 Flash aspect_ratio CANARY uncertainty — RESOLVED by SC434.

**Gaps opened this window:** MiniMax H3 Highspeed canary (9:16, actual billing, audio strip), MiniMax H3 Lite canary (PRIORITY HIGH), ACM MM 2026 Chronos check (after Nov 14).

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 3.85/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC433: "Terminal-state endpoint prompts = identity preservation technique, not just motion quality. Validates CLAUDE.md defined-endpoint policy." — research explicitly linked to policy | Evidence-to-policy bridging ✅ |
| SC433: "Multi-reference guidance at inference time is single strongest lever for identity consistency — adding refs outperforms stronger model variants with 1 ref." | Actionable research synthesis ✅ |
| SC434: Gemini Omni 1.2 Flash aspect_ratio confirmed from THREE independent sources (Google native API, Krea, fal.ai) before marking resolved | Multi-source triangulation ✅ |
| SC434: "AIMLAPI oddly cheaper" than MiniMax native — anomaly noticed and flagged for CANARY | Epistemic rigor ✅ |
| SC434: "40% cheaper than Hailuo 2.3 Fast ($0.0416/sec → $0.025/sec)" — quantified cost savings | Quantified reasoning ✅ |
| SC435: post-production.md magnify() rated "HIGH relevance for brand callouts"; lightning() rated "LOW relevance for Snelverhuizen brand tone" — relevance differentiated | Use-case scoping ✅ |
| **O3 $1.46 contradiction in generation-video.md** — Day 84 | ❌ DISCIPLINE |
| **CLAUDE.md P0 pricing freeze** — v3 Pro $1.46→$0.728; v3 Standard $1.09→$0.546 — Day 61 | ❌ DISCIPLINE |
| **CLAUDE.md routing matrix — Veo 3.1 Lite still listed** — Day 3 | ❌ DISCIPLINE |

**Score: 3.85/5.0** (↑ +0.05 — SC433 research-to-policy bridging and SC434 three-source triangulation are high-quality reasoning signals; persistent DISCIPLINE failures cap the score)

---

### D2 — Execution Accuracy (20%) → 3.85/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC435: post-production.md updated for Remotion v4.0.542 — **closes version drift gap from Day 1** | Gap closed same-window ✅ |
| SC434: Non-char routing section updated in credit-efficiency.md alongside Hailuo note | Targeted, minimal-change update ✅ |
| DB compliance 3/3 (100%) this window — fourth consecutive full-compliance window | ✅ Strong continuation |
| SC433: FaceFusion v3.9.2 + InsightFace v2.1 confirmed unchanged — no spurious update | Accurate null update ✅ |
| CLAUDE.md NOT updated for Veo 3.1 Lite retirement (Day 3) | ❌ DISCIPLINE |
| **O3 $1.46 — generation-video.md — Day 84** | ❌ DISCIPLINE |
| CLAUDE.md pricing errors (Day 61) | ❌ DISCIPLINE |

**Score: 3.85/5.0** (↑ +0.05 — SC435 closes the Remotion version drift gap within the window it was opened; fourth consecutive 100% DB compliance window)

---

### D3 — Memory & Continuity (15%) → 3.95/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC433: "KeyID (arXiv 2608.16154) already documented from SC310" — multi-month recall (SC310 → SC433 = 123 cycles ago) | Deep multi-cycle recall ✅ |
| SC433: Explicitly notes "FaceFusion v3.9.2 still current (no v3.9.3 found)" — recalls prior confirmed version | Version-state recall ✅ |
| SC434: "Resolves CANARY uncertainty in API template and param notes" — links resolution to prior open item | CANARY tracking ✅ |
| DB running tally: ~73/100 = 73.0% (↑3pp from 70.0%) — fourth consecutive window above 70% | ✅ Sustained improvement |
| DB compliance: fourth consecutive 100% window | ✅ Established pattern |
| SC408–SC415 + SC419 + SC422 still absent from pipeline.db | ❌ OPERATIONAL (slowly improving) |

**Score: 3.95/5.0** (↑ +0.05 — SC433 KeyID recall from 123 cycles prior is a strong memory signal; DB tally 73% sustained above 70% threshold for second window)

---

### D4 — Reliability (20%) → 3.75/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC433: "First retry action on InsightFace fail: add more reference images BEFORE changing prompts" — operational guidance improves retry reliability | Reliability heuristic ✅ |
| SC434: MiniMax H3 Highspeed + H3 Lite: "Audio always ON — strip required" explicitly flagged twice | Proactive failure prevention ✅ |
| SC435: Remotion v4.0.542 player timing fix documented — users on v4.0.541 may hit caption timing issue | Reliability hazard documented ✅ |
| CLAUDE.md routing matrix still shows retired Veo 3.1 Lite (P0) — Day 3 | ❌ DISCIPLINE |
| **O3 $1.46 — Day 84** | ❌ DISCIPLINE |
| **CLAUDE.md P0 pricing — Day 61** | ❌ DISCIPLINE |

**Score: 3.75/5.0** (→ unchanged — SC433 retry guidance and SC434 audio strip warnings improve reliability; still blocked by three persistent P0 discipline failures)

---

### D5 — Integration (15%) → 4.20/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC435: post-production.md now matches captions-and-titles.md at Remotion v4.0.542 — **cross-skill version drift closed** | Integration gap closed ✅ |
| SC434: Gemini Omni 1.2 Flash aspect_ratio confirmed + non-char routing section updated in same cycle | Parameter resolution + routing update in one pass ✅ |
| SC434: Hailuo 2.3 Fast note updated to reflect H3 Lite pending — forward reference maintained | Routing section cohesion ✅ |
| SC433: character-consistency.md Future Watch updated; no cross-skill contradiction introduced | Clean isolated update ✅ |
| credit-efficiency.md Kling v3 Pro $0.728/5s vs CLAUDE.md routing matrix $1.46 | ❌ PERSISTS — P0 Day 61 |

**Score: 4.20/5.0** (↑ +0.05 — post-production.md Remotion drift closed; Gemini Omni param confirmed and integrated into routing; overall cross-skill coherence improved)

---

### D6 — Social / Communication (10%) → 3.90/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC434: "CANARY PRIORITY HIGH: if 9:16 and quality pass at 720p+, H3 Lite becomes new cheapest non-character B-roll — 40% cheaper than Hailuo 2.3 Fast ($0.0416/sec → $0.025/sec)" | Priority-ranked, quantified ✅ |
| SC433: "check github.com/wenc-k/Chronos after Nov 14 for official Track 1+2 results" — specific follow-up date | Actionable deferred tracking ✅ |
| SC434: "AIMLAPI oddly cheaper" — anomaly explicitly surfaced | Anomaly flagging ✅ |
| SC435: "HIGH relevance for brand callouts" vs "LOW relevance for Snelverhuizen brand tone" | Relevance differentiated clearly ✅ |

**Score: 3.90/5.0** (→ unchanged — solid communication quality; no regression)

---

### AUDIT 1 SUMMARY

| Dimension | Weight | Score | Contribution |
|-----------|--------|-------|-------------|
| D1 Reasoning | 20% | 3.85 | 0.770 |
| D2 Execution | 20% | 3.85 | 0.770 |
| D3 Memory | 15% | 3.95 | 0.593 |
| D4 Reliability | 20% | 3.75 | 0.750 |
| D5 Integration | 15% | 4.20 | 0.630 |
| D6 Social | 10% | 3.90 | 0.390 |
| **TOTAL** | | | **3.90/5.0** |

**Failure summary:**
- DISCIPLINE (dominant): O3 $1.46 contradiction Day 84; CLAUDE.md P0 pricing Day 61; CLAUDE.md Veo 3.1 Lite routing Day 3
- OPERATIONAL: SC408–SC415 + SC419 + SC422 absent from data/pipeline.db; running tally ~73%

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

### Skills Assessed This Window (SC433–SC435)

**character-consistency.md (SC433)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: Keyframe-Anchored Identity Preservation findings explicitly scoped to Future Watch (not production use); retry guidance ("add more refs BEFORE changing prompts") is explicit operational default ✅
4. RFC 2119: prior audit confirmed ✅
5. Approval gates: prior audit confirmed ✅
6. Length: targeted addition (Future Watch section) ✅
7. Negative triggers: prior audit confirmed ✅
8. Consistency: validates CLAUDE.md defined-endpoint policy (terminal-state endpoints = identity preservation); no contradiction ✅

**Score: 8/8 (100%)**

---

**credit-efficiency.md (SC434)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: Gemini Omni 1.2 Flash aspect_ratio default explicitly stated ("16:9"); H3 Lite audio strip "required" ✅
4. RFC 2119: prior audit confirmed ✅
5. Approval gates: prior audit confirmed ✅
6. Length: three targeted insertions ✅
7. Negative triggers: prior audit confirmed ✅
8. Consistency: MiniMax H3 Lite at $0.025/sec pending CANARY — not yet added to routing tables as confirmed option; CANARY required before CLAUDE.md update ✅

**Score: 8/8 (100%)**

---

**post-production.md (SC435)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: magnify() rated HIGH relevance; lightning() rated LOW relevance with specific constraint ("≤8 frame interstitial"); npm install updated to v4.0.542 ✅
4. RFC 2119: prior audit confirmed ✅
5. Approval gates: prior audit confirmed ✅
6. Length: targeted insertions (§11s, tool table, checklist line) ✅
7. Negative triggers: prior audit confirmed ✅
8. Consistency: post-production.md now at v4.0.542, matching captions-and-titles.md — **Remotion drift gap closed** ✅

**Score: 8/8 (100%)**

---

### Cross-Skill Consistency

| Check | Status |
|-------|--------|
| post-production.md Remotion v4.0.541 vs captions-and-titles.md v4.0.542 | ✅ **CLOSED** (SC435 — was Day 1 drift) |
| captions-and-titles.md ElevenLabs v2.77.0 vs halal-audio.md v2.77.0 | ✅ CONSISTENT |
| credit-efficiency.md Gemini Omni 1.2 Flash aspect_ratio snake_case (SC434) | ✅ RESOLVED (was CANARY) |
| credit-efficiency.md Kling v3 Pro $0.728/5s vs CLAUDE.md routing matrix $1.46 | ❌ PERSISTS — P0 Day 61 |
| CLAUDE.md routing matrix Veo 3.1 Lite vs credit-efficiency.md Gemini Omni 1.2 Flash | ❌ PERSISTS — P0 Day 3 |
| character-consistency.md "add more refs BEFORE changing prompts" (SC433) vs CLAUDE.md 3-retry limit | ✅ No contradiction — CLAUDE.md limits retries per clip; SC433 guidance is per-attempt action |

### CLAUDE.md Audit

| Component | Present | Status |
|-----------|---------|--------|
| Instruction count vs 150 limit | ~100 instructions | ✅ |
| Three-agent pattern | ✅ PLANNER/GENERATOR/EVALUATOR | ✅ |
| Snorkel triage | ✅ ZERO/3-5 taxonomy | ✅ |
| Model routing matrix | ✅ Present | ❌ **Two distinct P0 errors:** pricing (Day 61) + Veo 3.1 Lite retired (Day 3) |
| Brand binary checklist | ✅ All 6 items | ✅ |
| Production gates | ✅ All 10 | ⚠️ Pre-gen check #5/#7 wording — Day 126 |

**CLAUDE.md deduction: −0.75 (unchanged — same two P0 errors as yesterday)**

### Hindsight / Memory Status

- `data/pipeline.db`: study_cycles entries through SC435; SC422 + SC408–SC415 + SC419 absent; running tally ~73/100 = 73.0%
- DB compliance this window: **3/3 (100%)** — fourth consecutive full-compliance window
- Feedback catalog: Current (pattern-extractor.py runs Sundays)
- Skills updated this window: character-consistency.md, credit-efficiency.md, post-production.md

### Gap Analysis

| Gap | Severity | Days Open |
|----|---------|-----------|
| **Veo 3.1 Lite still in CLAUDE.md routing matrix** — retired Oct 22; replace with Gemini Omni 1.2 Flash (aspect_ratio confirmed SC434) | 🔴 CRITICAL | **3** |
| **O3 $1.46 contradiction in generation-video.md** | 🔴 CRITICAL | **84** |
| **SC408–SC415 + SC419 + SC422 absent from data/pipeline.db** | 🔴 CRITICAL | varies |
| Kling v4 canary: audio strip, face adherence, billing | 🔴 CRITICAL | **19** |
| Wan 2.7 R2V canary on AIMLAPI ($0.65/5s) | 🔴 CRITICAL | **13** |
| **CLAUDE.md pricing errors (P0)** — v3 Pro $1.46→$0.728; v3 Standard $1.09→$0.546 | 🟠 HIGH | **61** |
| **MiniMax H3 Lite canary** — 9:16, 720p+ quality, billing (CANARY PRIORITY HIGH — $0.025/sec = cheapest B-roll candidate) | 🟠 HIGH | **1 (NEW)** |
| MiniMax H3 Highspeed canary — 9:16, billing, audio strip | 🟠 HIGH | **1 (NEW)** |
| Kling O3/Omni canary — live API + pricing (docs pages confirmed SC430) | 🟠 HIGH | **2** |
| ElevenLabs v4 Dutch canary | 🟠 HIGH | **16** |
| Luma Uni-1 canary: pricing + face adherence | 🟠 HIGH | **8** |
| GPT Image 2.6 Flare/Sunburst canary — size param (864x1536?), billing | 🟠 HIGH | **4** |
| SC408–SC422 DB gaps retroactive repair | 🟠 HIGH | varies |
| ffmpeg-normalize --verify flag: add to §4a production loudnorm commands (SC432 recommends; not yet in runbook) | 🟡 MEDIUM | **2** |
| Grok Video 1.5 Preview canary (SC413) | 🟡 MEDIUM | **7** |
| NB2.1 production canary | 🟡 MEDIUM | **16** |
| Kling v4 T2V / R2V dual-string active canary (SC423) | 🟡 MEDIUM | **4** |
| CLAUDE.md pre-gen check #5/#7 wording | 🟡 MEDIUM | **126** |
| Remotion v4.0.540 breaking changes in production code | 🟡 MEDIUM | — |
| **ACM MM 2026 (Nov 10-14, Rio) — Chronos check after Nov 14** | 🟡 MEDIUM | **check Nov 15** |

**Closed this window:** Remotion version drift (post-production.md v4.0.541 → v4.0.542). Gemini Omni 1.2 Flash aspect_ratio CANARY.
**Opened this window:** MiniMax H3 Lite canary (PRIORITY HIGH), MiniMax H3 Highspeed canary, ACM MM 2026 Chronos check.

### Skill Score Calculation

| Category | Passes | Possible | Notes |
|----------|--------|----------|-------|
| Core skills (18 files × 8 criteria) | 142.50 | 144 | Pre-existing: −0.75 (O3 in generation-video.md); character-consistency.md, credit-efficiency.md, post-production.md clean 8/8 |
| CLAUDE.md structural components | 5.25 | 6 | −0.75 total (pricing P0 Day 61 + Veo 3.1 Lite routing Day 3) |
| Cross-skill consistency | 11 | 10 | Two contradictions tracked (pricing + routing); Remotion drift CLOSED this window |
| **TOTAL** | **158.75** | **160** | **99.2%** |

**Total: 99.2%** (→ unchanged — no new skill-level deductions; Remotion drift closure does not affect score under current methodology)

**Target ≥95%: PASS**

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved output:** V2-Proces (2026-04-12)
**Days since last approval:** **212 days**
**Output produced since Nov 10 audit:** None

No new clips to score. Scores carry forward from V2-Proces reference.

### Tier 1 — Technical (binary pass/fail)

Based on V2-Proces (last approved video):
- Resolution ≥1080p ✅ | Frame rate 24fps ✅ | Aspect ratio 9:16 ✅
- No corruption ✅ | No watermarks ✅ | Duration correct ✅

**PASS**

### Tier 2 — Visual Quality (1-5, ≥3.5 required)

Carrying forward from V2-Proces: **4.1/5.0** (above threshold)

### Tier 3 — Brand Compliance (1-5, ≥4.0 required)

**4.1/5.0** (above threshold, V2-Proces)

### Tier 4 — Advertising Effectiveness (1-5, ≥3.5 required)

**4.0/5.0** (above threshold)

**Overall Creative Score: 4.07/5.0** (→ unchanged — no new output)

### Ralph Loop

*"What would a senior creative director still reject about this pipeline's creative output?"*

1. **212 days without a single approved video.** The routing matrix has had a retired model (Veo 3.1 Lite) in it for 3 days with a confirmed replacement (Gemini Omni 1.2 Flash, aspect_ratio now confirmed as snake_case by SC434). This is a 5-minute fix. It has not been made. The pipeline cannot safely produce B-roll shots without it.

2. **MiniMax H3 Lite is the most cost-efficient canary available today.** A 5-second test clip costs $0.125 — cheaper than any currently approved B-roll model. SC434 marks it CANARY PRIORITY HIGH. The pipeline is spending more auditing these models than it would cost to run a canary. Six CANARY REQUIRED items have accumulated (H3 Lite, H3 Highspeed, Kling O3/Omni, Kling v4, GPT Image 2.6, Wan 2.7). The first production session will need $5–10 of unplanned canary cost before the first real shot unless these are resolved now.

3. **SC433 confirms multi-reference guidance is the single strongest identity consistency lever.** The pipeline's current character-consistency skill now has this finding documented. But production hasn't started, so the finding cannot be applied. The research quality of this pipeline has outpaced its production output by roughly 200 days.

### Model Capability Notes (New Since Nov 10)

- **MiniMax H3 Lite CONFIRMED ON AIMLAPI (SC434):** $0.025/sec · 5s=$0.125 · 480p/768p · first/last frame · audio always ON. 40% cheaper than Hailuo 2.3 Fast. CANARY PRIORITY HIGH.
- **MiniMax H3 Highspeed CONFIRMED ON AIMLAPI (SC434):** $0.04/sec · 5s=$0.20 · 768p · first/last frame · audio always ON. CANARY required.
- **Gemini Omni 1.2 Flash aspect_ratio RESOLVED (SC434):** snake_case `aspect_ratio: "9:16"` confirmed. Ready for CLAUDE.md routing swap after Veo 3.1 Lite retirement fix.
- **Remotion v4.0.542 magnify() effect (SC435):** HIGH relevance for brand callouts (truck logo, box text, phone number) without regenerating shots.
- **ACM MM 2026 (Nov 10-14, Rio):** Chronos paper results expected after Nov 14. Check github.com/wenc-k/Chronos.

### Cost Metric

Credits per APPROVED video: **MATHEMATICALLY UNDEFINED** (0 approved videos since April 12, 2026)

### Predicted Pass Rate

**~70% confidence, 70% predicted pass rate** (→ unchanged)

**Note:** B-roll routing is still broken (Veo 3.1 Lite retired, CLAUDE.md not updated Day 3). Pass rate will drop if production runs before the three P0 fixes are made. Gemini Omni 1.2 Flash aspect_ratio is now confirmed — CLAUDE.md routing fix is unblocked.

CREATIVE_AUDIT_COMPLETE

---

## TOP ACTION ITEMS (Prioritized)

| # | Priority | Action | Deadline |
|---|----------|--------|---------|
| 1 | 🔴 CRITICAL | **Fix CLAUDE.md routing matrix** — Veo 3.1 Lite RETIRED Oct 22. Replace B-roll/establishing rows with Gemini Omni 1.2 Flash ($0.0695/sec, aspect_ratio snake_case NOW CONFIRMED by SC434). **Day 3. Production broken without this.** | Immediate |
| 2 | 🔴 CRITICAL | **Fix O3 $1.46 contradiction in generation-video.md** — line 703: `\| Final character shot \| v3 Pro \| $1.46 \|` → `$0.728`. **Day 84.** | Immediate |
| 3 | 🟠 HIGH | **Run MiniMax H3 Lite canary** — CANARY PRIORITY HIGH. $0.125/5s clip. 9:16 aspect_ratio, quality at 720p+, audio strip. If passes: cheapest non-character B-roll at $0.025/sec (40% cheaper than Hailuo 2.3 Fast). | Before next production |
| 4 | 🟠 HIGH | **Fix CLAUDE.md pricing errors (P0)** — v3 Pro $1.46→$0.728; v3 Standard $1.09→$0.546. 5-minute edit. **Day 61.** | Immediate |
| 5 | 🔴 CRITICAL | **Run combined canary session** — (a) Kling O3/Omni live API + pricing; (b) Kling v4 I2V audio+face; (c) GPT Image 2.6 Flare size param; (d) Wan 2.7 R2V; (e) Gemini Omni 1.2 Flash billing. Total: ~$3–5. | Before next production |
| 6 | 🟡 MEDIUM | **Add --verify to halal-audio.md §4a loudnorm command** — SC432 recommends; not yet in runbook. **Day 2.** | Next SC |
| 7 | 🟡 MEDIUM | **Check github.com/wenc-k/Chronos after Nov 14** — ACM MM 2026 official Track 1+2 results. | Nov 15 |
| 8 | 🟠 HIGH | **Repair DB gaps** — SC408–SC415 + SC419 + SC422 absent from pipeline.db. Running tally 73.0%. | Next maintenance session |
| 9 | 🔴 CRITICAL | **START PRODUCTION** — 212 days since last approved video. Fix items 1+4 first (10 min), then canary H3 Lite (item 3, $0.125), then produce. | Now |

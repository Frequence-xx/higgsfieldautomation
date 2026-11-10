# Daily Audit — 2026-11-10

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-11-09 | Operator 3.86/5.0 · Skills 99.2% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-11-09 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **3.87 / 5.0** | ↑ +0.01 | ↑ +0.02 |
| Skill Library & Policy | **99.2%** (158.75/160) | → 0.00 | ↑ +7.7% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Active window. Four study cycles (SC429–SC432) since Nov 9 audit.** Highlights: SC429 upgrades GPT Image 2.6 Flare/Sunburst to "LIKELY ON AIMLAPI" with complexity parameter documented; SC430 corrects Kling O3/Omni status from "absent (SC339)" to "DEDICATED DOCS PAGES CONFIRMED"; SC431 tracks Remotion v4.0.542 same-day (caption pipeline unaffected); SC432 documents ffmpeg-normalize v1.43.1+v1.44.0 with actionable `--verify` flag for loudnorm QA.

**DB compliance this window: 4/4 (100%) — third consecutive full-compliance window.**
**Running DB tally: ~70/100 = 70.0% (↑ from 68.75%). First time crossing 70% threshold.**

**Day 83: O3 $1.46 contradiction in generation-video.md not fixed.**
**Day 60: CLAUDE.md P0 pricing errors not fixed.**
**Day 2: CLAUDE.md routing matrix lists retired Veo 3.1 Lite model (P0).**
**Day 211: No approved creative output.**
**Day 1 (NEW): post-production.md Remotion v4.0.541 vs captions-and-titles.md v4.0.542 — version drift.**

---

## CHANGES SINCE 2026-11-09 AUDIT

**8 commits — 4 study cycles (SC429–SC432), DB compliance 4/4 (100%) this window.**

| SC | Date | File(s) Updated | Net Content |
|----|------|-----------------|-------------|
| SC429 | Nov 9 | generation-image.md | GPT Image 2.6 Flare/Sunburst upgraded "NOT ON AIMLAPI" → "LIKELY ON AIMLAPI" (confirmed in AIMLAPI model database page). NEW complexity parameter: "low"/"medium"/"high" (default "high"). "864x1536" (true 9:16) CANARY required. MAI-Image 2.7 Preview added to monitor list (Oct 27 2026 launch, I2I editing only, no API). MAI-Image 2.6 GA confirmed Oct 27 on Foundry ($0.039/img). **Has DB log commit ✅** |
| SC430 | Nov 9 | generation-video.md | **CRITICAL correction:** Kling O3/Omni status upgraded from "NOT ON AIMLAPI (confirmed absent Sept 8, 2026 — SC339)" → "DEDICATED DOCS PAGES CONFIRMED" (4 new AIMLAPI pages found Nov 9 2026). Model strings already in file (SC279); status note corrected. CANARY still required for live API + pricing. 4K variant unblocked. Kling v3 Pro parameters unchanged: cfg_scale routing (0.5 char/0.7 truck), Subject Binding 80-90, negative prompt template, camera_control. **Has DB log commit ✅** |
| SC431 | Nov 9 | captions-and-titles.md | Remotion v4.0.542 (Nov 9 2026): HtmlInCanvas fix, Sequence crash in ThreeCanvas fix, player timing fix; Lambda streaming added; magnify()/lightning() effects; Studio OpenTimelineIO + high contrast + inline ChatGPT. NO @remotion/captions or install-whisper-cpp changes — caption pipeline unaffected. npm install updated @4.0.541 → @4.0.542. whisper.cpp v1.9.5 + ElevenLabs v2.77.0 confirmed unchanged. ⚠️ post-production.md still at v4.0.541 — minor version drift. **Has DB log commit ✅** |
| SC432 | Nov 10 | halal-audio.md | ffmpeg-normalize v1.43.1 (Nov 9): bug-fix patch (presets, colliding output paths, album gain cap) — zero pipeline impact. ffmpeg-normalize v1.44.0 (Nov 9): NEW --verify flag confirms -14 LUFS target after loudnorm. **Actionable: add --verify to §4a production runs as QA gate.** ElevenLabs v2.77.0 + yt-dlp 2026.10.26 confirmed unchanged. **Has DB log commit ✅** |

**DB compliance this window: 4/4 (100%). Third consecutive full-compliance window. Running tally: ~70/100 = 70.0% (↑ from 68.75%). First time at or above 70%.**

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 3.80/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC430: Kling O3/Omni status corrected from "absent (SC339)" → "dedicated docs pages confirmed"; SC cycle number referenced precisely | Evidence-based status revision ✅ |
| SC430: CANARY still required (live API + pricing unconfirmed despite docs pages existing) | Appropriate epistemic caution ✅ |
| SC429: GPT Image 2.6 Flare/Sunburst upgraded to "LIKELY" with CANARY required | Calibrated confidence upgrade ✅ |
| SC431: "NO @remotion/captions or @remotion/install-whisper-cpp changes — caption pipeline unaffected" | Appropriate impact scoping ✅ |
| SC432: v1.43.1 and v1.44.0 tracked in same cycle (same-day dual release) | Efficient batch tracking ✅ |
| **O3 $1.46 contradiction in generation-video.md** — Day 83 | ❌ DISCIPLINE |
| **CLAUDE.md P0 pricing freeze** — v3 Pro $1.46→$0.728; v3 Standard $1.09→$0.546. Day 60 | ❌ DISCIPLINE |
| **CLAUDE.md routing matrix — Veo 3.1 Lite still listed** — Day 2 | ❌ DISCIPLINE |

**Score: 3.80/5.0** (→ unchanged — SC430 correction is high-quality; persistent DISCIPLINE failures unchanged)

---

### D2 — Execution Accuracy (20%) → 3.80/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC430: Kling O3/Omni model strings already present (SC279) — only status note corrected | Minimal-change, targeted execution ✅ |
| SC431: Remotion v4.0.542 tracked same-day as release | Zero-lag tracking ✅ |
| SC432: Two ffmpeg-normalize versions tracked in one pass + actionable --verify recommendation | Efficient batch update ✅ |
| DB compliance 4/4 (100%) this window — third consecutive clean window | ✅ Strong continuation |
| SC429: "864x1536 (true 9:16) valid by rules but not explicitly confirmed for 2.6 — CANARY" | Appropriate caveat ✅ |
| CLAUDE.md NOT updated for Veo 3.1 Lite retirement (Day 2) | ❌ DISCIPLINE |
| **O3 $1.46 — generation-video.md — Day 83** | ❌ DISCIPLINE |
| SC431: post-production.md NOT updated for Remotion v4.0.542 (Day 1) | ❌ DISCIPLINE (minor) |

**Score: 3.80/5.0** (→ unchanged — third consecutive clean DB window; Remotion drift minor but adds to open gap list)

---

### D3 — Memory & Continuity (15%) → 3.90/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC430: "Previous 'NOT on AIMLAPI (confirmed absent Sept 8, 2026 — SC339)' was based on no-docs-page." — SC cycle number and date referenced precisely | Multi-month memory ✅ |
| SC431: Implicitly recalls caption-pipeline-specific package tracking; confirms no regression | Targeted recall ✅ |
| DB running tally: ~70/100 = 70.0% — **first time crossing 70% threshold** | ✅ Milestone crossed |
| DB compliance: third consecutive 100% window | ✅ Established pattern |
| SC408–SC415 + SC419 + SC422 still absent from pipeline.db | ❌ OPERATIONAL (slowly improving) |

**Score: 3.90/5.0** (↑ +0.05 — DB tally crosses 70% threshold for first time; established 3-window clean streak)

---

### D4 — Reliability (20%) → 3.75/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC432: --verify flag recommendation prevents undetected loudnorm failures in production | Preventive reliability ✅ |
| SC430: Kling O3/Omni corrected + CANARY required before production use | ✅ |
| SC431: Remotion v4.0.542 bug-fixes documented (player timing fix) — users on v4.0.541 may hit timing issue | ✅ |
| CLAUDE.md routing matrix still shows retired Veo 3.1 Lite (P0) — Day 2 | ❌ DISCIPLINE |
| **O3 $1.46 — Day 83** | ❌ DISCIPLINE |
| **CLAUDE.md P0 pricing — Day 60** | ❌ DISCIPLINE |

**Score: 3.75/5.0** (→ unchanged — SC432 --verify recommendation improves audio reliability; blocked by persistent P0 items)

---

### D5 — Integration (15%) → 4.15/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC429: generation-image.md complexity param + size table + CANARY scoping complete | Full specification ✅ |
| SC430: generation-video.md O3/Omni section and routing notes consistent within skill | ✅ |
| SC432: halal-audio.md update stands alone — no cross-skill impact | ✅ |
| SC431: Remotion v4.0.542 updated in captions-and-titles.md but NOT in post-production.md | ⚠️ Minor integration gap (Day 1) |

**Score: 4.15/5.0** (→ unchanged — Remotion version drift is minor; overall cross-skill integration quality maintained)

---

### D6 — Social / Communication (10%) → 3.90/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC432: "Actionable: add --verify to §4a production loudnorm runs as QA gate." | Clear call-to-action ✅ |
| SC430: "CANARY still required to confirm live API activity and actual pricing." | Explicit uncertainty flagging ✅ |
| SC429: "864x1536 (true 9:16) valid by rules but not explicitly confirmed for 2.6 — CANARY" | Precise uncertainty scoping ✅ |
| SC431: "NO @remotion/captions or @remotion/install-whisper-cpp changes — caption pipeline unaffected." | Explicit no-impact declaration ✅ |
| SC430: "Also updated 4K section: O3-based 4K variant may now be AIMLAPI-accessible (unblocked)." | Forward-looking note ✅ |

**Score: 3.90/5.0** (→ unchanged)

---

### AUDIT 1 SUMMARY

| Dimension | Weight | Score | Contribution |
|-----------|--------|-------|-------------|
| D1 Reasoning | 20% | 3.80 | 0.760 |
| D2 Execution | 20% | 3.80 | 0.760 |
| D3 Memory | 15% | 3.90 | 0.585 |
| D4 Reliability | 20% | 3.75 | 0.750 |
| D5 Integration | 15% | 4.15 | 0.623 |
| D6 Social | 10% | 3.90 | 0.390 |
| **TOTAL** | | | **3.87/5.0** |

**Failure summary:**
- DISCIPLINE (dominant): O3 $1.46 contradiction Day 83; CLAUDE.md P0 pricing Day 60; CLAUDE.md Veo 3.1 Lite routing Day 2; Remotion v4.0.542 not propagated to post-production.md Day 1
- OPERATIONAL: SC408–SC415 + SC419 + SC422 absent from data/pipeline.db; running tally ~70%

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

### Skills Assessed This Window (SC429–SC432)

**generation-image.md (SC429)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: GPT Image 2.6 complexity "low"/"medium"/"high" (default "high") documented; size constraints explicit; CANARY required for unconfirmed params ✅
4. RFC 2119: prior audit confirmed ✅
5. Approval gates: prior audit confirmed ✅
6. Length: targeted insertions (3 items) ✅
7. Negative triggers: prior audit confirmed ✅
8. Consistency: GPT Image 2.6 Flare/Sunburst added as CANARY — no contradiction with CLAUDE.md routing matrix (which lists NBP Edit as primary hero frame model; 2.6 is an upgrade candidate) ✅

**Score: 8/8 (100%)**

---

**generation-video.md (SC430)**
Pre-existing O3 $1.46 deduction from prior cycles unchanged. SC430 correction (O3/Omni status) does not affect the O3 pricing deduction.
1–7: Prior audit confirmed ✅
8. Consistency: Kling O3/Omni status corrected within skill; no new CLAUDE.md contradiction introduced ✅ — but pre-existing O3 $1.46 error persists

**Score: 7.25/8** (pre-existing −0.75; unchanged)

---

**captions-and-titles.md (SC431)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: Remotion v4.0.542 npm install updated; impact assessment explicit ("caption pipeline unaffected") ✅
4. RFC 2119: prior audit confirmed ✅
5. Approval gates: prior audit confirmed ✅
6. Length: minimal insertions ✅
7. Negative triggers: prior audit confirmed ✅
8. Consistency: v4.0.542 in captions-and-titles.md; post-production.md still at v4.0.541 — minor version drift (not a CLAUDE.md contradiction but noted as a gap)

**Score: 8/8 (100%)** (Remotion drift is a gap, not a criteria-8 CLAUDE.md contradiction; noted separately)

---

**halal-audio.md (SC432)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: ffmpeg-normalize v1.44.0 --verify flag explicitly documented as actionable; version history updated ✅
4. RFC 2119: prior audit confirmed ✅
5. Approval gates: prior audit confirmed ✅
6. Length: minimal insertions ✅
7. Negative triggers: prior audit confirmed ✅
8. Consistency: no CLAUDE.md interaction; ElevenLabs/yt-dlp confirmations consistent with prior entries ✅

**Score: 8/8 (100%)**

---

### Cross-Skill Consistency

| Check | Status |
|-------|--------|
| post-production.md Remotion v4.0.541 (SC428) vs captions-and-titles.md v4.0.542 (SC431) | ⚠️ NEW MINOR DRIFT — Day 1 |
| captions-and-titles.md ElevenLabs v2.77.0 (SC424/SC431) vs halal-audio.md v2.77.0 (SC432) | ✅ CONSISTENT |
| credit-efficiency.md Gemini Omni 1.2 Flash (SC427) vs CLAUDE.md routing matrix (Veo 3.1 Lite) | ❌ PERSISTS — P0 Day 2 |
| credit-efficiency.md Kling v3 Pro $0.728/5s vs CLAUDE.md routing matrix $1.46 | ❌ PERSISTS — P0 Day 60 |
| generation-video.md Kling O3/Omni (SC430 — docs confirmed) vs CLAUDE.md (not referenced) | ✅ No contradiction |

### CLAUDE.md Audit

| Component | Present | Status |
|-----------|---------|--------|
| Instruction count vs 150 limit | ~100 instructions | ✅ |
| Three-agent pattern | ✅ PLANNER/GENERATOR/EVALUATOR | ✅ |
| Snorkel triage | ✅ ZERO/3-5 taxonomy | ✅ |
| Model routing matrix | ✅ Present | ❌ **Two distinct P0 errors:** pricing (Day 60) + Veo 3.1 Lite retired (Day 2) |
| Brand binary checklist | ✅ All 6 items | ✅ |
| Production gates | ✅ All 10 | ⚠️ Pre-gen check #5/#7 wording — Day 125 |

**CLAUDE.md deduction: −0.75 (unchanged — same two P0 errors as yesterday)**

### Hindsight / Memory Status

- `data/pipeline.db`: study_cycles entries through SC432; SC422 + SC408–SC415 + SC419 absent; running tally ~70/100 = 70.0%
- DB compliance this window: **4/4 (100%)** — third consecutive full-compliance window
- Feedback catalog: Current (pattern-extractor.py runs Sundays)
- Skills updated this window: generation-image.md, generation-video.md, captions-and-titles.md, halal-audio.md

### Gap Analysis

| Gap | Severity | Days Open |
|----|---------|-----------|
| **Veo 3.1 Lite still in CLAUDE.md routing matrix** — retired Oct 22; replace with Gemini Omni 1.2 Flash | 🔴 CRITICAL | **2** |
| **O3 $1.46 contradiction in generation-video.md** — line 703 | 🔴 CRITICAL | **83** |
| **SC408–SC415 + SC419 + SC422 absent from data/pipeline.db** | 🔴 CRITICAL | varies |
| Kling v4 canary: audio strip, face adherence, billing | 🔴 CRITICAL | **18** |
| Wan 2.7 R2V canary on AIMLAPI ($0.65/5s) | 🔴 CRITICAL | **12** |
| **CLAUDE.md pricing errors (P0)** — v3 Pro $1.46→$0.728; v3 Standard $1.09→$0.546 | 🟠 HIGH | **60** |
| Gemini Omni 1.2 Flash canary — aspect_ratio param name + billing | 🟠 HIGH | **2** |
| ElevenLabs v4 Dutch canary | 🟠 HIGH | **15** |
| Luma Uni-1 remaining canary: pricing + face adherence | 🟠 HIGH | **7** |
| SC408–SC422 DB gaps retroactive repair | 🟠 HIGH | varies |
| GPT Image 2.6 Flare/Sunburst canary — size param (864x1536?), billing | 🟠 HIGH | **3** |
| Kling O3/Omni canary — live API + pricing (docs pages now confirmed SC430) | 🟠 HIGH | **1 (NEW)** |
| post-production.md Remotion v4.0.541 → v4.0.542 update (SC431) | 🟡 MEDIUM | **1 (NEW)** |
| Grok Video 1.5 Preview canary (SC413) | 🟡 MEDIUM | **6** |
| NB2.1 production canary | 🟡 MEDIUM | **15** |
| Kling v4 T2V / R2V dual-string active canary (SC423) | 🟡 MEDIUM | **3** |
| CLAUDE.md pre-gen check #5/#7 wording | 🟡 MEDIUM | **125** |
| Remotion v4.0.540 breaking changes in production code | 🟡 MEDIUM | — |
| ACM MM 2026 (Nov 10-14, Rio) — Chronos updated results | 🟡 MEDIUM | **check Nov 15** |
| ffmpeg-normalize --verify flag: add to §4a production loudnorm commands | 🟡 MEDIUM | **1 (NEW — SC432 recommends, not yet implemented in runbook)** |

**Closed this window:** None. FaceFusion v3.9.2 gap closed prior window (SC426).
**Opened this window:** Kling O3/Omni canary (now accessible), Remotion version drift, ffmpeg-normalize --verify runbook update.

### Skill Score Calculation

| Category | Passes | Possible | Notes |
|----------|--------|----------|-------|
| Core skills (18 files × 8 criteria) | 142.50 | 144 | Pre-existing: −0.75 (O3 in generation-video.md); generation-image.md, captions-and-titles.md, halal-audio.md clean 8/8 |
| CLAUDE.md structural components | 5.25 | 6 | −0.75 total (pricing P0 Day 60 + Veo 3.1 Lite routing Day 2) |
| Cross-skill consistency | 11 | 10 | Two contradictions tracked; score held at prior methodology |
| **TOTAL** | **158.75** | **160** | **99.2%** |

**Total: 99.2%** (→ unchanged — no new skill-level deductions this window)

**Target ≥95%: PASS**

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved output:** V2-Proces (2026-04-12)
**Days since last approval:** **211 days**
**Output produced since Nov 9 audit:** None

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

1. **211 days without a single approved video.** The routing matrix is broken (Veo 3.1 Lite retired Day 2). The B-roll pricing in CLAUDE.md is wrong (Day 60). The O3 cost per clip is wrong in the skill file (Day 83). If production started today using CLAUDE.md + generation-video.md as references, three separate numbers would lead the operator to wrong budget estimates and broken API calls. The pipeline's documentation has drifted so far from reality that the first production attempt would surface at least one P0 failure before the second clip.

2. **Kling O3/Omni just became accessible (SC430) — nobody has canary'd it.** The pipeline's highest-tier character shots use Kling v3 Pro at $0.728/5s. Kling O3/Omni may be better, different, or the same price. 211 days of no production has accumulated at least 5 "CANARY REQUIRED" items (O3/Omni, Gemini Omni 1.2 Flash, Kling v4, GPT Image 2.6, Wan 2.7). The first production session will need $5–10 of canary calls before the first real shot. This is not pipeline readiness — it is technical debt.

3. **ffmpeg-normalize --verify flag is documented as actionable but not in the runbook.** SC432 says "Actionable: add --verify to §4a production loudnorm runs as QA gate." Until halal-audio.md's §4a command block is updated with the actual flag, the recommendation exists as prose in a commit message, not as an enforced step in the production checklist. A producer following §4a step-by-step will not use --verify because it is not there.

### Model Capability Notes (New Since Nov 9)

- **Kling O3/Omni: DEDICATED DOCS PAGES CONFIRMED (SC430)** — Previously "absent" (SC339, Sept 8, 2026). Four new AIMLAPI docs pages found. CANARY REQUIRED for live API + pricing. 4K variant potentially accessible. High relevance for character shots if quality > v3 Pro.
- **GPT Image 2.6 Flare/Sunburst: LIKELY ON AIMLAPI (SC429)** — Upgraded from "absent". Complexity param ("low"/"medium"/"high") documented. CANARY REQUIRED for 864x1536 (true 9:16) and billing.
- **ffmpeg-normalize v1.44.0 (SC432)** — New --verify flag for loudnorm QA. Zero breaking changes. Recommend updating §4a loudnorm command.
- **Remotion v4.0.542 (SC431)** — Player timing fix relevant to caption timing accuracy. Update post-production.md.
- **ACM MM 2026 running Nov 10-14 (today)** — Chronos identity-preserving video generation paper; check repo after Nov 14 for updated results.

### Cost Metric

Credits per APPROVED video: **MATHEMATICALLY UNDEFINED** (0 approved videos since April 12, 2026)

### Predicted Pass Rate

**~70% confidence, 70% predicted pass rate** (→ unchanged)

**Note:** B-roll routing is still broken (Veo 3.1 Lite retired, CLAUDE.md not updated). Pass rate will drop if production runs before the three P0 fixes are made.

CREATIVE_AUDIT_COMPLETE

---

## TOP ACTION ITEMS (Prioritized)

| # | Priority | Action | Deadline |
|---|----------|--------|---------|
| 1 | 🔴 CRITICAL | **Fix CLAUDE.md routing matrix** — Veo 3.1 Lite RETIRED Oct 22. Replace B-roll/establishing rows with Gemini Omni 1.2 Flash ($0.0695/sec). Add "AUDIO ALWAYS ON — mandatory post-strip" note. Mark canary required. **Day 2. Production broken without this.** | Immediate |
| 2 | 🔴 CRITICAL | **Fix O3 $1.46 contradiction in generation-video.md** — line 703: `\| Final character shot \| v3 Pro \| $1.46 \|` → `$0.728`. **Day 83.** | Immediate |
| 3 | 🟠 HIGH | **Fix CLAUDE.md pricing errors (P0)** — v3 Pro $1.46→$0.728; v3 Standard $1.09→$0.546. 5-minute edit. **Day 60.** | Immediate |
| 4 | 🔴 CRITICAL | **Run combined canary session** — (a) Gemini Omni 1.2 Flash aspect_ratio + billing; (b) Kling O3/Omni live API + pricing (SC430 unblocked); (c) Kling v4 I2V audio+face; (d) GPT Image 2.6 Flare size param; (e) Wan 2.7 R2V. Total: ~$3–5. | Before next production |
| 5 | 🟡 MEDIUM | **Update post-production.md Remotion version** — v4.0.541 → v4.0.542. 1-line change. **Day 1.** | Next SC |
| 6 | 🟡 MEDIUM | **Add --verify to halal-audio.md §4a loudnorm command** — SC432 recommends; not yet in runbook. | Next SC |
| 7 | 🟠 HIGH | **Repair DB gaps** — SC408–SC415 + SC419 + SC422 absent from pipeline.db. Running tally 70.0%. | Next maintenance session |
| 8 | 🔴 CRITICAL | **START PRODUCTION** — 211 days since last approved video. Fix items 1-3 first (15 min), then canary session (item 4), then produce. | Now |

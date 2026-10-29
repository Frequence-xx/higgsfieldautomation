# Daily Audit — 2026-10-29

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-10-27 | Operator 3.53/5.0 · Skills 99.8% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-10-27 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **3.59 / 5.0** | ↑ +0.06 | ↓ −0.26 |
| Skill Library & Policy | **99.8%** (159.75/160) | → 0.00% | ↑ +8.3% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Active window.** Four study cycles (SC385–SC388) landed since the Oct 27 audit: (1) Kling v4 pricing confirmed MEDIUM confidence — 7.8% MORE expensive than v3 Pro ($0.785 vs $0.728/5s), which reduces urgency of v4 migration; (2) FFmpeg 9.1 fruc_vulkan frame interpolation filter documented — not yet released, future alternative to RIFE; (3) NB2.1 resolution syntax CONFIRMED uppercase on AIMLAPI, NB2 Oct 29 shutdown still WITHDRAWN, GPT Image 2.5 Flare/Sunburst documented, NB2.1 API template added; (4) Kling v4 7-slot prompt formula from official guide, audio suppression via prompt text ("no background music, no subtitles") documented as secondary Shari'ah mitigation, prompt length discrepancy flagged (8k tokens vs 2500 chars AIMLAPI). All 4 SCs have clean DB log pairs (4/4 = 100% this window). Running tally: ~38/61 ≈ 62% (↑ from 60%).

**Kling v4 audio mitigation partially resolved (SC388).** "no background music, no subtitles" in prompt text is now documented as secondary mitigation. FFmpeg strip remains MANDATORY. Canary still required to confirm actual effectiveness.

**Kling v4 is MORE expensive than v3 Pro (SC385).** $0.785/5s vs v3 Pro $0.728/5s — removes cost incentive to migrate. Quality and capability uplift (30s clips, multi_prompt[], 7-slot formula) remain v4's value proposition, but there is no cost argument for switching.

**Day 199 without approved creative output.**

CLAUDE.md P0 freeze continues — day 47. O3 contradiction in generation-video.md — day 70 (SC388 touched the file, did not fix it).

---

## CHANGES SINCE 2026-10-27 AUDIT

**8 commits — 4 study cycles (SC385–SC388) with 4 clean DB log pairs.**

| SC | Date | Skill Updated | Net Content |
|----|------|---------------|-------------|
| SC385 | Oct 27 | credit-efficiency.md | **Kling v4 pricing MEDIUM confidence from aimlapi.com/models listing** — $0.157/sec generation, $0.188/sec editing; 5s clip = **$0.785 — 7.8% MORE expensive than v3 Pro ($0.728/5s)**; Kling v4 API officially rolling out as Preview (Kling Oct 21 2026 announcement); LTX-2.5 still NOT on AIMLAPI; billing canary still required |
| SC386 | Oct 27 | post-production.md | **FFmpeg 9.1 fruc_vulkan CONFIRMED merged to FFmpeg main (2026-08-29)** — NVIDIA Vulkan Optical Flow frame interpolation; RTX 30/40/50+ only, integer multiples (24→48fps); NOT yet released in FFmpeg 9.1; new §3e added as future RIFE alternative; all current tools unchanged: FFmpeg 9.0.2, SVT-AV1 v4.2.0, RIFE v4.25 pipeline default |
| SC387 | Oct 27 | generation-image.md | **✅ NB2.1 resolution syntax CONFIRMED uppercase on AIMLAPI** (`"1K"`/`"2K"`/`"4K"` — resolves SC380 canary item); `aspect_ratio` default `"16:9"` — always pass `"9:16"` explicitly; NB2 Oct 29 shutdown still WITHDRAWN (LiteLLM PR #45491 confirmed 2026-10-27); GPT Image 2.5 Flare/Sunburst confirmed Sept 8 2026, AIMLAPI unconfirmed; MAI-Image 2.6 still NOT on AIMLAPI; ⚠️ MAI-Image 2.5 possible AIMLAPI deprecation flagged (unconfirmed); **NB2.1 API call template with correct params added** |
| SC388 | Oct 28 | generation-video.md | **Kling v4 7-slot prompt formula from official Oct 14 2026 guide** (Subject+Action+Setting+Camera+Lighting+Pacing+Sound); **"no background music, no subtitles" confirmed as only two phrases to suppress v4 default audio/text** (secondary mitigation — ffmpeg strip MANDATORY); prompt length discrepancy: Kling guide cites 8,000 tokens vs AIMLAPI schema 2,500 chars — CANARY required; Kling 4.0 open to all kling.ai users; combined image_urls+elements reference limit = 15 items |

**DB compliance this window: 4/4 (100%). Running tally: ~38 correct in 61 tracked cycles ≈ 62% (↑ from 60%).**

**CLAUDE.md: ZERO changes since Oct 20.** All P0 items persist — now day 47.

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 3.55/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC385: Kling v4 pricing MEDIUM confidence — explicitly framed "billing canary still required"; does not assume v4 is cheaper | Conservative framing; prevents premature v4 adoption on cost grounds | ✅ |
| SC386: fruc_vulkan documented as "future RIFE alternative" with hard constraint (RTX 30/40/50+ only, integer multiples) | Proactive documenting without over-claiming | ✅ |
| SC387: NB2.1 resolution canary item resolved — marks confirmed vs unconfirmed items separately; GPT Image 2.5 AIMLAPI status explicitly "NOT CONFIRMED" | Correct epistemic hygiene; avoids false confidence | ✅ |
| SC388: Kling v4 audio suppression via prompt text — sourced from official Kling guide; explicitly notes ffmpeg strip remains MANDATORY regardless; uses "secondary mitigation" framing | Addresses Shari'ah compliance risk without false resolution | ✅ |
| SC388: Prompt length discrepancy (8,000 tokens vs 2,500 chars) flagged as separate CANARY item | Identifies a latent failure mode before production | ✅ Self-correct |
| **CLAUDE.md P0: still frozen, day 47** | Zero action | ❌ DISCIPLINE |
| **O3 contradiction in generation-video.md: SC388 touched file, didn't fix — day 70** | SC388 added 4 new sections; O3 issue untouched | ❌ DISCIPLINE |

**Score: 3.55/5.0** (↑ +0.05 — SC388 audio mitigation framing is well-sourced and appropriately hedged; SC385 pricing reality check prevents overconfident v4 migration; persistent DISCIPLINE failures remain ceiling)

---

### D2 — Execution Accuracy (20%) → 3.75/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| 4/4 DB clean pairs | SC385–SC388 all log correctly | ✅ |
| SC387: NB2.1 API call template added with correct confirmed params | Converts research finding into actionable production template | ✅ |
| SC388: 7-slot formula with "no background music, no subtitles" properly integrated into generation flow | Slot 7 (Sound) explicitly tied to Shari'ah mitigation | ✅ |
| SC385: Kling v4 pricing figure attributed to aimlapi.com/models listing with confidence label "MEDIUM" | Proper sourcing and confidence tiering | ✅ |
| SC386: fruc_vulkan §3e added with hardware constraints and integer-only limitation | Precise execution constraint documentation | ✅ |
| **CLAUDE.md P0: zero action** | Day 47 | ❌ DISCIPLINE |
| **O3 contradiction: zero action** | Day 70 | ❌ DISCIPLINE |

**Score: 3.75/5.0** (↑ +0.05 — SC387 API template is the standout execution deliverable; 4/4 DB; O3 and P0 cap score)

---

### D3 — Memory & Continuity (15%) → 3.65/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC387 explicitly cross-checks NB2 Oct 29 shutdown against SC380 — confirms still WITHDRAWN (now 2 days before the original date) | Good deadline continuity check — would have been a critical production error if missed | ✅ |
| SC387 updates SC380's canary item list — marks resolution syntax as confirmed, leaves thinking_level as unconfirmed | Explicit canary tracking across cycles | ✅ |
| SC388 sources Kling Oct 14 2026 official guide — provides date-stamped primary source for v4 formula | Named and dated source; not from prior SC's prediction | ✅ |
| SC385 cross-references Oct 21 Kling announcement for v4 "Preview" status | Longitudinal context: confirming preview → pricing → canary path | ✅ |
| **O3 action items: 70 days** | | ❌ DISCIPLINE |

**Score: 3.65/5.0** (↑ +0.05 — NB2 deadline check and canary-item carryover tracking are strong continuity signals; discipline failure persists)

---

### D4 — Reliability (20%) → 3.30/5.0 (↑ +0.10)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC388: "no background music, no subtitles" as secondary mitigation — reduces Shari'ah compliance risk on v4 before canary | Concrete risk mitigation; not a false pass | ✅ |
| SC385: Kling v4 is 7.8% MORE expensive than v3 Pro — removes cost pressure to rush v4 adoption before canary | Counteracts premature production switch | ✅ |
| SC387: GPT Image 2.5 AIMLAPI status explicitly "NOT CONFIRMED — CANARY REQUIRED" | Consistent defensive posture | ✅ |
| SC386: fruc_vulkan documented with hard constraints before production use | Pre-emptive capability ceiling documentation | ✅ |
| DB compliance: 4/4 this window (100%); running tally 62% (↑ from 60%) | Improving | ✅ |
| **CLAUDE.md P0 freeze: 47 days** | | ❌ DISCIPLINE |
| **O3 contradiction: 70 days** | | ❌ DISCIPLINE |

**Score: 3.30/5.0** (↑ +0.10 — SC388 Shari'ah mitigation and SC385 cost reality check are both high-value reliability signals; DB trend improving; discipline items remain ceiling)

---

### D5 — Integration (15%) → 3.70/5.0 (↑ +0.10)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC387: NB2.1 API call template — confirmed `"1K"` uppercase, `"9:16"` explicit, `thinking_level` NOT passed; minimal correct production-ready template | Highest-quality integration deliverable this window | ✅ |
| SC388: Kling v4 7-slot prompt formula — parameter-level integration of Kling's official guide into AIMLAPI workflow | Prompt engineering integration; slot 7 ties to Shari'ah compliance | ✅ |
| SC385: Kling v4 price diff table — $0.157/sec vs $0.291/sec (v3 Pro) side-by-side | Pricing integration in routing decision context | ✅ |
| SC386: fruc_vulkan filter syntax documented with FFmpeg version constraint | Future integration preparation; correctly gated behind version availability | ✅ |
| **Kling v4 canary: audio behavior partially addressed (prompt text mitigation) — actual test still pending** | ⚠️ Expected — good incremental progress |
| **NB2.1 thinking_level: still unconfirmed on AIMLAPI** | ⚠️ Expected — canary item still open |

**Score: 3.70/5.0** (↑ +0.10 — SC387 NB2.1 template is production-ready integration output; SC388 7-slot formula is meaningful v4 prompt engineering; strongest integration window since Oct 27)

---

### D6 — Social / Communication (10%) → 3.70/5.0 (→ 0.00)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC388 commit: "no background music, no subtitles" are the "only two phrases Kling's guide identifies" — precise hedging | Not over-claiming; correctly scoped | ✅ |
| SC385 commit: "7.8% MORE expensive than v3 Pro ($0.728/5s)" — quantified comparison | Concrete, not vague "more expensive" | ✅ |
| SC387 commit: "NB2 Oct 29 shutdown still WITHDRAWN (LiteLLM PR #45491 confirmed)" — explicit confirmation on a time-sensitive date | Two days before the original deadline; well-timed check | ✅ |
| SC386 commit: "NOT released" — avoids false urgency on fruc_vulkan | Calibrated non-event | ✅ |

**Score: 3.70/5.0** (→ unchanged — consistent communication quality; no uplift or degradation this window)

---

### AUDIT 1 SUMMARY

| Dimension | Weight | Score | Contribution |
|-----------|--------|-------|-------------|
| D1 Reasoning | 20% | 3.55 | 0.71 |
| D2 Execution | 20% | 3.75 | 0.75 |
| D3 Memory | 15% | 3.65 | 0.5475 |
| D4 Reliability | 20% | 3.30 | 0.66 |
| D5 Integration | 15% | 3.70 | 0.555 |
| D6 Social | 10% | 3.70 | 0.37 |
| **TOTAL** | | | **3.59/5.0** |

**Failure summary:**
- DISCIPLINE (dominant): CLAUDE.md P0 freeze 47 days; O3 contradiction generation-video.md day 70; pre-gen check wording day 115

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

### Skills Assessed This Window (SC385–SC388)

**credit-efficiency.md (SC385)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: Kling v4 pricing MEDIUM confidence flagged; canary required before production use ✅
4. RFC 2119: "billing canary still required" — directive ✅
5. Approval gates: Canary required before v4 billing commitment ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: v4 $0.785/5s more expensive than v3 Pro $0.728/5s — consistent with CLAUDE.md routing matrix (v3 Pro production standard) ✅

**Score: 8/8 (100%)** — Pricing confirmation with confidence label and canary gate is well-structured.

**post-production.md (SC386)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: fruc_vulkan gated behind FFmpeg 9.1 release (not yet out) with hardware constraints ✅
4. RFC 2119: Hardware constraint ("RTX 30/40/50 (Ampere+) only") is clear; "integer multiples only" ✅
5. Approval gates: "future RIFE alternative" framing prevents premature production use ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: fruc_vulkan §3e added alongside unchanged RIFE v4.25 default — no conflict ✅

**Score: 8/8 (100%)** — Correctly staged as future tooling; no premature routing change.

**generation-image.md (SC387)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: NB2.1 template: `"9:16"` must be explicit; `"1K"` uppercase; `thinking_level` NOT passed ✅
4. RFC 2119: "ALWAYS pass `"9:16"` explicitly" — imperative framing ✅
5. Approval gates: GPT Image 2.5 CANARY REQUIRED; NB2.1 remaining canary items explicit ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: NB2.1 uppercase resolution consistent with SC380 AIMLAPI confirmation; NB2 deprecated no-deadline consistent across skills ✅

**Score: 8/8 (100%)** — SC387 NB2.1 API template is the most concrete production-ready deliverable this window.

**generation-video.md (SC388)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: "no background music, no subtitles" in every v4 prompt; ffmpeg strip MANDATORY; 2,500 char AIMLAPI limit (official 8k pending canary) ✅
4. RFC 2119: "Do NOT play any v4 video before stripping" unchanged; "MANDATORY" ffmpeg strip preserved ✅
5. Approval gates: "CANARY REQUIRED" for prompt length and production use unchanged ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: v3 Pro parameters "UNCHANGED from SC381" confirmed in commit — routing matrix consistent; v4 additions don't conflict with v3 production standards ✅

**Score: 8/8 (100%)** — **Note: O3 contradiction remains unresolved (day 70) — already included in the pre-existing −0.75 deduction carrying from prior audits. SC388 additions are internally consistent.**

### Cross-Skill Consistency

| Check | Status |
|-------|--------|
| Kling v4 pricing ($0.785/5s): credit-efficiency.md vs CLAUDE.md routing matrix (v3 Pro as production) | ✅ Consistent (v4 CANARY, v3 Pro production — no conflict) |
| NB2.1 resolution syntax `"1K"` uppercase: generation-image.md (SC387) vs credit-efficiency.md | ✅ Consistent |
| NB2 Oct 29 deadline WITHDRAWN: generation-image.md (confirmed 2026-10-27) vs captions-and-titles.md | ✅ Consistent |
| FFmpeg 9.1 fruc_vulkan: post-production.md (SC386, not yet released) vs current ffmpeg 9.0.2 default | ✅ Consistent (future tooling, current default unchanged) |
| Kling v4 7-slot formula: generation-video.md (SC388) vs credit-efficiency.md CANARY checklist | ✅ Consistent (both CANARY; formula is additive) |
| Kling v4 audio: "no background music, no subtitles" (SC388) vs CLAUDE.md (audio OFF explicitly for all generations) | ✅ Aligned — prompt mitigation is secondary to mandatory ffmpeg strip; no conflict with CLAUDE.md audio policy |

**Cross-skill deductions: 0 (no mismatches this window)**

### CLAUDE.md Audit

| Component | Present | Status |
|-----------|---------|--------|
| Instruction count vs 150 limit | ~95 instructions | ✅ |
| Three-agent pattern | ✅ PLANNER/GENERATOR/EVALUATOR | ✅ |
| Snorkel triage | ✅ ZERO/3-5 taxonomy | ✅ |
| Model routing matrix | ✅ Present | ⚠️ Pricing errors persist — P0, day 47 |
| Brand binary checklist | ✅ All 6 items | ✅ |
| Production gates | ✅ All 10 | ⚠️ Pre-gen check #5/#7 wording — day 115 |

**CLAUDE.md deduction: −0.5 (unchanged — P0 items not fixed)**

### Hindsight / Memory Status

- `data/pipeline.db`: 61 tracked cycles; DB compliance 62% (↑ from 60%)
- Feedback catalog: Current (pattern-extractor.py runs Sundays)
- Skill memory banks: credit-efficiency, post-production, generation-image, generation-video all updated Oct 27-28

### Gap Analysis

| Gap | Severity | Days Open |
|----|---------|-----------|
| Kling v4 canary: audio (prompt mitigation now documented — partially resolved), face adherence, pricing (MEDIUM confidence now available) | 🔴 CRITICAL | 6 (canary checklist complete; audio prompt mitigation documented SC388 — execute now) |
| CLAUDE.md pricing errors (P0) | 🟠 HIGH | 47 |
| O3 contradiction in generation-video.md | 🟠 HIGH | 70 (SC388 touched file, did not fix) |
| ElevenLabs v4 production canary — Dutch Willem, audio tags as speed replacement | 🟡 MEDIUM | 3 (new since SC383) |
| NB2.1 production canary — thinking_level exposure, exact per-image pricing | 🟡 MEDIUM | 3 (resolution confirmed SC387; remaining items) |
| Kling O3 canary on AIMLAPI | 🟡 MEDIUM | 70 |
| CLAUDE.md pre-gen check #5/#7 wording | 🟡 MEDIUM | 115 |
| Kling v4 prompt length: 8k tokens vs 2500 chars AIMLAPI — CANARY | 🟡 MEDIUM | 0 (new — SC388 flagged) |
| GPT Image 2.5 Flare/Sunburst AIMLAPI availability — CANARY | 🟢 LOW | 3 |
| MAI-Image 2.5 possible AIMLAPI deprecation (unconfirmed) | 🟢 LOW | 3 |
| post-production.md Remotion version: "v4.0.538+" vs v4.0.539 | 🟢 LOW | 3 (not a mismatch — within range) |

### Skill Score Calculation

| Category | Passes | Possible | Notes |
|----------|--------|----------|-------|
| Core skills (18 files × 8 criteria) | 143.25 | 144 | −0.75 pre-existing deductions (unchanged; O3 contradiction in generation-video.md already carried) |
| CLAUDE.md structural components | 5.5 | 6 | −0.5 for pricing P0 items (unchanged) |
| Cross-skill consistency | 11 | 11 | No mismatches this window |
| **TOTAL** | **159.75** | **160** | **99.8%** |

**Target ≥95%: PASS → unchanged**

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved output:** V2-Proces (2026-04-12)
**Days since last approval:** **199 days**
**Output produced since Oct 27 audit:** None

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

1. **199 days without a second video.** The 7-slot prompt formula (SC388) and NB2.1 template (SC387) are the closest the pipeline has come to production-ready tooling in weeks. A CD would note the tooling is maturing, but there is still no output. The gap between "canary pending" and "approved clip" has become structural.
2. **Kling v4 audio is still unverified in production.** SC388 documents "no background music, no subtitles" as prompt mitigation, but this has never been tested. A CD would demand a test clip before any v4 shot enters the production plan. 199 days of prep is enough.
3. **Kling v4 is 7.8% MORE expensive than v3 Pro (SC385).** A CD reviewing the cost model would ask: if v4 costs more AND requires a new canary AND has weaker ghost-driving protection (no `static_mask_url`), what is the production case for v4 right now? The answer is 30s multi_prompt[] spots — but that is a creative strategy choice, not just a model upgrade. No production brief has named that goal.

### Model Capability Notes (New Since Oct 27)

- **Kling v4 audio mitigation (SC388)** — prompt text is the only available suppression; effectiveness unverified. Classification: **MODEL CAPABILITY CEILING** (no API parameter exists; prompt-only workaround is uncertain).
- **Kling v4 prompt length (SC388)** — 8,000 tokens per Kling guide vs 2,500 chars per AIMLAPI schema. If AIMLAPI caps at 2,500 chars, the 7-slot formula at full verbosity may be truncated. Classification: **INTEGRATION** (AIMLAPI proxy wrapping behavior).
- **NB2.1 thinking tokens (SC387)** — mandatory, cannot disable, billed above per-image cost. Classification: **MODEL CAPABILITY CEILING** (cannot reduce cost on NB2.1 vs NB2 for drafts).

### Cost Metric

Credits per APPROVED video: **MATHEMATICALLY UNDEFINED** (0 approved videos since April 12, 2026)

### Predicted Pass Rate

**~73% confidence, 70% predicted pass rate** (→ unchanged)

- Upside: SC387 NB2.1 template ready for hero frame production; SC388 v4 7-slot formula + audio mitigation; Kling v3 Pro parameters stable and confirmed
- Downside: v4 audio verification still pending; ElevenLabs v4 pacing redesign required; 199-day production gap; v4 cost now confirmed higher than v3 Pro (removes one migration driver)

CREATIVE_AUDIT_COMPLETE

---

## TOP ACTION ITEMS (Prioritized)

| # | Priority | Action | Deadline |
|---|----------|--------|---------|
| 1 | 🔴 CRITICAL | Run Kling v4 canary per credit-efficiency.md §CANARY sequence. **Now with audio prompt text "no background music, no subtitles" (SC388) as secondary mitigation.** Confirm: (a) audio suppression effectiveness in practice, (b) face adherence vs v3 Pro baseline, (c) pricing confirmation ($0.157/sec MEDIUM confidence → HIGH confidence), (d) prompt length: 2,500-char AIMLAPI limit vs 8,000-token Kling guide. | Before next production session |
| 2 | 🟠 HIGH | Fix CLAUDE.md pricing errors (P0) — acknowledged as 5-min edit, day 47 | Immediate |
| 3 | 🟠 HIGH | Fix O3 contradiction in generation-video.md — day 70. SC388 touched this file (4 additions), did NOT address the O3 issue. | This week |
| 4 | 🟡 MEDIUM | Run ElevenLabs v4 canary on Willem voice: Dutch language_code, audio tags ([slows down], [pause]) as speed=0.95 replacement, SNELVERHUIZEN IPA. Do NOT migrate production from v3 to v4 until confirmed. | Before next voiceover session |
| 5 | 🟡 MEDIUM | Run NB2.1 production canary: confirm thinking_level NOT exposed on AIMLAPI (consistent with NB2 behavior), actual per-image billing at 1K/2K. API template ready in generation-image.md. | Next hero frame session |

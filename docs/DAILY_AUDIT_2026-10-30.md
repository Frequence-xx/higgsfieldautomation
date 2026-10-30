# Daily Audit — 2026-10-30

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-10-29 | Operator 3.59/5.0 · Skills 99.8% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-10-29 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **3.64 / 5.0** | ↑ +0.05 | ↓ −0.21 |
| Skill Library & Policy | **99.8%** (159.75/160) | → 0.00% | ↑ +8.3% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Active window.** Three study cycles (SC389–SC391) landed after the Oct 29 audit: (1) SC389: `parseVtt()` behavioral details confirmed from official Remotion docs; Remotion v5.0 pre-release watch section added — 5 breaking changes documented, including license change requiring `licenseKey` for Automators tier and contractors counting toward team size; (2) SC390: ElevenLabs Oct 5 2026 ~20% TTS price cut documented across all models — v4 now confirmed same cost as v3 post-cut ($0.08/1K), removing cost barrier to v4 migration (Dutch canary is now the only blocker); (3) SC391: FaceFusion **3.9.2 CRITICAL NVIDIA driver fatal error fix** — any GPU machine on v3.9.1 with recently-updated NVIDIA drivers will crash fatally; upgrade immediately. Wan 2.7 R2V upgraded from "NOT YET LIVE" to **CONFIRMED LIVE on AIMLAPI** ($0.65/5s — 2.2× cheaper than Kling O1). All 3 SCs have clean DB log pairs (3/3 = 100% this window). Running tally: ~41/64 ≈ 64% (↑ from 62%).

**Wan 2.7 R2V is now CONFIRMED LIVE on AIMLAPI (SC391).** $0.65/5s at 720P. Model string and binding syntax still require canary (try both `alibaba/wan-2-7-r2v` and `alibaba/wan2.7-r2v`). This is the most significant routing development in weeks — B-roll character shots 2.2× cheaper than Kling O1.

**ElevenLabs v4 cost barrier removed (SC390).** v4 now costs same as v3 post Oct 5 cut ($0.08/1K). Only Dutch canary prevents production switch.

**Day 200 without approved creative output.**

CLAUDE.md P0 freeze continues — day 48. O3 contradiction in generation-video.md — day 71 (SC388–SC391 all skipped fixing it).

---

## CHANGES SINCE 2026-10-29 AUDIT

**6 commits — 3 study cycles (SC389–SC391) with 3 clean DB log pairs.**

| SC | Date | Skill Updated | Net Content |
|----|------|---------------|-------------|
| SC389 | Oct 29 | captions-and-titles.md | `parseVtt()` behavioral details from official remotion.dev docs (WEBVTT header optional, comma-as-separator accepted, cue settings discarded silently, multi-line text joined); Remotion v5.0 watch section added — PR #3750 still open, NOT released; 5 pipeline-relevant breaking changes including `<Sequence>` premount default, bt709 color space, and license changes (contractors count toward team size, Automators tier needs `licenseKey`); no new library releases |
| SC390 | Oct 29 | halal-audio.md | **ElevenLabs Oct 5 2026 ~20% TTS price cut**: v3 $0.10→$0.08/1K, Multilingual v2 $0.10→$0.08/1K, Flash v2.5 $0.05→$0.04/1K chars; v4 pricing confirmed $0.08/1K (usagepricing.com, Oct 2026 — matches v3 post-cut, "unverified" flag removed); **Practical implication: v4 now costs no more than v3 — Dutch canary is the only remaining blocker** |
| SC391 | Oct 29 | character-consistency.md | **FaceFusion v3.9.2 (Oct 26 2026) CRITICAL**: NVIDIA driver fatal error fix — v3.9.1 on GPU machines with recently-updated NVIDIA drivers crashes fatally; drop-in upgrade; install code updated to `git checkout 3.9.2`. **Wan 2.7 R2V: CONFIRMED LIVE on AIMLAPI** — dedicated page at aimlapi.com/models/alibaba-wan2-7-r2v; pricing $0.13/sec = $0.65/5s at 720P; model string and binding syntax still require canary |

**DB compliance this window: 3/3 (100%). Running tally: ~41/64 ≈ 64% (↑ from 62%).**

**CLAUDE.md: ZERO changes since Oct 20.** All P0 items persist — now day 48.

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 3.60/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC391: Wan 2.7 R2V upgraded from "NOT YET LIVE" to "CONFIRMED LIVE" — sources AIMLAPI dedicated models page; binding syntax and param schema remain flagged as canary-required | Correct epistemic hygiene: confirms status but does not over-claim production readiness | ✅ |
| SC391: FaceFusion 3.9.2 CRITICAL NVIDIA driver fix — "Upgrade immediately" language used; v3.9.1 → v3.9.2 as drop-in | Appropriate severity classification; no hedging on a safety-critical tool fix | ✅ |
| SC390: ElevenLabs pricing: v4 confirmed same cost as v3 post-cut; conclusion clearly drawn: "only Dutch canary prevents switch" | Correct consequence-reasoning from a pricing change — removes a false cost barrier | ✅ |
| SC389: Remotion v5.0 framed as "NOT YET RELEASED" with PR number and incomplete migration guide acknowledgment | Conservative framing of pre-release state; proactive break-glass planning | ✅ Self-correct |
| SC389: License change flagged with action item ("verify Farouq's license tier before v5.0 upgrade") | Proactive compliance risk identification before it becomes a problem | ✅ |
| **CLAUDE.md P0: still frozen, day 48** | Zero action | ❌ DISCIPLINE |
| **O3 contradiction in generation-video.md: day 71 — SC389-SC391 all skipped** | SC390 touched halal-audio.md, SC391 touched character-consistency.md — neither file is the problem; the issue is in generation-video.md and has been untouched for 71 days | ❌ DISCIPLINE |

**Score: 3.60/5.0** (↑ +0.05 — SC391 FaceFusion CRITICAL classification and Wan 2.7 upgrade are well-sourced; SC390 pricing implication reasoning is direct and correct; persistent DISCIPLINE ceiling)

---

### D2 — Execution Accuracy (20%) → 3.75/5.0 (→ 0.00)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| 3/3 DB clean pairs | SC389–SC391 all log correctly | ✅ |
| SC391: FaceFusion install code block updated to `git checkout 3.9.2` — production-ready fix | Converts research finding directly into actionable production artifact | ✅ |
| SC390: ElevenLabs pricing table updated model-by-model; historical note preserved; new "pricing update" section is additive | Structured execution; no prior context lost | ✅ |
| SC389: parseVtt() behavioral details AND v5.0 watch section both delivered in one cycle — two distinct deliverables | Efficient execution | ✅ |
| **CLAUDE.md P0: zero action** | Day 48 | ❌ DISCIPLINE |
| **O3 contradiction: zero action** | Day 71 | ❌ DISCIPLINE |

**Score: 3.75/5.0** (→ unchanged — execution quality consistent; SC391 code-block fix is the standout deliverable; O3 and P0 cap score)

---

### D3 — Memory & Continuity (15%) → 3.70/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC391 correctly upgrades Wan 2.7 R2V status that has been tracked since SC384 (Oct 27) — maintains version-history notes in commit and skill file | Long-running canary item resolved correctly; prior "unconfirmed" framing preserved as historical record | ✅ |
| SC390: May 7 PAYG pricing note preserved as historical baseline; Oct 5 cut added as additive note with clear before/after figures | Longitudinal pricing history maintained — avoids silent history rewrites | ✅ |
| SC389: cross-references SC382 (v4.0.539 status) and SC375 (parseVtt correction) in version footnote | Continuous accuracy across 14+ study cycles | ✅ |
| SC391: FaceFusion 3.9.1 section preserved as "historical record" after 3.9.2 section added | Correct continuity practice — does not delete prior version context | ✅ |
| **O3 action items: 71 days** | | ❌ DISCIPLINE |

**Score: 3.70/5.0** (↑ +0.05 — Wan 2.7 long-tracked status upgrade, ElevenLabs pricing history preservation, and FaceFusion version continuity are all strong memory signals)

---

### D4 — Reliability (20%) → 3.40/5.0 (↑ +0.10)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC391: FaceFusion 3.9.2 CRITICAL NVIDIA driver fix — catches a fatal crash risk before any production use of FaceFusion on a GPU machine | **Highest-value reliability finding this window** — would have caused QA pipeline crash on updated NVIDIA driver | ✅ |
| SC390: ElevenLabs v4 cost barrier removed — prevents false "v4 is more expensive" reasoning that would block a valid model upgrade | Corrects a decision-making constraint that was subtly wrong | ✅ |
| SC389: Remotion v5.0 license change pre-documented — prevents unexpected license non-compliance on upgrade | Proactive compliance gate before availability | ✅ |
| SC389: `<Sequence>` premount behavior documented — prevents subtle caption timing regression on v5.0 upgrade | Pre-emptive regression documentation | ✅ |
| DB compliance: 3/3 this window (100%); running tally: ~41/64 ≈ 64% (↑ from 62%) | Improving trend | ✅ |
| **CLAUDE.md P0 freeze: 48 days** | | ❌ DISCIPLINE |
| **O3 contradiction: 71 days** | | ❌ DISCIPLINE |

**Score: 3.40/5.0** (↑ +0.10 — SC391 CRITICAL crash prevention is the highest-value reliability signal in recent windows; SC389 license compliance pre-doc is strong proactive risk management; DB trend improving; discipline items remain ceiling)

---

### D5 — Integration (15%) → 3.75/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC391: Wan 2.7 R2V AIMLAPI pricing confirmed $0.65/5s — routing decision data now available vs Kling O1 $1.46/5s; model string canary specified | Actionable routing context; correctly staged behind canary | ✅ |
| SC391: FaceFusion install code block updated to `git checkout 3.9.2` — production-ready | Direct integration fix; no documentation gap between research and tooling | ✅ |
| SC390: ElevenLabs table reflects new $0.08/1K v3 rate — cost ceiling calculations ($15/video) now based on current prices | Budget integration accuracy improved | ✅ |
| SC389: `parseVtt()` comma-as-separator documented — prevents silent integration failure with subtitle providers using SRT-style VTT files | Subtle but critical interoperability fix | ✅ |
| **Wan 2.7 R2V binding syntax (Image1 vs character1) still unconfirmed on AIMLAPI** | ⚠️ Expected — canary item correctly flagged; next step is execution |
| **NB2.1 thinking_level: still unconfirmed on AIMLAPI** | ⚠️ Expected — canary item open |

**Score: 3.75/5.0** (↑ +0.05 — SC391 Wan 2.7 AIMLAPI pricing gives direct routing data; FaceFusion code-block fix is clean integration delivery; parseVtt comma detail prevents a real interop bug)

---

### D6 — Social / Communication (10%) → 3.75/5.0 (↑ +0.05)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC391 commit: "CRITICAL NVIDIA driver fatal error fix" + "Upgrade immediately" — correct escalation for severity | Not over-hedged; reader cannot miss urgency | ✅ |
| SC390 commit: "v4 now costs no more than v3; only the Dutch canary requirement blocks switching production" — direct actionable conclusion | No vagueness; owner can act on this sentence alone | ✅ |
| SC389 commit: "v5.0 NOT YET RELEASED (PR #3750 still open, npm latest = v4.0.539)" — concrete falsifiable state | Specific enough to verify; not "likely not released yet" | ✅ |
| SC389: License change flagged with "Action needed: verify Farouq's license tier before v5.0 upgrade" | Addressed by name; clear owner assignment | ✅ |

**Score: 3.75/5.0** (↑ +0.05 — SC391 CRITICAL framing and SC389 "Action needed" with owner name are the strongest communication deliverables this window)

---

### AUDIT 1 SUMMARY

| Dimension | Weight | Score | Contribution |
|-----------|--------|-------|-------------|
| D1 Reasoning | 20% | 3.60 | 0.720 |
| D2 Execution | 20% | 3.75 | 0.750 |
| D3 Memory | 15% | 3.70 | 0.5550 |
| D4 Reliability | 20% | 3.40 | 0.680 |
| D5 Integration | 15% | 3.75 | 0.5625 |
| D6 Social | 10% | 3.75 | 0.375 |
| **TOTAL** | | | **3.64/5.0** |

**Failure summary:**
- DISCIPLINE (dominant): CLAUDE.md P0 freeze 48 days; O3 contradiction generation-video.md day 71; pre-gen check wording day 116

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

### Skills Assessed This Window (SC389–SC391)

**captions-and-titles.md (SC389)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: `parseVtt()` comma separator documented; v5.0 `premountFor={0}` opt-out clearly stated; Automators license action flagged ✅
4. RFC 2119: "Action needed: verify Farouq's license tier before v5.0 upgrade" — mandatory framing ✅
5. Approval gates: v5.0 upgrade gated behind license verification; v4.0.539 still the install command ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: v5.0 not yet released; v4.0.539 remains current; no routing matrix conflict; bt709 color space note additive ✅

**Score: 8/8 (100%)** — parseVtt behavioral docs and v5.0 pre-release watch section are both production-relevant preventive documentation.

**halal-audio.md (SC390)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: New $0.08/1K v3 rate reflected in table; "always check elevenlabs.io/pricing/api before budgeting" maintained ✅
4. RFC 2119: "Verify current rates at elevenlabs.io/pricing before each production session" — imperative ✅
5. Approval gates: v4 canary still required before production switch; Dutch canary unchanged ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: v4 $0.08/1K confirmed = v3 post-cut — no conflict with CLAUDE.md $15/video ceiling; canary rule unchanged ✅

**Score: 8/8 (100%)** — Oct 5 price cut well-documented with source (usagepricing.com); practical implication stated directly; historical baseline note preserved.

**character-consistency.md (SC391)**
1. Description: Positive + negative triggers ✅
2. Stem: Imperative ✅
3. Explicit defaults: FaceFusion v3.9.2 now required; Wan 2.7 AIMLAPI confirmed live; canary required for binding syntax; both model string variants documented ✅
4. RFC 2119: "Upgrade immediately" for FaceFusion 3.9.2 — appropriately imperative for CRITICAL finding ✅
5. Approval gates: Wan 2.7 canary required before production use; both model string variants given with instruction to test both ✅
6. Length: Under 5000 words ✅
7. Negative triggers: `negatives:` field present ✅
8. Consistency: FaceFusion 3.9.2 consistent with FFmpeg 9.x pipeline; Wan 2.7 R2V $0.65/5s vs CLAUDE.md routing matrix (Wan 2.6 I2V as B-roll fallback — Wan 2.7 is additive upgrade at lower cost; no conflict) ✅

**Score: 8/8 (100%)** — CRITICAL crash prevention and Wan 2.7 AIMLAPI confirmation are both high-value outputs. FaceFusion code block updated to v3.9.2.

### Cross-Skill Consistency

| Check | Status |
|-------|--------|
| ElevenLabs v4 pricing ($0.08/1K = v3 post-cut): halal-audio.md vs CLAUDE.md (no ElevenLabs pricing in CLAUDE.md) | ✅ No conflict |
| FaceFusion v3.9.2: character-consistency.md vs post-production.md | ✅ No conflict — post-production.md does not reference FaceFusion version |
| Wan 2.7 R2V $0.65/5s: character-consistency.md vs CLAUDE.md routing matrix | ✅ Additive (CLAUDE.md lists Wan 2.6 I2V as B-roll fallback; Wan 2.7 R2V is upgrade path, not conflict) |
| Remotion v5.0 not yet released: captions-and-titles.md (SC389) vs post-production.md | ✅ Consistent |
| parseVtt() comma separator: captions-and-titles.md vs no other skill reference | ✅ No conflict |

**Cross-skill deductions: 0 (no mismatches this window)**

### CLAUDE.md Audit

| Component | Present | Status |
|-----------|---------|--------|
| Instruction count vs 150 limit | ~95 instructions | ✅ |
| Three-agent pattern | ✅ PLANNER/GENERATOR/EVALUATOR | ✅ |
| Snorkel triage | ✅ ZERO/3-5 taxonomy | ✅ |
| Model routing matrix | ✅ Present | ⚠️ Pricing errors persist — P0, day 48 |
| Brand binary checklist | ✅ All 6 items | ✅ |
| Production gates | ✅ All 10 | ⚠️ Pre-gen check #5/#7 wording — day 116 |

**CLAUDE.md deduction: −0.5 (unchanged — P0 items not fixed)**

### Hindsight / Memory Status

- `data/pipeline.db`: 64 tracked cycles; DB compliance 64% (↑ from 62% per Oct 29 audit)
- Feedback catalog: Current (pattern-extractor.py runs Sundays)
- Skill memory banks: captions-and-titles, halal-audio, character-consistency all updated Oct 29

### Gap Analysis

| Gap | Severity | Days Open |
|----|---------|-----------|
| Wan 2.7 R2V canary on AIMLAPI — **NOW CONFIRMED LIVE** ($0.65/5s) — model string, binding syntax, param schema unverified | 🔴 CRITICAL | NEW (SC391) — canary is now urgent, not exploratory |
| Kling v4 canary: audio (prompt mitigation documented SC388), face adherence, pricing ($0.785/5s MEDIUM confidence), prompt length (2500 char AIMLAPI vs 8000 token Kling) | 🔴 CRITICAL | 7 |
| CLAUDE.md pricing errors (P0) | 🟠 HIGH | 48 |
| O3 contradiction in generation-video.md | 🟠 HIGH | 71 |
| ElevenLabs v4 production canary — Dutch Willem, audio tags as speed replacement — **cost barrier now removed (SC390)** | 🟠 HIGH | 4 (escalated from MEDIUM — cost no longer blocking) |
| FaceFusion v3.9.2 upgrade on production GPU machine | 🟠 HIGH | NEW (SC391 CRITICAL) — upgrade before any FaceFusion run |
| NB2.1 production canary — thinking_level exposure, per-image billing at 1K/2K | 🟡 MEDIUM | 4 |
| Kling O3 canary on AIMLAPI | 🟡 MEDIUM | 71 |
| CLAUDE.md pre-gen check #5/#7 wording | 🟡 MEDIUM | 116 |
| Remotion v5.0 license tier verification (Farouq — SC389) | 🟡 MEDIUM | NEW — before v5.0 upgrade |
| Kling v4 prompt length: 8k tokens vs 2500 chars AIMLAPI | 🟡 MEDIUM | 1 |
| GPT Image 2.5 Flare/Sunburst AIMLAPI availability — CANARY | 🟢 LOW | 4 |
| MAI-Image 2.5 possible AIMLAPI deprecation (unconfirmed) | 🟢 LOW | 4 |

### Skill Score Calculation

| Category | Passes | Possible | Notes |
|----------|--------|----------|-------|
| Core skills (18 files × 8 criteria) | 143.25 | 144 | −0.75 pre-existing deductions (O3 contradiction in generation-video.md, unchanged) |
| CLAUDE.md structural components | 5.5 | 6 | −0.5 for pricing P0 items (unchanged) |
| Cross-skill consistency | 11 | 11 | No mismatches this window |
| **TOTAL** | **159.75** | **160** | **99.8%** |

**Target ≥95%: PASS → unchanged**

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved output:** V2-Proces (2026-04-12)
**Days since last approval:** **200 days**
**Output produced since Oct 29 audit:** None

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

1. **200 days. A symbolic number.** The pipeline hit its 200th day without a second approved video on this audit. The tooling is arguably better than it has ever been: NB2.1 template confirmed, v3 Pro parameters stable, Wan 2.7 AIMLAPI confirmed live at 2.2× cheaper than Kling O1, FaceFusion CRITICAL crash risk caught and flagged before production. A CD reviewing this would say: the research machine is excellent; the production machine has never started. These are not the same machine.
2. **Wan 2.7 R2V changes the routing economics, but no production brief has named it.** At $0.65/5s vs Kling O1 $1.46/5s, the case for using Wan 2.7 R2V on B-roll character shots is strong — but only once the canary confirms binding syntax. A CD would push to run the canary today. The info is there. The decision to act is not.
3. **FaceFusion 3.9.2 CRITICAL fix (SC391) highlights a systemic gap.** The QA pipeline caught a fatal crash risk from a third-party tool update — before any production run triggered it. This is the audit system working correctly. But a CD would note that this fix has been documented, not applied. The GPU machine may still be on v3.9.1. Application of the fix is the only thing that counts.

### Model Capability Notes (New Since Oct 29)

- **Wan 2.7 R2V on AIMLAPI (SC391)** — CONFIRMED LIVE; model string (`alibaba/wan-2-7-r2v` vs `alibaba/wan2.7-r2v`), binding syntax (Image1 vs character1), param schema — unverified. Classification: **INTEGRATION** (AIMLAPI parameter schema unknown — canary determines which path to use).
- **FaceFusion 3.9.2 CRITICAL (SC391)** — NVIDIA driver fatal crash on v3.9.1 on GPU machines with updated drivers. Classification: **OPERATIONAL** (tool upgrade required — not a model capability limit; a maintenance failure).
- **ElevenLabs v4 cost parity (SC390)** — v4 now same cost as v3 post-cut. Dutch canary is the only blocker. Classification: **OPERATIONAL** (canary not yet run — no architectural or ceiling barrier).

### Cost Metric

Credits per APPROVED video: **MATHEMATICALLY UNDEFINED** (0 approved videos since April 12, 2026)

### Predicted Pass Rate

**~73% confidence, 70% predicted pass rate** (→ unchanged)

- Upside: SC391 Wan 2.7 AIMLAPI confirmed live adds a lower-cost B-roll path; SC390 removes ElevenLabs v4 cost barrier; Kling v3 Pro parameters stable and confirmed
- Downside: Wan 2.7 binding syntax unverified; FaceFusion CRITICAL fix not yet applied; ElevenLabs v4 Dutch canary still pending; 200-day production gap; Kling v4 audio behavior still unverified

CREATIVE_AUDIT_COMPLETE

---

## TOP ACTION ITEMS (Prioritized)

| # | Priority | Action | Deadline |
|---|----------|--------|---------|
| 1 | 🔴 CRITICAL | **Run Wan 2.7 R2V canary on AIMLAPI.** Now confirmed live ($0.65/5s). Confirm: (a) model string (`"alibaba/wan-2-7-r2v"` vs `"alibaba/wan2.7-r2v"`), (b) binding syntax (Image1 vs character1), (c) param schema (reference_images key name, aspect_ratio format). This is the most actionable new canary in weeks — 2.2× cost reduction for B-roll character shots is realizable once confirmed. | Next session |
| 2 | 🔴 CRITICAL | **Run Kling v4 canary per credit-efficiency.md §CANARY sequence.** Confirm: (a) audio suppression via "no background music, no subtitles" prompt text, (b) face adherence vs v3 Pro baseline, (c) pricing confirmation ($0.157/sec MEDIUM confidence → HIGH confidence), (d) prompt length: 2,500-char AIMLAPI limit vs 8,000-token Kling guide. Day 7. | Next session |
| 3 | 🟠 HIGH | **Upgrade FaceFusion to v3.9.2 immediately** (`git checkout 3.9.2` in facefusion dir). CRITICAL NVIDIA driver fatal crash risk on v3.9.1. Do this before ANY FaceFusion QA run. | Before next FaceFusion run |
| 4 | 🟠 HIGH | **Fix CLAUDE.md pricing errors (P0)** — acknowledged as 5-min edit, day 48. | Immediate |
| 5 | 🟠 HIGH | **Run ElevenLabs v4 Dutch canary** — cost barrier removed (SC390: v4 = v3 in price). Test: Dutch `language_code="nl"`, audio tags as `speed=0.95` replacement, SNELVERHUIZEN IPA, `apply_text_normalization` on Willem voice. Only Dutch verification remains before production v4 switch. | Before next voiceover session |
| 6 | 🟠 HIGH | **Fix O3 contradiction in generation-video.md** — day 71. SC388–SC391 all touched the file or adjacent skills without addressing it. | This week |

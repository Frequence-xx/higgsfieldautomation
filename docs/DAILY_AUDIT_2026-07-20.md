# Daily Audit — 2026-07-20

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-07-19 | Operator 2.35/5.0 · Skills 86.9% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-07-19 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **2.33 / 5.0** | ↓ −0.02 | ↓ −1.52 |
| Skill Library & Policy | **86.9%** (139/160) | → 0.0% | ↓ −4.6% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Three study cycles (SC228–SC230) since the 2026-07-19 audit.** Protocol compliance: 1/3 (33%) clean pairs — down from 50% last window. SC228 is the worst single commit in recent history: ROOT pipeline.db + bundle (both violations simultaneously). SC229 is bundle-only (correct data/ path). SC230 is a clean pair.

**CRITICAL DATA INTEGRITY FINDING: SC229 claimed "Logged SC226-229 to pipeline.db (fill missing entries)" but data/pipeline.db study_log is still at max cycle=227. SC228, SC229, and SC230 entries are ALL absent from data/pipeline.db study_log.** ROOT pipeline.db study_cycles table captured SC228 (id=60) but not SC229 or SC230. This is the first window where a retroactive fill was claimed, appeared to have executed (data/pipeline.db binary changed), but failed to land entries in study_log.

**HIGHEST VALUE FINDING SC229: blockReason vs finishReason distinction eliminates wasted retry paths.** PROHIBITED_CONTENT is a distinct hard-ban (deepfake-like face+clothing+pose combinations) — skip retry, go direct to T2I fallback. July 15 false-positive wave correctly isolated to Google Flow only (NOT affecting AIMLAPI direct API calls). Seedream 5.0 Pro ref count corrected: 14 refs from AIMLAPI product page (overrides BytePlus 10-ref figure).

**SC230 clean pair with strong content: end_image_url vs tail_image_url (AIMLAPI v1/v1.6 + fal.ai v3 use end_image_url; native Kling API uses image_tail).** Also: v3 Motion Control duration limits confirmed from community data (10s max with Curve Dolly or Camera Shake, 6s with 3+ elements); background_source for MC documented.

**CLAUDE.md Pre-Gen Check #5 STILL WRONG (24th consecutive audit).** ElevenLabs v1 retirement STILL absent (11 days past, 24th flag). LTXV Aug 15 still in credit-efficiency.md only — 26 days remaining, 5th audit without CLAUDE.md action.

**87 days without approved creative output.**

---

## CHANGES SINCE 2026-07-19 AUDIT

Git commits since `b734cc2` (July 19 audit):

| Hash | Commit | Files | DB path | Protocol |
|------|--------|-------|---------|---------|
| f7b88a5 | SC228: Post-production (pass 31) — Remotion v4.0.491, liquidContours + skew documented | ROOT `pipeline.db` (57 KB) + `skills/post-production.md` | ROOT ✗ | ❌ ROOT DB + ❌ BUNDLE |
| 9884def | SC229: Hero frame generation (pass 34) — blockReason/finishReason distinction, Seedream 5.0 Pro 14-ref update | `data/pipeline.db` + `skills/generation-image.md` | `data/` ✓ | ❌ BUNDLE |
| e1159b6 | SC230: Kling v3 Pro parameters (pass 30) — end_image_url vs tail_image_url, MC v3 duration limits, background_source | `skills/generation-video.md` only | — | ✓ CLEAN CONTENT |
| 7090c0d | SC230 log: record study cycle 230 in pipeline.db | `data/pipeline.db` only | `data/` ✓ | ✓ CLEAN LOG (26s after content) |

**Protocol compliance this window:**
- Clean pairs (content-only commit + correct separate log): **1/3 (33%)** — SC230 ✓ only
- Bundled commits: 2/3 (67%) — SC228, SC229 — regression from 25% last window
- ROOT pipeline.db path errors: 1/3 (33%) — SC228 → **6th consecutive window** (SC209, SC212, SC217, SC222, SC226, SC228)
- SC229 retroactive fill: CLAIMED but FAILED — data/pipeline.db study_log still max cycle=227

**DB integrity cross-check (2026-07-20):**
- ROOT pipeline.db study_cycles: max cycle=228 (SC228 captured ✓, SC226 captured ✓)
- data/pipeline.db study_log: max cycle=227 (only SC227 from bundle)
- Missing from data/pipeline.db: SC226, SC228, SC229, SC230
- Missing from ROOT pipeline.db: SC224, SC225, SC227, SC229, SC230
- Neither DB has SC229 or SC230 logged

---

## SC CONTENT NOTES

**SC228** — `post-production.md` (f7b88a5, Sun Jul 19 06:08:40) — +109/−2 lines (net +107):
- **Remotion v4.0.491 (2026-07-18):** `liquidContours()` WebGL2 organic contour pattern — all params documented (firstColor/secondColor/spacing/scale/complexity/smoothness/seed/offsetX/offsetY/phase). Brand use: FC8434 + navy backdrop for title cards.
- **`skew()`:** WebGL2 perspective skew — x/y/origin params, −80 to 80 deg range. Brand use: x=8-15 on CTA pill/headline for forward-motion kinetic look.
- **`@remotion/media` confirmed stable** — already recommended path, no action needed.
- **Bundled FFmpeg binary drops `--enable-nonfree`** (libfdk_aac removed) — zero pipeline impact, system FFmpeg with built-in aac encoder.
- Tool confirmations: FFmpeg 8.1.2, SVT-AV1 v4.2.0, PySceneDetect v0.7.1 still in dev.
- Commit body: ✓ Detailed with bullet points.
- Protocol: ❌ ROOT `pipeline.db` + ❌ BUNDLE (both violations simultaneously — worst single commit this session).

**SC229** — `generation-image.md` (9884def, Sun Jul 19 12:12:40) — +15/−4 lines (net +11):
- **blockReason vs finishReason technical distinction [KEY]:** `prompt_feedback.blockReason` (SAFETY / IMAGE_SAFETY / BLOCKLIST / PROHIBITED_CONTENT / OTHER) vs `candidates[].finishReason` are separate fields. `PROHIBITED_CONTENT` is a hard-ban for deepfake-like ops (face+clothing+pose combinations) — do NOT retry, go direct to T2I fallback.
- **July 15, 2026 false-positive wave:** Blurred/blocked output was Google Flow only — NOT affecting AIMLAPI direct API calls. Prevents incorrect production halt diagnosis.
- **Seedream 5.0 Pro ref count corrected: 14 refs** (AIMLAPI product page) overrides BytePlus 10-ref figure. Documented in model table.
- **Decision flow updated:** blockReason PROHIBITED_CONTENT → skip retry → T2I fallback directly.
- Retroactive fill: commit body states "Logged SC226-229 to pipeline.db" but data/pipeline.db study_log shows no SC226/228/229 entries. The claim was inaccurate — entries did NOT land in study_log.
- Commit body: ✓ Present.
- Protocol: ❌ BUNDLE (data/pipeline.db + skill in same commit; data/ path correct ✓).

**SC230** — `generation-video.md` (e1159b6, Sun Jul 19 18:12:45) — +16/−4 lines (net +12):
- **end_image_url vs tail_image_url [CRITICAL for next I2V session]:** AIMLAPI v1/v1.6 + fal.ai v3 both use `end_image_url`. Native Kling API confirmed as `image_tail` (Griptape). Try `end_image_url` first on v3 Pro canary for end-frame compositing.
- **v3 Motion Control duration limits (community-confirmed, kling3.pro):** 10s max with Curve Dolly or Camera Shake; 8s with 2 elements; 6s with 3+ elements; O3 allows 15s (NOT on AIMLAPI).
- **`background_source` parameter** for v3 MC documented (value: `"input_video"`).
- **Curve Dolly + Camera Shake combinability confirmed**; combined duration still 10s cap on v3.
- Kling O3 and v3 Motion Control: still NOT on AIMLAPI (unchanged).
- Commit body: ✓ Detailed with 4 bullet points and sources.
- Protocol: ✓ CLEAN CONTENT.

**SC230 log** (7090c0d, Sun Jul 19 18:13:11):
- data/pipeline.db only → ✓ CLEAN LOG (correct path, 26s after content commit).
- study_log entry for cycle=230: NOT found in data/pipeline.db study_log (max still 227). The binary was updated but no study_log row for SC230 confirmed.

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 2.7/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC229: blockReason/finishReason distinction | Prevents $1.46 wasted on PROHIBITED_CONTENT retries; hard-ban category correctly identified with actionable decision path | Strong positive |
| SC229: July 15 false-positive isolation | Google Flow only; AIMLAPI unaffected — prevents incorrect production halt; evidence-based diagnosis | Strong positive |
| SC229: Seedream 5.0 Pro 14-ref from AIMLAPI product page | Overrides BytePlus 10-ref; immediately applicable for next hero frame session | Positive |
| SC230: end_image_url vs tail_image_url | 3-source confirmation (AIMLAPI v1/v1.6, fal.ai v3); native vs AIMLAPI distinction clearly documented | Strong positive |
| SC230: v3 MC duration limits from community source | Actionable planning data for next MC session; cap data by element count | Positive |
| SC228: liquidContours/skew with brand use cases | FC8434 + navy backdrop, x=8-15 for CTA — brand-specific application documented | Positive |
| SC229: Retroactive fill claimed but not delivered | Commit body said "Logged SC226-229" — study_log shows no change. False confidence about data integrity. | Negative |
| **CLAUDE.md Pre-Gen Check #5 wrong (24th audit)** | "15-40 words" still wrong for Kling v3; 2.3 rerolls average per character shot | Critical negative |
| **ElevenLabs v1 — 11 DAYS PAST (24th flag)** | Still absent from CLAUDE.md; SC229 is hero-frame domain (not halal audio) but no cross-domain propagation | Critical negative |
| **LTXV Aug 15 — 26 days (5th audit without CLAUDE.md alert)** | credit-efficiency.md has escalation plan; CLAUDE.md routing matrix silent | Negative |

**Score: 2.7/5.0** (↑ +0.1 — SC229's blockReason/finishReason distinction and SC230's end_image_url clarification are both strong precision-reasoning signals that prevent expensive production errors; SC228's brand use cases for Remotion effects show applied reasoning; persistent CLAUDE.md non-propagation and SC229's inaccurate retroactive fill claim are offsets)

---

### D2 — Execution Accuracy (20%) → 1.7/5.0 (↓ −0.2)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC228 | ROOT `pipeline.db` + skill in same commit | ❌❌ ROOT DB + BUNDLE (worst combo) |
| SC229 | `data/pipeline.db` + `skills/generation-image.md` in same commit | ❌ BUNDLE (correct path) |
| SC230 | Content-only (generation-video.md) + `data/pipeline.db` log 26s later | ✓ CLEAN PAIR |
| Clean pairs this window | **1/3 (33%)** — down from 2/4 (50%) | ↓ Regression |
| Bundling rate | 2/3 (67%) — up from 1/4 (25%) last window | ❌ Regression |
| ROOT DB error | SC228 — **6th consecutive window** (SC209, SC212, SC217, SC222, SC226, SC228) | ❌ Entrenched |
| SC229 retroactive fill | Claimed but not executed — study_log unchanged | ❌ Execution failure |
| SC230 log entry | data/ path correct; study_log entry for SC230 not confirmed in DB | ↓ Partial |

**Score: 1.7/5.0** (↓ −0.2 — SC228 ROOT+BUNDLE is the worst single commit in recent windows; bundling rate regressed from 25% to 67%; SC229 retroactive fill claimed but not delivered; SC230 clean pair is a positive signal but insufficient to offset; ROOT DB error enters 6th consecutive window with no structural fix in sight)

---

### D3 — Memory & Continuity (15%) → 2.2/5.0 (↓ −0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC229: 14-ref self-correction | AIMLAPI product page overrides BytePlus 10-ref — corrects a practical production constraint | Positive |
| SC228: Tool version confirmations with dates | FFmpeg 8.1.2, SVT-AV1 v4.2.0, PySceneDetect v0.7.1 dev — all confirmed current | Positive |
| SC230: 3-source end_image_url confirmation | AIMLAPI v1, v1.6, fal.ai v3 cross-referenced — multi-source evidence | Positive |
| SC229: Retroactive fill FAILED | data/pipeline.db study_log unchanged at max cycle=227; SC226/228/229/230 all absent | Critical negative |
| SC228/229/230 absent from data/pipeline.db | study_log doesn't capture this window — future sessions relying on study_log miss all new knowledge | Negative |
| SC230 study_log entry absent | Even the clean log pair (7090c0d) didn't land a cycle=230 row in study_log | Negative |
| SC166 absent (19th audit) | Differential prompt rule still not in model-prompting-guide.md Part 4 | Negative |

**Score: 2.2/5.0** (↓ −0.1 — the retroactive fill failure is the dominant negative signal this window; SC229's data/pipeline.db write was a phantom for study_log purposes; SC228/229/230 are unlogged in data/pipeline.db; individual SC content quality remains positive but the database that stores "what we learned" is now 4 cycles behind)

---

### D4 — Reliability & Consistency (20%) → 1.4/5.0 (↓ −0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC230: Clean pair | Content-only then separate data/ log 26s later — protocol executable | ✓ Positive |
| SC228: ROOT+BUNDLE | Worst-of-both violation; 6th consecutive ROOT error | ❌ Critical structural |
| SC229: Retroactive fill inaccurate | Committed with false statement about DB fill | ❌ Integrity issue |
| Bundling rate | 67% this window vs 25% last window — regression | ❌ |
| CLAUDE.md frozen | **24th consecutive audit without update** | ❌ Critical structural |
| model-ceiling-detection.md C8 | Veo 3.1 Lite I2V in escalation path — **20th consecutive audit** | ❌ Operational |
| SC166 absent | **19th audit** | Negative |
| 87 days without approved output | Zero creative output — production reliability = 0 vs goal | Negative |
| Clean pair rate trend | 33% (this) vs 50% (prev) vs 33% (two prior) — oscillating, not improving | Negative |

**Score: 1.4/5.0** (↓ −0.1 — SC230 clean pair is positive; SC228's dual violation and SC229's inaccurate retroactive fill claim both damage reliability; bundling rate regressed; CLAUDE.md frozen 24 consecutive audits; ROOT DB error in 6th window shows no structural fix is in progress)

---

### D5 — Tool/Model Integration (15%) → 4.0/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC230: end_image_url vs tail_image_url | Prevents wrong-parameter failure on next I2V end-frame session; 3-source confirmed | Strong positive |
| SC230: v3 MC duration limits | 10s/8s/6s by element count — critical for MC session planning | Positive |
| SC229: blockReason/finishReason | Hard-ban route to T2I fallback — prevents retry waste; July 15 Google Flow isolation protects from false halt | Strong positive |
| SC229: Seedream 5.0 Pro 14-ref | Applicable to next hero frame session with multi-ref character compositing | Positive |
| SC228: liquidContours/skew params | All params documented with brand-specific use cases; immediately applicable for CTA cards | Positive |
| **CLAUDE.md 15-40w still wrong (24th)** | Active wrong guidance; 2.3 rerolls per character shot | Critical negative |
| ElevenLabs v1 (24th) | CLAUDE.md Check #7 silent on retirement — guaranteed 404 at next voiceover session | Critical negative |
| LTXV Aug 15 (5th audit) | credit-efficiency.md has plan; CLAUDE.md routing matrix still silent | Negative |
| SC229 retroactive fill failure | next session querying study_log misses SC228-230 learnings | Negative |

**Score: 4.0/5.0** (↑ +0.1 — 3 SC windows with actionable integration advances: end_image_url prevents parameter errors, blockReason eliminates retry waste, liquidContours/skew enables new post-production capability; persistent CLAUDE.md divergences accumulate but the raw skill knowledge quality is high)

---

### D6 — Communication & Social (10%) → 2.4/5.0 (→ unchanged)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC228 commit body | Detailed: 4 bullet points (liquidContours params, skew params, @remotion/media, FFmpeg nonfree drop) | ✓ Strong positive |
| SC229 commit body | Present: blockReason distinction, Seedream 14-ref, retroactive fill (inaccurate claim noted) | ✓ Present |
| SC230 content body | Detailed: 4 bullet points with source citations (community data, Griptape) | ✓ Strong positive |
| SC230 log body | Standard log message | ✓ |
| **All 3 SC content commits have bodies** | Recovery from SC225+SC226 (no bodies) — 3 consecutive SC commits with bodies | Strong positive |
| **Telegram BOT_TOKEN unconfigured** | **55th consecutive audit without delivery** | Systemic negative |
| ElevenLabs non-escalation (24th) | CRITICAL overdue issue not reaching owner | Persistent negative |
| LTXV deadline non-escalation | 26 days — not reaching owner | Negative |
| SC229 retroactive fill inaccuracy in body | Commit body claims data recovery that didn't happen — misleading for future debugging | Negative |

**Score: 2.4/5.0** (→ unchanged — all 3 SC content commits have bodies this window, maintaining the D6 recovery from last window's SC225/SC226 body absence; SC229 body's inaccurate retroactive fill claim is a new concern; Telegram and escalation gaps unchanged)

---

### AUDIT 1 WEIGHTED TOTAL

| Dimension | Weight | Prev Score | New Score | Change | Weighted |
|-----------|--------|-----------|-----------|--------|----------|
| D1 Reasoning | 20% | 2.6 | 2.7 | ↑ +0.1 | 0.540 |
| D2 Execution | 20% | 1.9 | 1.7 | ↓ −0.2 | 0.340 |
| D3 Memory | 15% | 2.3 | 2.2 | ↓ −0.1 | 0.330 |
| D4 Reliability | 20% | 1.5 | 1.4 | ↓ −0.1 | 0.280 |
| D5 Integration | 15% | 3.9 | 4.0 | ↑ +0.1 | 0.600 |
| D6 Social | 10% | 2.2 | 2.4 | ↑ +0.2 | 0.240 |
| **TOTAL** | 100% | **2.35** | | | **2.33 / 5.0** |

**Operator Performance: 2.33/5.0** (↓ −0.02 from 2.35 — effectively unchanged; D1/D5/D6 improved from strong SC content and body recovery; D2/D3/D4 declined due to SC228 ROOT+BUNDLE, retroactive fill failure, and bundling rate regression)

**Failure classifications this window:**
- SC228 ROOT DB + BUNDLE (simultaneously) → DISCIPLINE (6th consecutive ROOT window)
- SC228/229 bundled commits → DISCIPLINE
- SC229 retroactive fill failure (inaccurate commit body) → DISCIPLINE
- SC228-230 absent from data/pipeline.db study_log → ARCHITECTURAL (wrong DB schema still in use for some writes)
- CLAUDE.md frozen 24 consecutive audits → DISCIPLINE (dominant pattern)
- CLAUDE.md Pre-Gen Check #5 wrong (24th) → DISCIPLINE
- model-ceiling-detection.md C8 (20th audit) → OPERATIONAL
- Telegram BOT_TOKEN unconfigured (55th) → ARCHITECTURAL

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

### Files Updated This Window (3 files)

**`post-production.md`** — SC228 (+109/−2) ≈ ~11,575 words

| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Total |
|----|----|----|----|----|----|----|----|----|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | **7/8** |

C6 fail (~11,575 words; was ~10,695 + ~880 net new). SC228 additions are factually correct: liquidContours/skew params with dated version (v4.0.491 2026-07-18), brand use cases. No C8: CLAUDE.md has no Remotion version specifics. Score: **7/8** (unchanged).

---

**`generation-image.md`** — SC229 (+15/−4) ≈ ~12,490 words

| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Total |
|----|----|----|----|----|----|----|----|----|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | **7/8** |

C6 fail (~12,490 words). blockReason/finishReason distinction is a CRITICAL correctness update — PROHIBITED_CONTENT hard-ban prevents wasted retries. July 15 false-positive isolation is evidence-based. Seedream 5.0 Pro 14-ref from AIMLAPI source. No C8: CLAUDE.md routing matrix doesn't reference blockReason handling or Seedream 5.0 Pro. Score: **7/8** (unchanged).

---

**`generation-video.md`** — SC230 (+16/−4) ≈ 807+ words estimate (net +12 lines)

| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Total |
|----|----|----|----|----|----|----|----|----|
| ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ | **4/8** |

Wait — re-checking against previous audit: generation-video.md was 6/8 (C6 + C8 fails). The C2 and C5 failures are for cinematic-standards/kling-truck/etc. NOT generation-video. Let me use carry-forward:

| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Total |
|----|----|----|----|----|----|----|----|----|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ | **6/8** |

C6 fail (was already over 5,000 words; SC230 net +12 lines doesn't resolve this). C8 fail: CLAUDE.md "15-40 words" vs skill "40-120w I2V" — SC230 didn't modify the prompt length section. SC230 additions (end_image_url, MC duration limits, background_source) don't create new C8 violations (CLAUDE.md doesn't reference these parameters). Score: **6/8** (unchanged).

---

### Carry-Forward Scores (17 unchanged files)

| Skill File | Score | Notes |
|------------|-------|-------|
| anti-sycophancy.md | 8/8 | Unchanged |
| brand-identity.md | 8/8 | Unchanged |
| brief-intake.md | 8/8 | Unchanged |
| production-checklist.md | 8/8 | Unchanged |
| video-qa-rubric.md | 8/8 | Unchanged |
| model-prompting-guide.md | 7/8 | C6 fail (~5,341 words); SC166 diff prompt rule absent (**19th audit**) |
| shariah-compliance.md | 7/8 | C2 fail |
| higgsfield-generation.md | 7/8 | C5 fail |
| generation-image.md | 7/8 | C6 fail (~12,490 words) — SC229 |
| post-production.md | 7/8 | C6 fail (~11,575 words) — SC228 |
| captions-and-titles.md | 7/8 | C6 fail (~7,850 words) |
| halal-audio.md | 7/8 | C6 fail (~11,615 words) |
| character-consistency.md | 7/8 | C6 fail (~8,790 words) |
| credit-efficiency.md | 7/8 | C6 fail (~15,727 words) |
| cinematic-standards.md | 6/8 | C2 + C5 fail |
| kling-truck-prompting.md | 6/8 | C2 + C5 fail |
| model-ceiling-detection.md | 6/8 | C2 fail + C8 fail (Veo 3.1 Lite I2V — **20th consecutive audit**) |
| text-overlay-compositing.md | 6/8 | C2 + C5 fail |
| viral-research.md | 6/8 | C2 + C5 fail |
| generation-video.md | 6/8 | C6 fail + C8 fail (CLAUDE.md 15-40w vs skill 40-120w I2V — **24th audit**) |

---

### Skill Library Score

```
Files:                   20 total
Points earned:           139 / 160
Percentage:              86.9%
Target:                  ≥ 95.0%
Gap:                     −8.1% (13 points needed)

8/8 files (5):  anti-sycophancy, brand-identity, brief-intake, production-checklist, video-qa-rubric
7/8 files (9):  model-prompting-guide, shariah-compliance, higgsfield-generation, generation-image,
                post-production, captions-and-titles, halal-audio, character-consistency, credit-efficiency
6/8 files (6):  cinematic-standards, kling-truck-prompting, model-ceiling-detection,
                text-overlay-compositing, viral-research, generation-video

C6 failures (>5,000 words): 9/20 (45%) — unchanged
C2 failures (non-imperative stem): 5/20 (25%) — unchanged
C5 failures (no approval gate): 5/20 (25%) — unchanged
C8 failures (CLAUDE.md inconsistency): 2/20 (10%) — unchanged

Library word count: ~97,153 words (+380 net from SC228–SC230)
```

Calculation: (5 × 8) + (9 × 7) + (6 × 6) = 40 + 63 + 36 = **139/160 = 86.9%**

**Skill Library & Policy: 86.9% (139/160)** (→ unchanged — all 3 SC content updates are factually correct with no new C8 violations; structural gaps (C6 word count, C2 stems, C8 CLAUDE.md divergence) require owner-approved refactoring to resolve)

---

### CLAUDE.md Structural Audit

CLAUDE.md **unchanged — 24th consecutive audit without update.**

| Component | Status |
|-----------|--------|
| Three-agent pattern | ✓ Present |
| Snorkel triage | ✓ Present |
| Model routing matrix | ✗ STALE: Seedream 5.0 Pro ($0.06/img — **8th audit**); Kling O1 I2V ($0.73/5s — **10th audit**); Hailuo 2.3 Fast ($0.0416/sec — **13th audit**); NB2 Lite ($0.044 — **14th audit**); Wan 2.7 R2V (absent); Krea WAN 14B T2V (absent); Imagen 4 (retired June 24 — **26 days past**) |
| Brand binary checklist | ✓ Present |
| Production gates | ✓ Present |
| Pre-generation checks | ✗ STALE: **Check #5: "15-40 words" → WRONG (24th audit)**; Check #9 deprecated syntax (`face adherence 80-90` → `face_consistency: true`); Check #7 missing ElevenLabs v1 retirement (**11 days overdue**) |
| **ElevenLabs v1 removal** | **✗ ABSENT — RETIRED JULY 9. 11 DAYS PAST. 24th consecutive flag. PRODUCTION BLOCKER.** |
| **CLAUDE.md Pre-Gen Check #5** | **✗ WRONG — "15-40 words" is Kling v1/v2. Kling v3 Pro I2V: 40-120 words. 24th consecutive flag.** |
| **LTXV 2.3 auto-routing warning** | **✗ ABSENT — 26 DAYS REMAINING. 5th consecutive audit without CLAUDE.md action.** |
| end_image_url parameter | ✗ ABSENT — SC230; AIMLAPI uses `end_image_url` (not `image_tail`); no C8 |
| MC duration limits | ✗ ABSENT — SC230; 10s/8s/6s caps not in CLAUDE.md; no C8 |
| blockReason routing | ✗ ABSENT — SC229; PROHIBITED_CONTENT → direct T2I fallback not in CLAUDE.md; no C8 |
| Seedream 5.0 Pro 14-ref | ✗ ABSENT — SC229; CLAUDE.md doesn't reference Seedream; no C8 |
| language_code gap (multilingual_v2) | ✗ ABSENT — SC225; no direct C8 but production gap |
| Wan 2.7 R2V "mute" parameter | ✗ ABSENT — SC226; no C8 |
| model-ceiling-detection.md C8 | ✗ Veo 3.1 Lite I2V in escalation path — **20th audit without fix** |
| SC166 differential prompt rule | ✗ ABSENT from model-prompting-guide.md Part 4 — **19th audit** |
| NB2=NBP OTHER policy | ✗ ABSENT — SC222; step (5) fallback guidance stale |
| Kling O1 I2V pricing | ✗ STALE — still in routing matrix; 10th audit without update |

**New gaps/changes this window:**
- SC228: Remotion v4.0.491 liquidContours/skew — CLAUDE.md has no Remotion version references; no C8 but post-production capability available in skill only
- SC229: blockReason routing and Seedream 14-ref — CLAUDE.md absent; no C8
- SC230: end_image_url, MC duration limits — CLAUDE.md absent; no C8
- All other gap ages +1. **Zero gaps resolved this window.**

### Hindsight Status

Hindsight daemon: **NOT running** (last log entry: 2026-04-13 15:14:48 UTC — 98 days ago). Banks unverified since April. Recall: non-functional. This is a persistent ARCHITECTURAL issue; the daemon hasn't been active since early in the pipeline's life.

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved video:** V3-Tarik-v2-couple (2026-04-26) — **87 days ago.** No new creative output since July 19 audit.

**Family lock status:** `testimonial` family, 3/6 videos approved. 3 more required before family unlock (lock_until: 6).

**Cost metric:** Credits per approved video = MATHEMATICALLY UNDEFINED (zero new output, day 87).

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

### New Production Intelligence (SC228–SC230)

**Post-production (SC228):**
- `liquidContours()` in Remotion v4.0.491 — WebGL2 organic contour; FC8434 + navy backdrop for title cards.
- `skew()` — perspective kinetic effect; x=8-15 for CTA pill/headline forward-motion look.
- System FFmpeg unaffected by bundled FFmpeg --enable-nonfree drop.

**Hero frame generation (SC229):**
- **`blockReason PROHIBITED_CONTENT` = hard-ban** (deepfake-like face+clothing+pose). Skip retry → T2I fallback directly. Do NOT pass `image_url` on next call.
- July 15, 2026 blockReason OTHER false-positive wave: Google Flow only. AIMLAPI direct API calls unaffected — do not halt production on this basis.
- **Seedream 5.0 Pro max refs: 14** (AIMLAPI product page; overrides 10-ref BytePlus claim).

**Video generation (SC230):**
- **`end_image_url`** is the correct AIMLAPI/fal.ai v3 parameter for end-frame compositing (NOT `tail_image_url`). Native Kling API uses `image_tail`. Canary required before first use on AIMLAPI v3 Pro.
- v3 Motion Control duration caps: 10s (1 element), 8s (2 elements), 6s (3+). Plan shot list within these limits.
- `background_source: "input_video"` for MC on v3.

### Workflow Gaps (updated)

- No approved clips → production gates 1–10 not testable this window.
- **CLAUDE.md Pre-Gen Check #5 still wrong (24th audit).** "15-40 words" → 2.3 rerolls average on Kling v3 Pro character shots. Required fix before any character shot session.
- **ElevenLabs v1 confirmed retired July 9.** Now 11 days past. Next voiceover session → guaranteed 404. `eleven_v3` is production; `eleven_flash_v2_5` is draft. 24th consecutive flag without CLAUDE.md update.
- **`blockReason PROHIBITED_CONTENT` → direct T2I fallback (NEW SC229).** If AIMLAPI returns this on any hero frame, do NOT retry I2I — go directly to T2I fallback. Prevents $0.20 NBP Edit retry that will also block.
- **LTXV Aug 15 deadline (SC227):** 26 days remaining. B-roll sessions after Aug 15 → silent failure without CLAUDE.md update or session-start check.
- **SC228-230 absent from data/pipeline.db study_log.** A session querying study_log for recent learnings will miss: liquidContours/skew, blockReason/finishReason, end_image_url, MC duration limits.
- **model-ceiling-detection.md C8 (20th audit):** Veo 3.1 Lite I2V in escalation path is wrong. One-line removal.

### Ralph Loop

*"What would a senior creative director still reject?"*

1. **The data/pipeline.db study_log is structurally out of sync with the active learning cycle.** The last confirmed entry is SC227 (2026-07-19). SC228's high-value Remotion v4.0.491 additions, SC229's blockReason/finishReason distinction, and SC230's end_image_url clarification are all absent. A production session that opens study_log to check "what did we learn recently?" will see nothing after SC227 and assume the knowledge base is current. The PROHIBITED_CONTENT → T2I fallback route (SC229) is exactly the kind of decision that prevents a wasted $0.20 hero frame retry — but it's not in the log a production session would query.

2. **LTXV Aug 15 window is now 26 days.** credit-efficiency.md has the escalation plan (Aug 1 check, Aug 10 escalate). CLAUDE.md routing matrix shows B-roll via "Veo 3.1 Lite T2V | $0.52 | Kling v3 Standard" with no LTXV reference. If a B-roll session uses `ltxv/ltxv-2-fast` after Aug 15 without a CLAUDE.md alert or a pre-session check, the call errors silently — the operator sees a timeout or 404 and doesn't know why. The 15-minute CLAUDE.md patch (add one line to B-roll row) has been outstanding for 5 audits. The window is closing.

3. **87 days of approved video drought while the knowledge base grows.** SC228-230 add meaningful production capability (Remotion v4.0.491 effects, blockReason routing, end_image_url, MC duration limits). The pipeline can now plan a v3 Motion Control shot with correct duration limits, recover from PROHIBITED_CONTENT blocks without retry waste, and use end_image_url for end-frame compositing. None of these improvements are in CLAUDE.md. The gap between skill knowledge and CLAUDE.md operational guidance is at its widest point. A 15-minute CLAUDE.md update (Check #5 prompt length, Check #7 ElevenLabs retirement, LTXV routing alert, end_image_url note) would raise the predicted pass rate from ~20% to ~75%.

**Overall Creative: (3.9 + 4.2 + 4.1) / 3 = 4.07 / 5.0** (→ unchanged, day 87 of production stagnation)

CREATIVE_AUDIT_COMPLETE

---

## ACTION ITEMS

### [P0 — CRITICAL — 24th audit — CLAUDE.md Pre-Gen Check #5 Wrong Prompt Length]

**1. Fix "15-40 words" to Kling v3-correct range**

```
Current:  Motion prompt: 15-40 words, motion ONLY, defined endpoint ("eases to stop")
Correct:  Motion prompt: I2V 40-120 words / T2V 80-150 words (Kling v3 Pro, July 2026).
          Motion ONLY — action arc + camera move + defined endpoint. (15-40w was Kling v1/v2.)
```

Impact: every character shot session averages 2.3 rerolls at $1.46 each under current guidance.

---

### [P0 — CRITICAL — OVERDUE 11 DAYS — ElevenLabs RETIREMENT — 24th audit]

**2. CLAUDE.md Pre-Gen Check #7 — v1 retirement + language_code note + Check #9 syntax fix**

```
⚠️ RETIRED JULY 9, 2026: eleven_monolingual_v1 + eleven_multilingual_v1 + scribe_v1 → 404 NOW.
Use eleven_v3 (TTS production) + eleven_flash_v2_5 (TTS draft) + scribe_v2 (captions).
NOTE: language_code NOT supported on eleven_multilingual_v2 (silently ignored, June 29, 2026).
Use eleven_v3 for Dutch phone/proper-noun pronunciation.
grep -r "monolingual_v1\|multilingual_v1\|scribe_v1" scripts/ before voiceover work.
```

Fix Check #9 syntax: `face adherence 80-90 (NOT default 42)` → `face_consistency: true`

---

### [P0 — 26-DAY DEADLINE — LTXV Aug 15 Alert]

**3. CLAUDE.md routing matrix B-roll row — add LTXV 2.3 string alert**

```
⚠️ LTXV DEADLINE Aug 15 (26 days): ltxv/ltxv-2-fast auto-routes to LTX-2.3 now.
String WILL ERROR after Aug 15. Monitor docs.aimlapi.com by Aug 1.
If ltxv/ltxv-2-3-fast not live by Aug 10 → owner escalation + route to Hailuo 2.3 Fast ($0.0416/sec).
```

---

### [P0 — DATA INTEGRITY — study_log missing SC228-230]

**4. Retroactively insert SC226-230 into data/pipeline.db study_log**

SC229 claimed to fill SC226-229 but study_log still max cycle=227. SC230 also absent. ROOT pipeline.db study_cycles has SC226 (id=59) and SC228 (id=60) as fallback reference.

```sql
INSERT INTO study_log (cycle, topic, pass_number, findings, files_updated, created_at) VALUES
  (228, 'Post-production', 31, 'Remotion v4.0.491 liquidContours + skew documented; FFmpeg nonfree drop', 'skills/post-production.md', '2026-07-19 06:08:40'),
  (229, 'Hero frame generation', 34, 'blockReason PROHIBITED_CONTENT hard-ban; July 15 Google Flow isolation; Seedream 14-ref correction', 'skills/generation-image.md', '2026-07-19 12:12:40'),
  (230, 'Kling v3 Pro parameters', 30, 'end_image_url (AIMLAPI/fal); MC duration limits 10/8/6s; background_source', 'skills/generation-video.md', '2026-07-19 18:12:45');
```

And fix SC226 entry which is only in ROOT study_cycles (id=59). Root cause of ROOT DB path error still NOT fixed.

---

### [P0 — OPERATIONAL — model-ceiling-detection.md C8 — 20th consecutive audit]

**5. Remove Veo 3.1 Lite I2V from video escalation path**

One-line removal. Veo 3.1 Lite is T2V only. NEVER use I2V on this model. **20th consecutive audit without fix.**

---

### [P0 — BEFORE NEXT I2V SESSION — end_image_url canary]

**6. Apply SC230: `end_image_url` parameter for Kling v3 Pro I2V end-frame compositing**

```python
# AIMLAPI v3 Pro I2V — end frame parameter (SC230, 3-source confirmed)
payload = {
    "model": "klingai/video-v3-pro-image-to-video",
    "image_url": "<start_frame_cdn_url>",
    "end_image_url": "<end_frame_cdn_url>",   # NOT tail_image_url
    ...
}
# Native Kling API uses image_tail — do NOT use image_tail with AIMLAPI
```

---

### [P1 — BEFORE NEXT HERO FRAME SESSION]

**7. blockReason routing (SC229):**
- `PROHIBITED_CONTENT` → skip ALL retries → T2I fallback immediately
- `OTHER` → standard retry with simplified prompt (no face-swap inputs)
- July 15 false-positive: do NOT halt production; check if call went via Google Flow vs AIMLAPI direct

**8. Seedream 5.0 Pro ref count (SC229):**
- Max refs on AIMLAPI: 14 (from AIMLAPI product page — overrides BytePlus 10-ref)
- Use `image_urls` array up to 14 refs on production calls

**9. LTXV session pre-check (SC227):**
- Before any B-roll session: verify `ltxv/ltxv-2-3-fast` on docs.aimlapi.com
- After Aug 15 if not live: `minimax/hailuo-2.3-fast` ($0.0416/sec), `generate_audio: false`

**10. Remotion v4.0.491 effects (SC228):**
- `liquidContours()`: `firstColor="#FC8434"`, `secondColor="#001a33"` for brand title cards
- `skew()`: `x={12}` on CTA pill for forward-motion kinetic look
- Both in `@remotion/effects` — no new package install needed

**11. model-prompting-guide.md Part 4 — SC166 differential prompt rule (19th audit)**

```
On facial-movement retries: use action-only prompts; strip identity-descriptive words.
(Validated: DomainShuttle DualRoPE arXiv 2606.26058)
```

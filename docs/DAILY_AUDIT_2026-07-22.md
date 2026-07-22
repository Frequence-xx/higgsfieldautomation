# Daily Audit — 2026-07-22

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-07-21 | Operator 2.53/5.0 · Skills 86.9% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-07-21 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **2.54 / 5.0** | ↑ +0.01 | ↓ −1.31 |
| Skill Library & Policy | **87.5%** (140/160) | ↑ +0.6% | ↓ −4.0% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Four study cycles (SC235–SC238) since the 2026-07-21 audit.** Operator score is essentially flat — strong integration content (camera_control API correction, Turbo Pro HIGH confidence) masked by a sharp protocol regression: bundling rate surged from 0% to 75% (3/4 cycles bundled), wiping out last window's breakthrough. One major structural improvement: ROOT pipeline.db path error streak ended (8 consecutive windows → 0 this window; all DB operations landed in `data/pipeline.db`). CLAUDE.md remains frozen for the **26th consecutive audit**.

**SC237 is the highest-value finding this window:** camera presets orbit/crane/boom/handheld are Kling UI Inspiration panel presets — NOT `camera_control.type` API values. The 6 API types are the complete set. If used incorrectly, a production call returns invalid type errors or silently ignores the parameter. Additionally: fal.ai's Kling I2V wrapper silently caps elements at 1 (vs native/AIMLAPI 3) — do NOT copy elements code from fal.ai examples.

**SC237 also upgrades Turbo Pro character consistency confidence to HIGH** — multi-source July 2026 confirmation that wardrobe and face hold across multi-shot cuts. This is the first time in session history a cheaper character animation tier has reached HIGH quality confidence. Canary for AIMLAPI cost/audio confirmation is required before production use, but quality risk is now LOW.

**89 days without approved creative output.** 26 days to LTXV Aug-15 deadline with no CLAUDE.md routing alert. 13 days past ElevenLabs v1 retirement with no CLAUDE.md fix.

---

## CHANGES SINCE 2026-07-21 AUDIT

Git commits since `970b016` (July 21 audit):

| Hash | Commit | Files changed | DB path | Protocol |
|------|--------|---------------|---------|---------|
| de77584 | SC235: Post-production (pass 32) — Remotion v4.0.495, Sequence opacity fix, wave()/noiseDisplacement() documented | `skills/post-production.md` + `data/pipeline.db` | `data/` ✓ | ❌ BUNDLED |
| b70bc9d | SC235 log: record study cycle 235 in pipeline.db | `data/pipeline.db` only | `data/` ✓ | → extra log (SC235 DB already written in de77584) |
| ea18cbb | SC236: Hero frame generation (pass 35) — Meta Muse Image (no API), FLUX.2 Max/Edit docs still absent 2026-07-21, Gemini Omni Flash still not on AIMLAPI, MAI-Image 2.5 Flash pricing confirmed | `skills/generation-image.md` only | — | ✓ CLEAN CONTENT (no dedicated log) |
| 90c3203 | SC237: Kling v3 Pro parameters (pass 31) — camera preset UI vs API clarification, fal.ai elements limit, Turbo Pro quality confirmation | `skills/generation-video.md` + `data/pipeline.db` | `data/` ✓ | ❌ BUNDLED |
| 7040a43 | SC237 log: update commit hash for SC236 and SC237 in pipeline.db | `data/pipeline.db` only | `data/` ✓ | → retroactive SC236 log via SC237 commit |
| 0858262 | SC238: Caption pipeline (pass 36) — Remotion 4.0.496, FFmpeg 8.0 whisper filter clarification | `skills/captions-and-titles.md` + `data/pipeline.db` | `data/` ✓ | ❌ BUNDLED |
| d192a92 | SC238 log: record study cycle 238 commit hash in pipeline.db | `data/pipeline.db` only | `data/` ✓ | → separate log |

**Protocol compliance this window:**
- Clean pairs (skill-only content commit + dedicated log commit): **0/4 (0%)** — worst in recorded session history (last window: 3/4 = 75%)
- Bundled commits: **3/4 (75%)** — major regression from 0/4 (0%) last window (SC235, SC237, SC238 all bundled skill+DB in content commit)
- ROOT pipeline.db path errors: **0/4** — ROOT error streak ENDED (was 7 consecutive windows: SC209, SC212, SC217, SC222, SC226, SC228, SC233). All DB operations landed in `data/pipeline.db`. **First ROOT-clean window in 8 windows.** ✓
- SC236: clean content commit (skill-only) ✓ but NO dedicated log — retroactively captured via SC237's "update commit hash" log
- SC235: BUNDLED in content commit; then extra separate log commit b70bc9d also writes to data/pipeline.db — double DB write with no incremental value

**DB integrity cross-check (2026-07-22):**
- `data/pipeline.db` **study_cycles** table: SC235 (id=114), SC236 (id=115), SC237 (id=116), SC238 (id=117) — all 4 present ✓
- `data/pipeline.db` **study_log** table: max cycle = 234 (id=39); **SC235–SC238 ABSENT** — study_log has not been written since SC234 (9th consecutive cycle missing from study_log)
- ROOT `pipeline.db`: SC233 ROOT error from last window is the last known ROOT entry. No new ROOT errors this window ✓

**Critical implication:** Production sessions querying `study_log` for recent intelligence will miss SC235–SC238 findings — including the Remotion opacity fix, wave()/noiseDisplacement() effects, camera_control API correction, fal.ai elements cap, and FFmpeg 8.0 whisper filter warning. The SC log mechanism appears to write to `study_cycles` but NOT `study_log`. Investigate and backfill.

---

## SC CONTENT NOTES

**SC235** — `post-production.md` (de77584, Tue Jul 21 06:09:34) — +74 lines (net):
- **Remotion 4.0.491 → 4.0.495 (released 2026-07-20):** Full changelog for v4.0.492–4.0.495.
  - v4.0.492: `muted` prop on `<Video>` — use to silence source audio when layering SFX/VO. Negative sequence offset support.
  - v4.0.494: **Sequence opacity preservation fix.** Prior bug: `<Sequence>` opacity did not persist while active. **Pipeline impact:** caption overlay sequences using opacity fade-in/fade-out must upgrade to ≥4.0.494.
  - v4.0.493/495: Studio-only — no pipeline impact.
- **`wave()` and `noiseDisplacement()` documented in new §11m** — both ship in `@remotion/effects` since v4.0.464 but were previously undocumented. Full parameter tables, code examples, and Snelverhuizen use-case notes included. `@remotion/effects` count updated to 60+ (from 50+).
- Commit body: ✓ Detailed with per-version breakdown.
- Protocol: ❌ BUNDLED (skill + data/pipeline.db in same commit).

**SC236** — `generation-image.md` (ea18cbb, Tue Jul 21 12:11:51) — +7/−4 lines (net +7):
- **Meta Muse Image (released 2026-07-07 — NO API):** Full entry added. Consumer-only at launch (Meta AI, Instagram, WhatsApp). Arena #2 for T2I, #2 single-image editing, #2 multi-image editing. Agent-style: plans layout, pulls real-time web context. No AIMLAPI, no Replicate. Monitor for API. Not actionable under AIMLAPI-only policy until Meta opens an image API.
- **FLUX.2 Max docs still absent (2026-07-21 recheck):** Product page exists on aimlapi.com but dedicated docs.aimlapi.com page still not published. Canary still required.
- **FLUX.2 Max Edit docs still absent (2026-07-21 recheck):** Same status. Confirmed NOT on docs.aimlapi.com Flux index.
- **Gemini Omni Flash NOT on AIMLAPI (2026-07-21 recheck):** Status date updated.
- **MAI-Image 2.5 Flash pricing $19.50/M confirmed:** Status date updated to 2026-07-21.
- Commit body: ✓ Co-Authored-By present; session metadata included.
- Protocol: ✓ CLEAN CONTENT — but NO dedicated log commit (retroactively captured in SC237 log 7040a43).

**SC237** — `generation-video.md` (90c3203, Tue Jul 21 18:12:36) — +10/−4 lines (net +6):
- **Camera presets vs API — HIGH-VALUE CORRECTION:** orbit, crane up, boom, pan, tilt, handheld are Kling UI Inspiration panel presets, NOT `camera_control.type` API values. The 6 types in CLAUDE.md are the **complete API set**. Confirmed via Griptape README July 2026. Explicit warning added: "These 6 types are the COMPLETE API set — orbit/crane/boom are NOT `camera_control.type` API values." Previous ambiguity could cause invalid-type API errors or silent param drops.
- **fal.ai elements wrapper limit — PRODUCTION SAFETY:** fal.ai's Kling v3 I2V wrapper silently caps elements at 1 (wrapper limitation, not native API limit). Native Kling API and AIMLAPI both allow max 3. Warning added: "Do NOT copy elements code from fal.ai examples — their wrapper silently drops elements 2 and 3."
- **Turbo Pro character consistency: confidence → HIGH.** Multi-source July 2026 confirmation: "wardrobe+face hold across multi-shot cuts" (Atlas Cloud). Canary still required for AIMLAPI cost/audio confirmation, NOT for quality validation.
- Kling O3 not on AIMLAPI: status date updated to July 21 (unchanged: still NOT confirmed).
- V3 Motion Control not on AIMLAPI: status date updated to July 21 (unchanged: still NOT confirmed).
- Commit body: ✓ Detailed with 5 specific corrections.
- Protocol: ❌ BUNDLED (skill + data/pipeline.db in same commit); extra "SC237 log" commit 7040a43 retroactively also logs SC236.

**SC238** — `captions-and-titles.md` (0858262, Wed Jul 22 00:09:40) — +23/−2 lines (net +21):
- **Remotion 4.0.495/496 changelogs:** v4.0.495 (Jul 20) — Studio improvements (Figma paste, SVG drag-and-drop, composition inspector). v4.0.496 (Jul 21) — Studio layout refinements, HtmlInCanvas fallback rendering fixes. Both: **no `@remotion/captions` API changes.** Version reference updated to 4.0.496.
- **FFmpeg 8.0 built-in whisper filter — NOT for our pipeline:** FFmpeg 8.0 (Aug 2025; current: 8.1.1) added a native `whisper` audio filter. It produces **segment-level SRT only** — no word-level timestamps. **NOT suitable for word-by-word orange-highlight caption pipeline.** Explicit note added with code example and reason, to prevent misuse if a session encounters references to this feature.
- whisper.cpp v1.9.1 still latest; WhisperX v3.8.6 still stable; ElevenLabs scribe_v2 unchanged.
- Commit body: ✓ Present with specific bullet points.
- Protocol: ❌ BUNDLED (skill + data/pipeline.db in same commit).

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 2.9/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC237: Camera preset vs API correction | Identifies orbit/crane/boom as UI-panel presets, NOT API types — derives from Griptape README as authoritative source; adds explicit warning to prevent production-breaking API calls | Strong positive |
| SC237: fal.ai elements silent cap | Correctly attributes the 1-element limit to wrapper (not native API); explicitly warns against copying fal.ai examples — prevents silent production data loss | Strong positive |
| SC237: Turbo Pro confidence → HIGH | Upgrade based on multi-source multi-review confirmation; correctly scopes remaining canary to cost/audio only (not quality) | Positive |
| SC235: wave()/noiseDisplacement() use-case notes | Correctly identifies "NOT for character/truck shots" — wave distortion on subjects reads as technical defect | Positive |
| SC238: FFmpeg 8.0 whisper filter scope | Correctly identifies that FFmpeg's native whisper filter outputs segment-level only, NOT word-level — prevents pipeline misuse | Positive |
| SC236: Meta Muse Image policy note | Correctly notes "not actionable under AIMLAPI-only policy" — applies policy constraint without guesswork | Positive |
| **CLAUDE.md Pre-Gen Check #5 still wrong (26th audit)** | "15-40 words" → 2.3 rerolls per character shot | Critical negative |
| **ElevenLabs v1 retirement still absent (26th flag, 13 days past)** | Guaranteed 404 at next voiceover session | Critical negative |
| **LTXV Aug-15 — 24 days, 7th audit without CLAUDE.md alert** | CLAUDE.md routing matrix still includes LTXV for B-roll non-char I2V | Negative |
| **SC166 absent (21st audit)** | Differential prompt rule validated by 2 papers; still not in model-prompting-guide.md Part 4 | Negative |

**Score: 2.9/5.0** (↑ +0.1 — SC237 camera_control and fal.ai elements findings are high-precision corrections that prevent real production errors; SC237 Turbo Pro confidence upgrade is evidence-based and correctly scoped; persistent CLAUDE.md non-propagation is the structural floor)

---

### D2 — Execution Accuracy (20%) → 1.7/5.0 (↓ −0.5)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC235 content commit | skills/post-production.md + data/pipeline.db bundled | ❌ BUNDLED |
| SC235 extra log (b70bc9d) | data/pipeline.db written AGAIN after already-bundled content commit | ❌ Redundant double write |
| SC236 content commit | skills/generation-image.md only | ✓ CLEAN |
| SC236 log | NO dedicated log; retroactively captured in SC237 log commit | ❌ MISSING DEDICATED LOG |
| SC237 content commit | skills/generation-video.md + data/pipeline.db bundled | ❌ BUNDLED |
| SC237 log | data/pipeline.db only (also retroactively logs SC236) | ✓ data/ path |
| SC238 content commit | skills/captions-and-titles.md + data/pipeline.db bundled | ❌ BUNDLED |
| SC238 log | data/pipeline.db only | ✓ data/ path |
| Bundling rate | **3/4 (75%)** — major regression from 0/4 (0%) last window | ❌ Critical regression |
| Clean pairs | **0/4 (0%)** — worst in recorded session history | ❌ Critical regression |
| ROOT DB errors | **0/4** — ROOT streak ended (was 7 consecutive windows) | ✓ Major improvement |
| CLAUDE.md frozen | **26th consecutive audit** | ❌ Critical structural |

**Score: 1.7/5.0** (↓ −0.5 — 75% bundling rate reverses last window's breakthrough; 0% clean pairs is the worst recorded; ROOT error streak ending is a genuine positive but cannot offset the protocol regression; SC235 double-writes pipeline.db with no incremental value)

---

### D3 — Memory & Continuity (15%) → 2.3/5.0 (→ 0.0)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC237: Kling O3 not on AIMLAPI (pass 31 recheck) | Consistent conclusion — date updated, no premature upgrade | Positive |
| SC237: V3 Motion Control not on AIMLAPI (pass 31 recheck) | Consistent multi-SC tracking | Positive |
| SC236: FLUX.2 Max/Edit docs absent — 2nd+ consecutive recheck | No false conclusion; "STILL NOT published" noted explicitly | Positive |
| study_cycles table: SC235–238 all present (id 114–117) | ✓ study_cycles is current and complete | Positive |
| **study_log: max cycle = 234; SC235–238 ABSENT** | 9th consecutive cycle missing from study_log; production sessions querying study_log miss SC235–238 intelligence | Critical negative |
| **SC166 absent (21st audit)** | Differential prompt rule never formalized in model-prompting-guide.md Part 4 | Negative |
| Camera_control finding NOT in CLAUDE.md | SC237's API correction in skill; CLAUDE.md routing matrix has no camera_control section | Negative (structural gap) |

**Score: 2.3/5.0** (→ 0.0 — consistent longitudinal tracking (O3, Motion Control, FLUX.2) continues; study_cycles is now well-maintained; study_log fragmentation (9 consecutive missing cycles) undermines retrieval for any session using that table; SC237 camera_control correction is in the skill but production sessions referencing the wrong check would still fail)

---

### D4 — Reliability & Consistency (20%) → 1.5/5.0 (↓ −0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| 0/4 clean pairs | Worst window in recorded session history | ❌ Critical regression |
| 3/4 bundled | Regression from 0/4 last window; last window's 0% bundling was the lone breakthrough | ❌ Critical regression |
| ROOT DB error streak ENDED | 7 consecutive windows → 0; all data/pipeline.db this window | ✓ Major structural improvement |
| No false retroactive fill claims | No misleading commit body claims (contrast with SC229 window) | Positive |
| CLAUDE.md frozen 26th audit | Zero structural updates in 26 days | ❌ Critical structural |
| 89 days without approved output | Production reliability = 0 | Negative |
| SC235 double pipeline.db write | Redundant DB write — inconsistency in log protocol | ❌ Minor |

**Score: 1.5/5.0** (↓ −0.1 — ROOT error ending is real and significant; bundling regression offsets it; 0% clean pairs is the worst reliability signal since current tracking began)

---

### D5 — Tool/Model Integration (15%) → 4.2/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC237: camera_control type correction | Prevents wrong API type strings in production calls; "orbit"/"crane"/"handheld" would be ignored or error — now documented | Strong positive |
| SC237: fal.ai elements cap | Prevents silent production data loss (elements 2+3 silently dropped in fal.ai wrapper) | Strong positive |
| SC237: Turbo Pro HIGH confidence | First cheaper character tier to reach HIGH quality confidence — narrows canary scope to cost/audio only | Positive |
| SC235: wave()/noiseDisplacement() with code examples | Two previously undocumented effects now available with full parameter reference and use cases | Positive |
| SC235: Remotion 4.0.494 opacity fix noted | Prevents caption fade regression on upgrade; <Video> muted prop documented | Positive |
| SC238: FFmpeg 8.0 whisper filter scoped | "Segment-level only" note with code example prevents future misuse in caption pipeline | Positive |
| SC236: Meta Muse Image with Arena rankings | No-API status + policy note prevents wasted time; full spec ready for API release | Positive |
| **CLAUDE.md routing matrix: LTXV still active (24 days to Aug-15 deadline)** | Production session would route new B-roll shots to LTXV | Critical negative |
| **CLAUDE.md Check #5 wrong prompt length (26th audit)** | Active wrong guidance at point of generation | Critical negative |
| **CLAUDE.md Check #7: ElevenLabs v1 retirement absent (26th flag)** | Guaranteed 404 on next voiceover session | Critical negative |
| Wan 2.2 Animate Replace canary STILL unrun (SC234) | Parameters confirmed; $0.06/gen; 24× cheaper than Kling Pro; canary outstanding | Negative |

**Score: 4.2/5.0** (↑ +0.1 — SC237 camera_control and fal.ai corrections are immediately production-applicable with high error-prevention value; Turbo Pro confidence upgrade to HIGH is significant; CLAUDE.md divergence remains the dominant drag; Wan 2.2 Animate Replace canary continues to be the highest-ROI unrun test)

---

### D6 — Communication & Social (10%) → 3.5/5.0 (↑ +1.0)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC235 commit body | Full per-version Remotion changelog with pipeline impact flags (v4.0.492 muted prop, v4.0.494 opacity fix, v4.0.493/495 studio-only) | ✓ Strong |
| SC236 commit body | Present; Co-Authored-By metadata included | ✓ Present |
| SC237 commit body | 5 specific corrective bullets with source ("Griptape README July 2026") and production warnings | ✓ Strong |
| SC238 commit body | Specific bullets: Remotion 4.0.496 (no caption API changes), FFmpeg 8.0 whisper filter scope | ✓ Strong |
| 4/4 commit bodies | All SC235–238 commits have substantive bodies — consistent recovery from the "title-line only" SC234 body | ✓ Best window in 6 audits |

**Score: 3.5/5.0** (↑ +1.0 — all 4 SC commit bodies are detailed and substantive with source citations and production implications; marked improvement from SC234's thin body and prior windows with absent bodies)

---

### D1–D6 Weighted Score

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|-------------|
| D1 Reasoning | 2.9 | 20% | 0.580 |
| D2 Execution | 1.7 | 20% | 0.340 |
| D3 Memory | 2.3 | 15% | 0.345 |
| D4 Reliability | 1.5 | 20% | 0.300 |
| D5 Integration | 4.2 | 15% | 0.630 |
| D6 Social | 3.5 | 10% | 0.350 |
| **Total** | — | 100% | **2.54 / 5.0** |

**Delta vs 2026-07-21: +0.01** (essentially flat — strong integration content and commit body quality canceled by severe protocol regression)

**Failure classification:**
- DISCIPLINE: CLAUDE.md frozen (26th audit), bundling regression, SC166 absent, ElevenLabs v1 not fixed, LTXV Aug-15 not in CLAUDE.md
- ARCHITECTURAL: study_log not receiving SC log entries (write mechanism uses study_cycles table, not study_log); ROOT DB error structural (now resolved)
- MODEL CAPABILITY CEILING: none this window

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

**20 skills × 8 criteria = 160 total points maximum**

Skills assessed: anti-sycophancy, brand-identity, brief-intake, captions-and-titles, character-consistency, cinematic-standards, credit-efficiency, generation-image, generation-video, halal-audio, higgsfield-generation, kling-truck-prompting, model-ceiling-detection, model-prompting-guide, post-production, production-checklist, shariah-compliance, text-overlay-compositing, video-qa-rubric, viral-research.

**Previous: 139/160 = 86.9%**

### Changes this window (SC235–SC238)

**post-production.md (SC235):**
- Coverage: +0.5 (wave()/noiseDisplacement() documented; 60+ effects count accurate)
- Accuracy: +0.5 (Remotion 4.0.495 current; opacity fix scoped; changelog complete)
- Net: +1.0 point

**generation-video.md (SC237):**
- Accuracy: +1.0 (camera_control API types corrected — was ambiguous; now definitive with source)
- Actionability: +0.5 (fal.ai elements cap warning directly prevents production error)
- Net: +1.5 points

**captions-and-titles.md (SC238):**
- Coverage: +0.5 (FFmpeg 8.0 whisper filter scope documented — new section)
- Accuracy: +0.5 (Remotion 4.0.496 current)
- Net: +1.0 point (partially offset by skill-already-strong baseline; awarding +0.5 net)

**generation-image.md (SC236):**
- Coverage: +0.5 (Meta Muse Image new entry with full spec and policy note)
- Accuracy: +0.5 (FLUX.2 Max/Edit and Gemini Omni Flash dates updated 2026-07-21)
- Net: +0.5 points (existing skill was already current; marginal delta)

**Total new points this window: +3.0 (raw) → applying conservatively as +1.0 net (skills were already partially credited)**

**Persistent deductions (unchanged from previous audit):**
- model-ceiling-detection.md: C8 wrong (Veo 3.1 Lite I2V in escalation path) — 21st audit, −1
- model-prompting-guide.md Part 4: SC166 differential prompt rule absent — 21st audit, −1
- CLAUDE.md meta-compliance: Pre-Gen Check #5 wrong prompt length, ElevenLabs v1 absent, LTXV Aug-15 absent — continuing −3+ deductions
- Wan 2.2 Animate Replace absent from CLAUDE.md routing matrix (SC234 finding, now 9 days outstanding)

**Score: 140/160 = 87.5%** (↑ +0.6% — generation-video.md camera_control correction and post-production.md wave()/noiseDisplacement() documentation are the meaningful gains; structural skill gaps unchanged)

### CLAUDE.md Structural Audit

| Component | Status |
|-----------|--------|
| THREE-AGENT PATTERN | ✓ Present |
| PRE-GENERATION CHECKS (10 items) | ❌ Check #5 wrong ("15-40 words" → should be I2V 40-120 / T2V 80-150); Check #7 ElevenLabs v1 IDs absent; Check #9 syntax stale (`face adherence 80-90` → `face_consistency: true`) |
| PRODUCTION GATES (10 items) | ✓ Present and accurate |
| MODEL ROUTING MATRIX | ❌ LTXV row missing deprecation warning (24 days to Aug-15 deadline); Wan 2.2 Animate Replace absent; Turbo Pro not reflected as HIGH-quality confirmed |
| BRAND BINARY CHECKLIST | ✓ Present |
| BANNED WORDS IN MOTION PROMPTS | ✓ Present |
| SHARI'AH COMPLIANCE | ✓ Present |
| ANTI-SYCOPHANCY | ✓ Present |
| FAMILY LOCK-IN | ✓ Present |
| SNORKEL TRIAGE | ✓ Present |

**CLAUDE.md structural score: 7/10 components fully correct** (3 components with active errors/omissions)

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved video:** V3-Tarik-v2-couple (2026-04-26) — **89 days ago.** No new creative output this window.

**Family lock status:** `testimonial` family, 3/6 videos approved. 3 more required before family unlock (lock_until: 6).

**Cost metric:** Credits per approved video = MATHEMATICALLY UNDEFINED (zero new output, day 89).

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

### New Production Intelligence (SC235–SC238)

**Post-production (SC235):**
- **Upgrade pipeline to Remotion ≥4.0.494:** Sequence opacity bug fix is required for caption fade-in/fade-out on overlay sequences. `npm install remotion@4.0.496`.
- `muted` prop now available on `<Video>` — use to silence source audio in compositions.
- `wave()` and `noiseDisplacement()` effects now documented with code examples — available for brand-color background animations.

**Hero frame (SC236):**
- Meta Muse Image exists but no API — monitor for AIMLAPI addition.
- FLUX.2 Max/Edit: docs still absent; canary still required before production use.
- Gemini Omni Flash: still NOT on AIMLAPI as of 2026-07-21.

**Generation video (SC237):**
- **Camera control:** Only use the 6 documented `camera_control.type` values in API calls. Achieve orbit/crane/boom via `simple` config parameters or prompt text.
- **Elements:** Native AIMLAPI allows max 3 elements; fal.ai wrapper caps at 1 — copy from AIMLAPI docs only.
- **Turbo Pro character consistency: HIGH confidence.** First character animation tier below Kling Pro to reach HIGH quality confirmation. Run cost/audio canary before locking finals.

**Caption pipeline (SC238):**
- `npm install remotion@4.0.496` — Studio improvements, no caption API changes.
- FFmpeg 8.0 built-in `whisper` filter produces segment-level SRT only — NOT word-level. Do not use for word-by-word orange-highlight captions.
- All pipeline options A/B/C (whisper.cpp, WhisperX, ElevenLabs scribe_v2) unchanged.

### Ralph Loop

*"What would a senior creative director still reject?"*

1. **89 days of production stagnation while the Wan 2.2 Animate Replace canary ($0.06) has been the highest-priority unrun test for 3 consecutive cost-optimization cycles (SC220, SC234, and now this audit).** Parameters confirmed (`alibaba/wan2.2-14b-animate-replace`, `video_url`, `image_url`, `resolution: "720p"`). Billing confirmed ($0.06/gen). Canary sequence documented. This is 24× cheaper than Kling Pro ($1.46). A single canary session (Move mode → Replace mode) would either unlock the cheapest character animation on the platform or provide a "not production-quality" verdict. Nothing blocks this except no production session was run.

2. **SC237 confirms Kling Turbo Pro has HIGH character consistency confidence — wardrobe and face hold across multi-shot cuts — yet no Turbo Pro canary on AIMLAPI has been run.** The remaining unknowns are cost confirmation and audio default behavior on AIMLAPI (not quality). Turbo Pro is a direct drop-in for character shots at lower cost than Pro. A 3s reference canary would confirm pricing and audio settings. This has been the most production-ready untested upgrade since Kling Pro launched.

3. **ElevenLabs v1 retirement: 13 days past (July 9, 2026).** `eleven_monolingual_v1`, `eleven_multilingual_v1`, `scribe_v1` return 404 NOW. CLAUDE.md Check #7 still silent. The next production session involving voiceover will produce a 404 error the operator will spend time debugging. This is a known, documented, preventable failure that takes 5 minutes to fix. A senior creative director reviewing pipeline health would flag this as unacceptable operational hygiene.

4. **LTXV Aug-15 deadline: 24 days.** CLAUDE.md routing matrix still lists B-roll I2V without any deprecation warning. A production session today following the routing matrix could route shots to `ltxv/ltxv-2-fast` — a model that will return errors on August 15. The replacement (`minimax/hailuo-2.3-fast`) is documented in `credit-efficiency.md` but not in CLAUDE.md routing. One CLAUDE.md edit prevents a guaranteed deadline failure.

**Overall Creative: (3.9 + 4.2 + 4.1) / 3 = 4.07 / 5.0** (→ unchanged, day 89 of production stagnation)

CREATIVE_AUDIT_COMPLETE

---

## ACTION ITEMS

### [P0 — CRITICAL — 26th audit — CLAUDE.md: 3 fixes needed in one edit session]

**1. Fix Pre-Gen Check #5: prompt length**
```
Current:  Motion prompt: 15-40 words, motion ONLY, defined endpoint ("eases to stop")
Correct:  Motion prompt: I2V 40-120 words / T2V 80-150 words (Kling v3, July 2026).
          Motion ONLY — action arc + camera move + defined endpoint. (15-40w was Kling v1/v2.)
```

**2. Fix Pre-Gen Check #7: ElevenLabs v1 retirement (13 DAYS OVERDUE)**
```
⚠️ RETIRED JULY 9, 2026: eleven_monolingual_v1 / eleven_multilingual_v1 / scribe_v1 → 404 NOW.
Use: eleven_v3 (TTS production) / eleven_flash_v2_5 (TTS draft) / scribe_v2 (captions).
NOTE: language_code NOT supported on eleven_multilingual_v2 (silently ignored, June 29, 2026).
grep -r "monolingual_v1\|scribe_v1" scripts/ before voiceover work.
```

**3. Routing matrix: LTXV alert + Wan 2.2 Animate Replace + Turbo Pro**
```
⚠️ LTXV DEADLINE Aug 15 (24 days): ltxv/ltxv-2-fast WILL ERROR after Aug 15.
  → Use minimax/hailuo-2.3-fast ($0.0416/sec) for non-char I2V until AIMLAPI adds ltxv/ltxv-2-3-fast.

Add row: Character animation canary | Wan 2.2 Animate Replace | $0.06/gen
  (alibaba/wan2.2-14b-animate-replace; params: video_url, image_url, resolution: "720p")

Update: Kling Turbo Pro character consistency: HIGH confidence (multi-source July 2026).
  Canary required for AIMLAPI cost/audio only — run 3s reference before locking finals.
```

---

### [P0 — BEFORE NEXT PRODUCTION SESSION — Wan 2.2 Animate Replace canary]

**4. Run Move mode canary (SC234, 9 days outstanding):**
- Step 1: Pass NBP Edit hero frame as `image_url` + simple 5s drive video as `video_url`, mode: Move
- Step 2: Verify output quality + confirm $0.06 billing in AIMLAPI credit log
- Step 3 (if Move passes): Run Replace mode with B-roll + hero frame reference
- If confirmed: adds $0.06/gen character animation tier (24× cheaper than Kling Pro $1.46)

---

### [P0 — BEFORE NEXT CHARACTER SESSION — Kling Turbo Pro canary]

**5. Run 3s Turbo Pro canary on AIMLAPI:**
- Quality confidence is now HIGH (multi-source confirmed). Remaining unknowns: AIMLAPI cost per second, audio default (on/off).
- Canary: `klingai/video-v3-turbo-pro` with `generate_audio: false`, 3s reference clip, confirm billing.
- If audio and cost confirm: Turbo Pro becomes the draft character animation tier, replacing Standard.

---

### [P0 — DATA INTEGRITY — study_log missing SC235–SC238]

**6. Investigate study_log write mechanism and backfill SC235–SC238:**
- study_cycles (data/pipeline.db) has SC235–238 (id 114–117) — SC log commits write to `study_cycles`.
- study_log (data/pipeline.db) stuck at cycle 234 (id=39) — 9 consecutive cycles missing.
- Production sessions querying study_log miss all intelligence since SC234 (camera_control fix, fal.ai cap, Turbo Pro HIGH, wave()/noiseDisplacement(), FFmpeg whisper filter scope).
- Action: Determine whether study_log is legacy (production sessions should query study_cycles) or active (SC log commits should write to both). Backfill accordingly.

---

### [P0 — OPERATIONAL — model-ceiling-detection.md C8 — 21st consecutive audit]

**7. Remove Veo 3.1 Lite I2V from video escalation path** (one-line removal — Veo 3.1 Lite is T2V only; listing it in I2V escalation is wrong and would cause production routing errors)

---

### [P0 — BEFORE NEXT CHARACTER SESSION — SC166 — 21st audit]

**8. model-prompting-guide.md Part 4 — add SC166 differential prompt rule:**
```
On facial-movement retries: use action-only prompts; strip identity-descriptive words.
(Validated by Stand-In (arXiv 2508.07901) + WildActor (arXiv 2603.00586) — both confirm
character attributes in text compete with identity flow. Text = action+camera ONLY.)
```

---

### [P1 — COMMIT PROTOCOL]

**9. Return to clean pair protocol:**
SC235, SC237, SC238 all bundled skill + data/pipeline.db in content commit. Last window had 0% bundling (best ever). This window: 75% bundling. 
Rule: content commit = skill file(s) ONLY. Separate log commit = data/pipeline.db ONLY. No exceptions.
Root cause to investigate: are these bundlings from the same session or different? If SC235's extra log (b70bc9d) triggered only because de77584 was bundled, fix the content commit protocol and the redundant log disappears.

---

### [P1 — BEFORE NEXT B-ROLL SESSION]

**10. Upgrade Remotion to ≥4.0.496:** `npm install remotion@4.0.496` — fixes Sequence opacity bug (4.0.494) and adds muted prop (4.0.492). Both affect caption overlay sequences.

**11. ffmpeg-normalize update (SC232, 10 days outstanding):** `pip install ffmpeg-normalize --upgrade` to get v1.41.1. Add `--threshold 1.0` to normalize command; remove `-c:a aac` flag (v1.41.0 infers from container).

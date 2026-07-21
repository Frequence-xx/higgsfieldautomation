# Daily Audit — 2026-07-21

**Pipeline:** Snelverhuizen Cinematic Video Ad Production
**Auditor:** Daily Audit Agent (automated)
**Previous audit:** 2026-07-20 | Operator 2.33/5.0 · Skills 86.9% · Creative 4.07/5.0
**Baseline (2026-04-12):** Operator 3.85/5.0 · Skills 91.5% · Creative 4.4/5.0

---

## SUMMARY

| Audit | Score | Delta vs 2026-07-20 | Delta vs Baseline |
|-------|-------|--------------------|-------------------|
| Operator Performance | **2.53 / 5.0** | ↑ +0.20 | ↓ −1.32 |
| Skill Library & Policy | **86.9%** (139/160) | → 0.0% | ↓ −4.6% |
| Creative Output Quality | **4.07 / 5.0** | → 0.00 | ↓ −0.33 |

**Four study cycles (SC231–SC234) since the 2026-07-20 audit.** Best execution window in recent history: 0% bundling rate, 75% clean pairs. SC233 log committed to ROOT pipeline.db (7th consecutive ROOT error window). SC231, SC232, SC233 absent from data/pipeline.db study_log; SC234 confirmed present.

**HIGHEST VALUE FINDING SC234: Wan 2.2 Animate Replace parameters fully confirmed.** Model strings, parameter names (video_url, image_url, resolution), and $0.06/generation billing confirmed from AIMLAPI docs. At $0.06 vs Kling Pro $1.46, this is the highest-ROI canary on the platform — 24× cheaper for character animation. Canary sequence: Move mode first (hero frame + drive video), then Replace mode (B-roll + character reference).

**SC233: Stand-In + WildActor research papers both independently validate the differential prompt rule.** Stand-In (arXiv 2508.07901) explicitly recommends generic descriptors over character-specific text. WildActor's AIPA unidirectional design is the architectural proof that character attributes in text compete with identity flow. Both code-released, neither on AIMLAPI yet. SC166 rule still absent from model-prompting-guide.md Part 4 — **20th consecutive audit.**

**CLAUDE.md Pre-Gen Check #5 STILL WRONG (25th consecutive audit).** ElevenLabs v1 retirement STILL absent (12 days past, 25th flag). LTXV Aug 15 still in credit-efficiency.md only — 25 days remaining, 6th audit without CLAUDE.md action.

**88 days without approved creative output.**

---

## CHANGES SINCE 2026-07-20 AUDIT

Git commits since `799d5cd` (July 20 audit):

| Hash | Commit | Files | DB path | Protocol |
|------|--------|-------|---------|---------|
| 47170f3 | SC231: Caption pipeline (pass 35) — Remotion 4.0.494, CSR caption CSS warning, Sequence opacity fix | `skills/captions-and-titles.md` only | — | ✓ CLEAN CONTENT |
| 300c8a7 | SC231 log: record study cycle 231 in pipeline.db | `data/pipeline.db` only | `data/` ✓ | ✓ CLEAN LOG (34s after content) |
| 0deda9b | SC232: Halal audio (pass 35) — ffmpeg-normalize v1.38-v1.41.1 June-July 2026 updates | `skills/halal-audio.md` only | — | ✓ CLEAN CONTENT |
| dff16ee | SC232 log: record study cycle 232 in pipeline.db | `data/pipeline.db` only | `data/` ✓ | ✓ CLEAN LOG (9s after content) |
| c795bd8 | SC233: Character consistency (pass 34) — Stand-In + WildActor, Wan 2.7 R2V + Kling O3 still not on AIMLAPI (2026-07-20 recheck) | `skills/character-consistency.md` only | — | ✓ CLEAN CONTENT |
| 1d1f5ca | SC233 log: record study cycle 233 in pipeline.db | ROOT `pipeline.db` | ROOT ✗ | ❌ ROOT DB |
| 94916e0 | SC234: Cost optimization (pass 32) — LTXV Aug-15 risk confirmed (25 days), Wan 2.2 Animate Replace params clarified, Wan 2.7 R2V 4th cycle NOT CALLABLE, Seedance 2.5 BytePlus live but not on AIMLAPI | `skills/credit-efficiency.md` only | — | ✓ CLEAN CONTENT |
| 8f7cef2 | SC234 log: record study cycle 234 in pipeline.db | `data/pipeline.db` only | `data/` ✓ | ✓ CLEAN LOG |

**Protocol compliance this window:**
- Clean pairs (content-only commit + correct separate log): **3/4 (75%)** — SC231 ✓, SC232 ✓, SC234 ✓ | **Best window in recent session history**
- Bundled commits: **0/4 (0%)** — first zero-bundle window recorded
- ROOT pipeline.db path errors: 1/4 (SC233 log) → **7th consecutive ROOT error window** (SC209, SC212, SC217, SC222, SC226, SC228, SC233)
- SC233 log retroactive fill: SC233 captured in ROOT study_cycles (id=61) but NOT in data/pipeline.db study_log

**DB integrity cross-check (2026-07-21):**
- ROOT pipeline.db study_cycles: max cycle=233 (SC233 captured id=61; SC231, SC232, SC234 absent)
- data/pipeline.db study_log: max cycle=234 (SC234 confirmed ✓; SC228–SC233 all absent — 6 consecutive cycles missing)
- SC234 is the ONLY cycle from this window that landed in data/pipeline.db study_log

---

## SC CONTENT NOTES

**SC231** — `captions-and-titles.md` (47170f3, Mon Jul 20 06:08:24) — +38/−2 lines (net +36):
- **Remotion 4.0.490 → 4.0.494 (confirmed 2026-07-20):** Version history block for v4.0.491–4.0.494 added.
- **v4.0.494 Sequence opacity fix:** `opacity` on `<Sequence>` now preserved while active. Caption fade-out animations using `<Sequence style={{ opacity: ... }}>` affected — upgrade resolves it.
- **v4.0.491 CSR caption CSS warning:** `-webkit-text-stroke`, `paint-order: stroke fill`, `borderRadius` may not render in client-side rendering. HTML-in-canvas mode (Chrome 152+) required for correct CSR caption output. **Server-side render pipeline (our pipeline) unaffected.**
- Tool confirmations: whisper.cpp v1.9.1 (no new release), WhisperX v3.8.6 stable, ElevenLabs Python SDK v2.58.0.
- Commit body: ✓ Detailed with 6 bullet points.
- Protocol: ✓ CLEAN PAIR.

**SC232** — `halal-audio.md` (0deda9b, Mon Jul 20 12:08:39) — +12/−1 lines (net +11):
- **ffmpeg-normalize v1.38.0–v1.41.1 June-July 2026 releases documented:**
  - v1.38.0: no longer writes temp files (less disk I/O)
  - v1.39.0: `--keep-mtime` flag; bit depth preservation default
  - v1.40.0: `--threshold` to skip already-normalized files; per-file `--print-stats`; non-zero exit on failure
  - v1.41.0: auto output codec from container (**aac no longer required for MP4**)
  - v1.41.1: Windows fix (no pipeline impact)
- `§4f` updated with `--threshold 1.0` flag and version history block.
- 3 new Known Issues entries.
- Commit body: ✓ Detailed with per-version notes.
- Protocol: ✓ CLEAN PAIR.

**SC233** — `character-consistency.md` (c795bd8, Mon Jul 20 18:10:01) — +24/−2 lines (net +22):
- **Stand-In (arXiv 2508.07901) — Future Watch:** Wan2.1-14B plug-and-play, only 1% additional params. Code + weights released. Explicit recommendation: generic descriptors ("a man") only, no character-specific text → **validates differential prompt rule from first principles.** Frontal + medium-to-close-up shots only; wide shots and profiles degrade.
- **WildActor (arXiv 2603.00586) — Future Watch:** AIPA (Asymmetric Identity-Preserving Attention) unidirectional flow — identity reference→video only, not bidirectional. Full-body viewpoint transitions handled. **AIPA is the architectural proof that character attributes in prompts compete with identity flow.** Handles walking-away and large viewpoint transitions where Kling O1 drifts.
- **Kling O3 not on AIMLAPI (pass 34, 2026-07-20):** Confirmed on Runware/fal.ai/Atlas Cloud; AIMLAPI-only per directive.
- **Wan 2.7 R2V: pass 34 recheck** — still NOT live on AIMLAPI; Wan 2.6 R2V remains the only confirmed R2V fallback.
- Commit body: ✓ Detailed with 4 bullet points.
- Protocol: ❌ ROOT pipeline.db (log commit 1d1f5ca used ROOT path — 7th consecutive ROOT error window).

**SC234** — `credit-efficiency.md` (94916e0, Tue Jul 21 00:09:24) — +7/−0 lines (net +7):
- **LTXV Aug-15 deadline — 25 days, STILL no AIMLAPI string update.** `ltxv/ltxv-2-fast` still callable (auto-routes to LTX-2.3 since July 15) but WILL ERROR after August 15. **Do NOT route new production shots to LTXV — use Hailuo 2.3 Fast exclusively for non-char I2V.**
- **Wan 2.7 R2V — FOURTH consecutive cost-optimization cycle NOT CALLABLE on AIMLAPI** (SC220, SC227, SC233, SC234). All third-party platforms have it; AIMLAPI is the holdout. Do not canary until dedicated docs page appears.
- **Wan 2.2 Animate Replace parameters CONFIRMED from AIMLAPI docs:** `alibaba/wan2.2-14b-animate-replace` (Replace) + `alibaba/wan2.2-14b-animate-move` (Move). Params: `video_url` (driving motion), `image_url` (reference character), `resolution: "720p"`. Cost: $0.06/generation CONFIRMED. Canary sequence documented.
- **Krea WAN 14B V2V workflow clarified:** T2V $0.033/sec, V2V $0.026/sec (cheapest restyling on AIMLAPI).
- **Seedance 2.5:** BytePlus live July 16; NOT on AIMLAPI as of July 21.
- Commit body: ✓ Present but title-line only (no sub-bullets — weaker than SC231/232/233).
- Protocol: ✓ CLEAN PAIR.

---

## AUDIT 1 — OPERATOR PERFORMANCE

Weights: Reasoning 20% · Execution 20% · Memory 15% · Reliability 20% · Integration 15% · Social 10%

### D1 — Reasoning Quality (20%) → 2.8/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC233: Stand-In validates differential prompt rule | Explicit inference guide says "generic descriptors only" — same as our Step 3a policy; 1-param-overhead makes it the lightest identity adapter documented | Strong positive |
| SC233: WildActor AIPA is architectural proof | Unidirectional identity flow proves text character attributes compete with reference → text must be action-only | Strong positive |
| SC234: Wan 2.7 R2V 4th cycle conclusion | "NOT CALLABLE" conclusion re-confirmed after 4 consecutive cost-opt cycles; disciplined not upgrading to "UNVERIFIED" without docs page evidence | Positive |
| SC234: Wan 2.2 Animate Replace full canary plan | Move-then-Replace sequence with specific params, billing verification, fallback path — actionable plan for first canary | Strong positive |
| SC234: LTXV Aug-15 — clear routing decision | "Do NOT route new production shots to LTXV — use Hailuo 2.3 Fast exclusively" — unambiguous decision, 25 days to act | Positive |
| SC232: ffmpeg-normalize 6 releases with per-version flags | `--threshold 1.0`, non-zero exit on failure, aac-no-longer-required — immediately applicable improvements | Positive |
| SC231: Remotion version tracking with opacity fix | 4.0.490→4.0.494 with specific bug fix (Sequence opacity) — prevents caption fade regression on upgrade | Positive |
| **CLAUDE.md Pre-Gen Check #5 wrong (25th audit)** | "15-40 words" still wrong; 2.3 rerolls per character shot average | Critical negative |
| **ElevenLabs v1 — 12 DAYS PAST (25th flag)** | Still absent from CLAUDE.md; guaranteed 404 at next voiceover session | Critical negative |
| **LTXV Aug 15 — 25 days (6th audit without CLAUDE.md alert)** | credit-efficiency.md has full plan; CLAUDE.md routing matrix silent | Negative |
| SC166 absent (20th audit) | Differential prompt rule now validated by 2 independent papers yet still not in model-prompting-guide.md Part 4 | Negative |

**Score: 2.8/5.0** (↑ +0.1 — SC233's Stand-In/WildActor findings are the strongest theoretical grounding for our existing practices seen in recent windows; SC234's Wan 2.2 Animate Replace canary plan is the most actionable $-saving finding since Kling v3 Pro launch; persistent CLAUDE.md non-propagation offsets)

---

### D2 — Execution Accuracy (20%) → 2.2/5.0 (↑ +0.5)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC231 | content-only + data/ log (34s gap) | ✓ CLEAN PAIR |
| SC232 | content-only + data/ log (9s gap) | ✓ CLEAN PAIR |
| SC233 | content-only → ✓; log → ROOT pipeline.db | ✓ CONTENT / ❌ ROOT LOG |
| SC234 | content-only + data/ log | ✓ CLEAN PAIR |
| Bundling rate | **0/4 (0%)** — first zero-bundle window | ↑↑ Breakthrough |
| Clean pairs | **3/4 (75%)** — best rate in recorded session history | ↑↑ Major improvement |
| ROOT DB error | SC233 log → **7th consecutive ROOT error window** | ❌ Entrenched structural |
| CLAUDE.md frozen | **25th consecutive audit without update** | ❌ Critical structural |

**Score: 2.2/5.0** (↑ +0.5 — zero-bundle rate and 75% clean pair rate are genuine structural improvements; ROOT DB error is entrenched (7th window) but now isolated to log commits only; the 0% bundling is the dominant positive signal — all 4 content commits were skill-only)

---

### D3 — Memory & Continuity (15%) → 2.3/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC234: 4-cycle Wan 2.7 R2V longitudinal tracking | SC220, SC227, SC233, SC234 — consistent "NOT CALLABLE" conclusion across cycles; no premature upgrade | Positive |
| SC234: LTXV tracked across SC206, SC213, SC220, SC227, SC234 | 5 cycles of monitoring; routing decision updated correctly | Positive |
| SC233: Wan 2.7 R2V pass 34 recheck | Correctly did not change status without new evidence | Positive |
| SC234: data/pipeline.db study_log cycle 234 confirmed | ✓ First cycle in this window to land in study_log | Positive |
| SC228-SC233 absent from data/pipeline.db study_log | 6 consecutive cycles missing; study_log last confirmed entry before SC234 was cycle 227 | Critical negative |
| SC231, SC232, SC233 log entries absent from data/pipeline.db study_log | Only SC234 landed; SC231/232/233 not in study_log despite correct path commits for SC231/232 | Negative |
| SC166 absent (20th audit) | Differential prompt rule still not formalized in model-prompting-guide.md Part 4 | Negative |
| ROOT pipeline.db study_cycles | SC233 captured (id=61); SC231, SC232, SC234 not in ROOT | Architectural fragmentation |

**Score: 2.3/5.0** (↑ +0.1 — SC234 landing in study_log is a positive signal; longitudinal tracking in SC233/234 shows consistent pattern recognition; data/pipeline.db study_log is fragmented with 6 cycles missing; paradoxically SC231 and SC232 had correct data/ log path commits but their entries are absent from study_log — indicates a schema-level write failure, not just a path error)

---

### D4 — Reliability & Consistency (20%) → 1.6/5.0 (↑ +0.2)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| 3/4 clean pairs | Best window in session history | ✓ Positive |
| 0% bundling rate | First time recorded | ✓ Strong positive |
| SC233 ROOT log | 7th consecutive ROOT error window | ❌ Critical structural |
| CLAUDE.md frozen | **25 consecutive audits without update** | ❌ Critical structural |
| study_log write failure | SC231/232 had correct data/ paths but no study_log entries landed | ❌ Architectural |
| 88 days without approved output | Production reliability = 0 vs goal | Negative |
| No false retroactive fill claims this window | No misleading commit bodies (unlike SC229) | Positive |
| Clean pair trend | 75% (this) vs 33% (prev) vs 50% (two prior) — clear improvement signal | ↑ Positive |

**Score: 1.6/5.0** (↑ +0.2 — breakthrough improvements in clean pair rate and zero bundling; zero false retroactive fill claims (contrast with SC229); ROOT DB error entrenched (7th window) and CLAUDE.md freeze (25th audit) keep floor low)

---

### D5 — Tool/Model Integration (15%) → 4.1/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC234: Wan 2.2 Animate Replace full parameter set | model strings, param names, `$0.06` billing CONFIRMED, canary sequence — production-ready | Strong positive |
| SC233: Stand-In + WildActor integration insights | AIPA unidirectional flow maps to our existing prompt-only-action rule; frontal/medium limitation documented | Positive |
| SC232: ffmpeg-normalize v1.41.0 | `aac no longer required for MP4` — removes a mandatory flag from our normalize command | Positive |
| SC231: Remotion 4.0.494 Sequence opacity fix | Prevents caption regression on upgrade; CSR warning prevents misdiagnosis if pipeline ever migrates | Positive |
| SC234: Seedance 2.5 on BytePlus (NOT AIMLAPI) | Status update prevents canary waste; AIMLAPI-only directive confirmed | Positive |
| **CLAUDE.md 15-40w still wrong (25th)** | Active wrong guidance at point of generation | Critical negative |
| ElevenLabs v1 (25th) | CLAUDE.md Check #7 silent; guaranteed 404 next voiceover session | Critical negative |
| LTXV Aug 15 (6th audit) | Production routing gap growing | Negative |
| SC234 body: no sub-bullets | LTXV/Wan 2.2 details in skill; commit body too brief for future commit-log query | Minor negative |

**Score: 4.1/5.0** (↑ +0.1 — Wan 2.2 Animate Replace is the most actionable integration advance since Kling v3 Pro launch; ffmpeg-normalize flag and Remotion opacity fix are both immediately deployable; CLAUDE.md divergences remain the primary drag)

---

### D6 — Communication & Social (10%) → 2.5/5.0 (↑ +0.1)

| Signal | Evidence | Verdict |
|--------|----------|---------|
| SC231 commit body | 6 bullet points: version bump, opacity fix, CSR warning, tool confirmations | ✓ Strong positive |
| SC232 commit body | 5 per-version release notes with feature flags | ✓ Strong positive |
| SC233 commit body | 4 bullet points with arXiv references and production implications | ✓ Strong positive |
| SC234 commit body | Title-line only, no sub-bullets — weaker than SC231/232/233 | ✓ Present but thin |
| 4 consecutive SC content commits with bodies | Consistent recovery from SC225/226 body absence 5 windows ago | Strong positive |
| **Telegram BOT_TOKEN unconfigured** | **56th consecutive audit without delivery** | Systemic negative |
| ElevenLabs non-escalation (25th) | CRITICAL overdue issue not reaching owner | Persistent negative |
| LTXV deadline non-escalation (6th) | 25 days — not reaching owner | Negative |
| SC166 non-escalation (20th) | Validated by 2 papers this window — still not escalated | Negative |

**Score: 2.5/5.0** (↑ +0.1 — 4 consecutive SC commits with quality bodies; SC234 body lacks sub-bullets (contrast with SC231/232/233 quality); Telegram and escalation gaps unchanged; 56th audit without owner notification)

---

### AUDIT 1 WEIGHTED TOTAL

| Dimension | Weight | Prev Score | New Score | Change | Weighted |
|-----------|--------|-----------|-----------|--------|----------|
| D1 Reasoning | 20% | 2.7 | 2.8 | ↑ +0.1 | 0.560 |
| D2 Execution | 20% | 1.7 | 2.2 | ↑ +0.5 | 0.440 |
| D3 Memory | 15% | 2.2 | 2.3 | ↑ +0.1 | 0.345 |
| D4 Reliability | 20% | 1.4 | 1.6 | ↑ +0.2 | 0.320 |
| D5 Integration | 15% | 4.0 | 4.1 | ↑ +0.1 | 0.615 |
| D6 Social | 10% | 2.4 | 2.5 | ↑ +0.1 | 0.250 |
| **TOTAL** | 100% | **2.33** | | | **2.53 / 5.0** |

**Operator Performance: 2.53/5.0** (↑ +0.20 from 2.33 — best single-window improvement in recent session history; driven by zero bundling (first time), 75% clean pairs, strong SC231-234 content quality, and Wan 2.2 Animate Replace as highest-ROI actionable finding in weeks; ROOT DB error (7th window) and CLAUDE.md freeze (25th audit) remain structural ceilings preventing score recovery above 3.0)

**Failure classifications this window:**
- SC233 ROOT DB log → DISCIPLINE (7th consecutive ROOT window — no structural fix attempted)
- SC231/232 study_log write failure (correct path, no entry) → ARCHITECTURAL (wrong DB schema still affects some writes)
- CLAUDE.md frozen 25 consecutive audits → DISCIPLINE (dominant pattern)
- CLAUDE.md Pre-Gen Check #5 wrong (25th) → DISCIPLINE
- ElevenLabs v1 non-escalation (12 days overdue, 25th flag) → DISCIPLINE
- LTXV Aug-15 non-escalation (6th audit) → DISCIPLINE
- SC166 absent (20th audit, now validated by 2 papers) → DISCIPLINE
- Telegram BOT_TOKEN unconfigured (56th audit) → ARCHITECTURAL
- study_log write failure for SC231-233 → ARCHITECTURAL

OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2 — SKILL LIBRARY & POLICY

### Files Updated This Window (4 files)

**`captions-and-titles.md`** — SC231 (+38/−2) ≈ ~8,000 words (1,064 lines)

| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Total |
|----|----|----|----|----|----|----|----|----|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | **7/8** |

C6 fail (~8,000 words; SC231 +36 net lines, no resolution). SC231 additions: version history block for v4.0.491–4.0.494, Sequence opacity fix flagged for caption fade-out usage. C8 pass: CLAUDE.md has no Remotion version specifics; no new inconsistency. Score: **7/8** (unchanged).

---

**`halal-audio.md`** — SC232 (+12/−1) ≈ ~11,700 words (1,180 lines)

| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Total |
|----|----|----|----|----|----|----|----|----|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | **7/8** |

C6 fail (~11,700 words). SC232 additions: ffmpeg-normalize version history block, `--threshold 1.0` flag, 3 Known Issues entries. No C8: CLAUDE.md doesn't reference ffmpeg-normalize version specifics. Score: **7/8** (unchanged).

---

**`character-consistency.md`** — SC233 (+24/−2) ≈ ~8,850 words (860 lines)

| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Total |
|----|----|----|----|----|----|----|----|----|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | **7/8** |

C6 fail (~8,850 words; SC233 +22 net lines). SC233 additions: Stand-In (Future Watch), WildActor (Future Watch), Kling O3/Wan 2.7 R2V pass-34 rechecks. No C8: CLAUDE.md doesn't reference Stand-In/WildActor (both no-API-yet). Score: **7/8** (unchanged).

---

**`credit-efficiency.md`** — SC234 (+7/−0) ≈ ~15,800 words (1,021 lines)

| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Total |
|----|----|----|----|----|----|----|----|----|
| ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | **7/8** |

C6 fail (~15,800 words). SC234 adds status refresh entry #52. **New gap identified (not a C8 violation since CLAUDE.md lacks Wan 2.2 routing):** Wan 2.2 Animate Replace ($0.06/generation CONFIRMED) is now the highest-ROI canary on the platform — credit-efficiency.md has full parameters + canary sequence but CLAUDE.md routing matrix doesn't list it. Score: **7/8** (unchanged).

---

### Carry-Forward Scores (16 unchanged files)

| Skill File | Score | Notes |
|------------|-------|-------|
| anti-sycophancy.md | 8/8 | Unchanged |
| brand-identity.md | 8/8 | Unchanged |
| brief-intake.md | 8/8 | Unchanged |
| production-checklist.md | 8/8 | Unchanged |
| video-qa-rubric.md | 8/8 | Unchanged |
| model-prompting-guide.md | 7/8 | C6 fail (~5,341 words); SC166 diff prompt rule absent (**20th audit**) |
| shariah-compliance.md | 7/8 | C2 fail |
| higgsfield-generation.md | 7/8 | C5 fail |
| generation-image.md | 7/8 | C6 fail (~12,490 words) |
| post-production.md | 7/8 | C6 fail (~11,575 words) |
| captions-and-titles.md | 7/8 | C6 fail (~8,000 words) — SC231 |
| halal-audio.md | 7/8 | C6 fail (~11,700 words) — SC232 |
| character-consistency.md | 7/8 | C6 fail (~8,850 words) — SC233 |
| credit-efficiency.md | 7/8 | C6 fail (~15,800 words) — SC234 |
| cinematic-standards.md | 6/8 | C2 + C5 fail |
| kling-truck-prompting.md | 6/8 | C2 + C5 fail |
| model-ceiling-detection.md | 6/8 | C2 fail + C8 fail (Veo 3.1 Lite I2V — **21st consecutive audit**) |
| text-overlay-compositing.md | 6/8 | C2 + C5 fail |
| viral-research.md | 6/8 | C2 + C5 fail |
| generation-video.md | 6/8 | C6 fail + C8 fail (CLAUDE.md 15-40w vs skill 40-120w I2V — **25th audit**) |

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

Library word count: ~97,700 words (+547 net from SC231–SC234)
```

Calculation: (5 × 8) + (9 × 7) + (6 × 6) = 40 + 63 + 36 = **139/160 = 86.9%**

**Skill Library & Policy: 86.9% (139/160)** (→ unchanged — all 4 SC content updates factually correct, no new C8 violations; structural gaps (C6 word count, C2 stems, C8 CLAUDE.md divergences) require owner-approved refactoring to resolve; new gap: Wan 2.2 Animate Replace $0.06 CONFIRMED — CLAUDE.md routing matrix doesn't list it)

---

### CLAUDE.md Structural Audit

CLAUDE.md **unchanged — 25th consecutive audit without update.**

| Component | Status |
|-----------|--------|
| Three-agent pattern | ✓ Present |
| Snorkel triage | ✓ Present |
| Model routing matrix | ✗ STALE: Seedream 5.0 Pro ($0.06/img — **9th audit**); Kling O1 I2V ($0.73/5s — **11th audit**); Hailuo 2.3 Fast ($0.0416/sec — **14th audit**); NB2 Lite ($0.044 — **15th audit**); Wan 2.7 R2V (absent); Wan 2.2 Animate Replace/Move (absent, $0.06 CONFIRMED); Krea WAN 14B T2V (absent); Imagen 4 (retired — **27 days past**) |
| Brand binary checklist | ✓ Present |
| Production gates | ✓ Present |
| Pre-generation checks | ✗ STALE: **Check #5: "15-40 words" → WRONG (25th audit)**; Check #9 deprecated syntax (`face adherence 80-90` → `face_consistency: true`); Check #7 missing ElevenLabs v1 retirement (**12 days overdue**) |
| **ElevenLabs v1 removal** | **✗ ABSENT — RETIRED JULY 9. 12 DAYS PAST. 25th consecutive flag. PRODUCTION BLOCKER.** |
| **CLAUDE.md Pre-Gen Check #5** | **✗ WRONG — "15-40 words" is Kling v1/v2. Kling v3 Pro I2V: 40-120 words. 25th consecutive flag.** |
| **LTXV 2.3 auto-routing warning** | **✗ ABSENT — 25 DAYS REMAINING. 6th consecutive audit without CLAUDE.md action.** |
| **Wan 2.2 Animate Replace** | **✗ ABSENT — SC234 confirmed $0.06/generation + parameters. NOT in CLAUDE.md routing matrix. NEW gap this window.** |
| end_image_url parameter | ✗ ABSENT — SC230; no C8 (2nd audit without fix) |
| MC duration limits | ✗ ABSENT — SC230; no C8 (2nd audit without fix) |
| blockReason routing | ✗ ABSENT — SC229; no C8 (3rd audit without fix) |
| Seedream 5.0 Pro 14-ref | ✗ ABSENT — SC229; no C8 (3rd audit without fix) |
| model-ceiling-detection.md C8 | ✗ Veo 3.1 Lite I2V in escalation path — **21st audit without fix** |
| SC166 differential prompt rule | ✗ ABSENT from model-prompting-guide.md Part 4 — **20th audit** (now validated by Stand-In + WildActor papers) |

**New gaps this window:**
- SC231: Remotion 4.0.494 Sequence opacity fix — no CLAUDE.md Remotion version refs; no C8 but production capability in skill only
- SC232: ffmpeg-normalize `--threshold` / `aac-no-longer-required` — no C8
- SC233: Stand-In / WildActor — Future Watch sections, both no-API-yet; no C8
- SC234: **Wan 2.2 Animate Replace — NEW GAP.** CONFIRMED $0.06/generation (24× cheaper than Kling Pro) with full parameters. Not in CLAUDE.md routing matrix. Highest-ROI canary on platform, fully documented in skill, invisible in CLAUDE.md.
- All other gap ages +1. **Zero gaps resolved this window.**

### Hindsight Status

Hindsight daemon: **NOT running** (last log entry: 2026-04-13 15:14:48 UTC — **99 days ago**). Banks unverified. Recall: non-functional. Persistent ARCHITECTURAL issue.

SKILL_AUDIT_COMPLETE

---

## AUDIT 3 — CREATIVE OUTPUT QUALITY

**Last approved video:** V3-Tarik-v2-couple (2026-04-26) — **88 days ago.** No new creative output this window.

**Family lock status:** `testimonial` family, 3/6 videos approved. 3 more required before family unlock (lock_until: 6).

**Cost metric:** Credits per approved video = MATHEMATICALLY UNDEFINED (zero new output, day 88).

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

### New Production Intelligence (SC231–SC234)

**Caption pipeline (SC231):**
- Remotion 4.0.494 — upgrade fixes Sequence opacity for caption fade-out animations. `npm install remotion@4.0.494`.
- CSR caption CSS warning: `-webkit-text-stroke` and `paint-order` may not render in `renderMediaOnWeb()`. Server-side render (our pipeline) unaffected.

**Halal audio (SC232):**
- **ffmpeg-normalize v1.41.0 — `aac` no longer required for MP4.** Remove `-c:a aac` flag from normalize command.
- **`--threshold 1.0` recommended** — skips files already within 1 LU of target; saves I/O on already-normalized clips.
- v1.40.0 non-zero exit on failure — add to health check if used in CI context.

**Character consistency (SC233):**
- **Stand-In validates differential prompt rule:** Use "a man", "a worker" — NOT "Karel with black crewneck, orange logo." Identity in reference image, action only in prompt.
- **WildActor AIPA proves architectural reason:** Character attributes in text COMPETE with identity flow. Prompt must be action+camera only.
- Neither on AIMLAPI; both confirm our existing Step 3a policy is architecturally correct.

**Cost optimization (SC234):**
- **Wan 2.2 Animate Replace: $0.06/generation CONFIRMED.** `alibaba/wan2.2-14b-animate-replace`, params: `video_url` (driving), `image_url` (reference), `resolution: "720p"`. HIGHEST PRIORITY CANARY — run Move mode first, then Replace.
- **LTXV routing: stop using `ltxv/ltxv-2-fast` for new shots.** Route B-roll non-char I2V to `minimax/hailuo-2.3-fast` ($0.0416/sec) exclusively until AIMLAPI adds `ltxv/ltxv-2-3-fast`.
- Krea WAN 14B V2V at $0.026/sec — cheapest restyling on AIMLAPI; canary priority HIGH.

### Workflow Gaps (updated)

- **CLAUDE.md Pre-Gen Check #5 still wrong (25th audit).** "15-40 words" → 2.3 rerolls average on Kling v3 Pro character shots.
- **ElevenLabs v1 confirmed retired July 9, 12 days past (25th flag).** Next voiceover session → guaranteed 404. Use `eleven_v3` (TTS production), `eleven_flash_v2_5` (TTS draft), `scribe_v2` (captions).
- **LTXV Aug-15 deadline (25 days).** Do NOT route new production shots to LTXV. Hailuo 2.3 Fast is the B-roll non-char I2V replacement.
- **Wan 2.2 Animate Replace canary outstanding (SC234).** $0.06/generation, parameters confirmed. No canary completed. 24× cheaper than Kling Pro for character animation shots.
- **SC228-233 absent from data/pipeline.db study_log.** Production session querying study_log misses: liquidContours/skew, blockReason routing, end_image_url, Remotion 4.0.494 opacity fix, ffmpeg-normalize flags, Stand-In/WildActor rule validation.
- **model-ceiling-detection.md C8 (21st audit):** Veo 3.1 Lite I2V in escalation path is wrong. One-line removal.
- **SC166 differential prompt rule (20th audit):** Now validated by Stand-In and WildActor papers. One bullet to model-prompting-guide.md Part 4.

### Ralph Loop

*"What would a senior creative director still reject?"*

1. **88 days of production stagnation while the Wan 2.2 Animate Replace canary ($0.06) has been the highest-priority unrun test for two consecutive cost-optimization cycles (SC220, SC234).** Parameters are confirmed. Billing is confirmed. Model strings are confirmed. Canary sequence is documented (Move mode → Replace mode). A 15-minute canary session would either unlock $0.06/generation character animation shots (vs. $1.46 Kling Pro = 24× savings) or provide a definitive "not production-quality" verdict. Nothing blocks this except no production session was run.

2. **ElevenLabs v1 has been retired for 12 days and is STILL not removed from CLAUDE.md.** The next voiceover session will produce a guaranteed 404 on `eleven_monolingual_v1`. The pipeline operator would see a network error and spend time debugging a known, flagged, documented issue. A 5-minute CLAUDE.md edit (Check #7 update + grep note) would prevent this completely. This has been flagged for 25 consecutive audits without action.

3. **SC233 brought Stand-In and WildActor — two independent papers both proving that our differential prompt rule (SC166) is architecturally correct — yet SC166 is still absent from model-prompting-guide.md Part 4 for the 20th consecutive audit.** The rule exists empirically in practice. The papers are now documented in character-consistency.md. The formalized one-bullet rule is not in the prompting guide. A session doing character retries must re-derive the rule from first principles rather than reading it at the top of Part 4.

**Overall Creative: (3.9 + 4.2 + 4.1) / 3 = 4.07 / 5.0** (→ unchanged, day 88 of production stagnation)

CREATIVE_AUDIT_COMPLETE

---

## ACTION ITEMS

### [P0 — CRITICAL — 25th audit — CLAUDE.md Pre-Gen Check #5 Wrong Prompt Length]

**1. Fix "15-40 words" to Kling v3-correct range**

```
Current:  Motion prompt: 15-40 words, motion ONLY, defined endpoint ("eases to stop")
Correct:  Motion prompt: I2V 40-120 words / T2V 80-150 words (Kling v3 Pro, July 2026).
          Motion ONLY — action arc + camera move + defined endpoint. (15-40w was Kling v1/v2.)
```

Impact: every character shot session averages 2.3 rerolls at $1.46 each.

---

### [P0 — CRITICAL — OVERDUE 12 DAYS — ElevenLabs RETIREMENT — 25th audit]

**2. CLAUDE.md Pre-Gen Check #7 — v1 retirement + language_code note + Check #9 syntax fix**

```
⚠️ RETIRED JULY 9, 2026: eleven_monolingual_v1 + eleven_multilingual_v1 + scribe_v1 → 404 NOW.
Use eleven_v3 (TTS production) + eleven_flash_v2_5 (TTS draft) + scribe_v2 (captions).
NOTE: language_code NOT supported on eleven_multilingual_v2 (silently ignored, June 29, 2026).
grep -r "monolingual_v1\|multilingual_v1\|scribe_v1" scripts/ before voiceover work.
```

Fix Check #9 syntax: `face adherence 80-90 (NOT default 42)` → `face_consistency: true`

---

### [P0 — 25-DAY DEADLINE — LTXV Aug 15 Alert]

**3. CLAUDE.md routing matrix B-roll row — add LTXV 2.3 string alert + Wan 2.2 Animate Replace entry**

```
⚠️ LTXV DEADLINE Aug 15 (25 days): ltxv/ltxv-2-fast WILL ERROR. Do NOT route new shots here.
Use minimax/hailuo-2.3-fast ($0.0416/sec I2V) for non-char I2V until AIMLAPI adds ltxv/ltxv-2-3-fast.
```

Add Wan 2.2 Animate Replace to routing matrix:

```
Character animation canary | Wan 2.2 Animate Replace | $0.06/gen | alibaba/wan2.2-14b-animate-replace
                          (video_url: drive video, image_url: ref photo, resolution: "720p")
```

---

### [P0 — DATA INTEGRITY — study_log missing SC228-233]

**4. Retroactively insert SC228-233 into data/pipeline.db study_log**

SC234 (cycle 234) confirmed in study_log. SC228-233 absent. ALSO: SC231/232 had correct data/ path log commits but entries did NOT land in study_log — investigate schema-level write failure.

---

### [P0 — OPERATIONAL — model-ceiling-detection.md C8 — 21st consecutive audit]

**5. Remove Veo 3.1 Lite I2V from video escalation path** (one-line removal)

---

### [P0 — BEFORE NEXT CHARACTER SHOT SESSION — SC166 differential prompt rule]

**6. model-prompting-guide.md Part 4 — add SC166 differential prompt rule (20th audit, now validated by 2 papers)**

```
On facial-movement retries: use action-only prompts; strip identity-descriptive words.
(Validated by Stand-In (arXiv 2508.07901) + WildActor (arXiv 2603.00586) — both confirm
that character attributes in text compete with identity flow. Text = action+camera ONLY.)
```

---

### [P1 — BEFORE NEXT PRODUCTION SESSION]

**7. Wan 2.2 Animate Replace canary (SC234):**
- Step 1: Pass NBP Edit hero frame as `image_url` + simple drive video as `video_url`, mode: Move
- Step 2: Verify output quality + confirm $0.06 billing in AIMLAPI credit log
- Step 3 if Move passes: Run Replace mode with existing B-roll + hero frame

**8. Remotion 4.0.494 upgrade (SC231):** `npm install remotion@4.0.494` — fixes Sequence opacity bug affecting caption fade-out animations.

**9. ffmpeg-normalize update (SC232):** Add `--threshold 1.0` to normalize command; remove `-c:a aac` flag (v1.41.0 infers from container). Run `pip install ffmpeg-normalize --upgrade` to get v1.41.1.

**10. Krea WAN 14B canary (SC234):** T2V at $0.165/5s — run one 5s establishing shot before next B-roll session to unlock cheapest T2V on AIMLAPI (50% cheaper than Veo 3.1 Lite).

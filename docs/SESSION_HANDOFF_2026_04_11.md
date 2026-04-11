# Session Handoff Report — 2026-04-11
## Complete state for fresh context continuation

---

## CURRENT STATUS: Pre-operational. 0/3 videos approved. Preparing for complete pipeline rebuild (6 phases).

## WHAT WAS ACCOMPLISHED THIS SESSION

### Test Productions (all rejected)
- **V1 "Meet the Team"**: 5 shots, 15s. Rejected: black bars (square hero frames), character inconsistency, choppy motion, bad captions. Cost: ~$9.10
- **V2 "Meet the Team" redux**: 2 shots, 10s. Rejected: ghost truck, breathing artifacts, doubled captions. Cost: ~$3.46
- **V3 "Verhuizen zonder zorgen"**: 5 shots, 15s. Rejected: ghost truck AGAIN, fabricated URL "sedeerhuiren.nl", choppy motion, bad captions. Cost: ~$8.12
- **One clip passed all 4 tiers**: A3-S4 Box Detail Close-up (static object, no people, minimal camera, close-up)

### Audits Completed
- **Operator Audit**: Score 2.40/5.00. 54% discipline failures, 31% operational, 8% ceiling, 0% architectural.
- **Skill Library Audit**: 0/11 skills pass all 8 criteria. 49% avg invocation rate. CLAUDE.md at 86 instructions (too many).
- **Creative Output Audit**: 1/11 clips passes all tiers (9%). 82% of failures fixable. 18% model ceiling.
- **Full report**: `/opt/pipeline/docs/COMBINED_AUDIT_REPORT_FULL.md`

### Research & Documentation
- **Model Prompting Guide**: `/opt/pipeline/skills/model-prompting-guide.md` (441 lines, 7 parts covering all models)
- **AI Automation Audit Framework v2**: `/opt/pipeline/docs/AI_AUTOMATION_AUDIT_FRAMEWORK_v2.md`
- **3 study cycles completed**: Native 9:16 verified, Kling v3 best practices, caption design overhaul
- **PIPELINE_PLAN.md updated** with real AIMLAPI costs

### Security Fixes Applied
- chmod 600 on session files and database
- node_modules removed from git (9,795 files, 2.1M lines)
- SQLite PRAGMAs: WAL, foreign_keys, busy_timeout=5000
- First database backup created

### CLAUDE.md Updates
- Anti-sycophancy behavioral rules (owner-provided)
- Model Prompting Guide Integration (10 pre-generation checks)
- Production Gates (10 mandatory steps)
- PreToolUse hook on Bash(*aimlapi.com*) for pre-generation gate

---

## THE 6-PHASE PLAN (owner instructions, execute in fresh context)

Full instructions saved at: `/opt/pipeline/docs/PHASE_INSTRUCTIONS.md` (see below)

### Phase 1: Three-Agent Pattern
Encode Planner/Generator/Evaluator in CLAUDE.md as Tier A. Generator cannot self-approve. Evaluator runs in separate context with skeptical persona. Ralph loop on every PASS.

### Phase 2: CLAUDE.md Tier A Rewrite
Reduce from ~86 to ~50 instructions. Move anti-sycophancy body, generation details, telegram details, maintenance to skills. Add: native 9:16, model routing matrix, Kling text ceiling workaround, brand binary checklist, anti-ghost-driving, anti-breathing, Kling character params, Seedance character params (IF available), NBP hero frame params, per-clip video review, caption timestamps, cost ceiling.

### Phase 3: Snorkel Triage
Zero critique on routine tasks. 3-5 loops on creative decisions (hero frame composition, motion prompts, caption timing, model selection, brand elements).

### Phase 4: Hindsight Install
Reinstall hindsight-embed. Replace gpt-4o-mini with local embeddings (ollama available: qwen3.5:2b). Hard caps: 30% RAM, 50% CPU. Migrate 26 markdown lessons. 48h monitor. **Dedicate a monitoring agent** to detect and fix CPU/RAM issues proactively.

### Phase 5: Skill Fixes
- Production-checklist to Tier A
- Negative triggers on all 11 skills
- Character-consistency decision tree in pre-generation gate
- Split higgsfield-generation.md
- New skills: model-ceiling-detection, agent-coordination, seedance-character-prompting, kling-truck-prompting, text-overlay-compositing
- Brand binary checklist + InsightFace + failure classification in video-qa-rubric

### Phase 6: Produce ONE Video with Characters
Only after Phases 1-5 complete. Ask owner for brief. A3-S4 pattern: close-ups, simple compositions, one subject per shot, never people+truck+text simultaneously. Character sheets first. Full Planner→Generator→Evaluator flow. InsightFace similarity checks. Word-level caption timestamps. Text as post-overlay only. Deliver with per-clip Evaluator scores.

---

## CRITICAL BLOCKERS IDENTIFIED

1. **Seedance 2.0 blocked on AIMLAPI** for human faces (content_policy_violation, 3x tested). **Decision: Kling v3 Pro with Subject Binding 80-90 is primary for characters.** Seedance only via Atlas Cloud ($0.022/sec) if added later.

2. **InsightFace not installed.** Needed for Evaluator face similarity checks. Install via pip.

3. **whisper-cpp not installed.** Needed for caption word-level timestamps. Install via @remotion/install-whisper-cpp or test ElevenLabs REST API directly.

4. **Hindsight daemon dead.** hindsight-embed not in PATH. Last used >33h ago. Ollama available for local embeddings.

5. **Brand color is #FC8434** (confirmed in brand-identity.md). The instruction's reference to #F47920 is incorrect.

---

## KEY FILES

| File | Purpose |
|------|---------|
| `/opt/pipeline/CLAUDE.md` | Pipeline rules (needs Phase 2 rewrite) |
| `/opt/pipeline/skills/model-prompting-guide.md` | Definitive prompting reference (441 lines) |
| `/opt/pipeline/skills/production-checklist.md` | Mandatory QA gates |
| `/opt/pipeline/docs/COMBINED_AUDIT_REPORT_FULL.md` | Full 746-line audit |
| `/opt/pipeline/docs/AI_AUTOMATION_AUDIT_FRAMEWORK_v2.md` | Correct audit paradigm |
| `/opt/pipeline/docs/PHASE_INSTRUCTIONS.md` | Full 6-phase instructions (create from Telegram messages) |
| `/home/farouq/.claude/projects/-opt-pipeline/memory/MEMORY.md` | Memory index (27 entries) |
| `/opt/pipeline/data/pipeline.db` | SQLite: briefs, generation_history, learned_preferences, feedback_log |
| `/opt/pipeline/assets/crew/` | Mourad and Karel reference photos |
| `/opt/pipeline/assets/truck/` | Truck reference photos |
| `/opt/pipeline/assets/brand/` | Box reference sheet, workwear reference |

## GIT STATE
- Branch: main
- 25+ commits this session
- All changes committed
- Not pushed to remote

## BUDGET
- ~$40 remaining on AIMLAPI (Farouq added $50, spent ~$10)
- Phase 6 target: $15 per video max
- Hindsight/InsightFace/whisper installs: $0

## OWNER COMMUNICATION
- Telegram chat_id: 1677012496
- Owner name: Farouq
- Voice messages: download via MCP, convert OGA→MP3, transcribe via ElevenLabs STT (production use only, never for study)
- Always send "even bezig" before tasks >30 seconds
- Anti-sycophancy: flag issues BEFORE owner asks, never send marginal work

## MEMORY ENTRIES (27 files)
All at `/home/farouq/.claude/projects/-opt-pipeline/memory/`. Key ones:
- feedback_anti_sycophancy.md — Stop being a yes-man
- feedback_v3_critical_failures.md — Must watch every clip before assembly
- feedback_reference_based_generation.md — Always use actual reference images
- feedback_aspect_ratio_native.md — Generate NATIVELY in 9:16, never crop/zoom/pad
- feedback_video_motion_quality.md — Kling v3 motion issues likely our settings, not model
- project_session_2026_04_10.md — Full first session summary
- reference_audit_framework.md — AI-automation audit framework v2

## NEXT ACTION
Clear context, then execute Phases 1-5 sequentially. Phase 6 only after owner approval of the rebuild. Dedicate a monitoring agent for Hindsight CPU/RAM.

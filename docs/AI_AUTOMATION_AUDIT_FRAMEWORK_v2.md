# Auditing AI-Automation Systems Where the AI Is the Runtime
## Snelverhuizen Pipeline Framework — Revision 2

The previous audit committed a category error: it evaluated an AI-automation system using a software engineering framework. When Claude Code (Opus 4.6) is the orchestrator, markdown skill files are SOPs, and CLAUDE.md is the policy document, the correct evaluation paradigm comes from agent evaluation, not code review. AI-as-runtime systems require probabilistic evaluation of judgment quality, trajectory analysis, and outcome grading — not test suites, architecture scores, or demands for a Python daemon.

However, the original document's conclusion of "operational with three improvement vectors" was too generous. Zero approved videos after three attempts is not operational. The honest framing is **"pre-operational with proven architecture."** The agent pattern is legitimate, the security findings were valid and have since been remediated, but the system has not yet demonstrated end-to-end success. The three improvement vectors must be implemented BEFORE the system can be called operational, not after.

The original document missed an entire failure category: model capability ceiling. If Kling v3 at $1.46/5s produces structurally choppy motion or expression drift, no amount of prompting fixes that. The audit framework must distinguish "the agent did it wrong" from "the model cannot do this well enough yet."

---

## Failure category framework (the missing fourth dimension)

When the pipeline produces an unapproved video, the diagnostic question is "where in this decision tree does the failure originate?" There are now **four** categories, not three.

**ARCHITECTURAL failures** (rebuild needed): over-privileged identities, missing control planes, no idempotency. Test: would a structural boundary have prevented this? For Snelverhuizen, almost no failures fall here — the architecture is correct.

**OPERATIONAL/PROCEDURAL failures** (improve skills): ambiguous SOPs, missing skill coverage, poor tool documentation. Test: was the agent making reasonable decisions given the instructions it had? For Snelverhuizen, missing self-critique skill, missing brand-validation skill, missing model-selection skill all fall here.

**DISCIPLINE failures** (self-critique protocols): agent had what it needed and didn't use it. Test: does the agent have everything but isn't applying it? Generator-as-evaluator cycles, ignoring stored Hindsight lessons, no Ralph loop.

**MODEL CAPABILITY CEILING failures** (escalate or accept) — NEW: the underlying generation model cannot produce the required quality at any prompt sophistication. Indicators: same artifact across 5+ varied prompts, artifact appears in industry benchmarks for that model, competing models in the same price tier produce the same artifact. Examples for video: choppy motion at low credit tiers, expression drift over 8s+, hand anatomy on rapid action, text rendering. **The audit must explicitly tag failures here so the team escalates to a more capable model or accepts the limitation rather than blaming the operator.**

For each failure: classify into ONE of the four. Stop blaming the operator for ceiling problems. Stop blaming the model for discipline problems.

---

## Hindsight memory: implementation with caution

Hindsight will be implemented in this pipeline, with monitored rollout. Earlier installation caused CPU/RAM problems, so the approach is: install, monitor 48 hours, intervene immediately if resource issues recur. Once stable, the audit recommendations become directly applicable.

The current markdown memory system is **too passive** — lessons are saved but not proactively retrieved. Hindsight's semantic retrieval (91.4% on LongMemEval vs Mem0 49% and Zep 63.8%) fixes this gap with four-strategy parallel retrieval (semantic, BM25, graph traversal, temporal) and cross-encoder reranking.

**Critical audit points once installed:**

**Auto-recall firing**: UserPromptSubmit hook must query Hindsight on every prompt and inject relevant memories as `additionalContext`. Verify via `HINDSIGHT_LOG_LEVEL=debug` showing "Found N memories." Without this, the system stays passive.

**Auto-retain firing**: Check `retainEveryNTurns` configuration. Significant decisions should be captured automatically, not require manual storage.

**Bank scoping**: Verify `dynamicBankId` and `dynamicBankGranularity` in `~/.hindsight/claude-code.json` are set to project scope, not global.

**Lesson application rate**: When correction-derived memories are recalled, does the agent actually avoid repeating the same mistake? **Target >50%**. Track by logging when correction memories surface and checking whether the same error recurs in the next attempt.

**Signal-to-noise ratio**: >60% of stored memories should be useful. Append-only memory degrades over time — periodic consolidation is essential. The FiFA benchmark showed naive retention degrading task completion versus structured forgetting.

**Absence test**: Temporarily disable auto-recall, compare agent behavior, confirm quality degrades. If it doesn't, the memory system isn't contributing value and should be reconfigured.

**Resource ceiling**: Hard memory and CPU caps at install time. If Hindsight exceeds 30% RAM or 50% CPU sustained, kill and reconfigure. The previous failure was unbounded resource consumption — that must not recur.

---

## Security findings remain valid (and have been fixed)

The paradigm shift from software-audit to agent-audit was correct. But world-readable credentials, missing firewall rules, and node_modules in git tracking are real risks that don't disappear when the evaluation framework changes. The original framework document treated security as out-of-scope for AI-automation review — that was wrong. **An AI-automation system with leaked credentials is a dangerous AI-automation system, regardless of how its architecture is categorized.**

These findings have been remediated:
- chmod 600 on session files and database
- node_modules removed from git tracking, added to .gitignore
- SQLite PRAGMAs configured (WAL, synchronous=NORMAL, busy_timeout=5000, foreign_keys=ON)
- Telegram allow-list restricted to owner ID only

Security audit must be a permanent layer in every audit cycle, parallel to operator/skill/output audits. The categories are different but both matter.

---

## The three-agent architecture is the highest-priority fix

Anthropic's March 2026 harness design research states explicitly: **"Self-evaluation is unreliable. Tuning a standalone evaluator to be skeptical is far more tractable than making a generator critical of its own work."** This single finding explains why three attempts produced the same class of failures — Claude was generator AND evaluator simultaneously, with all the bias that creates.

**The fix is the three-agent pattern:**

**Planner agent**: Receives the brief, decomposes into shots, assigns model selection, defines acceptance criteria upfront. Output: structured production plan with explicit quality gates per shot.

**Generator agent**: Executes each shot. Calls Higgsfield/AIMLAPI, generates assets, drafts captions. Has NO authority to mark anything "approved" — only "produced and ready for evaluation." This separation is the entire point.

**Evaluator agent**: Receives generated output PLUS the original acceptance criteria from the Planner. Runs in a separate context window with a skeptical persona. Scores against the four-tier rubric. Returns PASS / RETRY-WITH-NOTES / REJECT-AND-ESCALATE. The Evaluator never sees the Generator's reasoning, only its output — preventing rationalization bias.

The Ralph loop sits on top: when the Evaluator returns PASS, a final check asks "are you really done? what would still concern a senior creative director?" before the work goes to the owner.

**This is the highest-impact change the pipeline can make.** It directly attacks the root cause of the three failed attempts. Implement this before any other improvement.

---

## Snorkel AI triage: stop wasting critique on routine tasks

Snorkel AI's stress test of self-critique loops revealed a paradox that maps directly to the Snelverhuizen failures. On easy tasks, 5 critique loops dropped Claude Sonnet 4.5's accuracy from **98.1% to 56.9%** — the critic hallucinated errors that didn't exist. On hard tasks, 5 critique loops jumped accuracy from **0% to 60%** — real errors finally got caught.

**The discipline failure in the previous attempts was not "no critique" — it was "uniform critique."** Routine tasks (file naming, format checks, render queue management) probably got the same shallow review as creative decisions (hero frame composition, motion prompts, caption timing). The triage protocol fixes both ends:

**Zero critique loops for routine tasks**: file management, standard renders, status updates, queue operations, log writes. These have right answers and the critic adds noise.

**3-5 critique loops for creative decisions**: hero frame composition, character reference selection, motion prompts, scene transitions, caption timing, brand color matching, model selection per shot complexity. These have judgment dimensions and the critic catches real problems.

**Explicit criteria per critique loop**: not "is this good?" but "does this match the brand color spec? does this maintain temporal consistency? does the hero frame anchor the action?" Vague critique is the same as no critique.

The triage rule must be encoded in CLAUDE.md (not buried in a skill) because skill invocation reliability is too low (see next section).

---

## Skill invocation: the 56% failure rate that explains everything

Vercel's Q1 2026 controlled evaluations found that **skills failed to invoke 56% of the time** even when available and relevant. This single finding likely explains why stored feedback wasn't applied across the three failed attempts — the production-checklist skill may not have been triggering. The agent had the lessons but never read them.

**The fix has two parts:**

**First**: critical rules that require near-100% compliance must be promoted from skill files to CLAUDE.md content, accepting the context cost. Examples for Snelverhuizen: "every video clip MUST be visually inspected before assembly," "every shot MUST verify brand color compliance," "every character clip MUST verify reference frame match," "every approval MUST go through the Evaluator agent, never the Generator." These cannot live in skills with 44% reliability.

**Second**: skill descriptions must include both positive AND negative trigger conditions. Without negative conditions, skills fire on irrelevant queries or fail to fire when needed. Every skill description gets the format: "Use when X. Do NOT use when Y." Test invocation rate after the change.

**Audit metric**: invocation rate per skill across the next 30 sessions. Target >80% when relevant. Skills under 50% are broken regardless of content quality.

---

## CLAUDE.md compliance and the 150-instruction wall

Anthropic's research indicates CLAUDE.md compliance sits around **70%** at moderate sizes, dropping further as length increases. Claude Code's own system prompt already consumes ~50 instruction slots. The practical ceiling for project-level CLAUDE.md is **~100 additional instructions** before compliance becomes unreliable.

**The Snelverhuizen CLAUDE.md is growing fast.** Triage is essential:

**Tier A (must be in CLAUDE.md)**: rules that protect against expensive failures or compliance violations. Three-agent enforcement, Snorkel triage rule, brand color spec, Shari'ah compliance gates, cost ceiling. Maximum 50 entries.

**Tier B (skill files with explicit invocation triggers)**: detailed procedures, reference material, style guides, model-specific prompt patterns. These can tolerate 56% invocation rate because they're advisory, not protective.

**Tier C (hooks for 100% enforcement)**: rules that must NEVER be violated. PreToolUse hooks that block dangerous operations. PostToolUse hooks that verify state after destructive actions. Stop hooks that prevent "completion" without Evaluator sign-off. The gap between 70% advisory compliance and 100% hook enforcement is the difference between operational discipline and architectural guarantee.

**Audit action**: every quarter, audit CLAUDE.md for instructions that have not influenced any decision in the last 30 sessions. Delete or demote them.

---

## On cost-per-success: the budget defense and the data

The original framework cited a $720/video benchmark from Clarity Media as a sanity check on the $5-10/video target. The comparison was misleading. Clarity Media is a full-service human agency with editors, multiple revision rounds, and client management overhead — fundamentally a different model. The whole point of AI-automation is structurally lower cost, and the budget is a deliberate strategic constraint, not a mistake.

However: the data still says zero approved videos at any price. The honest cost metric is credits per APPROVED video, not credits per generation attempt. With 0 approvals, that ratio is undefined — not "high," not "expensive," but mathematically undefined because the denominator is zero.

**The right framing for the audit:**
- Budget target: $5-10 per approved video (deliberate, defensible)
- Current cost-per-success: undefined (no successes exist)
- Cost-per-attempt: $3-7 (within budget per attempt, but every attempt currently produces zero approved output)
- The fix is not "spend more per attempt" — the fix is "improve the pipeline so attempts produce approvals"

Once the three-agent pattern is in place and the first 5 videos are approved, cost-per-success becomes a meaningful metric. Until then, tracking cost-per-attempt is meaningless because all attempts cost money and produce nothing.

---

## Verdict: pre-operational with proven architecture

The system is not "operational with improvement vectors." It is **pre-operational with proven architecture and identified blockers.** The architecture (Claude Code + skills + Hindsight + Telegram) is legitimate and documented. The security holes have been fixed. But three operational requirements remain unmet:

1. **Three-agent pattern not yet implemented** — Generator and Evaluator are still the same context. This is the #1 blocker.
2. **Snorkel triage protocol not yet encoded** — critique discipline is uniform across task types.
3. **Hindsight not yet stably installed** — proactive memory retrieval is the gap that lets old failures repeat.

Once all three are in place and the first 5 videos pass owner approval, the system moves from pre-operational to operational. Until then, calling it operational is dishonest framing that delays the real fixes.

**Confidence on this assessment: 88%.** The 12% uncertainty is about model capability ceilings — some current failures might be ceiling problems rather than discipline problems, and we won't know which until the three-agent pattern surfaces them clearly.

---

## What changed from Revision 1

1. Hindsight section rewritten from "audit existing system" to "implementation with monitored rollout and resource caps"
2. Verdict downgraded from "operational with three vectors" to "pre-operational with proven architecture"
3. Security findings restored as a permanent parallel audit layer (not out-of-scope)
4. $720/video comparison removed; cost-per-success reframed as undefined until denominator >0
5. Three-agent architecture promoted from "recommendation" to "highest priority fix" with explicit Generator/Evaluator/Planner role definitions
6. Snorkel triage added as a CLAUDE.md tier-A rule, not a buried skill
7. Skill invocation 56% failure rate added as the explanation for why stored lessons weren't applied
8. CLAUDE.md three-tier triage (A/B/C) introduced with explicit instruction count limits and hook escalation path
9. Model capability ceiling added as a fourth failure category — the most important addition. The audit must distinguish operator failures from skill failures from discipline failures from model-can't-do-this failures.

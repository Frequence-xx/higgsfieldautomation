---
name: Credit Efficiency
description: Rules for the static-first validation funnel, model routing, and credit conservation to keep monthly usage within the 6,000 credit budget.
autoInvoke: true
triggers:
  - generation
  - credits
  - budget
  - model selection
---

# Credit Efficiency Rules

## Static-First Validation Funnel

**NEVER spend video credits without a passed static frame first.**

For any shot costing >10 credits:
1. Generate a still frame using an unlimited/cheap image model (Flux.2 Pro, Seedream, Nano Banana — 0-2 credits)
2. Run the still through the full QA rubric (all 8 dimensions including Shari'ah compliance)
3. Only if the still passes → proceed to video generation
4. If the still fails → fix the prompt and regenerate the still (free/cheap)

This catches composition errors, compliance violations, and brand mismatches before any significant credits are spent.

## Model Routing

| Budget tier | Model | Credits | Use for |
|-------------|-------|---------|---------|
| Economy (80% of shots) | Kling 3.0 | ~6 | Establishing shots, truck footage, interiors, B-roll, medium shots |
| Premium (15% of shots) | Cinema Studio + base model | ~12-20 | Hero shots needing camera control, reference-anchored shots |
| Ultra (5% of shots) | Veo 3.1 | 40-70 | Money shot only — emotional climax, reveal, CTA. ALWAYS static-first. |
| Free/cheap | Flux.2 Pro, Seedream, Nano Banana | 0-2 | Static frame validation, storyboard frames, composition testing |

## Monthly Budget

- **Total allocation:** 6,000 credits/month
- **Month 1 target:** 30-35 videos (~4,800 credits at 2× iteration)
- **Steady state target:** 50 videos (~3,120 credits at 1.3× iteration)
- **Warning threshold:** Notify owner at 4,500 credits consumed
- **Hard stop:** At 5,500 credits, switch to Kling 3.0 only (no premium models)
- **Emergency reserve:** Always keep 500 credits for re-generations and fixes

## Rules

1. Check remaining credits before starting any batch
2. Log every generation with model and credit cost in SQLite
3. If a shot fails QA 3 times, do NOT keep burning credits — escalate to owner
4. Prefer Kling 3.0 unless the shot specifically requires camera control or premium quality
5. Never use Veo 3.1 for establishing shots or B-roll — that's credit waste
6. Track per-model success rates in learned_preferences — route future shots to the most efficient model

---
name: Model Ceiling Detection
description: Detects when a model has hit its quality ceiling for a given shot type. Prevents wasted credits by routing to a stronger model or simplifying composition after 2 consecutive failures.
autoInvoke: true
triggers:
  - QA fail
  - regeneration
  - retry
  - model failure
  - low score
  - ceiling
negatives:
  - Do NOT invoke on a first-attempt failure (single failures are normal — retry with corrective prompt first)
  - Do NOT invoke when the failure is Shari'ah compliance (that is a content issue, not a model ceiling)
  - Do NOT invoke when the failure is a prompt error that can be fixed without changing models
---

# Model Ceiling Detection

Detect when a model cannot produce acceptable output for a given shot type. Prevent wasted credits by escalating early.

## The Rule

**When a model fails the same shot type 2 consecutive times with any QA dimension scoring <6, mark that model/shot-type combination as a ceiling.**

MUST NOT retry the same model for the same shot type more than 2 times. After 2 failures, escalate.

## Detection Criteria

A "failure" for ceiling detection means:

- Any QA dimension scores <6 on the generated output, AND
- The corrective prompt on retry 2 did not raise the score above 6, AND
- The failure category is Cat B (model limit) — not Cat A (prompt-fixable)

See `video-qa-rubric.md` for failure category classification.

## Ceiling Logging

When a ceiling is detected, log to `learned_preferences` in SQLite:

```sql
INSERT INTO learned_preferences (key, value, updated_at) VALUES (
    'ceiling:<model_string>:<shot_type>',
    json_object(
        'model', '<model_string>',
        'shot_type', '<shot_type>',
        'failing_dimensions', '<comma-separated dimension names>',
        'best_score_achieved', <highest score from 2 attempts>,
        'attempts', 2,
        'detected_at', datetime('now'),
        'notes', '<brief description of the failure pattern>'
    ),
    datetime('now')
);
```

## Escalation Protocol

After marking a ceiling, route to the next-tier model:

### Image Model Escalation

```
Nano Banana Pro (text-only)
  → Nano Banana Pro Edit (add references)
    → Flux Kontext Max (character lock)
      → Flux Pro v1.1 Ultra (highest quality)
        → STOP: simplify composition
```

### Video Model Escalation

```
Kling v3 Standard I2V
  → Kling v3 Pro I2V
    → Kling O1 Reference-to-Video (character binding)
      → Veo 3.1 Lite I2V
        → STOP: simplify composition
```

### Composition Simplification (Last Resort)

If the highest-tier model also hits a ceiling:

1. **Reduce subject count:** One person per shot, never people + truck + text simultaneously
2. **Widen the framing:** Medium → wide, close-up → medium (wider = less detail to get wrong)
3. **Remove motion complexity:** Walking → standing, carrying → holding still
4. **Remove text from generation:** Composite ALL text in post-production
5. **Shorten duration:** 5s → 3s (less time for artifacts to accumulate)
6. **Log the simplified approach** and notify owner via Telegram

## Pre-Generation Ceiling Check

Before generating ANY shot, query learned_preferences:

```sql
SELECT value FROM learned_preferences
WHERE key = 'ceiling:' || '<model_string>' || ':' || '<shot_type>';
```

If a ceiling record exists for this model/shot-type combination:
- MUST skip directly to the next-tier model
- SHOULD notify the operator that a known ceiling was avoided
- MAY re-test the ceiling monthly (models update, ceilings can be lifted)

## Monthly Ceiling Review

On the first production run each month:

1. Query all ceiling records older than 30 days
2. Run a single canary test for each with the original prompt
3. If the score now exceeds 7 on all dimensions, remove the ceiling record
4. If the score still fails, update `detected_at` and keep the record

## Integration with Three-Try Fallback

The three-try fallback chain in `model-prompting-guide.md` Part 6 aligns with this skill:

- **Try 1:** Primary model per routing matrix
- **Try 2:** Corrective prompt (if Cat A) or next-tier model (if Cat B)
- **Try 3:** Conservative fallback — reduce motion, shorten duration, simplify composition

After Try 3 fails: STOP, escalate to owner with specific frames, failure codes, all 3 prompts tried, and a recommendation.

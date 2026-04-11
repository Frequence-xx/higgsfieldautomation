# Snelverhuizen Pipeline — Combined Audit Report
## Operator + Skill Library + Creative Output
### Date: 2026-04-11

---

# PART 1: OPERATOR AUDIT

## Operator Score: 2.40 / 5.00

| Dimensie | Gewicht | Score | Gewogen |
|----------|---------|-------|---------|
| Reasoning | 20% | 2/5 | 0.40 |
| Execution | 20% | 3/5 | 0.60 |
| Memory | 15% | 1/5 | 0.15 |
| Reliability | 20% | 2/5 | 0.40 |
| Integration | 15% | 3/5 | 0.45 |
| Social | 10% | 4/5 | 0.40 |

## Findings

### REAS-001 — Geen alternatieven-analyse bij creatieve keuzes
- **Category:** DISCIPLINE | **Severity:** Hoog | **Confidence:** 95%
- Poging 1 begon met text-only prompts zonder te overwegen of referentie-gebaseerd beter zou zijn — ondanks dat character-consistency.md dit voorschreef. Resultaat: 4 hero frames weggegooid ($0.78).
- **Fix:** Three-agent pattern. Planner-agent moet alternatieven overwegen vóór generatie.

### REAS-002 — Geen model-selectie onderbouwing
- **Category:** OPERATIONAL | **Severity:** Medium | **Confidence:** 85%
- Skill beschreef WANNEER welk model, maar operator checkte dit niet per generatie.
- **Fix:** Model-selectie tabel als Tier A regel in CLAUDE.md.

### EXEC-001 — Video clips NIET bekeken voor assembly
- **Category:** DISCIPLINE | **Severity:** Kritiek | **Confidence:** 100%
- Directe oorzaak van ghost-driving trucks en expression drift in alle 3 eindproducten. Operator extraheerde QA frames van stills maar niet van video's.
- **Fix:** Three-agent pattern. Generator mag niet "klaar" zeggen.

### EXEC-002 — Caption timestamps 3x handmatig geschat
- **Category:** OPERATIONAL | **Severity:** Hoog | **Confidence:** 90%
- SOP zei "gebruik echte timestamps" maar specificeerde niet HOE. ElevenLabs STT gaf alleen tekst.
- **Fix:** Concrete procedure: ElevenLabs met word_timestamps=true, of Whisper lokaal. Schat NOOIT.

### EXEC-003 — Choppy/laggy motion in alle pogingen
- **Category:** MODEL CAPABILITY CEILING (deels) + DISCIPLINE (deels) | **Severity:** Medium | **Confidence:** 70%
- Poging 1-2: verkeerde API parameters. Poging 3: correcte settings maar nog steeds issues. Onvoldoende data om ceiling vs operator te scheiden.
- **Fix:** Systematische test nodig met optimale settings.

### MEM-001 — Memory lesson application rate <20%
- **Category:** DISCIPLINE | **Severity:** Kritiek | **Confidence:** 100%
- 26 memory bestanden opgeslagen. Bewijs: feedback zegt "geen breathing motion" maar poging 3 gebruikte "subtle natural breathing movement." Memory is write-only.
- **Fix:** Hindsight installatie + procedurele afdwinging.

### REL-001 — pass^k = 0% over 3 pogingen
- **Category:** DISCIPLINE | **Severity:** Hoog | **Confidence:** 95%
- Technisch competent (APIs werken) maar creatief onbetrouwbaar (kwaliteitsoordeel te mild).
- **Fix:** Evaluator agent met skeptische persona.

### INT-001 — API integraties werkten pas na trial-and-error
- **Category:** OPERATIONAL | **Severity:** Medium | **Confidence:** 80%
- Verkeerd endpoint, missende parameters, verkeerde model strings — alles ontdekt door te falen.
- **Fix:** Nu gedocumenteerd. Vraag is of het wordt toegepast.

### SOC-001 — Marginal output naar owner gestuurd
- **Category:** DISCIPLINE | **Severity:** Medium | **Confidence:** 85%
- "Hier is de video" zonder "ik heb zorgen over motion quality in shot 2" is oneerlijke communicatie.
- **Fix:** Bij elke aflevering EERST problemen benoemen, DAN het product.

## Primaire Blokkade
De operator beoordeelt zijn eigen werk en accepteert subpar kwaliteit — de generator-als-evaluator bias.

## Failure Category Distributie
| Categorie | Aantal | % |
|-----------|--------|---|
| DISCIPLINE | 7 | 54% |
| OPERATIONAL | 4 | 31% |
| MODEL CEILING | 1 | 8% |
| ARCHITECTURAL | 0 | 0% |

## Status Drie Blokkades
1. Three-agent pattern: ❌ OPEN
2. Snorkel triage protocol: ❌ OPEN
3. Hindsight stabiel: ❌ OPEN

## Top 3 Interventies
1. **Three-agent pattern** (Planner → Generator → Evaluator) — adresseert 54% van failures
2. **Hindsight met 48-uur monitoring** — lesson application van <20% naar >50%
3. **Kritieke regels naar CLAUDE.md Tier A** — van 56% invocation failure naar near-100%

---

# PART 2: SKILL LIBRARY AUDIT

## Skill Health Score: 0/11 skills pass all 8 criteria (0%)
Average pass rate: 4.2/8 (52%). Universal failure: ALL 11 skills lack negative trigger conditions.

## Invocation Reliability: 49% gemiddeld

| Skill | Estimated Rate |
|-------|---------------|
| shariah-compliance | 80% |
| cinematic-standards | 55% |
| video-qa-rubric | 60% |
| viral-research | 20% |
| brief-intake | 65% |
| brand-identity | 60% |
| credit-efficiency | 65% |
| character-consistency | 25% |
| captions-and-titles | 30% |
| production-checklist | 20% |
| higgsfield-generation | 55% |

Kritieke skills (production-checklist, character-consistency, captions-and-titles) hebben de LAAGSTE invocation rates.

## CLAUDE.md Instruction Count
- **Huidig:** ~86 instructies
- **System prompt overhead:** ~50 slots
- **Totaal:** ~136 / ~200 praktisch plafond
- **Aanbevolen Tier A limiet:** 50 instructies
- **Huidig overschot:** ~36 instructies moeten naar Tier B

## Tier Verdeling
- Tier A (CLAUDE.md): 86 instructies (te veel, max 50)
- Tier B (skills): 11 bestanden, ~12.655 woorden
- Tier C (hooks): 0 — geen hooks bestaan

## Hindsight Status: ❌ BLOKKADE 3 NOG OPEN
Profiel bestaat maar daemon draait niet. Laatste activiteit >33 uur geleden. Auto-recall en auto-retain niet functioneel.

## Key Findings

### SKILL-039 — Production-checklist in verkeerde tier (KRITIEK)
De belangrijkste enforcement skill zit in Tier B (56% failure rate) terwijl het Tier A moet zijn. ALLE 10 bekende fouten uit de checklist zijn voorgekomen in productie.
**Fix:** Samenvatting in CLAUDE.md Non-Negotiable Rules + Tier C hook.

### SKILL-033 — Character-consistency niet toegepast (25% invocation)
Text-only prompts gebruikt voor character shots ondanks dat de skill referentie-gebaseerd voorschrijft.
**Fix:** Type A/B/C beslisboom integreren in production-checklist als mandatory pre-generation stap.

### CMD-001 — CLAUDE.md op 86% van capaciteit
Bij 136 totale instructies (50 system + 86 project) zit compliance in de gevarenzone.
**Fix:** Anti-sycophancy body (30 instructies) → skill file. Generation architecture details → verwijderen (al in skills). Telegram details → skill file.

### CMD-004 — Geen production gates in CLAUDE.md
De non-negotiable rules noemen QA scores maar mandateren niet de stap-voor-stap gates.
**Fix:** Toevoegen: "MUST QA elke clip voor assembly. MUST owner approval per clip. NOOIT assembleren van onbeoordeelde clips."

### GAP-006 — Geen cost ceiling enforcement (KRITIEK)
Geen per-video, per-sessie, of maandelijks budget hard cap. Test run kostte $9.10 voor een afgekeurde video.
**Fix:** CLAUDE.md: "MUST NOT exceed $15/video. MUST NOT exceed $50/sessie. Bij 80%: Telegram warning."

## Top 5 Skill Fixes
1. Production-checklist naar Tier A (voorkomt ~80% afwijzingen)
2. Character-consistency invocation fixen (elimineert character drift)
3. Negatieve triggers toevoegen aan ALLE 11 skills
4. higgsfield-generation.md splitsen (image + video)
5. Caption timing regels naar production-checklist

## Top 5 Nieuwe Procedures
1. Cost ceiling enforcement (Tier A)
2. Model capability ceiling detection (Tier B)
3. Per-clip evaluator handoff template (Tier B)
4. Brand compliance binary checklist (Tier B)
5. Agent coordination protocol (Tier B)

---

# PART 3: CREATIVE OUTPUT AUDIT

## Clips Onderzocht
- 11 geanimeerde video clips (4 in V1, 2 in V2, 5 in V3)
- 3 finale assemblages
- ~20 hero frames

## Pass Rate Per Tier

| Tier | Pass | Fail | Rate |
|------|------|------|------|
| TIER 1 (Technical) | 5/11 | 6/11 | 45% |
| TIER 2 (Visual Quality ≥3.5) | 3/11 | 8/11 | 27% |
| TIER 3 (Brand Compliance ≥4.0) | 1/11 | 10/11 | 9% |
| TIER 4 (Ad Effectiveness ≥3.5) | 1/11 | 10/11 | 9% |
| **ALLE TIERS** | **1/11** | **10/11** | **9%** |

Enige clip die alle tiers haalt: **A3-S4 (Box Detail Close-up)** — een statisch product-shot zonder mensen.

## Root Cause Distributie

| Categorie | Aantal | % | Clips |
|-----------|--------|---|-------|
| OPERATOR FAILURE | 5 | 45% | A1-S1, A1-S2, A1-S4, A2-S1, A3-S2 |
| DISCIPLINE FAILURE | 3 | 27% | A2-S2, A3-S3, Finals |
| MODEL CEILING | 2 | 18% | A3-S1, A3-S5 |
| SKILL/PROCEDURE | 1 | 9% | A1-S3 |

## Cost Metric
- Approved videos: **0**
- Total credits gespendeerd: **~$25-30**
- Credits per approved video: **WISKUNDIG ONGEDEFINIEERD (denominator is 0)**

## Ceiling Alert
Kling v3 kan complexe tekst NIET behouden over 5 seconden animatie. Dit is een bewezen ceiling.
**Workarounds:** (1) Tekst als overlay compositen na animatie, (2) Camera-hoek kiezen waarbij tekst niet prominent is, (3) Clips korter houden (3s ipv 5s).

## Workflow Gaps

| Gate | Bestond? | Toegepast? |
|------|----------|------------|
| Brief validatie | Ja | Ja |
| Prompt quality review | Nee | Nee |
| 3-5 varianten per shot | Nee (altijd 1) | N/A |
| I2V (niet T2V) | Ja | Ja |
| First-pass visual review | Gedeeltelijk (stills ja, video nee) | Nee voor video |
| Frame-by-frame assessment | Nee | Nee |
| Brand compliance gate | Nee (als apart gate) | Nee |
| Three-agent Evaluator | Nee | Nee |
| Gestructureerde owner feedback | Ja | Ja |

## Kan Output 80%+ Approval Rate Bereiken?
**JA, met confidence 65%** — mits:
1. Three-agent Evaluator geïmplementeerd
2. Elke clip individueel beoordeeld voor assembly
3. Native 9:16 (bewezen werkend)
4. Tekst-overlay compositing voor brand text (ceiling workaround)
5. Minimal motion prompts met endpoints

82% van failures is FIXBAAR. 18% is ceiling met viable workarounds.

## Top 3 Veranderingen
1. **Hard-gate frame extraction + visual review na ELKE clip** — vangt 7/10 failures
2. **Native 9:16 afdwingen** — elimineert V1 black bar ramp (4 clips)
3. **Tekst als overlay compositen na animatie** — omzeilt Kling v3 text ceiling

---

# GECOMBINEERD VERDICT

**Status:** Pre-operationeel met bewezen architectuur.

**Primaire failure mode:** De operator (ik) beoordeelt eigen werk niet kritisch genoeg en past opgeslagen feedback niet consequent toe.

**82% van alle failures is fixbaar** door betere executie. 18% is model ceiling met bewezen workarounds.

**Drie blokkades moeten weg:**
1. ❌ Three-agent pattern (Planner/Generator/Evaluator)
2. ❌ Snorkel AI triage (zero loops routine, 3-5 loops creatief)
3. ❌ Hindsight stabiel (auto-recall, auto-retain)

**Na implementatie blokkades + eerste 5 goedgekeurde video's → operationeel.**

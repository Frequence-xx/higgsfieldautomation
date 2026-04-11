# Audit Prompts — Herbruikbaar bij elke audit cyclus

Drie audits die samen de pipeline-gezondheid meten. Draai alle drie na elke significante wijziging. Target: operator ≥4.0/5.0, skills ≥95%, creative ≥70% predicted pass rate.

---

## AUDIT 1: AI OPERATOR PERFORMANCE

Scoor op 6 dimensies (1-5) met bewijs uit logs, database, Hindsight, commits:

1. **REASONING** — Multi-step planning. Worden creatieve keuzes onderbouwd? Worden alternatieven overwogen? Is three-agent pattern actief?
2. **EXECUTION** — Tool selection accuracy. Zijn production gates mandatory? Is pre-generation hook actief? Zijn approval gates aanwezig?
3. **MEMORY** — Wordt Hindsight VOOR beslissingen bevraagd? Lesson application rate >50%? Zijn banks gevuld?
4. **RELIABILITY** — pass^k consistency. Welke beslissingen waren stabiel, welke varieerden? Zijn alle V1-V3 failure modes structureel geadresseerd?
5. **INTEGRATION** — API parameters gedocumenteerd? Model strings correct? InsightFace beschikbaar? Hindsight API functioneel?
6. **SOCIAL** — Heldere Telegram communicatie, escalatie van onzekerheid, anti-sycophancy, flag issues first.

Gewogen gemiddelde: Reasoning 20%, Execution 20%, Memory 15%, Reliability 20%, Integration 15%, Social 10%.

Four-category failure classification voor elke faal:
- ARCHITECTURAL — structurele grens ontbreekt
- OPERATIONAL — slechte of ontbrekende SOPs
- DISCIPLINE — agent had alles maar gebruikte het niet
- MODEL CAPABILITY CEILING — model kan dit niet bij elke prompt

Eindig met: OPERATOR_AUDIT_COMPLETE

---

## AUDIT 2: SKILL LIBRARY & POLICY

Per skill (alle bestanden in /opt/pipeline/skills/), scoor op 8 criteria:

1. **DESCRIPTION** — Heeft ZOWEL positieve ALS negatieve trigger condities?
2. **STEM** — Imperatief ("Run", "Generate") of passief ("can be executed")? Passief = finding.
3. **EXPLICIETE DEFAULTS** — Wat als gebruiker iets niet specificeert?
4. **RFC 2119** — MUST/SHOULD/MAY voor kritieke regels?
5. **APPROVAL GATES** — Expliciete bevestiging voor dure/destructieve acties?
6. **LENGTE** — Body onder 5000 woorden?
7. **NEGATIEVE TRIGGERS** — negatives: veld in YAML frontmatter?
8. **CONSISTENTIE** — Geen contradicties met CLAUDE.md?

CLAUDE.md audit:
- Instructie count vs 150 limiet
- Three-agent pattern aanwezig?
- Snorkel triage aanwezig?
- Model routing matrix aanwezig?
- Brand binary checklist aanwezig?
- Production gates aanwezig?

Hindsight status: daemon actief? Banks gevuld? Recall functioneel?

Gap analysis: welke procedures ontbreken?

Bereken: (totaal passes / totaal mogelijk) = percentage. Target: ≥95%.

Eindig met: SKILL_AUDIT_COMPLETE

---

## AUDIT 3: CREATIVE OUTPUT QUALITY

Voor elke clip in output, scoor tegen vier-tier rubric:

**TIER 1 — TECHNISCH (binary pass/fail)**
- Resolutie ≥1080p, frame rate 24-30fps, correcte duur en aspect ratio, geen corruptie, tekst leesbaar, geen watermerken

**TIER 2 — VISUELE KWALITEIT (1-5, gemiddelde ≥3.5)**
- Imaging quality, subject consistency, background consistency, temporal flickering, motion smoothness, physics plausibility, human anatomy, aesthetic quality, cinematic quality

**TIER 3 — BRAND COMPLIANCE (1-5, vereist ≥4.0)**
- Snelverhuizen oranje #FC8434, logo integriteit, truck branding vs reference, crew uniform, tone, Shari'ah compliance

**TIER 4 — ADVERTISING EFFECTIVENESS (1-5, vereist ≥3.5)**
- Hook sterkte, boodschap helderheid, CTA, doelgroep fit, trust/authenticiteit

Per afgekeurde clip: root cause in EXACT ÉÉN categorie (operator / skill / discipline / ceiling).

Cost metric: credits per APPROVED video (als 0 approved: WISKUNDIG ONGEDEFINIEERD).

Workflow gaps: welke gates bestonden vs ontbraken.

Voorspelde pass rate bij correcte uitvoering + confidence %.

Eindig met: CREATIVE_AUDIT_COMPLETE

---

## WANNEER DRAAIEN

- Na elke Phase implementatie (1-5)
- Voor elke productie-start (Phase 6)
- Na elke owner rejection
- Bij significante skill of CLAUDE.md wijzigingen
- Minimaal 1x per week tijdens actieve productie

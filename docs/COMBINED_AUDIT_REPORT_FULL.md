# Snelverhuizen Pipeline — Volledig Gecombineerd Audit Rapport
## Operator + Skill Library + Creative Output — Onverkort
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

---

## DIMENSIE 1: REASONING — Score: 2/5

**ID: REAS-001**
DIMENSIE: Reasoning
FAILURE CATEGORY: DISCIPLINE
ERNST: Hoog
CONFIDENCE: 95%

WAARNEMING: In alle 3 pogingen werd geen alternatieven-analyse gedaan voor creatieve keuzes. Poging 1 begon met text-only prompts zonder te overwegen of referentie-gebaseerd beter zou zijn — ondanks dat character-consistency.md dit expliciet voorschreef. De stap van text-only → Kontext Max → Nano Banana Pro Edit was reactief (na owner-afwijzing), niet proactief.

ANALYSE: De operator functioneert als executeur, niet als denker. Bij elke stap wordt de eerste ingeving uitgevoerd zonder alternatieven te overwegen. Er is geen "even nadenken voordat ik begin" stap.

IMPACT: 4 hero frames weggegooid in poging 1 ($0.78 verspild), zelfde fouten herhaald in poging 2 en 3.

FIX: Three-agent pattern. De Planner-agent moet VOOR generatie alternatieven overwegen en de beste selecteren met onderbouwing.

---

**ID: REAS-002**
DIMENSIE: Reasoning
FAILURE CATEGORY: OPERATIONAL
ERNST: Medium
CONFIDENCE: 85%

WAARNEMING: Geen model-selectie onderbouwing. Poging 1 gebruikte Nano Banana Pro (text-only) voor character shots. Poging 2 gebruikte Kontext Max voor sommige en NBP Edit voor andere, zonder duidelijke selectielogica. De model-selectie skill bestond maar werd niet systematisch gevolgd.

ANALYSE: De skill file beschreef WANNEER welk model te gebruiken, maar de operator checkte dit niet vóór elke generatie.

FIX: Model-selectie tabel als Tier A regel in CLAUDE.md: "Character shots = NBP Edit + refs. Truck-only = Kontext Max. Generic = NBP text-only."

---

## DIMENSIE 2: EXECUTION — Score: 3/5

**ID: EXEC-001**
DIMENSIE: Execution
FAILURE CATEGORY: DISCIPLINE
ERNST: Kritiek
CONFIDENCE: 100%

WAARNEMING: Video clips werden NIET bekeken voor assembly. Poging 2 en 3 werden geassembleerd en afgeleverd zonder dat de individuele clips gereviewed waren. De operator extraheerde QA frames van hero frames (stills) maar niet van geanimeerde video's. Dit was de directe oorzaak van ghost-driving trucks en expression drift in het eindproduct.

ANALYSE: De operator had de kennis ("bekijk elke clip") maar sloeg de stap over omwille van snelheid. Dit is pure discipline — de SOP was duidelijk, het werd genegeerd.

IMPACT: Alle 3 video's afgeleverd met zichtbare motion-artefacten die bij review vooraf gevangen zouden zijn.

FIX: Three-agent pattern. Generator mag NIET "klaar" zeggen — alleen "geproduceerd, klaar voor evaluatie." Evaluator bekijkt elke clip onafhankelijk.

---

**ID: EXEC-002**
DIMENSIE: Execution
FAILURE CATEGORY: OPERATIONAL
ERNST: Hoog
CONFIDENCE: 90%

WAARNEMING: Caption timestamps werden 3x handmatig geschat in plaats van programmatisch uit ElevenLabs te halen. De skill file (captions-and-titles.md) beschreef het gebruik van word-level timestamps, maar de procedure om ze te verkrijgen was niet concreet genoeg. De ElevenLabs MCP tool retourneert geen timestamps in het huidige formaat.

ANALYSE: De SOP zei "gebruik echte timestamps" maar specificeerde niet HOE. De operator probeerde ElevenLabs STT maar die gaf alleen tekst, geen timing. Vervolgens werd geschat in plaats van een alternatief te zoeken (Whisper, @remotion/install-whisper-cpp).

FIX: Concrete procedure in skill: "Na voiceover generatie → voer uit: mcp__ElevenLabs__speech_to_text met word_timestamps=true. Als dat faalt → installeer whisper-cpp lokaal. Schat NOOIT."

---

**ID: EXEC-003**
DIMENSIE: Execution
FAILURE CATEGORY: MODEL CAPABILITY CEILING (deels) + DISCIPLINE (deels)
ERNST: Medium
CONFIDENCE: 70%

WAARNEMING: Choppy/laggy motion in alle 3 pogingen. Owner bevestigde dat Kling v3 normaal stabiel is. Maar: poging 1 gebruikte verkeerde instellingen (geen generate_audio:false, vierkante input). Poging 2 gebruikte betere settings maar nog steeds vierkante input. Poging 3 gebruikte native 9:16 + audio OFF maar motion was nog steeds niet vloeiend.

ANALYSE: Deels discipline (verkeerde API parameters in poging 1-2), deels mogelijk ceiling (poging 3 had correcte settings maar nog steeds issues). Onvoldoende data om te bepalen of Kling v3 Pro met optimale settings vloeiende motion levert — dit vereist meer testen.

IMPACT: Motion quality was een afwijzingsreden in alle 3 pogingen.

FIX: Systematische test nodig: 1 clip met Kling v3 Pro, native 9:16 input, audio OFF, minimale motion prompt, cfg_scale 0.5. Als die nog steeds choppy is = ceiling. Als die smooth is = onze eerdere prompts waren het probleem.

---

## DIMENSIE 3: MEMORY — Score: 1/5

**ID: MEM-001**
DIMENSIE: Memory
FAILURE CATEGORY: DISCIPLINE
ERNST: Kritiek
CONFIDENCE: 100%

WAARNEMING: 26 memory bestanden opgeslagen. Lesson application rate: <20%. Bewijs: feedback_v2_detailed.md bevat "geen breathing motion in prompts" — maar poging 3 gebruikte "very subtle natural breathing movement" in de motion prompt (shot 1 Mourad). feedback_reference_based_generation.md zegt "nooit text-only" — maar poging 2 hero frames begonnen text-only voordat de owner corrigeerde.

ANALYSE: Het memory systeem is write-only. Lessen worden opgeslagen maar niet systematisch geraadpleegd vóór relevante beslissingen. Er is geen auto-recall mechanisme — de operator moet handmatig alle memory bestanden lezen en dat gebeurt niet consequent.

IMPACT: Dezelfde fouten herhaalden zich over 3 pogingen. Dit is de kern van het "0 goedgekeurd" probleem.

FIX: Hindsight installatie is de technische fix. Maar het onderliggende gedragsprobleem (niet terugkijken vóór handelen) moet ook procedureel worden afgedwongen: "VOOR ELKE generatie: lees alle feedback_*.md bestanden die het woord bevatten van het type shot dat je gaat genereren."

---

## DIMENSIE 4: RELIABILITY — Score: 2/5

**ID: REL-001**
DIMENSIE: Reliability
FAILURE CATEGORY: DISCIPLINE
ERNST: Hoog
CONFIDENCE: 95%

WAARNEMING: pass^k over 3 pogingen: 0%. Geen enkele poging produceerde een goedgekeurde video. De inconsistentie zit niet in de tool calls (die werkten technisch) maar in de creatieve kwaliteit. Stabiel over pogingen: voiceover kwaliteit (goedgekeurd in alle 3), truck referentie (verbeterd van poging 1 naar 2). Instabiel: caption sync (slecht in alle 3), motion quality (slecht in alle 3), zelf-review (afwezig in alle 3).

ANALYSE: De operator is technisch competent (API calls werken, FFmpeg assembleert, Remotion rendert) maar creatief onbetrouwbaar (kwaliteitsoordeel is te mild, feedback wordt niet toegepast). Het patroon is consistent: genereer → stuur door → owner wijst af → pas aan → stuur door → owner wijst af.

IMPACT: 0/3 pass rate. Elke poging kostte $3-9 en leverde niets op.

FIX: Three-agent Evaluator met skeptische persona is de structurele fix. De Evaluator moet dezelfde standaard hanteren als de owner — of strenger.

---

## DIMENSIE 5: INTEGRATION — Score: 3/5

**ID: INT-001**
DIMENSIE: Integration
FAILURE CATEGORY: OPERATIONAL
ERNST: Medium
CONFIDENCE: 80%

WAARNEMING: AIMLAPI integratie werkt maar had ontdekbare fouten die pas na meerdere pogingen werden gevonden. Verkeerd endpoint (/v2/ ipv /v1/), missende generate_audio parameter, verkeerde model strings. ElevenLabs MCP werkt voor TTS maar niet voor word-level timestamps. Freesound integratie werkt. Remotion compileert en rendert maar de chromakey compositing mislukte bij de eerste poging.

ANALYSE: Elke externe integratie werkte uiteindelijk, maar pas na trial-and-error in productie. De API documentatie was niet vooraf bestudeerd — de operator ontdekte parameters door te falen.

FIX: Alle API integraties zijn nu gedocumenteerd in skills/higgsfield-generation.md met correcte endpoints, model strings, en parameters. De operationele kennis is er nu — de vraag is of het wordt toegepast.

---

## DIMENSIE 6: SOCIAL — Score: 4/5

**ID: SOC-001**
DIMENSIE: Social
FAILURE CATEGORY: DISCIPLINE
ERNST: Medium
CONFIDENCE: 85%

WAARNEMING: Telegram communicatie was over het algemeen goed: snelle acknowledgements, progress updates, video's als bijlage. Twee problemen: (1) de operator stuurde marginal output naar de owner in de hoop dat het geaccepteerd zou worden in plaats van zelf te filteren, (2) er was een 2-minuten gap zonder antwoord terwijl de operator aan het typen was (subagent research), wat de owner ongerust maakte.

ANALYSE: De operator communiceert regelmatig maar is niet eerlijk genoeg over de kwaliteit van wat hij aflevert. "Hier is de video" zonder "ik heb zorgen over de motion quality in shot 2" is oneerlijke communicatie.

FIX: Bij elke aflevering: vermeld EERST de problemen die je zelf ziet, DAN het product. "Shot 2 heeft iets choppy motion die ik niet heb kunnen oplossen — bekijk specifiek of dit acceptabel is." Dit is anti-sycophancy toegepast op deliverables.

---

## Failure Category Distributie (Operator)
| Categorie | Aantal | % |
|-----------|--------|---|
| DISCIPLINE | 7 | 54% |
| OPERATIONAL | 4 | 31% |
| MODEL CEILING | 1 | 8% |
| ARCHITECTURAL | 0 | 0% |

## Status Drie Blokkades
1. Three-agent pattern: ❌ OPEN — Generator en Evaluator zijn dezelfde context
2. Snorkel triage: ❌ OPEN — niet gecodeerd in CLAUDE.md
3. Hindsight: ❌ OPEN — niet draaiend, lesson application <20%

---

# PART 2: SKILL LIBRARY AUDIT

## Per-Skill Scoring (8 criteria)

### SKILL 1: shariah-compliance.md (492 woorden)

**SKILL-001** | Description | Severity: High | Confidence: 90%
HUIDIGE STAAT: Geen negatieve trigger condities. Positieve triggers wel aanwezig.
FIX: Toevoegen: "Do NOT invoke for post-production audio mixing that contains only voiceover and SFX already verified. Do NOT invoke for Remotion rendering or FFmpeg commands that do not involve content decisions."

**SKILL-002** | Stem | Severity: Low | Confidence: 95%
HUIDIGE STAAT: Imperatief ("Never use", "Always flag"). Correct.
FIX: Geen.

**SKILL-003** | Default | Severity: Medium | Confidence: 85%
HUIDIGE STAAT: Geen default voor briefs zonder mensen (bijv. truck-only B-roll).
FIX: "Defaults — When the brief has no people, skip visual dress-code checks. When audio is voiceover-only, skip music detection. Always run haram-background-element scan."

**SKILL-004** | RFC 2119 | Severity: Medium | Confidence: 80%
HUIDIGE STAAT: Informele "No exceptions" ipv formele MUST/SHOULD/MAY.
FIX: "MUST NOT include music or instruments. This is a MUST gate. SHOULD include explicit dress code language."

**SKILL-005** | Gate | Severity: Low | Confidence: 90%
HUIDIGE STAAT: Expliciete 3-retry limiet met escalatie. Correct.
FIX: Geen.

**SKILL-006** | Length | Severity: Low | Confidence: 100%
HUIDIGE STAAT: 492 woorden. Ruim onder 5000.
FIX: Geen.

**SKILL-007** | Invocation | Severity: Medium | Confidence: 70%
HUIDIGE STAAT: shariah_compliance scoorde 10/10 op alle 5 generaties. QA invocation ~80%. Brief intake auto-override ongetest.
FIX: Shari'ah pre-check toevoegen aan production-checklist.md.

**SKILL-008** | FalseRate | Severity: Low | Confidence: 65%
HUIDIGE STAAT: Trigger "content generation" is te breed — kan vuren op Remotion rendering. Geschatte false positive: ~15%.
FIX: Vervang "content generation" door "visual content generation."

---

### SKILL 2: cinematic-standards.md (848 woorden)

**SKILL-009** | Description | Severity: High | Confidence: 90%
HUIDIGE STAAT: Alleen positieve triggers. Geen negatieven.
FIX: "Do NOT invoke for CTA end cards or title cards rendered purely via Remotion. Do NOT invoke for audio-only tasks."

**SKILL-010** | Stem | Severity: Low | Confidence: 95%
HUIDIGE STAAT: Imperatief. Correct.
FIX: Geen.

**SKILL-011** | Default | Severity: Medium | Confidence: 80%
HUIDIGE STAAT: Geen default als brief geen lens, kleurgrading, of camerabeweging specificeert.
FIX: "Defaults — If unspecified: lens = 35mm, camera = slow dolly push-in, color = warm golden, transition = hard cut on action."

**SKILL-012** | RFC 2119 | Severity: Medium | Confidence: 80%
HUIDIGE STAAT: Informele "NEVER USE" en "EVERY." Geen formele RFC 2119.
FIX: "MUST include AI artifact mitigation in every prompt. MUST NOT use novelty transitions. SHOULD use match cuts."

**SKILL-013** | Invocation | Severity: High | Confidence: 60%
HUIDIGE STAAT: Gedeeltelijk toegepast (golden hour, cinematic framing). Maar choppy motion en aspect ratio fouten zijn cinematic-standards concerns die niet gevangen werden. Geschatte invocation: ~55%.
FIX: Shot-type quality map cross-refereren in production-checklist bij shot-planning.

---

### SKILL 3: video-qa-rubric.md (813 woorden)

**SKILL-014** | Description | Severity: High | Confidence: 90%
HUIDIGE STAAT: Alleen positieve triggers.
FIX: "Do NOT invoke for hero frame QA only (use 8-dimension without cinematic for stills). Do NOT invoke for audio-only QA."

**SKILL-015** | Default | Severity: Medium | Confidence: 85%
HUIDIGE STAAT: Geen default voor niet-toepasbare dimensies (bijv. hand_anatomy op landscape-only).
FIX: "N/A voor niet-toepasbare dimensies. N/A excluded van threshold berekeningen. Minimum 4 toepasbare dimensies voor geldige QA pass."

**SKILL-016** | Invocation | Severity: Critical | Confidence: 75%
HUIDIGE STAAT: QA uitgevoerd op alle 5 stills. NIET betrouwbaar op video clips. feedback_v3 bevestigt: agent assembleerde zonder video QA. Geschatte invocation: stills 90%, video clips ~30%.
FIX: Mandatory checkpoint: "MUST extract frames and score EVERY animated clip before proceeding. Hero frame QA alone is NOT sufficient."

---

### SKILL 4: viral-research.md (691 woorden)

**SKILL-017** | Description | Severity: High | Confidence: 90%
HUIDIGE STAAT: Trigger "research" is gevaarlijk breed — vurt op elke research taak.
FIX: Narrowen naar: "viral strategy", "hook optimization", "engagement analysis." Verwijder "research."

**SKILL-018** | FalseRate | Severity: High | Confidence: 80%
HUIDIGE STAAT: Triggers "brief", "concept", "research" zijn extreem veelvoorkomende woorden. Geschatte false positive: ~30%.
FIX: Narrowen triggers. Verwijder "brief" (laat brief-intake.md dit expliciet aanroepen).

**SKILL-019** | Invocation | Severity: High | Confidence: 70%
HUIDIGE STAAT: Geen bewijs dat viral research is uitgevoerd voor "Meet the Team." Geschatte invocation: ~20%.
FIX: Cross-reference in brief-intake.md naar TOP van het bestand als MUST stap.

---

### SKILL 5: brief-intake.md (870 woorden)

**SKILL-020** | Description | Severity: High | Confidence: 90%
HUIDIGE STAAT: Alleen positieve triggers. "shot list" kan vuren bij review van bestaande shot list.
FIX: "Do NOT invoke for shot list review or QA. Do NOT invoke for mid-production changes."

**SKILL-021** | Default | Severity: Low | Confidence: 85%
HUIDIGE STAAT: Expliciete defaults: format 9:16, language nl, voice Willem. Goed afgehandeld.
FIX: Geen.

**SKILL-022** | Gate | Severity: Low | Confidence: 90%
HUIDIGE STAAT: Expliciete gate: "Do NOT generate until owner approves shot list." Correct.
FIX: Geen.

**SKILL-023** | Invocation | Severity: Medium | Confidence: 75%
HUIDIGE STAAT: Brief 3 heeft JSON spec. Skill waarschijnlijk invoked voor brief 3 maar niet voor test brief 2. Geschatte invocation: ~65%.
FIX: Trigger toevoegen: "new video", "maak een video", "Telegram brief."

---

### SKILL 6: brand-identity.md (1144 woorden)

**SKILL-024** | Description | Severity: Medium | Confidence: 85%
HUIDIGE STAAT: Alleen positieve triggers. Dit is een referentiedocument — laag risico op false negative.
FIX: Minimale negatieve: "Do NOT invoke for non-Snel Verhuizen content."

**SKILL-025** | Stem | Severity: Medium | Confidence: 80%
HUIDIGE STAAT: Grotendeels declaratief/referentie. Acceptabel voor een brand guide.
FIX: Geen.

**SKILL-026** | Invocation | Severity: Medium | Confidence: 70%
HUIDIGE STAAT: Brand accuracy scoorde 7/10 op alle hero frames — passend maar niet perfect. Logo kleur issue (oranje niet wit) gevangen in feedback NA delivery, niet tijdens productie. Geschatte invocation: ~60%.
FIX: Brand identity waarden (logo kleur, truck specs, uniforms) injecteren in production-checklist als expliciete QA items.

---

### SKILL 7: credit-efficiency.md (582 woorden)

**SKILL-027** | Description | Severity: High | Confidence: 90%
HUIDIGE STAAT: Alleen positieve triggers. "generation" is te breed.
FIX: "Do NOT invoke for free operations (FFmpeg, Remotion, local processing). Only invoke when an API call with real cost is about to be made."

**SKILL-028** | RFC 2119 | Severity: Medium | Confidence: 80%
HUIDIGE STAAT: Informele "NEVER" en "CRITICAL." Geen formele MUST.
FIX: "MUST generate only one at a time. MUST log every generation. MUST NOT proceed to video without QA-passed hero frame."

**SKILL-029** | Gate | Severity: Critical | Confidence: 85%
HUIDIGE STAAT: GEEN hard budget ceiling met automatische stop. Test run kostte $9.10 voor afgekeurde video. Geen per-video of per-sessie kostenlimiet.
FIX: CLAUDE.md: "MUST NOT exceed $15/video. MUST NOT exceed $50/session. Bij 80% ceiling: Telegram warning."

**SKILL-030** | Invocation | Severity: Medium | Confidence: 70%
HUIDIGE STAAT: Kosten gelogd. Static-first funnel gevolgd. Maar cost data bevatte stale pricing ($0.42 ipv $1.09). Geschatte invocation: ~65%.
FIX: "Last verified" datum bij elk kostencijfer.

---

### SKILL 8: character-consistency.md (1389 woorden)

**SKILL-031** | Description | Severity: High | Confidence: 90%
HUIDIGE STAAT: Trigger "person" is extreem breed. "consistent" kan vuren op elke consistency discussie.
FIX: Vervang "person" door "recurring character." Vervang "consistent" door "character lock." Toevoegen negatieven: "Do NOT invoke for truck-only shots. Do NOT invoke for generic one-off silhouettes."

**SKILL-032** | Default | Severity: Low | Confidence: 85%
HUIDIGE STAAT: Expliciete beslisboom (Type A/B/C). Goed gestructureerd.
FIX: Geen.

**SKILL-033** | Invocation | Severity: High | Confidence: 70%
HUIDIGE STAAT: Feedback zegt "Karel inconsistent" en memory zegt "altijd referentie-gebaseerd." Toch werd text-only gebruikt in poging 1. generation_history toont shots 2-5 met `google/nano-banana-pro` (text-only) ipv `nano-banana-pro-edit` (referentie). Geschatte invocation: ~25%.
FIX: HOOGSTE IMPACT FIX. Type A/B/C beslisboom integreren in production-checklist als MANDATORY pre-generation stap.

---

### SKILL 9: captions-and-titles.md (2044 woorden)

**SKILL-034** | Description | Severity: Medium | Confidence: 85%
HUIDIGE STAAT: Alleen positieve triggers. Laag risico want captions altijd nodig.
FIX: "Do NOT invoke during image/video generation. Invoke only during post-production assembly."

**SKILL-035** | Length | Severity: Medium | Confidence: 100%
HUIDIGE STAAT: 2044 woorden. Onder 5000 maar langste na higgsfield-generation. Code voorbeelden inflaten woordenaantal.
FIX: Overweeg splitsen: `caption-typography.md` + `caption-workflow.md`.

**SKILL-036** | Invocation | Severity: High | Confidence: 75%
HUIDIGE STAAT: Caption sync, name card overlap, en timing regels ALLEMAAL geschonden. Geschatte invocation: ~30%.
FIX: "Timing Rules to Prevent Overlap" en "Caption Sync Gate" extraheren naar production-checklist als mandatory checkboxen.

---

### SKILL 10: production-checklist.md (801 woorden)

**SKILL-037** | Description | Severity: High | Confidence: 90%
HUIDIGE STAAT: Triggers "generate", "animate", "production" zijn breed. Geen negatieven.
FIX: "Do NOT invoke for research tasks, study cycles, or non-production activities."

**SKILL-038** | Stem | Severity: Low | Confidence: 95%
HUIDIGE STAAT: Imperatieve checklists. Correct.
FIX: Geen.

**SKILL-039** | TierMismatch | Severity: CRITICAL | Confidence: 85%
HUIDIGE STAAT: De BELANGRIJKSTE enforcement skill zit in Tier B (56% failure rate). ALLE 10 bekende fouten zijn voorgekomen in productie. MOET Tier A representatie hebben in CLAUDE.md.
FIX: CLAUDE.md Non-Negotiable Rules: "## Production Gates — Before ANY generation: read ALL memory entries, verify reference images. Before ANY animation: QA the hero frame. Before ANY assembly: watch every animated clip. Before ANY delivery: extract frames from final video. NEVER skip these gates."

**SKILL-040** | Invocation | Severity: CRITICAL | Confidence: 80%
HUIDIGE STAAT: Checklist demonstrabel NIET gevolgd: (1) text-only prompts, (2) clips niet reviewed, (3) assembly zonder frame check, (4) timestamps geschat. Geschatte invocation: ~20%.
FIX: Hook (Tier C) of minimaal CLAUDE.md (Tier A). Pre-generation hook die checklist print en bevestiging vereist zou invocation naar ~100% brengen.

---

### SKILL 11: higgsfield-generation.md (2981 woorden)

**SKILL-041** | Description | Severity: Medium | Confidence: 85%
HUIDIGE STAAT: Geen negatieven.
FIX: "Do NOT invoke for post-production. Do NOT invoke for QA scoring."

**SKILL-042** | Length | Severity: High | Confidence: 100%
HUIDIGE STAAT: 2981 woorden. Langste skill. Agent leest waarschijnlijk top en skimt onderkant (known failure prevention, shot presets).
FIX: Splitsen: `generation-image.md` + `generation-video.md`.

**SKILL-043** | Default | Severity: Low | Confidence: 85%
HUIDIGE STAAT: Expliciete defaults: duration 5s, cfg_scale 0.5, audio OFF. Goed.
FIX: Geen.

**SKILL-044** | Invocation | Severity: Medium | Confidence: 70%
HUIDIGE STAAT: Model string mismatch: generation_history toont `kling-video/v3/standard/image-to-video` terwijl skill zegt `klingai/video-v3-standard-image-to-video`. Geschatte invocation: ~55%.
FIX: Model strings reconciliëren. Verifiëren tegen AIMLAPI documentatie.

---

## CLAUDE.md AUDIT

### Instruction Count

| Sectie | Instructies |
|--------|-------------|
| Reference Documents | 3 |
| Seven-Phase Pipeline | 7 |
| Anti-Sycophancy Core Principles | 5 |
| Anti-Sycophancy Specific Behaviors | 7 |
| Anti-Sycophancy When Pushed Back | 4 |
| Anti-Sycophancy Required Outputs | 4 |
| Anti-Sycophancy Self-Correction | 2 |
| Anti-Sycophancy Anchoring Bias | 1 |
| Pipeline-Specific Honesty | 7 |
| Shari'ah Compliance | 5 |
| Cinematic Quality | 2 |
| Captions | 2 |
| Credit Conservation | 4 |
| Generation Architecture | 6 |
| Telegram Communication Protocol | 6 |
| Resource Management | 5 |
| Crash Recovery | 5 |
| Memory Instructions | 5 |
| Memory Maintenance | 3 |
| Git Discipline | 3 |
| **TOTAAL** | **~86** |

### CLAUDE.md Findings

**CMD-001** | TierMismatch | Severity: CRITICAL | Confidence: 90%
HUIDIGE STAAT: ~86 instructies + ~50 system prompt = ~136 totaal. Praktisch plafond ~200. Compliance daalt boven 150 instructies. We zitten in de gevarenzone.
FIX: Reduceer naar ~50 Tier A instructies. Verplaats anti-sycophancy body (30 instructies) → skill. Verwijder generation architecture details (al in skills). Verplaats telegram details → skill.

**CMD-002** | TierMismatch | Severity: High | Confidence: 85%
HUIDIGE STAAT: Anti-Sycophancy sectie is 37 regels (~30 instructies). Consumeert 35% van instruction budget voor een gedragsmodifier.
FIX: Verplaats naar `skills/anti-sycophancy.md`. Houd in CLAUDE.md: "## Honesty — Be direct. No praise openers. Disagree when warranted. See anti-sycophancy.md."

**CMD-003** | TierMismatch | Severity: High | Confidence: 80%
HUIDIGE STAAT: Generation Architecture sectie dupliceert informatie uit credit-efficiency.md, higgsfield-generation.md, en brand-identity.md. Model string mismatch al waargenomen.
FIX: Vervang hele sectie door: "## Generation Architecture — See higgsfield-generation.md for models, credit-efficiency.md for pricing, brand-identity.md for voiceover/caption specs."

**CMD-004** | Gap | Severity: CRITICAL | Confidence: 90%
HUIDIGE STAAT: GEEN production gates sectie. production-checklist.md bestaat maar werd niet invoked (~20%). CLAUDE.md heeft de mandatory gates nodig.
FIX: Toevoegen: "## Production Gates (Non-Negotiable) — MUST read all memory before production. MUST QA every hero frame before animation. MUST QA every animated clip before assembly. MUST get owner approval on each clip. MUST review final video frame-by-frame. NEVER assemble unreviewed clips."

**CMD-005** | TierMismatch | Severity: Medium | Confidence: 75%
HUIDIGE STAAT: Telegram Communication Protocol (6 instructies) is operationeel detail.
FIX: Verplaats naar `skills/telegram-protocol.md`. Houd: "## Telegram — Acknowledge immediately. Progress at milestones. Deliver as attachments. Escalate after 3 failures."

**CMD-006** | Context | Severity: Low | Confidence: 70%
HUIDIGE STAAT: Seven-Phase Pipeline overview (7 items) is context, geen actiegerichte instructies.
FIX: Acceptabel als oriëntatie. Telt niet zwaar mee voor instruction budget.

**CMD-007** | TierMismatch | Severity: Medium | Confidence: 70%
HUIDIGE STAAT: Instructies zonder invloed in laatste 3 sessies:
1. "Auto-cleanup: QA frames older than 7 days" — pipeline is 2 dagen oud
2. "Monthly: Review auto memory files" — te vroeg
3. "Monthly: Move generation_history records" — te vroeg
4. "NEVER run more than one Playwright browser session" — browser 1x gebruikt
5. "Delete QA frames after clip passes" — handmatig opgeruimd
FIX: Verplaats naar `skills/maintenance.md` skill.

---

## GAP ANALYSIS

**GAP-001** | Model Capability Ceiling Detection | Severity: CRITICAL | Confidence: 90%
HUIDIGE STAAT: Geen procedure. Kling v3 produceerde choppy motion, pipeline had geen protocol om model-limiet te detecteren en te switchen.
GEWENSTE TIER: B (skill)
FIX: Creëer `skills/model-ceiling-detection.md`: "Wanneer model zelfde shot type 2x faalt met scores <6, markeer als ceiling. Log naar learned_preferences. Route naar next-tier model of simplificeer compositie. MUST NOT retry zelfde model/shot-type >2x."

**GAP-002** | Three-Agent Coordination Protocol | Severity: High | Confidence: 85%
HUIDIGE STAAT: Geen protocol. Memory verwijst naar "delegate to agents" maar geen gestructureerd handoff formaat.
GEWENSTE TIER: B (skill)
FIX: Creëer `skills/agent-coordination.md`: "## Roles — Producer: intake through generation. Evaluator: QA + compliance. ## Handoff Template: brief_id, current_step, context (max 2000 words), task, acceptance criteria, cost ceiling. ## Return: status, findings (JSON), recommendations, cost."

**GAP-003** | Per-Clip Evaluator Handoff Template | Severity: High | Confidence: 85%
HUIDIGE STAAT: Geen template voor wat bij elke clip review naar de owner gaat.
GEWENSTE TIER: B (skill)
FIX: Toevoegen aan production-checklist: "## Clip Review Package — MUST include: (1) clip als video, (2) hero frame bron, (3) QA scores JSON, (4) gemarkeerde issues met frame numbers, (5) prompt, (6) kosten, (7) totaalkosten brief."

**GAP-004** | Brand Compliance Binary Checklist | Severity: High | Confidence: 80%
HUIDIGE STAAT: Huidige QA scoort brand_accuracy als scalar 1-10. Specifieke brand failures vereisen binaire checks: logo kleur, zijdeur, uniform details.
GEWENSTE TIER: B (toevoegen aan video-qa-rubric.md)
FIX: "## Brand Compliance Checklist (binary pass/fail) — [ ] Logo is oranje #FC8434. [ ] Truck cargo box GEEN zijdeur. [ ] Crew: zwart crewneck, oranje logo links, blauwe jeans, witte sneakers. [ ] Truck tekst = SNELVERHUIZEN. [ ] Branded dozen correct design. Any binary fail = reject."

**GAP-005** | Failure Category Classification | Severity: Medium | Confidence: 80%
HUIDIGE STAAT: Geen gestructureerde manier om te classificeren of een failure prompt-fixbaar, model-limiet, referentie-kwaliteit, of concept-issue is.
GEWENSTE TIER: B (toevoegen aan video-qa-rubric.md)
FIX: "## Failure Classification — Cat A (Prompt-fixbaar): adjust prompt. Cat B (Model limiet): simplificeer shot of wissel model. Cat C (Referentie kwaliteit): regenereer hero frame. Cat D (Concept issue): herontwerp shot concept."

**GAP-006** | Cost Ceiling Enforcement | Severity: CRITICAL | Confidence: 90%
HUIDIGE STAAT: Geen hard budget ceiling. Test run $9.10 voor afgekeurde video. Geen per-video, per-sessie, of maandelijkse cap.
GEWENSTE TIER: A (non-negotiable in CLAUDE.md)
FIX: "## Cost Ceiling — MUST track cumulative cost per brief. Per-video hard ceiling: $15. Per-session: $50. Monthly target: $300-400. Bij 80%: Telegram warning. Bij 100%: STOP, escalate, wait for approval."

---

## HINDSIGHT STATUS

**HIND-001** | Gap | Severity: High | Confidence: 95%
HUIDIGE STAAT: GEDEELTELIJK geïnstalleerd. `~/.hindsight/profiles/` directory bestaat met `claude-code` profiel (port 9077, aangemaakt 2026-04-09). Metadata en env bestaan. MAAR: `hindsight-embed` niet in PATH, binary niet operationeel, log 26MB maar daemon draait niet, last_used >33 uur geleden. Env wijst naar `gpt-4o-mini` als LLM provider (externe afhankelijkheid).
FIX: BLOKKADE 3 IS NOG OPEN. Stappen: (1) Install hindsight-embed correct. (2) Startup hook: verifieer daemon draait voor productie. (3) Overweeg lokale embeddings ipv gpt-4o-mini.

---

## FINAL VERDICT (Skill Library)

### A. Skill Health Score
**0/11 skills halen alle 8 criteria (0%).** Gemiddelde pass rate: 4.2/8 (52%).
Universele failure: ALLE 11 skills missen negatieve trigger condities.

### B. Invocation Reliability
**Gemiddeld: 49%** — consistent met Vercel's 44% success rate. Kritieke enforcement skills hebben LAAGSTE rates (production-checklist 20%, character-consistency 25%, captions 30%).

### C. CLAUDE.md Instruction Count
- Huidig: ~86 instructies + ~50 system = ~136 totaal
- Aanbevolen Tier A: max 50
- Na aanbevolen wijzigingen: ~50 (add production gates + cost ceiling, remove anti-sycophancy body + generation details + telegram details + maintenance)

### D. Tier Verdeling
- Tier A (CLAUDE.md): 86 instructies (te veel, max 50)
- Tier B (skills): 11 bestanden, ~12.655 woorden
- Tier C (hooks): 0 — GEEN hooks bestaan
- Wrong-tier items: 5 gevonden

### E. Hindsight Status
**BLOKKADE 3 NOG OPEN.** Daemon draait niet. Geen auto-recall of auto-retain actief.

### F. Top 5 Skill Fixes
1. Production-checklist naar Tier A — voorkomt ~80% afwijzingen
2. Character-consistency invocation fixen — elimineert character drift
3. Negatieve triggers aan ALLE 11 skills — reduceert false positives 15-20%
4. higgsfield-generation.md splitsen — verbetert selectieve aandacht
5. Caption timing regels naar production-checklist — elimineert caption rejections

### Top 5 Nieuwe Procedures
1. Cost ceiling enforcement (Tier A) — voorkomt runaway spend
2. Model capability ceiling detection (Tier B) — voorkomt herhaalde waste
3. Per-clip evaluator handoff template (Tier B) — voorkomt blind assembly
4. Brand compliance binary checklist (Tier B) — vangt specifieke brand failures
5. Agent coordination protocol (Tier B) — formaliseert multi-agent workflows

---

# PART 3: CREATIVE OUTPUT AUDIT

## Clips Onderzocht
- 11 geanimeerde video clips (4 in V1, 2 in V2, 5 in V3)
- 3 finale assemblages
- ~20 hero frames

## Cost Metric
- Approved videos: **0**
- Total credits gespendeerd: **~$25-30**
- Credits per approved video: **WISKUNDIG ONGEDEFINIEERD (denominator is 0)**

---

## ATTEMPT 1: "Meet the Team" (V1)

### A1-S1 — Truck Establishing
**TIER 1: FAIL** — 1464x628 (ultrawide, niet 9:16). Massive black bars bij scaling naar 1080x1920.
**TIER 2: 3.25/5 FAIL** — Choppy camera, truck text warps t=2.5-4, wrong aspect ratio kills cinematic quality (2.5/5).
**TIER 3: 3.6/5 FAIL** — Logo degrades during animation. Truck branding readable at t=0, garbled at t=4.
**TIER 4: 2.0/5 FAIL** — Tiny truck in black bars is niet een hook. Brand barely legible.
**ROOT CAUSE: OPERATOR** — Hero frame 1024x1024, niet 9:16. Skill voorschreef aspect_ratio: "9:16" maar niet toegepast.

### A1-S2 — Mourad Portrait
**TIER 1: FAIL** — 960x960 (1:1, niet 9:16).
**TIER 2: 3.44/5 FAIL** — Expression changes: warm smile t=0 → neutral t=2.5 → different t=4. Truck text behind morphs.
**TIER 3: 3.75/5 FAIL** — Truck branding behind Mourad degrades (SNELVERHUIZEN → garbled).
**TIER 4: 2.6/5 FAIL** — Square format in vertical slot.
**ROOT CAUSE: OPERATOR** — 1:1 ipv 9:16. Expression changes niet gevangen door QA.

### A1-S3 — Karel with Box
**TIER 1: FAIL** — 960x960.
**TIER 2: 3.22/5 FAIL** — Box text morphs, phantom SNELVERHUIZEN label verschijnt op shirt. Slight rocking motion.
**TIER 3: 3.58/5 FAIL** — Box branding warps, phantom brand elements.
**TIER 4: 2.5/5 FAIL** — Wrong format.
**ROOT CAUSE: OPERATOR + MODEL CEILING** — Aspect ratio fout (operator). Text morphing during I2V (ceiling).

### A1-S4 — Team Together
**TIER 1: CONDITIONAL PASS** — 704x1304 (portrait maar niet 1080p).
**TIER 2: 3.44/5 FAIL (net)** — Karel face drift t=4. "Breathing" artifacts.
**TIER 3: 3.83/5 FAIL** — Truck logos blurry, branding in achtergrond onleesbaar.
**TIER 4: 2.8/5 FAIL** — Undersize resolution.
**ROOT CAUSE: OPERATOR** — Resolutie te laag.

### A1-S5 — Logo End Card
**TIER 1: PASS** — Statische end card via FFmpeg, 1080x1920. Niet AI-gegenereerd.

### A1-FINAL — Assembled Video
**TIER 1: FAIL** — Massive black bars shots 1-3. Captions via FFmpeg drawtext (niet Remotion). "MOURAD" name card + VO caption simultaan. Geen word-by-word, geen oranje highlight.
**ROOT CAUSE: OPERATOR (aspect ratio) + SKILL/PROCEDURE (captions)**

---

## ATTEMPT 2: "Meet the Team" (V2)

### A2-S1 — Mourad Portrait v2
**TIER 1: CONDITIONAL PASS** — 1076x1924 (native 9:16, ~1080p). Verbetering over V1.
**TIER 2: 3.28/5 FAIL** — Ghost truck (drifts position, license plate "SREE K" gibberish t=2.5). Truck branding op WITTE achtergrond ipv oranje panel. Breathing artifacts.
**TIER 3: 3.33/5 FAIL** — Truck shows white panel with small text ipv signature full orange panel. Major branding deviation.
**TIER 4: 2.7/5 FAIL** — Ghost truck destroys credibility.
**ROOT CAUSE: OPERATOR + MODEL CEILING** — Camera angle hides brand (operator). Ghost truck motion (discipline — was geflagged in V1). Truck text morphing (ceiling).

### A2-S2 — Team Together v2
**TIER 1: CONDITIONAL PASS** — 1056x1956 (9:16).
**TIER 2: 3.39/5 FAIL (net)** — "Weird breathing" (owner). Truck branding wrong style (white panel, small text).
**TIER 3: 3.42/5 FAIL** — Truck angle doesn't show orange branding.
**TIER 4: 2.7/5 FAIL** — Two men standing is not dynamic.
**ROOT CAUSE: OPERATOR** — Truck angle STILL wrong despite V1 feedback. Breathing artifacts STILL present despite V1 correction instructions.

### A2-FINAL — Assembled Video
**TIER 1: FAIL** — "MOURAD" + "MOURAD EN KAREL" simultaan (doubled text issue from V1 STILL PRESENT). Captions nog block-appear, niet word-by-word. Geen oranje highlight. Slechts 2 shots.
**ROOT CAUSE: DISCIPLINE** — Alle 4 V1 issues (doubled text, word-by-word, ghost truck, breathing) recurred. Checklist bestond. Memory bestond. Agent paste het niet toe.

---

## ATTEMPT 3: "Verhuizen zonder zorgen"

### A3-S1 — Truck at Canal
**TIER 1: PASS** — 1056x1956 (9:16).
**TIER 2: 3.38/5 FAIL** — Truck CREEPS FORWARD (ghost driving WEER). Truck on flooded canal questionable physics. Text garbled by t=4.
**TIER 3: 3.9/5 FAIL (net)** — SNELVERHUIZEN readable at t=0, garbled at t=4.
**TIER 4: 2.9/5 FAIL** — Beautiful frame ruined by ghost truck on repeat viewing.
**ROOT CAUSE: MODEL CEILING (text) + DISCIPLINE (ghost truck)** — Text degradation = ceiling. Ghost truck = discipline (was flagged in V1 AND V2).

### A3-S2 — Boxes Interior
**TIER 1: PASS** — 1076x1924.
**TIER 2: 4.06/5 PASS** — Excellent interior, natural light, stable boxes.
**TIER 3: 3.8/5 FAIL (net)** — Box text uses YELLOW/GOLD instead of orange. Box material wrong (brown/kraft ipv white).
**TIER 4: 3.2/5 FAIL** — CTA absent drags score.
**ROOT CAUSE: OPERATOR** — Box branding color wrong. Agent didn't compare against reference.

### A3-S3 — Mourad at Doorway
**TIER 1: PASS** — 1076x1924.
**TIER 2: 3.28/5 FAIL** — MAJOR: truck text changes to garbled. URL becomes "www.sedeerhuiren.nl" (FABRICATED). Subtext becomes "verhuizen in de nego" (WRONG).
**TIER 3: 3.25/5 FAIL** — WORST brand integrity across all attempts. Fabricated URL.
**TIER 4: 2.1/5 FAIL** — Fabricated URL would send viewers to wrong website. WORSE than no CTA.
**ROOT CAUSE: DISCIPLINE (primary) + MODEL CEILING (secondary)** — Agent did NOT watch clips before assembly (confirmed in post-mortem). Text morphing is ceiling, but DELIVERY without catching it is discipline.

### A3-S4 — Box Detail Close-up ★
**TIER 1: PASS** — 1076x1924.
**TIER 2: 4.31/5 PASS** — Highest scoring clip. Beautiful close-up, stable text, smooth motion.
**TIER 3: 4.4/5 PASS** — SNELVERHUIZEN.NL, 085 3331133, VERHUIZEN ZONDER ZORGEN all correct and legible throughout animation.
**TIER 4: 3.6/5 PASS (net)** — Phone number visible. Looks completely real.
**ROOT CAUSE: N/A — PASSES ALL TIERS** — Succeeds because: static object, no human anatomy, minimal camera movement, close-up framing eliminates complex backgrounds, text at large scale preserved. VALIDATES THE APPROACH: simple compositions with limited text and no people produce broadcast-quality results.

### A3-S5 — Truck Golden Hour
**TIER 1: PASS** — 1056x1956.
**TIER 2: 3.63/5 PASS (net)** — Better than earlier attempts. Truck appears stationary (IMPROVEMENT). Text degrades but less severe.
**TIER 3: 3.9/5 FAIL (net)** — Text degradation during animation.
**TIER 4: 3.0/5 FAIL (net)** — CTA absent.
**ROOT CAUSE: MODEL CEILING** — Correct composition, stationary truck (learned!), correct format. Text degradation is genuine Kling v3 ceiling.

### A3-FINAL — Assembled Video
**TIER 1: FAIL** — Caption positioning wrong (top-left, not centered). Not word-by-word. Ghost truck in shot 1. Fabricated URL in shot 3. No end card/CTA.
**ROOT CAUSE: DISCIPLINE** — Clips not reviewed. Caption spec not followed.

---

## Pass Rate Per Tier

| Tier | Pass | Fail | Rate |
|------|------|------|------|
| TIER 1 (Technical) | 5/11 | 6/11 | 45% |
| TIER 2 (Visual Quality ≥3.5) | 3/11 | 8/11 | 27% |
| TIER 3 (Brand Compliance ≥4.0) | 1/11 | 10/11 | 9% |
| TIER 4 (Ad Effectiveness ≥3.5) | 1/11 | 10/11 | 9% |
| **ALLE TIERS PASS** | **1/11** | **10/11** | **9%** |

Enige clip die alle tiers haalt: **A3-S4 (Box Detail Close-up)**

## Root Cause Distributie

| Categorie | Aantal | % | Clips |
|-----------|--------|---|-------|
| OPERATOR FAILURE | 5 | 45% | A1-S1, A1-S2, A1-S4, A2-S1, A3-S2 |
| DISCIPLINE FAILURE | 3 | 27% | A2-S2, A3-S3, A2/A3 Finals |
| MODEL CEILING | 2 | 18% | A3-S1 (partial), A3-S5 |
| SKILL/PROCEDURE | 1 | 9% | A1-S3 (partial, caption pipeline) |

## Ceiling Alert
**Kling v3 kan complexe tekst NIET behouden over 5 seconden animatie.** Dit is bewezen over alle 3 pogingen.
**Workarounds:** (1) Tekst compositen als overlay na animatie, (2) Camera-hoek waarbij tekst niet prominent is, (3) Clips korter (3s), (4) Close-ups van tekst (A3-S4 bewijst dat dit WERKT op grote schaal).

## Workflow Gaps

| Gate | Bestond? | Toegepast? | Impact |
|------|----------|------------|--------|
| Brief validatie | Ja | Ja | Laag |
| Prompt quality review | Nee | Nee | Hoog — slecht prompts kosten credits |
| 3-5 varianten per shot | Nee (altijd 1) | N/A | Hoog — geen selectie = geen kwaliteitsoptimalisatie |
| I2V (niet T2V) | Ja | Ja | N/A — correct |
| First-pass visual review (stills) | Ja | Ja | Laag |
| First-pass visual review (video) | Nee | Nee | KRITIEK — 7/10 failures gevangen als dit bestond |
| Frame-by-frame assessment | Nee | Nee | Hoog |
| Brand compliance gate | Nee | Nee | Hoog — 10/11 clips falen op brand |
| Three-agent Evaluator | Nee | Nee | KRITIEK — kern van het probleem |
| Gestructureerde owner feedback | Ja | Ja | Laag |

## Kan Output 80%+ Approval Rate Bereiken?
**JA, met confidence 65%** — mits:
1. Three-agent Evaluator geïmplementeerd
2. Elke clip individueel beoordeeld vóór assembly
3. Native 9:16 (bewezen werkend)
4. Tekst-overlay compositing (ceiling workaround)
5. Minimale motion prompts met endpoints
82% van failures is FIXBAAR. 18% is ceiling met viable workarounds.

## Top 3 Veranderingen
1. **Hard-gate frame extraction + visual review na ELKE clip** — vangt 7/10 failures
2. **Native 9:16 afdwingen** — elimineert V1 black bar ramp (4 clips)
3. **Tekst als overlay compositen na animatie** — omzeilt Kling v3 text ceiling

---

# GECOMBINEERD VERDICT

**Status:** Pre-operationeel met bewezen architectuur.

**Primaire failure mode:** De operator beoordeelt eigen werk niet kritisch genoeg en past opgeslagen feedback niet consequent toe. Dit is een discipline probleem, niet een architectuur probleem.

**82% van alle failures is fixbaar** door betere executie. 18% is model ceiling met bewezen workarounds (tekst overlay compositing, simpelere composities, kortere clips).

**De enige clip die ALLE tiers haalt (A3-S4 Box Detail) bewijst:** wanneer het shot simpel is (statisch object, geen mensen, minimale camera, close-up), produceert de pipeline broadcast-kwaliteit. De weg vooruit is niet complexere technologie maar slimmere shot-keuzes plus rigoureuze QA.

**Drie blokkades moeten weg:**
1. ❌ Three-agent pattern (Planner/Generator/Evaluator)
2. ❌ Snorkel AI triage (zero loops routine, 3-5 loops creatief)
3. ❌ Hindsight stabiel (auto-recall, auto-retain, 48u monitoring)

**Na implementatie blokkades + eerste 5 goedgekeurde video's → operationeel.**

**Confidence:** 55% dat operator binnen 1-2 weken na blokkade-implementatie betrouwbaar 1 video/dag kan leveren. 65% dat output 80%+ approval rate kan bereiken met de fixes.

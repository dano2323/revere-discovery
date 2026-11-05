# 01 — Audit and reconciliation

**Version 0.1 · Draft · 5 Nov 2026 · Step 1 of the work plan.** What Discovery takes from each source, what today's platform shows and what happens to it, how the brand and employer lines differ, and the decisions needed before step 2 (the skill). Decisions are numbered **D1…**; open questions **Q1…**.

---

## 1. Sources reviewed
| Source | What it is | Status |
|---|---|---|
| **Employer Discovery docs** (Sept 2026): build playbook v1.23, content guidelines v1.21, design system v1.33, `revere-discovery-presentation.css` v1.32, `collision_sweep.py`, Caterpillar deck | The last full Discovery process: a 16-slide, 1280×720 HTML deck built in chat from the computed export | **Superseded on methodology and stance** (§3, §4); kept for the deck's form, archetypes and Gate D checks |
| **Category Briefs** (`revere-category-reports`): `category-brief-spec.md`, `employer-overrides.md` | The current Index methodology for both lines | **Governs methodology** (Dan, 5 Nov) |
| **Trust Engine** (`revere-lippincott-trust-engine`, `revere-te-design-system`) | The process model: runbook → build playbook → design system → prototype → PRD. TEDR spec for discovery-as-teaser | **Model for process and design**; TE wins design conflicts |
| **Core platform screenshots** (`source/platform/screens/`), both logins | Today's Discovery setup, settings, template editor, report view, drill-downs, history, versions, share link | **A catalog, not inspiration** (Dan, 5 Nov) |
| **Sample exports** (`inbox/`): Allstate (brand, Gemini 3.1 with search), Jimmy John's (employer, GPT-5.6 with search) | The current computed export, one file per run | Sample data for the skill and prototype only (§7) |

## 2. What carries over from Trust Engine
| Take | Adapt | Leave behind |
|---|---|---|
| The shape of the work: runbook (setup) → build playbook (gates) → spec → content guidelines → design system → prototype → PRD | Setup is **light**: no working intent, fact sheet or question-set authoring (Dan, 5 Nov). Setup is the intake form, then review and launch | Steps 3–5 of the TE runbook (intent, question set, fact sheet) and their documents |
| One general extract from day one; no per-report scripts | The extract reads platform **records**, not exports, in the PRD | Co-branding; Lippincott framework, dimensions and vocabulary |
| Report = container; locked, numbered versions; nothing a prospect received is lost | Versions already exist on today's platform ("Reporting – … Generate new version"); keep the idea, replace the screen | |
| Signals and opportunities, never findings; "In a full audit" line per section; "More signals worth a closer look"; a held-back list | Applied to both lines (§4) | |
| Tier 1 components shared by platform and print; evidence panel; no platform-only charts | Add a **slide** surface beside platform and print (§8) | TE-specific figures with no Discovery use (CoverageBars, MatchMap, ChainDiagram) stay in TE's layer |
| Methodology hidden: no prompts, run counts or scoring mechanics in the product; admin-only prompt and raw views | Stricter on core: an individual brand lead may log in (Dan, 5 Nov) | |

## 3. Methodology (Category Briefs govern)
| Item | Brand line | Employer line | Note |
|---|---|---|---|
| Index name | Revere AI Brand Index | Revere AI Employer Index | |
| Components and weights | Visibility 35 · Sentiment 35 · Brand Pillars 15 · Purchase Criteria 15 | Rank 25 · Sentiment 25 · EVP Pillars 25 · Choice Criteria 25 | Brand matches today's platform. Employer: Category Brief rule (Dan, 1 Nov). Whether brand moves to equal weights is open in the Category Brief repo; Discovery follows whatever it decides |
| Scale | Every displayed score 0–100 | Same | Platform still shows /50 and /10; the report never does |
| Verdict bands | Strong ≥67 · Mixed 50–66 · <50 | Same | **D2** names the word for <50 |
| Relative read | Leading · Inline · Lagging tag, never a color | Same | "The divergence is the finding" stays |
| Rank (employer) | — | Category Briefs compute Rank from full 20-item lists (mean points × 5). Discovery lists are top-10 (absent = 11) | **Q4**: one Rank formula for both products, set in the platform |
| Index visual | The Category Brief's **Index Visual** (mark + contribution bar), not the Discovery wheel | Same | The brief rejected arc length = weight (every subject looked identical). Retire the wheel |

**Retired from the Employer Discovery docs:** "Rank is retired" (§1.2a); the 50/25/25 index; the completeness doctrine (§1.6); the standalone Emergent Framing chapter as a measured dimension (keep emergent framing as a *signal* where the data shows one).

## 4. Discovery is a teaser (the content stance)
Discovery exists to open a conversation for a full audit (Dan and Mike, 4–5 Nov; Mike: "not giving away too much information if these will be free").

1. **Signals and opportunities, never findings.** Headlines lean to the question or the opening. Same rule as TEDRs.
2. **Show the Index; hold back the parts.** Subject's Index and its four components, against the set. Competitors' components appear only where a section's signal needs them.
3. **One signal per section,** one figure, at most one verbatim quote, one "In a full audit" line.
4. **"More signals worth a closer look":** a short list, each ending "Worth a follow-up." The only next step is a full audit (no Focus Areas, no action list).
5. **Short.** Target 10–12 slides (was 16). Cover with the photographic ground stays (Mike).
6. **Held back for the full audit** (proposal, **D3**): results by question; all ranked lists; every pillar and criterion explanation; sources beyond the subject's own vs. outside; multiple models, personas and markets; recommendations.

**Report, platform and audit are nested** (agreed 5 Nov). Report ⊂ platform ⊂ full audit. Every report figure is a platform figure; the platform adds the evidence behind it (the answers, explanations, sources), never new measures. What the audit sells is held back on both. A prospect only ever sees the report.

## 5. Today's report view: catalog and fate
Fates: **Report** (on a slide) · **Evidence** (platform panel, behind a report figure) · **Held** (full audit only) · **Drop**.

| Today (both lines unless noted) | Fate | Note |
|---|---|---|
| Subject header + model-written company description | Drop | Unverified model text with inline markdown links |
| Index donut, four component tiles (/50, /10) | Report | As the Index Visual, 0–100 |
| "Generated by <model>" chip | Report | As the scope stamp (model · market · persona) |
| Positive / negative attributes | Report (one signal) · Evidence (full list) | Praise and fault themes, as TE ThemeColumns |
| Competitor Analysis cards (donut per competitor) | Report | One comparison figure, not a card per competitor |
| Brand Pillars / EVP matrix (subject × competitors) | Report (signal) · Evidence (rest) | Dumbbell or comparison table; explanations and sources in Evidence |
| Purchase / Choice Criteria matrix | Same as pillars | Criteria are model-generated; say so once |
| Summary panels (model prose) beside each matrix | Drop | Replaced by the authored signal |
| Sources table, type filter, frequency bars, Validated mark, citations popover | Report (own vs. outside) · Evidence (top domains) · Held (full explorer) | Never compare citation frequency across brands (TE rule) |
| Focus Areas, "Add all to action list" | Drop | Workstreams belong after an audit (Dan, 5 Nov) |
| Drill-down: Visibility/Rank sets (each ranked list) | Evidence (subject's position) · Held (full lists) | |
| Drill-down: sentiment by question × dataset (emoji grid) | Drop | Run counts; methodology |
| Drill-down: one answer, its grade, explanation, sources | Evidence | The verbatim layer; no grader explanation for non-admins |
| Drill-down: average sentiment by question, competitor average | Report (questions where the subject trails) · Held (full table) | As TE QuestionBars |
| Drill-down: sentiment drivers (mentions, signal strength) | Evidence | |
| Drill-down: pillar / criteria explanation tables | Evidence | |
| Drill-down: Index formula (raw, normalized, contribution) | Report (contribution bar) | No raw scales |
| Share link (login required) | Replace | Locked report versions (TE §6.4); not a platform link |
| Reporting: versions, Generate new version | Replace | TE report versions |
| Download icons per table, Export | Admin only | Records replace exports (§7) |

## 6. Today's setup: catalog and fate
| Today | Fate | Note |
|---|---|---|
| Brand / Product switch | Keep (brand line only) | **Q2**: what Product mode changes. Known: it limits purchase criteria |
| Brand / Employer name | Keep | |
| LLM (offline and search variants) | Keep, search models only, default GPT-6.1 with search | One model in Discovery |
| Category (suggested from the brand, or manual) | Keep | |
| Category Type | Hide | Confirm unused (**Q3**) |
| Market | Keep | |
| Competitors (suggested from the category; same list as the gear's Competitive Set, up to 10) | Keep, on the form only | Dan tested 5 Nov: one list |
| Template dropdown; template editor (Visibility/Rank prompt, sentiment questions, pillars, criteria) | Hide from users; Revere admin | Discovery runs the line's standard template. Base prompts versioned and visible to admins (TE PRD §5.6) |
| Visibility attributes (Top, Best, Most Recommended; custom) | Admin | Part of the standard template |
| Batch mode (employer) | Default on for Discovery (**D5**) | Async, cheaper. Discovery is a volume BD tool |
| Rank methodology: by category / by named competitor (employer) | Admin; default by category | |
| Launch limit ("10 launches remaining") | Keep, quiet | |
| View History modal | Replace | A Discovery Reports list page (TE APP-3) |
| Progress ("13 of 13 tasks completed") | Keep, as run status | |

## 7. Data
- **Target state: no exports.** Every step reads the run's records on the platform (TE PRD v0.7 principle). Exports are sample data for the skill and prototype until then, and an admin download after.
- **The export is now self-describing:** a `key_legend` documents every field, origin (raw or processed) and scale. Use it as the dev team's own field definitions in the PRD.
- **Already in the export:** a source rollup by type (own, competitors, PR and media, third party), by model and by metric. This closes the old Sources gap.
- **New question types exist on the core platform:** open-ended (no brand named) and fact-based questions (`OEQ`, `FBQ`, "present only when configured"); neither sample uses them. **Q5**: are they in the standard Discovery template, or available to add?
- **Run shape in the samples:** one model, General market, General persona; brand set of 4 (Allstate + 3), employer set of 6 (Jimmy John's + 5); 12 and 8 sentiment questions.

## 8. Design system
- **Source of truth: `revere-design-system`,** seeded from the TE tokens and Tier 1 components. TE wins conflicts. TE keeps its own copy until its round 1 ships, then moves to the shared one.
- **Three surfaces, one component:** `platform`, `print` (portrait), `slide` (1280×720). A slide is a composition of Tier 1 pieces (headline, signal, one figure, quote, audit line). On the platform the figure takes the main panel; the narrative pieces move to the evidence panel. Nothing is drawn only for the platform (TE rule 13).
- **From the Discovery deck system, keep:** fixed 1280×720 canvas and scaling contract; light content, dark frame (cover, dividers, close); cover photo under a scrim; one primary component per slide; density budgets; Gate D collision sweep (ported to the slide surface).
- **Replace with TE:** tokens (identical brand values, plus platform tokens); type rules (no italic; bold for scanning); figures (Dumbbell, RankedBars, QuestionBars, ThemeColumns, SourceMix, ComparisonTable).
- **Line switch:** `line: 'brand' | 'employer'` swaps labels only (Visibility ↔ Rank, Brand Pillars ↔ EVP Pillars, Purchase ↔ Choice Criteria, brand ↔ employer, customers ↔ candidates). Set by login.
- **Ignore** the old project file "Revere presentation design inspiration.png."

## 9. Brand vs. employer
| | Brand | Employer |
|---|---|---|
| Who reads it | CMO, brand and comms leads, agencies | CHRO, heads of talent, employer-brand leads, agencies |
| Presence measure | Visibility | Rank |
| Qualities | Brand Pillars (standard set, editable) | EVP Pillars (12 in the standard template) |
| Decision lens | Purchase Criteria (model-generated) | Choice Criteria (model-generated) |
| Index weights | 35/35/15/15 | 25/25/25/25 |
| Sentiment questions | 12 (standard template) | 8 (standard template); several name the competitors |
| Product mode | Yes | No |
| Lead framing | Named ≠ recommended | "Are we losing the people we want, to whom, and why?" (CHRO lens); Glassdoor is the benchmark readers check |

Everything else is shared: process, gates, spec, slide architecture, components.

## 10. Decisions
| # | Decision | Recommendation |
|---|---|---|
| D1 | Methodology source | **Category Briefs govern** (decided, Dan, 5 Nov) |
| D2 | Word for <50 | **"Opening"** in Discovery (TE's discovery word; reads as opportunity); "Weak" in audits |
| D3 | Held back for the full audit | The list in §4.6 |
| D4 | Deck length | 10–12 slides |
| D5 | Batch mode | Default on for Discovery |
| D6 | Index visual | Category Brief Index Visual; retire the wheel |
| D7 | Repo layout | Shared `system/` (runbook, playbook, spec, guidelines, tools) over `brand/` and `employer/` overrides, as in Category Briefs |
| D8 | One run per report; a re-run is a new report | As TE |

## 11. Open questions
| # | For | Question |
|---|---|---|
| Q1 | Mike | Who uses the core platform's Discovery views: BD only (Revere, agency AMs), or also brand leads? (Asked by Dan, 5 Nov) |
| Q2 | Mike | What Product mode changes besides limiting purchase criteria |
| Q3 | Mike | Is Category Type used anywhere in Discovery prompts? |
| Q4 | Mike / dev team | One Rank formula for the employer line: Category Brief (20-item lists, mean points × 5) or the platform's (top-10, absent = 11)? |
| Q5 | Mike / dev team | Are open-ended and fact-based questions part of the standard Discovery templates? |
| Q6 | Dan | Contact block and CTA on the close: Revere only, or agency-branded when an agency runs it? |

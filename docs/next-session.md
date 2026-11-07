# Next session: handoff (6 Nov 2026, after the sweep)

Start here in a new chat, with `revere-discovery`, `revere-design-system` and `revere-category-reports` attached (and the TE repos if needed for reference).

## Where things stand
| Step | Status |
|---|---|
| 1 Audit | Done: `docs/01-audit.md` v0.2, decisions D1–D9; open questions `docs/open-questions.md` (DEV-1–6, RV-1–3) |
| 2 Skill | Docs done: `CLAUDE.md`, `system/runbook.md`, `spec.md` v0.3 (13 slides), `content-guidelines.md`, `build-playbook.md`, `brand/` and `employer/overrides.md`, templates. `system/tools/build_extract.py` done and tested on both samples. `system/tools/collision_sweep.py` done: specimen passes all hard gates; each check proven on a seeded defect |
| 3 Design system | `revere-design-system` v0.2: tokens, Tier 1 components, slide surface ported from the Caterpillar deck, deck viewer. Specimen approved by Dan, 6 Nov: `specimen/slides.html` (fictional brand sample, 13 slides) |
| 4 Prototype (platform views) | Not started |
| 5 PRD | Not started; after TE round 1 ships (about two weeks from 5 Nov) |

## Next
1. **Build the deck renderer** (`system/tools/`): `extract.json` + `draft.md` → a deck HTML using `revere-design-system` components. Proposed: a small per-deck `deck.jsx` built with esbuild, like the specimen.
2. **Proof builds through the skill**, one per line, cold: "Start a new Discovery for Allstate" (brand; Gemini 3.1 with search) and "… for Jimmy John's" (employer; GPT-5.6 with search). Exports are in `inbox/`. Runbook steps 1–2 already happened (the runs exist), so begin at step 3 (check the data), then Gates A–D. Gaps the cold build finds are doc gaps: fix the docs.
3. Then step 4: platform views (main panel + evidence panel), same components.

## Settled in the specimen review (don't relitigate)
- Copy density per signal slide: title, lede, two-to-four-sentence reading, figure, note; quote at the column foot.
- Emergent framing is its own slide, for both lines.
- Competitors' component scores are shown (Index table unblurred).
- Position tags colored; band shading beats striping; rows good on top.
- Layout rules: `revere-design-system/docs/02-caterpillar-pass.md`.

## Open
- Fonts: the sweep runs in Claude's workspace, where Google Fonts is blocked, so it is fed the fontsource files (`build-playbook.md`, Gate D). Proposal: self-host Outfit and JetBrains Mono in `revere-design-system/assets/fonts/` (OFL), so decks and PDFs render the same offline. Dan to decide.
- C1: sentiment bar color (system: only the subject in color; Caterpillar: by rank). Dan to decide.
- Product mode: needs a Product-mode export to add Product Dimensions to the extract.
- Sample quotes in the specimen are invented; real decks quote verbatim, checked at Gate B.

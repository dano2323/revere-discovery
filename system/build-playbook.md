# Discovery — Build Playbook

**Version 0.1 · 5 Nov 2026.** From the run's data to a client-ready deck. Both lines. Before the data: `runbook.md`. What the deck says: `spec.md`. How it's said: `content-guidelines.md`. How it renders: the shared design system.

---

## Gates
| Gate | What | Closes when |
|---|---|---|
| 0 | Data checked (runbook step 3) | Blocking questions answered |
| A | Scope and story: the scope stamp, the cover signal read in the raw answers, the slide list | Report lead approves |
| B | `build_extract.py` → `extract.json`: every figure and quote the deck shows | Script runs clean; quotes asserted verbatim |
| C | `draft.md`, then the two draft checks | Report lead approves; both checks pass |
| D | HTML deck, PDF, the sweeps, the two checks again on the built text | All pass |

## The deliverable folder
`subjects/<slug>/deck/`: `draft.md` (content in slide order; reviewed before the build) · `fact-check.md` (both checks, logged) · `extract.json` · `index.html` · `<subject>-ai-discovery.pdf`. The draft is the artifact of record: fix the draft first, then the deck.

## Gate A — Scope and story
1. **Scope stamp:** model · market · persona (General) · the brands. As run, from `record.md`.
2. **The cover signal** (`content-guidelines.md` §3): propose it and one alternate. For each, quote the raw answers it rests on and pass the four tests: holds in the answers; a contrast, not a score; rests on two measures or names its one; names the position, not the reason.
3. **Slide list:** the 12 slides of `spec.md`, with the signal proposed for each of slides 5–9 and the three or four tests for slide 10. Note any slide folded (a thin read may fold one).
4. **Index:** computed for each brand from the line's weights (`<line>/overrides.md`). Each component must be present for each brand; a missing one is a Gate 0 question, not a gap to bridge.

## Gate B — The extract
- **One script for both lines,** `system/tools/build_extract.py`, reading the run's data (today, the export in `data/raw/`; on the platform, its records). Never a per-subject copy.
- Writes `extract.json`: each figure on the deck, already on 0–100; the Index and its parts for each brand; Position tags; verdict bands; the quotes.
- **Quotes are listed with the answer they come from and asserted verbatim** against the answer text. A miss stops the build.
- Pillar and criteria scores come from the **unrounded run averages** (`rla`), never the rounded scores: rounding creates false ties and flips Position tags.
- No figure in the deck that isn't in `extract.json`.

## Gate C — The draft and the two checks
Write `draft.md` in slide order: for each slide, the eyebrow, headline, lede, the figure (named, with its `extract.json` keys), the quote, the "In a full audit" line. Then run both checks and log each in `fact-check.md`: statement, slide, what the data shows, resolution.

**1. Fact check.** Each statement stands only if a measure or a count of answers supports it *as written*: the number, the comparison, the direction, words like "all" and "none." A claim about what AI says is tested by searching the answer text, not by the score alone. Interpretation is labeled as interpretation.

**2. Plain-language check** (titles, ledes, the cover). A reader who hasn't seen the data can restate the line in their own words. Each sentence stands on its own. Nothing reads the wrong way round. Read the headlines aloud, in order, before the report lead reviews the draft. Then check the writing traps (`content-guidelines.md` §9).

**Also at Gate C:** one message per slide; one figure; at most one set-apart device (quote or callout); no title over two lines; no prose figure the adjacent figure already shows; the held-back list respected.

## Gate D — The deck
1. **Build** from `draft.md` and `extract.json` with the shared design system's slide surface (1280×720). Mark it Draft. Cover image from the Intake table; never invent one.
2. **Sweeps** (`system/tools/collision_sweep.py`, headless, at 1280×720), all slides:
   - **Fit:** nothing past the canvas. Fixed in the draft (split or trim), never with smaller type.
   - **Foot and stack collision:** no two blocks overlap, including the slide foot.
   - **Scaling:** the composition holds at other window sizes, 16:9, no reflow.
   - **Orphans:** no title or lede ends on a single word.
   - **Adherence:** Position tags match the rule from the visible numbers; one Index value and one placement across the cover, slide 2 and slide 4; no inline style sets a color, font or border.
3. **Look at every slide** in the browser and in the PDF.
4. **Re-run both checks on the built text;** log build-time changes in `fact-check.md`. `pdftotext <deck>.pdf - | grep -ciw every` for the "every" trap.
5. **Status** in `record.md`; commit.

When a build misses a rule that was already written, fix the deck **and** add the check to the sweep, so the rule stops depending on memory.

## Traps already paid for
- **A sharp result is usually ours.** "Zero Rank" came from the wrong prompt frame; the "missing career site" from a broken source chart. Read the raw answers before a sharp signal reaches the draft.
- **Typed figures drift.** Scores keyed to the nearest ten flipped Position tags. Take each figure from `extract.json`.
- **Rounded scores create ties.** Use the unrounded run averages.
- **A headline is a claim.** "Shares the lead on tolerability" failed: the tie was on two named qualities, not tolerability.
- **A single-measure cover gets rejected** ("rated highest" from one measure with a small gap). Two measures, or name the one.
- **The platform's own position field tags tied-last as Lagging.** Ignore it; compute the tag (ties are Inline).
- **Type raised late re-opens fit.** After any change to type size, re-run all the sweeps.
- **A second slide on the same measure must show something the first can't,** or it's restatement.

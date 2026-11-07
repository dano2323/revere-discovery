# Discovery Report — Spec

**Version 0.3 · 6 Nov 2026.** What a Discovery report says, in what order, and why. Both lines; line labels per `CLAUDE.md` rule 7. Decisions behind it: `docs/01-audit.md`.

---

## Purpose and reader
**Purpose:** open the conversation for a full audit. Show the subject, with its own data, one or two things about how AI represents it that it didn't know, and that one read raises questions only a full audit answers.
**Sent by:** Revere, agency account managers, or service providers Revere partners with (employer line). **Reader:** brand line, the CMO and brand or comms leads; employer line, the CHRO and heads of talent. Plus their agencies. Received by email, from Revere or an agency.
**Format:** presentation, 1280×720, HTML → PDF. **13 slides.** Readable in ten minutes; presentable live.

## Scope
One model (default: latest GPT with search) · one market · General persona · the subject and its competitors (up to 10). The scope is stated, never apologized for: it is what makes the full audit worth buying.

## Slides
Figures were chosen slide by slide against the Caterpillar deck and the TE figure set (`docs/01-audit.md` §8); the better of the two wins.

| # | Slide | Shows | Figure |
|---|---|---|---|
| 1 | **Cover** (dark, photo) | "A first look at <subject> in AI"; the cover signal as the headline; scope stamp; Draft mark | — |
| 2 | **The Discovery read** | The subject's Index and its four components, each with its verdict word (Strong · Mixed · Opening), weight and one line; one paragraph on how the components disagree | Index Visual + component stat list (Caterpillar slide 2) |
| 3 | **Where this measure sits** (report only) | The three lanes (surveys, review sites, the model layer); Discovery as the first of three depths (Discovery · Full audit · Monitoring) | Lanes and depths cards (Caterpillar slide 3); brand line names its own lanes |
| 4 | **Where it stands** | The Index across the set, subject outlined. Competitors' components shown blurred, "in a full audit" | Comparison table with blurred cells (Caterpillar slide 5 + Category Brief blurred table) |
| 5 | **Visibility / Rank** | Whether AI names the subject when asked for the best in the category, how often and how high | Ranked bars, plus appearance rate |
| 6 | **Sentiment** | Subject against the set; what lifts it and what holds it down; one verbatim quote. A cold spot by question is named in the text, not tabled | Ranked bars + lifts/holds columns (Caterpillar slide 6) |
| 7 | **Brand / EVP Pillars** (Product Dimensions in Product mode) | Where the subject leads, sits inline and trails. Product mode: the five dimensions as rows; subdimensions in the evidence panel | Comparison table with Position tags (Caterpillar slide 9), subject + up to 3 competitors + set average; larger sets use the Dumbbell |
| 8 | **Purchase / Choice Criteria** | What AI says buyers (candidates) weigh, and how the subject compares. Criteria are AI's own choice; say so once | Comparison table with Position tags (Caterpillar slide 10) |
| 9 | **Emergent framing** | The frames the model volunteers about the subject, unprompted by any pillar or criterion, by signal (how insistently it returns to them). Each mapped to the scored item it belongs to, or to none: those are **Emergent**, the frames no standard measure names. Both lines | Frame table (Caterpillar slide 11) |
| 10 | **Sources** | Share of citations by surface, the subject's own in green; its most-cited own pages. Never compare citation counts across brands | Ranked share bars (Caterpillar slide 12) |
| 11 | **What a full audit would test** | Three or four tests, each from a signal in this read, including any emergent frame, each "Worth a follow-up" | Numbered tests (Caterpillar slide 14) |
| 12 | **A full audit delivers** | What the audit adds: models, personas, markets, source attribution, strategic recommendations | Two-column list (Caterpillar slide 15) |
| 13 | **Close** (dark) | The CTA and contact (agency when an agency runs it; Revere otherwise); About this read (model, market, brands, date; scores 0–100; never run counts) | — |

**Copy on each signal slide** (sample deck: `revere-design-system/specimen/slides.html`): a title, a one- or two-sentence lede, a reading of two to four sentences that says what the figure means, and the figure. The figure carries the numbers; the copy carries the meaning.

No section dividers. Slides 5–10 follow the signal pattern below. Slide 3 is report only: the platform has no equivalent view.

**Figures new to the shared design system** (Tier 1, from the Caterpillar deck and Category Briefs): blurred cells on ComparisonTable; component stat list; lifts/holds columns; ranked share bars with own-site highlight. Report only (Tier 3): lanes and depths cards; numbered tests.

**Wide sets:** tables carry the subject, up to three competitors and the set average. Above that, the slide switches to the figure that scales (Dumbbell, ranked bars).

## Each signal slide (5–10)
1. **Eyebrow:** the measure.
2. **Headline:** a question or an opening, never a verdict.
3. **The signal:** one sentence, its scope in the sentence; then one or two of evidence.
4. **One figure,** sized to the claim.
5. **At most one verbatim quote,** serving this slide's claim; omit when none does.
6. **"In a full audit":** one line, what the audit adds for this measure.

## The cover signal
The single biggest signal in the read, whatever its measure. It must: hold in the raw answers; be a contrast, not a score; rest on at least two measures or name the one it rests on; name the position, not the reason. (TEDR spec, The cover signal.)

## Held back for the full audit
Not built in a Discovery; named on slides 10–11 as what an audit delivers:
- results by question (full table); all ranked lists; the emoji-style grid of individual answers
- each pillar and criterion explanation
- competitors' component scores
- the full sources explorer
- other models, personas and markets
- recommendations and focus areas

## Open for review
- Slide 4: competitors' Index shown, components blurred (decided, Dan, 5 Nov).
- Slide 7: the subject-only profile bars (Caterpillar slide 8) are dropped; the comparison carries the signal.

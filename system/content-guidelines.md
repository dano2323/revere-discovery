# Discovery — Content Guidelines

**Version 0.1 · 5 Nov 2026.** How a Discovery report is said. Both lines. `spec.md` owns what appears; the design system owns how it renders; `build-playbook.md` owns when it's checked. Line wording: `<line>/overrides.md`.

---

## 1. What we report
- **Revere reports on representation, not on the company.** "AI describes Allstate as…," never "Allstate is…." "AI says," never "AI knows."
- **One read, as far as the reader knows.** Page copy never refers to earlier runs, builds or versions.
- **Draft until published.** Each deck is marked Draft unless Dan and Mike approve publication; the approval (date, who) goes in `record.md`.

## 2. Discovery is a teaser
A Discovery opens a conversation for a full audit. It shows enough to make the reader want the rest, and no more.
- **Signals and opportunities, never findings.** On the page: "The signal:", "Worth a follow-up," "What a full audit would test."
- **Each signal carries its frame in the same sentence:** "In GPT-6.1's answers, …." State the signal plainly inside the frame; never hedge after it. The frame is what makes the reader ask what other models, personas and markets would show.
- **Make the signal interesting, not conclusive.** Name what a full audit *tests*, never what it *will find*.
- **Scope is a design, not a shortfall.**

| Write | Never write |
|---|---|
| Early signal · a signal worth testing · an opportunity to explore | Limitation · caveat · only · just · small sample |
| "A full audit tests whether this holds across models and markets" | "This may not hold for other models" |
| "In none of five answers" | "0%" |

- **The opportunity names where to look next, not what to do.** Recommendations and focus areas belong to the full audit.
- **Hold back what the audit sells** (`spec.md`, Held back). When a signal needs a held-back analysis, name it once as what the audit adds.
- **Show the whole set, then the highlight.** A figure shows all the measures in its view; the signal is one row of it. Never hand-pick rows that support the story.

## 3. The cover signal
- **The single biggest signal in the read,** whatever its measure.
- **It summarizes, not spotlights:** it rests on at least two measures, or names the one it rests on ("on AI's shortlists"). Never one pillar or one question presented as the overall picture.
- **It names the position, not the reason:** where the subject stands and who is ahead. Why AI places it there goes to a slide.
- **A competitor beating the subject across a measure is a major signal.** Name it.
- **It leans toward opportunity.** Name a competitor's advantage plainly, then the opening. "An opening in…," never "missing from…."

## 4. Headlines
- **A claim with a turn, not a label.** Setup clause, then a payoff clause in green: "Competitive everywhere, <span class="g">ahead almost nowhere</span>." Would a busy CMO or CHRO stop and read the slide?
- **Two lines, never three.** No single word stranded on the last line of a title or lede: reword, don't shrink.
- **Plain-language test:** a reader who hasn't seen the data can restate the line without asking what a word refers to. Each sentence stands on its own. If the clear version is too long, choose a simpler headline and let the copy carry the contrast.
- **A headline is a claim:** it goes through the fact check like any sentence.
- **Scope any single-measure statement:** "on the claims-service criterion," never an unqualified "rated highest."

## 5. Scores
- **Every score on the page is 0–100, a whole number** (`round()`), never rounded to the tens; no tilde. Rescaling happens in `build_extract.py`, never by hand.

| Native scale | To 0–100 |
|---|---|
| Sentiment, Visibility (0–50) | × 2 |
| Pillars, Product Dimensions, criteria (0–10) | × 10, from the unrounded run averages |
| Sentiment by question (1–5) | (x − 1) × 25 |
| Rank (employer) | `employer/overrides.md` |

- **Verdict bands** for the subject's own scores: Strong ≥67 · Mixed 50–66 · **Opening** <50. Never "Weak" in a Discovery.
- **Position tag** for the relative read: **Leading** = strictly above each competitor; **Lagging** = strictly below each; **Inline** = anything else, ties included. Computed, never typed. Color means the absolute band only; the tag is a word.
- **The divergence is the finding.** A strong score tagged Lagging, or a weak one tagged Leading, is the signal. Never collapse it.
- **Counts stay counts** ("four of five answers") where a measure rests on ten answers or fewer.
- **Never say how many times a question is run.** "Repeatedly," not "asked five times."
- **The Index is always shown with its parts,** never as a bare number.

## 6. Quotes
- **Verbatim model text only,** trimmed with an ellipsis, never paraphrased. Asserted word for word at Gate B.
- **A quote must serve the slide's claim.** If none does, omit it; never add one to fill space.
- **One per slide.** Attributed to the model and what it was asked about ("GPT-6.1, asked about the strongest and weakest aspects of working at Caterpillar").

## 7. Artifact-first
A sharp or surprising signal (a zero, a full score, a large gap) is a measurement artifact until the raw answers prove otherwise. Before it reaches the draft: (1) confirm the answers support it; (2) check whether the measurement causes it; (3) only then write it. Hedge an *interpretation* of why AI says something; keep the counts plain.

## 8. Sources
- Read the subject's own sites against outside sources; name the most-cited outside sources.
- **Each competitor is its own bar,** never pooled into one.
- **Never compare citation frequency across brands.**
- Shares, not counts.

## 9. Voice
- Confident and specific. Short sentences; break a long one into two.
- **No litanies of numbers in prose.** The figure carries the numbers; the sentence names the shape.
- American spelling and punctuation: periods and commas inside closing quotation marks.
- Models by family and version ("GPT-6.1, with live search"); "GPT," never "ChatGPT."

### Writing traps
Check the draft and the built text for each.

| Trap | Use instead |
|---|---|
| **every** | "each," "all," the count, or drop it |
| **finding** | "signal," "opportunity" |
| "rated highest," "best," "leads" without scope | Name the measure it rests on |
| Run counts | "repeatedly" |
| "AI knows" | "AI says" |
| "recommend" in a signal | "worth a follow-up" |
| Self-narrating honesty ("to be candid," "rather than paper over it") | Cut |
| A figure in prose that the adjacent figure already shows | Name the shape |

## 10. Calls to action and branding
- **"In a full audit" names a mechanism,** not a virtue: "the same questions asked of Claude and Gemini, with and without search," never "deeper insight." One line per signal slide.
- **The full audit is sold in two places:** "What a full audit would test" and "A full audit delivers." The close carries the contact.
- **Who sends it, signs it:** when an agency or partner runs the report, its name and contact go on the close; Revere's otherwise. Revere stays the measurement credit ("Measured by Revere").

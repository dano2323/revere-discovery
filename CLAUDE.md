# Revere Discovery — instructions for Claude

This repository is a skill: it builds Revere Discovery reports (brand and employer lines) and holds the design, prototype and PRD that move the process onto the core platform. Confidential. © 2026 Revere, Inc.

## Start here
- **"Start a new Discovery for <subject>"** or **"Continue the Discovery for <subject>":** follow `system/runbook.md` (setup to data), then `system/build-playbook.md` (data to deck). Existing subject: read `subjects/<slug>/record.md` first and resume at the first step not done.
- **Platform design or PRD work:** `docs/` (start with `docs/01-audit.md`).
- Docs still being written are marked "owed" in the table below. Don't improvise their rules; ask.

| When | Open |
|---|---|
| Setup to data | `system/runbook.md` (owed) |
| What the deck says, slide by slide | `system/spec.md` |
| Building and checking | `system/build-playbook.md` (owed) |
| How it's said | `system/content-guidelines.md` (owed) |
| Brand or employer differences | `brand/overrides.md`, `employer/overrides.md` (owed) |
| How it renders | `revere-design-system` repo (shared) |
| Decisions and their reasons | `docs/01-audit.md` |

A fact lives in one document; the others point to it.

## Rules that apply everywhere
1. **Discovery is a teaser.** Signals and opportunities, never findings. The only next step is a full audit. Hold back what the audit sells (`system/spec.md`, Held back).
2. **Methodology is private.** No prompts, run counts or scoring mechanics on any page or platform view.
3. **Every figure comes from the run's data,** through `build_extract.py`. Never type a number. Quotes are verbatim and checked.
4. **Artifact-first:** a sharp or surprising signal is a measurement artifact until the raw answers prove it.
5. **Mark every deck Draft** unless Dan and Mike decide to publish it.
6. **Words:** American spelling and punctuation; "GPT," not "ChatGPT"; "each" or "all," not "every"; scores 0–100; headlines pass a plain-language test.
7. **Line labels switch, nothing else:** Visibility ↔ Rank, Brand Pillars ↔ EVP Pillars, Purchase ↔ Choice Criteria.

## Working with Dan
- **Ask before writing new code or changing existing code.** Docs and data reviews don't need asking.
- Confirm structure (outlines, slide lists) before building.
- Brief answers; offer alternatives; say "I don't know" rather than guess.
- **Git:** Claude commits as work progresses (`Dan Olson` identity is set in this repo); Dan pushes. Exports stay in `inbox/` and are never committed.
- Docs are spec, not narrative: state the rule, not its history. No changelogs; git keeps history. Stable filenames; versions inside files.

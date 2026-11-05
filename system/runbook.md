# Discovery — Runbook

**Version 0.1 · 5 Nov 2026.** From "start a new Discovery for X" to the run's data in hand. Then `build-playbook.md` takes over. Written for the people involved and for Claude, which runs it. On the platform, these steps become the intake, Review and launch, and Check the data (`docs/`).

---

## How to use it
**People:** say *"Start a new Discovery for <subject>."* or *"Continue the Discovery for <subject>."* Claude stops whenever it needs an answer, an approval, or something only a person can do (configure the platform, download the export).

**Claude, throughout:**
1. **Find your place.** New subject: step 1. Existing: read `subjects/<slug>/record.md` and resume at the first step not done.
2. **Do your part, then stop at the gate.** Ask in one message, as a short list. Never pass a gate on your own judgment.
3. **Use the templates** in `system/templates/`; never write a subject file from scratch.
4. **Update `record.md` at the end of each step:** what was done, the date, who approved, what is waiting and on whom.
5. **Address people by role,** never by name, except in the record's Roles table.
6. **End with a Review line:** each file created or changed, what to check, and whether it's needed before the gate.

## Roles
| Role | Does |
|---|---|
| **Requester** | Asks for the report and sends it: Revere, an agency account manager, or a Revere partner. Confirms scope |
| **Report lead** | Reviews everything Claude drafts; owns the report |
| **Platform operator** | Configures and launches the run on the core platform; downloads the export |
| **Claude** | Runs this runbook and the build playbook |

## Where files go
```
subjects/<slug>/          <slug> = subject in kebab-case
  record.md               Status of each step; decisions; log
  setup/screens/          Platform setup screenshots
  data/                   data-manifest.md (committed); raw/ holds the export (never committed)
  deck/                   draft.md, fact-check.md, extract.json, index.html, the PDF
```

---

## Step 1 — Intake
**Claude:**
1. Propose the slug. Create the folder. Copy `templates/record.md` to it.
2. Fill the Intake table from the request: line (brand or employer), mode (brand or product; brand line only), subject, category, competitors, market, model, who sends it (and their contact for the close), cover image URL. Mark the rest "unknown — <role>".
3. Where the request is silent, propose: the category (as the platform would suggest it), up to 10 competitors from public sources (cite them), market "General Market," model "the latest GPT with search." Questions, pillars and ranked-list attributes: the line's default set (`<line>/overrides.md`), unless the requester asks to add or remove items.

**Gate — requester:** confirm or change each proposed row. Above all, the competitors: the read is only as meaningful as the set.
**Done when:** each Intake row is decided.

## Step 2 — Review and launch
**Gate first — platform operator:** configure the run on the Discovery tab from the Intake table: the line's standard template, batch mode on, items added or removed as decided. Screenshot each setup screen into `setup/screens/`. Say when done.
**Claude, once the screenshots are there:** check them against the Intake table, row by row. Write any fixes in platform terms.
**Gate — platform operator:** launch; say when the run completes.
**Done when:** the run has completed, and any difference from the Intake table is logged in `record.md` as run.

## Step 3 — Check the data
**Gate first — report lead:** download the run's export, unrenamed, into `data/raw/`.
**Claude, once it's there:**
1. Copy `templates/data-manifest.md` to `data/` and complete it: what arrived; coverage expected against present (brands × sentiment questions × pillars × criteria × ranked lists); sources present; every warning the export carries (`_meta`, `data_integrity_warnings`).
2. Read the raw answers behind any score that looks sharp: a zero, a full score, a large gap to the set (artifact-first, `content-guidelines.md` §7).
3. Write each question the data can't answer, and each failed check, as one numbered list, each marked blocking or not.

**Gate — requester (or platform operator for platform questions):** send the list; record answers in the manifest.
**Done when:** each blocking question is answered. **Next:** `build-playbook.md`, Gate A.

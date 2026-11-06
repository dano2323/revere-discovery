# Open questions

**For Revere's dev team and for Revere.** Each question is numbered once and never renumbered. Answered questions stay, with the answer and date.

## For the dev team
| # | Question | Found in | Status |
|---|---|---|---|
| DEV-1 | **Appearance rate above 1.** In the Jimmy John's employer run, Burger King's appearance rate (`RD` › `ac` › `ar`) is 1.4. A share of ranked answers should be at most 1. Is a brand being counted more than once in a list (e.g. two name variants), or is `ar` something other than a share? | Jimmy John's export (employer, GPT-5.6 with search) | Open |
| DEV-2 | **A competitor missing from the rank data.** Subway is in the run's competitor set but appears in neither the competitor rows (`ac`) nor the category list (`cl`). We read that as "never named in any ranked list" and score Rank 0. Is that right, or was Subway dropped (e.g. a name mismatch such as "Subway Restaurants")? | Jimmy John's export | Open |
| DEV-3 | **One name per brand.** The subject is "Jimmy John’s" (curly apostrophe) in the rank data and "Jimmy John's" (straight) elsewhere; a competitor is "Jersey Mike’s Subs" in `cl` and "Jersey Mike's" in `ac`. Can each brand carry one canonical name (and an ID) across all sections? | Jimmy John's export | Open |
| DEV-4 | **Employer Rank scoring.** Discovery scores Rank from 10-item lists: 10 points for first … 1 for tenth, 0 if not named, mean × 10 → 0–100. With absence imputed at 11, that equals (11 − rank score) × 10. Can the platform compute and store it? | `employer/overrides.md` | Open |
| DEV-5 | **Pillar names as typed.** The brand Standard Template's pillars arrive as entered: "innovation" (lower case), "Reponsibilty and Impact" (typo). Can names be fixed at source, and kept stable so runs compare? | Allstate export (brand, Gemini 3.1 with search) | Open |
| DEV-6 | **Tooling in the sources.** `validate.perfdrive.com` (a bot-check service) is counted as a third-party source, 2.7% of citations. Should tooling and redirect domains be dropped before sources are counted? | Allstate export | Open |

## For Revere
| # | Question | For | Status |
|---|---|---|---|
| RV-1 | Product mode: do Product Dimensions take Brand Pillars' 15% in the Brand Index? How do Purchase Criteria behave in Product mode? | Mike | **Answered 5 Nov:** yes, they take the 15%; Purchase Criteria still run |
| RV-2 | Is Category Type used anywhere in Discovery prompts? | Mike | Open (Q3) |
| RV-3 | Confirm employer Rank scoring (DEV-4) | Mike | Open (Q4) |

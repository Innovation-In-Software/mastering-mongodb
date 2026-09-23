# Kahoot quizzes — Mastering MongoDB

Instructor-only Kahoot Excel banks aligned to the module decks in
`decks/pptx_new/` (Modules 1–8). One quiz per module, 15 questions, 30 seconds.
Correct answers are shuffled so the right option is not always in the same slot.
All four answers are padded to **equal length** so players cannot guess by picking the longest.

Import `Kahoot_Module_N.xlsx` in Kahoot (Create → Import spreadsheet). Players join at [kahoot.it](https://kahoot.it) with the classroom PIN.

## Layout

```text
kahoot/
  README.md
  module_questions.json          ← generated snapshot (shuffled)
  Kahoot_Module_1.xlsx … 8.xlsx
  Kahoot_Quiz_Share_Links.xlsx   ← Creator / Share URLs, filled in after upload
```

| Day | Modules | Theme |
| --- | ------- | ----- |
| 1 | 1–3 | NoSQL, setup, data modeling |
| 2 | 4–5 | Query language, aggregation |
| 3 | 6–8 | Indexes, replication and sharding, production readiness |

| File | Matches |
| ---- | ------- |
| `Kahoot_Module_1.xlsx` | `MongoDB_Module01_Introduction_to_NoSQL_Databases.pptx` |
| `Kahoot_Module_2.xlsx` | `MongoDB_Module02_Installation_and_Setup.pptx` |
| `Kahoot_Module_3.xlsx` | `MongoDB_Module03_Data_Modeling_with_MongoDB.pptx` |
| `Kahoot_Module_4.xlsx` | `MongoDB_Module04_The_MongoDB_Query_Language.pptx` |
| `Kahoot_Module_5.xlsx` | `MongoDB_Module05_The_Aggregation_Framework.pptx` |
| `Kahoot_Module_6.xlsx` | `MongoDB_Module06_Indexing_and_Query_Performance.pptx` |
| `Kahoot_Module_7.xlsx` | `MongoDB_Module07_Introduction_to_Replication_and_Sharding.pptx` |
| `Kahoot_Module_8.xlsx` | `MongoDB_Module08_Best_Practices_Security_and_Troubleshooting.pptx` |

## Excel format

`Question | Answer 1 | Answer 2 | Answer 3 | Answer 4 | Time | Correct`

- **Time:** 30 seconds per question
- **Correct:** 1-based answer index (1–4); answer order is shuffled per question (stable seed)
- **Questions per module:** 15 (conceptual; drawn from that module's deck; no lab or slide numbers)
- **Answer length:** all four options the same character count (Kahoot max 60; question max 95)

Suggested Kahoot title: `Mastering MongoDB — Module N — <module title>`.

## Regenerate Excel from the question bank

`scripts/mongodb_kahoot_questions.py` is the source of truth.

```powershell
python scripts/check_kahoot_length_tells.py
python scripts/regenerate_kahoot_xlsx.py
python scripts/kahoot_share_links.py
```

After a quiz is created in Kahoot, paste the Creator and Share URLs into
`Kahoot_Quiz_Share_Links.xlsx`. Re-running `kahoot_share_links.py` keeps URLs already stored in that workbook.

## Bulk upload (Playwright)

Kahoot has no public bulk-create API. `scripts/kahoot_bulk_upload/kahoot_bulk_upload.py` drives the creator: Create → Import spreadsheet → Save as Private. It reuses the instructor Chrome profile that is already logged in to Kahoot. Modules already marked Uploaded in the share-links workbook are skipped.

```powershell
python scripts/kahoot_bulk_upload/kahoot_bulk_upload.py
```

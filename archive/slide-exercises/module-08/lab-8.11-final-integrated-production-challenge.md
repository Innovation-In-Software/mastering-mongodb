# Lab 8.11: Final Integrated Production Challenge

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 45–60 min  
**Difficulty:** Intermediate

**Objective:** Prepare training_store for a production-readiness review: one schema fix, validation, monthly sales pipeline, indexes, least-privilege notes, RPO/RTO, monitoring, alerts, one runbook, and a completed checklist.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

**Prerequisite:** `training_store` is loaded from [`datasets/training_store/load.js`](../../datasets/training_store/load.js). Reload at the start of Day 3 if Day 2 writes remain.

```javascript
use training_store
```

**Scratch database:** Labs that change validation, users, or restored data use `training_store_ops` so `training_store` stays intact for later work.

**Small-data note:** Twelve products and seventeen orders will not produce dramatic wall-clock wins. Record **plan shape**, **examined vs returned**, and **correctness**, not stopwatch time.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Fix one schema problem

**Do this:** Document `XBAD`’s string `price` (or another real defect you found). On `training_store_ops`, copy products and convert the bad price **or** quarantine the document. Do not silently rewrite historical orders.

**Expected result:** A before/after note exists. `training_store` catalog may stay unchanged; the ops copy shows the repaired type.

---

### Step 2 — Validation + monthly pipeline

**Do this:** Reuse or complete Lab 8.6 validation on `orders_validated`. Run your Lab 8.3/8.4 monthly paid-sales pipeline against `training_store.orders` and save the result documents.

**Expected result:** Validator rejects a bad insert. Pipeline output has month, order count, revenue, AOV, unique customers, units sold.

---

### Step 3 — Indexes and explain

**Do this:** Ensure at least one history index and one paid-report index exist (create on `training_store` only if the instructor allows Day 3 leftovers). Explain the C101 history query and the pipeline `$match`. Record IXSCAN vs COLLSCAN.

**Expected result:** Two explain summaries are in the notes. Overlap is mentioned if both indexes share a prefix.

---

### Step 4 — Ops pack

**Do this:** In one page: least-privilege table (app vs report vs admin); RPO/RTO for orders; three critical alerts; one runbook (backup failed or no primary); checklist scores for the six production-readiness areas.

**Expected result:** The page is complete. Classification is Ready with conditions or Not ready, with evidence. No production-ready claim without auth, tested restore, and restricted network.

---

## Production-readiness checklist (score each)

| Area | Ready / Conditional / Not ready | Evidence |
|------|----------------------------------|----------|
| Data model | | |
| Queries and indexes | | |
| Security | | |
| Availability and scalability | | |
| Backup and recovery | | |
| Monitoring and operations | | |

**Overall:** Production-ready / Ready with conditions / Not production-ready

## Success criteria

- [ ] One schema defect is repaired in a scratch space
- [ ] Validation and monthly pipeline evidence exist
- [ ] Explains are recorded
- [ ] Ops pack includes alerts, runbook, and checklist

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

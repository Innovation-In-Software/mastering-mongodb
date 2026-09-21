# Lab 8.9: Backup and Restore Verification

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 30 min  
**Difficulty:** Intermediate

**Objective:** Record source counts and sample ids, take an approved backup, restore to an isolated database, verify documents and indexes, and compare duration to a stated RTO.

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

### Step 1 — Record the source

**Do this:** In notes: `db.orders.countDocuments()`, `db.products.countDocuments()`, three `orderNumber` values, and `db.orders.getIndexes()`. Use `training_store`.

**Expected result:** Counts match the loader (about 17 orders, 13 products) unless the class mutated data — write the actual numbers. Three order numbers and index names are recorded.

---

### Step 2 — Take a backup

**Do this:** From the course repo in PowerShell (MongoDB Database Tools must be on PATH), run:

```text
New-Item -ItemType Directory -Force -Path .\datasets\backups | Out-Null
mongodump --uri="mongodb://localhost:27017" --db=training_store --out=".\datasets\backups\lab89"
```
If `mongodump` is not installed, use Compass export of `orders` and `products` JSON into `datasets/backups/lab89` and note that it is a logical export, not a full physical snapshot.

**Expected result:** A dump directory (or JSON export) exists. The command finished without authentication errors (or the instructor supplied a URI).

---

### Step 3 — Restore isolated and verify

**Do this:** Restore into a **new** database name:

```text
mongorestore --uri="mongodb://localhost:27017" --nsFrom="training_store.*" --nsTo="training_store_restore.*" --drop ".\datasets\backups\lab89\training_store"
```
Then in `mongosh`: compare counts, `find` one recorded `orderNumber`, and `getIndexes()` on `training_store_restore.orders`. Record start/end time. Do not restore over `training_store`.

**Expected result:** Counts match the source note. Sample order exists. Indexes are present (rebuild may apply for some logical imports). Elapsed time is written and compared to a classroom RTO such as 30 minutes.

---

## RPO / RTO for this lab

Assume classroom targets: **RPO = since last dump** (here: minutes, because you dumped just now) and **RTO = 30 minutes**. If restore exceeded 30 minutes, the procedure failed the RTO even if data looks correct.

Atlas users: take a snapshot in a disposable project or follow the instructor’s restore-to-new-cluster path. Still verify counts and sample ids.

## Success criteria

- [ ] Source counts and sample ids are written before backup
- [ ] Restore target is not `training_store`
- [ ] Verification includes counts, a sample document, and indexes

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

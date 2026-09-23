# Lab 8.5: Index Design and Validation

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Identify query shapes for the sales report and application queries, propose a small index set, create training indexes, and compare explain examined vs returned counts.

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

### Step 1 — List current indexes

**Do this:** Run `db.orders.getIndexes()`, `db.products.getIndexes()`, and `db.reviews.getIndexes()`. Note leftovers from Module 6.

**Expected result:** A written inventory exists. `_id_` is present. Extra indexes from Day 3 morning are labeled, not blindly dropped.

---

### Step 2 — Create or reuse two useful indexes

**Do this:** If missing, create training indexes (names optional):

```javascript
db.orders.createIndex(
  { customerId: 1, paymentStatus: 1, createdAt: -1 },
  { name: "ix_orders_cust_pay_date" }
)
db.orders.createIndex(
  { paymentStatus: 1, createdAt: -1 },
  { name: "ix_orders_pay_date" }
)
```
Explain the C101 paid-history query and the paid `$match` of the monthly report.

**Expected result:** Winning plans show IXSCAN (unless a better leftover index wins). Examined counts are written down. Prefix overlap between the two new indexes is noted.

---

### Step 3 — Overlap decision

**Do this:** State whether both new indexes should survive in production, or whether one prefix makes the other a hide candidate. Do **not** drop indexes in this lab.

**Expected result:** A sentence exists: keep both only if both query shapes are hot; otherwise hide the redundant one after monitoring. No `dropIndex` in this lab.

---

## Success criteria

- [ ] Index inventory is written
- [ ] Two explains are recorded after index creation
- [ ] No index is dropped

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

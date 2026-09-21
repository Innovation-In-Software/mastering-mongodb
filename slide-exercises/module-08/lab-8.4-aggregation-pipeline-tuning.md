# Lab 8.4: Aggregation Pipeline Tuning

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Capture an inefficient pipeline’s output and explain stats, then filter earlier, drop unused fields, control $unwind, review $lookup, and confirm identical business results.

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

### Step 1 — Run the slow shape

**Do this:** Run this inefficient pipeline once and save the result documents plus `explain("executionStats")` notes (stage order, docs leaving `$lookup`):

```javascript
db.orders.aggregate([
  { $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer"
  }},
  { $unwind: "$items" },
  { $match: { paymentStatus: "PAID" } },
  { $group: { _id: "$customer.name.full", revenue: { $sum: "$total" } } }
])
```

**Expected result:** Lookup and unwind run on unpaid orders too. Revenue is inflated where orders have multiple items. Record the output even if the numbers look ‘busy’.

---

### Step 2 — Rewrite and compare

**Do this:** Rewrite: `$match` PAID first, `$project` only fields you need, `$group` by `customerId` summing `$total` **without** unwinding, then `$lookup` names, then `$sort`. Compare revenue to a manual `find` of paid totals for C101.

**Expected result:** C101’s paid `total` sum matches the grouped revenue. Unpaid orders never enter `$lookup`. Explain shows a smaller working set after `$match`.

---

### Step 3 — Index recommendation

**Do this:** Write whether `{ paymentStatus: 1, createdAt: -1 }` (or `{ paymentStatus: 1 }`) would help this pipeline’s `$match`, and whether a `$lookup` on `customers._id` already has an index.

**Expected result:** `_id` is already indexed. A `paymentStatus` (and optional date) index can support the early `$match`. Do not index every grouped field.

---

## Success criteria

- [ ] Before and after outputs are recorded
- [ ] Early `$match` is in the rewrite
- [ ] C101 revenue is checked against a manual sum

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

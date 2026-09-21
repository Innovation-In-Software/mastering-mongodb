# Lab 6.9: Tune an Aggregation Pipeline

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Index an early $match/$sort on paid orders, then explain which later stages still run in memory.

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

**Small-data note:** Twelve products and seventeen orders will not produce dramatic wall-clock wins. Record the **plan** (`COLLSCAN` vs `IXSCAN`), **index name**, and **examined vs returned** counts. That is the teaching signal.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Baseline pipeline explain

**Do this:** Run:

```javascript
db.orders.explain("executionStats").aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $sort: { createdAt: -1 } },
  { $group: {
      _id: "$fulfillmentStatus",
      revenue: { $sum: "$total" },
      orderCount: { $sum: 1 }
  }}
])
```

**Expected result:** Record whether $match/$sort used COLLSCAN and whether a sort stage appears. Do not expect $group to use an index.

---

### Step 2 — Create a supporting index

**Do this:** Run:

```javascript
db.orders.createIndex(
  { paymentStatus: 1, createdAt: -1 },
  { name: "idx_orders_payment_created" }
)
```
Re-explain the same pipeline.

**Expected result:** Winning plan for the cursor should show IXSCAN on idx_orders_payment_created for the match/sort prefix.

---

### Step 3 — Compare statistics

**Do this:** Compare totalDocsExamined / keys examined before and after. Note nReturned from the group (number of fulfillment statuses).

**Expected result:** Examined counts should drop or the stage should switch from COLLSCAN to IXSCAN. Group output still has a few buckets (SHIPPED, DELIVERED, and similar).

---

### Step 4 — Explain remaining memory work

**Do this:** Write which stages still cannot be served by this index.

**Expected result:** $group (and accumulators) still process documents in the pipeline after the indexed match/sort. Indexing does not remove grouping work.

---



## Success criteria

- [ ] Baseline and post-index explains exist
- [ ] idx_orders_payment_created is used for $match/$sort
- [ ] $group is identified as remaining in-memory work

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

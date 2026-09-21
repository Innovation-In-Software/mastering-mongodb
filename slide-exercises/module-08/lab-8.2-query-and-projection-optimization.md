# Lab 8.2: Query and Projection Optimization

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Tighten assigned application queries with filters, correct BSON types, projection, stable sort, limit, explain output, and index recommendations.

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

### Step 1 — Baseline the broad query

**Do this:** Run and record nReturned and totalDocsExamined:

```javascript
use training_store
db.orders.find({}).explain("executionStats")
```

**Expected result:** The plan examines every order. nReturned equals the collection size. This is the ‘return everything’ anti-pattern.

---

### Step 2 — Add filter, projection, sort, and limit

**Do this:** Look up C101’s `_id`, then run:

```javascript
const c101 = db.customers.findOne({ customerNumber: "C101" })._id
db.orders.find(
  { customerId: c101, paymentStatus: "PAID" },
  { _id: 0, orderNumber: 1, fulfillmentStatus: 1, total: 1, createdAt: 1 }
).sort({ createdAt: -1 }).limit(10)
```

**Expected result:** Only C101 paid orders, shaped fields, newest first, at most ten documents.

---

### Step 3 — Explain and recommend an index

**Do this:** Run `.explain("executionStats")` on the improved query. Record winning stage, docs examined, and whether a SORT stage appears. Write one candidate index.

**Expected result:** Likely COLLSCAN on this small set unless Module 6 indexes remain. Candidate `{ customerId: 1, paymentStatus: 1, createdAt: -1 }`. Note examined vs returned.

---

## Success criteria

- [ ] Broad find({}) baseline is recorded
- [ ] Improved query uses filter, projection, sort, and limit
- [ ] An ESR-style index is recommended

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

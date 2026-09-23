# Lab 5.9: Pipeline Performance Review

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.7)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Compare `explain` output before and after an early `$match` and name a supporting index.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

Use the same connection string from Module 2. **Dataset:** `use training_store`.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Explain a late filter

**Do this:** Run:

```javascript
db.orders.explain("executionStats").aggregate([
  { $sort: { createdAt: -1 } },
  { $match: { paymentStatus: "PAID" } }
])
```

**Expected result:** Note COLLSCAN or a sort that examines all 17 orders, then filters. Record documents examined.

---

### Step 2 — Move `$match` earlier and compare

**Do this:** Run:

```javascript
db.orders.explain("executionStats").aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $sort: { createdAt: -1 } }
])
```

Write one index you would add in Module 6, for example `{ paymentStatus: 1, createdAt: -1 }`. Do not treat this small set as a load test — you are reading the plan shape.

**Expected result:** The plan still may scan on this tiny collection. The teaching point is stage order plus a future compound index, not milliseconds.

---

## Success criteria

- [ ] You captured `executionStats` for both pipelines
- [ ] `$match` is earlier in the revised pipeline
- [ ] You named a supporting index without inventing a second dataset

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

# Lab 5.10: Integrated Aggregation Challenge

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.8)  
**Time:** 40 min  
**Difficulty:** Intermediate

**Objective:** Build a monthly e-commerce performance report using `$match`, `$set` or `$project`, `$unwind`, `$group`, `$sort`, `$limit`, and `$facet` or `$lookup`.

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

## Required output per month

- Reporting month
- Paid-order count
- Total revenue
- Average order value
- Unique customer count
- Units sold
- Top product by revenue
- Revenue by fulfillment status

Use at least: `$match`, `$set` or `$project`, `$unwind`, `$group`, `$sort`, `$limit`, and `$facet` or `$lookup`.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Monthly core metrics

**Do this:** Start with paid orders, attach a `YYYY-MM` key, and `$facet` (or two pipelines) so one branch groups month-level totals and another unwinds items.

A workable month total branch:

```javascript
{
  $group: {
    _id: "$month",
    paidOrderCount: { $sum: 1 },
    totalRevenue: { $sum: "$total" },
    averageOrderValue: { $avg: "$total" },
    uniqueCustomers: { $addToSet: "$customerId" }
  }
}
```

Then `$size` the `uniqueCustomers` array in a later `$set`.

**Expected result:** Three months. Unique customer counts are at least 1. September includes more paid orders than July.

---

### Step 2 — Units, top product, and status revenue

**Do this:** In other facet branches, unwind items for units and top SKU, and group fulfillment status. Sort months ascending. Keep a copy of the pipeline and one sample output document.

**Expected result:** You used every required stage at least once. Manual check: July paid orders are O6101–O6103.

---

### Step 3 — Recommend an index

**Do this:** Write one index that would support the opening `$match` plus a date sort or range, for Module 6.

**Expected result:** Example: `{ paymentStatus: 1, createdAt: 1 }`.

---

## Success criteria

- [ ] Required stages are all present
- [ ] Sample output is saved
- [ ] One month was validated by hand
- [ ] One supporting index is named

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

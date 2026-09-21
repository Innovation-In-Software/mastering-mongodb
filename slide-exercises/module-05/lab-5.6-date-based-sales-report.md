# Lab 5.6: Date-Based Sales Report

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.6)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Group paid orders by calendar month with count, revenue, and average order value.

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

### Step 1 — Month key and metrics

**Do this:** Run:

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  {
    $set: {
      month: {
        $dateToString: { format: "%Y-%m", date: "$createdAt" }
      }
    }
  },
  {
    $group: {
      _id: "$month",
      orderCount: { $sum: 1 },
      revenue: { $sum: "$total" },
      averageOrderValue: { $avg: "$total" }
    }
  },
  { $sort: { _id: 1 } },
  {
    $project: {
      _id: 0,
      reportingMonth: "$_id",
      orderCount: 1,
      revenue: 1,
      averageOrderValue: 1
    }
  }
])
```

**Expected result:** Three rows: `2026-07`, `2026-08`, `2026-09` in that order.

---

### Step 2 — Optional time zone

**Do this:** Change `$dateToString` to include `timezone: "America/Toronto"` and compare whether any order moves month versus UTC.

**Expected result:** You can explain that production reports must name a time zone. On this dataset most orders stay in the same calendar month.

---

## Success criteria

- [ ] Months sort chronologically as strings `YYYY-MM`
- [ ] Pending O5001 is excluded
- [ ] You can state why timezone matters

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

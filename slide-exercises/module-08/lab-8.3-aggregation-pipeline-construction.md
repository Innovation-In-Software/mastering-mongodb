# Lab 8.3: Aggregation Pipeline Construction

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 30 min  
**Difficulty:** Intermediate

**Objective:** Build a monthly paid-sales report with month, order count, revenue, average order value, unique customers, and units sold using $match, $set or $project, $unwind, $group, $sort, and a final $project.

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

### Step 1 — Filter and stamp the month

**Do this:** Start a pipeline that matches `paymentStatus: "PAID"` and sets `month` from `createdAt` (UTC date-to-string `YYYY-MM` is acceptable in training).

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $set: { month: { $dateToString: { format: "%Y-%m", date: "$createdAt" } } } }
])
```

**Expected result:** About 13 paid orders remain. Each document has a `month` such as `2026-07`.

---

### Step 2 — Unwind safely, then group twice

**Do this:** Unwind `items`, group by `{ month: "$month", orderNumber: "$orderNumber" }` keeping `total` with `$first`, `customerId` with `$first`, and `units` as `$sum` of `$items.quantity`. Then group by month: `orderCount: { $sum: 1 }`, `revenue: { $sum: "$total" }`, `uniqueCustomers: { $addToSet: "$customerId" }`, `unitsSold: { $sum: "$units" }`.

**Expected result:** Revenue is not multiplied by line count. Units come from item quantities. July–September 2026 months appear.

---

### Step 3 — Sort and shape

**Do this:** Add `$set` for `uniqueCustomerCount: { $size: "$uniqueCustomers" }` and `averageOrderValue: { $divide: ["$revenue", "$orderCount"] }`, `$sort` by `_id` / month, and a final `$project` that outputs month, orderCount, revenue, averageOrderValue, uniqueCustomers, unitsSold.

**Expected result:** One document per month, sorted, with all six business metrics. No leftover `_id` object unless you alias it to `month`.

---

## Why two `$group` stages?

`$unwind` turns one order with three items into three documents. Summing the parent `total` there counts the order three times. Grouping back to one row per order (or summing only line-level quantity and line revenue) keeps the arithmetic honest.

## Success criteria

- [ ] Required stages are present
- [ ] Revenue is not double-counted after `$unwind`
- [ ] Report includes unique customers and units sold

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

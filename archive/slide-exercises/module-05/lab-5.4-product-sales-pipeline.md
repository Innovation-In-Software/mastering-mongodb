# Lab 5.4: Product Sales Pipeline

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.4)  
**Time:** 30 min  
**Difficulty:** Intermediate

**Objective:** Unwind paid items, compute line revenue, and return the top five SKUs by revenue.

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

### Step 1 — Paid, unwind, line revenue, group

**Do this:** Run:

```javascript
db.orders.aggregate([
  { $match: { paymentStatus: "PAID" } },
  { $unwind: "$items" },
  {
    $set: {
      lineRevenue: { $multiply: ["$items.quantity", "$items.unitPrice"] }
    }
  },
  {
    $group: {
      _id: "$items.sku",
      unitsSold: { $sum: "$items.quantity" },
      revenue: { $sum: "$lineRevenue" },
      orderCount: { $sum: 1 }
    }
  },
  { $sort: { revenue: -1 } },
  { $limit: 5 }
])
```

**Expected result:** Top five start with L110, then L100, then A500. Units for L110 are 2.

---

### Step 2 — Explain orderCount

**Do this:** State whether `$sum: 1` is order count or line count. This dataset does not repeat a SKU inside one order.

**Expected result:** Here it equals the number of paid orders that contain the SKU. If duplicates were allowed, you would `$addToSet` `orderNumber` and take `$size`.

---

## Success criteria

- [ ] Line revenue is after `$unwind`
- [ ] Top SKU is L110
- [ ] Five documents returned

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

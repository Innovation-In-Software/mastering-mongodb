# Exercise 5.4: Create Calculated Fields

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.2)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Add line revenue, shipping-safe totals, full names, value class, and reporting month.

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

### Step 1 — Line revenue and total with shipping

**Do this:** Run:

```javascript
db.orders.aggregate([
  { $match: { orderNumber: "O6301" } },
  { $unwind: "$items" },
  {
    $set: {
      lineRevenue: { $multiply: ["$items.quantity", "$items.unitPrice"] },
      shippingFeeSafe: { $ifNull: ["$shippingFee", Decimal128("0.00")] }
    }
  },
  {
    $set: {
      totalWithShipping: { $add: ["$subtotal", "$tax", "$shippingFeeSafe"] }
    }
  },
  { $project: { orderNumber: 1, "items.sku": 1, lineRevenue: 1, totalWithShipping: 1 } }
])
```

**Expected result:** Two item documents for O6301. Line revenues `1299.99` and `24.99`. `totalWithShipping` matches stored total `1512.23`.

---

### Step 2 — Name, class, and month

**Do this:** Run:

```javascript
db.customers.aggregate([
  {
    $project: {
      _id: 0,
      customerNumber: 1,
      customerName: { $concat: ["$name.first", " ", "$name.last"] }
    }
  }
])
db.orders.aggregate([
  { $match: { orderNumber: { $in: ["O6201", "O6202"] } } },
  {
    $set: {
      orderSize: {
        $cond: [
          { $gte: ["$total", Decimal128("1000.00")] },
          "HIGH_VALUE",
          "STANDARD"
        ]
      },
      orderMonth: {
        $dateToString: { format: "%Y-%m", date: "$createdAt" }
      }
    }
  },
  { $project: { _id: 0, orderNumber: 1, total: 1, orderSize: 1, orderMonth: 1 } }
])
```

**Expected result:** Full names such as Aisha Khan. O6201 is `STANDARD` in `2026-08`; O6202 is `HIGH_VALUE` in `2026-08`.

---

## Success criteria

- [ ] Line revenue uses quantity × unitPrice after unwind
- [ ] `$ifNull` covers missing `shippingFee`
- [ ] `HIGH_VALUE` uses Decimal128 `1000.00`

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

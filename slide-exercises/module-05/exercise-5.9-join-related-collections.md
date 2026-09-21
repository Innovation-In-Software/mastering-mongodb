# Exercise 5.9: Join Related Collections

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.5)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Lookup customers from orders, format names, sort by total, and keep unmatched orders.

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

### Step 1 — Join and flatten matches

**Do this:** Run:

```javascript
db.orders.aggregate([
  {
    $lookup: {
      from: "customers",
      localField: "customerId",
      foreignField: "_id",
      as: "customer"
    }
  },
  {
    $unwind: {
      path: "$customer",
      preserveNullAndEmptyArrays: true
    }
  },
  {
    $project: {
      _id: 0,
      orderNumber: 1,
      total: 1,
      customerNumber: "$customer.customerNumber",
      customerName: {
        $concat: ["$customer.name.first", " ", "$customer.name.last"]
      }
    }
  },
  { $sort: { total: -1 } }
])
```

**Expected result:** Most rows show a customer number and full name. Totals sort descending.

---

### Step 2 — Find the unmatched order

**Do this:** Scan for a document whose `customerNumber` is missing. Confirm its `orderNumber`.

**Expected result:** O6499 has an empty lookup array. Because `preserveNullAndEmptyArrays` is true, it still appears.

---

## Success criteria

- [ ] `$lookup` output is treated as an array
- [ ] Unmatched O6499 is not dropped
- [ ] Sort is on order total, not customer name

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

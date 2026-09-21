# Lab 5.7: Price-Band Analysis

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.6)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Bucket products into price bands with count, average price, and product names.

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

### Step 1 — Define business boundaries

**Do this:** Run:

```javascript
db.products.aggregate([
  {
    $bucket: {
      groupBy: "$price",
      boundaries: [0, 50, 100, 500, 2000],
      default: "Other",
      output: {
        productCount: { $sum: 1 },
        averagePrice: { $avg: "$price" },
        productNames: { $push: "$name" }
      }
    }
  }
])
```

**Expected result:** Four buckets. Under 50 includes USB Hub, Wireless Mouse, Query Cookbook, Clearance Shoe, Wireless Keyboard. L190 (`499.99`) is in 100–500, not 500–2000.

---

### Step 2 — State the boundary rule

**Do this:** Write whether a price of exactly 50 belongs to under-50 or 50–100.

**Expected result:** It enters the bucket whose lower bound is 50. Lower bound inclusive, upper bound exclusive.

---

## Success criteria

- [ ] `boundaries` match the business bands
- [ ] Names are collected with `$push`
- [ ] You can explain inclusive lower bounds

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

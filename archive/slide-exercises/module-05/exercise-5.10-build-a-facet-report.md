# Exercise 5.10: Build a $facet Report

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.5)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Return one document with product totals, category counts, average price, price bands, and top expensive products.

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

### Step 1 — Build five facets

**Do this:** Run:

```javascript
db.products.aggregate([
  {
    $facet: {
      totals: [{ $count: "totalProducts" }],
      byCategory: [{ $sortByCount: "$category" }],
      averagePrice: [
        { $group: { _id: null, averagePrice: { $avg: "$price" } } }
      ],
      priceBands: [
        {
          $bucket: {
            groupBy: "$price",
            boundaries: [0, 50, 100, 500, 2000],
            default: "Other",
            output: { productCount: { $sum: 1 } }
          }
        }
      ],
      mostExpensive: [
        { $sort: { price: -1, sku: 1 } },
        { $limit: 5 },
        { $project: { _id: 0, sku: 1, name: 1, price: 1 } }
      ]
    }
  }
])
```

**Expected result:** Exactly one document. `totals` is an array with 12. `mostExpensive` starts with L110.

---

### Step 2 — Read each array

**Do this:** For each facet key, state whether the array holds one summary or many rows.

**Expected result:** `totals` and `averagePrice` are one-element arrays. `byCategory`, `priceBands`, and `mostExpensive` have several.

---

## Success criteria

- [ ] Output is one document, not twelve
- [ ] Each facet is an array
- [ ] Price bands use the stated boundaries

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

# Exercise 5.5: Group and Calculate Totals

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.3)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Group active products by category and compute count, average, min, and max price.

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

### Step 1 — Group active products

**Do this:** Run:

```javascript
db.products.aggregate([
  { $match: { active: true } },
  {
    $group: {
      _id: "$category",
      productCount: { $sum: 1 },
      averagePrice: { $avg: "$price" },
      minimumPrice: { $min: "$price" },
      maximumPrice: { $max: "$price" }
    }
  }
])
```

**Expected result:** Four groups. LAPTOP count 2 (`L190` is inactive). ACCESSORY count 4. SHOE 3. BOOK 2.

---

### Step 2 — Sort by average price

**Do this:** Add `{ $sort: { averagePrice: -1 } }` as the last stage and rerun.

**Expected result:** LAPTOP first (highest average), then ACCESSORY, SHOE, BOOK.

---

## Success criteria

- [ ] Inactive `L190` is excluded
- [ ] `$sum: 1` counts documents, not prices
- [ ] Sort is on the grouped metric, not the original price field

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

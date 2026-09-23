# Lab 5.2: Product Summary Pipeline

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.3)  
**Time:** 25 min  
**Difficulty:** Beginner

**Objective:** Build a category report of active products with count, average, min, and max price.

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

### Step 1 — Filter and group

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

**Expected result:** Four categories. LAPTOP count is 2.

---

### Step 2 — Sort and rename

**Do this:** Add these stages and rerun the full pipeline:

```javascript
  { $sort: { averagePrice: -1 } },
  {
    $project: {
      _id: 0,
      category: "$_id",
      productCount: 1,
      averagePrice: 1,
      minimumPrice: 1,
      maximumPrice: 1
    }
  }
```

**Expected result:** LAPTOP is first. Output field is `category`, not `_id`.

---

## Success criteria

- [ ] Inactive products are excluded
- [ ] Average, min, and max are present
- [ ] Final documents are report-shaped

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

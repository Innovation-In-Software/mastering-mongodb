# Exercise 5.3: Reshape Documents with $project

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.2)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Rename product fields and build a nested report document without `_id`.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

Use the same connection string from Module 2. **Dataset:** `use training_store`. Reload `load.js` if counts are far below 6 / 12 / 17 / 6.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Flat renamed projection

**Do this:** Run:

```javascript
db.products.aggregate([
  {
    $project: {
      _id: 0,
      productCode: "$sku",
      productName: "$name",
      category: 1,
      sellingPrice: "$price"
    }
  }
])
```

**Expected result:** Twelve documents. Fields are `productCode`, `productName`, `category`, `sellingPrice`. No `_id`.

---

### Step 2 — Nested output

**Do this:** Run:

```javascript
db.products.aggregate([
  { $match: { sku: "L100" } },
  {
    $project: {
      _id: 0,
      product: { code: "$sku", name: "$name" },
      pricing: { amount: "$price" }
    }
  }
])
```

**Expected result:** One document: `product.code` is `L100`, `pricing.amount` is Decimal128 `1299.99`.

---

## Success criteria

- [ ] Renames use the `$field` prefix
- [ ] Nested projection builds objects, not dotted key names as output
- [ ] `_id` is omitted from the report shape

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

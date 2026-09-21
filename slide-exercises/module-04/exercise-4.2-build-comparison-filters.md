# Exercise 4.2: Build Comparison Filters

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Write `$gt`, `$gte`, `$lte`, range, and `$nin` filters using Decimal128 for money.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

**Prerequisite:** `training_store` is loaded from [`datasets/training_store/load.js`](../../datasets/training_store/load.js). If writes from an earlier lab remain, reload that script unless the exercise says otherwise.

```javascript
use training_store
```


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Products priced above 100

**Do this:** Run:

```javascript
db.products.find({ price: { $gt: Decimal128("100.00") } })
```

**Expected result:** Laptops and `S200` appear. `XBAD` does not — its price is a string, not Decimal128.

---

### Step 2 — Products priced between 50 and 500

**Do this:** Run:

```javascript
db.products.find({
  price: {
    $gte: Decimal128("50.00"),
    $lte: Decimal128("500.00")
  }
})
```

**Expected result:** Includes `S200`, `S210`, `A400`, and similar mid-range items. Both bounds are inclusive.

---

### Step 3 — Orders with totals above 1,000

**Do this:** Run:

```javascript
db.orders.find({ total: { $gt: Decimal128("1000.00") } })
```

**Expected result:** `O5001` and `O6401` match (both contain L100 and have totals above 1,000). Paid high-value orders such as `O6101` also match.

---

### Step 4 — Reviews rated at least 4

**Do this:** Run:

```javascript
db.reviews.find({ rating: { $gte: 4 } })
```

**Expected result:** Five reviews match. The rating-3 review of `P1001` does not.

---

### Step 5 — Products outside LAPTOP and SHOE

**Do this:** Run:

```javascript
db.products.find({ category: { $nin: ["LAPTOP", "SHOE"] } })
```

**Expected result:** Books and accessories remain, including the legacy `XBAD` document.

---



## Success criteria

- [ ] Used Decimal128 for money comparisons
- [ ] Explained why `XBAD` misses numeric price queries
- [ ] Used `$nin` on one field rather than two `$ne` clauses without need

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

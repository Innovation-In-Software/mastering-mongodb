# Exercise 5.2: Build a $match Stage

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.2)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Write `$match` stages for paid orders, high-value orders, active products, review dates, and customer provinces.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

Use the same connection string from Module 2. **Dataset:** `use training_store`. If counts are far below 6 customers / 12 products / 17 orders / 6 reviews, reload [`datasets/training_store/load.js`](../../datasets/training_store/load.js).

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Paid and high-value paid orders

**Do this:** Run:

```javascript
db.orders.aggregate([{ $match: { paymentStatus: "PAID" } }])
db.orders.aggregate([
  {
    $match: {
      paymentStatus: "PAID",
      total: { $gte: Decimal128("1000.00") }
    }
  }
])
```

**Expected result:** First pipeline: 13 documents. Second: four high-value paid orders (O6101, O6202, O6301, O6304).

---

### Step 2 — Products, reviews, and provinces

**Do this:** Run:

```javascript
db.products.aggregate([
  {
    $match: {
      active: true,
      category: { $in: ["LAPTOP", "ACCESSORY"] }
    }
  }
])
db.reviews.aggregate([
  {
    $match: {
      createdAt: {
        $gte: ISODate("2026-08-01T00:00:00Z"),
        $lt: ISODate("2026-09-01T00:00:00Z")
      }
    }
  }
])
db.customers.aggregate([
  { $match: { "addresses.province": { $in: ["Ontario", "Quebec"] } } }
])
```

**Expected result:** Laptops plus accessories that are active; August reviews; customers whose nested address province is Ontario or Quebec (including inactive C515).

---

## Success criteria

- [ ] Paid-order `$match` returns 13 documents
- [ ] High-value filter uses Decimal128, not a Double
- [ ] Province filter uses the dotted path `addresses.province`

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

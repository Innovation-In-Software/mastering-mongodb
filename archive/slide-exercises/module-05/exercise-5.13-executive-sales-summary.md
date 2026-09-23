# Exercise 5.13: Executive Sales Summary

**Module 5:** The Aggregation Framework  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 5, Lesson 5.8)  
**Time:** 30–45 min  
**Difficulty:** Intermediate

**Objective:** Produce a date-bounded executive report covering revenue, monthly trend, products, customers, categories, and price bands.

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

## Business request

For paid activity in **2026-07-01 through 2026-09-30** (inclusive start, exclusive end `2026-10-01`), report:

1. Total paid revenue
2. Number of paid orders
3. Average order value
4. Revenue by month
5. Revenue by product
6. Top five customers
7. Product count by category (catalog, not sales)
8. Price-band distribution (catalog)

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Choose collections and the date filter

**Do this:** Orders drive items 1–6. Products drive 7–8. Write the `$match` on `createdAt` and `paymentStatus`.

**Expected result:** Date range uses ISODate bounds. Pending orders are excluded.

---

### Step 2 — Build and structure the output

**Do this:** Use `$facet` so one aggregate call returns the metrics. Join customer names only on the top-customer branch. Handle missing `shippingFee` if you add it into a calculation. Explain stage order in three sentences.

**Expected result:** One result document (or a small set of clearly named documents). Top product L110. Top customer C101. You named likely indexes: `paymentStatus+createdAt`, and perhaps `sku`.

---

## Evaluation criteria

- Correct source documents
- Correct stage order
- Accurate calculations
- Appropriate array handling
- Clear output fields
- Missing values handled
- Reasonable performance decisions

## Success criteria

- [ ] Date-range `$match` is first on the order branches
- [ ] `$lookup` is not applied to every order unless needed
- [ ] You can defend stage order and one index

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

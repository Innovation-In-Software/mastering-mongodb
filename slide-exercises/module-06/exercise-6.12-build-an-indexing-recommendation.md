# Exercise 6.12: Build an Indexing Recommendation

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Write a short recommendation for one training_store query shape with validation and rollback.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may use `mongosh` to test ideas, but reasoning is the deliverable. You do not need to create production indexes during discussion exercises.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Fill the template

**Do this:** Pick the catalog query (active products in a category, sorted by price) or customer order history. Write: query shape, current plan assumption, proposed index, expected improvement, write/storage cost.

**Expected result:** A complete paragraph or bullet list covering those five items. Example: `{ category: 1, active: 1, price: 1 }` named `idx_products_category_active_price`.

---

### Step 2 — Validation and rollback

**Do this:** Add a validation procedure (explain before/after, examined counts) and a rollback procedure (dropIndex of the named index; keep the createIndex snippet).

**Expected result:** Baseline explain → createIndex → explain again → compare nReturned vs keys/docs examined and SORT absence. Rollback: `db.products.dropIndex("idx_products_category_active_price")`.

---



## Success criteria

- [ ] One query shape is specified
- [ ] Field order is justified
- [ ] Write cost and rollback are included

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

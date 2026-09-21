# Exercise 3.6: Find and Correct Schema Anti-Patterns

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.4)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Identify anti-patterns in a flawed product document and rewrite it with correct types, a bounded relationship, and a Date.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | Instructor clocks this | Stay on the slide timer |

You do **not** need MongoDB running for this exercise.

---

## Flawed document

```javascript
{
  productId: "P1001",
  price: "49.99",
  isActive: "yes",
  allReviews: [
    // unlimited growth
  ],
  created: "September 20, 2026"
}
```

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Name the problems

**Do this:** List every issue you can see: types, growth, naming, identifier strategy.

**Expected result:** Price stored as a string; Boolean stored as text; unbounded `allReviews` array; nonstandard date string; identifier is `productId` rather than `_id` or `sku` with a stated convention.

---

### Step 2 — Rewrite the document

**Do this:** Produce a corrected document. Move reviews out (reference). Use Decimal128, Boolean, Date, and a clear `_id`/`sku` convention.

**Expected result:** Something like `sku`/`_id`, `price: Decimal128("49.99")`, `active: true`, `createdAt: ISODate(...)`, and **no** `allReviews` array.

---

## Success criteria

- [ ] At least four anti-patterns named
- [ ] Corrected types for money, Boolean, and date
- [ ] Reviews are not an unbounded embedded array


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

# Exercise 3.2: Discover Application Access Patterns

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.2)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Turn e-commerce requirements into access patterns: frequency, data returned together, and a modeling implication.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | Instructor clocks this | Stay on the slide timer |

You do **not** need MongoDB running for this exercise.

---

## Scenario

The application must support product search, product-detail pages, customer profiles, order placement, order history, reviews, and inventory display.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — List the high-frequency reads

**Do this:** Name the three operations you expect to run most often. For each, write the data that must come back in one user-facing response.

**Expected result:** Typical high-frequency reads: find product by SKU (full product), retrieve order by order number (items, totals, address, status), load customer profile (name, contact, addresses). Inventory and review lists may be medium frequency.

---

### Step 2 — Fill the access-pattern table

**Do this:** Complete at least four rows:

| Access pattern | Frequency | Required data | Modeling implication |
|----------------|----------:|---------------|----------------------|
| Find product by SKU | High | Product details | Single product document |
| Retrieve order | High | Items, totals, address | Embed order aggregate |

Add rows for list-orders-for-customer, paginated reviews, and any snapshot you must preserve (purchase-time price).

**Expected result:** Each row names frequency, the fields returned together, and whether that implies embed, reference, or a snapshot.

---

## Success criteria

- [ ] At least four access patterns are listed
- [ ] “Data returned together” is specific, not “everything”
- [ ] At least one row says embed and one says reference


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

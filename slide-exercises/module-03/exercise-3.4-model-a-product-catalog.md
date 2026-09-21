# Exercise 3.4: Model a Product Catalog

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.3)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Create three product documents in one collection with a consistent core and category-specific attributes.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | Instructor clocks this | Stay on the slide timer |

You do **not** need MongoDB running for this exercise.

MongoDB is optional. Write JSON-like documents in a scratch file.

---

## Required common fields

SKU, name, description, category, price, active status, creation date.

### Type-specific fields

- **Laptop:** processor, memory, storage, screen size
- **Shoe:** size, color, material, gender category
- **Book:** author, ISBN, publisher, language

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Design the shared core

**Do this:** List the common field names and BSON types (`sku` string, `price` Decimal128, `active` Boolean, `createdAt` Date). Decide whether category-specific fields live at the top level or under `attributes`.

**Expected result:** One core field list used by all three products. You did not invent `productPrice` on one document and `price` on another.

---

### Step 2 — Write three documents

**Do this:** Draft one laptop, one shoe, and one book in the same `products` collection. Keep the core identical. Put type-specific data in `attributes` (or an equivalent nested object).

**Expected result:** Three documents that a later `find({ category: "LAPTOP" })` and `find({ "attributes.isbn": ... })` could use. Category-specific fields do not appear as required for every product.

---

## Success criteria

- [ ] Common fields use the same names and types
- [ ] Three categories exist in one collection
- [ ] Type-specific fields are nested or clearly optional


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

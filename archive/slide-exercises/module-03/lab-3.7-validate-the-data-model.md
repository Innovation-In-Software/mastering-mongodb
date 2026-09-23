# Lab 3.7: Validate the Data Model

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Review `training_store` against a maintainability and performance checklist before Day 2 querying.

**Prerequisite:** Module 2 — a working `mongosh` session. If `training_store` still holds the Module 1 starter documents, these labs **replace** that shape with the Day 2 application model.


---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | Instructor clocks this | Stay on the slide timer |

You do **not** need MongoDB running for this exercise.

Use `mongosh` only if you want to re-open a document while you check the list.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Check togetherness, growth, and types

**Do this:** For products, customers, and orders, answer: Are frequently accessed values stored together? Are arrays bounded? Are financial values Decimal128 (or noted)? Are timestamps Dates?

**Expected result:** Order items and shipping address are together. Customer `addresses` is bounded. Reviews are a separate collection. Prices are decimal. `createdAt` is a date.

---

### Step 2 — Check relationships, snapshots, and naming

**Do this:** Confirm embed vs reference is deliberate, purchase-time snapshots exist on the order, collection names are plural and consistent, field names are consistent, and the main queries from Exercise 3.2 can run. Note one improvement you would make later (index, extra field, or validation on `orders`).

**Expected result:** A completed checklist with at least one future improvement. You are ready for Module 4.

---

## Checklist

- [ ] Frequently accessed values stored together
- [ ] Arrays bounded
- [ ] Financial values stored appropriately
- [ ] Timestamps stored as dates
- [ ] Required fields identified
- [ ] Relationships deliberately embedded or referenced
- [ ] Historical snapshots preserved
- [ ] Collection names consistent
- [ ] Field names consistent
- [ ] Main application queries can be supported


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

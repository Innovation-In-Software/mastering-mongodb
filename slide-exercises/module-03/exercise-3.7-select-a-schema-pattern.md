# Exercise 3.7: Select a Schema Design Pattern

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.5)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Match seven modeling requirements to Attribute, Bucket, Subset, Computed, Extended reference, Outlier, or Polymorphic.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | Instructor clocks this | Stay on the slide timer |

You do **not** need MongoDB running for this exercise.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Match the first four requirements

**Do this:** Assign a pattern to:

- Sensor readings grouped by hour
- Latest three product reviews
- Stored average rating
- Dynamic product specifications

**Expected result:** Bucket, Subset, Computed, Attribute — in that order.

---

### Step 2 — Match the remaining three and debrief

**Do this:** Assign a pattern to:

- Customer name copied into an order
- Rare products with extremely high review volume
- Multiple product types in one collection

Compare with the instructor answer key.

**Expected result:** Extended reference, Outlier, Polymorphic. You can state one benefit and one tradeoff for any two patterns.

---

## Expected answers

| Requirement | Pattern |
|-------------|---------|
| Sensor readings grouped by hour | Bucket |
| Latest three product reviews | Subset |
| Stored average rating | Computed |
| Dynamic product specifications | Attribute |
| Customer name copied into an order | Extended reference |
| Rare products with extremely high review volume | Outlier |
| Multiple product types in one collection | Polymorphic |

---

## Success criteria

- [ ] Seven matches recorded
- [ ] You can explain Bucket vs one-document-per-event
- [ ] You can explain why Outlier exists


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

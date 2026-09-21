# Exercise 3.3: Embed or Reference?

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.3)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Choose embedding or referencing for eight relationships and justify each choice from ownership, cardinality, and growth.

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

### Step 1 — Decide relationships 1–4

**Do this:** For each, write Embed or Reference and a one-line why (ownership, size, or growth).

1. Customer’s primary contact information
2. Customer’s complete order history
3. Order line items
4. Product’s millions of reviews

**Expected result:** (1) Embed (2) Reference (3) Embed (4) Reference. The justification mentions bound vs unbounded, not only “it feels nested.”

---

### Step 2 — Decide relationships 5–8

**Do this:** Repeat for:

5. Employee’s office address
6. Blog post tags
7. Purchase-time product price
8. Account’s complete transaction history

Then compare with the instructor table.

**Expected result:** (5) Embed or reference depending on reuse across employees (6) Embed (7) Embed as a snapshot (8) Reference. You can explain why (5) is the only “it depends.”

---

## Expected direction

| Relationship | Likely choice |
|--------------|---------------|
| Primary contact information | Embed |
| Complete order history | Reference |
| Order line items | Embed |
| Millions of reviews | Reference |
| Office address | Embed or reference, depending on reuse |
| Blog post tags | Embed |
| Purchase-time price | Embed |
| Complete transaction history | Reference |

---

## Success criteria

- [ ] Eight rows have a choice and a reason
- [ ] Unbounded histories are referenced
- [ ] Purchase-time price is treated as a snapshot


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

# Exercise 6.2: Select Single or Compound Indexes

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Classify each requirement as a single-field index, a compound index, a specialized index, or not enough evidence.

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

### Step 1 — Classify four requirements

**Do this:** Classify: (A) lookup product by SKU, (B) active accessories sorted by price, (C) expire session documents, (D) a manager’s one-time ad-hoc count of all orders.

**Expected result:** A single-field unique. B compound. C specialized TTL. D no new index without evidence — one-time reporting is not a standing query shape.

---

### Step 2 — Justify one borderline case

**Do this:** Write two sentences on why a boolean `active` field is a poor standalone index but a useful compound or partial-index field.

**Expected result:** Low selectivity: most products are active, so `{ active: 1 }` barely narrows the scan. Combined with category (and optionally a partial filter) it supports the catalog shape.

---



## Success criteria

- [ ] Four classifications match the intended types
- [ ] The one-time query is not indexed by default
- [ ] Low-selectivity fields are justified only in context

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

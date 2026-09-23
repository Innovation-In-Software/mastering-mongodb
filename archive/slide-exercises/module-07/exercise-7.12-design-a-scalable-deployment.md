# Exercise 7.12: Design a Scalable Deployment

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Design availability, sharding, shard key, routing, and residency for a 24/7 order platform.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may inspect `training_store` or `rs.status()` to test ideas. Reasoning is the deliverable unless a step asks you to run a command.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Availability and placement

**Do this:** Specify replica-set size, failure-domain placement, and how Canada vs Europe data-residency could be met (zones vs separate clusters). Assume 24/7 order writes.

**Expected result:** At least three data-bearing voters across failure domains. Residency: zoned sharding on a residency field **or** separate regional clusters — not an afterthought on `createdAt`.

---

### Step 2 — Orders versus products

**Do this:** State which collection you shard first, a candidate order shard key, which queries stay targeted, and which monthly global reports become scatter-gather.

**Expected result:** Orders first under write growth. Products often wait. Targeted: customer/tenant order history. Scatter-gather: monthly global revenue unless pre-aggregated.

---

## Success criteria

- [ ] Standalone is rejected for production
- [ ] Residency is explicit
- [ ] Global reports are costed as scatter-gather or redesigned

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

# Exercise 6.5: Identify Index Prefixes

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** State which query prefixes a compound index can support directly.

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

### Step 1 — List usable prefixes

**Do this:** Given `{ customerId: 1, paymentStatus: 1, createdAt: -1 }`, list the prefixes MongoDB can use from the left.

**Expected result:** customerId; customerId + paymentStatus; customerId + paymentStatus + createdAt.

---

### Step 2 — Mark unsupported shapes

**Do this:** Decide whether these can use that index as a leading prefix: (1) filter only paymentStatus, (2) filter customerId, (3) filter customerId and sort createdAt without paymentStatus.

**Expected result:** (1) No — paymentStatus is not leading. (2) Yes. (3) Usually not for the sort: skipping paymentStatus breaks the sort prefix, so an extra SORT is likely.

---



## Success criteria

- [ ] Three prefixes are listed in left-to-right order
- [ ] A paymentStatus-only filter is not treated as supported
- [ ] Skipped-field sort is called out as a problem

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

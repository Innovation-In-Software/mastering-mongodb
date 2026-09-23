# Exercise 7.10: Compare Ranged and Hashed Sharding

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Evaluate ranged versus hashed sharding for equality, range queries, sequential writes, locality, even distribution, and operational complexity.

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

### Step 1 — Fill the comparison

**Do this:** For equality queries, range queries, sequential writes, geographic locality, even distribution, and operational complexity, mark which strategy is usually stronger (or “depends”).

**Expected result:** Equality: both can target. Range: ranged wins. Sequential writes: hashed usually spreads. Locality: ranged. Even distribution: hashed often easier. Complexity: similar conceptually; zones add complexity on ranged designs.

---

### Step 2 — Pick for this workload

**Do this:** Customer history by `customerId` plus newest-first `createdAt`, versus random UUID inserts with only equality lookups. Which strategy for each?

**Expected result:** History: ranged compound `{ customerId: 1, createdAt: 1 }`. UUID equality-only: hashed (or ranged UUID if already random).

---

## Success criteria

- [ ] Range queries are not claimed to be efficient on hashed keys
- [ ] Monotonic ranged keys are not recommended blindly
- [ ] Two workloads can justify two strategies

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

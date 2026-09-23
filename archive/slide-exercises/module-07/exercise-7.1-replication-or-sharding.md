# Exercise 7.1: Replication or Sharding?

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Choose replication, sharding, both, or neither yet for six architecture requirements.

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

### Step 1 — Classify six requirements

**Do this:** For each item, write **Replication**, **Sharding**, **Both**, or **Neither yet**: (1) survive one server failure, (2) increase total data capacity, (3) automatically elect a replacement primary, (4) distribute write load, (5) create a local development database, (6) provide production availability and scale.

**Expected result:** 1 Replication. 2 Sharding. 3 Replication. 4 Sharding. 5 Neither yet (standalone is enough). 6 Both (sharded replica sets).

---

### Step 2 — Defend one borderline case

**Do this:** In two sentences, explain why copying data to secondaries does **not** increase total storage capacity for the application dataset.

**Expected result:** Each member stores the same logical dataset. Extra members add redundancy, not a larger working set.

---

## Success criteria

- [ ] Six classifications match the intended mechanisms
- [ ] Local development is not forced into a replica set or shard
- [ ] Capacity is not confused with redundancy

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

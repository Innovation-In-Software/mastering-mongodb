# Exercise 6.10: Balance Read and Write Performance

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Plan how to investigate fourteen secondary indexes on a write-heavy (80/20) workload with rising insert latency.

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

### Step 1 — Evidence to collect

**Do this:** List the measurements you would gather before dropping anything.

**Expected result:** Insert/update latency and opcounters; index sizes (`collStats` / `indexSizes`); `$indexStats` since last restart; slow query log / profiler; explain on the 20% reads; replication lag if replica set.

---

### Step 2 — Safe test path

**Do this:** Describe how to test removal of one unused-looking index and which metrics to watch afterward.

**Expected result:** Hide the index (it still costs writes until dropped). Rerun the read queries and explain. If reads stay healthy, drop in a maintenance window. Monitor insert latency, disk, and the previously indexed query shapes. Keep the createIndex command as rollback.

---



## Success criteria

- [ ] Write-path metrics are included, not only read explain
- [ ] Hiding is used before dropping
- [ ] A rollback (re-create) plan exists

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

# Exercise 7.4: Sequence a Failover

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Arrange detection, election, new primary, driver discovery, and application retry.

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

### Step 1 — Arrange the sequence

**Do this:** Order: primary becomes unavailable; members detect failure; election starts; eligible members vote; new primary is selected; driver discovers new topology; application retries eligible operations.

**Expected result:** That order. Detection uses heartbeats. Writes pause during the election window.

---

### Step 2 — Name an application requirement

**Do this:** Write two application behaviors that make failover survivable.

**Expected result:** Replica-set connection string (not a pinned host) and retryable / idempotent operations with sensible timeouts.

---

## Success criteria

- [ ] Election happens before a new primary accepts writes
- [ ] Driver discovery is after the new primary exists
- [ ] Application retry is part of the story

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

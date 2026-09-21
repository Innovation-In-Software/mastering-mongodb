# Exercise 7.2: Label a Replica-Set Architecture

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Label application, driver, primary, secondaries, oplog flow, heartbeats, and read/write paths.

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

### Step 1 — Label members and clients

**Do this:** On the replica-set diagram, mark Application, Driver, Primary, and two Secondaries.

**Expected result:** One primary, two secondaries, client path through the driver — not a raw single-host arrow to a secondary for writes.

---

### Step 2 — Label flows

**Do this:** Draw oplog flow (primary → secondaries), heartbeats (all members), write path (app → primary), and a primary-preference read path.

**Expected result:** Writes hit the primary. Heartbeats are separate from oplog copy. Reads to secondaries are not the default write path.

---

## Success criteria

- [ ] Primary is unique
- [ ] Oplog and heartbeats are not the same arrow
- [ ] Writes are not drawn to a secondary

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

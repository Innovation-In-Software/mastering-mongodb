# Exercise 7.3: Trace a Replicated Write

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Sequence a write from the client through oplog application and write-concern acknowledgment.

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

### Step 1 — Order the seven events

**Do this:** Number these 1–7: client sends write; driver selects primary; primary applies write; oplog entry is created; secondaries copy the operation; secondaries apply it; acknowledgment returns based on write concern.

**Expected result:** That listed order is the teaching sequence. Acknowledgment is last and depends on `w`.

---

### Step 2 — Change one setting

**Do this:** State what changes if write concern is majority instead of primary-only acknowledgment.

**Expected result:** The client waits until a majority of voting data-bearing members have durably acknowledged, so latency can increase and durability confidence increases.

---

## Success criteria

- [ ] The seven-step order is correct
- [ ] Write concern is not treated as read preference
- [ ] Secondaries apply after they copy oplog entries

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

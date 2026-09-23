# Exercise 7.6: Diagnose Replication Lag

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Match lag symptoms to cause, impact, evidence, and a first corrective action.

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

### Step 1 — Map five symptoms

**Do this:** For each: high disk latency; heavy reporting on a secondary; network congestion; rapid write growth; small oplog window — write likely cause, impact, evidence to collect, and first action.

**Expected result:** Disk: storage saturation → growing lag → iostat/Atlas metrics → faster disks or less write amplification. Reporting: secondary CPU/IO → lag + stale reads → isolate analytics. Network: delayed oplog fetch. Write burst: primary faster than apply. Small oplog: member may fall off and need initial sync.

---

### Step 2 — Pick the first metric

**Do this:** If a secondary is 90 seconds behind and reporting dashboards look empty, which two checks do you run first?

**Expected result:** `rs.printSecondaryReplicationInfo()` / member optimes, and secondary CPU, disk, and current operations — not an immediate rebuild.

---

## Success criteria

- [ ] Each symptom has a distinct first check
- [ ] Oplog window is treated as a recovery risk
- [ ] Reporting load is not ignored as free capacity

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

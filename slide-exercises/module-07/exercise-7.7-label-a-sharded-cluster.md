# Exercise 7.7: Label a Sharded Cluster

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 10 min  
**Difficulty:** Beginner

**Objective:** Label application, driver, mongos, configuration servers, shards, replica-set members, metadata, and query flow.

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

### Step 1 — Label components

**Do this:** On the cluster diagram, mark Application, Driver, `mongos`, config replica set, and three shards each drawn as a replica set.

**Expected result:** Clients talk to `mongos`, not directly to a random shard primary as the only entry. Config servers are separate from shards.

---

### Step 2 — Label the two flows

**Do this:** Draw query/write flow (app → mongos → targeted shard) and metadata flow (mongos ↔ config servers).

**Expected result:** Metadata is not application documents. `mongos` stores no collection data.

---

## Success criteria

- [ ] Config servers are not a shard of orders
- [ ] `mongos` is on the client path
- [ ] Each shard shows P/S members

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

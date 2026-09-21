# Lab 7.10: Integrated Availability and Scaling Challenge

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 40–45 min  
**Difficulty:** Intermediate

**Objective:** Design replication, sharding, shard key, routing, read/write settings, failover, and monitoring for the e-commerce order platform.

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

### Step 1 — Collections and topology

**Do this:** Decide which collections stay replica-set only versus shard candidates. Design a three-member (or more) replica-set topology per shard with failure domains.

**Expected result:** Orders are the first shard candidate under write growth. Products/customers often remain unsharded initially. Each shard is a replica set.

---

### Step 2 — Shard key and routing

**Do this:** Select a candidate order shard key. Compare ranged, hashed, and compound. List targeted queries vs unavoidable scatter-gather reports.

**Expected result:** A scored key (not `paymentStatus`). Customer history targeted. Monthly global revenue scatter-gather or redesigned.

---

### Step 3 — Read/write and failover

**Do this:** Recommend read preference and write concern for order placement vs catalog browse. Describe what the app sees during a primary election.

**Expected result:** Order placement: primary + majority. Catalog may use primaryPreferred. Election: brief write errors, driver rediscovery, retries.

---

### Step 4 — Monitoring

**Do this:** List monitoring for lag, oplog window, chunk distribution, balancer, mongos availability, and CSRS health.

**Expected result:** A checklist with owners/thresholds sketched, not “we will watch the dashboard.”

---

## Scenario (keep this visible)

E-commerce requires continuous order processing, server-failure resilience, customer-order lookup, high order-write volume, regional data placement, and global sales reporting.

## Success criteria

- [ ] Replication and sharding are both addressed
- [ ] Shard-key risks are explicit
- [ ] Settings differ by operation
- [ ] Monitoring covers replica set and cluster

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

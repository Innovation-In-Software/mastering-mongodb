# Exercise 8.9: Design a Monitoring Dashboard

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Select essential metrics for availability, query performance, resources, connections, replication, sharding, storage, backups, and security — each with an operational purpose.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may use `mongosh` to inspect `training_store`, but reasoning is the deliverable unless a step says otherwise. Do not enable authentication on a shared training instance unless the instructor provides a disposable environment.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Pick twelve tiles

**Do this:** Choose at most twelve dashboard tiles that a weekday on-call would actually use. For each, write the metric and the question it answers. Reject vanity metrics.

**Expected result:** Examples: primary/alive, request latency p99, slow ops, CPU, disk %, connections vs limit, replication lag, oplog window, targeted vs scatter (if sharded), backup last success, auth failures. Not: ‘documents in collection’ with no threshold.

---

### Step 2 — Drop two candidates

**Do this:** Name two metrics you would leave off the primary dashboard and why.

**Expected result:** Per-collection document counts or raw opcounters without a baseline are noise. Shard-balancer internals may belong on a secondary view unless the cluster is sharded and balancing is a live risk.

---

## Success criteria

- [ ] Each tile has a purpose question
- [ ] Availability, latency, replication, backup, and security appear
- [ ] At least one metric is explicitly excluded

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

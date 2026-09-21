# Exercise 8.14: Production-Readiness Review for training_store

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 45 min  
**Difficulty:** Intermediate

**Objective:** Produce a six-part action plan covering data model, performance, security, reliability, monitoring, and a final production-readiness classification with evidence.

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

### Step 1 — Write model and performance recommendations

**Do this:** Correct BSON types; separate unbounded reviews; preserve order snapshots; add validation; plan migration. Then rewrite broad queries, add projections, tune the sales aggregation, recommend indexes, flag redundant indexes, and name baseline metrics.

**Expected result:** A two-section note exists. Reviews are a collection. Prices are Decimal128. Queries are selective. Indexes follow ESR. At least one overlapping index is flagged. Baseline includes latency, examined counts, and connections.

---

### Step 2 — Write security, reliability, and monitoring

**Do this:** Restrict network access; replace shared credentials; least privilege; TLS; secret storage; audit privileged activity. Test failover; review lag and oplog; define RPO/RTO; test restore. Add query, connection, storage, replication, backup, and security monitoring with three critical alerts and named owners.

**Expected result:** Security list includes network, authn, authz, TLS, secrets. Reliability includes tested failover and restore plus RPO/RTO. Monitoring has owners, not only metrics.

---

### Step 3 — Classify with evidence

**Do this:** Select Production-ready, Ready with conditions, or Not production-ready. Cite evidence from the current environment list (no validation, public network, untested restore, CPU-only monitoring, and the rest).

**Expected result:** Not production-ready is the defensible call. Ready with conditions is acceptable only if conditions are explicit and blocking. Production-ready is not justified.

---

## Current environment (do not treat as ready)

- Flexible documents without validation
- Several inconsistent price types
- Large review arrays embedded in products (in the scenario; `training_store` already separates reviews — call that out as the target state)
- Broad queries returning complete documents
- Multiple overlapping indexes
- Shared administrative credentials
- Public network access
- Replica set but no failover test
- Successful backups but no restore test
- Basic CPU monitoring only
- No operational runbooks

## Final classification

Choose one: **Production-ready** · **Ready with conditions** · **Not production-ready**

## Success criteria

- [ ] All six deliverable sections are present
- [ ] Classification is supported by evidence
- [ ] Critical alerts have owners

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

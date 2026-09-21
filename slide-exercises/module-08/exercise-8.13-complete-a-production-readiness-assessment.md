# Exercise 8.13: Complete a Production-Readiness Assessment

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Assess a fictional deployment across data model, queries, indexes, security, availability, backup, monitoring, documentation, and ownership, then classify it as ready, ready with conditions, or not ready.

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

### Step 1 — Score nine areas

**Do this:** Using the fictional `training_store` production story on the slides (no validation, mixed price types, embedded unbounded reviews, broad queries, overlapping indexes, shared admin credentials, public network, untested failover, untested restore, CPU-only monitoring, no runbooks), mark each area Ready / Conditional / Not ready with one evidence sentence.

**Expected result:** Most areas are Not ready. Indexes might be Conditional if some useful keys exist but overlap is unproven. Availability is Conditional (replica set exists, failover untested).

---

### Step 2 — Classify the deployment

**Do this:** Choose one overall label and list the three conditions that would have to be true before a go-live.

**Expected result:** Not production-ready. Conditions typically: authentication + network restriction, tested backup restore, and indexed selective queries with a baseline. Shared admin and public exposure alone are enough to fail the gate.

---

## Success criteria

- [ ] Nine areas are scored with evidence
- [ ] Overall classification is Not ready (or Ready with conditions only if the learner tightens scope unrealistically — instructor challenges that)
- [ ] Three go-live conditions are specific

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

# Exercise 8.11: Diagnose an Operational Incident

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Determine likely cause, mitigation, evidence, permanent correction, and prevention when the order API slows after a release with higher documentsExamined and an unchanged index set.

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

### Step 1 — Form the hypothesis

**Do this:** Evidence: CPU moderately up; documents examined up sharply; no election; connections normal; a query filter changed; indexes unchanged. What is the likely cause, and what is not the cause?

**Expected result:** Likely: the new filter no longer uses the existing index (predicate, type, or field name), causing a collection scan or a weakly selective plan. Not: failover, connection exhaustion, or a missing replica set.

---

### Step 2 — Mitigate and prevent

**Do this:** Write immediate mitigation, evidence to collect, permanent correction, and one prevention action for the next release.

**Expected result:** Mitigate: revert the filter or add a matching index if the new shape is intended. Collect: the exact query, explain before/after, deploy diff. Permanent: index for the new shape or restore the selective predicate. Prevent: explain the changed query in staging; include query-shape review in the release checklist.

---

## Success criteria

- [ ] Hypothesis ties the filter change to examined-document growth
- [ ] Failover is ruled out with evidence
- [ ] Prevention includes testing explain on the new shape

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

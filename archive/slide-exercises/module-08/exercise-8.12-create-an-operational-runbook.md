# Exercise 8.12: Create an Operational Runbook

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Write a runbook for one event: no primary, rising replication lag, disk nearing capacity, backup failure, authentication failures, or a slow-query spike.

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

### Step 1 — Fill the template

**Do this:** Pick one event. Write: alert name, meaning, business impact, required access, diagnostic commands, expected normal state, decision points, corrective actions, escalation, rollback, verification, and where the incident is documented.

**Expected result:** A complete page exists. Diagnostics are real commands (`rs.status()`, `explain`, disk checks). Corrective actions are sequenced. Escalation has a person or role, not ‘tell someone’.

---

### Step 2 — Add a verification step

**Do this:** Write how you know the incident is over (metric + user-facing check) and what you will change so it does not recur silently.

**Expected result:** Example: primary exists for 15 minutes, checkout succeeds, lag < baseline. Follow-up: alert threshold, dashboard tile, or change-review item.

---

## Runbook template

| Section | Your notes |
|---------|------------|
| Alert name | |
| Meaning | |
| Business impact | |
| Required access | |
| Diagnostic commands | |
| Expected normal state | |
| Decision points | |
| Corrective actions | |
| Escalation | |
| Rollback | |
| Verification | |
| Incident documentation | |

## Success criteria

- [ ] The runbook is for a single named alert
- [ ] Diagnostics and verification are concrete
- [ ] Escalation and rollback are present

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

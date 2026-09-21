# Exercise 8.6: Design Least-Privilege Roles

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Define permitted and prohibited operations for application, reporting, support, monitoring, backup, and administrator identities.

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

### Step 1 — Fill the permission matrix

**Do this:** For each identity — application service, reporting service, support engineer, monitoring service, backup service, database administrator — list one permitted operation and one prohibited operation on `training_store`.

**Expected result:** App: read/write app collections, not userAdmin. Reporting: read approved collections, not update. Support: read (maybe limited PII), not drop. Monitoring: clusterMonitor-style, not data writes. Backup: backup privileges, not arbitrary deletes. DBA: admin with change control, not used by the app.

---

### Step 2 — Call out the anti-pattern

**Do this:** Write two sentences on why the application must not use a cluster-administrator account, even in training-like environments that later become production.

**Expected result:** A stolen app credential would inherit every privilege. Least privilege limits blast radius and makes audit trails meaningful.

---

## Success criteria

- [ ] Six identities have permit and deny examples
- [ ] The application is not given clusterAdmin
- [ ] Reporting is read-only

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

# Exercise 8.10: Set Alert Priorities

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Classify operational alerts as critical, high, medium, or informational and name the first action for each.

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

### Step 1 — Classify eight alerts

**Do this:** Classify: no primary; increasing replication lag; disk 90% full; backup failed; authentication-failure spike; slow-query increase; one secondary unavailable; high connection usage.

**Expected result:** Critical: no primary. High: disk 90%, backup failed, auth-failure spike, lag still growing toward oplog risk. Medium: one secondary down (if majority remains), high connections, slow-query increase. Informational: brief lag blip with a known backup window — if you alert at all.

---

### Step 2 — Attach first actions

**Do this:** For critical and high items, write the first action and the runbook name you would open.

**Expected result:** No primary → check replica-set status and network, do not reconfigure hastily. Disk 90% → identify growth, free space, page the owner. Backup failed → verify job, storage, credentials. Auth spike → confirm not a deploy, then lock down.

---

## Success criteria

- [ ] No primary is critical
- [ ] Each high alert has a first action
- [ ] Not every metric is critical

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

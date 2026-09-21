# Lab 7.3: Observe Election and Failover

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Watch a controlled step-down, record the interruption, identify the new primary, and confirm the old primary returns as a secondary.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected with a **replica-set URI**.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

**Replica-set labs:** Atlas (`mongodb+srv://`) is a replica set. A local standalone `mongod` is not. If `rs.status()` reports that the process is not running with `--replSet`, switch to the instructor Atlas URI.

**Failover and sharding labs:** Use only an instructor-controlled disposable cluster. Do **not** step down or shard a shared classroom Atlas deployment unless the instructor says it is disposable.

```javascript
use training_store
```


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Record the current primary

**Do this:** On the **instructor disposable replica set**, run `rs.status()` and write the current primary host. Do **not** run this lab against a shared Atlas class cluster unless the instructor confirms it is disposable.

**Expected result:** One hostname/port labeled PRIMARY.

---

### Step 2 — Observe the step-down

**Do this:** Watch the instructor run a controlled `rs.stepDown()` (or stop the primary process). Note the time writes pause. Then run `rs.status()` again.

**Expected result:** A different member is PRIMARY, or you recorded the election window from the instructor’s screen if students cannot reconnect yet.

---

### Step 3 — Verify writes resume

**Do this:** After a primary exists, insert a one-document probe and read it back. Then confirm the former primary’s state when it rejoins.

**Expected result:** Insert succeeds. Former primary is SECONDARY (not still claiming PRIMARY).

---

### Step 4 — Document application behavior

**Do this:** Write what a well-behaved driver should do: rediscover topology, retry eligible operations, surface errors if retry is exhausted.

**Expected result:** Notes mention replica-set URI, transient errors, and retry — not “the application must be restarted by hand.”

---

## Success criteria

- [ ] Old and new primary are recorded
- [ ] Write pause is acknowledged
- [ ] Former primary rejoins as secondary
- [ ] No student stepped down a shared cluster without permission

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

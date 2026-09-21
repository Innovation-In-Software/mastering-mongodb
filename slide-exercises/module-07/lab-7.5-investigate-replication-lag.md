# Lab 7.5: Investigate Replication Lag

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Compare replication timestamps, consider secondary load and oplog window, and propose corrective actions.

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

### Step 1 — Capture member optimes

**Do this:** Run:

```javascript
rs.status()
rs.printSecondaryReplicationInfo()
```

**Expected result:** A table of members and lag. In a quiet training set, lag may be ~0. Still record it as a baseline.

---

### Step 2 — Inspect oplog window

**Do this:** Run:

```javascript
use local
db.oplog.rs.stats()
rs.printReplicationInfo()
```

**Expected result:** You can state that the oplog is a capped collection in `local.oplog.rs` and note size / time window if printed. Command names can vary slightly by version — record what your shell returned.

---

### Step 3 — Review causes against this lab

**Do this:** If the instructor injected lag (heavy secondary query, paused member), list the likely cause. If not, write the five causes you would check in production: disk, CPU, network, write burst, secondary workload.

**Expected result:** A cause list tied to evidence, not a guess-only paragraph.

---

### Step 4 — Propose actions

**Do this:** Write two actions you would take if lag were growing (for example 30s, then minutes) and one action you would **not** take first (panic rebuild).

**Expected result:** First: reduce secondary load / check disk. Not first: delete the replica and hope.

---

## Success criteria

- [ ] Timestamps were compared
- [ ] Oplog is identified as the replication log
- [ ] Corrective actions are ordered sanely

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

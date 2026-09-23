# Lab 7.1: Verify Replica-Set Health

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Inspect replica-set name, member states, health, votes, and replication timestamps, then write a short health report.

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

### Step 1 — Confirm you are on a replica set

**Do this:** Connect with the replica-set / Atlas URI, then run:

```javascript
rs.status()
rs.conf()
```

**Expected result:** A replica-set name, one `PRIMARY`, one or more `SECONDARY` members, `health: 1` on reachable members. If you see a standalone error, stop and switch URI.

---

### Step 2 — Record identity and votes

**Do this:** From `rs.status()` and `rs.conf()`, write: set name, primary host, secondary hosts, each member’s `votes` and `priority`. Note any arbiter.

**Expected result:** A table of members with state, votes, and priority. Atlas typically shows three data-bearing members and no arbiter.

---

### Step 3 — Record replication timestamps

**Do this:** Run:

```javascript
rs.printSecondaryReplicationInfo()
```

**Expected result:** Each secondary shows how far behind the primary (often 0–2 seconds when idle). Record the values even if they are zero.

---

### Step 4 — Write the health report

**Do this:** One short paragraph: is a primary present? Is a majority reachable? Is lag concerning? Any config smell (arbiter-only durability, priority 0 on the only nearby member)?

**Expected result:** A report that would make sense to another operator. No unexplained red states.

---

## Success criteria

- [ ] Primary is identified
- [ ] Voting configuration is recorded
- [ ] Lag is measured, not guessed
- [ ] Concerns are listed even if the set is healthy

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

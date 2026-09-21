# Lab 7.2: Write and Verify Replication

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Insert a test document through the replica set, confirm acknowledgment, and observe it after replication.

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

### Step 1 — Insert through the replica-set URI

**Do this:** Use the replica-set connection string (not a single secondary host). Run:

```javascript
use training_store
db.repl_lab.insertOne({
  lab: "7.2",
  note: "replication check",
  createdAt: new Date()
})
```

**Expected result:** `acknowledged: true` and an `_id`. You are talking to the current primary.

---

### Step 2 — Read it back on primary preference

**Do this:** Run:

```javascript
db.repl_lab.find({ lab: "7.2" })
rs.printSecondaryReplicationInfo()
```

**Expected result:** The document is visible. Lag remains small after a single insert.

---

### Step 3 — Discuss secondary inspection

**Do this:** If the instructor provides a safe secondary read (read preference `secondary` in a disposable cluster), run the same `find`. Otherwise write why secondary reads can be stale even when this insert already appears.

**Expected result:** Either the document is visible on a secondary, or a written explanation of replication delay and read preference.

---

### Step 4 — Remove the temporary record

**Do this:** Run:

```javascript
db.repl_lab.deleteMany({ lab: "7.2" })
```

**Expected result:** `deletedCount` matches what you inserted. Collection may remain empty.

---

## Success criteria

- [ ] Write used a replica-set URI
- [ ] Acknowledgment was recorded
- [ ] Temporary document was deleted

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

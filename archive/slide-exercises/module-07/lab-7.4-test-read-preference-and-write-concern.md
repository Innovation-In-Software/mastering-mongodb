# Lab 7.4: Test Read Preference and Write Concern

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Compare serving members for primary versus secondary-preferred reads and perform writes with assigned write concerns.

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

### Step 1 — Primary read

**Do this:** In `mongosh` connected to the replica set, run a `find` with default (primary) read preference on `training_store.products` and note which member you are on:

```javascript
db.hello()
db.products.find({ sku: "L100" }).limit(1)
```

**Expected result:** `db.hello()` shows `isWritablePrimary: true` (or equivalent) for the default connection. The product document returns.

---

### Step 2 — Secondary-preferred read (if permitted)

**Do this:** If the instructor allows, start a second shell with read preference `secondaryPreferred` (connection string `readPreference=secondaryPreferred` or `db.getMongo().setReadPref("secondaryPreferred")`) and run the same find. Compare `db.hello()`.

**Expected result:** You either hit a secondary (`secondary: true`) or fell back to primary. Staleness risk is written down even if data matched.

---

### Step 3 — Compare write concerns

**Do this:** Insert two probe documents with different write concerns:

```javascript
db.repl_lab.insertOne(
  { lab: "7.4", wc: "majority" },
  { writeConcern: { w: "majority", wtimeout: 5000 } }
)
db.repl_lab.insertOne(
  { lab: "7.4", wc: "1" },
  { writeConcern: { w: 1, wtimeout: 5000 } }
)
```

**Expected result:** Both acknowledge in a healthy set. Record approximate duration if the shell shows it. Majority should not be described as “always slower enough to skip.”

---

### Step 4 — Map to business operations

**Do this:** State which pair of settings you would use for payment confirmation versus product-catalog browsing. Delete probes: `db.repl_lab.deleteMany({ lab: "7.4" })`.

**Expected result:** Payment: primary reads + majority writes. Catalog: primaryPreferred/nearest and `w: majority` still preferred in production; secondary reads only if staleness is acceptable.

---

## Success criteria

- [ ] Primary versus secondary-preferred serving member is compared
- [ ] Two write concerns were attempted
- [ ] Business mapping is written
- [ ] Probe documents were removed

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

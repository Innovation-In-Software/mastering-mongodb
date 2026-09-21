# Lab 7.7: Shard a Training Collection

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** On a disposable sharded cluster, create a supporting index, shard a training collection, insert sample documents, and inspect the key.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell · `mongosh` against the **instructor sharded training cluster** when provided.

| Task | Windows | Where |
|------|---------|-------|
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| Connect | Instructor `mongos` URI | Same terminal |

Atlas M0 is a replica set, **not** a sharded cluster. If no `mongos` URI is available, complete the steps using the sample output in this guide and the instructor demonstration.

Do **not** enable sharding on a shared production-like database.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Use only a disposable cluster

**Do this:** Confirm with the instructor that this is a throwaway sharded cluster. Create a training database namespace they specify (example `training_shard`).

**Expected result:** You are not connected to the shared Atlas class replica set as if it were mongos.

---

### Step 2 — Create the shard-key index and enable sharding

**Do this:** Commands vary by MongoDB version. A typical training sequence:

```javascript
use training_shard
db.orders_lab.createIndex({ customerId: 1, createdAt: 1 })
sh.enableSharding("training_shard")
sh.shardCollection(
  "training_shard.orders_lab",
  { customerId: 1, createdAt: 1 }
)
```
If `enableSharding` is unnecessary on your version, follow the instructor’s exact commands.

**Expected result:** Collection is sharded. Errors about existing keys or already-sharded collections are resolved with the instructor, not by dropping unknown data.

---

### Step 3 — Insert sample documents

**Do this:** Insert several documents with different `customerId` values and `createdAt` dates. Then `sh.status()` and confirm the shard key.

**Expected result:** Documents insert. Status shows `{ customerId: 1, createdAt: 1 }` (or the assigned key).

---

### Step 4 — Inspect distribution

**Do this:** Note chunk/range counts per shard. Small samples may still sit on one shard — write that down; do not force-balance unless instructed.

**Expected result:** A distribution note that does not assume instant perfect balance on a handful of documents.

---

## Success criteria

- [ ] Supporting index exists
- [ ] Shard key is confirmed in status
- [ ] Sample inserts succeeded
- [ ] No shared classroom cluster was sharded without permission

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

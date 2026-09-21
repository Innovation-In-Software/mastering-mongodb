# Lab 7.6: Inspect Sharded-Cluster Components

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Identify mongos, shards, shard replica sets, the config replica set, sharded collections, and shard keys.

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

### Step 1 — Connect to mongos

**Do this:** Using the instructor `mongos` URI (or the sample `sh.status()` the instructor pastes), run:

```javascript
sh.status()
```

**Expected result:** Output lists shards, a config server replica set, and optionally sharded databases/collections. On a replica set without sharding, this command is not the right topology — use the sample output instead.

---

### Step 2 — List shards and config

**Do this:** Write the shard names and the config replica-set name. Note that each shard should itself be a replica set in production.

**Expected result:** At least one shard id and a config RS name are recorded.

---

### Step 3 — List sharded collections

**Do this:** From `sh.status()` (or `db.getSiblingDB("config").collections.find()` on mongos), record each sharded collection and its shard key.

**Expected result:** A table: database.collection → shard key. Empty is acceptable on a fresh training cluster.

---

### Step 4 — Describe data placement

**Do this:** If chunks/ranges are shown, note whether they look even. If none, write “unsharded / not yet chunked.”

**Expected result:** A one-sentence distribution comment.

---

## Success criteria

- [ ] `mongos` is distinguished from shard mongod
- [ ] Config servers are named
- [ ] Shard keys are copied from status, not invented

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

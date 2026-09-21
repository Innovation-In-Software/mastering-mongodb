# Lab 7.8: Analyze Query Routing

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Explain targeted versus scatter-gather plans for shard-key equality, ranges, partial compound keys, and non-key filters.

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

### Step 1 — Full shard-key equality

**Do this:** On the sharded training collection, run `explain` for a find that includes the full shard key (or leading equality + range the instructor specifies). Record `shards` / `winningPlan` targeting.

**Expected result:** The plan indicates one (or a small set of) targeted shards, not all shards, when the key is present.

---

### Step 2 — Non-shard-key equality

**Do this:** Explain a find on `paymentStatus` (or another non-key field) only. Record whether mongos scatters.

**Expected result:** Scatter-gather / query all shards is expected.

---

### Step 3 — Partial compound key and global aggregation

**Do this:** Explain a filter that uses only the trailing field of a compound key, and a simple `$count` / `$group` with no shard-key `$match`. Record merge behavior.

**Expected result:** Trailing-only predicates usually cannot target. Aggregations without a targeted `$match` merge across shards.

---

### Step 4 — Summarize for the app team

**Do this:** Write which of the five query shapes (full key, key range, partial compound, non-key, global agg) must stay rare in the hot path.

**Expected result:** Non-key finds and global aggregations are called out as expensive when frequent.

---

## Success criteria

- [ ] At least two explain outputs are recorded
- [ ] Scatter-gather is identified by evidence
- [ ] Hot-path advice is written

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

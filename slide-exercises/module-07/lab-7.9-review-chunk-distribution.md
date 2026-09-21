# Lab 7.9: Review Chunk Distribution

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Examine data and range distribution, balancer state, zones, and hotspot indicators, then write a distribution-health assessment.

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

### Step 1 — Inspect status

**Do this:** Run `sh.status()` (or instructor sample). Record shards, chunk/range counts, and whether the balancer is enabled/running.

**Expected result:** A small table: shard → chunk count. Balancer state is noted.

---

### Step 2 — Look for imbalance

**Do this:** If one shard owns most ranges, write whether that is expected (new cluster, hashed vs ranged, tiny dataset) or a hotspot smell.

**Expected result:** An interpretation, not only raw counts. Tiny training data often looks “imbalanced.”

---

### Step 3 — Zones and hotspots

**Do this:** Note any tags/zones. List hotspot indicators: monotonic key, jumbo chunks, one shard’s data size far ahead.

**Expected result:** Zones listed or “none.” At least one hotspot indicator is considered.

---

### Step 4 — Write the assessment

**Do this:** Five to eight sentences: healthy / watch / action. Include what you would monitor next week.

**Expected result:** A short distribution-health assessment suitable to paste into an ops channel.

---

## Success criteria

- [ ] Balancer state is recorded
- [ ] Imbalance is interpreted in context
- [ ] A written assessment exists

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

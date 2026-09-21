# Exercise 7.9: Targeted or Scatter-Gather?

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Classify queries as single-shard targeted, multi-shard targeted, scatter-gather, or insufficient information.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may inspect `training_store` or `rs.status()` to test ideas. Reasoning is the deliverable unless a step asks you to run a command.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Assume ranged `{ customerId: 1, createdAt: 1 }`

**Do this:** Classify: (A) `{ customerId: C101._id }`, (B) `{ customerId: C101._id, createdAt: { $gte: start } }`, (C) `{ paymentStatus: "PAID" }`, (D) `{ createdAt: { $gte: start } }`, (E) hashed-key range on `createdAt` if the key were hashed customerId.

**Expected result:** A targeted (one or few chunks for that customer). B targeted range within the customer prefix. C scatter-gather. D multi-shard or scatter depending on how dates map — usually many shards. E hashed customerId range on createdAt is scatter-gather.

---

### Step 2 — Name one redesign

**Do this:** If monthly global revenue must stay fast, is a better shard key the fix, or a different reporting design?

**Expected result:** Usually a different design: pre-aggregated reports, an analytics replica/cluster, or accepting scatter-gather for a rare job — not a shard key that hurts the OLTP path.

---

## Success criteria

- [ ] Non-shard-key filters are classified as scatter-gather
- [ ] Prefix equality can target
- [ ] Global reports are not assumed to be single-shard

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

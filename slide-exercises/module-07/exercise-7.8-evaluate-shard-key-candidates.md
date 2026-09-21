# Exercise 7.8: Evaluate Shard-Key Candidates

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 20 min  
**Difficulty:** Intermediate

**Objective:** Score order-collection shard-key candidates from 1–5 for cardinality, distribution, write scale, targeting, hotspot risk, locality, and growth.

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

### Step 1 — Score six candidates

**Do this:** Score `status` / `paymentStatus`, `createdAt`, `customerId`, hashed `customerId`, `{tenantId, orderId}`, `{customerId, createdAt}` for the seven criteria. Use `training_store.orders` as the mental model (few statuses, many customers, monotonic dates).

**Expected result:** status: low cardinality, hotspot, poor targeting. createdAt ranged: monotonic write hotspot. customerId: good targeting for history, possible tenant skew. hashed customerId: even writes, weak range locality. compound tenant+order: targeting if queries lead with tenant. customerId+createdAt: history queries target; ranged writes per customer are usually fine.

---

### Step 2 — Recommend one for orders

**Do this:** Pick one candidate for customer-order lookup plus high write volume. List two risks you still monitor.

**Expected result:** A defensible pick is `{ customerId: 1, createdAt: 1 }` or hashed `customerId` depending on whether range-by-date across customers matters. Risks: celebrity customers, scatter-gather global reports.

---

## Success criteria

- [ ] Low-cardinality status is rejected as a standalone key
- [ ] Monotonic ranged `createdAt` is flagged for hotspots
- [ ] The recommendation names a remaining risk

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

# Exercise 7.11: Diagnose Hotspot Risks

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** 15 min  
**Difficulty:** Intermediate

**Objective:** Review five hotspot patterns and propose a mitigation for each.

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

### Step 1 — Name the hotspot

**Do this:** For timestamp shard key; dominant tenant; low-cardinality status; region zones with 90% of users in one region; celebrity product receiving most traffic — state what becomes hot.

**Expected result:** Timestamp: max chunk / one shard writes. Tenant: one shard’s CPU and storage. Status: few chunks ever receive writes. Zone: the popular region’s shards. Product: one document/range if productId is the key, or one catalog shard.

---

### Step 2 — Propose mitigations

**Do this:** Write one mitigation per case (hashed key, compound key, isolate tenant, split collection, cache, zone redesign, or not sharding that collection).

**Expected result:** Timestamp → hash or compound with high-cardinality leading field. Dominant tenant → isolate or further shard inside tenant. Status → do not use as key. Region skew → more shards in that zone or accept it. Celebrity product → cache, not a new shard key by itself.

---

## Success criteria

- [ ] Each pattern has a distinct mitigation
- [ ] Zones are not treated as a free locality win
- [ ] Low-cardinality keys are rejected

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

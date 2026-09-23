# Exercise 6.6: Select Specialized Index Types

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Match eight requirements to unique, partial, sparse, TTL, text, wildcard, geospatial, or hashed indexes.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may use `mongosh` to test ideas, but reasoning is the deliverable. You do not need to create production indexes during discussion exercises.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Match the first four

**Do this:** Match: (1) product SKU must never duplicate, (2) index only active products, (3) optional discountCode present on few documents, (4) delete sessions after expiresAt.

**Expected result:** 1 unique, 2 partial, 3 sparse (or a partial filter on $exists), 4 TTL.

---

### Step 2 — Match the last four

**Do this:** Match: (5) word search on product names, (6) unpredictable attributes.* paths, (7) nearby stores from a GeoJSON point, (8) hashed shard-key distribution on tenantId.

**Expected result:** 5 text (or an external search product for advanced relevance), 6 wildcard, 7 geospatial 2dsphere, 8 hashed.

---



## Success criteria

- [ ] Eight matches are recorded
- [ ] Partial is preferred over sparse when an explicit subset filter exists
- [ ] Hashed is not chosen for range queries

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

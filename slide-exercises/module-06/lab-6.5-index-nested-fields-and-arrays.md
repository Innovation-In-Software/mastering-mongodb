# Lab 6.5: Index Nested Fields and Arrays

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 25 min  
**Difficulty:** Intermediate

**Objective:** Index a dotted customer email path and product tags, then confirm nested and multikey behavior.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

**Prerequisite:** `training_store` is loaded from [`datasets/training_store/load.js`](../../datasets/training_store/load.js). Reload at the start of Day 3 if Day 2 writes remain.

```javascript
use training_store
```

**Small-data note:** Twelve products and seventeen orders will not produce dramatic wall-clock wins. Record the **plan** (`COLLSCAN` vs `IXSCAN`), **index name**, and **examined vs returned** counts. That is the teaching signal.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Nested email index

**Do this:** Run:

```javascript
db.customers.createIndex(
  { "contact.email": 1 },
  { name: "idx_customers_contact_email" }
)
db.customers.find({ "contact.email": "aisha@example.com" }).explain("executionStats")
```

**Expected result:** IXSCAN on idx_customers_contact_email. nReturned 1.

---

### Step 2 — Multikey tags index

**Do this:** Run:

```javascript
db.products.createIndex(
  { tags: 1 },
  { name: "idx_products_tags" }
)
db.products.find({ tags: "technology" }).explain("executionStats")
db.products.getIndexes()
```

**Expected result:** The tags index is listed. Explain uses it. getIndexes / explain may show `multikey: true`.

---

### Step 3 — Inspect multikey

**Do this:** In getIndexes output for idx_products_tags, find `multikey` (and optional `multikeyPaths`). Query tags `"wireless"` as well.

**Expected result:** multikey is true because tags is an array. Several accessories match wireless.

---

### Step 4 — Record examined counts

**Do this:** Write keys examined and docs examined for the email query and the technology-tag query.

**Expected result:** Two rows of stats. Email should be a single-key lookup; tags examines keys for matching array values.

---



## Success criteria

- [ ] Email query uses the dotted-path index
- [ ] Tags index is identified as multikey
- [ ] Examined counts are recorded for both

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

# Exercise 6.1: Identify Candidate Indexes

**Module 6:** Indexing and Query Performance  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 6)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Name the fields that belong in an index for six recurring training_store queries.

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

### Step 1 — Identifier lookups

**Do this:** For (1) product by SKU and (2) customer by email, write the collection, the filter field, and whether uniqueness is a business rule.

**Expected result:** products.sku (unique) and customers.contact.email (unique if the store treats email as a login). `_id` already covers ObjectId lookups.

---

### Step 2 — History and catalog queries

**Do this:** For (3) a customer’s orders newest first, (4) active products by category and price, (5) reviews by product and date, and (6) orders by payment status and creation date, list equality, sort, and range fields.

**Expected result:** (3) customerId equality, createdAt sort. (4) category + active equality, price sort/range. (5) productId equality, createdAt sort. (6) paymentStatus equality, createdAt sort/range.

---



## Success criteria

- [ ] Each query names a collection and indexed fields
- [ ] SKU and email are treated as identifier lookups
- [ ] Sort fields are listed separately from equality fields

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

# Exercise 4.18: Lab 4.4 Projection and Pagination Lab

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Shape result documents and page through a sorted product list.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

**Prerequisite:** `training_store` is loaded from [`datasets/training_store/load.js`](../../datasets/training_store/load.js). If writes from an earlier lab remain, reload that script unless the exercise says otherwise.

```javascript
use training_store
```


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Product summary projection

**Do this:** Active products: `name`, `category`, `price`, no `_id`.

**Expected result:** Compact catalog rows.

---

### Step 2 — Customer-contact projection

**Do this:** `name.first`, `name.last`, `contact.email` for ACTIVE customers.

**Expected result:** No addresses in the result.

---

### Step 3 — Order-status projection

**Do this:** `orderNumber`, `status`, `total`.

**Expected result:** Operations list without line items.

---

### Step 4 — Sorted product list

**Do this:** Sort `{ category: 1, price: -1, _id: 1 }`.

**Expected result:** Deterministic order within category.

---

### Step 5 — Limited result set

**Do this:** Limit 5 on the sorted active products.

**Expected result:** Exactly five documents.

---

### Step 6 — Two pages of results

**Do this:** skip 0 limit 5 then skip 5 limit 5 with the same sort.

**Expected result:** No overlapping `_id` values.

---

### Step 7 — Count matching documents

**Do this:** `countDocuments` on the same filter as the list.

**Expected result:** Count equals how many documents pagination would eventually cover.

---



## Success criteria

- [ ] Did not mix inclusion and exclusion
- [ ] Used a stable sort for pagination
- [ ] Counted with `countDocuments`

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

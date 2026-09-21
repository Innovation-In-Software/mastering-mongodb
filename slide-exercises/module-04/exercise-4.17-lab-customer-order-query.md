# Exercise 4.17: Lab 4.3 Customer and Order Query Lab

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 30 min  
**Difficulty:** Intermediate

**Objective:** Query customers and orders by identifier, nested contact, addresses, items, status, dates, and totals.

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

### Step 1 — Customer by number

**Do this:** findOne `{ customerNumber: "C101" }`.

**Expected result:** Aisha Khan with nested `name` and `contact`.

---

### Step 2 — Customer by email

**Do this:** find `{ "contact.email": "aisha@example.com" }`.

**Expected result:** The same customer. Quote the dotted path.

---

### Step 3 — Address in a city

**Do this:** find `{ "addresses.city": "Toronto" }` or `$elemMatch` on SHIPPING + Toronto.

**Expected result:** `C101`.

---

### Step 4 — Order by number

**Do this:** findOne `{ orderNumber: "O5001" }`.

**Expected result:** Two line items (L100 qty 1, A410 qty 2), paymentStatus PENDING.

---

### Step 5 — Orders for a customer

**Do this:** Store C101 `_id`, then find `{ customerId: c101Id }`.

**Expected result:** `O5001`, `O6101`, and other C101 orders.

---

### Step 6 — Orders containing a SKU

**Do this:** find `{ "items.sku": "L100" }`.

**Expected result:** `O5001`, `O6101`, and `O6401`.

---

### Step 7 — Same item two conditions

**Do this:** Use `$elemMatch` for sku L100 and quantity ≥ 2.

**Expected result:** Only `O6401`.

---

### Step 8 — One of several statuses

**Do this:** `paymentStatus` `$in: ["PENDING", "FAILED"]`.

**Expected result:** `O5001`, `O6401`, `O6402`, `O6499`.

---

### Step 9 — Created during a date range

**Do this:** Filter `createdAt` `$gte` ISODate 2026-09-01 and `$lt` ISODate 2026-10-01.

**Expected result:** September 2026 orders including `O5001` and `O6401`.

---

### Step 10 — Orders above a total

**Do this:** total `$gt` Decimal128("1000.00").

**Expected result:** Includes `O5001`, `O6101`, `O6401`, and other high-value orders.

---



## Success criteria

- [ ] Used dotted paths for nested customer fields
- [ ] Applied `$elemMatch` on order items
- [ ] Used ISODate for the date range, not strings

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

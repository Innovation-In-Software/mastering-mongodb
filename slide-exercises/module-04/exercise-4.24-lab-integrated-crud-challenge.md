# Exercise 4.24: Lab 4.10 Integrated CRUD Challenge

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 45 min  
**Difficulty:** Intermediate

**Objective:** Walk a store scenario from new product through order updates to a verified soft-delete.

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

### Step 1 — Insert the product

**Do this:** Insert sku `A800`, name "Magnetic Charger", ACCESSORY, Decimal128 34.99, stockQuantity 10, active true.

**Expected result:** findOne by sku succeeds.

---

### Step 2 — Verify the product

**Do this:** Project sku, name, price, stockQuantity.

**Expected result:** Types: decimal price, int stock.

---

### Step 3 — Add unique tags

**Do this:** `$addToSet` `$each` `["usb-c", "featured", "accessory"]`.

**Expected result:** No duplicates if a tag already existed.

---

### Step 4 — Increase inventory

**Do this:** `$inc` stockQuantity by 15.

**Expected result:** Stock is 25 on a first run.

---

### Step 5 — Create a customer

**Do this:** C801 with nested name/contact and status ACTIVE.

**Expected result:** findOne by customerNumber.

---

### Step 6 — Add a shipping address

**Do this:** `$push` an address `{ type: "shipping", city: "Montreal", country: "Canada" }`.

**Expected result:** addresses is an array with Montreal.

---

### Step 7 — Create an order containing the product

**Do this:** O5800 with snapshot of C801 and one item A800 qty 1, status NEW, Decimal128 total.

**Expected result:** Order exists with embedded item.

---

### Step 8 — Update the order status

**Do this:** `$set` status `"PROCESSING"` and `$push` statuses `"PROCESSING"` (or `$addToSet`).

**Expected result:** Status is PROCESSING.

---

### Step 9 — Update the item quantity

**Do this:** Positional `$` set quantity to 2 and `$set` total to Decimal128("69.98").

**Expected result:** Line quantity and order total agree.

---

### Step 10 — Order summary projection

**Do this:** find O5800 projecting orderNumber, status, total, items.sku, items.quantity — no `_id`.

**Expected result:** Compact summary only.

---

### Step 11 — Count the customer’s orders

**Do this:** countDocuments `{ customerId: c801Id }` after looking up C801.

**Expected result:** At least 1.

---

### Step 12 — Soft-delete the product

**Do this:** `$set` `{ active: false, deletedAt: new Date() }` on A800 — do not deleteOne.

**Expected result:** Product still exists; active is false.

---

### Step 13 — Verify all final documents

**Do this:** find customer C801, order O5800, product A800.

**Expected result:** All three exist. Product is inactive. Order is PROCESSING with qty 2.

---



## Success criteria

- [ ] Completed the scenario without dropping collections
- [ ] Used unique add for tags and positional update for quantity
- [ ] Soft-deleted rather than hard-deleted the product
- [ ] Verified every write

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

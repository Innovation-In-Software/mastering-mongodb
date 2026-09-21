# Exercise 4.9: Insert New Application Data

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Insert one document, several documents, a customer, and an order, then verify each write.

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

### Step 1 — Insert one product

**Do this:** Run:

```javascript
db.products.insertOne({
  sku: "A620",
  name: "USB-C Hub",
  category: "ACCESSORY",
  price: Decimal128("69.99"),
  tags: ["usb-c", "accessory"],
  active: true,
  stockQuantity: 10,
  createdAt: new Date()
})
```

**Expected result:** `acknowledged: true` and an `insertedId`. If `sku` already exists, unique index `sku_unique` rejects the insert — reload the dataset.

---

### Step 2 — Insert three products

**Do this:** Run:

```javascript
db.products.insertMany([
  { sku: "A610", name: "Laptop Stand", category: "ACCESSORY", price: Decimal128("49.99"), active: true, stockQuantity: 6 },
  { sku: "A611", name: "HDMI Adapter", category: "ACCESSORY", price: Decimal128("24.99"), active: true, stockQuantity: 15 },
  { sku: "A612", name: "Sleeve", category: "ACCESSORY", price: Decimal128("19.99"), active: true, stockQuantity: 20 }
])
```

**Expected result:** `insertedIds` contains three keys. Inspect `insertedCount` / `insertedIds`.

---

### Step 3 — Insert a customer with an address

**Do this:** Run:

```javascript
db.customers.insertOne({
  customerNumber: "C801",
  name: { first: "Elena", last: "Novak" },
  contact: { email: "elena@example.com" },
  addresses: [{ type: "SHIPPING", city: "Vancouver", country: "Canada" }],
  status: "ACTIVE"
})
```

**Expected result:** One customer with nested `name`, `contact`, and `addresses`.

---

### Step 4 — Insert an order with two items

**Do this:** Run:

```javascript
db.orders.insertOne({
  orderNumber: "O5100",
  customerId: db.customers.findOne({ customerNumber: "C801" })._id,
  items: [
    { sku: "A620", quantity: 1, unitPrice: Decimal128("69.99") },
    { sku: "A610", quantity: 1, unitPrice: Decimal128("49.99") }
  ],
  total: Decimal128("119.98"),
  paymentStatus: "PENDING",
  fulfillmentStatus: "NEW",
  createdAt: new Date()
})
```

**Expected result:** The order snapshots customer fields and embeds line items.

---

### Step 5 — Verify every insert

**Do this:** Run:

```javascript
db.products.find({ sku: { $in: ["A620", "A610", "A611", "A612"] } }, { sku: 1, name: 1, price: 1 })
db.customers.findOne({ customerNumber: "C801" })
db.orders.findOne({ orderNumber: "O5100" })
```

**Expected result:** Four products, one customer, one order. Confirm `price` and `unitPrice` are Decimal128, not strings.

---



## Success criteria

- [ ] Captured insert ids / acknowledged results
- [ ] Used Decimal128 for money
- [ ] Verified with `find` / `findOne` after writing

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

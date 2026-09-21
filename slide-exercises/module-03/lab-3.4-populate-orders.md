# Lab 3.4: Create and Populate the Orders Collection

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.6)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Insert order `O5001` that references the customer, embeds line-item snapshots, and stores Decimal128 totals.

**Prerequisite:** Module 2 — a working `mongosh` session. If `training_store` still holds the Module 1 starter documents, these labs **replace** that shape with the Day 2 application model.


---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

Use the same connection string from Module 2. Do **not** paste real passwords into chat or screenshots.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Load the customer and product

**Do this:**

```javascript
const customer = db.customers.findOne({ customerNumber: "C101" })
const product = db.products.findOne({ sku: "L100" })
```

Confirm both are not `null`.

**Expected result:** `customer._id` and `product.price` print if you inspect them. You will copy those values into the order.

---

### Step 2 — Insert the order and verify

**Do this:** Run:

```javascript
db.orders.insertOne({
  orderNumber: "O5001",
  customerId: customer._id,
  items: [
    {
      productId: product._id,
      sku: product.sku,
      name: product.name,
      quantity: 1,
      unitPrice: product.price
    }
  ],
  shippingAddress: {
    street: "100 King Street",
    city: "Toronto",
    province: "Ontario",
    postalCode: "M5X 1A9",
    country: "Canada"
  },
  paymentStatus: "PENDING",
  fulfillmentStatus: "NEW",
  subtotal: Decimal128("1299.99"),
  tax: Decimal128("169.00"),
  total: Decimal128("1468.99"),
  createdAt: new Date()
})

db.orders.findOne({ orderNumber: "O5001" })
```

**Expected result:** One order document. Items and address are embedded. Customer is an id reference, not a full customer copy.

---

## Success criteria

- [ ] Order O5001 exists
- [ ] `customerId` matches the customer `_id`
- [ ] Line item preserves sku, name, and unitPrice


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

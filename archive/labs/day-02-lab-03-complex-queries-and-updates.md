# Lab 3: Complex Queries and Data Manipulations

**Day 2 · Module 4**  
**PPT:** `decks/pptx/MongoDB_Day2_Query_and_Transform_Data.pptx` — Module 4 section (Hands-On Lab: Complex Queries, Exercises 1–12 + Challenge)  
**Time:** 60–75 min  
**Difficulty:** Intermediate

**Objective:** Write filters, projections, array queries, and verified updates against live `training_store` documents.

**Prerequisite:** Reload the dataset so leftover Day 1 writes do not change counts.

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

Then in `mongosh`: `use training_store`

Slide examples that mention `Electronics`, `ELEC-1001`, `stock`, or `status: "Processing"` are **generic**. Use the commands in this guide.

**Companion in-class labs:** [Lab 4.1](../slide-exercises/module-04/exercise-4.15-lab-dataset-verification.md)–[Lab 4.10](../slide-exercises/module-04/exercise-4.24-lab-integrated-crud-challenge.md)

---

## Environment basics

**Demonstration environment:** Windows 10/11 · PowerShell · `mongosh`

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

---

## Steps from the training slides

### Step 1 — Affordable, available accessories (PPT Exercise 1)

**Do this:** Category `ACCESSORY`, `active: true`, price below 75 as Decimal128. Project sku, name, price. Sort price ascending.

```javascript
db.products.find(
  {
    category: "ACCESSORY",
    active: true,
    price: { $lt: NumberDecimal("75.00") }
  },
  { _id: 0, sku: 1, name: 1, price: 1 }
).sort({ price: 1 })
```

**Expected result:** `A410` (19.99), `A400` (24.99), `P1001` (49.99). `A500` is 249.99. `XBAD` has a **string** price, so it should not satisfy a Decimal128 `$lt`.

---

### Step 2 — Priority products (PPT Exercise 2)

**Do this:** Active products whose tags contain `clearance` **or** `premium`.

```javascript
db.products.find({
  active: true,
  $or: [
    { tags: "clearance" },
    { tags: "premium" }
  ]
})
```

**Expected result:** Includes `S290` (clearance), `L110` and `A500` (premium). `L190` has `clearance` but `active: false` — it must be absent.

---

### Step 3 — Price range (PPT Exercise 3)

**Do this:**

```javascript
db.products.find(
  {
    price: {
      $gte: NumberDecimal("40.00"),
      $lte: NumberDecimal("100.00")
    }
  },
  { _id: 0, sku: 1, name: 1, category: 1, price: 1 }
).sort({ price: -1 })
```

**Expected result:** Includes `S210` (89.99), `B300` (59.99), `P1001` (49.99), `S290` (44.99). `B310` (39.99) is below the floor. `S200` (129.99) is above the ceiling.

---

### Step 4 — Exclude selected categories (PPT Exercise 4)

**Do this:**

```javascript
db.products.find({
  category: { $nin: ["SHOE", "BOOK"] }
})
```

**Expected result:** Laptops and accessories only (including `XBAD`). No shoes or books.

---

### Step 5 — Customers in selected cities (PPT Exercise 5)

**Do this:** Use the nested address path, not `firstName`:

```javascript
db.customers.find(
  { "addresses.city": { $in: ["Toronto", "Montreal"] } },
  {
    _id: 0,
    customerNumber: 1,
    "name.first": 1,
    "name.last": 1,
    "contact.email": 1,
    addresses: 1
  }
)
```

**Expected result:** `C101` (Toronto) and `C412` (Montreal). Ottawa (`C515`) is absent.

---

### Step 6 — High-quantity inexpensive line (PPT Exercise 6)

**Do this:** `$elemMatch` so **the same item** has quantity ≥ 2 **and** `unitPrice` below 50:

```javascript
db.orders.find(
  {
    items: {
      $elemMatch: {
        quantity: { $gte: 2 },
        unitPrice: { $lt: NumberDecimal("50.00") }
      }
    }
  },
  { _id: 0, orderNumber: 1, items: 1, total: 1 }
)
```

**Expected result:** `O5001` matches because `A410` is qty 2 at 19.99. `O6302` has qty 2 of `S200` at 129.99 — it must **not** match. `O6401` has qty 2 of `L100` at 1299.99 — it must **not** match.

---

### Step 7 — Recent processing orders (PPT Exercise 7)

**Do this:** Fulfillment `PROCESSING` and `createdAt` on or after 1 August 2026:

```javascript
db.orders.find({
  fulfillmentStatus: "PROCESSING",
  createdAt: { $gte: ISODate("2026-08-01T00:00:00Z") }
}).sort({ createdAt: -1 })
```

**Expected result:** `O6401` (2026-09-18, PENDING), `O6302` (2026-09-07, PAID), `O6202` (2026-08-11, PAID). There is no order-level field named `status`.

---

### Step 8 — Guarded inventory update (PPT Exercise 8)

Catalog documents have no `stock` field. Add a working `stockQuantity` on `A410`, then decrement only if enough units remain.

**Do this:**

```javascript
db.products.updateOne(
  { sku: "A410" },
  { $set: { stockQuantity: 18 } }
)

db.products.findOne({ sku: "A410", stockQuantity: { $gte: 2 } })

db.products.updateOne(
  { sku: "A410", stockQuantity: { $gte: 2 } },
  {
    $inc: { stockQuantity: -2 },
    $currentDate: { updatedAt: true }
  }
)

db.products.findOne({ sku: "A410" }, { sku: 1, stockQuantity: 1, updatedAt: 1 })
```

**Expected result:** After the increment, `stockQuantity` is 16. If you rerun the guarded update with `$gte: 100`, `matchedCount` is 0 and stock does not change.

---

### Step 9 — Unique tags (PPT Exercise 9)

**Do this:**

```javascript
db.products.updateOne(
  { sku: "A410" },
  {
    $addToSet: { tags: { $each: ["featured", "office", "wireless"] } },
    $currentDate: { updatedAt: true }
  }
)

db.products.findOne({ sku: "A410" }, { sku: 1, tags: 1 })
```

**Expected result:** `wireless` was already present and is **not** duplicated. `featured` and `office` appear once.

---

### Step 10 — Remove discontinued tags (PPT Exercise 10)

**Do this:**

```javascript
db.products.updateMany(
  {},
  { $pull: { tags: { $in: ["discontinued", "temporary", "old-stock"] } } }
)

db.products.find({ tags: "discontinued" }, { sku: 1, tags: 1 })
```

**Expected result:** `L190` no longer lists `discontinued`. Other tags on `L190` (`clearance`, `refurbished`) remain.

---

### Step 11 — Ship a processing order and append history (PPT Exercise 11)

**Do this:** Update `O6202` only while it is still `PROCESSING`:

```javascript
db.orders.updateOne(
  { orderNumber: "O6202", fulfillmentStatus: "PROCESSING" },
  {
    $set: { fulfillmentStatus: "SHIPPED" },
    $push: {
      statusHistory: { status: "SHIPPED", changedAt: new Date() }
    },
    $currentDate: { updatedAt: true }
  }
)

db.orders.findOne(
  { orderNumber: "O6202" },
  { orderNumber: 1, fulfillmentStatus: 1, statusHistory: 1 }
)
```

**Expected result:** `fulfillmentStatus` is `SHIPPED`. `statusHistory` has one entry. A second run with the same filter matches **zero** documents — the status guard prevented a double ship.

---

### Step 12 — Rename a mistaken review field (PPT Exercise 12)

Do **not** rewrite existing `body` fields. Insert a throwaway review, then rename.

**Do this:**

```javascript
const p = db.products.findOne({ sku: "A400" })
const c = db.customers.findOne({ customerNumber: "C101" })

db.reviews.insertOne({
  productId: p._id,
  sku: "A400",
  customerId: c._id,
  rating: 4,
  title: "Lab rename fixture",
  reviewText: "Temporary field name for $rename practice.",
  createdAt: new Date()
})

db.reviews.find({ reviewText: { $exists: true } })

db.reviews.updateMany(
  { reviewText: { $exists: true }, body: { $exists: false } },
  { $rename: { reviewText: "body" } }
)

db.reviews.find({ sku: "A400", title: "Lab rename fixture" })
```

**Expected result:** After `$rename`, the fixture has `body` and no `reviewText`. Catalog reviews (`L100`, `L110`, …) still use `body`.

---

### Step 13 — Challenge query (PPT Challenge Query)

**Do this:** Active products in `BOOK` or `ACCESSORY`, price 15–80, tags include `wireless` or `database`, tags do not include `discontinued`. Project sku, name, category, price, tags. Sort category then price.

```javascript
db.products.find(
  {
    active: true,
    category: { $in: ["BOOK", "ACCESSORY"] },
    price: {
      $gte: NumberDecimal("15.00"),
      $lte: NumberDecimal("80.00")
    },
    tags: { $in: ["wireless", "database"], $nin: ["discontinued"] }
  },
  { _id: 0, sku: 1, name: 1, category: 1, price: 1, tags: 1 }
).sort({ category: 1, price: 1 })
```

**Expected result:** `A410` (wireless), `P1001` (wireless), `B310` (database), `B300` (database). `XBAD` is excluded (string price and `legacy` tag). `L190` is a laptop and inactive.

---

## Success criteria

- [ ] Accessory price filter used Decimal128 and skipped `XBAD`
- [ ] `$elemMatch` kept `O5001` and rejected `O6302` / `O6401`
- [ ] Order query used `fulfillmentStatus`, not `status`
- [ ] Guarded inventory update changed `A410` from 18 to 16
- [ ] Shipping `O6202` twice did not match the second time
- [ ] Challenge query returned four SKUs

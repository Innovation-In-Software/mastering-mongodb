# Lab 3 — Complex Queries and Updates

**Day:** 2 — Query and Transform Data · **Module:** 4, The MongoDB Query Language  
**Time:** 60–75 minutes  
**Difficulty:** Intermediate

**Deck:** `decks/pptx_new/MongoDB_Module04_The_MongoDB_Query_Language.pptx` — slide 50, "Lab 3 — Complex Queries and Updates"

**Objective:** Write filters, projections, array queries and verified updates against live `training_store` documents. Steps 1–7 read, steps 8–12 write and verify, step 13 is the challenge.

---

## What you will finish with

By the end of this lab you will have:

- Filters that compare money as Decimal128 and skip the planted `XBAD` string price
- A tag query that keeps only **active** products
- A price range sorted high to low, and a `$nin` category filter
- A dot-notation query on `addresses.city` and an `$elemMatch` query on order items
- An order query on `fulfillmentStatus` and `createdAt` (there is no order field named `status`)
- A **guarded** stock decrement on `A410` (18 → 16) that cannot oversell
- Tags changed with `$addToSet` and `$pull`, an order shipped exactly once, and a field renamed with `$rename`
- One precise challenge query that returns four SKUs

---

## Knowledge you need (from Module 4)

| Module 4 idea | Where it appears in this lab |
| --- | --- |
| **Implicit AND and projection** | Every step: commas combine conditions; `{ _id: 0, sku: 1, … }` keeps output short. |
| **Decimal128 comparisons** | Steps 1, 3 and 13: `NumberDecimal("75.00")` (same as `Decimal128("75.00")`). `XBAD`'s string price never matches. |
| **`$or` versus `$in`** | Step 2 uses `$or`; `tags: { $in: ["clearance", "premium"] }` is the shorter equivalent. |
| **`$nin`** | Steps 4 and 13. `$nin` also matches documents that lack the field. |
| **Dot notation through arrays** | Step 5: `"addresses.city"` checks every address. |
| **`$elemMatch`** | Step 6: both conditions on the **same** item. |
| **Date range** | Step 7: `createdAt` from 1 August 2026. |
| **Guarded update** | Steps 8 and 11: the business rule sits in the filter, so check and change are one atomic write. |
| **Array update operators** | Steps 9 and 10: `$addToSet` with `$each`, `$pull` with `$in`. |
| **Write results** | Every write step: read `matchedCount` and `modifiedCount` before trusting the change. |

---

## Before you start

### 1. Reload the dataset

The exercises and demos change data (for example, Exercise 4.3 creates `A700`). Reload so every count below is right. Run this in **PowerShell from the repository root**, not inside `mongosh`:

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

The script prints:

```text
Loaded training_store
customers: 6
products: 13
orders: 17
reviews: 6
paid orders: 13
```

### 2. Open the shell on training_store

```powershell
mongosh "mongodb://localhost:27017"
```

```javascript
use training_store
db.products.countDocuments({})   // 13
```

### 3. Use the real field names

Values are uppercase: `category: "ACCESSORY"`, `paymentStatus: "PAID"`, `fulfillmentStatus: "PROCESSING"`. Products have **no stock field** on a fresh load; step 8 creates `stockQuantity`. Older slide examples that say `Electronics`, `ELEC-1001`, `stock` or `status: "Processing"` are generic — use the commands in this guide.

### Environment basics

| Task | How |
| --- | --- |
| Terminal | ``Ctrl+` `` → PowerShell (bottom panel of Cursor or VS Code) |
| MongoDB shell | `mongosh` in the same terminal |
| Multi-line commands | Paste one whole command at a time; `mongosh` waits until the brackets close |
| Rerun a command | Up arrow in `mongosh` |

---

## Steps

Follow the steps in order: later steps depend on earlier writes (step 13 expects step 9's tags on A410).

### Step 1 — Affordable, available accessories

Category `ACCESSORY`, `active: true`, price below 75 as Decimal128. Project sku, name and price; sort by price ascending.

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

**Check:** three accessories, cheapest first. `A500` costs 249.99. `XBAD`'s price is a string, so it does not satisfy a Decimal128 `$lt`.

### Step 2 — Priority products

Active products whose tags contain `clearance` **or** `premium`.

```javascript
db.products.find(
  {
    active: true,
    $or: [
      { tags: "clearance" },
      { tags: "premium" }
    ]
  },
  { _id: 0, sku: 1, name: 1, tags: 1 }
)
```

**Check:** `L190` is tagged `clearance` but `active: false` — it must be absent. Try the same filter with `tags: { $in: ["clearance", "premium"] }`; the result is identical.

### Step 3 — Price range, most expensive first

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

**Check:** four products. `B310` (39.99) is below the floor and `S200` (129.99) is above the ceiling. `XBAD` is excluded by the range, so it cannot top this descending sort.

### Step 4 — Exclude selected categories

```javascript
db.products.find(
  { category: { $nin: ["SHOE", "BOOK"] } },
  { _id: 0, sku: 1, category: 1 }
)

db.products.countDocuments({ category: { $nin: ["SHOE", "BOOK"] } })
```

**Check:** laptops and accessories only, `XBAD` included. No shoes or books.

### Step 5 — Customers in selected cities

Use the nested address path (`addresses` is an array of documents):

```javascript
db.customers.find(
  { "addresses.city": { $in: ["Toronto", "Montreal"] } },
  {
    _id: 0,
    customerNumber: 1,
    "name.first": 1,
    "name.last": 1,
    "contact.email": 1,
    "addresses.city": 1
  }
)
```

**Check:** two customers. `C515` (Ottawa) is absent.

### Step 6 — High-quantity, inexpensive line items

Use `$elemMatch` so **the same item** has quantity ≥ 2 **and** `unitPrice` below 50:

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
  { _id: 0, orderNumber: 1, "items.sku": 1, "items.quantity": 1, "items.unitPrice": 1, total: 1 }
)
```

**Check:** three orders. `O6302` (S200 × 2 at 129.99), `O6401` (L100 × 2 at 1299.99) and `O6103` (B300 × 2 at 59.99) have quantity 2 of an item that costs 50 or more — they must **not** match.

### Step 7 — Recent processing orders

Fulfilment `PROCESSING` and `createdAt` on or after 1 August 2026, newest first:

```javascript
db.orders.find(
  {
    fulfillmentStatus: "PROCESSING",
    createdAt: { $gte: ISODate("2026-08-01T00:00:00Z") }
  },
  { _id: 0, orderNumber: 1, paymentStatus: 1, fulfillmentStatus: 1, createdAt: 1 }
).sort({ createdAt: -1 })
```

**Check:** three orders. There is no order-level field named `status` — `{ status: "Processing" }` returns nothing.

### Step 8 — Guarded inventory update

Catalog documents have no stock field. Add a working `stockQuantity` on `A410`, then decrement only if enough units remain.

```javascript
db.products.updateOne(
  { sku: "A410" },
  { $set: { stockQuantity: 18 } }
)

db.products.findOne({ sku: "A410", stockQuantity: { $gte: 2 } }, { _id: 0, sku: 1, stockQuantity: 1 })

db.products.updateOne(
  { sku: "A410", stockQuantity: { $gte: 2 } },
  {
    $inc: { stockQuantity: -2 },
    $currentDate: { updatedAt: true }
  }
)

db.products.findOne({ sku: "A410" }, { _id: 0, sku: 1, stockQuantity: 1, updatedAt: 1 })
```

Now prove the guard: rerun the decrement with a threshold that cannot be met.

```javascript
db.products.updateOne(
  { sku: "A410", stockQuantity: { $gte: 100 } },
  { $inc: { stockQuantity: -2 } }
)
```

**Check:** `stockQuantity` goes from 18 to 16. The guarded rerun returns `matchedCount: 0` and stock stays 16.

### Step 9 — Unique tags

```javascript
db.products.updateOne(
  { sku: "A410" },
  {
    $addToSet: { tags: { $each: ["featured", "office", "wireless"] } },
    $currentDate: { updatedAt: true }
  }
)

db.products.findOne({ sku: "A410" }, { _id: 0, sku: 1, tags: 1 })
```

**Check:** `wireless` was already present and is **not** duplicated. `featured` and `office` appear once.

### Step 10 — Remove discontinued tags

```javascript
db.products.updateMany(
  {},
  { $pull: { tags: { $in: ["discontinued", "temporary", "old-stock"] } } }
)

db.products.find({ tags: "discontinued" }, { _id: 0, sku: 1, tags: 1 })
db.products.findOne({ sku: "L190" }, { _id: 0, sku: 1, tags: 1 })
```

This is the one place the lab uses an empty filter on purpose: `$pull` changes only documents that contain a listed tag. Read the write result — how many matched, and how many were modified?

**Check:** `L190` no longer lists `discontinued`; its other tags (`clearance`, `refurbished`) remain.

### Step 11 — Ship a processing order and append history

Update `O6202` only while it is still `PROCESSING`:

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
  { _id: 0, orderNumber: 1, fulfillmentStatus: 1, statusHistory: 1 }
)
```

Run the same `updateOne` a **second** time and read the result.

**Check:** `fulfillmentStatus` is `SHIPPED` and `statusHistory` has one entry. The second run matches **zero** documents — the status guard prevents a double ship.

### Step 12 — Rename a mistaken review field

Do **not** rewrite existing `body` fields. Insert a throwaway review, then rename its field.

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

db.reviews.find({ reviewText: { $exists: true } }, { _id: 0, sku: 1, title: 1, reviewText: 1 })

db.reviews.updateMany(
  { reviewText: { $exists: true }, body: { $exists: false } },
  { $rename: { reviewText: "body" } }
)

db.reviews.find({ sku: "A400", title: "Lab rename fixture" }, { _id: 0, sku: 1, title: 1, body: 1, reviewText: 1 })
```

**Check:** the fixture now has `body` and no `reviewText`. The six catalog reviews (`L100`, `L110`, …) still use `body` and are untouched.

### Step 13 — Challenge query

Active products in `BOOK` or `ACCESSORY`, price 15–80, tags include `wireless` or `database`, tags do not include `discontinued`. Project sku, name, category, price and tags. Sort by category, then price. Try it yourself before you read the command.

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

**Check:** four SKUs. `XBAD` is excluded (string price and only a `legacy` tag). `L190` is a laptop and inactive.

---

## Success criteria

- [ ] The accessory price filter used Decimal128 and skipped `XBAD`
- [ ] Step 2 left out the inactive `L190`
- [ ] `$elemMatch` returned `O5001`, `O6201` and `O6305`, and rejected `O6302` and `O6401`
- [ ] The order query used `fulfillmentStatus`, not `status`
- [ ] The guarded inventory update changed `A410` from 18 to 16, and the `$gte: 100` rerun matched 0
- [ ] `$addToSet` did not duplicate `wireless`
- [ ] Shipping `O6202` a second time matched 0 documents
- [ ] The challenge query returned four SKUs: A410, P1001, B310, B300

---

## Troubleshooting

| Symptom | Likely cause and fix |
| --- | --- |
| Counts differ from this guide (for example 14 products) | Leftover writes from exercises or demos (A700, DEMO-1, …). Reload `load.js` from PowerShell and restart at step 1. |
| A price query returns nothing | The value is a number or a string instead of Decimal128. Use `NumberDecimal("75.00")`. |
| `XBAD` appears first in a descending price sort | Its price is the string `"49.99"`; strings sort after numbers, so descending puts it first. Add a price range or `price: { $type: "decimal" }`. |
| `{ category: "Accessory" }` or `{ status: "Processing" }` returns nothing | Values are uppercase and orders have no `status` field. Use `"ACCESSORY"` and `fulfillmentStatus: "PROCESSING"`. |
| Step 6 returns only `O5001`, or returns `O6302` | Only one or the other condition is inside `$elemMatch`, or dot notation was used. Put both `quantity` and `unitPrice` in one `$elemMatch`. |
| Step 8 guarded update shows `matchedCount: 0` | The `$set: { stockQuantity: 18 }` was skipped — products (L100 included) have no `stockQuantity` on a fresh load. Run the `$set` first. |
| Step 8 ends at 14 or lower | The decrement ran more than once. Reset with `$set: { stockQuantity: 18 }` and run it once. |
| Step 11 first run shows `matchedCount: 0` | O6202 was already shipped in an earlier attempt. That is the guard working; reload to repeat the step. |
| `SyntaxError: Identifier 'p' has already been declared` | Step 12 was pasted twice in the same session. Use new names (`p2`, `c2`) or open a new `mongosh`. |
| `E11000 duplicate key error` | You inserted a SKU or email that already exists. Reload, or pick an unused test value. |
| Step 13 returns three SKUs | Check the price bounds (15 and 80, inclusive) and that `category` uses `$in` for both `BOOK` and `ACCESSORY`. |

---

## Clean up

This lab changes A410, L190, O6202 and adds a review. Reload `load.js` before Module 5 so everyone's aggregation totals match.

## Next

Module 5 — The Aggregation Framework: today's filters become `$match` stages, and today's projections become `$project`.

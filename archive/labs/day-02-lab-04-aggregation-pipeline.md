# Lab 4: Build a Multi-Stage Aggregation Pipeline

**Day 2 · Module 5**  
**PPT:** `decks/pptx/MongoDB_Module05_The_Aggregation_Framework.pptx` (Hands-On Analytical Challenge)  
**Time:** 45–60 min  
**Difficulty:** Intermediate

**Objective:** Build one pipeline that filters completed sales, unwinds line items, joins products, groups by category, and returns a ranked report.

This is the outline hands-on: *Building an aggregation pipeline* (scheduled on Day 2 in this package so it sits next to the query language).

**Prerequisite:** Fresh `load.js` **or** accept that Lab 3 changed `O6202` and `A410`. For matching expected numbers, reload:

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

```javascript
use training_store
```

Slide examples that match `status: "Shipped"` are generic. Live orders use `paymentStatus` and `fulfillmentStatus`. Line items store `unitPrice` and `quantity` — there is no `items.lineTotal` field until you compute it.

**Companion labs:** [Lab 5.1](../slide-exercises/module-05/lab-5.1-aggregation-dataset-verification.md)–[Lab 5.10](../slide-exercises/module-05/lab-5.10-integrated-aggregation-challenge.md)

---

## Environment basics

**Demonstration environment:** Windows 10/11 · PowerShell · `mongosh`

---

## Business requirement (PPT)

Report the top-selling **product categories** for completed sales:

- Include only **PAID** orders that are **SHIPPED** or **DELIVERED**
- Expand line items
- Join each item to the current product (for category)
- Group by `product.category`
- Total units, total sales, distinct customers, sales per customer
- Keep categories with sales of at least 50
- Sort highest sales first; return the top five

---

## Steps from the training slides

### Step 1 — Confirm the input set

**Do this:**

```javascript
db.orders.countDocuments({
  paymentStatus: "PAID",
  fulfillmentStatus: { $in: ["SHIPPED", "DELIVERED"] }
})
```

**Expected result:** **10** orders (13 PAID minus PROCESSING and NEW). PROCESSING paid orders (`O6202`, `O6302`) are excluded until they ship.

---

### Step 2 — Filter, unwind, and compute line sales

**Do this:** Run only the first three stages and inspect two documents:

```javascript
db.orders.aggregate([
  {
    $match: {
      paymentStatus: "PAID",
      fulfillmentStatus: { $in: ["SHIPPED", "DELIVERED"] }
    }
  },
  { $unwind: "$items" },
  {
    $set: {
      lineSales: { $multiply: ["$items.quantity", "$items.unitPrice"] }
    }
  },
  { $limit: 2 }
])
```

**Expected result:** Each output document is one line. `lineSales` is a decimal (quantity × snapshot `unitPrice`).

---

### Step 3 — Join the product and group by category

**Do this:**

```javascript
db.orders.aggregate([
  {
    $match: {
      paymentStatus: "PAID",
      fulfillmentStatus: { $in: ["SHIPPED", "DELIVERED"] }
    }
  },
  { $unwind: "$items" },
  {
    $set: {
      lineSales: { $multiply: ["$items.quantity", "$items.unitPrice"] }
    }
  },
  {
    $lookup: {
      from: "products",
      localField: "items.productId",
      foreignField: "_id",
      as: "product"
    }
  },
  { $unwind: "$product" },
  {
    $group: {
      _id: "$product.category",
      totalUnitsSold: { $sum: "$items.quantity" },
      totalSales: { $sum: "$lineSales" },
      customers: { $addToSet: "$customerId" }
    }
  },
  {
    $set: {
      distinctCustomers: { $size: "$customers" },
      salesPerCustomer: { $divide: ["$totalSales", { $size: "$customers" }] }
    }
  },
  {
    $match: { totalSales: { $gte: NumberDecimal("50.00") } }
  },
  { $sort: { totalSales: -1 } },
  { $limit: 5 },
  {
    $project: {
      _id: 0,
      category: "$_id",
      totalUnitsSold: 1,
      totalSales: 1,
      distinctCustomers: 1,
      salesPerCustomer: 1
    }
  }
])
```

**Expected result:** `LAPTOP` is first (high unit prices: `L100` / `L110`). Other categories that clear 50 appear below. Empty `$lookup` arrays would mean a broken `productId` — none of the completed paid orders should fail the join.

---

### Step 4 — Prove one number

**Do this:** Spot-check laptop units from completed paid orders:

```javascript
db.orders.aggregate([
  {
    $match: {
      paymentStatus: "PAID",
      fulfillmentStatus: { $in: ["SHIPPED", "DELIVERED"] }
    }
  },
  { $unwind: "$items" },
  { $match: { "items.sku": { $in: ["L100", "L110", "L190"] } } },
  { $group: { _id: null, units: { $sum: "$items.quantity" } } }
])
```

**Expected result:** The unit count matches `totalUnitsSold` for `LAPTOP` in Step 3.

---

### Step 5 — Optional: `$explain` placement

**Do this:** If time remains, run the same pipeline with `.explain("executionStats")` (or wrap in `db.orders.aggregate(..., { explain: true })` depending on shell version) and note whether `$match` is first.

**Expected result:** The first stage is `$match`. Filtering after `$unwind` would expand more documents than needed.

---

## Success criteria

- [ ] Pipeline uses `paymentStatus` / `fulfillmentStatus`, not a single `status` field
- [ ] Line sales are computed, not read from a missing `lineTotal`
- [ ] `$unwind` comes after the order-level `$match`
- [ ] `$lookup` is after `$unwind` (item → product)
- [ ] Top category is `LAPTOP` on a fresh load
- [ ] One grouped metric was checked with a second pipeline or count

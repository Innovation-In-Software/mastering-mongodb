# Lab 2: Create and Populate the Sample Application

**Day 1 · Module 3**  
**PPT:** `decks/pptx/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx`  
**Time:** 50 min (load.js path) · 90 min (hand-insert path)  
**Difficulty:** Beginner

**Objective:** Put `training_store` on disk with `products`, `customers`, `orders`, and `reviews`, then justify embed vs reference from the documents you can see.

This is the outline hands-on: *Creating and populating collections against a sample application dataset.*

---

## Environment basics

**Demonstration environment:** Windows 10/11 · PowerShell · `mongosh` connected from Lab 1.

If Module 1 leftover documents remain, this lab **replaces** them with the Day 2 application model.

---

## Path A — Instructor load (time-boxed)

Use this when the afternoon must stay near 50 minutes.

### Step 1 — Load the dataset

**Do this:** From the course repository root in PowerShell (not inside `mongosh`):

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

**Expected result:** The script drops and recreates the four collections. No error on unique indexes (`sku`, `customerNumber`, `orderNumber`).

---

### Step 2 — Verify counts

**Do this:** In `mongosh`:

```javascript
use training_store
db.products.countDocuments({})
db.customers.countDocuments({})
db.orders.countDocuments({})
db.reviews.countDocuments({})
show collections
```

**Expected result:** products **13**, customers **6**, orders **17**, reviews **6**.

---

### Step 3 — Inspect the model

**Do this:**

```javascript
db.products.findOne({ sku: "L100" })
db.customers.findOne({ customerNumber: "C101" })
db.orders.findOne({ orderNumber: "O5001" })
db.reviews.findOne({ sku: "L100" })
```

**Expected result:** You can point to:

| Pattern | Where |
|---------|--------|
| Flexible schema | `L100.attributes` vs `S200.attributes` vs `B300.attributes` |
| Bounded embed | `C101.addresses` |
| Snapshot + reference | `O5001.items` (copied name/price) and `O5001.customerId` |
| Unbounded data stored separately | `reviews` — not an array on the product |
| Type exception | `XBAD.price` is a **string**, not Decimal128 |

---

## Path B — Hand insert (full)

If every laptop should type the core documents, complete these in order then run `load.js` at the **start of Day 2** to pick up the analytical volume (13 products, 17 orders):

1. [Lab 3.1 Create the sample database](../slide-exercises/module-03/lab-3.1-create-the-sample-database.md)
2. [Lab 3.2 Populate products](../slide-exercises/module-03/lab-3.2-populate-products.md)
3. [Lab 3.3 Populate customers](../slide-exercises/module-03/lab-3.3-populate-customers.md)
4. [Lab 3.4 Populate orders](../slide-exercises/module-03/lab-3.4-populate-orders.md)
5. [Lab 3.5 Query nested documents](../slide-exercises/module-03/lab-3.5-query-nested-documents.md)
6. [Lab 3.6 Add collection validation](../slide-exercises/module-03/lab-3.6-add-collection-validation.md)
7. [Lab 3.7 Validate the data model](../slide-exercises/module-03/lab-3.7-validate-the-data-model.md)

---

## Lab review questions (PPT “Lab Review Questions”)

Write one sentence each. Suggested answers are in [`scripts/module03_content_source.md`](../scripts/module03_content_source.md) §17 — try first.

1. Why are customer addresses embedded?
2. Why are product reviews stored separately?
3. Why does an order contain both `productId` and a copied product name?
4. What happens to old orders if the product price changes?
5. Should order items live in a separate collection?
6. Which BSON types should money and timestamps use?
7. Which relationships still need a second query or `$lookup`?
8. Which arrays are bounded, and which could grow without limit?

---

## Success criteria

- [ ] Four collections exist in `training_store`
- [ ] Counts match a fresh load **or** you completed Path B core inserts
- [ ] You can explain one embed choice and one reference choice from a real document
- [ ] You recorded that `XBAD.price` is the wrong type on purpose

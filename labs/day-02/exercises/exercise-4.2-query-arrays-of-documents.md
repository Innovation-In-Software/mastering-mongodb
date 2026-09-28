# Exercise 4.2 — Query Arrays of Documents

**Module 4** (The MongoDB Query Language) · Day 2 · **Checkpoint B**  
**Time:** 15 min · **Type:** hands-on in `mongosh` · **Difficulty:** Intermediate

**Deck:** `decks/pptx_new/MongoDB_Module04_The_MongoDB_Query_Language.pptx` — slide 47, "Exercise 4.2 — Query Arrays of Documents"

## Purpose

Prove the O5001 `$elemMatch` trap: show that dot notation on an array of documents lets **different** elements satisfy different conditions, and that `$elemMatch` makes **one** element satisfy them all.

## Prerequisites

- Module 4, Part 3 ("Querying Nested Fields" and "Querying Arrays of Documents with $elemMatch")
- A fresh load of `training_store` (O5001 must be unchanged). From the repository root, in PowerShell:

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

Then `use training_store`.

## Scenario

`O5001` holds `L100` × 1 and `A410` × 2. Show why dot notation is not enough.

```text
1  "items.sku": "L100"
2  "items.quantity": { $gte: 2 }
3  $elemMatch: L100 and qty ≥ 2
4  1 and 2 with dot notation
5  addresses $elemMatch:
   SHIPPING in Toronto
```

Look at the trap first:

```javascript
db.orders.findOne(
  { orderNumber: "O5001" },
  { _id: 0, orderNumber: 1, "items.sku": 1, "items.quantity": 1 }
)
```

## Tasks

### Task 1 — Run steps 1 and 2; list the orders

```javascript
// Step 1 — orders containing SKU L100
db.orders.find({ "items.sku": "L100" }, { _id: 0, orderNumber: 1 })

// Step 2 — orders with any item of quantity 2 or more
db.orders.find({ "items.quantity": { $gte: 2 } }, { _id: 0, orderNumber: 1 })
```

List every order number each step returns.

### Task 2 — Run steps 3 and 4 side by side

```javascript
// Step 3 — the SAME item is L100 with quantity 2 or more
db.orders.find(
  { items: { $elemMatch: { sku: "L100", quantity: { $gte: 2 } } } },
  { _id: 0, orderNumber: 1 }
)

// Step 4 — steps 1 and 2 combined with dot notation
db.orders.find(
  { "items.sku": "L100", "items.quantity": { $gte: 2 } },
  { _id: 0, orderNumber: 1 }
)
```

### Task 3 — Name the false positive and why

Which order appears in step 4 but not in step 3? Explain in one sentence which item satisfies each condition.

### Task 4 — Query addresses with `$elemMatch`

`addresses` on customers is also an array of documents. Find customers with a **shipping** address in Toronto:

```javascript
// Step 5
db.customers.find(
  { addresses: { $elemMatch: { type: "SHIPPING", city: "Toronto" } } },
  { _id: 0, customerNumber: 1, "name.first": 1, "name.last": 1 }
)
```

Address `type` values in this dataset are uppercase.

## Deliverable

| Step | Orders or customers returned |
| --- | --- |
| 1. `"items.sku": "L100"` | |
| 2. `"items.quantity": { $gte: 2 }` | |
| 3. `$elemMatch` L100 and qty ≥ 2 | |
| 4. Dot notation, both conditions | |
| 5. `addresses` `$elemMatch` | |
| The false positive, and why | |

## Expected outcome

The solution is revealed on the slide after the debrief. You are done when you can name the order that dot notation wrongly returns and say which two different items made it match.

## Success criteria

- [ ] Listed every order for steps 1 and 2 (not only the ones you expected)
- [ ] Wrote a correct `$elemMatch` on `items`
- [ ] Named the false positive without `$elemMatch` and explained it
- [ ] Queried `addresses` as an array of documents

## Next

[Exercise 4.3 — Perform an Upsert](exercise-4.3-perform-an-upsert.md)

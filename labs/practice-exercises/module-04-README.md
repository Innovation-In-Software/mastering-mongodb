# Module 4 — Practice exercise solutions

**Deck:** `decks/pptx_new/MongoDB_Module04_The_MongoDB_Query_Language.pptx`  
**Story:** the `training_store` online store (`datasets/training_store/load.js`)  
Attempt the slide activity first, then compare your answers here. Every result is from a fresh load of the dataset.

Official numbered checkpoints for this module:
[Exercise 4.1](../day-02/exercises/exercise-4.1-build-comparison-filters.md) ·
[Exercise 4.2](../day-02/exercises/exercise-4.2-query-arrays-of-documents.md) ·
[Exercise 4.3](../day-02/exercises/exercise-4.3-perform-an-upsert.md) ·
[Exercise 4.4](../day-02/exercises/exercise-4.4-correct-unsafe-operations.md).
Day 2 lab: [Lab 3 — Complex Queries and Updates](../day-02/lab3/LAB-3-GUIDE.md).

---

## Exercise: Predict the Sorted Result

**Slide 14** · **Time:** 10 minutes · **How to run:** two minutes to write a prediction, then run it on the instructor screen. Most people predict A500 first.

### Scenario

The five accessories cost 19.99, 24.99, 49.99 and 249.99 — and XBAD, whose price is stored as the string `"49.99"`.

```javascript
db.products.find(
  { category: "ACCESSORY" },
  { _id: 0, sku: 1, price: 1 }
).sort({ price: -1 })
 .limit(3)
```

### Tasks

1. Write the three SKUs you expect, in order.
2. Say where XBAD lands, and why.
3. Run it on the instructor's screen.
4. Change the filter so only Decimal128 prices sort.

### Solution

```text
{ sku: 'XBAD', price: '49.99' }
{ sku: 'A500', price: Decimal128('249.99') }
{ sku: 'P1001', price: Decimal128('49.99') }
```

| Task | Answer |
| --- | --- |
| Three SKUs | **XBAD, A500, P1001** |
| Where XBAD lands | **First.** MongoDB sorts mixed types by BSON type first, then value; numbers come before strings, so in a descending sort the string `"49.99"` lands above every Decimal128 price. |
| After XBAD | A500 at 249.99, then P1001 at 49.99. The limit stops there, so A400 (24.99) and A410 (19.99) are not shown. |
| Decimal128 only | Add `price: { $type: "decimal" }` to the filter → **A500, P1001, A400** |

```javascript
db.products.find(
  { category: "ACCESSORY", price: { $type: "decimal" } },
  { _id: 0, sku: 1, price: 1 }
).sort({ price: -1 }).limit(3)
```

### Why this is the answer

One bad document can top a price list. The real fix is to correct XBAD's price in the data; the course leaves it as a string on purpose, so the same trap appears in any descending price sort over all 13 products (XBAD first, then L110).

---

## Exercise: Turn a Business Question into a Filter

**Slide 23** · **Time:** 10 minutes · **How to run:** pairs, five minutes. Ask one pair to type their query on the instructor screen.

### Scenario

Merchandising asks: which active products are on clearance or premium? They want the SKU and name only.

```javascript
db.products.find(
  { /* your filter */ },
  { /* your projection */ }
)
```

### Tasks

1. Choose the fields and operators.
2. Write the filter and the projection.
3. Predict the SKUs before you run it.
4. Explain why L190 is not in the result.

### Solution

```javascript
db.products.find(
  { active: true, tags: { $in: ["clearance", "premium"] } },
  { _id: 0, sku: 1, name: 1 }
)
```

```text
{ sku: 'L110', name: 'Ultrabook' }
{ sku: 'S290', name: 'Clearance Shoe' }
{ sku: 'A500', name: 'Docking Station' }
```

| Task | Answer |
| --- | --- |
| Fields and operators | `active: true` plus `tags: { $in: [ … ] }` |
| Projection | `{ _id: 0, sku: 1, name: 1 }` |
| SKUs | **L110, S290 and A500** — L110 and A500 are premium, S290 is clearance |
| L190 | The Refurbished Laptop is tagged clearance but `active` is `false`, so the implicit AND removes it — exactly what the business asked for |

An `$or` with two tag conditions (`$or: [{ tags: "clearance" }, { tags: "premium" }]`) is also correct; `$in` is shorter because both alternatives use the same field. This is Day 2 Lab 3, step 2.

### Why this is the answer

Each phrase of the request becomes one condition: "active" → `active: true`, "clearance or premium" → one `$in` on `tags`, "SKU and name only" → the projection. Then check the result against the data.

---

## Exercise: Choose the Right Array Query

**Slide 28** · **Time:** 10 minutes · **How to run:** individually for five minutes, then compare in pairs. Run the four answers on the instructor screen.

### Scenario

The store team sends four requests. Pick containment, dot notation, `$all` or `$elemMatch` for each.

```text
A  Shoes available in size 9
B  Orders with L100 × 2 or more
C  Customers in Toronto or Montreal
D  Products tagged office AND premium
```

### Tasks

1. Choose the operator for each request.
2. Write each filter.
3. Predict the matching documents.
4. Say which one dot notation gets wrong.

### Solution

| Request | Tool | Filter | Result |
| --- | --- | --- | --- |
| A | Containment through a dotted path | `db.products.find({ "attributes.sizes": 9 })` | **S200, S210, S290** |
| B | `$elemMatch` | `db.orders.find({ items: { $elemMatch: { sku: "L100", quantity: { $gte: 2 } } } })` | **O6401** (Luis Romero, two laptops) |
| C | Dot notation with `$in` | `db.customers.find({ "addresses.city": { $in: ["Toronto", "Montreal"] } })` | **C101** (Aisha Khan), **C412** (Jordan Lee) |
| D | `$all` | `db.products.find({ tags: { $all: ["office", "premium"] } })` | **A500** (Docking Station) |

**Which one dot notation gets wrong: B.** `{ "items.sku": "L100", "items.quantity": { $gte: 2 } }` also returns **O5001**, because its L100 line has quantity 1 and its A410 line has quantity 2 — different elements satisfy different conditions.

For D, `{ tags: ["office", "premium"] }` would be an exact array match: it depends on order and length, and happens to match A500 only because its tags are stored in exactly that order. `$all` matches in any order. A400 is tagged `office` but not `premium`.

### Why this is the answer

Choose the array tool from the question: one value (containment), all of several values (`$all`), a nested path (dot notation), or one element meeting several conditions (`$elemMatch`).

# Exercise 1.3 — Explore a MongoDB Dataset

**Module 1** (Introduction to NoSQL Databases) · Day 1 · **Checkpoint C**  
**Time:** 25 min · **Type:** hands-on in `mongosh` (or follow on the instructor screen) · **Difficulty:** Beginner

**Deck:** `decks/pptx_new/MongoDB_Module01_Introduction_to_NoSQL_Databases.pptx` — slide 45, "Exercise 1.3 — Explore a MongoDB Dataset"

## Purpose

Navigate `training_store` and read real documents. You list databases and collections, read one product and one order, label the structures inside them (`_id`, scalars, embedded objects, arrays, dates, numbers, Booleans), and compare two products to see a flexible schema in practice.

## Prerequisites

- The instructor has MongoDB running (local or Atlas) and has loaded the `training_store` sample database from `datasets/training_store/load.js`.
- `mongosh` connected to the training instance, using the connection string your instructor shares.
- **No `mongosh` yet?** Follow on the instructor screen. Module 2 covers installation.

## Scenario

The instructor has loaded `training_store`: an online store with four collections of customers, products, orders and reviews. Your job is to walk the MongoDB hierarchy — deployment, database, collection, document, field — and read what a real document looks like.

## Tasks

### Task 1 — List the databases and collections

```javascript
show dbs
use training_store
show collections
```

Write down the databases and the collections you see. Check that the prompt now shows `training_store`.

### Task 2 — Read one product and one order

```javascript
db.products.findOne()
db.orders.findOne()
```

Read both documents carefully. Note the order's identifying number and how it refers to the customer.

### Task 3 — Label the structures

On the product and the order you retrieved, find and write down at least one example of each:

| Structure | Example from the product | Example from the order |
| --- | --- | --- |
| `_id` | | |
| Scalar field (string) | | |
| Embedded object | | |
| Array | | |
| Date | | |
| Numeric value | | |
| Boolean value | | |

Some cells may stay empty — note which document does **not** have a given structure.

### Task 4 — Compare two products' fields

First look at the first two products:

```javascript
db.products.find().limit(2)
```

Then compare a laptop with a book:

```javascript
db.products.find(
  { sku: { $in: ["L100", "B300"] } })
```

List the fields the two documents share, and the fields that appear on one and not the other.

### Task 5 — Answer the observation sheet

1. Which databases and collections were available?
2. What is the purpose of `_id`?
3. Which document contained an embedded object?
4. Which document contained an array?
5. Which fields differed between product documents?
6. How does the document structure resemble an application object?

Be ready to share one difference between a table row and a document.

## Deliverable

The completed Task 3 table and the six observation-sheet answers. Keep them — Module 3 builds on them.

## Expected outcome

- You found the collections `customers`, `orders`, `products` and `reviews`.
- You can describe `_id` as the unique document identifier.
- You can point to an embedded object and an array in the order.
- You can explain that products in one collection differ by their category attributes.
- You can state one difference between a table row and a document.

## Success criteria

- [ ] Navigated to `training_store` and listed its collections
- [ ] Retrieved and read a product document and an order document
- [ ] Identified `_id`, an embedded object, an array, a date, a number and a Boolean
- [ ] Compared a laptop and a book and named the differing fields
- [ ] Observation sheet is complete

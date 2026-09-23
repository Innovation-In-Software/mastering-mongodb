# Module 1 — Practice exercise solutions

**Deck:** `decks/pptx_new/MongoDB_Module01_Introduction_to_NoSQL_Databases.pptx`  
**Story:** the `training_store` online store (`datasets/training_store/load.js`)  
Attempt the slide activity first, then compare your answers here.

Official numbered checkpoints for this module:
[Exercise 1.1](../day-01/exercises/exercise-1.1-choose-the-data-model.md) ·
[Exercise 1.2](../day-01/exercises/exercise-1.2-rows-to-documents.md) ·
[Exercise 1.3](../day-01/exercises/exercise-1.3-explore-a-mongodb-dataset.md).

---

## Exercise: What Does One Order Page Cost?

**Slide 13** · **Time:** 10 minutes · **How to run:** pairs for five minutes, then compare. Point back to the "Challenges with Traditional Relational Models" diagram with its five tables.

### Scenario

The order page shows O6102: Luis Romero's Running Shoe and Wireless Keyboard, total 211.38. In the relational design on the challenges slide, that order lives in five tables.

### Tasks

1. List the tables the page must read.
2. Count the joins needed.
3. Name the key columns that link them.
4. Sketch what one order document would hold.

### Solution

| Task | Answer |
| --- | --- |
| Tables | `customers`, `addresses`, `orders`, `order_items`, `payments` |
| Joins | **Four** joins for five tables — **five** if the page also shows product names (add `products`) |
| Key columns | `customer_id` links customers to orders and addresses; `address_id` links the order to its address; `order_id` links items and payments; `product_id` links items to products |
| One document | The order with its items and shipping address embedded |

In `training_store`, O6102 really is one document:

```javascript
{
  orderNumber: "O6102",
  customerId: ObjectId("…"),               // reference to Luis Romero, C204
  items: [                                 // embedded
    { sku: "S200", name: "Running Shoe",      quantity: 1, unitPrice: Decimal128("129.99") },
    { sku: "P1001", name: "Wireless Keyboard", quantity: 1, unitPrice: Decimal128("49.99") }
  ],
  shippingAddress: { street: "400 Congress Avenue", city: "Austin", province: "Texas",
                     postalCode: "78701", country: "USA" },   // embedded
  paymentStatus: "PAID",                   // the payments table becomes a field
  fulfillmentStatus: "DELIVERED",
  subtotal: Decimal128("179.98"), tax: Decimal128("23.40"),
  shippingFee: Decimal128("8.00"), total: Decimal128("211.38")
}
```

Check it with `db.orders.findOne({ orderNumber: "O6102" })`.

### Why this is the answer

One page can hide many joins — a document shaped like the page needs one read. Part 3 of the module looks at this shape in detail.

---

## Exercise: Translate SQL Thinking into MongoDB

**Slide 29** · **Time:** 10 minutes · **How to run:** individually for five minutes, then compare in pairs. Accept any wording that uses collection, document, field and `_id` correctly.

### Scenario

A teammate describes `training_store` in relational terms:

```text
"The products table has 13 rows."
"Each row's key is product_id."
"Order lines live in order_items."
"We join them to show an order."
```

### Tasks

1. Rewrite each sentence in MongoDB terms.
2. Name the field that replaces `product_id`.
3. Say what replaces the `order_items` join.
4. Write the `mongosh` command that counts products.

### Solution

| Relational sentence | In MongoDB terms |
| --- | --- |
| "The products table has 13 rows." | The `products` **collection** holds 13 **documents**. |
| "Each row's key is product_id." | Each document's key is **`_id`** (an ObjectId in our dataset) — plus **`sku`** as a unique business key (the loader creates a unique index on `sku`). |
| "Order lines live in order_items." | There is no `order_items` collection: each order **embeds an `items` array**. |
| "We join them to show an order." | No join is needed — one read of the order document returns its lines. |

Counting products:

```javascript
use training_store
db.products.countDocuments()   // 13
```

### Why this is the answer

Speaking MongoDB's vocabulary is the first step to thinking in documents. The design change — embedding the lines instead of joining a separate table — matters more than the renamed words. If learners don't have `mongosh` yet, run the count on the instructor screen.

---

## Exercise: Predict the Query Result

**Slide 36** · **Time:** 5 minutes · **How to run:** give everyone two minutes to write a prediction, then run the query on the instructor screen.

### Scenario

`training_store` has three shoes: Running Shoe 129.99, Trail Shoe 89.99 and Clearance Shoe 44.99.

```javascript
db.products.find(
  { category: "SHOE",
    price: { $lt: 100 } },
  { name: 1, price: 1, _id: 0 }
).sort({ price: 1 })
```

### Tasks

1. Say which shoes match the filter.
2. Put them in the order `sort()` returns.
3. List the fields each result shows.
4. Check your answer on the instructor's screen.

### Solution

`mongosh` prints:

```javascript
[
  { name: 'Clearance Shoe', price: Decimal128('44.99') },
  { name: 'Trail Shoe', price: Decimal128('89.99') }
]
```

| Task | Answer |
| --- | --- |
| Matches | **Clearance Shoe (44.99)** and **Trail Shoe (89.99)**. Running Shoe is excluded: 129.99 is not under 100. |
| Order | `sort({ price: 1 })` is ascending — Clearance Shoe first, then Trail Shoe. |
| Fields | Only `name` and `price`; the projection hides `_id`. |
| On screen | Prices print as `Decimal128` values. MongoDB still compares them correctly with the number 100. |

### Why this is the answer

The first argument of `find()` is the filter (both conditions must hold), the second is the projection. Reading a query before running it is the fastest way to learn the query language; Module 4 covers queries in depth.

# Exercise 1.2 — solution (instructor)

**Module 1** · Day 1 · Checkpoint B  
**Type:** modeling on paper · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-1.2-rows-to-documents.md`](../exercise-1.2-rows-to-documents.md) · Deck slide 44

## Running it

Twenty minutes. Learners write the document in a scratch file; MongoDB is optional.

## Task 1 — Tables and join keys

- Three tables: **Customer**, **Order**, **Order items**.
- Join `Customer` to `Order` on `customer_id`, then `Order` to `Order items` on `order_id`.
- Fields needed to show O5001: order id, status, total; customer id, name, email; for each line: product id, product name, quantity, price.
- The order total is 110.00 and there are two line items (2 × 25.00 + 1 × 60.00 = 110.00).

## Task 2 — Order header

```javascript
{ orderId: "O5001", status: "PLACED", total: 110.00 }
```

## Task 3 — Expected document

```javascript
{
  _id: "O5001",
  customer: {
    customerId: "C101",
    name: "Aisha Khan",
    email: "aisha@example.com"
  },
  items: [
    { productId: "P10", productName: "Keyboard", quantity: 2, price: 25.00 },
    { productId: "P22", productName: "Mouse",    quantity: 1, price: 60.00 }
  ],
  status: "PLACED",
  total: 110.00
}
```

Accept any field names that keep this shape: `_id` of `"O5001"`, a nested `customer` object, an `items` array of two lines, `status` and `total`. An `ObjectId` `_id` with a separate `orderId: "O5001"` field is also acceptable.

If a learner inserts it in `mongosh`, point out the course habit from the "Anatomy of a MongoDB Document" slide: money is stored as `Decimal128`, never as strings. A mongosh-ready version:

```javascript
use module1_scratch
db.orders.insertOne({
  _id: "O5001",
  customer: { customerId: "C101", name: "Aisha Khan", email: "aisha@example.com" },
  items: [
    { productId: "P10", productName: "Keyboard", quantity: 2, price: Decimal128("25.00") },
    { productId: "P22", productName: "Mouse",    quantity: 1, price: Decimal128("60.00") }
  ],
  status: "PLACED",
  total: Decimal128("110.00")
})
db.orders.findOne({ _id: "O5001" })
```

Clean up afterwards with `db.dropDatabase()` while `module1_scratch` is selected. Do not insert into `training_store`.

## Task 4 — Snapshot versus stale

| Question | Answer |
| --- | --- |
| Email embedded or referenced? | Either is defensible. Embedding a customer snapshot (id, name, email) serves "show the order in one read"; referencing avoids stale copies. |
| Purchase-time or current price? | **Purchase-time price.** It is a deliberate historical snapshot: the order must show what the customer actually paid, even if the catalog price changes. |
| Aisha changes her email? | The embedded email in this order **goes stale** — it still shows the old address unless the application updates it. For an order, that is often acceptable (it records the contact at purchase time). |
| Historical snapshot fields | Item `price`, `productName`, and the customer `name`/`email` as they were when the order was placed. |
| Main query | **Get order O5001 in one read** — no joins. |

## Dataset note (correction to the older guide)

The worksheet's O5001 is its own small example. The O5001 in the loaded `training_store` (from `datasets/training_store/load.js`) is **different**:

- `orderNumber: "O5001"` with an ObjectId `_id`
- `items`: 1 × Business Laptop (L100, `unitPrice` 1299.99) and 2 × Wireless Mouse (A410, `unitPrice` 19.99)
- `paymentStatus: "PENDING"`, `fulfillmentStatus: "NEW"`, `total` 1514.17
- The customer is a `customerId` **reference** to Aisha (C101), not an embedded customer

Both choices are valid. The deck's rows-to-documents diagram embeds a customer snapshot (the shape this exercise asks for); `training_store` makes the other choice and references the customer. Learners see the dataset's O5001 in Exercise 1.3.

## Debrief points

- Some duplication is intentional when it serves the access pattern and preserves history.
- Line items that are always read with the order belong **inside** the order as an array.
- Decide embedding from the main query: here, "get O5001 in one read".

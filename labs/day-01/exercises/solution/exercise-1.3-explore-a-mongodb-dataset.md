# Exercise 1.3 — solution (instructor)

**Module 1** · Day 1 · Checkpoint C  
**Type:** hands-on in `mongosh` · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-1.3-explore-a-mongodb-dataset.md`](../exercise-1.3-explore-a-mongodb-dataset.md) · Deck slide 45

## Before class

Load the dataset (it drops and recreates the four collections):

```powershell
mongosh "mongodb://localhost:27017" datasets/training_store/load.js
```

For Atlas, use the cluster's SRV connection string with your own database user — never paste a real password into shared materials. The script prints:

```text
Loaded training_store
customers: 6
products: 13
orders: 17
reviews: 6
paid orders: 13
```

If learners don't have `mongosh` yet, run every command on the instructor screen; Module 2 installs it.

## Task 1 — Databases and collections

- `show dbs` lists `training_store` beside `admin`, `config` and `local` (Atlas may show other databases instead of `config`/`local`).
- After `use training_store`, the prompt shows `training_store`.
- `show collections` lists **customers, orders, products, reviews**. (The older guide listed only three; `reviews` is the fourth.)

## Task 2 — The documents they will see

On a fresh load, `findOne()` returns the first inserted document in each collection.

`db.products.findOne()` — **L100, Business Laptop** (ObjectId value will differ):

```javascript
{
  _id: ObjectId('…'),
  sku: 'L100',
  name: 'Business Laptop',
  category: 'LAPTOP',
  price: Decimal128('1299.99'),
  attributes: { processor: 'Intel Core i7', memoryGB: 16, storageGB: 512, screenSizeInches: 14 },
  tags: [ 'business', 'portable' ],
  active: true,
  createdAt: ISODate('2026-08-20T09:00:00.000Z')
}
```

`db.orders.findOne()` — **O5001** (abridged):

```javascript
{
  _id: ObjectId('…'),
  orderNumber: 'O5001',
  customerId: ObjectId('…'),          // reference to Aisha Khan, C101
  items: [
    { productId: ObjectId('…'), sku: 'L100', name: 'Business Laptop', quantity: 1, unitPrice: Decimal128('1299.99') },
    { productId: ObjectId('…'), sku: 'A410', name: 'Wireless Mouse',  quantity: 2, unitPrice: Decimal128('19.99') }
  ],
  shippingAddress: { street: '100 King Street', city: 'Toronto', province: 'Ontario', postalCode: 'M5X 1A9', country: 'Canada' },
  paymentStatus: 'PENDING',
  fulfillmentStatus: 'NEW',
  subtotal: Decimal128('1339.97'),
  tax: Decimal128('174.20'),
  total: Decimal128('1514.17'),
  internalNotes: '…',
  createdAt: ISODate('2026-09-20T14:30:00.000Z')
}
```

Correction to the older guide: the order has **no embedded `customer`** object. The customer is a `customerId` reference; the embedded objects are `shippingAddress` and each element of `items`.

## Task 3 — Structure labels

| Structure | Product (L100) | Order (O5001) |
| --- | --- | --- |
| `_id` | ObjectId | ObjectId (`orderNumber` is the business key) |
| Scalar string | `sku`, `name`, `category` | `orderNumber`, `paymentStatus`, `fulfillmentStatus` |
| Embedded object | `attributes` | `shippingAddress` (and each `items` element) |
| Array | `tags` | `items` |
| Date | `createdAt` | `createdAt` |
| Numeric | `price` (Decimal128), `attributes.memoryGB` (number) | `total`, `subtotal`, `tax` (Decimal128), `items.quantity` |
| Boolean | `active: true` | none — the order has no Boolean field |
| Reference | — | `customerId`, `items.productId` (ObjectIds pointing to other collections) |

## Task 4 — Comparing products

- On a fresh load, `db.products.find().limit(2)` usually returns the **two laptops, L100 and L110**, which share the same fields — so it doesn't show the difference. (Correction: the older guide implied this command returns a laptop and a book.) That is why the slide adds the `$in` query.
- `db.products.find({ sku: { $in: ["L100", "B300"] } })` returns Business Laptop (L100) and MongoDB Fundamentals (B300).
  - **Shared fields:** `_id`, `sku`, `name`, `category`, `price`, `attributes`, `tags`, `active`, `createdAt`.
  - **Laptop only:** `attributes.processor`, `attributes.memoryGB`, `attributes.storageGB`, `attributes.screenSizeInches`.
  - **Book only:** `attributes.author`, `attributes.isbn`, `attributes.language`.
- Extra examples for fast groups: B310 and P1001 have a `discountPrice`; L190 has `legacyName`; A410 has `temporaryNote`; shoes have `attributes.sizes` as an array. XBAD (Legacy Cable Pack) has no `attributes` and a price stored as a string — a deliberate data-quality fixture for Module 4.

## Task 5 — Observation sheet answers

1. **Databases and collections:** `training_store` (plus `admin`, `config`, `local`); collections `customers`, `orders`, `products`, `reviews`.
2. **Purpose of `_id`:** the unique identifier of a document within its collection; MongoDB adds an ObjectId if you don't supply one.
3. **Embedded object:** both — the product's `attributes`, the order's `shippingAddress` (and each line in `items`).
4. **Array:** both — the product's `tags`, the order's `items`.
5. **Fields that differed:** the category attributes — laptop `processor`/`memoryGB`/`storageGB`/`screenSizeInches` versus book `author`/`isbn`/`language`.
6. **Resembles an application object:** one order document holds its lines and shipping address together, the way the order page shows it — nested fields, arrays and real types (Decimal128, Date, Boolean) in one record.

**One row-versus-document difference** (any of): a document can hold nested objects and arrays a row can't; documents in one collection can have different fields; one document replaces several joined rows.

## Debrief points

- A document looks like an application object: nested fields, arrays and real types in one record.
- Flexible schema is visible in one collection — laptops and books carry different attributes.
- `training_store` references the customer from the order but embeds the line items — the embed-or-reference choice from Part 3. Module 3 turns this into a modeling method.

# Lab 2 solution — Create and Populate training_store

Instructor reference: the expected output of every step in [LAB-2-GUIDE.md](../LAB-2-GUIDE.md). Deck slide 51. Values come from `datasets/training_store/load.js`; mongosh output is trimmed (`…`), and `ObjectId` / `new Date()` values differ on every machine.

Counts are always written in the order **products · customers · orders · reviews**.

| Path | Counts after the step sequence |
| --- | --- |
| A — load.js | **13 · 6 · 17 · 6** (13 orders PAID) |
| B — by hand | **3 · 1 · 1 · 0** (+ `validated_products`: 1) |

---

## Path A

### A1 — Load

```text
Loaded training_store
customers: 6
products: 13
orders: 17
reviews: 6
paid orders: 13
Module 4 fixtures: XBAD string price; C204 phone null; C515 missing phone; O5001 elemMatch trap; O6401 L100 qty 2.
Do not insert sku A600, A610, A611, A612, A700, A800, A900, TEMP-100 — Module 4 labs create those.
```

No error on the unique indexes. The script drops only the four application collections.

### A2 — Counts

```text
13
6
17
6
customers
orders
products
reviews
```

(`validated_products` also appears if Step 6 was run earlier.)

### A3 — Inspect

```javascript
// db.products.findOne({ sku: "L100" })
{ _id: ObjectId('…'), sku: 'L100', name: 'Business Laptop', category: 'LAPTOP',
  price: Decimal128('1299.99'),
  attributes: { processor: 'Intel Core i7', memoryGB: 16, storageGB: 512, screenSizeInches: 14 },
  tags: [ 'business', 'portable' ], active: true,
  createdAt: ISODate('2026-08-20T09:00:00.000Z') }

// db.customers.findOne({ customerNumber: "C101" })
{ _id: ObjectId('…'), customerNumber: 'C101', name: { first: 'Aisha', last: 'Khan' },
  contact: { email: 'aisha@example.com', phone: '+1-555-0100' },
  addresses: [ { type: 'SHIPPING', street: '100 King Street', city: 'Toronto',
                 province: 'Ontario', postalCode: 'M5X 1A9', country: 'Canada' } ],
  preferences: { newsletter: true, language: 'English' }, status: 'ACTIVE',
  createdAt: ISODate('2026-09-01T10:00:00.000Z') }

// db.orders.findOne({ orderNumber: "O5001" })
{ _id: ObjectId('…'), orderNumber: 'O5001', customerId: ObjectId('…'),   // C101's _id
  items: [
    { productId: ObjectId('…'), sku: 'L100', name: 'Business Laptop', quantity: 1,
      unitPrice: Decimal128('1299.99') },
    { productId: ObjectId('…'), sku: 'A410', name: 'Wireless Mouse', quantity: 2,
      unitPrice: Decimal128('19.99') } ],
  shippingAddress: { street: '100 King Street', city: 'Toronto', province: 'Ontario',
                     postalCode: 'M5X 1A9', country: 'Canada' },
  paymentStatus: 'PENDING', fulfillmentStatus: 'NEW',
  subtotal: Decimal128('1339.97'), tax: Decimal128('174.20'), total: Decimal128('1514.17'),
  internalNotes: 'Awaiting payment confirmation. …',
  createdAt: ISODate('2026-09-20T14:30:00.000Z') }

// db.reviews.findOne({ sku: "L100" })
{ _id: ObjectId('…'), productId: ObjectId('…'), sku: 'L100', customerId: ObjectId('…'),
  rating: 5, title: 'Excellent for travel',
  body: 'Light, quiet, and the battery lasts a full workday.',
  createdAt: ISODate('2026-09-21T11:00:00.000Z') }

// db.products.findOne({ sku: "XBAD" }, { _id: 0, sku: 1, price: 1 })
{ sku: 'XBAD', price: '49.99' }
```

---

## Path B

### Step 1 — Create the collections

```text
switched to db training_store
true          (×4 — the drop() calls; a collection that did not exist may print false)
{ ok: 1 }     (×4)
customers
orders
products
reviews
```

### Step 2 — Products

```javascript
{ acknowledged: true,
  insertedIds: { '0': ObjectId('…'), '1': ObjectId('…'), '2': ObjectId('…') } }
```

`db.products.find()` returns L100, S200 and B300 with `Decimal128` prices and `attributes` that differ by category. `db.products.countDocuments()` → `3`.

### Step 3 — Customers

```javascript
{ acknowledged: true, insertedId: ObjectId('…') }
```

`findOne` returns C101 with `name`, `contact`, one `SHIPPING` address in Toronto, `preferences`, `status: 'ACTIVE'` and today's `createdAt`.

### Step 4 — Orders

`customer._id` prints `ObjectId('…')`; `product.price` prints `Decimal128('1299.99')`.

```javascript
{ acknowledged: true, insertedId: ObjectId('…') }
// findOne:
{ _id: ObjectId('…'), orderNumber: 'O5001', customerId: ObjectId('…'),
  items: [ { productId: ObjectId('…'), sku: 'L100', name: 'Business Laptop',
             quantity: 1, unitPrice: Decimal128('1299.99') } ],
  shippingAddress: { street: '100 King Street', city: 'Toronto', … },
  paymentStatus: 'PENDING', fulfillmentStatus: 'NEW',
  subtotal: Decimal128('1299.99'), tax: Decimal128('169.00'), total: Decimal128('1468.99'),
  createdAt: ISODate('…') }
true
```

Tax is 13 % of 1299.99 = 168.9987, rounded to 169.00.

Counts now: **3 · 1 · 1 · 0**.

---

## Step 5 — Nested queries (both paths)

| Query | Path B returns | Path A returns | Why |
| --- | --- | --- | --- |
| `{ category: "LAPTOP" }` | L100 | L100, L110, L190 | Core field |
| `{ "attributes.memoryGB": 16 }` | L100 | L100 (L110 has 32, L190 has 8) | Dotted path into an embedded document |
| `{ tags: "technology" }` | B300 | B300 | Matches any element of the array |
| `{ "addresses.city": "Toronto" }` | C101 | C101 | Dotted path through an array of documents |
| `{ "items.sku": "L100" }` | O5001 | O5001, O6101, O6301, O6401 | Same, on order items |

Optional `$lookup` (Path A):

```javascript
[ { rating: 5, title: 'Excellent for travel', productName: 'Business Laptop' } ]
```

`getIndexes()` after `load.js`:

| Collection | Indexes |
| --- | --- |
| products | `_id_`, `sku_unique` `{ sku: 1 }` |
| customers | `_id_`, `customerNumber_unique` `{ customerNumber: 1 }`, `email_unique` `{ 'contact.email': 1 }` |
| orders | `_id_`, `orderNumber_unique` `{ orderNumber: 1 }` |

On the hand-built core every collection has only `_id_`.

---

## Step 6 — Validation (both paths)

```javascript
true                 // drop (false if it did not exist)
{ ok: 1 }            // createCollection
{ acknowledged: true, insertedId: ObjectId('…') }   // A100 valid insert
```

The invalid insert:

```text
Uncaught:
MongoServerError: Document failed validation
Additional information: {
  failingDocumentId: ObjectId('…'),
  details: {
    operatorName: '$jsonSchema',
    schemaRulesNotSatisfied: [
      { operatorName: 'properties',
        propertiesNotSatisfied: [
          { propertyName: 'price',  details: [ { operatorName: 'bsonType',
              specifiedAs: { bsonType: 'decimal' }, reason: 'type did not match',
              consideredValue: '39.99', consideredType: 'string' } ] },
          { propertyName: 'active', details: [ { operatorName: 'bsonType',
              specifiedAs: { bsonType: 'bool' }, reason: 'type did not match',
              consideredValue: 'yes', consideredType: 'string' } ] } ] },
      { operatorName: 'required',
        specifiedAs: { required: [ 'sku', 'name', 'category', 'price', 'active', 'createdAt' ] },
        missingProperties: [ 'createdAt' ] } ] } }
```

Exact formatting varies by server and mongosh version; the three failures are always `price` type, `active` type and missing `createdAt`. `minimum: 0` is not reported because it applies only to numbers. `db.validated_products.countDocuments()` → `1`.

---

## Step 7 — Model review (both paths)

### Checklist — expected ticks

| Item | Evidence in training_store |
| --- | --- |
| Accessed together, stored together | O5001 holds items, totals, shipping address and statuses |
| Arrays bounded | `addresses` (1 each), `items` (1–3), `tags` (1–3); reviews are a separate collection |
| Money | `Decimal128` on `price`, `unitPrice`, `subtotal`, `tax`, `total` — except XBAD's string price (deliberate) |
| Timestamps | `createdAt` is a Date everywhere |
| Required fields | Product core: `sku`, `name`, `category`, `price`, `active`, `createdAt` (enforced only on `validated_products`) |
| Deliberate relationships | Embed: `addresses`, `items`, `shippingAddress`. Reference: `customerId`, `items[].productId`, `reviews.productId` / `customerId` |
| Snapshots | `items[].sku`, `name`, `unitPrice`; `shippingAddress` |
| Collection names | Plural, lower case: `products`, `customers`, `orders`, `reviews` |
| Field names | camelCase throughout: `customerId`, `createdAt`, `paymentStatus`, `fulfillmentStatus` |
| Main queries | Product by `sku`, order by `orderNumber`, profile by `customerNumber`, history by `customerId`, reviews by `productId` |

Typical improvements: the planned indexes `{ category: 1, price: 1 }`, `{ customerId: 1, createdAt: -1 }` and `{ productId: 1, createdAt: -1 }` (Module 6); a validator on `orders`; `ratingAvg` / `reviewCount` on products (Computed pattern).

### Review questions — suggested answers

1. Addresses are bounded and normally read with their customer.
2. Reviews can grow without limit and exist as independent records.
3. `productId` identifies the product; the copied `name` (and `unitPrice`) preserves the order's history.
4. Nothing — the order keeps its `unitPrice`; O5001 still shows 1299.99 for L100.
5. Normally no: items belong to one order, are bounded and are read with it.
6. `Decimal128` for money; BSON Date for timestamps.
7. Orders → customers (`customerId`) and reviews → products (`productId`) need a second query or `$lookup`. Reviews copy `sku`, so "reviews for L100" needs no join.
8. Bounded: `addresses`, `items`, `tags`. Could grow without limit: a product's reviews and a customer's order history — which is why both are separate collections.

---

## Instructor notes

- Path A takes about 50 minutes (load.js, then Steps 5–7); Path B about 90.
- Whichever path ran, reload `load.js` at the start of Day 2 so Modules 4 and 5 have the full data.
- Do not let anyone "fix" XBAD — Module 4's `$type` lab needs it.

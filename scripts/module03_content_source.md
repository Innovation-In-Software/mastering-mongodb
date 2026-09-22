# Module 3: Data Modeling with MongoDB

Data modeling determines how application data will be organized, stored, connected and retrieved.

In a relational database, design commonly begins with entities, tables and normalization. In MongoDB, design should begin with the application’s most important operations:

* What information is read together?
* What information is updated together?
* Which queries run most frequently?
* How large can each record become?
* Which relationships are one-to-one, one-to-many or many-to-many?

The central principle is:

> Data that is accessed together should usually be stored together.

For this module, we will use the `training_store` e-commerce application with four business areas:

* Products
* Customers
* Orders
* Reviews

---

# 1. Databases, Collections and Documents

MongoDB organizes data using the following hierarchy:

```text
MongoDB deployment
└── Database: training_store
    ├── Collection: products
    ├── Collection: customers
    ├── Collection: orders
    └── Collection: reviews
```

## Database

A database is a logical container for related collections.

```javascript
use training_store
```

The command selects the database. MongoDB physically creates it after data is written.

Check the current database:

```javascript
db
```

## Collection

A collection contains related documents. It is approximately comparable to a relational table, although documents in a collection can have flexible structures.

Examples:

```text
products
customers
orders
reviews
```

Create a collection explicitly:

```javascript
db.createCollection("products")
```

MongoDB can also create it implicitly:

```javascript
db.customers.insertOne({
  firstName: "Aman",
  lastName: "Singh"
})
```

If `customers` does not exist, MongoDB creates it during the insertion.

## Document

A document is a set of field-value pairs. It represents a business object such as one product, customer or order.

```javascript
{
  _id: ObjectId("..."),
  name: "Wireless Mouse",
  category: "Electronics",
  price: NumberDecimal("39.99"),
  stock: 120,
  active: true
}
```

A document is comparable to a relational row, but it can also contain:

* Nested objects
* Arrays
* Objects inside arrays
* Arrays inside objects
* Different fields from other documents

## Field

A field is a named piece of information inside a document:

```javascript
{
  name: "Wireless Mouse",
  price: NumberDecimal("39.99")
}
```

Here, `name` and `price` are fields.

## The `_id` field

Every MongoDB document must have a unique `_id`.

If the application does not supply one, MongoDB normally generates an `ObjectId`:

```javascript
{
  _id: ObjectId("68f100a93e43...")
}
```

The `_id` field:

* Uniquely identifies a document
* Has a unique index automatically
* Cannot be changed after insertion
* Can contain an `ObjectId`, string, number or another suitable unique value

---

# 2. BSON and Varied Data Types

MongoDB stores documents using BSON, or Binary JSON. BSON supports JSON-style structures plus additional data types.

## Common BSON types

| Type              | Example                           | Typical use                         |
| ----------------- | ---------------------------------- | ------------------------------------ |
| String            | `"Electronics"`                   | Names and descriptions              |
| Integer           | `120`                             | Quantity and counters               |
| Decimal128        | `NumberDecimal("39.99")`          | Financial values                    |
| Double            | `4.7`                             | Measurements and approximate values |
| Boolean           | `true`                            | Status flags                        |
| Date              | `ISODate("2026-09-22T10:00:00Z")` | Dates and timestamps                |
| ObjectId          | `ObjectId("...")`                 | Document identifiers                |
| Array             | `["wireless", "mouse"]`           | Multiple values                     |
| Embedded document | `{ city: "Brampton" }`            | Structured nested data              |
| Null              | `null`                            | Known but absent values             |

## Example with several data types

```javascript
{
  _id: ObjectId("..."),
  name: "Wireless Mouse",
  price: NumberDecimal("39.99"),
  stock: 120,
  active: true,
  createdAt: ISODate("2026-09-22T10:00:00Z"),
  tags: ["wireless", "computer-accessory"],
  specifications: {
    connection: "Bluetooth",
    colour: "Black",
    rechargeable: true
  }
}
```

## Selecting appropriate types

Use types that represent the business meaning accurately.

For example:

```javascript
// Poor choices
{
  price: "39.99",
  stock: "120",
  active: "yes",
  createdAt: "September 22, 2026"
}
```

These strings make calculations, comparisons and sorting more difficult.

Better choices are:

```javascript
{
  price: NumberDecimal("39.99"),
  stock: 120,
  active: true,
  createdAt: ISODate("2026-09-22T10:00:00Z")
}
```

For currency, `Decimal128` is often preferable to floating-point values because it avoids many binary floating-point precision issues.

---

# 3. Designing Schemas Around Access Patterns

MongoDB has a flexible schema, but flexible does not mean unplanned.

A good schema supports the application’s common reads and writes efficiently.

## Step 1: Identify business entities

For `training_store`, the main entities are:

```text
Product
Customer
Order
Review
```

## Step 2: Identify relationships

```text
Customer 1 ─── places ─── many Orders
Customer 1 ─── writes ─── many Reviews
Product  1 ─── receives ─ many Reviews
Order    1 ─── contains ─ many Order Items
```

## Step 3: Identify important operations

Common access patterns might include:

1. Find a product by SKU.
2. Browse products by category.
3. Search products within a price range.
4. Display one customer’s profile and addresses.
5. Display one order with all purchased items.
6. Show a customer’s order history.
7. Display reviews for one product.
8. Calculate the average product rating.
9. Update product inventory.
10. Change an order’s status.

These operations should influence the document structures.

## Step 4: Estimate data growth

Ask:

* How many addresses can one customer have?
* How many items can one order contain?
* How many reviews can one product receive?
* Does the related data grow without a practical limit?
* How frequently does it change?
* Could the document approach MongoDB’s document-size limit?

A small, bounded list may be embedded. A large or continuously growing list is usually better stored separately.

---

# 4. Product Schema Design

Different product categories can contain different specifications.

An electronics product:

```javascript
{
  sku: "ELEC-1001",
  name: "Wireless Mouse",
  category: "Electronics",
  price: NumberDecimal("39.99"),
  stock: 120,
  specifications: {
    connection: "Bluetooth",
    colour: "Black",
    rechargeable: true
  }
}
```

A book:

```javascript
{
  sku: "BOOK-2001",
  name: "MongoDB Fundamentals",
  category: "Books",
  price: NumberDecimal("49.99"),
  stock: 75,
  specifications: {
    author: "A. Singh",
    isbn: "978-1234567890",
    pages: 420
  }
}
```

Both documents belong in `products`, but their `specifications` differ.

This design works when:

* All documents represent products.
* The application shares common operations across them.
* Category-specific attributes vary.
* The common fields remain consistent.

Avoid inconsistent names such as:

```javascript
// Inconsistent
{ productName: "Mouse" }
{ item_name: "Keyboard" }
{ title: "Monitor" }
```

Prefer:

```javascript
{ name: "Mouse" }
{ name: "Keyboard" }
{ name: "Monitor" }
```

---

# 5. Embedding Versus Referencing

MongoDB represents relationships using two primary approaches:

* Embedding related information inside a document
* Referencing documents stored in another collection

## Embedding

Embedding stores related data inside its parent document.

Example customer with embedded addresses:

```javascript
{
  _id: ObjectId("..."),
  firstName: "Aman",
  lastName: "Singh",
  email: "aman@example.com",
  addresses: [
    {
      type: "home",
      street: "100 Main Street",
      city: "Brampton",
      province: "ON",
      postalCode: "L6X 1A1"
    },
    {
      type: "work",
      street: "200 King Street",
      city: "Toronto",
      province: "ON",
      postalCode: "M5H 1B5"
    }
  ]
}
```

This works well because:

* Addresses belong to the customer.
* A customer normally has a limited number of addresses.
* The profile and addresses are commonly displayed together.
* An address does not need to exist independently.

### Advantages of embedding

* Retrieves related data in one query
* Avoids joins
* Supports atomic updates within one document
* Matches application objects naturally
* Can improve read performance

### Limitations of embedding

* Can duplicate shared information
* May produce large documents
* Is unsuitable for unbounded arrays
* Can make independent updates less convenient

## Referencing

Referencing stores related data in separate collections and connects documents using identifiers.

Customer:

```javascript
{
  _id: ObjectId("66a100000000000000000001"),
  firstName: "Aman",
  lastName: "Singh",
  email: "aman@example.com"
}
```

Review:

```javascript
{
  _id: ObjectId("..."),
  productId: ObjectId("65a100000000000000000001"),
  customerId: ObjectId("66a100000000000000000001"),
  rating: 5,
  comment: "Easy to use and very responsive.",
  createdAt: ISODate("2026-09-22T10:00:00Z")
}
```

The review refers to the customer and product.

### Advantages of referencing

* Avoids excessive duplication
* Supports independently changing data
* Works well for many-to-many relationships
* Handles large and growing relationships
* Keeps individual documents smaller

### Limitations of referencing

* May require multiple queries
* May require `$lookup` aggregation
* Makes application logic more complex
* Cross-document operations may require transactions

---

# 6. How to Choose Between Them

| Consideration                          | Embed         | Reference                        |
| --------------------------------------- | -------------- | ---------------------------------- |
| Data is normally read together         | Yes           | Possibly                         |
| Related data is small and bounded      | Yes           | Not required                     |
| Child belongs only to one parent       | Yes           | Possibly                         |
| Related data grows continuously        | No            | Yes                              |
| Related data is shared by many records | No            | Yes                              |
| Related data changes independently     | Sometimes     | Yes                              |
| One-query retrieval is important       | Yes           | Requires lookup or another query |
| Duplication would be substantial       | No            | Yes                              |
| Atomic update is required               | Strong choice | May require a transaction        |

A practical rule is:

> Embed bounded data that belongs to the parent; reference independent, shared or unbounded data.

---

# 7. Modeling Orders: A Hybrid Approach

Orders demonstrate that embedding and referencing can be used together.

```javascript
{
  _id: ObjectId("..."),
  orderNumber: "ORD-2026-1001",
  customerId: ObjectId("66a100000000000000000001"),

  items: [
    {
      productId: ObjectId("65a100000000000000000001"),
      sku: "ELEC-1001",
      productName: "Wireless Mouse",
      unitPrice: NumberDecimal("39.99"),
      quantity: 2
    }
  ],

  shippingAddress: {
    street: "100 Main Street",
    city: "Brampton",
    province: "ON",
    postalCode: "L6X 1A1"
  },

  status: "Shipped",
  total: NumberDecimal("79.98"),
  orderedAt: ISODate("2026-09-22T10:00:00Z")
}
```

This model uses:

* A reference to the customer
* A reference to each product
* Embedded order items
* Embedded shipping address
* Copied product name, SKU and price

## Why copy product information?

The product name or price might change later. An order should preserve the values that were applicable when the purchase occurred.

If the current product price changes from `$39.99` to `$44.99`, the historical order should still show `$39.99`.

This controlled duplication is called a snapshot or historical pattern.

---

# 8. Common Data-Modeling Mistakes

## Treating collections exactly like relational tables

Creating separate collections for every small component can force the application to reconstruct objects using numerous queries.

## Embedding an unbounded array

Avoid a product document containing every review:

```javascript
{
  name: "Wireless Mouse",
  reviews: [
    // Could eventually contain millions of elements
  ]
}
```

Store reviews in a separate collection instead.

## Storing frequently changing shared data everywhere

Duplicating a customer’s current profile in thousands of active records makes updates difficult. Duplicate only the fields that need to remain as a historical snapshot.

## Using inconsistent data types

Avoid:

```javascript
{ price: 39.99 }
{ price: "39.99" }
{ price: { amount: 39.99 } }
```

Choose one structure and apply it consistently.

## Designing without considering queries

A technically valid document model can still perform poorly if it does not support common queries and indexes.

---

# 9. Hands-On Lab: Create the Sample Dataset

## Step 1: Select the database

```javascript
use training_store
```

## Step 2: Remove previous lab collections

Only run this in a disposable training database:

```javascript
db.products.drop()
db.customers.drop()
db.orders.drop()
db.reviews.drop()
```

A result of `false` simply means the collection did not exist.

## Step 3: Create collections

```javascript
db.createCollection("products")
db.createCollection("customers")
db.createCollection("orders")
db.createCollection("reviews")
```

Verify:

```javascript
show collections
```

---

# 10. Populate the Products Collection

To make later references easy, the lab uses predetermined `ObjectId` values.

```javascript
const mouseId =
  ObjectId("65a100000000000000000001");

const keyboardId =
  ObjectId("65a100000000000000000002");

const bookId =
  ObjectId("65a100000000000000000003");
```

Insert the products:

```javascript
db.products.insertMany([
  {
    _id: mouseId,
    sku: "ELEC-1001",
    name: "Wireless Mouse",
    category: "Electronics",
    price: NumberDecimal("39.99"),
    stock: 120,
    active: true,
    tags: ["wireless", "mouse", "accessory"],
    specifications: {
      connection: "Bluetooth",
      colour: "Black",
      rechargeable: true
    },
    createdAt: ISODate("2026-09-20T09:00:00Z")
  },
  {
    _id: keyboardId,
    sku: "ELEC-1002",
    name: "Mechanical Keyboard",
    category: "Electronics",
    price: NumberDecimal("89.99"),
    stock: 45,
    active: true,
    tags: ["keyboard", "mechanical", "accessory"],
    specifications: {
      connection: "USB-C",
      switchType: "Tactile",
      backlit: true
    },
    createdAt: ISODate("2026-09-20T09:05:00Z")
  },
  {
    _id: bookId,
    sku: "BOOK-2001",
    name: "MongoDB Fundamentals",
    category: "Books",
    price: NumberDecimal("49.99"),
    stock: 75,
    active: true,
    tags: ["mongodb", "database", "nosql"],
    specifications: {
      author: "A. Singh",
      isbn: "978-1234567890",
      pages: 420
    },
    createdAt: ISODate("2026-09-20T09:10:00Z")
  }
])
```

---

# 11. Populate the Customers Collection

Create customer identifiers:

```javascript
const amanId =
  ObjectId("66a100000000000000000001");

const priyaId =
  ObjectId("66a100000000000000000002");
```

Insert customers with embedded addresses:

```javascript
db.customers.insertMany([
  {
    _id: amanId,
    firstName: "Aman",
    lastName: "Singh",
    email: "aman@example.com",
    phone: "+1-905-555-0101",
    addresses: [
      {
        type: "home",
        street: "100 Main Street",
        city: "Brampton",
        province: "ON",
        postalCode: "L6X 1A1",
        country: "Canada",
        default: true
      }
    ],
    createdAt: ISODate("2026-09-21T12:00:00Z")
  },
  {
    _id: priyaId,
    firstName: "Priya",
    lastName: "Sharma",
    email: "priya@example.com",
    phone: "+1-416-555-0102",
    addresses: [
      {
        type: "home",
        street: "250 Lake Road",
        city: "Toronto",
        province: "ON",
        postalCode: "M5V 2T6",
        country: "Canada",
        default: true
      },
      {
        type: "work",
        street: "80 King Street",
        city: "Toronto",
        province: "ON",
        postalCode: "M5H 1J9",
        country: "Canada",
        default: false
      }
    ],
    createdAt: ISODate("2026-09-21T12:10:00Z")
  }
])
```

---

# 12. Populate the Orders Collection

```javascript
db.orders.insertMany([
  {
    orderNumber: "ORD-2026-1001",
    customerId: amanId,
    items: [
      {
        productId: mouseId,
        sku: "ELEC-1001",
        productName: "Wireless Mouse",
        unitPrice: NumberDecimal("39.99"),
        quantity: 2,
        lineTotal: NumberDecimal("79.98")
      }
    ],
    shippingAddress: {
      street: "100 Main Street",
      city: "Brampton",
      province: "ON",
      postalCode: "L6X 1A1",
      country: "Canada"
    },
    status: "Shipped",
    subtotal: NumberDecimal("79.98"),
    tax: NumberDecimal("10.40"),
    total: NumberDecimal("90.38"),
    orderedAt: ISODate("2026-09-22T10:00:00Z")
  },
  {
    orderNumber: "ORD-2026-1002",
    customerId: priyaId,
    items: [
      {
        productId: keyboardId,
        sku: "ELEC-1002",
        productName: "Mechanical Keyboard",
        unitPrice: NumberDecimal("89.99"),
        quantity: 1,
        lineTotal: NumberDecimal("89.99")
      },
      {
        productId: bookId,
        sku: "BOOK-2001",
        productName: "MongoDB Fundamentals",
        unitPrice: NumberDecimal("49.99"),
        quantity: 1,
        lineTotal: NumberDecimal("49.99")
      }
    ],
    shippingAddress: {
      street: "250 Lake Road",
      city: "Toronto",
      province: "ON",
      postalCode: "M5V 2T6",
      country: "Canada"
    },
    status: "Processing",
    subtotal: NumberDecimal("139.98"),
    tax: NumberDecimal("18.20"),
    total: NumberDecimal("158.18"),
    orderedAt: ISODate("2026-09-22T11:30:00Z")
  }
])
```

---

# 13. Populate the Reviews Collection

Reviews are stored separately because their number can grow continuously.

```javascript
db.reviews.insertMany([
  {
    productId: mouseId,
    customerId: amanId,
    rating: 5,
    title: "Excellent mouse",
    comment: "Easy to use and very responsive.",
    verifiedPurchase: true,
    createdAt: ISODate("2026-09-22T14:00:00Z")
  },
  {
    productId: keyboardId,
    customerId: priyaId,
    rating: 4,
    title: "Comfortable keyboard",
    comment: "Good typing experience and build quality.",
    verifiedPurchase: true,
    createdAt: ISODate("2026-09-22T15:00:00Z")
  },
  {
    productId: bookId,
    customerId: priyaId,
    rating: 5,
    title: "Clear introduction",
    comment: "The examples are practical and easy to follow.",
    verifiedPurchase: true,
    createdAt: ISODate("2026-09-22T15:15:00Z")
  }
])
```

---

# 14. Verify the Dataset

## Count documents

```javascript
db.products.countDocuments()
db.customers.countDocuments()
db.orders.countDocuments()
db.reviews.countDocuments()
```

Expected results:

| Collection  | Expected count |
| ----------- | --------------: |
| `products`  |              3 |
| `customers` |              2 |
| `orders`    |              2 |
| `reviews`   |              3 |

## Find electronics products

```javascript
db.products.find(
  { category: "Electronics" },
  { name: 1, price: 1, stock: 1 }
)
```

## Find products below $50

```javascript
db.products.find({
  price: { $lt: NumberDecimal("50.00") }
})
```

## Query an embedded field

Find customers who have an address in Brampton:

```javascript
db.customers.find({
  "addresses.city": "Brampton"
})
```

## Query an embedded array

Find orders containing the wireless mouse:

```javascript
db.orders.find({
  "items.productId": mouseId
})
```

## Find one customer’s orders

```javascript
db.orders.find({
  customerId: amanId
})
```

## Find reviews for a product

```javascript
db.reviews.find({
  productId: mouseId
})
```

---

# 15. Join Referenced Data with `$lookup`

Retrieve reviews with product information:

```javascript
db.reviews.aggregate([
  {
    $match: {
      productId: mouseId
    }
  },
  {
    $lookup: {
      from: "products",
      localField: "productId",
      foreignField: "_id",
      as: "product"
    }
  },
  {
    $unwind: "$product"
  },
  {
    $project: {
      _id: 0,
      productName: "$product.name",
      rating: 1,
      title: 1,
      comment: 1
    }
  }
])
```

This operation shows the tradeoff of referencing: related data remains independent, but combining it requires another query or an aggregation join.

---

# 16. Recommended Indexes for the Model

Indexes should follow the identified access patterns.

```javascript
db.products.createIndex(
  { sku: 1 },
  { unique: true }
)

db.products.createIndex({
  category: 1,
  price: 1
})

db.customers.createIndex(
  { email: 1 },
  { unique: true }
)

db.orders.createIndex({
  customerId: 1,
  orderedAt: -1
})

db.reviews.createIndex({
  productId: 1,
  createdAt: -1
})
```

These indexes support:

* Product lookup by SKU
* Product browsing by category and price
* Customer lookup by email
* Customer order history
* Product review history

---

# 17. Lab Review Questions

1. Why are customer addresses embedded?
2. Why are product reviews stored separately?
3. Why does an order contain both `productId` and `productName`?
4. What would happen to old orders if the product price changed?
5. Should order items be placed in a separate collection?
6. Which field types should be used for money and dates?
7. Which queries require references to be resolved?
8. Which arrays are bounded, and which could grow indefinitely?

## Suggested answers

* Addresses are bounded and normally retrieved with their customer.
* Reviews can grow indefinitely and exist as independent records.
* `productId` identifies the product, while the copied name preserves order history.
* The historical order price remains unchanged.
* Normally, order items should remain embedded because they belong to one order and are retrieved with it.
* Use `Decimal128` for precise monetary values and BSON dates for timestamps.
* Orders-to-customers and reviews-to-products require separate queries or `$lookup`.
* Customer addresses and order items are normally bounded; product reviews may be unbounded.

---

# Module Outcome

After completing this module, learners should be able to:

* Explain databases, collections, documents and fields.
* Select appropriate BSON data types.
* Identify application access patterns.
* Model one-to-one, one-to-many and many-to-many relationships.
* Choose between embedding and referencing.
* Apply a hybrid model where appropriate.
* Populate a connected MongoDB dataset.
* Query embedded and referenced information.
* Create initial indexes around important access patterns.

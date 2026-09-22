# Module 1: Introduction to NoSQL Databases

## 1. Defining NoSQL and the Problems It Addresses

NoSQL means “Not Only SQL.” It refers to databases designed to store and retrieve data using models other than traditional relational tables.

Relational databases organize data into fixed tables containing rows and columns. They work well when the data structure is stable and relationships must be strictly enforced. However, modern applications often produce large volumes of rapidly changing or semi-structured data.

NoSQL databases address challenges such as:

* Frequently changing data structures
* Large volumes of data
* High-speed reads and writes
* Distributed applications
* Horizontal scaling across multiple servers
* Data that does not fit naturally into tables
* Rapid application development

For example, an e-commerce product may contain different attributes depending on its category:

```json
{
  "name": "Laptop",
  "brand": "Lenovo",
  "ram": "16 GB",
  "processor": "Intel Core i7"
}
```

A book might require different fields:

```json
{
  "name": "MongoDB Fundamentals",
  "author": "A. Singh",
  "isbn": "978-1234567890"
}
```

A relational system may require several tables or many optional columns. A document database can store each product with the fields appropriate to it.

NoSQL does not mean that SQL databases are obsolete. The appropriate database depends on the application’s data, access patterns, consistency requirements and scale.

---

## 2. Comparing Document, Key-Value and Graph Stores

### Document databases

Document databases store information as self-contained documents, usually in a JSON-like format.

Example:

```json
{
  "_id": 1001,
  "customer": {
    "name": "Aman",
    "email": "aman@example.com"
  },
  "items": [
    {
      "product": "Keyboard",
      "quantity": 2,
      "price": 49.99
    }
  ],
  "status": "Shipped"
}
```

Common products include MongoDB and Couchbase.

Document databases are suitable for:

* Product catalogues
* Customer profiles
* Content-management systems
* Mobile and web applications
* Order-management systems

Their main advantage is that an application object can often be stored as one document without splitting it across many tables.

### Key-value databases

Key-value databases store each value under a unique key.

```text
Key:   session:78421
Value: {"customerId": 1001, "cartItems": 4}
```

The application provides the key, and the database returns the associated value.

Common products include Redis and Amazon DynamoDB.

Key-value databases are suitable for:

* Caching
* User sessions
* Shopping carts
* Application preferences
* Real-time counters

They provide very fast access when the application knows the required key. However, complex relationship-based queries may be difficult.

### Graph databases

Graph databases represent data using:

* Nodes: entities such as customers or products
* Edges: relationships between entities
* Properties: information about nodes and relationships

Example:

```text
(Customer: Asha) ──PURCHASED──> (Product: Laptop)
(Customer: Asha) ──KNOWS──────> (Customer: Ravi)
```

Common products include Neo4j and Amazon Neptune.

Graph databases are suitable for:

* Social networks
* Recommendation engines
* Fraud detection
* Network analysis
* Identity and access relationships

They are particularly effective when relationships are as important as the entities themselves.

### Comparison

| Type      | Data model              | Main strength                          | Typical use               |
| --------- | ----------------------- | --------------------------------------- | -------------------------- |
| Document  | JSON-like documents     | Flexible, application-friendly records | Catalogues and profiles   |
| Key-value | Key mapped to a value   | Extremely fast lookup                  | Caching and sessions      |
| Graph     | Nodes and relationships | Relationship traversal                 | Fraud and recommendations |

---

## 3. Introducing MongoDB and Its Architecture

MongoDB is a document-oriented NoSQL database. It stores data as BSON documents. BSON is a binary representation of JSON-like data that supports additional types such as dates, decimals and ObjectIds.

### MongoDB data hierarchy

```text
MongoDB deployment
    └── Database
          └── Collection
                └── Document
                      └── Field
```

Using an e-commerce example:

```text
Database:    training_store
Collection:  products
Document:    One product
Fields:      name, category, price, stock
```

Example document:

```javascript
{
  _id: ObjectId("..."),
  name: "Wireless Mouse",
  category: "Electronics",
  price: 39.99,
  stock: 120,
  specifications: {
    connection: "Bluetooth",
    colour: "Black"
  },
  tags: ["wireless", "accessory"]
}
```

### Major architectural components

**MongoDB client**

Applications communicate with MongoDB through language-specific drivers. Administrators and developers can also use tools such as `mongosh` and MongoDB Compass.

**`mongod` process**

`mongod` is the primary MongoDB server process. It manages:

* Data storage
* Queries
* Indexes
* Authentication
* Replication
* Database operations

**Replica set**

A replica set is a group of MongoDB servers that maintain copies of the same data.

* The primary node accepts writes.
* Secondary nodes replicate the primary’s data.
* If the primary fails, an eligible secondary can become the new primary.

Replica sets provide redundancy and high availability.

**Sharded cluster**

Sharding distributes a large dataset across multiple servers called shards.

A sharded cluster typically includes:

* Shards that store the data
* Configuration servers that store cluster metadata
* `mongos` query routers that direct requests to appropriate shards

Sharding supports horizontal scaling when one server cannot efficiently handle the complete dataset or workload.

---

## 4. Core Features and Practical Benefits

### Flexible document model

Documents in the same collection do not always need identical fields.

```javascript
// Physical product
{
  name: "Laptop",
  price: 1200,
  weight: 1.8
}

// Digital product
{
  name: "Python Course",
  price: 99,
  durationHours: 30
}
```

This flexibility helps applications evolve without requiring constant table redesign.

### Embedded documents and arrays

MongoDB can store related information together:

```javascript
{
  orderId: 5001,
  customerId: 101,
  items: [
    { productId: 10, quantity: 2 },
    { productId: 24, quantity: 1 }
  ],
  shippingAddress: {
    city: "Brampton",
    province: "Ontario"
  }
}
```

This can reduce the number of joins and queries required to retrieve complete business objects.

### Rich query language

MongoDB supports:

* Filtering
* Sorting
* Projection
* Updates
* Array queries
* Geospatial queries
* Text and search capabilities
* Aggregation pipelines

Example:

```javascript
db.products.find(
  {
    category: "Electronics",
    price: { $lt: 100 }
  },
  {
    name: 1,
    price: 1
  }
)
```

### Indexing

Indexes improve query performance by helping MongoDB locate documents without scanning the entire collection.

```javascript
db.products.createIndex({ category: 1, price: 1 })
```

Indexes should be designed around the application’s common query patterns.

### Aggregation framework

Aggregation pipelines process documents through a sequence of stages:

```javascript
db.orders.aggregate([
  {
    $match: {
      status: "Completed"
    }
  },
  {
    $group: {
      _id: "$customerId",
      totalSpent: { $sum: "$total" }
    }
  },
  {
    $sort: {
      totalSpent: -1
    }
  }
])
```

This can be used for reporting, transformation and analytical processing.

### Replication and high availability

Replica sets protect applications from individual server failures by maintaining multiple copies of the data and supporting automatic election of a new primary.

### Horizontal scalability

MongoDB can distribute data across multiple shards. New servers can be added as the dataset and workload grow.

### Transactions and validation

Although MongoDB has a flexible schema, it can still enforce document rules using schema validation. It also supports atomic operations and multi-document transactions when a business process requires them.

---

## Practical Benefits

MongoDB can provide:

* Faster development with JSON-like documents
* Natural mapping between application objects and stored data
* Support for changing business requirements
* Efficient storage of nested and hierarchical information
* High availability through replication
* Horizontal scaling through sharding
* Powerful operational and analytical queries

A good MongoDB design does not simply move relational tables into collections. It models documents around how the application reads, writes and updates its data.

The central principle is:

> Store information together when the application commonly accesses it together.

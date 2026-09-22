# Module 6: Indexing

An index is a data structure that helps MongoDB locate documents without scanning every document in a collection.

Without a suitable index, MongoDB may perform a collection scan:

```text
Examine every document → test filter → return matches
```

With a suitable index:

```text
Search index entries → locate matching documents → return results
```

Indexes can greatly improve query performance, but they also:

* Consume disk and memory
* Add work to inserts, updates and deletes
* Require monitoring and maintenance
* Must be designed around real query patterns

The core principle is:

> Create indexes for important query shapes, not merely for every available field.

We will continue using:

```javascript
use training_store
```

---

## 1. How an Index Works

Suppose the `products` collection contains one million documents, and the application runs:

```javascript
db.products.find({
  sku: "ELEC-1001"
})
```

Without an index on `sku`, MongoDB may inspect every product until it finds the match.

Create an index:

```javascript
db.products.createIndex({
  sku: 1
})
```

MongoDB creates an ordered structure containing the indexed values and references to their documents.

```text
BOOK-1001  → Product document
BOOK-1002  → Product document
ELEC-1001  → Product document
ELEC-1002  → Product document
```

MongoDB can search this structure instead of reading the entire collection.

---

## 2. Default `_id` Index

Every standard MongoDB collection automatically receives a unique index on `_id`:

```javascript
{
  _id: 1
}
```

Therefore, this query is indexed automatically:

```javascript
db.products.find({
  _id: ObjectId("65a100000000000000000001")
})
```

The `_id` index:

* Uniquely identifies documents
* Prevents duplicate `_id` values
* Cannot normally be removed
* Supports efficient lookup by document identifier

---

## 3. Creating a Single-Field Index

Create an ascending index:

```javascript
db.products.createIndex({
  category: 1
})
```

Create a descending index:

```javascript
db.orders.createIndex({
  orderedAt: -1
})
```

For simple equality matching, ascending and descending single-field indexes generally provide equivalent lookup capability. Direction matters more when supporting sorts in compound indexes.

### Create an index with a custom name

```javascript
db.products.createIndex(
  {
    category: 1
  },
  {
    name: "idx_products_category"
  }
)
```

A clear naming convention makes indexes easier to identify and manage.

---

## 4. Creating Multiple Indexes

Multiple indexes can be requested together:

```javascript
db.products.createIndexes([
  {
    key: {
      sku: 1
    },
    name: "uq_products_sku",
    unique: true
  },
  {
    key: {
      category: 1,
      price: 1
    },
    name: "idx_products_category_price"
  },
  {
    key: {
      tags: 1
    },
    name: "idx_products_tags"
  }
])
```

MongoDB provides both `createIndex()` and `createIndexes()` for creating indexes.

---

## 5. Viewing Existing Indexes

List a collection’s indexes:

```javascript
db.products.getIndexes()
```

A result may resemble:

```javascript
[
  {
    key: { _id: 1 },
    name: "_id_"
  },
  {
    key: { sku: 1 },
    name: "uq_products_sku",
    unique: true
  },
  {
    key: { category: 1, price: 1 },
    name: "idx_products_category_price"
  }
]
```

Display only index names:

```javascript
db.products.getIndexes().map(
  index => index.name
)
```

---

## 6. Removing Indexes

### Remove one index by name

```javascript
db.products.dropIndex(
  "idx_products_category"
)
```

### Remove one index by key specification

```javascript
db.products.dropIndex({
  category: 1
})
```

### Remove all removable indexes

```javascript
db.products.dropIndexes()
```

This retains the required `_id` index.

Removing an index can cause performance regressions. Confirm that important queries do not depend on it before dropping it.

---

## 7. Hiding an Index for Testing

Instead of immediately dropping a questionable index, it can be hidden from the query planner:

```javascript
db.products.hideIndex(
  "idx_products_category_price"
)
```

Run representative tests while the index is hidden.

Restore it:

```javascript
db.products.unhideIndex(
  "idx_products_category_price"
)
```

Hiding is safer for evaluation because the existing index structure remains available and can be restored without rebuilding it. However, a hidden index still consumes storage and must still be maintained during writes.

---

## 8. How Indexes Affect Query Performance

Consider:

```javascript
db.products.find({
  category: "Electronics",
  price: {
    $lt: NumberDecimal("100.00")
  }
})
```

### Without a suitable index

MongoDB may perform:

```text
COLLSCAN
```

This means it scans collection documents.

### With a compound index

```javascript
db.products.createIndex({
  category: 1,
  price: 1
})
```

MongoDB may perform:

```text
IXSCAN → FETCH
```

* `IXSCAN` searches the index.
* `FETCH` retrieves qualifying documents.
* The query avoids examining unrelated collection documents.

### Performance is not determined by time alone

Execution time can vary because of:

* Caching
* Hardware activity
* Dataset size
* Concurrent workloads
* Network latency

Also compare:

* `totalDocsExamined`
* `totalKeysExamined`
* `nReturned`
* Selected execution stage
* Whether a blocking sort occurred

---

## 9. Examining a Query Plan

Use `explain("executionStats")`:

```javascript
db.products.find({
  category: "Electronics",
  price: {
    $lt: NumberDecimal("100.00")
  }
}).explain("executionStats")
```

An alternative form is:

```javascript
db.products.explain(
  "executionStats"
).find({
  category: "Electronics",
  price: {
    $lt: NumberDecimal("100.00")
  }
})
```

MongoDB’s `executionStats` mode reports query execution information including index use and examined documents.

### Important fields

#### `winningPlan`

Shows the plan chosen by the query optimizer.

Look for stages such as:

```text
COLLSCAN
IXSCAN
FETCH
SORT
```

#### `nReturned`

Number of documents returned to the caller.

#### `totalDocsExamined`

Number of collection documents inspected.

#### `totalKeysExamined`

Number of index entries inspected.

#### Example interpretation

```text
nReturned:         10
totalKeysExamined: 10
totalDocsExamined: 10
```

This may indicate a selective and efficient indexed query.

```text
nReturned:         10
totalKeysExamined: 100,000
totalDocsExamined: 80,000
```

An index may have been used, but the query still examines many unnecessary entries and documents.

---

## 10. Comparing Before and After Indexing

### Step 1: Inspect the query

```javascript
db.orders.find({
  customerId: ObjectId("66a100000000000000000001")
}).sort({
  orderedAt: -1
}).explain("executionStats")
```

### Step 2: Create an index matching the filter and sort

```javascript
db.orders.createIndex(
  {
    customerId: 1,
    orderedAt: -1
  },
  {
    name: "idx_orders_customer_date"
  }
)
```

### Step 3: Run the same explain operation

```javascript
db.orders.find({
  customerId: ObjectId("66a100000000000000000001")
}).sort({
  orderedAt: -1
}).explain("executionStats")
```

The desired improvement is:

* Index scan instead of collection scan
* Fewer documents examined
* Fewer unnecessary keys examined
* No in-memory blocking sort
* Faster and more predictable execution

---

## 11. Compound Indexes

A compound index contains multiple fields:

```javascript
db.products.createIndex({
  category: 1,
  price: 1
})
```

The index is ordered first by `category` and then by `price` within each category.

```text
Books
    19.99
    29.99
    49.99

Electronics
    39.99
    89.99
    499.99
```

Compound indexes support queries using the indexed fields and their prefixes.

### Index-prefix rule

For:

```javascript
{
  category: 1,
  price: 1,
  stock: 1
}
```

Useful prefixes include:

```javascript
{ category: 1 }

{ category: 1, price: 1 }

{ category: 1, price: 1, stock: 1 }
```

A query using only `price` normally cannot use this index as effectively as a query beginning with `category`.

This does not mean every query must include every indexed field. It means field order controls which leading portions of the index are directly useful.

---

## 12. Equality, Sort and Range Guideline

A practical compound-index design guideline is ESR:

1. **Equality**
2. **Sort**
3. **Range**

Suppose the query is:

```javascript
db.orders.find({
  customerId: customerId,
  status: "Completed",
  total: {
    $gte: NumberDecimal("100.00")
  }
}).sort({
  orderedAt: -1
})
```

Possible index:

```javascript
db.orders.createIndex({
  customerId: 1,
  status: 1,
  orderedAt: -1,
  total: 1
})
```

* `customerId` and `status` are equality conditions.
* `orderedAt` supports sorting.
* `total` is a range condition.

ESR is a guideline, not an absolute rule. Query selectivity, sorting requirements and actual explain results should determine the final design.

---

## 13. Supporting Sorts

Consider:

```javascript
db.orders.find({
  customerId: customerId
}).sort({
  orderedAt: -1
})
```

Recommended index:

```javascript
db.orders.createIndex({
  customerId: 1,
  orderedAt: -1
})
```

The index groups entries by customer and arranges each customer’s orders by date.

### Reverse traversal

An index:

```javascript
{
  customerId: 1,
  orderedAt: -1
}
```

can generally support the exact direction:

```javascript
{
  customerId: 1,
  orderedAt: -1
}
```

and its complete reverse:

```javascript
{
  customerId: -1,
  orderedAt: 1
}
```

It does not directly support every arbitrary combination of directions.

---

## 14. Unique Indexes

A unique index prevents duplicate indexed values.

```javascript
db.products.createIndex(
  {
    sku: 1
  },
  {
    unique: true,
    name: "uq_products_sku"
  }
)
```

Attempting to insert another product with the same SKU causes a duplicate-key error.

### Unique customer email

```javascript
db.customers.createIndex(
  {
    email: 1
  },
  {
    unique: true,
    name: "uq_customers_email"
  }
)
```

### Case-insensitive uniqueness

The strings below differ in case:

```text
priya@example.com
PRIYA@EXAMPLE.COM
```

For case-insensitive comparison, an index can use collation:

```javascript
db.customers.createIndex(
  {
    email: 1
  },
  {
    unique: true,
    name: "uq_customers_email_ci",
    collation: {
      locale: "en",
      strength: 2
    }
  }
)
```

Queries must use a compatible collation to use that index:

```javascript
db.customers.find({
  email: "PRIYA@EXAMPLE.COM"
}).collation({
  locale: "en",
  strength: 2
})
```

Applications should also normalize email addresses before storing them when that matches the business rule.

---

## 15. Multikey Indexes for Arrays

When an index is created on an array field, MongoDB creates a multikey index.

```javascript
db.products.createIndex({
  tags: 1
})
```

It supports queries such as:

```javascript
db.products.find({
  tags: "wireless"
})
```

MongoDB’s multikey indexes collect and sort values stored in arrays.

### Array of embedded documents

```javascript
db.orders.createIndex({
  "items.productId": 1
})
```

This can support:

```javascript
db.orders.find({
  "items.productId": mouseId
})
```

### Multikey consideration

Arrays may produce multiple index entries per document. Large arrays can therefore create large indexes and increase write overhead.

Compound multikey indexes also have restrictions when multiple indexed fields are arrays. Test the intended document structure before adopting such an index.

---

## 16. Partial Indexes

A partial index includes only documents matching a filter.

Suppose most product queries retrieve active products:

```javascript
db.products.createIndex(
  {
    category: 1,
    price: 1
  },
  {
    name: "idx_active_products_category_price",
    partialFilterExpression: {
      active: true
    }
  }
)
```

The index includes only active products.

This can:

* Reduce index size
* Reduce index maintenance
* Improve queries that match the partial condition

A query must satisfy the partial-filter condition for MongoDB to safely use the index:

```javascript
db.products.find({
  active: true,
  category: "Electronics",
  price: {
    $lt: NumberDecimal("100.00")
  }
})
```

A query that does not restrict `active` to `true` cannot generally rely on this partial index because inactive matching documents are absent from it.

---

## 17. Sparse Indexes

A sparse index includes documents that contain the indexed field.

```javascript
db.customers.createIndex(
  {
    loyaltyNumber: 1
  },
  {
    sparse: true,
    name: "idx_customers_loyalty_sparse"
  }
)
```

Sparse indexes can be useful for optional fields, but partial indexes offer more precise control and are often preferred.

Be especially careful with unique sparse indexes because uniqueness applies only to indexed documents.

---

## 18. TTL Indexes

A TTL, or time-to-live, index automatically removes expired documents.

Example session document:

```javascript
{
  sessionId: "S-1001",
  customerId: customerId,
  expiresAt: ISODate("2026-09-22T20:00:00Z")
}
```

Create a TTL index:

```javascript
db.sessions.createIndex(
  {
    expiresAt: 1
  },
  {
    expireAfterSeconds: 0,
    name: "ttl_sessions_expiresAt"
  }
)
```

With `expireAfterSeconds: 0`, each document expires based on the date stored in `expiresAt`.

TTL indexes are single-field indexes, and deletion can occur after the precise expiration time rather than exactly at that instant.

Common uses include:

* Login sessions
* Temporary verification codes
* Short-lived event data
* Temporary processing records
* Expiring audit data when permitted by policy

Do not use TTL deletion for records that must be retained for legal, audit or business purposes.

---

## 19. Text Indexes

A self-managed MongoDB deployment can use a text index for basic `$text` searches:

```javascript
db.products.createIndex(
  {
    name: "text",
    description: "text"
  },
  {
    name: "txt_products_name_description"
  }
)
```

Query:

```javascript
db.products.find({
  $text: {
    $search: "wireless ergonomic"
  }
})
```

Return the text score:

```javascript
db.products.find(
  {
    $text: {
      $search: "wireless ergonomic"
    }
  },
  {
    name: 1,
    score: {
      $meta: "textScore"
    }
  }
).sort({
  score: {
    $meta: "textScore"
  }
})
```

Traditional text indexes support basic word-based text queries, but they add write and storage cost. MongoDB recommends its newer search capabilities for more advanced search requirements.

Use a dedicated search solution when requirements include:

* Autocomplete
* Fuzzy matching
* Relevance tuning
* Faceting
* Synonyms
* Semantic or vector search
* Advanced language analysis

---

## 20. Wildcard Indexes

A wildcard index can cover varying or unpredictable field names.

The `specifications` fields differ by product category:

```javascript
// Electronics
{
  specifications: {
    connection: "Bluetooth",
    rechargeable: true
  }
}

// Book
{
  specifications: {
    author: "A. Singh",
    pages: 420
  }
}
```

A wildcard index can cover specification fields:

```javascript
db.products.createIndex(
  {
    "specifications.$**": 1
  },
  {
    name: "idx_products_specifications_wildcard"
  }
)
```

This may help varied queries such as:

```javascript
db.products.find({
  "specifications.connection": "Bluetooth"
})
```

or:

```javascript
db.products.find({
  "specifications.pages": {
    $gte: 300
  }
})
```

Wildcard indexes support flexible schemas with varying field names.

They are not a substitute for intentional indexes on stable, high-volume query patterns.

---

## 21. Geospatial Indexes

Use a `2dsphere` index for Earth-like geographic coordinates.

Store GeoJSON points with longitude first:

```javascript
{
  name: "Brampton Store",
  location: {
    type: "Point",
    coordinates: [
      -79.7624,
      43.7315
    ]
  }
}
```

Create the index:

```javascript
db.stores.createIndex(
  {
    location: "2dsphere"
  },
  {
    name: "geo_stores_location"
  }
)
```

Find nearby stores:

```javascript
db.stores.find({
  location: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [
          -79.7624,
          43.7315
        ]
      },
      $maxDistance: 10000
    }
  }
})
```

Geospatial indexes are designed for geographic proximity and containment queries.

---

## 22. Hashed Indexes

A hashed index stores a hash of a field’s value:

```javascript
db.customers.createIndex({
  customerNumber: "hashed"
})
```

Hashed indexes are primarily associated with hashed sharding and distributing values across shards.

They support equality-oriented access but are not appropriate for:

* Range queries
* Sorting by the original field value
* Prefix-based searches

MongoDB describes hashed indexes as indexing the hash of a field value and using them to support hashed sharding.

---

## 23. Covered Queries

A covered query can be answered entirely from the index without retrieving the full collection documents.

Create:

```javascript
db.products.createIndex({
  category: 1,
  name: 1,
  price: 1
})
```

Query only indexed fields:

```javascript
db.products.find(
  {
    category: "Electronics"
  },
  {
    _id: 0,
    category: 1,
    name: 1,
    price: 1
  }
)
```

Because the filter and returned fields are contained in the index, MongoDB may avoid the document-fetch stage.

If `_id` is not part of the index, exclude it from the projection when attempting to create a covered query.

---

## 24. Index Selectivity

A selective condition matches a relatively small portion of a collection.

Highly selective:

```javascript
{
  sku: "ELEC-1001"
}
```

Potentially low selectivity:

```javascript
{
  active: true
}
```

If nearly every product is active, an index on `active` alone may provide little value.

Instead, combine it with other fields used by the query:

```javascript
db.products.createIndex({
  active: 1,
  category: 1,
  price: 1
})
```

Whether this is the best field order depends on:

* Query frequencies
* Data distribution
* Sorting requirements
* Range conditions
* Explain-plan results

---

## 25. Index Costs

Indexes improve reads, but every additional index has a cost.

### Storage cost

Indexes consume disk space.

### Memory pressure

Frequently used index pages compete for memory.

### Write amplification

For an insertion:

```javascript
db.products.insertOne({
  sku: "ELEC-3000",
  name: "Webcam"
})
```

MongoDB must update:

* The collection data
* The `_id` index
* The SKU index
* Every other applicable index

### Update cost

Changing an indexed field requires updating its index entries:

```javascript
db.products.updateOne(
  {
    sku: "ELEC-3000"
  },
  {
    $set: {
      category: "Computer Accessories"
    }
  }
)
```

### Operational cost

More indexes mean:

* Longer index builds
* More monitoring
* More complex query-plan choices
* Additional backup and replication volume

Avoid indexing every field “just in case.”

---

## 26. Selecting an Index for a Workload

Index selection begins with the complete query shape:

* Filter fields
* Equality conditions
* Range conditions
* Sort fields and directions
* Projected fields
* Query frequency
* Number of matching documents
* Read-versus-write balance

### Query-shape worksheet

| Workload question | Example                          |
| ------------------ | --------------------------------- |
| Which collection? | `orders`                         |
| Equality filters? | `customerId`, `status`           |
| Range filters?    | `orderedAt`                      |
| Sort fields?      | `orderedAt: -1`                  |
| Returned fields?  | `orderNumber`, `total`, `status` |
| Frequency?        | Every customer-profile request   |
| Expected matches? | 20–100 orders per customer       |
| Write rate?       | Moderate                         |

Possible index:

```javascript
db.orders.createIndex({
  customerId: 1,
  status: 1,
  orderedAt: -1
})
```

---

## 27. Recommended `training_store` Indexes

### Product lookup by SKU

Query:

```javascript
db.products.findOne({
  sku: "ELEC-1001"
})
```

Index:

```javascript
db.products.createIndex(
  {
    sku: 1
  },
  {
    unique: true,
    name: "uq_products_sku"
  }
)
```

### Browse products by category and price

Query:

```javascript
db.products.find({
  category: "Electronics",
  price: {
    $lte: NumberDecimal("100.00")
  }
}).sort({
  price: 1
})
```

Index:

```javascript
db.products.createIndex(
  {
    category: 1,
    price: 1
  },
  {
    name: "idx_products_category_price"
  }
)
```

### Customer lookup by email

```javascript
db.customers.createIndex(
  {
    email: 1
  },
  {
    unique: true,
    name: "uq_customers_email"
  }
)
```

### Customer order history

Query:

```javascript
db.orders.find({
  customerId: customerId
}).sort({
  orderedAt: -1
})
```

Index:

```javascript
db.orders.createIndex(
  {
    customerId: 1,
    orderedAt: -1
  },
  {
    name: "idx_orders_customer_date"
  }
)
```

### Operational order queue

Query:

```javascript
db.orders.find({
  status: "Processing"
}).sort({
  orderedAt: 1
})
```

Index:

```javascript
db.orders.createIndex(
  {
    status: 1,
    orderedAt: 1
  },
  {
    name: "idx_orders_status_date"
  }
)
```

### Product review history

Query:

```javascript
db.reviews.find({
  productId: productId
}).sort({
  createdAt: -1
})
```

Index:

```javascript
db.reviews.createIndex(
  {
    productId: 1,
    createdAt: -1
  },
  {
    name: "idx_reviews_product_date"
  }
)
```

### Prevent duplicate customer reviews

If one customer may review a product only once:

```javascript
db.reviews.createIndex(
  {
    productId: 1,
    customerId: 1
  },
  {
    unique: true,
    name: "uq_reviews_product_customer"
  }
)
```

This index enforces the business rule at the database level.

---

## 28. Index-Type Selection Guide

| Workload                              | Appropriate index |
| --------------------------------------- | ------------------- |
| Lookup by one stable field            | Single-field      |
| Filter and sort across several fields | Compound          |
| Enforce unique SKU or email           | Unique            |
| Search array elements                 | Multikey          |
| Index only qualifying documents       | Partial           |
| Optional field exists in some records | Partial or sparse |
| Automatically expire documents        | TTL               |
| Basic self-managed word search        | Text              |
| Advanced full-text search             | MongoDB Search    |
| Flexible and unpredictable fields     | Wildcard          |
| Geographic proximity                  | `2dsphere`        |
| Hashed shard-key distribution         | Hashed            |

MongoDB supports compound, multikey, wildcard, geospatial, hashed, text and clustered index types, among others.

---

## 29. Hands-On Indexing Lab

### Exercise 1: Establish the baseline

```javascript
const customerId =
  ObjectId("66a100000000000000000001");
```

Run:

```javascript
db.orders.find({
  customerId: customerId
}).sort({
  orderedAt: -1
}).explain("executionStats")
```

Record:

```text
winning plan:
nReturned:
totalKeysExamined:
totalDocsExamined:
```

### Exercise 2: Create the index

```javascript
db.orders.createIndex(
  {
    customerId: 1,
    orderedAt: -1
  },
  {
    name: "idx_orders_customer_date"
  }
)
```

### Exercise 3: Measure again

```javascript
db.orders.find({
  customerId: customerId
}).sort({
  orderedAt: -1
}).explain("executionStats")
```

Compare the execution metrics.

### Exercise 4: Test a different query shape

```javascript
db.orders.find({
  status: "Processing"
}).sort({
  orderedAt: 1
}).explain("executionStats")
```

The customer-history index is not designed for this query because its leading field is `customerId`.

Create a workload-specific index:

```javascript
db.orders.createIndex(
  {
    status: 1,
    orderedAt: 1
  },
  {
    name: "idx_orders_status_date"
  }
)
```

Run `explain()` again.

### Exercise 5: Test a multikey index

Create:

```javascript
db.products.createIndex(
  {
    tags: 1
  },
  {
    name: "idx_products_tags"
  }
)
```

Analyze:

```javascript
db.products.find({
  tags: "wireless"
}).explain("executionStats")
```

### Exercise 6: Review all indexes

```javascript
db.products.getIndexes()
db.customers.getIndexes()
db.orders.getIndexes()
db.reviews.getIndexes()
```

For every non-`_id` index, document:

* Which query it supports
* How frequently that query runs
* Whether it supports sorting
* Whether it enforces a business rule
* Its expected write cost
* Whether another index makes it redundant

---

## 30. Common Indexing Mistakes

### Indexing every field

This wastes storage and harms write performance.

### Ignoring compound field order

These are different indexes:

```javascript
{ category: 1, price: 1 }
```

```javascript
{ price: 1, category: 1 }
```

They support different prefixes and query shapes.

### Creating separate indexes when a compound index is required

Separate indexes:

```javascript
{ customerId: 1 }
{ orderedAt: -1 }
```

do not necessarily support filtering and sorting as effectively as:

```javascript
{
  customerId: 1,
  orderedAt: -1
}
```

### Keeping redundant indexes

If the collection has:

```javascript
{ category: 1 }
```

and:

```javascript
{ category: 1, price: 1 }
```

the single-field index may be redundant because the compound index begins with `category`. Verify differences such as uniqueness, sparsity, collation and workload behavior before removing anything.

### Judging only by execution time

A tiny collection may be faster with a collection scan. Use realistic data volumes and examine keys and documents inspected.

### Using `hint()` as a permanent first response

`hint()` forces a particular index:

```javascript
db.products.find({
  category: "Electronics"
}).hint({
  category: 1,
  price: 1
})
```

It is valuable for testing, but forcing an index can become harmful as data distribution and workloads change. Allow the query planner to choose unless testing demonstrates a specific need.

---

# Module Outcome

After completing this module, learners should be able to:

* Explain how MongoDB indexes improve data access.
* Create, list, hide, restore and remove indexes.
* Interpret `COLLSCAN`, `IXSCAN`, `FETCH` and `SORT`.
* Compare query behavior using `explain("executionStats")`.
* Design compound indexes around filters and sorts.
* Apply the equality-sort-range guideline.
* Use unique indexes to enforce business rules.
* Identify multikey, partial, sparse, TTL, text, wildcard, geospatial and hashed index use cases.
* Recognize the storage and write costs of indexing.
* Select indexes according to real query shapes and workload evidence.

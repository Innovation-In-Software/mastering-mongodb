# Module 8: Best Practices

This module brings together data modeling, querying, aggregation, indexing, security and operations.

A production-ready MongoDB solution should be:

* Correct for the application’s access patterns
* Efficient at expected data volumes
* Secure by default
* Observable and recoverable
* Resilient to application and infrastructure failures
* Maintainable as requirements evolve

---

## 1. Data Modeling Guidelines That Hold Up Over Time

MongoDB’s flexible schema allows documents to evolve, but flexibility should be governed by explicit design rules.

### Model around access patterns

Start with the application’s most important operations:

* What data is read together?
* What data is updated together?
* Which queries run most often?
* Which operations are latency-sensitive?
* How large can each relationship become?
* Which information must remain historically accurate?

For `training_store`, an order can embed its purchased items:

```javascript
{
  orderNumber: "ORD-2026-1001",
  customerId: ObjectId("..."),

  items: [
    {
      productId: ObjectId("..."),
      sku: "ELEC-1001",
      productName: "Wireless Mouse",
      unitPrice: NumberDecimal("39.99"),
      quantity: 2,
      lineTotal: NumberDecimal("79.98")
    }
  ],

  total: NumberDecimal("90.38"),
  status: "Delivered"
}
```

This is appropriate because order items:

* Belong to one order
* Are normally retrieved with the order
* Form a bounded group
* Must preserve historical product and price information

### Embed bounded, owned information

Embedding works well when related data:

* Belongs to one parent
* Is normally accessed with the parent
* Has a practical size limit
* Is updated with the parent
* Benefits from single-document atomicity

Examples:

* Order items inside an order
* Shipping address snapshot inside an order
* A small number of addresses inside a customer
* Product specifications inside a product

### Reference independent or unbounded information

Referencing is generally better when related data:

* Grows without a practical limit
* Is shared among many documents
* Changes independently
* Must be queried separately
* Would make the parent document excessively large

Product reviews should normally be independent documents:

```javascript
{
  productId: ObjectId("..."),
  customerId: ObjectId("..."),
  rating: 5,
  comment: "Excellent product.",
  createdAt: new Date()
}
```

Avoid placing every review in the product:

```javascript
{
  name: "Wireless Mouse",
  reviews: [
    // Potentially millions of reviews
  ]
}
```

MongoDB identifies unbounded arrays as a schema anti-pattern because they can produce oversized documents and reduce performance.

### Keep documents focused

A document should contain information commonly used together.

Avoid bloated documents containing:

* Large fields rarely returned
* Unbounded event histories
* Repeated copies of unrelated records
* Large binary objects that most queries do not need

Large documents can reduce working-set efficiency and increase disk access. Separating information that is not commonly retrieved together can improve performance.

### Use consistent field names

Avoid several names for the same concept:

```javascript
{ customerId: ObjectId("...") }
{ customer_id: ObjectId("...") }
{ custId: ObjectId("...") }
```

Choose and enforce one:

```javascript
{
  customerId: ObjectId("...")
}
```

A common convention is:

```text
Collections: plural nouns
Fields: camelCase
Booleans: active, verifiedPurchase, emailConfirmed
Dates: createdAt, updatedAt, orderedAt
References: customerId, productId
```

### Use consistent BSON types

Poor consistency:

```javascript
{ price: "39.99" }
{ price: 39.99 }
{ price: NumberDecimal("39.99") }
```

Preferred:

```javascript
{
  price: NumberDecimal("39.99")
}
```

Recommended examples:

| Business value        | Suitable type                          |
| ----------------------- | ----------------------------------------- |
| Monetary amount       | `Decimal128`                           |
| Timestamp             | BSON Date                              |
| Count or quantity     | Integer                                |
| Identifier            | `ObjectId` or consistently defined key |
| Status flag           | Boolean                                |
| Multiple values       | Array                                  |
| Structured sub-object | Embedded document                      |

### Preserve historical snapshots

An order should preserve the information applicable when it was placed.

```javascript
{
  items: [
    {
      productId: ObjectId("..."),
      productName: "Wireless Mouse",
      unitPrice: NumberDecimal("39.99")
    }
  ]
}
```

If the current product is renamed or repriced, the historical order remains accurate.

This is intentional duplication, not accidental inconsistency.

---

## 2. Use Schema Validation

MongoDB’s flexible model can still enforce essential business rules.

Example validator for `products`:

```javascript
db.createCollection("validated_products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",

      required: [
        "sku",
        "name",
        "category",
        "price",
        "stock",
        "active"
      ],

      properties: {
        sku: {
          bsonType: "string",
          description: "SKU must be a string"
        },

        name: {
          bsonType: "string",
          minLength: 1
        },

        category: {
          bsonType: "string"
        },

        price: {
          bsonType: "decimal",
          minimum: NumberDecimal("0")
        },

        stock: {
          bsonType: [
            "int",
            "long"
          ],
          minimum: 0
        },

        active: {
          bsonType: "bool"
        },

        tags: {
          bsonType: "array",
          items: {
            bsonType: "string"
          }
        }
      }
    }
  },

  validationLevel: "strict",
  validationAction: "error"
})
```

Schema-validation rules can cover only the fields the application needs to control; they do not necessarily need to define every possible field.

Use validation for:

* Required fields
* Data types
* Allowed enumerations
* Numeric ranges
* Nested structures
* Application invariants

Validation should complement—not replace—application validation.

---

## 3. Plan for Schema Evolution

Production schemas change over time.

Suppose version 1 uses:

```javascript
{
  name: "Wireless Mouse",
  price: NumberDecimal("39.99")
}
```

Version 2 adds:

```javascript
{
  schemaVersion: 2,
  active: true,
  pricing: {
    amount: NumberDecimal("39.99"),
    currency: "CAD"
  }
}
```

Useful migration approaches include:

* Background batch migration
* Migration during deployment
* Read-old/write-new application logic
* Lazy migration when a document is accessed
* Explicit schema-version fields
* Temporary compatibility with both formats

Migration process:

1. Add application support for both formats.
2. Begin writing the new format.
3. Migrate existing documents in controlled batches.
4. Measure progress and failures.
5. Add or update validation rules.
6. Remove obsolete compatibility code after verification.

Avoid applying a massive untested update to a production collection.

---

## 4. Performance Optimization Techniques

Performance tuning should follow evidence:

```text
Observe → Measure → Diagnose → Change → Measure again
```

Do not begin by creating many speculative indexes.

### Understand query shapes

A query shape includes:

* Filter fields
* Operators
* Sort fields
* Projection
* Collation
* Limit
* Aggregation stages

Example:

```javascript
db.orders.find(
  {
    customerId: customerId,
    status: "Completed"
  },
  {
    orderNumber: 1,
    total: 1,
    orderedAt: 1
  }
).sort({
  orderedAt: -1
}).limit(20)
```

Potential index:

```javascript
db.orders.createIndex({
  customerId: 1,
  status: 1,
  orderedAt: -1
})
```

### Filter early

In aggregation pipelines, place selective `$match` stages early when logically possible:

```javascript
db.orders.aggregate([
  {
    $match: {
      status: "Delivered",
      orderedAt: {
        $gte: ISODate("2026-09-01T00:00:00Z")
      }
    }
  },
  {
    $unwind: "$items"
  },
  {
    $group: {
      _id: "$items.productId",
      unitsSold: {
        $sum: "$items.quantity"
      }
    }
  }
])
```

Filtering before `$unwind` reduces the number of documents and array elements processed downstream.

### Project only needed fields

For application queries:

```javascript
db.products.find(
  {
    category: "Electronics"
  },
  {
    _id: 0,
    sku: 1,
    name: 1,
    price: 1
  }
)
```

This reduces unnecessary network transfer and application processing.

Within aggregation, early projection may help when it removes very large fields, although MongoDB can optimize straightforward field dependencies automatically.

### Limit results

Avoid returning an unbounded result set:

```javascript
db.orders.find({
  customerId: customerId
}).sort({
  orderedAt: -1
}).limit(25)
```

Use pagination for user-facing lists.

For large datasets, range-based pagination is often more scalable than large `$skip` values.

```javascript
db.orders.find({
  customerId: customerId,
  orderedAt: {
    $lt: lastSeenDate
  }
}).sort({
  orderedAt: -1,
  _id: -1
}).limit(25)
```

### Use bulk operations

Instead of sending many individual writes:

```javascript
db.products.bulkWrite([
  {
    updateOne: {
      filter: {
        sku: "ELEC-1001"
      },
      update: {
        $inc: {
          stock: 10
        }
      }
    }
  },
  {
    updateOne: {
      filter: {
        sku: "ELEC-1002"
      },
      update: {
        $inc: {
          stock: 20
        }
      }
    }
  }
])
```

Bulk operations can reduce client-server round trips.

### Use atomic operators

Prefer:

```javascript
db.products.updateOne(
  {
    sku: "ELEC-1001",
    stock: {
      $gte: 2
    }
  },
  {
    $inc: {
      stock: -2
    }
  }
)
```

This is safer than:

1. Reading the stock into the application
2. Calculating a new value
3. Writing it back separately

The guarded filter prevents stock from falling below zero in this operation.

---

## 5. Indexing Best Practices

### Index important queries

Create indexes for frequent, important query patterns:

```javascript
db.products.createIndex(
  {
    sku: 1
  },
  {
    unique: true
  }
)

db.products.createIndex({
  category: 1,
  price: 1
})

db.orders.createIndex({
  customerId: 1,
  orderedAt: -1
})

db.reviews.createIndex({
  productId: 1,
  createdAt: -1
})
```

### Follow compound-index field order carefully

For many workloads, begin with:

1. Equality fields
2. Sort fields
3. Range fields

Example query:

```javascript
db.orders.find({
  status: "Completed",
  orderedAt: {
    $gte: ISODate("2026-09-01T00:00:00Z")
  }
}).sort({
  total: -1
})
```

A candidate index might be:

```javascript
db.orders.createIndex({
  status: 1,
  total: -1,
  orderedAt: 1
})
```

Whether this is best depends on:

* Date selectivity
* Importance of avoiding an in-memory sort
* Distribution of statuses
* Result size
* Frequency of the query

Validate it with realistic data and `explain()`.

### Avoid excessive indexing

Each index:

* Uses storage
* Consumes cache
* Adds insert cost
* Adds update cost
* Adds delete cost
* Increases operational complexity

Before creating an index, identify the query it serves.

Before dropping one, hide and test it where appropriate.

---

## 6. Measure with `explain()`

Use:

```javascript
db.orders.find({
  status: "Completed"
}).explain("executionStats")
```

For aggregation:

```javascript
db.orders.explain(
  "executionStats"
).aggregate([
  {
    $match: {
      status: "Completed"
    }
  }
])
```

Review:

* `winningPlan`
* `nReturned`
* `totalDocsExamined`
* `totalKeysExamined`
* `executionTimeMillis`
* Collection scan versus index scan
* Blocking sorts
* Index bounds

A high documents-examined-to-documents-returned ratio can indicate an inefficient query or missing index.

### Typical stages

| Stage        | Meaning                 |
| -------------- | ------------------------- |
| `COLLSCAN`   | Collection scan         |
| `IXSCAN`     | Index scan              |
| `FETCH`      | Retrieve full documents |
| `SORT`       | Sort results            |
| `GROUP`      | Group documents         |
| `PROJECTION` | Reshape output          |

A collection scan is not automatically wrong. It may be appropriate when:

* The collection is small
* Most documents must be returned
* The operation is an occasional administrative task
* An index would not be selective

---

## 7. Monitor Slow Operations

Potential tools include:

* MongoDB diagnostic logs
* Database profiler
* Atlas Query Profiler
* Atlas Performance Advisor
* MongoDB Compass explain plans
* Application performance monitoring
* Driver command monitoring

MongoDB’s diagnostic logs record slow operations, while its profiler and Atlas tools help identify inefficient query patterns.

### Database profiler caution

Profiling can add overhead, especially at aggressive settings. MongoDB warns that the database profiler can degrade performance.

Enable it deliberately and with an appropriate threshold or filter:

```javascript
db.setProfilingLevel(
  1,
  {
    slowms: 200,
    sampleRate: 0.2
  }
)
```

Check the current configuration:

```javascript
db.getProfilingStatus()
```

Return to disabled profiling:

```javascript
db.setProfilingLevel(0)
```

Profiler behavior and performance impact should be evaluated before use on a busy production system.

---

## 8. Resource and Capacity Optimization

Monitor at least:

* CPU utilization
* Memory utilization
* Disk latency and throughput
* Available disk space
* Network throughput
* Connection count
* Query latency
* Replication lag
* Oplog window
* Cache pressure
* Page faults
* Active operations
* Shard balance
* Chunk migrations

### Working set

The working set is the data and index information actively used by the workload.

If the active working set does not fit efficiently in memory, MongoDB must perform more disk I/O, increasing latency.

Possible responses include:

* Improve indexes
* Reduce unnecessary data retrieval
* Archive cold data
* Remodel large documents
* Increase memory
* Separate workloads
* Scale horizontally when justified

---

## 9. Security Considerations

MongoDB should not be exposed to an untrusted network without appropriate controls.

A secure deployment uses multiple layers:

```text
Network controls
      +
TLS encryption
      +
Authentication
      +
Authorization
      +
Encryption at rest
      +
Auditing and monitoring
      +
Backups and recovery
```

MongoDB’s self-managed security checklist emphasizes authentication, TLS and restricted network exposure.

### Enable authentication

Authentication answers:

> Who is connecting?

Never rely only on network location as proof of identity.

For a self-managed deployment, authorization must be enabled through the MongoDB security configuration.

Conceptual configuration:

```yaml
security:
  authorization: enabled
```

MongoDB documents `security.authorization` as the setting that enables authorization.

Create administrative users before enforcing authentication according to the supported deployment procedure.

### Apply least privilege

Authorization answers:

> What may this identity do?

Create role-appropriate accounts:

* Application read/write user
* Reporting read-only user
* Backup operator
* Monitoring user
* Database administrator

Example application user:

```javascript
use training_store

db.createUser({
  user: "trainingStoreApp",
  pwd: passwordPrompt(),
  roles: [
    {
      role: "readWrite",
      db: "training_store"
    }
  ]
})
```

Avoid giving an application broad administrative privileges.

Use separate identities for:

* Applications
* Developers
* Administrators
* Automated jobs
* Monitoring systems

### Protect credentials

Do not place credentials directly in:

* Source code
* Git repositories
* Container images
* Shared screenshots
* Course materials
* Shell-history commands
* Unprotected configuration files

Use:

* Environment-specific secret stores
* Cloud secret-management services
* Kubernetes Secrets with appropriate protection
* Rotated credentials
* Short-lived authentication when supported
* Restricted service accounts

A connection string should be treated as sensitive:

```text
mongodb+srv://username:<password>@cluster.example.net/
```

### Encrypt traffic with TLS

TLS protects data in transit between:

* Applications and MongoDB
* Administrative tools and MongoDB
* Replica-set members
* Sharded-cluster components

MongoDB supports TLS for encrypting network traffic.

Production clients should:

* Validate the server certificate
* Use trusted certificate authorities
* Avoid disabling certificate validation
* Protect private keys
* Rotate expiring certificates

### Restrict network exposure

Use:

* Private networks
* Firewalls
* Security groups
* Atlas IP access lists
* Private endpoints where appropriate
* Restricted `bindIp` settings
* Segmented administrative access
* VPN or controlled bastion access

Do not expose port `27017` broadly to the public internet.

`bindIp` controls the interfaces on which a self-managed MongoDB process listens.

### Protect data at rest

Depending on the deployment, use:

* Encrypted storage volumes
* Cloud-provider encryption
* MongoDB-supported encryption features
* Key-management systems
* Client-side field-level protection for sensitive fields where appropriate

Highly sensitive data might include:

* Government identifiers
* Payment-related information
* Medical information
* Authentication secrets
* Private customer information

Passwords should not be stored as plain text. Application passwords require an appropriate password-hashing design; encryption is not a substitute for secure password hashing.

### Audit important activity

Security monitoring should detect:

* Failed authentication attempts
* Privilege changes
* User creation
* Unusual exports
* Unexpected schema or index changes
* Large deletions
* Configuration changes
* Access from unusual locations

Audit capabilities vary by MongoDB edition and deployment model. Application-level audit events may also be necessary.

---

## 10. Backups and Recovery

Replication is not a backup.

An accidental deletion is replicated:

```javascript
db.orders.deleteMany({})
```

A recovery plan should define:

* Backup frequency
* Retention period
* Encryption
* Offsite or separate-account storage
* Point-in-time recovery requirements
* Restore procedures
* Restore testing
* Recovery time objective
* Recovery point objective

### Recovery objectives

**Recovery Point Objective (RPO)** asks:

> How much data loss is acceptable?

**Recovery Time Objective (RTO)** asks:

> How long may recovery take?

Backups are useful only if restoration works. Schedule restoration exercises rather than assuming backups are valid.

---

## 11. Troubleshooting Framework

Use a systematic process:

```text
Symptom → Scope → Evidence → Layer → Cause → Fix → Verify
```

### Step 1: Define the symptom

Avoid vague descriptions such as:

```text
MongoDB is slow.
```

Prefer:

```text
The customer order-history endpoint increased from
100 ms to 2.5 seconds after the September release.
```

### Step 2: Determine the scope

Ask:

* One query or all queries?
* One application instance or every instance?
* One collection or the complete database?
* One replica-set member or the entire cluster?
* Reads, writes or both?
* Continuous or intermittent?
* Started after a deployment?
* Related to data growth or traffic?

### Step 3: Gather evidence

Collect:

* Application error and trace
* Timestamp and timezone
* Query shape
* `explain()` result
* MongoDB logs
* Driver logs
* Server metrics
* Replica-set status
* Current operations
* Recent schema and index changes
* Deployment changes

### Step 4: Identify the layer

| Layer       | Example issue                           |
| ------------- | ------------------------------------------ |
| Application | Incorrect filter or unbounded result    |
| Driver      | Pool exhaustion or timeout              |
| Network     | DNS, firewall or TLS failure            |
| Query       | Collection scan or expensive sort       |
| Schema      | Unbounded array                         |
| Index       | Missing or unsuitable compound index    |
| Server      | CPU, memory or disk pressure            |
| Replication | Lag or election                         |
| Sharding    | Scatter-gather or imbalance             |
| Security    | Authentication or authorization failure |

### Step 5: Apply the smallest safe correction

Examples:

* Add a targeted index.
* Bound a query with a date range.
* Correct a connection-string option.
* Increase an undersized pool after measuring.
* Rewrite an unbounded array model.
* Fix a role rather than granting administrator access.

### Step 6: Verify

Repeat the same test and compare:

* Latency
* Documents examined
* Keys examined
* Error rate
* Resource usage
* Application behavior

---

## 12. Common Problems and Diagnostic Commands

### Connection refused

Possible causes:

* `mongod` is stopped.
* Incorrect host or port
* Firewall restriction
* `bindIp` restriction
* Container port not exposed
* DNS failure

Checks:

```javascript
db.hello()
```

Operating-system checks may include service state and port connectivity.

### Authentication failed

Check:

* Username
* Password
* Authentication database
* Authentication mechanism
* Credential encoding
* Atlas database-user configuration

The database user may have been created in `admin` even though the application accesses `training_store`.

Example:

```text
mongodb://user@host/training_store?authSource=admin
```

### Authorization failure

Authentication succeeded, but the user lacks permission.

Inspect the current connection’s authenticated roles through appropriate administrative methods and grant only the required privilege.

Do not solve every authorization error by assigning `root`.

### Slow query

Run:

```javascript
db.orders.find({
  customerId: customerId
}).sort({
  orderedAt: -1
}).explain("executionStats")
```

Check for:

* `COLLSCAN`
* Large `totalDocsExamined`
* Large `totalKeysExamined`
* Blocking sort
* Low selectivity
* Excessive result count

### Duplicate-key error

Typical code:

```text
E11000
```

Likely causes:

* Duplicate `_id`
* Duplicate SKU
* Duplicate email
* Compound unique-index violation

Treat expected uniqueness conflicts as business outcomes where appropriate:

```text
“This email is already registered.”
```

Do not expose the raw database error to the user.

### Document-validation failure

A failed schema rule may generate error code `121`.

Possible causes:

* Missing required field
* Incorrect BSON type
* Value outside allowed range
* Invalid nested structure

Log the validation details securely and return a safe application-level message.

### Write conflict or transient transaction error

Applications using transactions should follow the driver’s supported retry pattern.

Avoid blindly retrying every operation. A retry should be:

* Supported for that error type
* Bounded
* Observable
* Safe from duplicate side effects
* Designed for idempotency where possible

### Replication lag

Check:

```javascript
rs.status()
```

Possible causes:

* Slow secondary storage
* Network delay
* Heavy write volume
* Long-running operations
* Undersized oplog
* Resource saturation

### No primary available

Possible causes:

* Election in progress
* Loss of voting majority
* Network partition
* Misconfigured replica set
* Multiple members unavailable

Check:

```javascript
rs.status()
db.hello()
```

### Sharded query contacts every shard

Likely cause:

* Query does not include an appropriate shard-key predicate.

Investigate:

* Shard key
* Query shape
* Targeting information
* Data distribution
* Whether the workload has changed since shard-key selection

---

## 13. Application Error-Handling Practices

### Return appropriate messages

Internal log:

```text
MongoServerError: E11000 duplicate key error
collection: training_store.customers
index: uq_customers_email
```

User-facing response:

```text
An account already exists for that email address.
```

Do not expose:

* Stack traces
* Server hostnames
* Database names unnecessarily
* Connection strings
* Credentials
* Internal topology
* Complete raw documents

### Use structured logging

A useful log record may contain:

```javascript
{
  event: "order_query_failed",
  requestId: "REQ-2026-1025",
  operation: "findCustomerOrders",
  customerId: "masked-or-authorized-value",
  durationMs: 2200,
  errorCategory: "database_timeout",
  occurredAt: "2026-09-22T18:20:00Z"
}
```

Avoid logging credentials or unrestricted personal data.

### Use timeouts

Database operations should not wait indefinitely.

Configure appropriate:

* Server-selection timeout
* Connection timeout
* Socket timeout
* Operation time limit
* Transaction timeout
* Application request timeout

For selected operations:

```javascript
db.orders.find({
  status: "Processing"
}).maxTimeMS(3000)
```

Timeouts must be chosen according to the workload. Extremely low limits can create avoidable failures.

### Design idempotent operations

A retried request should not unintentionally create duplicate business effects.

Use:

* Unique request keys
* Unique order numbers
* Upserts where semantically appropriate
* Guarded state transitions
* Idempotency records

Example:

```javascript
db.orders.updateOne(
  {
    orderNumber: "ORD-2026-1002",
    status: "Processing"
  },
  {
    $set: {
      status: "Shipped"
    },
    $currentDate: {
      shippedAt: true
    }
  }
)
```

Running it again does not rematch an already shipped order.

---

## 14. Hands-On Lab: Build and Tune an Aggregation Pipeline

### Business requirement

Create a sales report showing the top products for a selected date range.

The report must:

* Include only `Shipped`, `Delivered` or `Completed` orders.
* Include orders from September 2026.
* Expand individual order items.
* Group by product.
* Calculate units sold.
* Calculate sales revenue.
* Count the number of contributing orders.
* Sort by revenue.
* Return the top ten products.

### Step 1: Verify the data range

```javascript
db.orders.find(
  {},
  {
    orderNumber: 1,
    status: 1,
    orderedAt: 1,
    total: 1
  }
).sort({
  orderedAt: 1
})
```

Confirm that `orderedAt` is a BSON Date rather than a string.

### Step 2: Construct the pipeline

```javascript
const salesPipeline = [
  {
    $match: {
      status: {
        $in: [
          "Shipped",
          "Delivered",
          "Completed"
        ]
      },

      orderedAt: {
        $gte: ISODate("2026-09-01T00:00:00Z"),
        $lt: ISODate("2026-10-01T00:00:00Z")
      }
    }
  },

  {
    $unwind: "$items"
  },

  {
    $group: {
      _id: {
        productId: "$items.productId",
        sku: "$items.sku",
        productName: "$items.productName"
      },

      unitsSold: {
        $sum: "$items.quantity"
      },

      revenue: {
        $sum: "$items.lineTotal"
      },

      orderIds: {
        $addToSet: "$_id"
      }
    }
  },

  {
    $project: {
      _id: 0,
      productId: "$_id.productId",
      sku: "$_id.sku",
      productName: "$_id.productName",
      unitsSold: 1,
      revenue: 1,

      orderCount: {
        $size: "$orderIds"
      }
    }
  },

  {
    $sort: {
      revenue: -1
    }
  },

  {
    $limit: 10
  }
];
```

Run it:

```javascript
db.orders.aggregate(salesPipeline)
```

### Step 3: Explain the baseline

```javascript
db.orders.explain(
  "executionStats"
).aggregate(salesPipeline)
```

Record:

```text
Winning input stage:
Documents examined:
Keys examined:
Documents returned by the initial match:
Execution time:
Blocking sort present:
```

On a small classroom dataset, differences may be tiny. The important lesson is how the execution plan changes.

### Step 4: Identify the indexable pipeline stage

The first stage is:

```javascript
{
  $match: {
    status: {
      $in: [
        "Shipped",
        "Delivered",
        "Completed"
      ]
    },
    orderedAt: {
      $gte: ISODate("2026-09-01T00:00:00Z"),
      $lt: ISODate("2026-10-01T00:00:00Z")
    }
  }
}
```

The relevant fields are:

```text
status     → equality-style membership condition
orderedAt  → date range
```

Candidate compound index:

```javascript
{
  status: 1,
  orderedAt: 1
}
```

### Step 5: Create the index

```javascript
db.orders.createIndex(
  {
    status: 1,
    orderedAt: 1
  },
  {
    name: "idx_orders_status_orderedAt"
  }
)
```

Verify:

```javascript
db.orders.getIndexes()
```

### Step 6: Explain the tuned pipeline

```javascript
db.orders.explain(
  "executionStats"
).aggregate(salesPipeline)
```

Compare with the baseline:

| Metric             |  Before index |   After index |
| -------------------- | --------------: | --------------: |
| Collection scan    | Record result | Record result |
| Index scan         | Record result | Record result |
| Documents examined |  Record value |  Record value |
| Keys examined      |  Record value |  Record value |
| Documents matched  |  Record value |  Record value |
| Execution time     |  Record value |  Record value |

Expected behavior on a sufficiently large and selective dataset:

* `$match` can use the compound index.
* Fewer unrelated order documents are examined.
* Less data reaches `$unwind`.
* Less data reaches `$group`.
* Downstream processing becomes less expensive.

The index does not directly perform the `$group`; it reduces the input that the aggregation must group.

### Step 7: Test the field order

Create an alternative index for controlled comparison:

```javascript
db.orders.createIndex(
  {
    orderedAt: 1,
    status: 1
  },
  {
    name: "idx_orders_orderedAt_status_test"
  }
)
```

Test each index using `hint()`:

```javascript
db.orders.explain(
  "executionStats"
).aggregate(
  salesPipeline,
  {
    hint: "idx_orders_status_orderedAt"
  }
)
```

```javascript
db.orders.explain(
  "executionStats"
).aggregate(
  salesPipeline,
  {
    hint: "idx_orders_orderedAt_status_test"
  }
)
```

Compare:

* Keys examined
* Documents examined
* Execution time
* Index bounds
* Behavior across different months and status distributions

Do not keep both automatically. Retain the index that best supports the broader workload, not merely one isolated test.

### Step 8: Add product-category analysis

Join the current product record:

```javascript
const categorySalesPipeline = [
  {
    $match: {
      status: {
        $in: [
          "Shipped",
          "Delivered",
          "Completed"
        ]
      },

      orderedAt: {
        $gte: ISODate("2026-09-01T00:00:00Z"),
        $lt: ISODate("2026-10-01T00:00:00Z")
      }
    }
  },

  {
    $unwind: "$items"
  },

  {
    $lookup: {
      from: "products",
      localField: "items.productId",
      foreignField: "_id",
      as: "product"
    }
  },

  {
    $unwind: "$product"
  },

  {
    $group: {
      _id: "$product.category",

      unitsSold: {
        $sum: "$items.quantity"
      },

      revenue: {
        $sum: "$items.lineTotal"
      },

      uniqueCustomers: {
        $addToSet: "$customerId"
      }
    }
  },

  {
    $project: {
      _id: 0,
      category: "$_id",
      unitsSold: 1,
      revenue: 1,

      customerCount: {
        $size: "$uniqueCustomers"
      }
    }
  },

  {
    $sort: {
      revenue: -1
    }
  }
];
```

Run:

```javascript
db.orders.aggregate(categorySalesPipeline)
```

The foreign field used by `$lookup` is `products._id`, which already has an index by default.

### Step 9: Validate correctness

Performance tuning must not change the report’s meaning.

Check:

```javascript
db.orders.countDocuments({
  status: {
    $in: [
      "Shipped",
      "Delivered",
      "Completed"
    ]
  },

  orderedAt: {
    $gte: ISODate("2026-09-01T00:00:00Z"),
    $lt: ISODate("2026-10-01T00:00:00Z")
  }
})
```

Validate sample totals manually:

```javascript
db.orders.find({
  orderNumber: "ORD-2026-1001"
})
```

Confirm:

* Included statuses are correct.
* Date boundaries are correct.
* Cancelled orders are excluded.
* Quantities are not double-counted.
* `lineTotal` uses a consistent numeric type.
* Missing product matches are handled intentionally.
* The report timezone matches the business requirement.

### Step 10: Clean up the test-only index

If testing shows the reverse-order index is unnecessary:

```javascript
db.orders.dropIndex(
  "idx_orders_orderedAt_status_test"
)
```

Keep:

```text
idx_orders_status_orderedAt
```

only if it supports an important workload and provides measurable value.

---

## 15. Production Readiness Checklist

### Data model

* Documents reflect access patterns.
* Embedded arrays are bounded.
* Historical snapshots are intentional.
* Field names and BSON types are consistent.
* Large documents have been evaluated.
* Validation rules protect essential invariants.
* Schema evolution has a migration strategy.

### Queries

* Results are filtered and bounded.
* Pagination is implemented where required.
* Queries use appropriate projection.
* Array queries use `$elemMatch` where necessary.
* Dates and timezones are handled consistently.
* Expensive query shapes have been tested at realistic scale.

### Indexes

* Important query shapes have supporting indexes.
* Compound field order has been validated.
* Unique indexes enforce business rules.
* Redundant and unused indexes are reviewed.
* Write overhead has been measured.
* Explain plans have been captured before and after tuning.

### Aggregation

* Selective `$match` stages appear early.
* `$unwind` expansion is controlled.
* `$lookup` fields are indexed appropriately.
* Grouping cardinality is understood.
* Large sorts are monitored.
* Output is verified for correctness.

### Security

* Authentication is enabled.
* Least-privilege roles are used.
* TLS protects network traffic.
* Credentials are stored securely.
* Network exposure is restricted.
* Sensitive fields are protected appropriately.
* Security activity is monitored.
* Dependencies and MongoDB versions are patched according to policy.

### Availability and recovery

* Production deployments use appropriate replication.
* Clients use topology-aware connection strings.
* Read and write concerns match business requirements.
* Backups are independent from replication.
* Restore procedures are tested.
* RPO and RTO are documented.
* Failover behavior is tested.

### Operations

* Metrics and alerts are configured.
* Slow queries are monitored.
* Logs are centralized and protected.
* Capacity trends are reviewed.
* Replication lag is monitored.
* Disk space alerts are configured.
* Deployment changes are documented.
* Operational runbooks exist.

---

## 16. Course Wrap-Up

The course progression can be summarized as follows:

| Module                      | Core capability                          |
| ------------------------------ | ------------------------------------------- |
| 1. Introduction to NoSQL    | Select an appropriate database model     |
| 2. Installation and Setup   | Establish and verify MongoDB             |
| 3. Data Modeling            | Design documents around access patterns  |
| 4. Query Language           | Retrieve and manipulate documents        |
| 5. Aggregation              | Transform data into analytical results   |
| 6. Indexing                 | Improve query performance using evidence |
| 7. Replication and Sharding | Design for availability and scale        |
| 8. Best Practices           | Operate MongoDB securely and reliably    |

The most important principles are:

1. Model around how the application uses data.
2. Embed bounded data that belongs together.
3. Reference shared, independent or unbounded data.
4. Keep field names and data types consistent.
5. Design indexes around real query shapes.
6. Measure performance before and after optimization.
7. Filter early in aggregation pipelines.
8. Apply authentication, authorization, TLS and network restrictions.
9. Treat replication, sharding and backups as different capabilities.
10. Troubleshoot from evidence instead of assumptions.

---

## 17. Question-and-Answer Discussion Prompts

Use these prompts to close the course:

1. When would you choose MongoDB instead of a relational database?
2. When should related data be embedded?
3. When should related data be referenced?
4. Why is an unbounded array dangerous?
5. What is the difference between `find()` and aggregation?
6. How does a compound-index prefix affect query support?
7. Why can too many indexes harm performance?
8. What does `COLLSCAN` mean?
9. How are replication and sharding different?
10. Why is replication not a backup?
11. What makes a strong shard key?
12. How would you diagnose a suddenly slow API endpoint?
13. Which security controls are essential before production?
14. How would you prevent duplicate order processing?
15. Which metrics would you monitor after deployment?

After completing the module, learners should be able to review a MongoDB application from schema, query, performance, security and operational perspectives—and justify each recommendation with observable evidence.

# Module 7: Introduction to Sharding and Replication

MongoDB uses two complementary mechanisms to support demanding production workloads:

* **Replication** maintains multiple copies of the same data for high availability.
* **Sharding** distributes different portions of data across multiple servers for horizontal scalability.

A production sharded cluster commonly uses both:

```text
Sharding distributes the dataset
            +
Replication protects each shard
```

---

## 1. High Availability and Scalability

These concepts solve different problems.

### High availability

High availability means the database remains accessible when a server or infrastructure component fails.

MongoDB provides high availability through replica sets:

```text
Same dataset
├── Primary copy
├── Secondary copy
└── Secondary copy
```

If the primary becomes unavailable, eligible replica-set members hold an election and select a new primary.

### Scalability

Scalability means increasing a system’s capacity as the workload grows.

A database may need additional capacity because of:

* More application users
* Larger datasets
* Higher write throughput
* Increased query traffic
* Larger indexes
* Analytical workloads
* Geographic expansion

There are two primary scaling strategies.

#### Vertical scaling

Vertical scaling increases the resources of one server:

```text
More CPU
More memory
Faster storage
Larger disk
```

Advantages:

* Relatively simple
* No data distribution required
* Fewer infrastructure components

Limitations:

* A server has a maximum size
* Larger hardware can be expensive
* Maintenance may affect the entire workload
* It does not independently provide high availability

#### Horizontal scaling

Horizontal scaling adds more servers and distributes the workload:

```text
Application workload
       │
       ▼
┌────────┬────────┬────────┐
│ Shard 1│ Shard 2│ Shard 3│
└────────┴────────┴────────┘
```

MongoDB provides horizontal data scaling through sharding.

---

## 2. Replication Versus Sharding

| Requirement                        | Replication          | Sharding                             |
| ----------------------------------- | --------------------- | -------------------------------------- |
| Maintain multiple copies           | Yes                  | Not by itself                        |
| Automatic primary failover         | Yes                  | Each shard normally uses replication |
| Increase data capacity             | Limited              | Yes                                  |
| Distribute write workload          | Not normally         | Yes                                  |
| Protect against one server failure | Yes                  | Only when shards are replicated      |
| Scale beyond one server            | Not the main purpose | Yes                                  |
| Main objective                     | Availability         | Capacity and throughput              |

### Important distinction

Replication does not normally divide the dataset. Each data-bearing replica-set member maintains a copy of the replica set’s data.

Sharding divides a collection’s documents across shards. Each shard stores only its assigned portion of the sharded dataset.

---

## 3. Replica Set Fundamentals

A replica set is a group of `mongod` processes that maintain the same dataset.

A common configuration contains three data-bearing members:

```text
                 Application
                      │
                      ▼
              ┌──────────────┐
              │   Primary    │
              │ Reads/Writes │
              └──────┬───────┘
                     │ oplog replication
             ┌───────┴────────┐
             ▼                ▼
      ┌─────────────┐  ┌─────────────┐
      │ Secondary 1 │  │ Secondary 2 │
      │ Data copy   │  │ Data copy   │
      └─────────────┘  └─────────────┘
```

Replica sets are the foundation of MongoDB high availability.

---

## 4. Primary Member

The primary receives write operations:

```javascript
db.orders.insertOne({
  orderNumber: "ORD-2026-2001",
  status: "Processing",
  total: NumberDecimal("125.00"),
  orderedAt: new Date()
})
```

The primary:

1. Applies the write.
2. Records the operation in its operation log.
3. Makes that operation available for secondary members to replicate.

MongoDB applies replica-set writes on the primary and records them in the primary’s oplog.

A replica set normally has one writable primary at a time.

---

## 5. Secondary Members

Secondaries maintain copies of the primary’s data.

Each secondary:

1. Reads operations from the replication stream.
2. Applies those operations locally.
3. Maintains a copy of the dataset.
4. Participates in elections when eligible.
5. Can potentially serve selected read workloads.

Applications cannot normally write directly to a secondary. Secondary reads are possible when an appropriate read preference is configured.

Because replication is asynchronous, a secondary may temporarily lag behind the primary.

---

## 6. The Oplog

The operation log, or oplog, is a special capped collection that records data-changing operations.

Conceptually:

```text
Primary write
    │
    ▼
Primary applies operation
    │
    ▼
Operation recorded in oplog
    │
    ▼
Secondaries copy the operation
    │
    ▼
Secondaries apply it locally
```

Examples of operations represented in the oplog include:

* Inserts
* Updates
* Deletes
* Certain administrative changes

The oplog has a fixed configured capacity. When it becomes full, older entries are overwritten.

### Replication window

The time covered by retained oplog entries is called the replication window.

If a secondary remains offline longer than the available window, it may be unable to catch up incrementally and may require resynchronization.

---

## 7. Replica Set Elections

If the primary becomes unreachable, eligible voting members hold an election.

```text
Before failure
Primary A
Secondary B
Secondary C

Primary A fails

Election occurs

After election
Unavailable A
Primary B
Secondary C
```

For an election to succeed, a candidate must obtain support from a majority of voting members.

A three-voter replica set can tolerate the loss of one voting member and still retain a majority:

```text
Total voters: 3
Majority:     2
```

A five-voter set can tolerate the loss of two voting members:

```text
Total voters: 5
Majority:     3
```

### Why odd numbers are common

An odd number of voting members helps produce a clear majority without adding a voter that cannot increase failure tolerance.

For example:

| Voting members | Majority | Members that may fail while retaining majority |
| --------------: | --------: | ------------------------------------------------: |
|              3 |        2 |                                              1 |
|              4 |        3 |                                              1 |
|              5 |        3 |                                              2 |

Four voters require three votes, so they do not tolerate more failures than three voters.

---

## 8. Failover Process

When the primary fails:

1. Replica-set members detect the failure.
2. An eligible secondary requests an election.
3. A majority selects a new primary.
4. The selected member transitions to primary.
5. Drivers discover the topology change.
6. Application operations resume after reconnection and server selection.

There is normally a short period during which writes cannot complete because no primary is available.

MongoDB drivers can detect primary loss and support retry behavior for certain operations.

Applications should still be designed to handle:

* Temporary connection errors
* Timeouts
* Retriable write failures
* Duplicate-request risks
* Transaction retries
* Short failover interruptions

---

## 9. Checking Replica Set Status

Connect to a replica-set member with `mongosh` and run:

```javascript
rs.status()
```

This displays:

* Replica-set name
* Current primary
* Secondary members
* Member health
* Member state
* Replication progress
* Election information

Display the replica-set configuration:

```javascript
rs.conf()
```

Check whether the connected server is writable:

```javascript
db.hello()
```

Useful response fields may include:

```javascript
{
  setName: "trainingRS",
  isWritablePrimary: true,
  secondary: false
}
```

---

## 10. A Basic Development Replica Set

A local learning environment can initialize a replica set after starting multiple `mongod` processes with the same replica-set name.

Conceptual configuration:

```javascript
rs.initiate({
  _id: "trainingRS",
  members: [
    {
      _id: 0,
      host: "localhost:27017"
    },
    {
      _id: 1,
      host: "localhost:27018"
    },
    {
      _id: 2,
      host: "localhost:27019"
    }
  ]
})
```

This is for a controlled local lab. Production deployments require additional planning for:

* Authentication
* TLS
* Network access
* Separate failure domains
* Monitoring
* Backups
* Storage
* Hostnames and certificates
* Resource allocation

MongoDB Atlas normally manages much of the replica-set infrastructure automatically.

---

## 11. Replica Set Connection String

Applications should receive multiple hosts in the connection configuration or use an SRV connection string.

Example:

```text
mongodb://db1:27017,db2:27017,db3:27017/training_store?replicaSet=trainingRS
```

The driver discovers:

* Which member is primary
* Which members are secondary
* When the topology changes
* Which server satisfies the requested operation

Connecting an application to only one host without proper replica-set discovery can weaken failover behavior.

---

## 12. Write Concern

Write concern controls the level of acknowledgment requested for a write.

### Basic acknowledged write

```javascript
db.orders.insertOne(
  {
    orderNumber: "ORD-2026-2002",
    status: "Processing"
  },
  {
    writeConcern: {
      w: 1
    }
  }
)
```

`w: 1` means the primary acknowledges the operation after accepting it under the applicable durability behavior.

### Majority write concern

```javascript
db.orders.insertOne(
  {
    orderNumber: "ORD-2026-2003",
    status: "Processing"
  },
  {
    writeConcern: {
      w: "majority"
    }
  }
)
```

This requests acknowledgment after the write has reached the calculated majority commit requirements.

#### Tradeoff

Stronger acknowledgment can provide better durability guarantees but may add latency.

Write concern should reflect the importance of the operation:

* Shopping-cart preference
* Completed payment
* Inventory deduction
* Audit record
* Temporary analytics event

These may require different durability decisions.

---

## 13. Read Preference

Read preference determines which eligible replica-set members may serve reads.

Common modes include:

| Mode                 | General behavior                                       |
| --------------------- | --------------------------------------------------------- |
| `primary`            | Reads from the primary                                 |
| `primaryPreferred`   | Uses primary when available                            |
| `secondary`          | Reads from eligible secondaries                        |
| `secondaryPreferred` | Prefers secondaries                                    |
| `nearest`            | Selects among eligible members based partly on latency |

### Default behavior

The typical default is:

```text
primary
```

This provides the simplest read-after-write behavior for many applications.

### Secondary-read tradeoff

Secondary reads can:

* Move selected read load away from the primary
* Support geographically distributed reading
* Help reporting workloads

But they may return data that is behind the primary.

Do not treat secondary reads as automatically “free scaling.” They require conscious consistency, latency and capacity decisions.

---

## 14. Read Concern

Read concern controls the consistency and isolation characteristics of returned data.

Common levels include:

* `local`
* `available`
* `majority`
* `linearizable`
* `snapshot`

For example:

```javascript
db.orders.find({
  status: "Completed"
}).readConcern("majority")
```

The appropriate level depends on whether the application prioritizes:

* Minimum latency
* Reading majority-committed data
* Transactional snapshots
* Stronger consistency guarantees

Read preference answers:

> Which member may serve the read?

Read concern answers:

> What visibility or consistency guarantees should the read have?

---

## 15. Replication Is Not Backup

A replica set improves availability, but it does not replace backups.

If a user accidentally runs:

```javascript
db.orders.deleteMany({})
```

the deletion is replicated to the secondaries.

Likewise, replication can propagate:

* Application bugs
* Accidental updates
* Malicious deletion
* Logical corruption

A backup provides a separate recovery point. A resilient system generally requires:

```text
Replication
    +
Backups
    +
Tested restoration procedures
```

---

## 16. What Is Sharding?

Sharding distributes documents from a collection across multiple shards.

Suppose `orders` contains hundreds of millions of documents. Instead of storing all orders on one replica set:

```text
All orders → One replica set
```

MongoDB can distribute them:

```text
Orders with key range A → Shard 1
Orders with key range B → Shard 2
Orders with key range C → Shard 3
```

The shard key determines how documents are distributed.

MongoDB defines sharding as a method for distributing data across multiple machines, with each document’s shard-key value determining its distribution.

---

## 17. Sharded Cluster Components

A traditional MongoDB sharded cluster contains:

1. Shards
2. Configuration servers
3. `mongos` query routers

```text
                 Applications
                      │
             ┌────────┴────────┐
             ▼                 ▼
          mongos 1          mongos 2
             │                 │
             └────────┬────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
     Shard 1       Shard 2       Shard 3
   Replica set   Replica set   Replica set
                      │
                      ▼
             Config server metadata
```

MongoDB documentation illustrates production sharded clusters using multiple `mongos` processes, configuration servers and replica-set shards.

---

## 18. Shards

A shard stores part of the sharded data.

In production, each shard is normally deployed as a replica set:

```text
Shard 1 replica set
├── Primary
├── Secondary
└── Secondary
```

This means:

* Sharding distributes data between shards.
* Replication provides availability within each shard.

If a shard were a single unreplicated server, that server would become a single point of failure for its assigned data.

---

## 19. The `mongos` Query Router

Applications connect to `mongos`, not directly to individual shards.

`mongos`:

1. Receives the application operation.
2. Reads cluster metadata.
3. Determines which shard or shards contain relevant data.
4. Sends the operation to those shards.
5. Combines results when necessary.
6. Returns the final result to the application.

MongoDB describes `mongos` as the interface through which applications access a sharded cluster.

`mongos` does not normally store the application dataset itself.

---

## 20. Config Servers

Config servers store sharded-cluster metadata, including information about:

* Sharded collections
* Shard membership
* Data distribution
* Shard-key ranges
* Cluster topology

`mongos` uses this metadata to route requests.

Config servers are themselves deployed with replication for availability.

They are critical infrastructure and should not be treated as ordinary application database servers unless intentionally using a supported architecture designed for that purpose.

---

## 21. Shard Keys

A shard key is an indexed field or combination of fields that MongoDB uses to distribute documents.

Example:

```javascript
{
  customerId: 1
}
```

Compound example:

```javascript
{
  customerId: 1,
  orderedAt: 1
}
```

Hashed example:

```javascript
{
  customerId: "hashed"
}
```

Once a collection is sharded, each document must have values for the complete shard key.

MongoDB divides the shard-key space into non-overlapping ranges and assigns those ranges to shards.

---

## 22. Ranged Sharding

Ranged sharding distributes documents according to ranges of shard-key values.

For:

```javascript
{
  orderedAt: 1
}
```

the conceptual distribution might be:

```text
Shard 1: Before January 2026
Shard 2: January–June 2026
Shard 3: After June 2026
```

### Benefits

* Efficient range queries
* Related key values remain near one another
* Time-range operations can target relevant shards

### Risk

If new values always increase, such as timestamps, new writes may initially concentrate in one area of the key space. This can create a write hotspot.

---

## 23. Hashed Sharding

Hashed sharding calculates a hash of the shard-key value and distributes hash ranges.

Example:

```javascript
{
  customerId: "hashed"
}
```

Conceptually:

```text
customerId
    │
    ▼
Hash function
    │
    ▼
Distributed hash value
    │
    ├── Shard 1
    ├── Shard 2
    └── Shard 3
```

### Benefits

* Often provides more even distribution
* Helps distribute monotonically increasing identifiers
* Can reduce concentration of writes

### Tradeoff

Hashed distribution is not naturally ordered by the original value, so range queries on that field may need to contact multiple shards.

---

## 24. Targeted Versus Scatter-Gather Queries

### Targeted query

A query containing an appropriate shard-key value can be routed to a specific shard or subset of shards:

```javascript
db.orders.find({
  customerId: customerId
})
```

If `customerId` is the shard key, `mongos` can determine where the customer’s data resides.

```text
mongos → Shard 2
```

### Scatter-gather query

A query that does not contain the shard key may need to be sent to every shard:

```javascript
db.orders.find({
  status: "Processing"
})
```

```text
             ┌→ Shard 1
mongos ──────┼→ Shard 2
             └→ Shard 3
```

The router gathers and merges the responses.

MongoDB notes that the fastest sharded queries are generally those routed to one shard using shard-key information.

Scatter-gather is not always wrong, but frequent high-volume scatter-gather operations may indicate that the shard key does not align with the workload.

---

## 25. Choosing a Shard Key

Shard-key selection is one of the most important sharding decisions.

A strong shard key should support:

* High cardinality
* Even value frequency
* Non-problematic value change patterns
* Common query targeting
* Balanced writes
* Long-term data growth

MongoDB describes an ideal shard key as one that distributes documents evenly while supporting common query patterns.

---

## 26. Shard-Key Cardinality

Cardinality means the number of distinct shard-key values.

### Low cardinality

```javascript
{
  status: "Processing"
}
```

An order status may have only a few possible values:

```text
Processing
Shipped
Delivered
Cancelled
```

This provides too few values to distribute a very large collection effectively.

### High cardinality

```javascript
{
  customerId: ObjectId("...")
}
```

A large customer base may have millions of distinct customer IDs.

Higher cardinality gives MongoDB more opportunities to divide the data.

---

## 27. Shard-Key Frequency

Frequency describes how commonly individual values occur.

Even with high overall cardinality, one extremely frequent value can create imbalance.

For example:

```text
customerId A → 10 orders
customerId B → 20 orders
customerId C → 50 million orders
```

`customerId C` may create an oversized or heavily accessed portion of data.

A suitable key should avoid a small number of dominant values.

MongoDB notes that uneven value frequency or insufficient cardinality can contribute to problematic data distribution.

---

## 28. Monotonically Changing Values

A monotonically increasing value continually grows:

* Timestamp
* Sequential order number
* Auto-incrementing identifier

Example:

```text
100001
100002
100003
100004
```

With ranged sharding, new inserts can concentrate at the high end of the range.

A hashed key can distribute such values more evenly, but this may reduce efficient range targeting.

The correct choice depends on whether the workload needs:

* Even write distribution
* Efficient range retrieval
* Customer or tenant locality
* Time-based locality

---

## 29. Query Locality

A shard key should align with frequent queries.

Suppose most operations retrieve one customer’s orders:

```javascript
db.orders.find({
  customerId: customerId
}).sort({
  orderedAt: -1
})
```

A candidate compound shard key could be:

```javascript
{
  customerId: 1,
  orderedAt: 1
}
```

Potential benefits:

* Queries for a particular customer can be targeted.
* Orders are logically organized by customer and time.
* The compound key has higher cardinality than status alone.

Potential limitation:

* A single extremely large customer could still create concentration.
* Queries by `status` without customer information may scatter.
* Write distribution must be evaluated against real customer activity.

---

## 30. Comparing Candidate Shard Keys

Consider the `orders` collection.

| Candidate                         | Advantage                       | Concern                                            |
| ----------------------------------- | ---------------------------------- | ----------------------------------------------------- |
| `{ status: 1 }`                   | Supports status queries         | Very low cardinality                               |
| `{ orderedAt: 1 }`                | Supports time ranges            | Monotonic write hotspot risk                       |
| `{ customerId: 1 }`               | Supports customer queries       | Large customers may concentrate data               |
| `{ customerId: "hashed" }`        | Even customer distribution      | Customer ranges and locality are reduced           |
| `{ region: 1, customerId: 1 }`    | Regional and customer targeting | Region-first queries and regional imbalance matter |
| `{ customerId: 1, orderedAt: 1 }` | Customer history targeting      | Distribution depends on customer workload          |

No shard key is universally correct. It must be evaluated using application traffic and realistic data distribution.

---

## 31. Chunks and Data Distribution

MongoDB divides shard-key space into logical ranges commonly discussed as chunks.

Conceptually:

```text
Chunk A: Key range 0–999       → Shard 1
Chunk B: Key range 1000–1999   → Shard 2
Chunk C: Key range 2000–2999   → Shard 3
```

As the dataset changes, MongoDB manages distribution across shards.

The balancing process moves ranges between shards to improve distribution:

```text
Before balancing

Shard 1: ████████████
Shard 2: ████
Shard 3: ███

After balancing

Shard 1: ██████
Shard 2: ██████
Shard 3: █████
```

Data movement consumes network, disk and compute resources, so production teams monitor migrations and workload impact.

---

## 32. Sharding Commands: Conceptual Example

Connect through `mongos`, then shard a collection using an appropriate shard key.

Example ranged key:

```javascript
sh.shardCollection(
  "training_store.orders",
  {
    customerId: 1,
    orderedAt: 1
  }
)
```

Example hashed key:

```javascript
sh.shardCollection(
  "training_store.orders",
  {
    customerId: "hashed"
  }
)
```

Inspect sharding status:

```javascript
sh.status()
```

A supporting index is required for shard-key operations. Sharding commands and prerequisites should be tested in a dedicated lab environment rather than applied casually to a production collection.

---

## 33. Replication Inside a Sharded Cluster

A production-style architecture might contain three shards, each implemented as a three-member replica set:

```text
Application
    │
    ▼
mongos routers
    │
    ├── Shard 1 replica set
    │   ├── Primary
    │   ├── Secondary
    │   └── Secondary
    │
    ├── Shard 2 replica set
    │   ├── Primary
    │   ├── Secondary
    │   └── Secondary
    │
    └── Shard 3 replica set
        ├── Primary
        ├── Secondary
        └── Secondary
```

If one server in Shard 2 fails:

* The Shard 2 replica set can elect another primary.
* Shards 1 and 3 continue operating.
* `mongos` updates its routing behavior as topology information changes.
* The application continues through the cluster interface, subject to failover timing.

---

## 34. Common Misconceptions

### “A replica set distributes writes across all members”

Normally, writes go to the primary. Secondaries replicate those writes.

### “Reading from secondaries always makes the application faster”

Secondary reads can distribute certain read workloads, but they may return stale data and can compete with replication work.

### “Sharding automatically improves every query”

Queries without an appropriate shard-key predicate may contact multiple shards and become more expensive.

### “More shards always mean better performance”

Additional shards add:

* Servers
* Network communication
* Routing
* Monitoring
* Balancing
* Operational complexity

MongoDB recommends beginning with an unsharded deployment when the dataset and workload fit comfortably on one server or replica set.

### “Replication is a backup”

Replication copies mistakes and deletions. Independent backups are still required.

### “The shard key is just another index”

The shard key determines data placement and query routing. Its consequences are much broader than those of a normal secondary index.

---

## 35. Practical Architecture Exercise

### Scenario

`training_store` has:

* 50 million customers
* 800 million orders
* Rapid growth across Canada and the United States
* Frequent customer-order-history queries
* Large daily write volume
* A requirement to continue operating after a server failure

### Step 1: Availability requirement

Each shard should be replicated:

```text
Shard → Replica set
```

This protects the shard from one-member failure within the designed fault tolerance.

### Step 2: Scaling requirement

The `orders` collection is distributed across multiple shards:

```text
Orders → Shard 1, Shard 2, Shard 3
```

### Step 3: Evaluate primary query pattern

Frequent query:

```javascript
db.orders.find({
  customerId: customerId
}).sort({
  orderedAt: -1
})
```

The shard key should allow customer-based routing.

### Step 4: Candidate shard key

```javascript
{
  customerId: 1,
  orderedAt: 1
}
```

### Step 5: Questions before selection

* Are orders distributed reasonably evenly between customers?
* Can one customer generate an extreme volume?
* Are most queries scoped to one customer?
* Are time-range queries global or customer-specific?
* Does the workload require regional placement?
* Are writes distributed across many customers?
* Would a hashed component better distribute writes?
* Which queries would become scatter-gather?
* How will the key behave in five years?

The final decision should be validated with representative production-like data and workload testing.

---

## 36. Diagnostic Exercises

### Exercise 1: Identify the mechanism

Choose replication, sharding or both.

| Requirement                                  | Answer                   |
| ---------------------------------------------- | --------------------------- |
| Continue after one database server fails     | Replication              |
| Store data larger than one server can handle | Sharding                 |
| Distribute high write volume                 | Sharding                 |
| Automatically elect a replacement primary    | Replication              |
| Scale data while tolerating server failures  | Both                     |
| Recover an order deleted last week           | Backup, not either alone |

### Exercise 2: Identify shard-key problems

#### Candidate: `{ status: 1 }`

Problem:

* Low cardinality
* Uneven frequency
* Few possible distribution boundaries

#### Candidate: `{ orderedAt: 1 }`

Potential problem:

* Monotonically increasing
* New writes may concentrate on one range

#### Candidate: `{ customerId: "hashed" }`

Benefits:

* High cardinality
* More even distribution
* Equality query on customer can be targeted

Tradeoff:

* Poorer support for range-based distribution using original customer ID values

### Exercise 3: Targeted or scatter-gather?

Assume the shard key is:

```javascript
{
  customerId: 1,
  orderedAt: 1
}
```

Customer history:

```javascript
db.orders.find({
  customerId: customerId
})
```

Result: potentially targeted because the query contains the shard-key prefix.

Status query:

```javascript
db.orders.find({
  status: "Processing"
})
```

Result: potentially scatter-gather because the query lacks the shard key.

One order by `_id` only:

```javascript
db.orders.find({
  _id: orderId
})
```

Result: potentially scatter-gather unless `_id` is also sufficient for routing under the chosen design.

---

# Module Outcome

After completing this module, learners should be able to:

* Distinguish high availability from horizontal scalability.
* Explain vertical and horizontal scaling.
* Describe primary, secondary and oplog responsibilities.
* Explain replica-set elections and majority requirements.
* Distinguish read preference, read concern and write concern.
* Explain why replication is not a backup.
* Identify shards, config servers and `mongos` routers.
* Explain targeted and scatter-gather operations.
* Compare ranged and hashed sharding.
* Evaluate shard-key cardinality, frequency, monotonicity and query locality.
* Explain how replication and sharding work together in production MongoDB architectures.

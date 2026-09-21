# Mastering MongoDB — Cheatsheet

Acronyms, definitions, and quick references by module.

---

## Module 1 — Introduction to NoSQL Databases

| Term | Definition |
|------|------------|
| **NoSQL** | “Not Only SQL” — a category of non-relational data models, not one product |
| **Document database** | Stores JSON-like records (documents) that may contain nested objects and arrays |
| **Key-value database** | Maps a key directly to a value; optimized for fast lookup (for example Redis) |
| **Column-family database** | Rows with flexible columns; typical for distributed high-write workloads (Cassandra, HBase) |
| **Graph database** | Nodes, edges, and properties; typical when relationship traversal is the query (Neo4j) |
| **Collection** | MongoDB equivalent of a table: a group of documents |
| **Document** | MongoDB equivalent of a row: one BSON record |
| **Field** | MongoDB equivalent of a column |
| **`_id`** | Unique identifier for a document; default type is ObjectId |
| **BSON** | Binary JSON — MongoDB’s on-disk document format (JSON-like on screen) |
| **Embedding** | Storing related data inside the same document |
| **Referencing** | Storing a related identifier and fetching the other document separately |
| **Driver** | Language library that sends application requests to the MongoDB server |

---

## Module 2 — Installation and Setup

| Term | Definition |
|------|------------|
| **`mongod`** | MongoDB database **server** process — stores data, accepts connections, writes logs |
| **`mongosh`** | MongoDB **Shell** — command-line **client**, not the server |
| **Compass** | Graphical desktop client for the same MongoDB server |
| **Connection string** | URI that tells a client how to reach MongoDB (protocol, host, port, credentials, options) |
| **`mongodb://`** | Standard connection-string scheme; lists hosts (and optional port) explicitly |
| **`mongodb+srv://`** | DNS seed-list scheme; common for managed clusters; discovers members via DNS |
| **Default port** | `27017` |
| **`bindIp`** | Configuration that controls which network interfaces `mongod` listens on |
| **Authentication** | “Who are you?” — username, password, authentication database |
| **Authorization** | “What are you allowed to do?” — roles and privileges |
| **`db.runCommand({ ping: 1 })`** | Connectivity check; success includes `ok: 1`. Does **not** prove write access |
| **`use dbName`** | Selects a database in the shell; it may not appear in `show dbs` until data is stored |

---

## Module 3 — Data Modeling with MongoDB

| Term | Definition |
|------|------------|
| **Access pattern** | What is requested, how often, which filters, what returns together, and how the data changes |
| **Embedding** | Storing related data inside the parent document (owned, bounded, often read together) |
| **Referencing** | Storing another document’s `_id` and fetching it separately (independent or unbounded data) |
| **Snapshot** | A copy of a value as it was at write time (for example purchase-time price on an order) |
| **Denormalization** | Intentionally copying selected fields to speed reads; requires an update policy |
| **Unbounded array** | An array that can grow for the life of the document — avoid it |
| **16 MiB limit** | Maximum BSON document size; stay comfortably smaller |
| **`$jsonSchema`** | Validator document that checks `bsonType`, `required`, `properties`, and similar rules on write |
| **`validationAction`** | `error` (reject) or `warn` (allow but log) |
| **`validationLevel`** | `strict` (all writes) or `moderate` (valid documents plus inserts) |
| **Attribute pattern** | Store similar optional fields as `{ name, value }` pairs |
| **Bucket pattern** | Group many time-based points into one bounded document |
| **Subset pattern** | Keep a hot subset on the parent; full set in another collection |
| **Extended reference** | Reference plus a few frequently displayed copied fields |
| **Computed pattern** | Store a calculated result (average rating, order total) and update it when sources change |
| **Outlier pattern** | Normal documents use the default shape; rare huge records use a different store |
| **Polymorphic pattern** | Different types share one collection and a common core (`type` / `category`) |
| **Decimal128** | BSON decimal type for money — prefer over Double |

---

## Module 4 — The MongoDB Query Language

| Term | Definition |
|------|------------|
| **Filter** | Document that selects which documents an operation affects |
| **Projection** | Document that selects which fields are returned |
| **Cursor** | Handle returned by `find()`; sort, skip, limit, then iterate |
| **`findOne()`** | Returns one matching document or `null` |
| **`find()`** | Returns a cursor of matching documents |
| **Implicit AND** | Two fields in one filter document must both match |
| **`$in` / `$nin`** | Field value is (not) in a list of alternatives |
| **`$or` / `$nor` / `$not`** | Logical or, none-of, and field-level negation |
| **`$exists`** | Field is present (`true`) or absent (`false`) |
| **`$type`** | Match a BSON type (for example `"decimal"`, `"string"`, `"null"`) |
| **`{ field: null }`** | Matches BSON null **or** a missing field |
| **`$all`** | Array contains every listed value (any order) |
| **`$size`** | Array has exactly this many elements |
| **`$elemMatch`** | Multiple conditions must apply to the **same** array element |
| **`$set` / `$unset`** | Set or remove named fields; other fields remain |
| **`$inc` / `$min` / `$max`** | Numeric increment; set only if lower / higher |
| **`$rename`** | Rename a field |
| **`$push` / `$addToSet`** | Append an array value; `$addToSet` skips duplicates |
| **`$pull` / `$pop`** | Remove matching values / remove first or last element |
| **`$` / `$[]` / `$[ident]`** | First matched, all, or filtered positional array updates |
| **`replaceOne()`** | Replaces the document except `_id`; omitted fields disappear |
| **Upsert** | Update a match, or insert if none — use a unique filter |
| **`$setOnInsert`** | Fields applied only when an upsert inserts |
| **`bulkWrite()`** | Several insert/update/delete operations in one round trip |
| **`matchedCount` / `modifiedCount`** | How many documents matched vs actually changed |
| **`countDocuments()`** | Accurate filtered count; prefer over legacy `count()` |
| **Soft delete** | Keep the document; set `active: false` and `deletedAt` |

---

## Module 5 — The Aggregation Framework

| Term | Definition |
|------|------------|
| **Aggregation pipeline** | Ordered list of stages; each stage’s output is the next stage’s input |
| **`aggregate()`** | Collection method that runs a pipeline array |
| **`$match`** | Filter pipeline documents (same query language as `find()`) |
| **`$project`** | Include, exclude, rename, or calculate fields; lists the output shape |
| **`$set` / `$addFields`** | Add or replace fields while keeping unspecified fields |
| **`$unset`** | Remove fields from pipeline documents (not from stored data) |
| **`$group`** | Combine documents that share `_id`; original fields are not kept unless accumulated |
| **`$group._id`** | Grouping key of the summary document — not necessarily the source `_id` |
| **`$sum: 1`** | Count documents in a group |
| **Accumulator** | `$sum` `$avg` `$min` `$max` `$first` `$last` `$push` `$addToSet` |
| **`$unwind`** | One pipeline document per array element |
| **`$lookup`** | Equality join; result is always an array in `as` |
| **`$facet`** | Several sub-pipelines on the same input; one output document of arrays |
| **`$bucket`** | Group numeric values into named ranges (lower bound inclusive) |
| **`$sort` → `$limit`** | Top-N pattern; limit before sort is the wrong N |
| **`$ifNull`** | Substitute a default for null or missing values |
| **Decimal128** | Required type for money in `$match` and arithmetic |
| **`$` vs `$$`** | `$field` is a document field; `$$var` is a pipeline variable (`$$item`, `$$ROOT`) |

---

## Module 6 — Indexing and Query Performance

| Term | Definition |
|------|------------|
| **Index** | Separate ordered structure of field values plus references to documents |
| **COLLSCAN** | Execution stage that reads collection documents |
| **IXSCAN** | Execution stage that reads index keys |
| **FETCH** | Load full documents after index hits |
| **Compound index** | One index on two or more fields; **order is part of the design** |
| **Prefix** | Left-to-right leading fields of a compound index that a query can use |
| **ESR** | Equality–Sort–Range guideline for compound-field order |
| **Multikey** | Index with one entry per array element |
| **Unique index** | Rejects duplicate keys (SKU, customerNumber, orderNumber) |
| **Partial index** | Indexes only documents matching `partialFilterExpression` |
| **Sparse index** | Omits documents that do not contain the indexed field |
| **TTL index** | Asynchronous expiration from a date field (`expireAfterSeconds`) |
| **Covered query** | Filter and projection satisfied from the index; no FETCH (exclude `_id` if it is not in the key) |
| **Selectivity** | How narrowly a predicate identifies documents (SKU high; `active` low) |
| **Query shape** | Filter fields/operators, sort, projection, collation — not example values |
| **`explain("executionStats")`** | Winning plan plus `nReturned`, `totalKeysExamined`, `totalDocsExamined` |
| **Hidden index** | Still maintained on writes; planner will not select it |
| **`$indexStats`** | Usage counters for the current process lifetime — not proof of unused in production |

---

## Module 7 — Introduction to Replication and Sharding

| Term | Definition |
|------|------------|
| **High availability** | Keep the database service accessible during component failure — replica sets |
| **Horizontal scalability** | Spread data and workload across servers — sharding |
| **Replica set** | `mongod` processes that maintain copies of the same dataset; one primary at a time |
| **Primary** | Member that accepts writes and records them in the oplog |
| **Secondary** | Member that copies and applies oplog operations; may be elected primary |
| **Oplog** | Capped collection of data-changing operations used for replication |
| **Heartbeat** | Health exchange among members; does not copy application data |
| **Election** | Voting members select a new primary when the old one is unavailable or steps down |
| **Voting majority** | Enough voters to elect and keep a primary; prevents two writable primaries |
| **Arbiter** | Votes but stores no data; not a copy and not extra read capacity |
| **Replication lag** | Delay between apply on the primary and apply on a secondary |
| **Read preference** | Which replica-set member may serve a read |
| **Read concern** | Visibility / isolation guarantee for a read |
| **Write concern** | How many members must acknowledge a write |
| **Shard** | Partition of sharded data; production shards are replica sets |
| **Config servers (CSRS)** | Replica set that stores cluster metadata (keys, ranges, zones) |
| **`mongos`** | Query router; does not store application collection data |
| **Shard key** | Field(s) used to distribute documents in a sharded collection |
| **Cardinality** | Number of distinct shard-key values |
| **Chunk / range** | Logical slice of shard-key space that can live on a shard and move |
| **Balancer** | Process that redistributes ranges across shards |
| **Targeted query** | Router can pick the needed shard(s) from shard-key predicates |
| **Scatter-gather** | Query sent to many or all shards, then merged |
| **Hashed sharding** | Distribute by hash of the key; even writes, weak range locality |
| **Ranged sharding** | Contiguous key ranges; good range queries, monotonic hotspot risk |
| **Zone** | Association of key ranges with particular shards (residency, tiers) |

---

## Module 8 — Best Practices, Security, and Troubleshooting

| Term | Definition |
|------|------------|
| **Production-ready** | Secure, available, observable, recoverable, tested, documented — not merely able to query |
| **Least privilege** | Grant only the operations a workload needs; never put cluster-admin in application code |
| **Authentication** | “Who are you?” — identity proof (user, certificate, workload identity) |
| **Authorization** | “What may you do?” — roles and privileges |
| **TLS** | Encryption in transit, with certificate validation |
| **Encryption at rest** | Protection of disks, snapshots, backups, exports, and similar stored copies |
| **RPO** | Recovery Point Objective — maximum acceptable data loss, measured in time |
| **RTO** | Recovery Time Objective — maximum acceptable time to restore service |
| **PITR** | Point-in-time recovery — restore to a moment before a bad change |
| **Logical backup** | Export of database content (for example `mongodump`); portable subsets |
| **Physical backup** | Storage-level copy or snapshot; efficient full-environment restore |
| **Runbook** | Named alert, impact, diagnostics, actions, escalation, rollback, verification |
| **Actionable alert** | Has an owner, a threshold vs baseline, and a linked runbook — not a naked metric |
| **`$unwind` expansion** | One parent document becomes one document per array element; parent totals can be double-counted |

---

## General

| Term | Definition |
|------|------------|
| **TOC** | [`FINAL_TABLE_OF_CONTENTS.md`](FINAL_TABLE_OF_CONTENTS.md) — master course index |
| **Deck** | Combined Marp slide source at `slides/course-complete-marp-with-notes.md` |
| **`training_store`** | Sample database loaded from [`datasets/training_store`](datasets/training_store) |

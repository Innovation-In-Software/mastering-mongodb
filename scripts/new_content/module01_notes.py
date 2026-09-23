#!/usr/bin/env python3
"""Speaker notes for the new Module 1 deck (Introduction to NoSQL Databases).

Written from scripts/module01_content_source.md, the Module 1 manifest, the
official exercises and the training_store dataset, in plain short sentences.
Composed into the notes pane by mdb_speaker_notes.compose(), so the layout
matches the day decks: KEY TALKING POINTS / REAL-WORLD EXAMPLES / USE-CASE SCENARIO.

Keys are topic numbers. Diagram topics (see build_module01_new.DIAGRAMS) are
merged with the diagram's own "what it shows" notes on the same slide.
"""
from __future__ import annotations


def tp(point: str, explain: str) -> dict:
    return {"point": point, "explain": explain}


NOTES: dict[int, dict] = {
    1: {
        "talking_points": [
            tp("NoSQL is a family, not a product",
               "Start by saying that NoSQL is a category of databases. "
               "It is not one product, and it is not a replacement for SQL. "
               "MongoDB is one member of that family: a document database."),
            tp("What this module does",
               "We look at why NoSQL databases appeared, compare the four main NoSQL models, "
               "and then meet MongoDB: its documents, its architecture and when it fits. "
               "Everything uses one sample database, training_store."),
            tp("Where the course goes next",
               "Module 2 installs MongoDB and mongosh. "
               "Module 3 goes deep on data modeling. "
               "This module gives the vocabulary both of them need."),
        ],
        "real_world_examples": [
            "An online store can keep its product catalog in MongoDB, its shopping sessions in "
            "Redis and its general ledger in a relational database. "
            "Each store is chosen for the way that data is used.",
        ],
    },
    2: {
        "talking_points": [
            tp("By the end of this module",
               "Walk through the six objectives on the left. "
               "Learners should be able to define NoSQL as a category and compare the four "
               "NoSQL models. "
               "They should be able to explain documents, collections and BSON, and describe "
               "the basic MongoDB architecture. "
               "They should also be able to judge when MongoDB is and isn't a good fit, and "
               "read real documents in mongosh."),
            tp("Six questions this module answers",
               "Why did NoSQL databases appear? "
               "What are the four NoSQL models? "
               "What exactly is a MongoDB document? "
               "How is MongoDB built? "
               "When is MongoDB the right choice? "
               "And how do we read real data with mongosh?"),
            tp("Set the expectation",
               "The skill we are building is choosing a data model from the access pattern. "
               "Product popularity is not a reason. "
               "The roadmap at the bottom shows the path through the four parts."),
        ],
    },
    3: {
        "talking_points": [
            tp("Three kinds of data",
               "Structured data has rows, columns and a fixed schema, like a table of SKUs, "
               "prices and quantities. "
               "Semi-structured data has nested fields and arrays, and its shape can vary. "
               "Unstructured data, such as images, logs and video, has no fixed fields at all."),
            tp("Why this matters",
               "Relational tables are built for the first kind. "
               "Modern applications produce a lot of the second kind: products with different "
               "attributes, customer profiles, reviews and events."),
            tp("Our dataset",
               "In training_store, order totals and quantities are structured values. "
               "The products are semi-structured: a laptop has a processor and memory, a shoe "
               "has sizes and a material, a book has an author and an ISBN."),
        ],
    },
    4: {
        "talking_points": [
            tp("Relational databases are good at this",
               "Relational databases organize data into fixed tables of rows and columns. "
               "They work well when the structure is stable and relationships must be strictly "
               "enforced."),
            tp("Keys and joins",
               "Primary keys identify rows. "
               "Foreign keys tie an order to a real customer and an order item to a real "
               "product. "
               "SQL joins put the pieces back together when the application asks."),
            tp("Keep this in mind",
               "Nothing in this module says relational databases are obsolete. "
               "For stable, strongly related data with strict integrity rules, they are often "
               "the best choice."),
        ],
        "real_world_examples": [
            "A bank's general ledger has a fixed structure, strict integrity rules and "
            "transactions that touch several accounts at once. "
            "That is classic relational territory.",
        ],
    },
    5: {
        "talking_points": [
            tp("One page, many tables",
               "To show one complete order, the application reads the customer, the address, "
               "the order, every order item and the payment. "
               "That is five tables and several joins for a single page."),
            tp("Change is expensive",
               "When the catalog adds a new kind of product with new attributes, a fixed "
               "schema needs new columns, new tables or many optional columns. "
               "Each change means a migration."),
            tp("Scale is harder",
               "Relational databases traditionally scale up on a bigger server. "
               "Spreading joined tables across many servers is hard."),
            tp("Be fair",
               "These are costs, not failures. "
               "They grow as the data changes faster and the volume grows."),
        ],
        "use_case_scenario":
            "Imagine the store's busiest page is the order history. "
            "Every page view runs the same five-table join, thousands of times a minute. "
            "The data rarely changes after the order is placed, yet it is reassembled every "
            "time.",
    },
    6: {
        "talking_points": [
            tp("Not Only SQL",
               "NoSQL means Not Only SQL. "
               "It refers to databases designed to store and retrieve data using models other "
               "than relational tables."),
            tp("Four families",
               "The four main NoSQL families are document, key-value, column-family and graph. "
               "Each organizes data differently, and each is fast at a different kind of "
               "access."),
            tp("Both exist",
               "NoSQL doesn't mean SQL databases are obsolete. "
               "The right database depends on the application's data, access patterns, "
               "consistency requirements and scale. "
               "Many real systems use both."),
        ],
    },
    7: {
        "talking_points": [
            tp("What pushed teams to NoSQL",
               "NoSQL databases address frequently changing data structures, large volumes of "
               "data and high-speed reads and writes. "
               "They also address distributed applications and horizontal scaling across many "
               "servers."),
            tp("The four outcomes",
               "Flexible schema lets fields change as the product changes. "
               "Horizontal scale adds servers instead of buying a bigger one. "
               "Availability keeps copies on several servers, so one failure doesn't stop the "
               "application. "
               "Faster delivery comes from storing objects the way the application already "
               "uses them."),
            tp("Keep the balance",
               "These are reasons to consider NoSQL, not a guarantee. "
               "A good design still starts from how the application reads and writes."),
        ],
    },
    8: {
        "talking_points": [
            tp("Document",
               "A document database stores self-contained, JSON-like documents. "
               "Examples are MongoDB and Couchbase."),
            tp("Key-value",
               "A key-value store keeps each value under a unique key and returns it when you "
               "give it that key. "
               "Examples are Redis and Amazon DynamoDB."),
            tp("Column-family",
               "A column-family store keeps wide rows found by a row key, with columns grouped "
               "into families, and rows can have different columns. "
               "Examples are Apache Cassandra and HBase."),
            tp("Graph",
               "A graph database stores nodes and the relationships between them as "
               "first-class data. "
               "Examples are Neo4j and Amazon Neptune."),
        ],
    },
    9: {
        "talking_points": [
            tp("Self-contained documents",
               "Document databases store information as self-contained documents, usually in a "
               "JSON-like format. "
               "Their main advantage is that one application object can often be stored as one "
               "document, without splitting it across many tables."),
            tp("A real training_store product",
               "The code card shows the Trail Shoe, SKU S210, from our products collection. "
               "Its sizes array and its color and material sit inside an attributes "
               "sub-document. "
               "A laptop in the same collection has a processor and memory instead."),
            tp("Where they fit",
               "Document databases suit product catalogs, customer profiles, content "
               "management, mobile and web applications, and order management."),
        ],
    },
    10: {
        "talking_points": [
            tp("How it works",
               "A key-value database stores each value under a unique key. "
               "The application provides the key, and the database returns the value."),
            tp("Opaque values",
               "The store usually treats the value as an opaque blob. "
               "It doesn't query inside the value; it simply returns it."),
            tp("Strengths and limits",
               "Access is very fast when the application knows the key. "
               "Typical uses are caching, user sessions, shopping carts, preferences and "
               "real-time counters. "
               "Complex, relationship-based queries are difficult."),
        ],
        "real_world_examples": [
            "A web store keeps each shopper's session under a key like session:abc in Redis. "
            "Every page request reads it by that key in well under a millisecond.",
        ],
    },
    11: {
        "talking_points": [
            tp("Row key first",
               "In a column-family store, every lookup starts from a row key, here a "
               "customerId."),
            tp("Families of columns",
               "Related columns are grouped into column families: profile, orders and "
               "activity. "
               "The application usually reads one family at a time."),
            tp("Sparse rows",
               "A row stores only the columns it actually has. "
               "The dashes in the diagram are missing values, and they cost nothing."),
            tp("Where they fit",
               "Column-family stores such as Apache Cassandra and HBase handle very large, "
               "distributed write volumes, such as events, sensor readings and time series."),
        ],
    },
    12: {
        "talking_points": [
            tp("Nodes, edges and properties",
               "A graph database represents data as nodes, such as customers and products, and "
               "edges, the relationships between them. "
               "Both nodes and edges can carry properties."),
            tp("The same store, as a graph",
               "These are real training_store facts drawn as a graph. "
               "Aisha Khan, customer C101, ordered the Business Laptop and the USB Hub, and "
               "reviewed the laptop with five stars. "
               "Luis Romero, customer C204, ordered the Business Laptop too."),
            tp("Traversal is the strength",
               "A recommendation is a walk along the edges: Luis ordered L100, Aisha also "
               "ordered L100, and Aisha ordered A400. "
               "So we can suggest the USB Hub to Luis. "
               "Graph databases make multi-step walks like this fast."),
            tp("Where they fit",
               "Social networks, recommendation engines, fraud detection, network analysis and "
               "identity and access relationships. "
               "Examples are Neo4j and Amazon Neptune."),
        ],
    },
    13: {
        "talking_points": [
            tp("A document database",
               "MongoDB is a document-oriented NoSQL database. "
               "It stores data as BSON documents, grouped into collections."),
            tp("BSON",
               "BSON is a binary representation of JSON-like data. "
               "It adds types that JSON doesn't have, such as dates, decimals and ObjectIds."),
            tp("Our four collections",
               "training_store has four collections: customers, products, orders and reviews. "
               "After the full load there are 6 customers, 13 products, 17 orders and 6 "
               "reviews."),
        ],
    },
    14: {
        "talking_points": [
            tp("The hierarchy",
               "A MongoDB deployment contains databases. "
               "A database contains collections. "
               "A collection contains documents, and a document contains fields."),
            tp("Walking it in mongosh",
               "show dbs lists the databases. "
               "use training_store selects ours. "
               "show collections lists its collections, and db.products.findOne() prints one "
               "document. "
               "That is exactly the path of Exercise 1.3."),
            tp("Created on first write",
               "MongoDB creates a database or a collection the first time you insert into it. "
               "There is no separate CREATE TABLE step."),
            tp("About the sample document",
               "The document in the diagram is a simplified illustration. "
               "A real one from our products collection is B300, MongoDB Fundamentals, priced "
               "at 59.99."),
        ],
    },
    15: {
        "talking_points": [
            tp("The mapping",
               "A relational table maps to a collection, a row to a document, and a column to "
               "a field. "
               "The primary key maps to _id."),
            tp("Where the mapping breaks",
               "A document can hold nested objects and arrays that a single row can't. "
               "So one document often replaces several joined rows."),
            tp("Joins",
               "Instead of joining at read time, MongoDB usually embeds data that is read "
               "together, or stores a reference to another document. "
               "When a join is really needed, the $lookup aggregation stage can do one."),
            tp("Schema",
               "The schema is implicit: it comes from the documents themselves. "
               "When fields must always exist or have a type, you add schema validation."),
        ],
    },
    16: {
        "talking_points": [
            tp("_id",
               "Every document has an _id field that is unique within its collection. "
               "If you don't supply one, the driver or mongosh adds an ObjectId. "
               "An ObjectId is 12 bytes and starts with a timestamp."),
            tp("Typed values",
               "BSON keeps real types: String, Decimal128, Boolean, Date, arrays and embedded "
               "documents. "
               "mongosh shows them as JSON-like text, but they are stored as typed binary."),
            tp("Money and time",
               "Use Decimal128 for prices, so 129.99 stays exactly 129.99. "
               "Use real dates, not date strings, so you can sort and filter by time."),
            tp("A warning from our dataset",
               "training_store deliberately contains one product, XBAD, whose price is the "
               "string \"49.99\" instead of a number. "
               "Module 4 uses it in the $type labs to find and fix values stored with the "
               "wrong type."),
        ],
    },
    17: {
        "talking_points": [
            tp("Normalized rows",
               "In the relational model, one order is spread across three tables: customers, "
               "orders and order_items. "
               "Showing it means joining them on customer_id and order_id."),
            tp("One aggregate",
               "In MongoDB the order becomes one document. "
               "The line items are an embedded array, and each keeps its purchase-time price."),
            tp("Snapshot or reference",
               "This diagram embeds a customer snapshot: id, name and email. "
               "That is one valid choice, and it is the shape Exercise 1.2 asks for. "
               "Our training_store orders make the other choice: they keep a customerId "
               "reference. "
               "The next slide shows why."),
        ],
    },
    18: {
        "talking_points": [
            tp("Same collection, different fields",
               "Documents in the same collection don't need identical fields. "
               "The laptop carries cpu and ram; the book carries isbn and pages."),
            tp("A shared core",
               "Both documents still share the core fields: _id, sku, name, category, price and "
               "active. "
               "The application can rely on those."),
            tp("Flexible doesn't mean unplanned",
               "This flexibility helps applications evolve without constant table redesign. "
               "But a flexible schema still needs design. "
               "Schema validation can require fields and types where the business needs "
               "rules."),
        ],
        "real_world_examples": [
            "In training_store the products collection holds four categories: LAPTOP, SHOE, "
            "BOOK and ACCESSORY. "
            "Each one keeps its own attributes, such as memoryGB for laptops and sizes for "
            "shoes.",
        ],
    },
    19: {
        "talking_points": [
            tp("Clients",
               "Applications talk to MongoDB through language-specific drivers. "
               "People use mongosh, the MongoDB Shell, and MongoDB Compass, the graphical tool."),
            tp("mongod",
               "mongod is the main MongoDB server process. "
               "It manages connections, queries, indexes, authentication, replication and "
               "database operations."),
            tp("Storage engine and data files",
               "Below mongod, the storage engine, WiredTiger by default, keeps a cache, writes a "
               "journal for durability, and reads and writes the data files. "
               "Those files hold our databases and collections."),
        ],
    },
    20: {
        "talking_points": [
            tp("Follow one request",
               "A client asks for products. "
               "The request travels over the MongoDB wire protocol to mongod on port 27017 by "
               "default."),
            tp("Inside mongod",
               "mongod parses the request and checks that the user is authorized. "
               "The query planner then chooses a plan: an index seek, or a scan of the whole "
               "collection."),
            tp("The result",
               "Matching documents are fetched and returned to the client as BSON. "
               "The driver or mongosh turns them into objects you can read."),
        ],
    },
    21: {
        "talking_points": [
            tp("Replica set",
               "A replica set is a group of MongoDB servers that keep copies of the same data. "
               "The primary accepts writes. "
               "Secondaries copy the primary's changes from its operations log, the oplog."),
            tp("Automatic failover",
               "If the primary fails, the remaining members hold an election and an eligible "
               "secondary becomes the new primary. "
               "Three members is the usual minimum, so a majority can still vote."),
            tp("Sharded cluster",
               "Sharding spreads a large dataset across several shards. "
               "Each shard is itself a replica set. "
               "Config servers store the cluster metadata, and mongos routers send each request "
               "to the right shards."),
            tp("When to shard",
               "Sharding is for when one server can't efficiently handle the whole dataset or "
               "workload. "
               "Module 7 covers both topics in depth."),
        ],
    },
    22: {
        "talking_points": [
            tp("Rich queries",
               "MongoDB supports filtering, sorting, projection and updates. "
               "It can also query arrays, run geospatial and text searches, and build "
               "aggregation pipelines."),
            tp("Indexes and aggregation",
               "Indexes help MongoDB find documents without scanning the whole collection. "
               "Aggregation pipelines pass documents through stages for reporting and "
               "analysis."),
            tp("Replication and sharding",
               "Replica sets give high availability, and sharding gives horizontal scale. "
               "Drivers connect applications in many languages."),
            tp("Rules when you need them",
               "A flexible schema can still enforce rules with schema validation. "
               "Single-document writes are atomic, and multi-document ACID transactions are "
               "available when a business process needs them."),
        ],
    },
    23: {
        "talking_points": [
            tp("Strong signals for MongoDB",
               "Varied attributes, such as product specifications. "
               "Data accessed together, such as an order and its line items. "
               "An evolving schema, such as new catalog fields."),
            tp("More signals",
               "Document aggregates, such as a review with its rating. "
               "And horizontal growth, such as a fast-growing orders collection that may one "
               "day need sharding."),
            tp("The principle",
               "A good MongoDB design doesn't simply move relational tables into collections. "
               "It models documents around how the application reads, writes and updates its "
               "data."),
        ],
    },
    24: {
        "talking_points": [
            tp("Consider alternatives",
               "These are workloads where another database may fit better. "
               "They are not things MongoDB cannot do."),
            tp("Transactions and reporting",
               "MongoDB supports multi-document transactions. "
               "But if most of the work spans many entities at once, like orders, payments and "
               "inventory together, a relational design may be simpler. "
               "Strict, fixed tabular reporting is also a natural relational fit."),
            tp("Other shapes",
               "Tiny single-value records with no aggregate gain little from documents. "
               "Deep relationship paths suit a graph database. "
               "A pure session cache suits a key-value store."),
        ],
    },
    25: {
        "talking_points": [
            tp("Before",
               "The relational catalog spreads each product across products, categories, "
               "attributes and inventory tables. "
               "Every catalog page needs many joins."),
            tp("Reshape and load",
               "The team reshapes each product into one document with its sku, name, price, "
               "tags and specifications. "
               "Then it loads those documents into the products collection."),
            tp("Same API",
               "The catalog API, GET /catalog/products, keeps its contract. "
               "Behind it, each product is now one document read."),
        ],
        "use_case_scenario":
            "A retailer's product pages are slow because each one joins four tables. "
            "The team models one product document around what the page shows, loads the "
            "catalog into MongoDB and switches the API to read it. "
            "The web and mobile apps don't change at all.",
    },
    26: {
        "talking_points": [
            tp("Why NoSQL",
               "Scale and flexibility for data that doesn't fit fixed tables."),
            tp("Four models",
               "Key-value, document, column-family and graph, each fast at a different access "
               "pattern."),
            tp("MongoDB",
               "BSON documents in collections, arranged as database, collection, document and "
               "field. "
               "Related data is embedded or referenced."),
            tp("Architecture",
               "mongosh, Compass and drivers talk to mongod, which stores training_store."),
        ],
    },
}

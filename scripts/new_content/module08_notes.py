#!/usr/bin/env python3
"""Speaker notes for the new Module 8 deck (Best Practices, Security and Troubleshooting).

Written from scripts/module08_content_source.md, the Module 8 manifest, the official
exercises 8.1-8.3 (labs/day-03/exercises/), Lab 7 (labs/day-03/lab7/) and the
training_store dataset, in
plain short sentences. Composed into the notes pane by mdb_speaker_notes.compose(), so
the layout matches the day decks: KEY TALKING POINTS / REAL-WORLD EXAMPLES / USE-CASE
SCENARIO.

Keys are topic numbers. Diagram topics use the diagram's number (see
build_module08_new.DIAGRAMS) and are merged with the diagram's own "what it shows"
notes on the same slide.

Where the content guide's generic example disagrees with training_store (field names
such as status, orderedAt, lineTotal or stock), the slides use the real fields and the
notes say so.
"""
from __future__ import annotations


def tp(point: str, explain: str) -> dict:
    return {"point": point, "explain": explain}


NOTES: dict[int, dict] = {
    1: {
        "talking_points": [
            tp("The last module",
               "This is the final module of the course. "
               "We stop learning new MongoDB features and start asking whether a MongoDB "
               "solution is safe to run for real."),
            tp("Production-ready is a claim you prove",
               "A database that accepts queries is only functional. "
               "Production-ready means the model holds up, queries are measured, access is "
               "locked down, restores are tested and someone can diagnose problems."),
            tp("Same dataset",
               "Everything uses training_store: 6 customers, 13 products, 17 orders and 6 "
               "reviews. "
               "By the end we decide whether it could go live — and why not yet."),
        ],
        "real_world_examples": [
            "Many real outages are not exotic bugs. "
            "They are a missing index after a release, an expired certificate, a disk that "
            "filled up, or a backup nobody had ever restored.",
        ],
    },
    2: {
        "talking_points": [
            tp("By the end of this module",
               "Learners can apply modeling, validation and schema-evolution rules, and tune "
               "queries, pipelines and indexes with explain evidence. "
               "They can secure access with authentication, least privilege, TLS and network "
               "limits, and plan backups against RPO and RTO. "
               "They can monitor health, troubleshoot by layer, and judge production "
               "readiness."),
            tp("Six questions",
               "Is the model safe to grow? How do we prove it is fast? Who may do what? "
               "Can we recover? What is wrong right now? Are we ready to go live?"),
            tp("How the module runs",
               "Five parts, three short practice exercises, a knowledge check, three official "
               "checkpoints — Exercises 8.1 to 8.3 — and Lab 7, which closes the course."),
        ],
    },
    3: {
        "talking_points": [
            tp("Three stages",
               "Functional: mongosh and Compass talk to one mongod with the four "
               "training_store collections. It works, and that is all. "
               "Hardened: authentication and TLS, indexes, validation and backups are added. "
               "Production-ready: a three-member replica set behind authentication and TLS, "
               "with monitoring, alerts and automated backups."),
            tp("Where training_store is today",
               "Our class instance is firmly in the first column. "
               "No authentication, one server, no validator, no tested restore. "
               "That is fine for learning — and the reason Lab 7 ends with not ready."),
            tp("Module 7 link",
               "The replica set in the third column is exactly what Module 7 built. "
               "Replication gives availability; this module adds everything around it."),
        ],
    },
    7: {
        "talking_points": [
            tp("Two questions",
               "First: is the data read and updated together with its parent? "
               "If yes, is it bounded? Bounded and owned data is embedded — order items in an "
               "order. "
               "If it grows without limit, reference it — reviews point to a product."),
            tp("The other branch",
               "If the data is not read together, ask whether many documents share it. "
               "Shared data such as a customer is referenced by customerId. "
               "Owned local detail such as product dimensions can still be embedded."),
            tp("training_store already follows this",
               "Orders embed items and a shippingAddress snapshot. "
               "They reference the customer with customerId. "
               "Reviews live in their own collection and carry productId and customerId."),
            tp("The anti-pattern to name",
               "Putting every review inside its product. "
               "A popular product's document would grow without limit and approach the 16 MB "
               "document limit, and every product read would drag the reviews along."),
        ],
    },
    10: {
        "talking_points": [
            tp("Mixed input",
               "The left panel shows the same idea written three ways: product_id or "
               "productId, Price or price, and the price as a string, a number or with an "
               "ObjectId key. "
               "Queries on one spelling silently miss the others."),
            tp("Normalize, then validate",
               "Pick one name per concept in camelCase and one BSON type per field: "
               "ObjectId for references, Decimal128 for money, Date for timestamps."),
            tp("training_store has real drift",
               "Product XBAD, the Legacy Cable Pack, stores price as the string '49.99'. "
               "The other 12 products use Decimal128. "
               "A range query on price never matches XBAD, and a sort puts it in the wrong "
               "place."),
            tp("Stray fields too",
               "L190 carries legacyName and A410 carries temporaryNote. "
               "Neither is part of the product model — they are leftovers to clean up."),
        ],
    },
    11: {
        "talking_points": [
            tp("What validation does",
               "mongod checks every insert and update against the collection's $jsonSchema. "
               "A valid document is stored; an invalid one is rejected with a validation "
               "error, code 121."),
            tp("Read the diagram's rule",
               "It requires name as a string, price as a number of zero or more, and a "
               "boolean flag. "
               "In $jsonSchema, bsonType number accepts int, long, double and Decimal128, so "
               "our Decimal128 prices pass it. "
               "training_store calls its flag active; inStock is the diagram's generic "
               "name."),
            tp("Cover what matters",
               "A validator does not have to list every field. "
               "Required fields, types, enums and ranges are enough. "
               "It complements application validation; it doesn't replace it."),
        ],
    },
    12: {
        "talking_points": [
            tp("Versions side by side",
               "Version 1 has name and price. "
               "Version 2 adds an optional category, so old and new documents are both "
               "valid. "
               "Version 3 backfills category everywhere and then tightens the validator."),
            tp("Old app keeps working",
               "The arrows from the old app show backward compatibility: it can still read "
               "v1 and v2 documents while the migration runs."),
            tp("The safe order",
               "Teach the application both shapes, write the new shape, migrate in "
               "controlled batches, measure, tighten validation, and only then remove the "
               "old code path. "
               "Never run one huge untested updateMany on production."),
        ],
    },
    13: {
        "talking_points": [
            tp("Copy at purchase",
               "When the order is placed, the product's name and price are copied into the "
               "order. "
               "Later the product's price changes from 89 to 99, but the order still says "
               "89."),
            tp("Intentional duplication",
               "This is not inconsistency. "
               "It is the historical truth of what the customer paid."),
            tp("In training_store",
               "The loader's snap() function copies productId, sku, name, quantity and "
               "unitPrice into each order item. "
               "For example, O6102 keeps the Running Shoe at 129.99 and the Wireless Keyboard "
               "at 49.99, even though the keyboard now has a discountPrice of 39.99. "
               "The diagram's Course Bundle P101 is a generic example."),
        ],
    },
    21: {
        "talking_points": [
            tp("Shrink the stream first",
               "The pipeline starts with many orders and many fields. "
               "$match keeps only the paid orders, $project keeps only the two fields the "
               "report needs, and $group then works on far less data."),
            tp("The numbers are illustrative",
               "The diagram shows 10,000 orders reduced to 1,200. "
               "Our class dataset has 17 orders, 13 of them paid, so timings will barely "
               "move. "
               "What matters is the shape of the plan."),
            tp("Field name",
               "The diagram's status is a generic name. "
               "In training_store the payment state is paymentStatus and the order date is "
               "createdAt."),
            tp("Indexes help only at the start",
               "A $match at the start of the pipeline can use an index. "
               "After $unwind or $group, the documents are new and no index applies."),
        ],
    },
    24: {
        "talking_points": [
            tp("Check the answer, not only the speed",
               "The pipeline says revenue is 300. "
               "A control total, calculated separately, also says 300. "
               "Only when both agree is the report validated."),
            tp("The $unwind trap in our data",
               "Unwinding items and then summing the order total counts each order once per "
               "item. "
               "For paid orders the true revenue is 9118.44, but the unwound version reports "
               "12119.25, because 13 orders become 21 item rows."),
            tp("A simple control",
               "countDocuments with paymentStatus PAID returns 13. "
               "If the pipeline's orderCount doesn't also add up to 13, something is double "
               "counted or filtered wrongly."),
        ],
    },
    25: {
        "talking_points": [
            tp("From query to index",
               "The frequent query filters on a customer and a payment state and sorts by "
               "date. "
               "The compound index lists the two equality fields first and the sort field "
               "last: equality, equality, sort."),
            tp("The payoff",
               "IXSCAN walks a narrow index range, examines about as many keys as it "
               "returns, and avoids a collection scan and an in-memory sort."),
            tp("Map it to training_store",
               "The diagram uses generic names: status, orderDate and a string customer "
               "code. "
               "Our fields are customerId, an ObjectId, paymentStatus and createdAt, so the "
               "index is customerId 1, paymentStatus 1, createdAt -1 — the one Exercise 8.1 "
               "recommends."),
            tp("Every index has a cost",
               "Each index uses disk and cache and slows every insert, update and delete. "
               "Name the query an index serves before creating it, and hide an index to test "
               "before dropping it."),
        ],
    },
    29: {
        "talking_points": [
            tp("Four numbers to read",
               "nReturned, totalKeysExamined, totalDocsExamined and executionTimeMillis. "
               "In the diagram all three counts are 24: the plan examined exactly what it "
               "returned."),
            tp("Plan stages",
               "IXSCAN reads the index, FETCH loads the documents. "
               "COLLSCAN means every document was read. "
               "A SORT stage means an in-memory sort that an index could have avoided."),
            tp("Our dataset",
               "Before an index, C101's paid-order history is a COLLSCAN that examines all "
               "17 orders to return 4. "
               "With the ESR index it examines 4 keys and 4 documents, with no SORT stage."),
            tp("A scan is not always wrong",
               "On a tiny collection, or when most documents are returned anyway, a "
               "collection scan can be the right plan."),
        ],
    },
    30: {
        "talking_points": [
            tp("Layers, not a single switch",
               "Traffic is encrypted with TLS. "
               "Then every connection is authenticated, authorized through roles, and "
               "limited to least privilege. "
               "Data files are encrypted at rest, and security events go to audit logs."),
            tp("Why layers",
               "If one control fails — a leaked password, a misconfigured firewall — the "
               "others still limit the damage."),
            tp("Our class instance",
               "The training instance runs without authentication on localhost. "
               "That is acceptable only because it is a disposable learning environment on "
               "one machine."),
        ],
    },
    31: {
        "talking_points": [
            tp("Who is connecting?",
               "Authentication proves identity. "
               "mongosh or Compass sends a username and password over TLS; mongod checks "
               "them against its user records."),
            tp("Success and failure",
               "Valid credentials give an authenticated session on training_store. "
               "Invalid credentials are refused before any data is touched."),
            tp("Turning it on",
               "On a self-managed server, security.authorization: enabled in mongod.conf "
               "switches access control on. "
               "Create the first administrative user before enforcing it, following the "
               "documented procedure."),
            tp("Never trust location alone",
               "Being on the same network is not proof of identity."),
        ],
    },
    33: {
        "talking_points": [
            tp("Grant only what the job needs",
               "The support analyst needs to read reviews. "
               "The minimum role allows the find action on the reviews collection only. "
               "Products, customers and orders stay locked, and there is no write at all."),
            tp("Blast radius",
               "If this analyst's credentials leak, the attacker can read reviews — nothing "
               "else. "
               "That is the point of least privilege."),
            tp("Separate identities",
               "The application, reporting, support, monitoring, backup and the DBA each get "
               "their own user and role. "
               "Exercise 8.2 builds exactly this matrix."),
        ],
    },
    34: {
        "talking_points": [
            tp("The network path",
               "Clients connect over TLS to a firewall that allows only trusted IP addresses "
               "on port 27017. "
               "Behind it, mongod sits on a private network and requires TLS itself."),
            tp("Untrusted sources are blocked",
               "Traffic from the internet never reaches mongod. "
               "Never expose port 27017 broadly to the public internet."),
            tp("bindIp",
               "bindIp controls which network interfaces mongod listens on. "
               "List localhost plus the specific private address the application uses. "
               "Binding to every interface on a reachable host, with authentication off, is "
               "how databases end up exposed."),
            tp("Managed option",
               "On MongoDB Atlas the same idea is an IP access list or a private endpoint."),
        ],
    },
    42: {
        "talking_points": [
            tp("Replication",
               "The primary copies every change to the secondaries continuously. "
               "If the primary fails, a secondary is elected. "
               "That is high availability."),
            tp("Why it's not a backup",
               "The red marks show the problem: a bad change on the primary is replicated "
               "too. "
               "Run db.orders.deleteMany({}) and every member loses the orders within "
               "seconds."),
            tp("Backup",
               "Backups are separate, immutable copies taken on a schedule. "
               "They let you restore an earlier state — the state before the mistake."),
            tp("You need both",
               "Replication for staying up, backups for going back."),
        ],
    },
    45: {
        "talking_points": [
            tp("Read the timeline",
               "The last backup ran at 10:00. "
               "The failure happened at 10:15. "
               "Service was restored at 10:45."),
            tp("RPO",
               "Recovery Point Objective: how much data you may lose. "
               "Here, the orders placed between 10:00 and 10:15 are at risk, so the RPO is "
               "15 minutes."),
            tp("RTO",
               "Recovery Time Objective: how long recovery may take. "
               "From 10:15 to 10:45 is 30 minutes."),
            tp("Business decides",
               "Orders and payments usually need the tightest RPO, often minutes with "
               "point-in-time recovery. "
               "Reviews can usually tolerate more."),
        ],
    },
    46: {
        "talking_points": [
            tp("Restore somewhere safe",
               "The backup is restored into an isolated test environment, never over the "
               "live database."),
            tp("Automated checks",
               "Check that the collections exist, the document counts match, and sample "
               "queries return the expected documents. "
               "Then record how long it took, so the RTO is measured, not guessed."),
            tp("Lab 7, Step 4",
               "Learners dump training_store and restore it into training_store_restore. "
               "They compare counts — 17 orders and 13 products — find one recorded order "
               "number, and check getIndexes()."),
        ],
    },
    49: {
        "talking_points": [
            tp("Three groups of metrics",
               "Database metrics: operations per second, connections and replication lag. "
               "Query metrics: latency, documents scanned versus returned, and slow "
               "queries. "
               "Resource metrics: CPU, memory and disk I/O."),
            tp("One health view",
               "All three feed one dashboard. "
               "A slow query shows up as latency and scanned documents before it shows up as "
               "CPU."),
            tp("The profiler",
               "db.setProfilingLevel(1) with slowms 200 and sampleRate 0.2 records a sample "
               "of operations slower than 200 milliseconds into system.profile. "
               "The profiler adds overhead, so turn it on deliberately and back off with "
               "db.setProfilingLevel(0)."),
        ],
    },
    54: {
        "talking_points": [
            tp("Four boxes",
               "Symptom: the orders query is slow. "
               "Layer: the problem is in query execution inside mongod. "
               "Cause: the filter on customerId has no index, so it scans the collection. "
               "Fix: create the customerId index and latency returns to normal."),
            tp("The verify loop",
               "The arrow back to the symptom matters most. "
               "Repeat the same test and compare latency, keys and documents examined."),
            tp("The full framework",
               "The content guide adds two steps: scope — one query or all, one instance or "
               "every instance — and evidence: logs, explain, metrics and recent changes."),
            tp("Smallest safe fix",
               "Add a targeted index, bound a query, correct a connection string, or fix one "
               "role. "
               "Not: restart everything, or grant root."),
        ],
    },
    59: {
        "talking_points": [
            tp("Follow one request",
               "Product search takes 2.8 seconds. "
               "The trace shows a query on training_store.products that filters by category "
               "and sorts by price."),
            tp("Explain, fix, verify",
               "explain() shows COLLSCAN — no matching index. "
               "A compound index on category and price supports both the filter and the "
               "sort, and the plan becomes IXSCAN at 85 milliseconds."),
            tp("Matches our data",
               "This is the same category-and-price index Module 1 showed in mongosh. "
               "For the active-only catalog page, Lab 7 suggests category, active, price."),
        ],
    },
    67: {
        "talking_points": [
            tp("The whole course in one picture",
               "mongosh and Compass connect to mongod, which holds training_store, its four "
               "collections, documents and fields."),
            tp("The path we took",
               "CRUD and aggregation on Day 2. "
               "Indexes and validation, replication and sharding on Day 3. "
               "And finally security, backup and monitoring in this module."),
            tp("Ask the room",
               "Ask learners which box they would find hardest to get right in their own "
               "systems — and why."),
        ],
    },
}

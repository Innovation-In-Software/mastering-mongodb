#!/usr/bin/env python3
"""Speaker notes for the new Module 6 deck (Indexing and Query Performance).

Written from scripts/module06_content_source.md, the Module 6 manifest, the
official Exercises 6.1-6.3, Day 3 Lab 5 and the training_store dataset, in
plain short sentences. Composed into the notes pane by mdb_speaker_notes.compose(),
so the layout matches the other decks: KEY TALKING POINTS / REAL-WORLD EXAMPLES /
USE-CASE SCENARIO.

Keys are topic numbers. Diagram topics (see build_module06_new.DIAGRAMS) are
merged with the diagram's own "what it shows" notes on the same slide.
"""
from __future__ import annotations


def tp(point: str, explain: str) -> dict:
    return {"point": point, "explain": explain}


NOTES: dict[int, dict] = {
    1: {
        "talking_points": [
            tp("Day 3 starts here",
               "Day 2 taught us to ask questions of training_store: find, update and the "
               "aggregation pipeline. "
               "Day 3 is about making those questions fast, then keeping the data available "
               "and scalable."),
            tp("What this module does",
               "We see how MongoDB finds documents with and without an index, create and manage "
               "named indexes, design compound indexes with the ESR guideline, meet the "
               "specialized index types, and prove every decision with explain()."),
            tp("The quote",
               "Index the query shape, not every field. "
               "An index is a trade: faster reads for one shape of query, paid for with "
               "storage and extra work on every write."),
        ],
        "real_world_examples": [
            "An online store's product page and order-history page run thousands of times an "
            "hour. "
            "Two well-chosen compound indexes can keep both fast, while ten speculative "
            "single-field indexes slow down every checkout.",
        ],
    },
    2: {
        "talking_points": [
            tp("By the end of this module",
               "Walk through the six objectives on the left. "
               "Learners explain how an index avoids a full scan, and manage named indexes. "
               "They order compound fields with ESR and choose specialized types. "
               "They read explain() output, build a covered query, and weigh selectivity, write "
               "cost and usage."),
            tp("Six questions",
               "Why does a query read every document? "
               "How do I create and manage indexes? "
               "Which field order goes in an index? "
               "Which index type fits the query? "
               "What does explain() really tell me? "
               "And when is an index not worth its cost?"),
            tp("Set the expectation",
               "training_store is tiny: 13 products and 17 orders. "
               "Every query will feel instant, with or without an index. "
               "So we judge a plan by its shape and its counts, keys and documents examined "
               "against documents returned, not by milliseconds."),
        ],
    },
    3: {
        "talking_points": [
            tp("Two paths for one query",
               "When a query arrives, mongod either walks an index to the matching documents or "
               "reads every document in the collection and tests each one."),
            tp("Why it matters",
               "A collection scan's cost grows with the collection. "
               "On a million orders the red path means a million documents read for a handful of "
               "results, and every other request waits behind it."),
            tp("On our data",
               "training_store is small enough that both paths finish in about a millisecond. "
               "That is why Lab 5 asks you to record counts, not times."),
        ],
        "real_world_examples": [
            "A customer-service screen that looks up orders by customer. "
            "Without an index it slows down a little more every day as the orders collection "
            "grows, until the support team notices.",
        ],
    },
    5: {
        "talking_points": [
            tp("COLLSCAN",
               "A collection scan reads every document and applies the filter to each one. "
               "It is the only option when no index matches the query."),
            tp("IXSCAN",
               "An index scan looks up the value in a sorted index, reads only the matching "
               "keys, and then fetches just those documents."),
            tp("The number to watch",
               "Compare documents examined with documents returned. "
               "8 examined for 3 returned is waste; 3 for 3 is the ideal."),
            tp("On training_store",
               "db.products.find({ category: \"BOOK\" }) on a fresh load is a COLLSCAN: 13 "
               "documents examined, 2 returned. "
               "With a category index it becomes IXSCAN: 2 keys, 2 documents, 2 returned."),
        ],
    },
    7: {
        "talking_points": [
            tp("An ordered structure",
               "An index stores the indexed values in sorted order, each with a pointer to its "
               "document. "
               "MongoDB keeps it as a B-tree, so a lookup takes a few steps down the tree."),
            tp("Sorted is the superpower",
               "Because keys are sorted, the same index answers equality, ranges such as price "
               "between 50 and 99, and sorts by price, without extra work."),
            tp("What it costs",
               "The tree lives on disk and in memory, and every insert, update or delete of an "
               "indexed value has to update it. "
               "We come back to that cost in Part 6."),
        ],
    },
    10: {
        "talking_points": [
            tp("Always there",
               "Every standard collection gets a unique index on _id, named _id_. "
               "A lookup by _id is always an index scan."),
            tp("Unique and permanent",
               "It prevents two documents from sharing an _id, and it cannot be dropped. "
               "dropIndexes() removes every other index but keeps _id_."),
            tp("On training_store",
               "Right after load.js, products has _id_ and sku_unique, customers has _id_, "
               "customerNumber_unique and email_unique, orders has _id_ and orderNumber_unique, "
               "and reviews has only _id_."),
            tp("A common surprise",
               "Learners often expect each collection to show only the default _id_ index. "
               "On a fresh load that isn't true: load.js also builds the four unique indexes "
               "listed here, and Lab 5, Step 6 asks learners to list them."),
        ],
    },
    14: {
        "talking_points": [
            tp("Hide instead of drop",
               "db.products.hideIndex(name) keeps the index on disk and up to date, but the "
               "query planner stops choosing it. "
               "Run the important queries and their explain() while it is hidden."),
            tp("Undo in an instant",
               "unhideIndex(name) makes it available again immediately. "
               "Dropping and recreating would mean a full index rebuild."),
            tp("Hidden still costs",
               "A hidden index is still maintained on every write and still takes storage. "
               "A hidden unique index still rejects duplicates."),
            tp("In Lab 5, Step 13",
               "Learners hide a non-unique helper index, idx_products_category_active_price, "
               "explain db.products.find({ category: \"ACCESSORY\" }) with queryPlanner, then "
               "unhide it. "
               "They never hide _id_ or a unique rule, and never drop in the lab."),
        ],
    },
    17: {
        "talking_points": [
            tp("Several fields, one index",
               "A compound index is sorted by its first field, then by the second field within "
               "each value of the first, and so on."),
            tp("Filter and sort together",
               "Because price is already in order inside each category, a query for one "
               "category sorted by price reads one run of keys and needs no SORT stage."),
            tp("Directions",
               "category: 1 is ascending and price: -1 descending. "
               "Direction matters when the index must serve a sort on more than one field."),
            tp("On training_store",
               "The course's catalog index is { category: 1, price: 1 }, named "
               "idx_products_category_price. "
               "It serves db.products.find({ category: \"SHOE\" }).sort({ price: 1 }): Clearance "
               "Shoe 44.99, Trail Shoe 89.99, Running Shoe 129.99."),
        ],
    },
    18: {
        "talking_points": [
            tp("Order is part of the design",
               "{ category: 1, price: 1 } and { price: 1, category: 1 } contain the same fields "
               "but are different indexes with different key orders."),
            tp("Which queries each serves",
               "Category first serves category equality, and category with a price range or "
               "sort. "
               "Price first serves price ranges and price sorts across all categories."),
            tp("How to choose",
               "Look at the queries the application actually runs. "
               "Our catalog always filters by category, so category goes first."),
        ],
    },
    19: {
        "talking_points": [
            tp("Leading fields",
               "A compound index can serve queries on any prefix of its fields, read from the "
               "left. "
               "For three fields that is the first; the first two; and all three."),
            tp("Not a prefix",
               "A query on the second field alone skips the first, so the matching keys are "
               "scattered through the index."),
            tp("Prefixes make indexes redundant",
               "If { customerId: 1, paymentStatus: 1, createdAt: -1 } exists, a separate "
               "{ customerId: 1 } index is usually redundant, because customerId is a prefix. "
               "Check uniqueness, partial filters and collation before removing anything."),
            tp("Skipping a middle field",
               "Filtering customerId and sorting createdAt without paymentStatus skips the middle "
               "field, so the index can't supply the sort and a SORT stage is likely."),
        ],
    },
    20: {
        "talking_points": [
            tp("Equality first",
               "Exact-match fields go first. "
               "They cut the index down to one contiguous block of keys."),
            tp("Then sort",
               "The sort field comes next, in the sort direction, so the keys inside that block "
               "are already in the order the query wants."),
            tp("Range last",
               "Range conditions such as $gte go last. "
               "A range placed before the sort field would break the sort order and force a "
               "SORT stage."),
            tp("A guideline, not a law",
               "On training_store: for one customer's PAID orders over a minimum total, "
               "customerId and paymentStatus are equality, createdAt is the sort, total is the "
               "range. "
               "Selectivity and real explain() results make the final call."),
        ],
    },
    24: {
        "talking_points": [
            tp("One key per value",
               "tags is an array. "
               "When you index it, MongoDB adds one index key for each value in each document's "
               "array, and marks the index multikey: true automatically."),
            tp("Read the index",
               "The Wireless Keyboard, P1001, contributes two keys, wireless and accessories. "
               "The keys are sorted, so all the wireless keys sit together. "
               "Across the 13 products the index holds 26 keys."),
            tp("The query",
               "db.products.find({ tags: \"wireless\" }) walks the two wireless keys and "
               "returns P1001 and A410: 2 keys examined, 2 documents examined. "
               "This is Lab 5, Step 5, with idx_products_tags."),
            tp("Arrays of documents and limits",
               "An index on items.productId lets you find every order that contains one "
               "product. "
               "Large arrays mean large indexes, and a compound index can't have two array "
               "fields in the same document."),
            tp("One more tag",
               "Step 5 also queries tags technology: only B300, MongoDB Fundamentals, carries "
               "that tag, so it returns one book.")],
    },
    28: {
        "talking_points": [
            tp("Only documents with the field",
               "A sparse index skips documents that don't have the indexed field. "
               "It is smaller than a normal index on an optional field."),
            tp("Null is not missing",
               "In training_store, Luis Romero, C204, has contact.phone set to null. "
               "The field exists, so a sparse index includes him. "
               "Sam Okonkwo, C515, has no phone field at all, so he is left out: 5 of the 6 "
               "customers are indexed."),
            tp("Careful with queries",
               "Because some documents are missing from it, MongoDB won't use a sparse index for "
               "a query or sort that must see every document, unless you hint it."),
            tp("Prefer partial",
               "A partial index with partialFilterExpression { \"contact.phone\": { $exists: "
               "true } } says the same thing more explicitly, and partial indexes can use any "
               "filter."),
        ],
    },
    31: {
        "talking_points": [
            tp("Text",
               "A text index supports word search with $text and a relevance score. "
               "In training_store we would index name, since products have no description. "
               "For autocomplete, fuzzy matching or synonyms, use a dedicated search product."),
            tp("Wildcard",
               "{ \"attributes.$**\": 1 } indexes every path under attributes. "
               "Our laptops have processor and memoryGB, shoes have color and material, books "
               "have author and isbn, so the paths vary. "
               "It supports queries such as { \"attributes.connection\": \"Bluetooth\" }."),
            tp("Geospatial",
               "A 2dsphere index supports $near and containment queries on GeoJSON points, "
               "stored longitude first. "
               "A store-locator collection would use it."),
            tp("Hashed",
               "A hashed index stores a hash of the value. "
               "It supports equality only, not ranges or sorts, and exists mainly for hashed "
               "sharding, which Module 7 covers."),
        ],
    },
    36: {
        "talking_points": [
            tp("No document read",
               "When the filter and every returned field are in one index, MongoDB answers from "
               "the index keys alone and skips the FETCH."),
            tp("Three conditions",
               "The filter fields are indexed. "
               "The returned fields are indexed. "
               "And _id is excluded, or is itself part of the index."),
            tp("Why _id matters",
               "_id is returned by default. "
               "If it isn't in the index, MongoDB must fetch the document just to read it, and "
               "the query is no longer covered."),
            tp("Field order in the diagram",
               "The diagram's index is { category: 1, name: 1, price: 1 }; Lab 5, Step 11 uses "
               "{ category: 1, price: 1, name: 1 }. "
               "Both cover this query: coverage needs the fields to be present, not in a "
               "particular order."),
        ],
    },
    37: {
        "talking_points": [
            tp("Selective means narrow",
               "A selective condition matches a small share of the collection. "
               "sku is perfectly selective: 13 products, 13 distinct values."),
            tp("Low selectivity",
               "active has two values, and 12 of our 13 products are true. "
               "An index on active alone barely narrows the search."),
            tp("Use it inside something bigger",
               "Put a low-selectivity field inside a compound index, as in "
               "{ category: 1, active: 1, price: 1 }, or use it as a partial filter."),
            tp("Measure it",
               "Selectivity is a property of your data, not of the field name. "
               "Check it with counts and explain()."),
        ],
    },
    44: {
        "talking_points": [
            tp("queryPlanner",
               "The default mode. "
               "It shows the chosen plan without running the query, which is safe on a busy "
               "system."),
            tp("executionStats",
               "Runs the winning plan and reports nReturned, totalKeysExamined, "
               "totalDocsExamined and executionTimeMillis. "
               "This is the mode for tuning, and the one every Lab 5 step uses."),
            tp("allPlansExecution",
               "Also reports the candidate plans the planner tried during plan selection and why "
               "they lost. "
               "Use it when the planner picks an index you didn't expect."),
            tp("Two ways to write it",
               "db.products.find(filter).explain(\"executionStats\") or "
               "db.products.explain(\"executionStats\").find(filter). "
               "The second form also works for aggregate, as in Lab 5, Step 12."),
        ],
    },
    48: {
        "talking_points": [
            tp("What SORT means",
               "A SORT stage in the winning plan means no index supplied the order, so MongoDB "
               "collected the matching documents and sorted them in memory."),
            tp("Why it hurts",
               "It is blocking: nothing is returned until every matching document has been read "
               "and sorted. "
               "Big sorts use up to 100 MB of memory and then spill to disk."),
            tp("The fix",
               "An index whose order matches the sort, after any equality fields. "
               "Our order-history index removed SORT for exactly this reason."),
            tp("On training_store",
               "Before the catalog index, active accessories sorted by price show SORT above "
               "COLLSCAN. "
               "After { category: 1, active: 1, price: 1 }, the SORT stage is gone."),
        ],
    },
    50: {
        "talking_points": [
            tp("Usage counters",
               "$indexStats returns one document per index with accesses.ops, the number of "
               "times the planner used it, and accesses.since, when counting started."),
            tp("Read with care",
               "The counters reset when mongod restarts and are per server. "
               "On a replica set, check every member before deciding an index is unused."),
            tp("In the lab",
               "Lab 5, Step 13 runs $indexStats on products and expects low or zero counts for "
               "some indexes, because the classroom server hasn't been running long."),
        ],
    },
    54: {
        "talking_points": [
            tp("Writes pay for reads",
               "Every insert updates the collection and every index on it. "
               "Every update to an indexed field rewrites that field's index keys. "
               "Every delete removes keys from every index."),
            tp("On training_store",
               "A new order already updates _id_ and orderNumber_unique. "
               "After Lab 5 it also updates idx_orders_customer_date and "
               "idx_orders_fulfillment_date."),
            tp("Storage and memory",
               "Indexes take disk space and compete with the documents for the storage "
               "engine's cache in RAM. "
               "Indexes that fit in memory are fast; ones that don't cause disk reads."),
            tp("Operational cost",
               "More indexes mean longer builds, more monitoring, more plan choices, and more "
               "data to back up and replicate."),
        ],
    },
    57: {
        "talking_points": [
            tp("Treat it as a change",
               "Adding or removing an index changes performance for every query on that "
               "collection. "
               "Plan it like a code release."),
            tp("Before and after",
               "Capture the explain() baseline and $indexStats first. "
               "Build on staging with production-like data. "
               "Watch CPU, I/O and latency after the production build."),
            tp("Rollback",
               "Keep both commands ready. "
               "For a new index, rollback is dropIndex by name; for a removal, hide first, and "
               "keep the original createIndex so it can be rebuilt."),
        ],
        "use_case_scenario":
            "A team adds { category: 1, price: 1 } to speed up the catalog page. "
            "They test it on staging, build it in the evening change window, and watch the "
            "dashboards for an hour. "
            "Catalog latency drops and write latency is unchanged, so they keep it.",
    },
    59: {
        "talking_points": [
            tp("Too many indexes",
               "One index per field, just in case, slows every write and fills memory. "
               "Index recurring query shapes instead."),
            tp("Wrong order",
               "{ createdAt: 1, status: 1 } puts the range and sort field first. "
               "For status equality with a date sort, equality must lead."),
            tp("Unused indexes",
               "An index nobody uses is pure cost. "
               "Find it with $indexStats, hide it, measure, then drop it."),
            tp("Three more",
               "Using hint() as a permanent fix locks in a plan that ages badly. "
               "Judging by time alone on tiny data proves nothing. "
               "And an IXSCAN that examines 50,000 keys for 10 results is not efficient."),
        ],
    },
    61: {
        "talking_points": [
            tp("Start from the pages",
               "The catalog page filters by category and sorts by price. "
               "The login looks a customer up by email. "
               "The account page lists orders newest first. "
               "The product page shows reviews."),
            tp("The indexes",
               "products { category: 1, price: 1 }, customers unique contact.email, orders "
               "{ customerId: 1, createdAt: -1 } and reviews { productId: 1, rating: -1 }."),
            tp("Two review indexes",
               "The diagram sorts a product's reviews by rating, for top-rated first. "
               "The content source also recommends { productId: 1, createdAt: -1 }, named "
               "idx_reviews_product_date, for newest first. "
               "Build the one the product page actually uses."),
            tp("Keep the integrity rules",
               "The unique indexes on sku, customerNumber, orderNumber and email stay whatever "
               "else changes."),
        ],
    },
    62: {
        "talking_points": [
            tp("The workflow",
               "Query patterns first: what does the application filter and sort on? "
               "Then choose the index: single, compound or unique."),
            tp("Prove it",
               "Validate the plan with explain(): IXSCAN, keys and documents close to returned, "
               "no SORT."),
            tp("Keep it healthy",
               "Monitor usage with $indexStats, then tune: keep, reorder or remove. "
               "The outcome is fast reads with controlled writes."),
        ],
    },
}

#!/usr/bin/env python3
"""Speaker notes for the new Module 3 deck (Data Modeling with MongoDB).

Written from scripts/module03_content_source.md, the Module 3 manifest, the
official Exercises 3.1-3.9 and Day 1 Lab 2 (Steps 1-7), and the training_store dataset
(datasets/training_store/load.js), in plain short sentences. Composed into the
notes pane by mdb_speaker_notes.compose(), so the layout matches the other decks:
KEY TALKING POINTS / REAL-WORLD EXAMPLES / USE-CASE SCENARIO.

Keys are topic numbers. Diagram topics (see build_module03_new.DIAGRAMS) are
merged with the diagram's own "what it shows" notes on the same slide.
"""
from __future__ import annotations


def tp(point: str, explain: str) -> dict:
    return {"point": point, "explain": explain}


NOTES: dict[int, dict] = {
    1: {
        "talking_points": [
            tp("Design before you insert",
               "Module 2 gave everyone a running MongoDB and a first collection. "
               "Module 3 is about deciding what the documents should look like before we "
               "insert many more of them."),
            tp("The central principle",
               "Data that is accessed together should usually be stored together. "
               "Every decision in this module comes back to that sentence."),
            tp("What this module does",
               "We look inside documents and BSON types, discover access patterns, choose "
               "between embedding and referencing, learn the common patterns and "
               "anti-patterns, and finish with validation and the training_store labs."),
            tp("End of Day 1",
               "This is the last module of Day 1. "
               "Tomorrow, Module 4 queries the database we model and populate today."),
        ],
        "real_world_examples": [
            "Most slow MongoDB applications are not slow because of the server. "
            "They are slow because the documents were shaped like relational tables, so every "
            "page needs several queries.",
        ],
    },
    2: {
        "talking_points": [
            tp("By the end of this module",
               "Walk through the seven objectives on the left. "
               "Learners should be able to read a document's structure, pick the right BSON "
               "type for each value, and list the application's access patterns. "
               "They should be able to model relationships by embedding or referencing, keep "
               "arrays bounded, apply a schema pattern and a validation rule, and build and "
               "query training_store."),
            tp("Six questions this module answers",
               "What is inside a document? "
               "Which type fits each value? "
               "How does the application use the data? "
               "When do we embed, and when do we reference? "
               "Which patterns and pitfalls matter? "
               "And how do we enforce the model and build it?"),
            tp("Set the expectation",
               "There is rarely one correct schema. "
               "There is a schema that fits the access patterns, and we must be able to "
               "justify it. "
               "The roadmap at the bottom shows the path through the five parts."),
        ],
    },
    3: {
        "talking_points": [
            tp("Nested documents",
               "A field's value can be a whole document. "
               "In training_store, a product's attributes and a customer's name and contact "
               "are embedded documents."),
            tp("Arrays",
               "An array holds several values in one field. "
               "It can hold simple values, like a product's tags, or whole documents, like an "
               "order's line items or a customer's addresses."),
            tp("Dot notation",
               "Queries reach inside with dot notation, in quotes: \"attributes.memoryGB\" or "
               "\"items.sku\". "
               "When the path crosses an array, MongoDB checks every element. "
               "Lab 2, Step 5, practises this, and Module 4 goes deeper."),
        ],
    },
    4: {
        "talking_points": [
            tp("Types carry meaning",
               "Choose the type that matches the business meaning. "
               "A price is money, a quantity is a whole number, a flag is a Boolean and a "
               "timestamp is a date."),
            tp("What goes wrong",
               "Strings compare character by character. "
               "Sorted as strings, \"100\" comes before \"20\" and \"9\". "
               "Range filters such as price below 50 also stop working, and calculations need "
               "conversions first."),
            tp("Money",
               "For currency, Decimal128 is usually better than a Double, because it avoids "
               "binary floating-point rounding. "
               "In mongosh you can write Decimal128(\"49.99\") or NumberDecimal(\"49.99\"); "
               "both create the same type."),
        ],
    },
    5: {
        "talking_points": [
            tp("One collection, many shapes",
               "All products live in one products collection, even though a laptop, a shoe "
               "and a book have different specifications."),
            tp("The shared core",
               "Every product has the same core fields with the same names and types: sku, "
               "name, category, price, tags, active and createdAt. "
               "Common operations such as browsing by category or price rely on them."),
            tp("Flexible attributes",
               "Category-specific fields go under attributes: processor and memoryGB for a "
               "laptop, sizes, color and material for a shoe, author and isbn for a book."),
            tp("Consistent names",
               "Avoid productName on one document, item_name on another and title on a third. "
               "Pick one name, name, and use it everywhere."),
        ],
    },
    6: {
        "talking_points": [
            tp("Start from the application",
               "Relational design often starts with entities and normalization. "
               "MongoDB design starts with the application's most important operations."),
            tp("The questions to ask",
               "What is read together? What is updated together? Which queries run most "
               "often? How large can each record become? "
               "Which relationships are one-to-one, one-to-many or many-to-many?"),
            tp("From question to design",
               "The answers decide the aggregate boundary: what belongs in one document. "
               "Then we choose embed or reference for each relationship, and finally the "
               "indexes that support the queries."),
        ],
    },
    7: {
        "talking_points": [
            tp("Three relationship types",
               "One-to-one: a customer has one set of preferences. "
               "One-to-many: a customer places many orders. "
               "Many-to-many: an order contains many products, and a product appears in many "
               "orders."),
            tp("In training_store",
               "Customer to preferences is embedded. "
               "Customer to orders is a reference: each order stores customerId. "
               "Orders to products is also a reference, through items[].productId."),
            tp("Count both sides",
               "The type alone doesn't decide the model. "
               "How many on the many side matters: a few addresses, dozens of orders or "
               "millions of reviews lead to different choices."),
        ],
    },
    8: {
        "talking_points": [
            tp("Estimate growth",
               "For every array ask: how many items can it hold, does it grow without a "
               "practical limit, and how often does it change?"),
            tp("Bounded",
               "A customer has a few addresses. An order has a handful of line items. "
               "These arrays stay small, so they can be embedded."),
            tp("Unbounded",
               "A popular product can receive thousands of reviews. "
               "An array like that keeps growing, every update rewrites a larger document, "
               "and it can eventually hit the 16 MiB limit for one BSON document."),
            tp("Rule",
               "A small, bounded list may be embedded. "
               "A large or continuously growing list belongs in its own collection."),
        ],
    },
    9: {
        "talking_points": [
            tp("Why addresses are embedded",
               "Addresses belong to the customer, a customer has only a few, they are "
               "displayed with the profile, and an address doesn't need to exist on its own."),
            tp("Advantages of embedding",
               "One query returns the whole profile. "
               "There is no join. "
               "Updates inside one document are atomic, and the document matches the "
               "application object."),
            tp("Limitations",
               "Embedding can duplicate shared information and make documents large. "
               "It is wrong for unbounded arrays, and it makes independent updates of the "
               "embedded data less convenient."),
        ],
    },
    10: {
        "talking_points": [
            tp("Referencing",
               "Referencing keeps related data in separate collections and connects documents "
               "with identifiers. "
               "Each review stores the productId of the product it belongs to, and the "
               "customerId of the person who wrote it."),
            tp("Advantages of referencing",
               "It avoids large-scale duplication, lets data change independently, works for "
               "many-to-many relationships, handles large and growing relationships, and keeps "
               "each document small."),
            tp("Limitations",
               "Combining the data needs a second query or a $lookup stage. "
               "Application logic is more complex, and a change that spans several documents "
               "may need a transaction."),
        ],
    },
    11: {
        "talking_points": [
            tp("Three questions",
               "Is the data read together with the parent? "
               "Is its size bounded? "
               "Does it share the parent's lifecycle, created and deleted with it?"),
            tp("All three yes",
               "Embed it. "
               "Addresses on a customer and line items on an order pass all three."),
            tp("Any no",
               "Reference it. "
               "Reviews are read on the product page, but they are not bounded and they have "
               "their own lifecycle. "
               "So training_store keeps them in their own collection."),
        ],
    },
    12: {
        "talking_points": [
            tp("Orders mix both approaches",
               "An order is the clearest example of a hybrid model. "
               "It references the customer and each product, and it embeds the line items and "
               "the shipping address."),
            tp("Copied fields",
               "Each line item also copies sku, name and unitPrice from the product. "
               "The productId still points to the catalog, but the copies keep what the "
               "customer actually bought."),
            tp("Why this shape",
               "The most common read is: show one order. "
               "This shape answers it with one document, while customers and products keep "
               "changing independently."),
        ],
    },
    13: {
        "talking_points": [
            tp("Why copy product information",
               "A product's name or price can change later. "
               "An order must keep the values that applied when the purchase happened."),
            tp("Controlled duplication",
               "If the catalog price changes, the historical order still shows the old price. "
               "This deliberate copy is called a snapshot, or the historical pattern."),
            tp("Snapshot versus live copy",
               "Don't copy data that must stay current, such as a customer's email, into "
               "thousands of documents. "
               "Duplicate only the fields that should stay frozen as history."),
        ],
    },
    14: {
        "talking_points": [
            tp("Collections like tables",
               "The most common first-design mistake is one collection for every relational "
               "table. "
               "The application then rebuilds each object with several queries or $lookup "
               "stages."),
            tp("The cost",
               "More round trips, more code and slower pages, for data that is always read "
               "together anyway."),
            tp("The fix",
               "Start again from the access pattern. "
               "Embed what the page reads together, and reference only what is shared, "
               "independent or unbounded."),
        ],
    },
    15: {
        "talking_points": [
            tp("Inconsistent names",
               "When one document says customerId, another customer_id and a third custId, a "
               "query on one name silently misses the others."),
            tp("Inconsistent types",
               "The same happens with types: price as 29.99, as \"29.99\" and as "
               "{ amount: 29.99 } in one collection breaks sorting, filtering and "
               "calculations."),
            tp("The fix",
               "Choose one name and one structure for each field, apply it everywhere, and "
               "enforce it with validation. "
               "training_store uses camelCase names such as customerId and createdAt "
               "throughout."),
        ],
    },
    16: {
        "talking_points": [
            tp("The problem",
               "Products have many optional attributes. "
               "Searching on each one would need its own index."),
            tp("The pattern",
               "The Attribute pattern stores them as an array of key-value pairs, "
               "{ k, v }. "
               "One compound index on attributes.k and attributes.v then serves every "
               "attribute search."),
            tp("training_store today",
               "Our attributes field is a plain embedded object, which is simpler and fine "
               "while queries use a few known fields. "
               "Switch to the pattern when attribute searches multiply."),
        ],
    },
    17: {
        "talking_points": [
            tp("The problem",
               "A product page shows a few recent reviews, but the product may have hundreds."),
            tp("The pattern",
               "The Subset pattern embeds only the hot part, such as the three most recent "
               "reviews, and keeps the complete history in the reviews collection."),
            tp("Trade-off",
               "The page loads in one read, but a new review is written in two places: the "
               "reviews collection and the product's small subset."),
        ],
    },
    18: {
        "talking_points": [
            tp("The problem",
               "Calculating the average rating from every review on every page view repeats "
               "the same work."),
            tp("The pattern",
               "The Computed pattern calculates once and stores the result, such as "
               "ratingAvg and reviewCount on the product."),
            tp("Trade-off",
               "Reads become fast, but the stored value must be recomputed when a review is "
               "added, either at write time or on a schedule."),
        ],
    },
    19: {
        "talking_points": [
            tp("Flexible, not unplanned",
               "MongoDB doesn't force one shape, but a collection can enforce rules with a "
               "validator. "
               "The $jsonSchema operator is the usual way."),
            tp("The three building blocks",
               "required lists the fields every document must have. "
               "properties gives each field a bsonType. "
               "Keywords such as minimum add range rules."),
            tp("When it runs",
               "The validator checks inserts and updates. "
               "A valid document is stored; an invalid one is rejected with an error that "
               "names the failing rule."),
        ],
    },
    20: {
        "talking_points": [
            tp("validationLevel",
               "strict, the default, checks every insert and every update. "
               "moderate checks inserts and updates to documents that are already valid, and "
               "leaves existing invalid documents alone."),
            tp("validationAction",
               "error, the default, rejects an invalid write. "
               "warn stores the write and records a warning in the log."),
            tp("When to relax",
               "Use moderate and warn when you add rules to a collection that already holds "
               "old documents. "
               "Fix the old data, then switch back to strict and error."),
        ],
    },
    21: {
        "talking_points": [
            tp("Schemas change",
               "Requirements change, so document shapes change. "
               "A new optional field is non-breaking. "
               "Renaming or restructuring a field is breaking for old readers and writers."),
            tp("Version the shape",
               "A schemaVersion field records which shape each document has. "
               "The application reads both versions and normalizes them to one model."),
            tp("Migrate safely",
               "Deploy readers that tolerate both shapes first. "
               "Then write the new shape, backfill old documents in small batches, and only "
               "then tighten validation to require it."),
        ],
    },
    22: {
        "talking_points": [
            tp("Access patterns",
               "Start from what the application does: browse, order, review."),
            tp("Relationships and shape",
               "Embed bounded data that belongs to the parent; reference independent, shared "
               "or unbounded data."),
            tp("Patterns and guardrails",
               "Schema patterns solve recurring problems. "
               "Validation, the 16 MiB limit and bounded arrays keep the model healthy."),
            tp("The result",
               "training_store: products, customers, orders and reviews, ready for Day 2."),
        ],
    },
}

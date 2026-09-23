#!/usr/bin/env python3
"""Speaker notes for the new Module 4 deck (The MongoDB Query Language).

Written from scripts/module04_content_source.md, the Module 4 manifest, the
official exercises, Day 2 Lab 3 and the training_store dataset, in plain short
sentences. Every result quoted is the result on a fresh load of
datasets/training_store/load.js. Composed into the notes pane by
mdb_speaker_notes.compose(), so the layout matches the day decks:
KEY TALKING POINTS / REAL-WORLD EXAMPLES / USE-CASE SCENARIO.

Keys are topic numbers. Diagram topics (see build_module04_new.DIAGRAMS) are
merged with the diagram's own "what it shows" notes on the same slide.
"""
from __future__ import annotations


def tp(point: str, explain: str) -> dict:
    return {"point": point, "explain": explain}


# Said once per diagram slide: the pictures use small sample documents.
def _sample(detail: str) -> dict:
    return tp("Diagram data versus our data",
              "The diagram uses simplified sample documents, not training_store. " + detail)


NOTES: dict[int, dict] = {
    1: {
        "talking_points": [
            tp("What MQL is",
               "The MongoDB Query Language, MQL, is how we read, filter, shape, insert, "
               "update and delete documents. Its filters are themselves documents, shaped "
               "like the data they match."),
            tp("What this module does",
               "Five parts: reading documents, query operators, nested fields and arrays, "
               "inserts and updates, and finally deletes, bulk writes and safe practice. "
               "Everything runs on training_store."),
            tp("Where it sits",
               "Module 4 opens Day 2, right after Module 3 designed the documents. Module 5, "
               "aggregation, reuses today's filters and projections as pipeline stages."),
        ],
        "real_world_examples": [
            "An online store's product page is a findOne by SKU, its category page is a "
            "filtered, sorted and paged find, and checkout is a guarded update of stock. "
            "This module covers all three.",
        ],
    },
    2: {
        "talking_points": [
            tp("By the end of this module",
               "Walk through the six objectives on the left. Learners should be able to read "
               "documents with find() and findOne(), shape results with projection, sort, "
               "paging and counts, combine operators, query nested fields and arrays, "
               "insert, update, upsert and replace documents, and delete safely while "
               "reading every write result."),
            tp("Six questions this module answers",
               "Which documents does my filter match? What fields should come back? How do "
               "operators combine? When is $elemMatch required? How do I change only what I "
               "mean? And how do I prove a write was right?"),
            tp("Set the expectation",
               "Precision is the skill: the right field name, the right case, the right BSON "
               "type. The roadmap at the bottom shows the path through the module."),
        ],
    },
    50: {
        "talking_points": [
            tp("Demo 4.2",
               "Start with an empty filter and add one condition at a time. Run "
               "countDocuments() after each step and explain the number before moving on."),
            tp("The counts",
               "{} counts 13. category ACCESSORY leaves 5: P1001, A400, A410, A500 and XBAD. "
               "Adding active: true keeps all 5, because every accessory is active. Adding "
               "price $lte Decimal128 100.00 leaves 3: P1001, A400 and A410."),
            tp("The two drops",
               "A500, the Docking Station, costs 249.99, so the price rule removes it. XBAD "
               "is removed for a different reason: its price is the string \"49.99\", and a "
               "Decimal128 comparison never matches a string."),
            tp("Why it matters",
               "If one step drops to zero or drops the wrong documents, you know exactly "
               "which condition to check. Usually it's a field name, a case or a type."),
        ],
    },
    7: {
        "talking_points": [
            tp("A filter is a document",
               "Each field-value pair in the filter is a condition, and a document matches "
               "only when every condition is true. That is an implicit AND."),
            tp("Exact and case-sensitive",
               "Equality is exact. category \"LAPTOP\" matches three products: L100, L110 "
               "and L190. \"Laptop\" matches none, because the stored values are uppercase. "
               "Field names are case-sensitive too."),
            tp("On training_store",
               "BOOK with price below Decimal128 50.00 returns only Query Cookbook at 39.99. "
               "MongoDB Fundamentals at 59.99 fails the price condition."),
            _sample("Its categories, Training, Office and Books, are illustrations; ours are "
                    "LAPTOP, SHOE, BOOK and ACCESSORY."),
        ],
    },
    8: {
        "talking_points": [
            tp("findOne()",
               "findOne() returns a single document, or null when nothing matches. Use it "
               "with a unique field: findOne({ sku: \"L100\" }) returns the Business Laptop, "
               "and the sku_unique index guarantees there is only one."),
            tp("find()",
               "find() returns a cursor, not an array. mongosh prints the first 20 documents "
               "and you type it to see more. An application driver fetches the rest in "
               "batches as it iterates."),
            tp("Look before you assume",
               "findOne({ orderNumber: \"O5001\" }) does not return an embedded customer "
               "object. In training_store, O5001 has a customerId reference, an embedded "
               "shippingAddress and an items array."),
            _sample("It uses category \"Laptop\" and products such as ProBook; in "
                    "training_store the value is \"LAPTOP\"."),
        ],
    },
    48: {
        "talking_points": [
            tp("Four questions",
               "Every read answers four questions: which documents, which fields, in which "
               "order, and how many. Filter, projection, sort and limit."),
            tp("On training_store",
               "find({ category: \"BOOK\" }, { _id: 0, name: 1, price: 1 }).sort({ price: 1 "
               "}).limit(10) returns Query Cookbook at 39.99, then MongoDB Fundamentals at "
               "59.99. There are only two books, so the limit is not reached."),
            tp("The order MongoDB applies",
               "However you chain them, the server sorts first, then skips, then limits. "
               "Writing limit before sort does not change the result."),
            _sample("Its books, such as Clean Code, are not in our catalog."),
        ],
        "real_world_examples": [
            "A category page on a shopping site is exactly this query: one category, the "
            "fields the card shows, sorted by price, twenty per page.",
        ],
    },
    23: {
        "talking_points": [
            tp("Inclusion",
               "{ name: 1, price: 1 } returns name, price and _id. _id is always included "
               "unless you add _id: 0."),
            tp("Exclusion",
               "{ attributes: 0, tags: 0 } returns every other field. Try it on L100."),
            tp("The mixing rule",
               "{ name: 1, tags: 0 } is an error. You choose inclusion or exclusion; _id is "
               "the only field that may be excluded in an inclusion projection."),
            tp("Nested paths",
               "find({ customerNumber: \"C101\" }, { _id: 0, \"name.first\": 1 }) returns "
               "{ name: { first: \"Aisha\" } }. The nested shape is kept."),
            tp("Also available",
               "items: { $elemMatch: { sku: \"L100\" } } in a projection returns only the "
               "matching line item, and $slice returns part of an array."),
            _sample("Its Courses product with stock and internalCost is an illustration."),
        ],
    },
    26: {
        "talking_points": [
            tp("sort()",
               "1 is ascending and -1 descending. Several keys sort in order. Add _id as a "
               "last key so documents with the same price always come back in the same "
               "order."),
            tp("Paging",
               "skip is (page − 1) × pageSize and limit is the page size. For page 2 of five "
               "active products sorted by price and _id, skip(5).limit(5) returns B300, "
               "S210, S200, A500 and L100."),
            tp("Mixed types",
               "Page 3 returns L110 and then XBAD. MongoDB sorts by BSON type first, and "
               "numbers come before strings, so XBAD's string price sorts after every "
               "Decimal128."),
            tp("At scale",
               "skip() still walks past the skipped documents, so deep pages get slower. "
               "A range filter on an indexed sort key scales better; Module 6 covers "
               "indexes."),
            _sample("Its eight Courses products are illustrations."),
        ],
    },
    12: {
        "talking_points": [
            tp("Operator placement",
               "Comparison operators sit inside the field they test: { price: { $gt: … } }. "
               "{ $gt: { price: … } } is an error — one of the classic mistakes gathered "
               "near the end of the module."),
            tp("Decimal128",
               "training_store stores money as Decimal128. Compare with Decimal128(\"100.00\") "
               "or NumberDecimal(\"100.00\"). A string such as \"100.00\" never matches a "
               "number."),
            tp("A range",
               "$gte 50.00 and $lte 500.00 on price returns L190 at 499.99, S200 at 129.99, "
               "S210 at 89.99, B300 at 59.99 and A500 at 249.99. Both ends are inclusive."),
            tp("Dates compare too",
               "The same operators work on Date fields such as createdAt, as a later slide "
               "shows."),
            _sample("Its prices, such as DataPad at 699, are illustrations."),
        ],
    },
    14: {
        "talking_points": [
            tp("Implicit AND",
               "Commas already mean AND: { active: true, category: \"BOOK\" }. Most filters "
               "need nothing more."),
            tp("Explicit $and",
               "Use $and when the same field or operator must appear twice, for example two "
               "separate $or clauses. For a simple range, one field with $gte and $lte is "
               "shorter."),
            tp("$or on training_store",
               "PENDING payment or PROCESSING fulfilment returns five orders: O5001, O6202, "
               "O6302, O6401 and O6499. O6401 matches both conditions and appears once."),
            tp("Don't miss two orders",
               "O6202 and O6302 are PAID but still PROCESSING, so the $or includes them "
               "alongside O5001, O6401 and O6499. Active laptops or books returns L100, L110, "
               "B300 and B310. When the alternatives share one field, $in is shorter than "
               "$or."),
            _sample("Its AirLite, ProBook and DataPad products are illustrations."),
        ],
    },
    16: {
        "talking_points": [
            tp("$not",
               "$not wraps another operator expression for one field. "
               "{ price: { $not: { $gt: Decimal128(\"100.00\") } } } returns 8 products: the "
               "seven priced at 100 or less, plus XBAD, whose string price cannot be greater "
               "than a number."),
            tp("$nor",
               "$nor keeps documents that fail every listed condition. $nor: "
               "[{ category: \"BOOK\" }, { active: false }] removes the two books and L190, "
               "leaving 10 of 13."),
            tp("Missing fields",
               "Negations also keep documents without the field. Add $exists: true when the "
               "field must be present."),
            tp("Prefer $ne",
               "For a simple not-equal, { category: { $ne: \"BOOK\" } } is clearer than $not."),
            _sample("Its Books category and stock field are illustrations; our products have "
                    "no stock field."),
        ],
    },
    17: {
        "talking_points": [
            tp("Null or missing",
               "{ \"contact.phone\": null } matches C204, whose phone is null, and C515, who "
               "has no phone field at all."),
            tp("Only explicit null",
               "{ \"contact.phone\": { $type: \"null\" } } matches C204 only."),
            tp("Only missing",
               "{ \"contact.phone\": { $exists: false } } matches C515 only. Every other "
               "customer has a string phone."),
            tp("Wrong type",
               "{ price: { $type: \"string\" } } finds XBAD, the planted type error. "
               "$type: \"decimal\" matches the other 12 products."),
            _sample("Its BK-101 product with a discount and a supplier is an illustration."),
        ],
    },
    11: {
        "talking_points": [
            tp("Quote the path",
               "Dot notation must be quoted in mongosh: \"attributes.memoryGB\". Without "
               "quotes it is a JavaScript syntax error, one of the classic query bugs."),
            tp("Embedded documents",
               "{ \"attributes.memoryGB\": { $gte: 16 } } returns L100 with 16 GB and L110 "
               "with 32 GB. L190 has 8 GB."),
            tp("Arrays of documents",
               "customers keep addresses as an array. \"addresses.city\" checks every address "
               "in the array. $in Toronto and Montreal returns C101, Aisha Khan, and C412, "
               "Jordan Lee."),
            _sample("It stores one address object; ours is an addresses array, and nobody in "
                    "training_store lives in Brampton."),
        ],
    },
    20: {
        "talking_points": [
            tp("Contains",
               "{ tags: \"wireless\" } matches any document whose tags array contains that "
               "value: P1001 and A410."),
            tp("Exact array",
               "{ tags: [\"database\", \"technology\"] } matches B300. The same two values in "
               "the other order match nothing."),
            tp("$all",
               "{ tags: { $all: [\"office\", \"premium\"] } } returns A500 in any order. "
               "$all with database and technology returns B300."),
            tp("$size",
               "$size matches an exact length. $size: 3 returns L190; $size: 2 returns 11 of "
               "the 13 products. There is no \"at least\" form."),
            _sample("Its MongoDB Masterclass product and tags are illustrations."),
        ],
    },
    22: {
        "talking_points": [
            tp("The trap",
               "With dot notation, \"items.sku\": \"L100\" and \"items.quantity\": "
               "{ $gte: 2 } can be satisfied by different items. O5001 has L100 quantity 1 "
               "and A410 quantity 2, so it matches."),
            tp("The fix",
               "$elemMatch requires one element to pass both conditions. It returns only "
               "O6401, Luis Romero's order for two laptops."),
            tp("Lab 3, step 6",
               "$elemMatch with quantity $gte 2 and unitPrice below 50 returns O5001, O6201 "
               "and O6305. O6302 and O6401 have quantity 2, but of expensive items, so they "
               "don't match."),
            _sample("Its orderId, product and qty fields are illustrations; ours are "
                    "orderNumber, sku and quantity."),
        ],
        "use_case_scenario":
            "A support agent searches for orders where a customer bought at least two "
            "laptops. Without $elemMatch the search also returns O5001, one laptop and two "
            "mice, and the agent contacts the wrong customer.",
    },
    28: {
        "talking_points": [
            tp("insertOne()",
               "Demo 4.5 inserts DEMO-1 and returns acknowledged: true and an insertedId. "
               "mongod adds an ObjectId _id because the document has none."),
            tp("insertMany()",
               "Takes an array and returns insertedIds, one ObjectId per document, keyed "
               "\"0\", \"1\" and so on. Practise with free test SKUs such as A610, A611 and "
               "A612, which load.js does not create."),
            tp("Unique index",
               "sku has the sku_unique index, so inserting an existing SKU fails with an "
               "E11000 duplicate key error. If an exercise hits it, the SKU is left from an "
               "earlier run: reload the dataset."),
            tp("Types and verification",
               "Write money as Decimal128 and times as Date. Then read the document back "
               "with findOne({ sku: \"DEMO-1\" }) and delete the demo document afterwards."),
            _sample("Its Courses products are illustrations."),
        ],
    },
    30: {
        "talking_points": [
            tp("Three parts",
               "updateOne(filter, update, options). The filter picks the document, the "
               "update operators say what changes, and options add things like upsert."),
            tp("updateOne() and updateMany()",
               "updateOne() changes the first match; updateMany() changes every match. "
               "Always preview an updateMany() filter with find() and countDocuments() "
               "first."),
            tp("Matched but not modified",
               "L100 is already active, so $set active: true returns matchedCount 1 and "
               "modifiedCount 0. The document was found, and it already had that value."),
            _sample("Its MongoDB Basics product and inventory.stock field are illustrations."),
        ],
    },
    31: {
        "talking_points": [
            tp("$set and $unset",
               "$set adds a field or replaces its value. $unset removes a field; the value "
               "you give it doesn't matter — for example, A410's temporaryNote."),
            tp("$inc and $mul",
               "$inc adds to a number and $mul multiplies it, both on the server in one "
               "step. For prices, keep the Decimal128 type in mind."),
            tp("$min and $max",
               "$min changes the field only if the new value is lower; $max only if it is "
               "higher. They are useful for lowest-price or high-water-mark fields."),
            tp("$rename",
               "Renaming legacyName to catalogName with updateMany on "
               "{ legacyName: { $exists: true } } matches only L190. Preview the filter "
               "first: a rename touches every match."),
            tp("$currentDate",
               "$currentDate: { updatedAt: true } stamps the server's current date."),
            _sample("Its MongoDB Basics product with oldSku is an illustration."),
        ],
    },
    33: {
        "talking_points": [
            tp("$push",
               "$push appends a value. Run it twice and the value appears twice. $each "
               "pushes several values, and "
               "$slice with $each keeps an array bounded, for example the last ten status "
               "changes."),
            tp("$addToSet",
               "Lab 3 adds featured, office and wireless to A410 with $addToSet and $each. "
               "wireless is already there, so it stays once. The tags become wireless, "
               "accessories, featured, office."),
            tp("$pull and $pop",
               "$pull removes every element that matches a value or condition; Lab 3 pulls "
               "discontinued from L190. $pop removes the first (-1) or last (1) element and "
               "does not look at values."),
            _sample("Its audio and clearance tags and its ratings array are illustrations."),
        ],
    },
    35: {
        "talking_points": [
            tp("Positional $",
               "The filter must include the array condition, here \"items.sku\": \"L100\". "
               "Then \"items.$.quantity\" means the first element that matched. On O5001 "
               "only the L100 line changes, from 1 to 2."),
            tp("All elements",
               "\"items.$[].reviewed\": false sets the field on every item of the order. "
               "Try both on O5001, then reload."),
            tp("Filtered elements",
               "\"items.$[item].requiresReview\" with arrayFilters: [{ \"item.quantity\": "
               "{ $gte: 2 } }] changes only the lines with quantity 2 or more."),
            tp("Reload afterwards",
               "These exercises change O5001. Reload the dataset before labs that expect the "
               "original $elemMatch trap."),
            _sample("Its order 501 and SKUs such as KB-10 are illustrations."),
        ],
    },
    36: {
        "talking_points": [
            tp("replaceOne()",
               "replaceOne() swaps the whole body of the document. Only _id is kept, and any "
               "field you leave out disappears."),
            tp("$set",
               "$set changes only the named fields. For almost every business change this is "
               "what you want."),
            tp("Practise safely",
               "Demo 4.8 uses a test document such as DEMO-REP or TEMP-200. Never practise "
               "replaceOne() on L100; later labs depend on it."),
            _sample("Its Keyboard product with _id 101 is an illustration."),
        ],
    },
    37: {
        "talking_points": [
            tp("Upsert",
               "{ upsert: true } means: update the match, or insert when nothing matches. "
               "The inserted document combines the filter's equality fields and the update's "
               "fields."),
            tp("$setOnInsert",
               "Fields in $setOnInsert are written only on the insert path, so createdAt is "
               "set once and never overwritten."),
            tp("Exercise 4.3",
               "The first run inserts A700, Portable Charger, and returns the new _id. The "
               "second run matches it: updatedAt changes and createdAt stays."),
            tp("Filter on a unique field",
               "sku has a unique index. An upsert on a non-unique field can update the "
               "wrong document or insert duplicates."),
            _sample("Its KB-NEW Keyboard Lite is an illustration."),
        ],
    },
    42: {
        "talking_points": [
            tp("The fields",
               "acknowledged means the server accepted the write. matchedCount is how many "
               "documents the filter found, modifiedCount how many really changed. "
               "upsertedCount and the upserted _id appear when an upsert inserted."),
            tp("mongosh naming",
               "mongosh prints the upserted _id as insertedId; drivers call it upsertedId. "
               "It is null when nothing was inserted."),
            tp("Matched but not modified",
               "updateMany({}, { $pull: { tags: \"discontinued\" } }) matches all 13 "
               "products but modifies only 1, L190. The other 12 had nothing to pull."),
            tp("Deletes and bulk writes",
               "deleteOne and deleteMany return deletedCount. bulkWrite returns all the "
               "counts together."),
            _sample("Its K100 Keyboard and stock field are illustrations."),
        ],
    },
    38: {
        "talking_points": [
            tp("The routine",
               "Put the filter in a variable. Preview with find(), count with "
               "countDocuments(), check the number, and only then delete with the same "
               "filter."),
            tp("Demo 4.9",
               "Insert TEMP-100 first if needed. The count is 1, deleteOne returns "
               "deletedCount: 1, and a final find confirms TEMP-100 is gone while L100 "
               "remains."),
            tp("deleteOne() and deleteMany()",
               "deleteOne() removes the first match; deleteMany() removes every match. "
               "deleteMany({}) empties the collection and is never the right answer in "
               "these labs."),
            tp("Soft delete",
               "When deleted data may need to come back, many teams set a deletedAt field "
               "instead and filter it out of normal reads."),
            _sample("Its cancelled and archived orders are illustrations; training_store "
                    "orders use paymentStatus and fulfillmentStatus."),
        ],
    },
    41: {
        "talking_points": [
            tp("One request",
               "bulkWrite() sends several inserts, updates, replaces and deletes in one "
               "request and returns one combined result."),
            tp("Demo 4.10",
               "Insert DEMO-BULK, update it to active: false, and delete TEMP-100. The result "
               "is insertedCount 1, matchedCount 1, modifiedCount 1 and deletedCount 0. "
               "TEMP-100 was already deleted in Demo 4.9, so 0 is a normal outcome."),
            tp("Ordered or not",
               "By default operations run in order and stop at the first error. With "
               "ordered: false, MongoDB attempts them all and reports every error."),
            tp("Not a transaction",
               "Each operation is atomic on its own document, but the batch is not "
               "all-or-nothing. Multi-document transactions are a separate feature."),
            _sample("Its K100 and OLD9 products are illustrations."),
        ],
    },
    46: {
        "talking_points": [
            tp("Reproduce",
               "find({ price: \"49.99\" }) returns only XBAD, the one broken document, "
               "because the query compares a string."),
            tp("Compare with a real document",
               "findOne({ sku: \"P1001\" }) shows price: Decimal128(\"49.99\"). The stored "
               "type is Decimal128, not a string."),
            tp("Fix and test small",
               "{ price: Decimal128(\"49.99\") } returns P1001, the Wireless Keyboard. Test "
               "the smallest query first, sku alone, then add one condition at a time."),
            tp("Common causes",
               "A wrong field name, the wrong case, the wrong type or an unquoted path. "
               "The next slide gathers seven of them."),
            _sample("Its K100 product priced 49.99 is an illustration."),
        ],
    },
    47: {
        "talking_points": [
            tp("Build a precise filter",
               "find, updateOne, deleteOne and bulkWrite all start with a filter. Parts 1 to "
               "3 were about making it precise."),
            tp("Execute and read the result",
               "mongod runs the command on training_store and returns a result: documents "
               "for a read, counts for a write."),
            tp("Verify, then refine",
               "Check the result with findOne or countDocuments, and refine the filter when "
               "it doesn't match what you expected."),
        ],
    },
}

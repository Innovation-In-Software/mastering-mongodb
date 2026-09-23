#!/usr/bin/env python3
"""Speaker notes for the new Module 5 deck (The Aggregation Framework).

Written from scripts/module05_content_source.md, the Module 5 manifest, the
official Exercises 5.1-5.4 (labs/day-02/exercises), Day 2 Lab 4
(labs/day-02/lab4) and the training_store dataset (datasets/training_store/load.js), in plain short sentences. Composed into
the notes pane by mdb_speaker_notes.compose(), so the layout matches the other
decks: KEY TALKING POINTS / REAL-WORLD EXAMPLES / USE-CASE SCENARIO.

Keys are topic numbers: 1 and 2 are the cover and objectives; the others are the
diagram numbers (see build_module05_new.DIAGRAMS), merged on the same slide with
the diagram's own "what it shows" notes. Every number quoted here was checked
against a fresh load of training_store.
"""
from __future__ import annotations


def tp(point: str, explain: str) -> dict:
    return {"point": point, "explain": explain}


NOTES: dict[int, dict] = {
    1: {
        "talking_points": [
            tp("What aggregation is",
               "The aggregation framework runs documents through a pipeline of stages. "
               "Each stage receives documents, transforms them and passes the result to the "
               "next stage. "
               "That is how MongoDB answers questions such as revenue per customer or the top "
               "five products."),
            tp("What this module does",
               "We build pipelines on training_store: filter with $match, shape with $project "
               "and $set, summarize with $group, expand arrays with $unwind, join with $lookup "
               "and combine several reports with $facet. "
               "We finish with stage order and performance."),
            tp("Where it sits in the course",
               "Module 4 taught find() and updates. "
               "This module is the second half of Day 2, and it leads into Day 2 Lab 4. "
               "Module 6, on Day 3, makes these pipelines fast with indexes."),
        ],
        "real_world_examples": [
            "An online store's sales dashboard, a finance team's monthly revenue report and a "
            "product page's average rating can all be one aggregation pipeline each.",
        ],
    },
    2: {
        "talking_points": [
            tp("By the end of this module",
               "Walk through the six objectives on the left. "
               "Learners should be able to explain how documents flow through a pipeline, "
               "filter and reshape documents, and group them with accumulators. "
               "They should be able to work with the items array and join collections, build "
               "one report with several metrics, and put the stages in an order that is both "
               "correct and cheap."),
            tp("Six questions this module answers",
               "What is a pipeline? "
               "How do we filter and shape documents? "
               "How do we summarize them? "
               "How do we use arrays and other collections? "
               "How do we build one report with several metrics? "
               "And why does stage order matter?"),
            tp("Set the expectation",
               "Every result on these slides comes from the real training_store data. "
               "Learners can run each pipeline and get the same numbers."),
        ],
    },
    3: {
        "talking_points": [
            tp("Two tools, two jobs",
               "find() returns stored documents that match a filter. "
               "It is the right tool for everyday reads: one order, a customer's orders, the "
               "books in the catalog."),
            tp("When to aggregate",
               "Use aggregate() when the answer isn't stored in any single document: a count, a "
               "total, an average, a ranking or a join. "
               "The pipeline computes new documents from the stored ones."),
            tp("In training_store",
               "find() can list Aisha Khan's paid orders. "
               "Only aggregate() can tell us that together they are worth 3418.62."),
        ],
    },
    6: {
        "talking_points": [
            tp("The syntax",
               "aggregate() takes an array. "
               "Each element is one stage document, such as { $match: … }. "
               "MongoDB runs them in array order."),
            tp("A stream, not a table",
               "Documents flow from stage to stage. "
               "The output of one stage is the only input the next stage sees."),
            tp("Count and shape",
               "Some stages change how many documents there are: $match, $group, $limit, "
               "$unwind. "
               "Others change what each document looks like: $project, $set. "
               "$group does both."),
            tp("Nothing is written",
               "A normal pipeline doesn't change the stored documents. "
               "Only the write stages $out and $merge save results."),
        ],
    },
    9: {
        "talking_points": [
            tp("Order is meaning",
               "Stages run in the order you write them. "
               "Swap two stages and you may ask a different question, or no question at all."),
            tp("Group, then match",
               "$group outputs only _id and the accumulator fields. "
               "A $match on paymentStatus after it looks for a field that no longer exists, so "
               "it returns nothing. "
               "On training_store this pipeline returns zero documents."),
            tp("The fix",
               "Filter first, then group. "
               "Every total is then paid revenue only."),
        ],
    },
    11: {
        "talking_points": [
            tp("$match filters",
               "$match keeps the documents that satisfy a filter and drops the rest. "
               "It uses exactly the query language from Module 4."),
            tp("Our high-value orders",
               "paymentStatus PAID and total at least Decimal128 1000.00 match four orders: "
               "O6101, O6202, O6301 and O6304."),
            tp("Put it first",
               "A selective $match at the start means every later stage works on fewer "
               "documents. "
               "As the first stage it can also use an index, which is Module 6."),
        ],
    },
    20: {
        "talking_points": [
            tp("$project controls the output shape",
               "1 includes a field and 0 excludes it. "
               "_id is included unless you set it to 0."),
            tp("Include or exclude — not both",
               "A projection is either a list of fields to keep or a list of fields to drop. "
               "The only field you may exclude in an inclusion projection is _id."),
            tp("Rename and compute",
               "A new name with a $ path copies a value: productName: \"$name\". "
               "An expression computes one. "
               "Both change only the pipeline output, never the stored product."),
        ],
    },
    25: {
        "talking_points": [
            tp("Expressions per document",
               "Arithmetic expressions run once for each document: $add, $subtract, "
               "$multiply, $divide and $round."),
            tp("Line revenue",
               "training_store stores items.quantity and items.unitPrice. "
               "There is no lineTotal field, so we compute it: quantity times unitPrice. "
               "Guides that read items.lineTotal get null and a zero sum."),
            tp("$project or $set",
               "$project returns only the fields you list. "
               "$set, also called $addFields, adds or replaces fields and keeps everything "
               "else. "
               "Use $set for helper fields in the middle of a pipeline, $project for the final "
               "shape."),
        ],
    },
    35: {
        "talking_points": [
            tp("Dates are stored in UTC",
               "createdAt is a BSON Date: one instant, stored in UTC."),
            tp("Reports need a local day",
               "Grouping by day or month needs a time zone. "
               "$dateToString, $dateTrunc and the other date operators accept a timezone "
               "option."),
            tp("The diagram is our data",
               "2026-09-20T14:30Z is order O5001's createdAt. "
               "It is 10:30 in Toronto, 07:30 in Vancouver and 20:00 in Delhi. "
               "An order placed late in the evening can land in a different day, or month, "
               "depending on the zone."),
        ],
    },
    37: {
        "talking_points": [
            tp("$cond is if-then-else",
               "$cond takes a condition, a value when true and a value when false. "
               "It runs for each document."),
            tp("Order size",
               "We label paid orders HIGH_VALUE when total is at least 1000.00, otherwise "
               "STANDARD. "
               "O6201 at 79.07 is STANDARD; O6202 at 2146.99 is HIGH_VALUE."),
            tp("$switch for more branches",
               "$switch checks cases in order and uses the first one that is true, with a "
               "default when none match. "
               "It reads better than nested $cond."),
        ],
    },
    39: {
        "talking_points": [
            tp("One output per key",
               "$group collects documents with the same _id value into one output document. "
               "_id: \"$customerId\" means one result per customer."),
            tp("Accumulators",
               "Every other field in $group must be an accumulator: $sum, $avg, $min, $max, "
               "$first, $last, $push or $addToSet."),
            tp("Two kinds of $sum",
               "$sum: 1 adds one per document, so it counts. "
               "$sum: \"$total\" adds the field's values."),
            tp("_id: null",
               "Use _id: null to put the whole input in one group, for a grand total."),
        ],
    },
    46: {
        "talking_points": [
            tp("What survives $group",
               "Only _id and the accumulator fields leave $group. "
               "Every other field, such as orderNumber, items or fulfillmentStatus, is gone."),
            tp("Keep what you need",
               "If the report needs a value, collect it with an accumulator. "
               "$push keeps every value, $addToSet keeps unique values, and $first or $last "
               "keeps one."),
            tp("$first needs a $sort",
               "Without a $sort before $group, first is whatever order the documents arrived "
               "in. "
               "Sort first, then $first is meaningful."),
        ],
    },
    47: {
        "talking_points": [
            tp("A compound key",
               "_id can be a document. "
               "Each unique combination of its fields becomes one group."),
            tp("Payment by fulfillment",
               "Grouping training_store orders by paymentStatus and fulfillmentStatus gives "
               "seven combinations. "
               "PAID and SHIPPED is the largest: six orders worth 3809.48."),
            tp("Read _id in words",
               "The group with _id PENDING and NEW means all orders that are pending and new. "
               "That is O5001 and O6499. "
               "_id here is the grouping key, not an order's ObjectId."),
        ],
    },
    50: {
        "talking_points": [
            tp("Top N needs sort first",
               "$limit keeps the first N documents that reach it. "
               "If they haven't been sorted yet, you get N arbitrary documents."),
            tp("Ties",
               "O6202 and O6304 both total 2146.99. "
               "Adding orderNumber as a second sort key makes the order repeatable."),
            tp("$skip",
               "$sort, then $skip, then $limit pages through results. "
               "Large skips get slow, so production code often pages by range instead."),
        ],
    },
    51: {
        "talking_points": [
            tp("$count",
               "$count outputs one document holding the number of documents that reached it. "
               "It counts the pipeline stream, not the whole collection."),
            tp("$sortByCount",
               "$sortByCount groups by an expression, counts each group and sorts by the "
               "count, highest first. "
               "It is shorthand for $group with $sum: 1 followed by $sort."),
            tp("The diagram is our data",
               "training_store has six reviews: three 5-star, two 4-star and one 3-star."),
        ],
    },
    53: {
        "talking_points": [
            tp("One per element",
               "$unwind outputs one copy of the document for each element of the array. "
               "In each copy, the array field holds just that one element."),
            tp("Our three-item order",
               "O6303 has three items: MongoDB Fundamentals, Query Cookbook and the Wireless "
               "Keyboard. "
               "After $unwind it is three documents."),
            tp("Watch the size",
               "The 13 paid orders become 21 line documents. "
               "An order with 100 items becomes 100 documents, so filter before you unwind."),
        ],
    },
    61: {
        "talking_points": [
            tp("A left outer join",
               "$lookup adds the matching documents from another collection to each input "
               "document. "
               "Input documents without a match are kept."),
            tp("Always an array",
               "The as field is always an array: one element for one match, several for "
               "several, and empty for none."),
            tp("Our unmatched order",
               "O6499's customerId matches no customer, so its customer array is empty. "
               "A plain $unwind would drop it. "
               "preserveNullAndEmptyArrays: true keeps it."),
        ],
    },
    64: {
        "talking_points": [
            tp("Fixed bands",
               "$bucket groups documents into ranges you choose with boundaries. "
               "Each lower bound is included and each upper bound excluded."),
            tp("Our price bands",
               "With boundaries 0, 50, 100, 500 and 2000, training_store has five products "
               "under 50, two from 50 to 100, three from 100 to 500 and two from 500 to 2000."),
            tp("The default bucket",
               "Anything outside the boundaries, or of another type, goes to default. "
               "XBAD's price is the string \"49.99\", so it lands in Other."),
            tp("$bucketAuto",
               "$bucketAuto chooses the ranges for you, given a number of buckets."),
        ],
    },
    65: {
        "talking_points": [
            tp("Several pipelines, one input",
               "$facet runs several sub-pipelines on the same documents in one aggregate "
               "call."),
            tp("One result document",
               "The output is a single document. "
               "Each facet name is a field holding that sub-pipeline's results as an array."),
            tp("When to use it",
               "Dashboards and API responses that need several metrics at once: totals, "
               "breakdowns and top-N lists."),
            tp("Filter before it",
               "A $match before $facet runs once, and every facet benefits."),
        ],
    },
    76: {
        "talking_points": [
            tp("Start from the output",
               "Write down the result you want first: its fields and roughly how many rows."),
            tp("One stage at a time",
               "Run the first stage and look at the documents. "
               "Add the next stage and run again. "
               "A wrong field path or filter shows up the moment it is added."),
            tp("Prove one number",
               "Check one result by hand. "
               "Aisha Khan's four paid orders add up to 3418.62, which must match the "
               "pipeline."),
        ],
    },
    79: {
        "talking_points": [
            tp("Early $match",
               "Filtering first means every later stage handles fewer documents. "
               "Here 13 paid orders flow on instead of 17."),
            tp("Late $match can be wrong too",
               "In the diagram's late version, $match status runs after $group. "
               "As we saw in Part 1, $group has already removed that field, so the pipeline is "
               "not only slow but also empty."),
            tp("The optimizer helps, a little",
               "MongoDB moves some stages itself, such as a $match after a $sort. "
               "It can't fix a pipeline whose meaning is wrong, so write the efficient order "
               "yourself."),
            tp("Indexes",
               "A $match at the start can use an index, such as { paymentStatus: 1, "
               "createdAt: 1 }. "
               "Module 6 covers this."),
        ],
    },
    86: {
        "talking_points": [
            tp("The trap",
               "After $unwind, every line document still carries the whole order's total. "
               "Summing total then counts a two-item order twice and a three-item order three "
               "times."),
            tp("On our data",
               "Paid revenue is 9118.44. "
               "Unwinding first and summing total gives 12119.25: wrong by more than 3000."),
            tp("The rule",
               "Sum order-level fields before $unwind. "
               "Sum line-level values, quantity times unitPrice, after it."),
        ],
    },
    88: {
        "talking_points": [
            tp("Filter",
               "$match first, with the real field names: paymentStatus and "
               "fulfillmentStatus."),
            tp("Shape",
               "$project and $set rename fields and compute new ones, such as line revenue."),
            tp("Group",
               "$group with accumulators turns many documents into one per key."),
            tp("Join and arrays",
               "$unwind expands items; $lookup adds customer or product details as an array."),
            tp("Always",
               "Keep stage order in mind, use $ for field references and verify each stage."),
        ],
    },
}

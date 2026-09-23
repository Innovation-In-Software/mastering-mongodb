"""Key terms and abbreviations for the Module 5 deck (The Aggregation Framework).

Read by mdb_glossary.intro("module05"), which builds the Key Terms and Full Forms
slides that follow Learning Objectives.
"""
from __future__ import annotations

TERMS = [
    ("Aggregation pipeline", "An ordered array of stages that db.collection.aggregate() runs "
                             "on a stream of documents."),
    ("Stage", "One step such as $match, $group or $sort: it takes documents in and passes new "
              "documents on."),
    ("Field path", "\"$total\" or \"$items.quantity\": the $ tells MongoDB to read a field's "
                   "value, not the text."),
    ("Expression", "A calculation evaluated per document, such as $multiply, $concat or "
                   "$cond."),
    ("Grouping key", "The _id of $group: every distinct value becomes one output document."),
    ("Accumulator", "An operator that combines values across a group: $sum, $avg, $min, $max, "
                    "$push."),
    ("$unwind", "Turns one document with an array into one document per array element."),
    ("$lookup", "A left outer join to another collection; the matches arrive as an array."),
]

# Abbreviations that appear on the Module 5 slides (including the diagrams).
USED = ["API", "BSON", "CRUD", "ID", "SKU", "UTC"]

# Full forms not in mdb_acronyms.ACRONYMS.
ACRONYMS = {
    "UTC": "Coordinated Universal Time",
}

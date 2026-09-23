"""Key terms and full forms slides that open every module deck.

``intro(key)`` returns two flow steps — a Key Terms slide and a Full Forms slide —
placed right after Learning Objectives. Each module keeps its own terms in
``glossary_<key>.py`` (e.g. glossary_module03.py) so modules can be written
independently:

    TERMS = [("Document", "A record stored as field-value pairs ..."), ...]
    USED = ["BSON", "JSON", ...]          # abbreviations that appear on the slides
    ACRONYMS = {"WT": "WiredTiger"}       # optional: full forms not in mdb_acronyms
"""
from __future__ import annotations

import importlib

import mdb_flow_slides as F
from mdb_acronyms import ACRONYMS
from mdb_flow_slides import tp


def _load(key):
    mod = importlib.import_module(f"glossary_{key}")
    return list(mod.TERMS), list(getattr(mod, "USED", [])), dict(getattr(mod, "ACRONYMS", {}))


def intro(key):
    """Key Terms and Full Forms slides for one module deck."""
    terms, used, extra = _load(key)
    full = {**ACRONYMS, **extra}
    missing = [a for a in used if a not in full]
    assert not missing, f"{key}: no full form for {missing} -- add them to glossary_{key}.ACRONYMS"
    items = [(abbr, full[abbr]) for abbr in sorted(used, key=str.lower)]
    steps = [
        F.key_terms("Key Terms for This Module",
                    "Plain definitions for the words we'll use most.",
                    terms,
                    takeaway="Agree on the words first — every later slide builds on them.",
                    notes=[tp("How to run this slide",
                              "Read each term once and give a quick example from the training_store "
                              "sample database.")]
                          + [tp(term, definition) for term, definition in terms]),
    ]
    if items:
        steps.append(
            F.full_forms("Full Forms Used in This Module",
                         "Every abbreviation on these slides, spelled out.",
                         items,
                         takeaway="When an abbreviation isn't clear, the full form is on this slide.",
                         notes=[tp("How to run this slide",
                                   "Don't read every row. Point out the few this module uses most, and "
                                   "say the full list is here for reference."),
                                tp("Reference",
                                   "; ".join(f"{abbr} is {full}" for abbr, full in items) + ".")]))
    return steps

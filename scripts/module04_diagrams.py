"""Module 4 Marp diagrams — Mastering MongoDB Query Language (diagrams 1–162).

Style tokens from marp_svg_common. Run:

    python scripts/module04_diagrams.py
"""
from __future__ import annotations

import html
from pathlib import Path

from marp_svg_common import BORDER, FONT, HEADER_BG, MONO, MUTED, PANEL, RED, TEXT

BG_BOX = "#ffffff"
ASSETS = Path(__file__).resolve().parent.parent / "slides" / "assets" / "module-04"
W = 920


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


def _svg(height: int, body: str, marker_id: str = "ae") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}">
<defs>
  <marker id="{marker_id}" viewBox="0 0 10 10" markerWidth="7" markerHeight="7" refX="9" refY="5" orient="auto" markerUnits="userSpaceOnUse">
    <path d="M0,1 L9,5 L0,9 Z" fill="{RED}"/>
  </marker>
</defs>
<rect width="{W}" height="{height}" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>
{body}
</svg>
'''


def _box(x, y, w, h, title, sub=None, *, header=False, fs=18, sub_fs=14) -> str:
    fill = HEADER_BG if header else BG_BOX
    title_y = y + (h / 2 + fs * 0.35 if not sub else h * 0.38)
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{RED}" stroke-width="2"/>',
        f'<text x="{x + w / 2}" y="{title_y:.1f}" text-anchor="middle" font-family="{FONT}" font-size="{fs}" fill="{RED if header else TEXT}">{_esc(title)}</text>',
    ]
    if sub:
        parts.append(
            f'<text x="{x + w / 2}" y="{y + h * 0.72:.1f}" text-anchor="middle" font-family="{FONT}" font-size="{sub_fs}" fill="{MUTED}">{_esc(sub)}</text>'
        )
    return "\n".join(parts)


def _label(x, y, text, *, fs=16, fill=MUTED, anchor="middle") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" '
        f'font-size="{fs}" fill="{fill}">{_esc(text)}</text>'
    )


def _arrow(x1, y1, x2, y2, mid="ae") -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{RED}" '
        f'stroke-width="2" marker-end="url(#{mid})"/>'
    )


def render_vflow(title: str, boxes: list[tuple[str, str | None]], *, caption: str | None = None) -> str:
    parts = [_label(460, 28, title, fs=18, fill=TEXT)] if title else []
    y = 48 if title else 16
    x, w, h, gap = 160, 600, 48, 16
    for i, (t, sub) in enumerate(boxes):
        parts.append(_box(x, y, w, h, t, sub, fs=16 if sub else 18, sub_fs=14))
        if i < len(boxes) - 1:
            parts.append(_arrow(x + w / 2, y + h, x + w / 2, y + h + gap - 4))
        y += h + gap
    if caption:
        parts.append(_label(460, y + 8, caption, fs=15))
        y += 28
    return _svg(max(y + 16, 200), "\n".join(parts))


def render_hflow(title: str, boxes: list[str], *, caption: str | None = None) -> str:
    n = len(boxes)
    gap = 18
    bw = min(200, int((W - 40 - gap * (n - 1)) / n))
    total = n * bw + (n - 1) * gap
    x0 = (W - total) / 2
    parts = [_label(460, 28, title, fs=18, fill=TEXT)] if title else []
    y = 50
    for i, t in enumerate(boxes):
        x = x0 + i * (bw + gap)
        parts.append(_box(x, y, bw, 90, t, fs=13 if len(t) > 22 else 15))
        if i < n - 1:
            parts.append(_arrow(x + bw, y + 45, x + bw + gap - 4, y + 45))
    h = 170
    if caption:
        parts.append(_label(460, 160, caption, fs=15))
        h = 190
    return _svg(h, "\n".join(parts))


def render_two(title: str, left: tuple, right: tuple, *, caption: str | None = None, headers: bool = True) -> str:
    lt, ls = left[0], left[1] if len(left) > 1 else None
    rt, rs = right[0], right[1] if len(right) > 1 else None
    parts = [_label(460, 26, title, fs=18, fill=TEXT)] if title else []
    y = 46 if title else 20
    parts.append(_box(30, y, 420, 180, lt, ls, header=headers, fs=17, sub_fs=14))
    parts.append(_box(470, y, 420, 180, rt, rs, header=headers, fs=17, sub_fs=14))
    h = y + 200
    if caption:
        parts.append(_label(460, h, caption, fs=15))
        h += 24
    return _svg(h + 12, "\n".join(parts))


def render_grid(title: str, cells: list[tuple[str, str | None]], *, cols: int = 3, caption: str | None = None) -> str:
    parts = [_label(460, 26, title, fs=18, fill=TEXT)] if title else []
    y0 = 48 if title else 16
    n = len(cells)
    rows = (n + cols - 1) // cols
    gap = 14
    bw = int((W - 40 - gap * (cols - 1)) / cols)
    bh = 78
    for i, cell in enumerate(cells):
        r, c = divmod(i, cols)
        x = 20 + c * (bw + gap)
        y = y0 + r * (bh + gap)
        t, s = cell[0], cell[1] if len(cell) > 1 else None
        parts.append(_box(x, y, bw, bh, t, s, fs=14 if s else 15, sub_fs=12))
    h = y0 + rows * (bh + gap) + 8
    if caption:
        parts.append(_label(460, h, caption, fs=15))
        h += 24
    return _svg(h + 8, "\n".join(parts))


def render_table(title: str, headers: list[str], rows: list[tuple[str, ...]], *, caption: str | None = None, fs: int = 14) -> str:
    parts = [_label(460, 24, title, fs=17, fill=TEXT)] if title else []
    y0 = 40 if title else 16
    n = len(headers)
    leftover = W - 40
    col_ws = [leftover // n] * n
    col_ws[-1] = leftover - sum(col_ws[:-1])
    header_h, row_h = 42, 44
    x = 20
    for i, h in enumerate(headers):
        parts.append(_box(x, y0, col_ws[i], header_h, h, header=True, fs=fs))
        x += col_ws[i]
    for r, row in enumerate(rows):
        y = y0 + header_h + 5 + r * (row_h + 4)
        x = 20
        for i, cell in enumerate(row):
            parts.append(_box(x, y, col_ws[i], row_h, cell, fs=fs))
            x += col_ws[i]
    h = y0 + header_h + 5 + len(rows) * (row_h + 4) + 8
    if caption:
        parts.append(_label(460, h, caption, fs=14))
        h += 22
    return _svg(h + 8, "\n".join(parts))


def d(kind: str, *args, **kwargs):
    return lambda: {
        "vflow": render_vflow,
        "hflow": render_hflow,
        "two": render_two,
        "grid": render_grid,
        "table": render_table,
    }[kind](*args, **kwargs)


DIAGRAMS: dict[str, callable] = {
    "001-crud-operations-overview.svg": d(
        "table",
        "MongoDB CRUD operations",
        ["Operation", "Methods"],
        [
            ("Create", "insertOne / insertMany"),
            ("Read", "findOne / find"),
            ("Update", "updateOne / updateMany"),
            ("Replace", "replaceOne"),
            ("Delete", "deleteOne / deleteMany"),
        ],
    ),
    "002-query-anatomy.svg": d(
        "hflow",
        "db.products.find(filter, projection)",
        ["db", "products", "find()", "filter", "projection"],
        caption="General form: db.collection.method(filter, options) → results",
    ),
    "003-business-requirement-to-query.svg": d(
        "hflow",
        "Business question to MongoDB query",
        ["Question", "Collection", "Filter", "Projection", "Sort", "Result"],
    ),
    "004-query-execution-flow.svg": d(
        "vflow",
        "Query execution flow",
        [
            ("Client sends find(filter, projection)", None),
            ("MongoDB server evaluates the filter", None),
            ("Matching documents are selected", None),
            ("Projection, sort, limit shape the cursor", None),
            ("Batches return to the client", None),
        ],
    ),
    "005-training-dataset.svg": d(
        "grid",
        "training_store — four collections",
        [
            ("products", "sku · price · tags · attributes"),
            ("customers", "name · contact · addresses"),
            ("orders", "customerId · items[] · totals"),
            ("reviews", "sku · rating · body"),
        ],
        cols=2,
        caption="Same Day 1 dataset — richer fields for query practice",
    ),
    "006-query-workflow.svg": d(
        "vflow",
        "Query workflow",
        [
            ("Select the database  —  use training_store", None),
            ("Inspect one sample document", None),
            ("Build a filter from field paths and types", None),
            ("Execute find / findOne", None),
            ("Validate the result set", None),
        ],
    ),
    "007-findone-vs-find.svg": d(
        "two",
        "findOne() vs find()",
        ("findOne()", "One document or null"),
        ("find()", "Cursor of 0..n documents"),
        caption="Use findOne when one result is expected",
    ),
    "008-empty-vs-targeted-filter.svg": d(
        "two",
        "Empty filter vs targeted filter",
        ("{}", "Every document in the collection"),
        ('{ category: "LAPTOP" }', "Only documents that match"),
        caption="Empty filters are legal on find and disastrous on deleteMany",
    ),
    "009-equality-filter.svg": d(
        "vflow",
        'Equality filter  —  category: "LAPTOP"',
        [
            ("All products", None),
            ("Keep documents where category equals LAPTOP", None),
            ("L100 · L110 · L190", None),
        ],
        caption="Field names and string values are case-sensitive",
    ),
    "010-implicit-and-filter.svg": d(
        "hflow",
        "Implicit AND — both fields on the same document",
        ["category: LAPTOP", "AND", "active: true"],
        caption="Comma-separated fields already mean AND",
    ),
    "011-nested-field-dot-notation.svg": d(
        "vflow",
        "Dot notation into nested fields",
        [
            ("product document", None),
            ("attributes { memoryGB: 16, ... }", None),
            ('Query  "attributes.memoryGB": 16', None),
        ],
        caption="Always quote dotted paths",
    ),
    "012-query-result-set.svg": d(
        "hflow",
        "Collection → filter → matching subset",
        ["Entire collection", "Filter", "Matching documents"],
    ),
    "013-field-name-and-type-matching.svg": d(
        "two",
        "Name and BSON type must both match",
        ("Matches", 'category: "LAPTOP"  ·  Decimal128 price'),
        ("Misses", "Category  ·  price as string  ·  laptop"),
        caption="XBAD is the planted string-price error",
    ),
    "014-comparison-operators-overview.svg": d(
        "table",
        "Comparison operators",
        ["Operator", "Meaning"],
        [
            ("$eq / $ne", "Equal / not equal"),
            ("$gt / $gte", "Greater than / or equal"),
            ("$lt / $lte", "Less than / or equal"),
        ],
        caption="Put operators inside the field: { price: { $gt: Decimal128(...) } }",
    ),
    "015-numeric-range-query.svg": d(
        "hflow",
        "Numeric range — inclusive bounds on price",
        ["$gte 50.00", "matching prices", "$lte 150.00"],
        caption="One field, two operators in the same object",
    ),
    "016-date-range-query.svg": d(
        "hflow",
        "Date range on createdAt",
        ["$gte 2026-09-01", "order date", "$lt 2026-10-01"],
        caption="Use BSON Date / ISODate — not date strings",
    ),
    "017-in-operator.svg": d(
        "vflow",
        "$in — one field, several permitted values",
        [
            ('category $in ["BOOK", "ACCESSORY"]', None),
            ("Match if the field equals any listed value", None),
            ("Books and accessories", None),
        ],
    ),
    "018-nin-operator.svg": d(
        "vflow",
        "$nin — exclude a list of values",
        [
            ('category $nin ["LAPTOP", "SHOE"]', None),
            ("Reject listed categories", None),
            ("Books, accessories, and XBAD remain", None),
        ],
    ),
    "019-equality-vs-in.svg": d(
        "two",
        "One accepted value vs several",
        ('Equality', 'category: "BOOK"'),
        ("$in", 'category: { $in: ["BOOK", "ACCESSORY"] }'),
        caption="$in is the clean form of $or when alternatives share one field",
    ),
    "020-inclusive-vs-exclusive.svg": d(
        "table",
        "Inclusive vs exclusive boundaries",
        ["Exclusive", "Inclusive"],
        [("$gt  50  —  above 50", "$gte  50  —  50 and above"), ("$lt  150  —  below 150", "$lte  150  —  150 and below")],
    ),
    "021-logical-operators-overview.svg": d(
        "grid",
        "Logical operators",
        [
            ("$and", "All expressions match"),
            ("$or", "At least one matches"),
            ("$nor", "None of them match"),
            ("$not", "Negate a field condition"),
        ],
        cols=2,
    ),
    "022-implicit-vs-explicit-and.svg": d(
        "two",
        "Implicit AND vs explicit $and",
        ("Implicit", "Two different fields in one document"),
        ("Explicit $and", "Array of conditions — use when keys would collide"),
    ),
    "023-or-operator.svg": d(
        "hflow",
        "$or — alternatives converge on one result set",
        ["category BOOK", "OR", "price < 50"],
    ),
    "024-nor-operator.svg": d(
        "vflow",
        "$nor — reject documents matching any listed condition",
        [
            ("Prohibited: tags discontinued  OR  active false", None),
            ("Keep documents matching none of those", None),
            ("L190 is excluded on both counts", None),
        ],
    ),
    "025-not-operator.svg": d(
        "vflow",
        "$not — field-level negation",
        [
            ("price $gt 500", None),
            ("$not that condition", None),
            ("Also matches missing price unless you add $exists", None),
        ],
    ),
    "026-combined-logical-query.svg": d(
        "vflow",
        "Required condition plus alternatives",
        [
            ("active: true  (required)", None),
            ("$or: category BOOK  or  tags business", None),
            ("Both layers must hold", None),
        ],
    ),
    "027-nested-logical-conditions.svg": d(
        "grid",
        "AND containing OR branches",
        [
            ("Outer AND", "Must all be true"),
            ("Branch A", "category LAPTOP"),
            ("Branch B", "price under 100"),
        ],
        cols=3,
        caption="Read the filter out loud as English before you run it",
    ),
    "028-query-logic-venn.svg": d(
        "grid",
        "AND, OR, and NOR result sets",
        [
            ("AND", "Intersection — both true"),
            ("OR", "Union — either true"),
            ("NOR", "Outside both sets"),
        ],
        cols=3,
    ),
    "029-field-exists-vs-missing.svg": d(
        "two",
        "$exists — field present vs absent",
        ("$exists: true", "P1001 and B310 have discountPrice"),
        ("$exists: false", "Most catalog items never had the field"),
    ),
    "030-null-vs-missing.svg": d(
        "table",
        "Null vs missing phone",
        ["Query", "Matches"],
        [
            ('{ "contact.phone": null }', "Null OR missing — too broad"),
            ('{ "contact.phone": { $type: "null" } }', "C204 — field present, BSON null"),
            ('{ "contact.phone": { $exists: false } }', "C515 — field absent"),
        ],
    ),
    "031-bson-type-query.svg": d(
        "grid",
        "$type groups documents by BSON type",
        [
            ("decimal", "Money — correct here"),
            ("string", "XBAD price"),
            ("date", "createdAt"),
            ("bool", "active"),
            ("int", "memoryGB · rating"),
            ("null", "Intentional empty"),
        ],
        cols=3,
    ),
    "032-data-type-quality-check.svg": d(
        "two",
        "Price type quality check",
        ("Decimal128", "Numeric comparisons work"),
        ('price: "49.99"', "XBAD — $gt misses or sorts wrongly"),
    ),
    "033-optional-field-analysis.svg": d(
        "hflow",
        "$exists for migrations",
        ["No discountPrice", "Migrating", "discountPrice present"],
        caption="Count both sides before a $unset or $rename",
    ),
    "034-regex-matching.svg": d(
        "vflow",
        "Regular-expression matching on name",
        [
            ("Product names in the collection", None),
            ("Pattern applied to the string field", None),
            ("Matching names returned", None),
        ],
        caption="Regex can be expensive — prefer anchored prefixes",
    ),
    "035-prefix-search.svg": d(
        "hflow",
        'Prefix search  ^Mongo',
        ["MongoDB Fundamentals", "matches", "Query Cookbook does not"],
        caption="Anchor with ^ so the index can participate",
    ),
    "036-case-sensitive-vs-insensitive.svg": d(
        "two",
        "Case-sensitive vs $options: i",
        ("Default", "Mongo ≠ mongo"),
        ('$options: "i"', "Mongo and mongo both match"),
    ),
    "037-anchored-vs-unanchored-regex.svg": d(
        "two",
        "Anchored vs unanchored regex",
        ("^Mongo", "Starts with Mongo — index-friendlier"),
        ("Mongo anywhere", "Substring scan of the field"),
    ),
    "038-array-query-fundamentals.svg": d(
        "vflow",
        "Array containment — tags: technology",
        [
            ("tags: [database, technology]", None),
            ("Scalar equality matches any element", None),
            ("B300 matches — extra tags are allowed", None),
        ],
    ),
    "039-exact-array-match.svg": d(
        "grid",
        "Exact array match requires all three",
        [
            ("Same values", None),
            ("Same order", None),
            ("Same length", None),
        ],
        cols=3,
        caption='tags: ["database","technology"] fails if a third tag exists',
    ),
    "040-contains-array-element.svg": d(
        "two",
        "Contains one value vs exact array",
        ("Contains", 'tags: "technology"'),
        ("Exact", 'tags: ["database","technology"]'),
    ),
    "041-all-operator.svg": d(
        "vflow",
        "$all — every listed value, any order, extras allowed",
        [
            ('$all: ["database", "technology"]', None),
            ("B300 matches", None),
        ],
    ),
    "042-size-operator.svg": d(
        "two",
        "$size — exact element count",
        ("$size: 2", "Most training_store tag arrays"),
        ("Cannot say ≥ 2", "Use aggregation or field.0 $exists"),
    ),
    "043-array-of-embedded-documents.svg": d(
        "vflow",
        "Order items — array of documents",
        [
            ("O5001", None),
            ("items[0]  L100  qty 1", None),
            ("items[1]  A410  qty 2", None),
        ],
        caption="Teaching trap: two conditions can hit different lines",
    ),
    "044-querying-field-inside-array.svg": d(
        "hflow",
        "Dot notation from items to sku",
        ["orders", "items[]", '"items.sku": "L100"'],
        caption="Enough for “orders that contain this product”",
    ),
    "045-why-elemmatch.svg": d(
        "two",
        "Why $elemMatch is needed",
        ("Without", "L100 on one item, qty ≥ 2 on another — O5001"),
        ("With $elemMatch", "Both conditions on the SAME item — O6401 only"),
        caption="O5001 is the classroom trap",
    ),
    "046-elemmatch-query-flow.svg": d(
        "vflow",
        "$elemMatch tests elements one at a time",
        [
            ("Open the items array", None),
            ("Test element 0 — all conditions?", None),
            ("If not, test element 1", None),
            ("Keep the parent document if any element passes", None),
        ],
    ),
    "047-scalar-vs-document-array.svg": d(
        "two",
        "Scalar array vs document array",
        ("tags[]", "Equality, $all, $size"),
        ("items[]", "Dot path or $elemMatch"),
    ),
    "048-filter-vs-projection.svg": d(
        "two",
        "Filter vs projection",
        ("Filter", "Which documents"),
        ("Projection", "Which fields"),
        caption="Do not mix inclusion and exclusion except for _id",
    ),
    "049-inclusion-projection.svg": d(
        "hflow",
        "Inclusion — only listed fields (+ _id unless excluded)",
        ["Full document", "{ name: 1, price: 1, _id: 0 }", "name + price"],
    ),
    "050-exclusion-projection.svg": d(
        "hflow",
        "Exclusion — all fields except listed",
        ["Full document", "{ attributes: 0, tags: 0 }", "Everything else"],
    ),
    "051-projection-rules.svg": d(
        "table",
        "Projection rules",
        ["Mode", "Rule"],
        [
            ("Inclusion", "List fields to keep"),
            ("Exclusion", "List fields to drop"),
            ("Mix", "Illegal — except excluding _id from inclusion"),
        ],
    ),
    "052-nested-field-projection.svg": d(
        "vflow",
        "Project nested customer fields",
        [
            ("Full C101 document", None),
            ('"name.first"  "name.last"  "contact.email"', None),
            ("Compact contact card", None),
        ],
    ),
    "053-array-projection-elemmatch.svg": d(
        "two",
        "$elemMatch in a projection",
        ("Filter", "Still selected the order document"),
        ("Projection", "items array reduced to the matching line"),
    ),
    "054-array-projection-slice.svg": d(
        "hflow",
        "$slice — keep the first or most recent N",
        ["Long array", "{ reviews: { $slice: 3 } }", "Three elements"],
        caption="$slice is positional, not a query",
    ),
    "055-network-payload-reduction.svg": d(
        "two",
        "Network payload",
        ("Full documents", "Attributes, tags, nested arrays"),
        ("Projected rows", "name · category · price"),
        caption="Projection is for clarity and transfer size — not security",
    ),
    "056-cursor-lifecycle.svg": d(
        "hflow",
        "Cursor lifecycle",
        ["Query", "Cursor", "Batches", "Iterate", "Exhausted"],
    ),
    "057-filter-sort-limit.svg": d(
        "vflow",
        "Filter, sort, and limit",
        [
            ("find(filter, projection)", None),
            ("sort({ price: -1, _id: 1 })", None),
            ("limit(5)", None),
        ],
        caption="Conceptual order: filter → shape → sort → limit",
    ),
    "058-ascending-vs-descending.svg": d(
        "two",
        "Sort direction",
        ("Ascending  1", "Low price to high"),
        ("Descending  -1", "High price to low"),
    ),
    "059-multi-field-sorting.svg": d(
        "hflow",
        "Multi-field sort",
        ["Group by category", "Then price -1", "Then _id 1"],
    ),
    "060-deterministic-sorting.svg": d(
        "vflow",
        "Deterministic sort needs a unique tiebreaker",
        [
            ("sort({ price: -1 })  —  ties are undefined", None),
            ("Add _id: 1", None),
            ("Page 1 and page 2 never overlap", None),
        ],
    ),
    "061-limiting-results.svg": d(
        "hflow",
        "limit() reduces a large match set",
        ["All matching docs", "limit(5)", "Five documents"],
    ),
    "062-skip-limit-pagination.svg": d(
        "hflow",
        "Skip-and-limit pagination",
        ["sort", "skip offset", "limit page size"],
        caption="Fine for shallow pages; costly for deep offsets",
    ),
    "063-page1-vs-page2.svg": d(
        "two",
        "Page 1 vs page 2 (size 5)",
        ("Page 1", "skip 0  ·  limit 5"),
        ("Page 2", "skip 5  ·  limit 5"),
        caption="Same sort key on every page",
    ),
    "064-offset-vs-range-pagination.svg": d(
        "two",
        "Offset vs range-based pagination",
        ("skip(10000)", "Server still walks the offset"),
        ("_id > lastSeen", "Indexed range — prefer for deep pages"),
    ),
    "065-count-operations.svg": d(
        "two",
        "Counting documents",
        ("countDocuments(filter)", "Accurate filtered count"),
        ("estimatedDocumentCount()", "Fast estimate — ignores the filter"),
        caption="Prefer countDocuments over legacy count()",
    ),
    "066-distinct-values.svg": d(
        "hflow",
        "distinct(category)",
        ["Repeated categories", "Unique list", "ACCESSORY BOOK LAPTOP SHOE"],
    ),
    "067-insertone-flow.svg": d(
        "vflow",
        "insertOne flow",
        [
            ("New document", None),
            ("Validation / unique index", None),
            ("_id generated if omitted", None),
            ("Stored + acknowledged + insertedId", None),
        ],
    ),
    "068-insertmany-flow.svg": d(
        "hflow",
        "insertMany — one round trip",
        ["Document batch", "Validate each", "insertedIds map"],
    ),
    "069-automatic-id-generation.svg": d(
        "hflow",
        "Automatic _id",
        ["Insert without _id", "ObjectId assigned", "Unique stored document"],
    ),
    "070-insert-result-anatomy.svg": d(
        "grid",
        "Insert result anatomy",
        [
            ("acknowledged", "Write concern met"),
            ("insertedId", "insertOne"),
            ("insertedIds", "insertMany"),
        ],
        cols=3,
    ),
    "071-insert-and-verify.svg": d(
        "vflow",
        "Insert-and-verify workflow",
        [
            ("insertOne / insertMany", None),
            ("Inspect insertedId(s)", None),
            ("findOne by sku / customerNumber", None),
            ("Confirm Decimal128 and Date types", None),
        ],
    ),
    "072-valid-vs-invalid-insert.svg": d(
        "two",
        "Valid vs invalid insert",
        ("Accepted", "Unique sku · Decimal128 price"),
        ("Rejected", "Duplicate sku_unique index"),
    ),
    "073-single-vs-batch-insert.svg": d(
        "two",
        "One insert vs a batch",
        ("insertOne × N", "N round trips"),
        ("insertMany", "One request, several documents"),
    ),
    "074-update-anatomy.svg": d(
        "hflow",
        "Update anatomy",
        ["Collection", "Filter", "Operator", "Options", "Result"],
    ),
    "075-updateone-flow.svg": d(
        "vflow",
        "updateOne",
        [
            ("Filter selects candidates", None),
            ("First match is updated", None),
            ("Read matchedCount and modifiedCount", None),
        ],
    ),
    "076-updatemany-flow.svg": d(
        "vflow",
        "updateMany",
        [
            ("Preview the filter with find()", None),
            ("Every match is updated", None),
            ("matchedCount should equal the preview count", None),
        ],
        caption="Never start with {}",
    ),
    "077-set-operator.svg": d(
        "two",
        "$set — change or add listed fields only",
        ("Existing field", "price becomes 64.99"),
        ("New field", "featured: true is added"),
    ),
    "078-unset-operator.svg": d(
        "hflow",
        "$unset removes a field; siblings remain",
        ["A410 with temporaryNote", "$unset", "Field gone"],
        caption="The assigned value is ignored",
    ),
    "079-inc-operator.svg": d(
        "hflow",
        "$inc is atomic",
        ["stockQuantity: 8", "$inc: 5", "13"],
        caption="Prefer $inc over read-modify-write",
    ),
    "080-mul-operator.svg": d(
        "hflow",
        "$mul multiplies a numeric field",
        ["price", "× 1.05", "New price"],
        caption="Be careful mixing Decimal128 and double",
    ),
    "081-min-and-max.svg": d(
        "two",
        "$min and $max",
        ("$min", "Set only if the new value is lower"),
        ("$max", "Set only if the new value is higher"),
    ),
    "082-rename-operator.svg": d(
        "hflow",
        "$rename",
        ["legacyName", "$rename", "catalogName"],
        caption="L190 is the leftover field in the seed",
    ),
    "083-nested-field-update.svg": d(
        "vflow",
        "Dot notation updates one child field",
        [
            ('$set: { "contact.email": "new@..." }', None),
            ("phone and other siblings remain", None),
        ],
    ),
    "084-targeted-vs-object-replacement.svg": d(
        "two",
        "Targeted update vs replacing the object",
        ("Safe", '"contact.email": "new@..."'),
        ("Unsafe", "contact: { email }  wipes phone"),
    ),
    "085-update-and-verify.svg": d(
        "hflow",
        "Update-and-verify loop",
        ["Preview find", "Update", "Read counts", "findOne again"],
    ),
    "086-updateone-vs-updatemany.svg": d(
        "two",
        "updateOne vs updateMany",
        ("updateOne", "First match only"),
        ("updateMany", "Every match — preview first"),
    ),
    "087-update-result-anatomy.svg": d(
        "grid",
        "Update result anatomy",
        [
            ("acknowledged", None),
            ("matchedCount", None),
            ("modifiedCount", None),
            ("upsertedId", "Present only on insert-via-upsert"),
        ],
        cols=2,
    ),
    "088-matched-but-not-modified.svg": d(
        "vflow",
        "matchedCount 1 · modifiedCount 0",
        [
            ("Filter found the document", None),
            ("Requested value was already stored", None),
            ("Not a failed update", None),
        ],
    ),
    "089-array-update-operators.svg": d(
        "table",
        "Array update operators",
        ["Operator", "Behavior"],
        [
            ("$push", "Add — may duplicate"),
            ("$addToSet", "Add only if absent"),
            ("$pull / $pullAll", "Remove by match / values"),
            ("$pop", "First (-1) or last (1)"),
        ],
    ),
    "090-push-operator.svg": d(
        "hflow",
        "$push appends",
        ["tags: [office]", '$push "featured"', "[office, featured]"],
    ),
    "091-push-each.svg": d(
        "hflow",
        "$push with $each",
        ["Existing tags", "$each [portable, usb-c]", "Several values added"],
    ),
    "092-push-position.svg": d(
        "hflow",
        "$position inserts at an index",
        ["Array", "$position: 0", "New value at the front"],
    ),
    "093-push-sort-slice.svg": d(
        "vflow",
        "Bounded recent-events array",
        [
            ("$each  +  $position: 0", None),
            ("$sort optional", None),
            ("$slice: 10 keeps the array bounded", None),
        ],
    ),
    "094-addtoset-operator.svg": d(
        "vflow",
        "$addToSet — duplicate check first",
        [
            ("Is the value already in the array?", None),
            ("No → add it", None),
            ("Yes → matchedCount 1, modifiedCount 0", None),
        ],
    ),
    "095-push-vs-addtoset.svg": d(
        "two",
        "$push vs $addToSet",
        ("$push twice", "Duplicate featured tags"),
        ("$addToSet twice", "Second run does not duplicate"),
    ),
    "096-pull-operator.svg": d(
        "hflow",
        "$pull removes matching values",
        ["tags include discontinued", "$pull", "All discontinued gone"],
    ),
    "097-pullall-operator.svg": d(
        "hflow",
        "$pullAll removes several exact values",
        ["[old, clearance, office]", "$pullAll [old, clearance]", "[office]"],
    ),
    "098-pop-operator.svg": d(
        "two",
        "$pop is positional",
        ("$pop: 1", "Remove last element"),
        ("$pop: -1", "Remove first element"),
        caption="Use $pull when the value — not the position — decides removal",
    ),
    "099-positional-dollar.svg": d(
        "vflow",
        "Positional $ — first matched element",
        [
            ("Filter must identify the array element", None),
            ('"items.sku": "A410"', None),
            ('$set "items.$.quantity": 4', None),
        ],
    ),
    "100-all-positional.svg": d(
        "hflow",
        "$[] updates every element",
        ["items[]", '"items.$[].reviewed": true', "All lines reviewed"],
    ),
    "101-filtered-positional.svg": d(
        "vflow",
        "Filtered positional $[item]",
        [
            ('$set "items.$[item].discounted": true', None),
            ("arrayFilters: item.unitPrice >= 100", None),
            ("L100 discounted; cheap A410 is not", None),
        ],
    ),
    "102-array-filter-execution.svg": d(
        "vflow",
        "arrayFilters execution",
        [
            ("Match the parent document", None),
            ("Test each array element against arrayFilters", None),
            ("Update only the matching elements", None),
        ],
    ),
    "103-field-update-vs-replacement.svg": d(
        "two",
        "$set vs replaceOne",
        ("$set", "Unspecified fields remain"),
        ("replaceOne", "Omitted fields disappear; _id stays"),
    ),
    "104-replaceone-flow.svg": d(
        "vflow",
        "replaceOne flow",
        [
            ("Filter finds one document", None),
            ("Replacement document applied", None),
            ("_id is preserved", None),
        ],
    ),
    "105-replacement-risk.svg": d(
        "hflow",
        "Replacement risk",
        ["Doc with notes + tags", "replaceOne omits them", "notes and tags gone"],
    ),
    "106-upsert-decision-flow.svg": d(
        "vflow",
        "Upsert decision",
        [
            ("Filter on unique sku", None),
            ("Match? → update", None),
            ("No match? → insert", None),
        ],
    ),
    "107-set-vs-setoninsert.svg": d(
        "two",
        "$set vs $setOnInsert",
        ("$set", "Applied on update and insert — e.g. updatedAt"),
        ("$setOnInsert", "Applied only when inserting — e.g. createdAt"),
    ),
    "108-stable-upsert-filter.svg": d(
        "two",
        "Stable upsert filter",
        ("Unique sku", "At most one document"),
        ("Broad filter", "Duplicate inserts"),
    ),
    "109-first-vs-second-upsert.svg": d(
        "two",
        "Run the same upsert twice",
        ("First run", "upsertedId present · createdAt set"),
        ("Second run", "No upsertedId · createdAt unchanged"),
    ),
    "110-deleteone-flow.svg": d(
        "vflow",
        "deleteOne",
        [
            ("Precise unique filter", None),
            ("First match removed", None),
            ("deletedCount 0 or 1", None),
        ],
    ),
    "111-deletemany-flow.svg": d(
        "vflow",
        "deleteMany",
        [
            ("Filter — never {}", None),
            ("All matches removed", None),
            ("deletedCount must equal the preview", None),
        ],
    ),
    "112-safe-delete-workflow.svg": d(
        "vflow",
        "Safe delete workflow",
        [
            ("Build a precise filter", None),
            ("find() + countDocuments()", None),
            ("Confirm intended documents", None),
            ("deleteOne / deleteMany", None),
            ("Check deletedCount and query again", None),
        ],
    ),
    "113-unsafe-empty-delete.svg": d(
        "two",
        "Unsafe empty delete",
        ("deleteMany({})", "Every document in the collection"),
        ("Safe", "sku: /^TEMP-/  after preview"),
    ),
    "114-hard-vs-soft-delete.svg": d(
        "two",
        "Hard delete vs soft delete",
        ("Hard", "Document is gone"),
        ("Soft", "active: false  +  deletedAt"),
    ),
    "115-delete-result-anatomy.svg": d(
        "two",
        "Delete result",
        ("acknowledged", "Write concern met"),
        ("deletedCount", "Must match the preview count"),
    ),
    "116-accidental-broad-filter.svg": d(
        "two",
        "Accidental broad filter",
        ("Intended", "Two TEMP- lab products"),
        ("If filter is {}", "The entire catalog"),
    ),
    "117-bulk-write-overview.svg": d(
        "hflow",
        "bulkWrite groups operations",
        ["insertOne", "updateOne", "deleteOne"],
        caption="One round trip for related writes",
    ),
    "118-bulk-write-request-flow.svg": d(
        "vflow",
        "Bulk write request flow",
        [
            ("Client builds an operations array", None),
            ("Server executes (ordered by default)", None),
            ("Combined counts returned", None),
        ],
    ),
    "119-ordered-vs-unordered-bulk.svg": d(
        "two",
        "Ordered vs unordered bulkWrite",
        ("Ordered (default)", "Stop on first error"),
        ("Unordered", "Independent ops continue"),
    ),
    "120-bulk-write-result-anatomy.svg": d(
        "grid",
        "Bulk write counts",
        [
            ("insertedCount", None),
            ("matchedCount", None),
            ("modifiedCount", None),
            ("deletedCount", None),
            ("upsertedCount", None),
        ],
        cols=3,
    ),
    "121-individual-vs-bulk.svg": d(
        "two",
        "Round trips",
        ("Three separate writes", "Three client-server hops"),
        ("One bulkWrite", "One hop, combined result"),
    ),
    "122-single-document-atomicity.svg": d(
        "vflow",
        "One document write is atomic",
        [
            ("Several fields in the same document", None),
            ("Readers see all changes or none", None),
        ],
        caption="Embed data that must change together",
    ),
    "123-order-aggregate-atomic.svg": d(
        "grid",
        "Atomic order update",
        [
            ("fulfillmentStatus", None),
            ("items[].quantity", None),
            ("total", None),
        ],
        cols=3,
        caption="One updateOne on O5001 — not three collections",
    ),
    "124-single-vs-multi-document.svg": d(
        "two",
        "Single-document vs multi-document",
        ("One order document", "Atomic"),
        ("Order + product + customer", "May need a transaction"),
    ),
    "125-concurrent-inventory.svg": d(
        "two",
        "Inventory under concurrency",
        ("Read-modify-write", "Two clients can clobber stock"),
        ("$inc: -1", "Atomic decrement"),
    ),
    "126-conditional-update.svg": d(
        "vflow",
        "Update only in the expected business state",
        [
            ('Filter: fulfillmentStatus: "NEW"', None),
            ("$set PROCESSING", None),
            ("matchedCount 0 means someone else moved it", None),
        ],
    ),
    "127-optimistic-concurrency.svg": d(
        "hflow",
        "Optimistic concurrency",
        ["Filter includes version", "Update + $inc version", "Mismatched version → no match"],
    ),
    "128-safe-update-workflow.svg": d(
        "hflow",
        "Safe update workflow",
        ["Inspect", "Filter", "Count", "Update", "Result", "Verify"],
    ),
    "129-safe-delete-workflow-backup.svg": d(
        "hflow",
        "Safe delete with backup",
        ["Preview", "Count", "Backup if needed", "Delete", "Validate"],
    ),
    "130-troubleshooting-layers.svg": d(
        "vflow",
        "Troubleshooting layers",
        [
            ("Database name", None),
            ("Collection name", None),
            ("Field path and nesting", None),
            ("BSON type", None),
            ("Operator placement", None),
            ("Result / write counts", None),
        ],
    ),
    "131-common-query-mistakes.svg": d(
        "table",
        "Common query mistakes",
        ["Mistake", "Symptom"],
        [
            ("Wrong field case", "Zero matches"),
            ("String vs Decimal128", "Comparison fails"),
            ("Unquoted dotted path", "Syntax error"),
            ("No $elemMatch", "Conditions on different items"),
            ("Mixed projection", "Error"),
            ("Broad write filter", "Data loss"),
        ],
    ),
    "132-string-vs-numeric.svg": d(
        "two",
        "String vs numeric comparison",
        ('"100" vs "20"', "Lexical — '20' > '100' is false"),
        ("Decimal128 100 vs 20", "Numeric — 100 is greater"),
    ),
    "133-string-date-vs-bson-date.svg": d(
        "two",
        "String date vs BSON Date",
        ('"2026-09-01"', "Cannot range-query reliably"),
        ("ISODate(...)", "createdAt $gte / $lt works"),
    ),
    "134-missing-quotes-dot-notation.svg": d(
        "two",
        "Quotes around dotted paths",
        ("Invalid", "attributes.memoryGB: 16"),
        ("Valid", '"attributes.memoryGB": 16'),
    ),
    "135-projection-mixing-error.svg": d(
        "two",
        "Projection mixing",
        ("Error", "{ name: 1, tags: 0 }"),
        ("Legal", "{ name: 1, _id: 0 }  or  { tags: 0 }"),
    ),
    "136-query-building-workflow.svg": d(
        "hflow",
        "Build queries incrementally",
        ["{}", "category", "active", "price <= 100"],
        caption="Demo 4.2 — add one condition at a time",
    ),
    "137-write-verification-workflow.svg": d(
        "hflow",
        "Write verification",
        ["Operate", "Read counts", "findOne", "Confirm types"],
    ),
    "138-ex-4-1-basic-query-builder.svg": d(
        "table",
        "Exercise 4.1 — assemble a query",
        ["Task", "Starting point"],
        [
            ("All products", "find({})"),
            ("One SKU", 'findOne({ sku: "L100" })'),
            ("Active products", "{ active: true }"),
            ("ACTIVE customers", '{ status: "ACTIVE" }'),
            ("One order", '{ orderNumber: "O5001" }'),
        ],
    ),
    "139-ex-4-2-comparison-number-line.svg": d(
        "hflow",
        "Exercise 4.2 — price on a number line",
        ["$gt 100", "50 ≤ price ≤ 500", "$nin categories"],
    ),
    "140-ex-4-3-logical-query-builder.svg": d(
        "grid",
        "Exercise 4.3 — business rules to logic",
        [
            ("AND", "active and under 100"),
            ("OR / $in", "PENDING or PROCESSING"),
            ("$nor", "not discontinued, not inactive"),
        ],
        cols=3,
    ),
    "141-ex-4-4-null-or-missing.svg": d(
        "grid",
        "Exercise 4.4 — classify phone",
        [
            ("String value", "Most customers"),
            ("BSON null", "C204"),
            ("Field missing", "C515"),
        ],
        cols=3,
    ),
    "142-ex-4-5-array-query-challenge.svg": d(
        "hflow",
        "Exercise 4.5 — tag queries",
        ["contains", "$all", "$size: 2"],
    ),
    "143-ex-4-6-elemmatch-challenge.svg": d(
        "two",
        "Exercise 4.6 — same item, two conditions",
        ("O5001 trap", "L100 qty 1 + A410 qty 2"),
        ("O6401", "L100 qty 2"),
    ),
    "144-ex-4-7-projection-designer.svg": d(
        "hflow",
        "Exercise 4.7 — UI fields only",
        ["Full document", "Inclusion / exclusion", "UI payload"],
    ),
    "145-ex-4-8-pagination-planner.svg": d(
        "hflow",
        "Exercise 4.8 — pages of five",
        ["sort + _id", "page 1 skip 0", "page 2 skip 5"],
    ),
    "146-ex-4-9-insert-workflow.svg": d(
        "hflow",
        "Exercise 4.9 — insert workflow",
        ["Build", "Insert", "IDs", "Retrieve", "Verify types"],
    ),
    "147-ex-4-10-update-operator-selection.svg": d(
        "table",
        "Exercise 4.10 — pick an operator",
        ["Change", "Operator"],
        [
            ("New price", "$set"),
            ("Remove note", "$unset"),
            ("Stock +5", "$inc"),
            ("legacyName", "$rename"),
        ],
    ),
    "148-ex-4-11-array-operator-selection.svg": d(
        "table",
        "Exercise 4.11 — pick an array operator",
        ["Need", "Operator"],
        [
            ("Append, duplicates OK", "$push"),
            ("Unique tag", "$addToSet"),
            ("Remove a value", "$pull"),
            ("One matching line", "$"),
        ],
    ),
    "149-ex-4-12-upsert-lifecycle.svg": d(
        "two",
        "Exercise 4.12 — run twice",
        ("First", "Insert A700 · createdAt set"),
        ("Second", "Update · createdAt unchanged"),
    ),
    "150-ex-4-13-find-the-unsafe-operation.svg": d(
        "grid",
        "Exercise 4.13 — three unsafe writes",
        [
            ("updateMany({})", "All products inactive"),
            ("deleteMany({})", "All orders gone"),
            ("Replace contact {}", "Wipes phone"),
        ],
        cols=3,
    ),
    "151-ex-4-14-query-error-diagnosis.svg": d(
        "grid",
        "Exercise 4.14 — diagnosis map",
        [
            ("Wrong case", "Zero matches"),
            ("Wrong type", "XBAD / string money"),
            ("Unquoted path", "Syntax error"),
            ("Operator placement", "$gt at top level"),
            ("Mixed projection", "Error"),
            ("No $elemMatch", "O5001 false positive"),
        ],
        cols=3,
    ),
    "152-lab-4-1-dataset-verification.svg": d(
        "hflow",
        "Lab 4.1 — dataset verification",
        ["use db", "show collections", "count", "findOne"],
        caption="Fresh load: products 13 · customers 6 · orders 17 · reviews 6",
    ),
    "153-lab-4-2-product-query.svg": d(
        "hflow",
        "Lab 4.2 — product queries",
        ["Equality", "Range / $in", "Nested / tags", "sort · distinct"],
    ),
    "154-lab-4-3-customer-order-paths.svg": d(
        "grid",
        "Lab 4.3 — nested query paths",
        [
            ("contact.email", None),
            ("addresses.city", None),
            ("items.sku", None),
            ("customerId + $elemMatch", None),
        ],
        cols=2,
    ),
    "155-lab-4-4-projection-pagination.svg": d(
        "hflow",
        "Lab 4.4 pipeline",
        ["Filter", "Project", "Sort", "Skip", "Limit"],
    ),
    "156-lab-4-5-insert-operations.svg": d(
        "hflow",
        "Lab 4.5 — insert then verify",
        ["insertOne", "insertMany", "Customer", "Order", "find"],
    ),
    "157-lab-4-6-update-operations.svg": d(
        "hflow",
        "Lab 4.6 — preview → update → counts → verify",
        ["Preview", "$set $inc $min", "Counts", "findOne"],
    ),
    "158-lab-4-7-array-manipulation.svg": d(
        "hflow",
        "Lab 4.7 — array manipulation",
        ["$push", "$addToSet", "$", "$[]", "arrayFilters"],
    ),
    "159-lab-4-8-replace-upsert.svg": d(
        "hflow",
        "Lab 4.8 — three write styles",
        ["$set keeps fields", "replaceOne drops them", "upsert twice"],
    ),
    "160-lab-4-9-safe-deletion.svg": d(
        "hflow",
        "Lab 4.9 — TEMP- records only",
        ["Insert TEMP-", "Preview", "Count", "Delete", "Confirm L100"],
    ),
    "161-lab-4-10-integrated-crud.svg": d(
        "hflow",
        "Lab 4.10 — integrated CRUD",
        ["Product", "Customer", "Order", "Update", "Soft-delete"],
    ),
    "162-practical-challenge.svg": d(
        "grid",
        "Practical challenge — product and order administration",
        [
            ("Find + project", "Active products under a price"),
            ("Write safely", "Upsert, tags, inventory, status"),
            ("Verify", "Counts + before/after evidence"),
        ],
        cols=3,
    ),
}

# Backward-compatible aliases for the previous 40 filenames.
_ALIASES = {
    "01-crud-operations.svg": "001-crud-operations-overview.svg",
    "02-sample-dataset.svg": "005-training-dataset.svg",
    "03-query-anatomy.svg": "002-query-anatomy.svg",
    "04-crud-flow.svg": "003-business-requirement-to-query.svg",
    "05-query-filters.svg": "008-empty-vs-targeted-filter.svg",
    "06-findone-vs-find.svg": "007-findone-vs-find.svg",
    "07-nested-fields.svg": "011-nested-field-dot-notation.svg",
    "08-comparison-operators.svg": "014-comparison-operators-overview.svg",
    "09-logical-operators.svg": "021-logical-operators-overview.svg",
    "10-combining-conditions.svg": "026-combined-logical-query.svg",
    "11-exists-type.svg": "031-bson-type-query.svg",
    "12-null-and-missing.svg": "030-null-vs-missing.svg",
    "13-array-queries.svg": "038-array-query-fundamentals.svg",
    "14-elemmatch.svg": "045-why-elemmatch.svg",
    "15-projection.svg": "048-filter-vs-projection.svg",
    "16-cursor-pipeline.svg": "057-filter-sort-limit.svg",
    "17-pagination.svg": "062-skip-limit-pagination.svg",
    "18-count-distinct.svg": "065-count-operations.svg",
    "19-insert-verify.svg": "071-insert-and-verify.svg",
    "20-update-operators.svg": "074-update-anatomy.svg",
    "21-nested-update.svg": "084-targeted-vs-object-replacement.svg",
    "22-array-update-operators.svg": "089-array-update-operators.svg",
    "23-positional-updates.svg": "099-positional-dollar.svg",
    "24-replace-and-upsert.svg": "103-field-update-vs-replacement.svg",
    "25-delete-safety.svg": "112-safe-delete-workflow.svg",
    "26-bulk-write.svg": "117-bulk-write-overview.svg",
    "27-write-results.svg": "087-update-result-anatomy.svg",
    "28-atomicity.svg": "122-single-document-atomicity.svg",
    "29-safe-practices.svg": "128-safe-update-workflow.svg",
    "30-common-mistakes.svg": "131-common-query-mistakes.svg",
    "31-troubleshooting.svg": "130-troubleshooting-layers.svg",
    "32-module-4-concept-map.svg": "001-crud-operations-overview.svg",
    "33-demo-incremental.svg": "136-query-building-workflow.svg",
    "34-ex-4-1-read.svg": "138-ex-4-1-basic-query-builder.svg",
    "35-lab-product-query.svg": "153-lab-4-2-product-query.svg",
    "36-lab-integrated-crud.svg": "161-lab-4-10-integrated-crud.svg",
    "37-practical-challenge.svg": "162-practical-challenge.svg",
    "38-day2-result-path.svg": "003-business-requirement-to-query.svg",
    "39-push-modifiers.svg": "093-push-sort-slice.svg",
    "40-soft-delete.svg": "114-hard-vs-soft-delete.svg",
}

for alias, target in _ALIASES.items():
    DIAGRAMS[alias] = DIAGRAMS[target]


def write_all() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    written = 0
    for name, fn in DIAGRAMS.items():
        path = ASSETS / name
        path.write_text(fn(), encoding="utf-8")
        written += 1
    print(f"Wrote {written} SVG files into {ASSETS}")
    return written


if __name__ == "__main__":
    write_all()

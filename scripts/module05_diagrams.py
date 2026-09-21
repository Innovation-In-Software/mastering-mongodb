"""Module 5 Marp diagrams — MongoDB Aggregation Framework (171 diagrams).

Style tokens from marp_svg_common. Run:

    python scripts/module05_diagrams.py
"""
from __future__ import annotations

import html
from pathlib import Path

from marp_svg_common import BORDER, FONT, HEADER_BG, MONO, MUTED, PANEL, RED, TEXT

BG_BOX = "#ffffff"
ASSETS = Path(__file__).resolve().parent.parent / "slides" / "assets" / "module-05"
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


def _mono(x, y, text, *, fs=15, fill=TEXT, anchor="middle") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" '
        f'font-size="{fs}" fill="{fill}">{_esc(text)}</text>'
    )


def _arrow(x1, y1, x2, y2, mid="ae") -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{RED}" '
        f'stroke-width="2" marker-end="url(#{mid})"/>'
    )


def _vflow(boxes: list[tuple[str, str | None]], *, x=260, y=16, w=400, h=48, gap=18, mid="ae") -> list[str]:
    parts: list[str] = []
    cy = y
    for i, (title, sub) in enumerate(boxes):
        parts.append(_box(x, cy, w, h, title, sub, fs=16 if sub else 17, sub_fs=13))
        if i < len(boxes) - 1:
            parts.append(_arrow(x + w / 2, cy + h, x + w / 2, cy + h + gap - 4, mid))
        cy += h + gap
    return parts


def _hflow(boxes: list[tuple[str, str | None]], *, y=50, h=100, gap=24, mid="ae", x0=20, box_w=160) -> list[str]:
    parts: list[str] = []
    x = x0
    n = len(boxes)
    if n > 1:
        usable = W - 40 - (n - 1) * gap
        box_w = min(box_w, usable // n)
    for i, (title, sub) in enumerate(boxes):
        parts.append(_box(x, y, box_w, h, title, sub, fs=14 if sub else 15, sub_fs=12))
        if i < n - 1:
            parts.append(_arrow(x + box_w, y + h / 2, x + box_w + gap - 4, y + h / 2, mid))
        x += box_w + gap
    return parts


def _table(headers: list[str], rows: list[tuple[str, ...]], *, col_ws: list[int] | None = None, row_h=44, header_h=42, x0=20, y0=16, fs=14) -> list[str]:
    n = len(headers)
    if col_ws is None:
        leftover = W - 40
        col_ws = [leftover // n] * n
        col_ws[-1] = leftover - sum(col_ws[:-1])
    parts: list[str] = []
    x = x0
    for i, h in enumerate(headers):
        parts.append(_box(x, y0, col_ws[i], header_h, h, header=True, fs=fs))
        x += col_ws[i]
    for r, row in enumerate(rows):
        y = y0 + header_h + 6 + r * (row_h + 4)
        x = x0
        for i, cell in enumerate(row):
            parts.append(_box(x, y, col_ws[i], row_h, cell, fs=fs))
            x += col_ws[i]
    return parts


def pair(left: tuple[str, str | None], right: tuple[str, str | None], cap: str, mid: str) -> str:
    parts = [
        _box(40, 28, 400, 148, left[0], left[1], fs=18, sub_fs=14),
        _box(480, 28, 400, 148, right[0], right[1], fs=18, sub_fs=14),
    ]
    h = 200
    if cap:
        parts.append(_label(460, 204, cap, fs=15))
        h = 230
    return _svg(h, "\n".join(parts), mid)


def trio(items: list[tuple[str, str | None]], cap: str, mid: str) -> str:
    parts = _hflow(items, y=40, h=120, box_w=260, mid=mid)
    h = 180
    if cap:
        parts.append(_label(460, 190, cap, fs=15))
        h = 220
    return _svg(h, "\n".join(parts), mid)


def hflow(items: list[tuple[str, str | None]], cap: str, mid: str, *, hbox=100) -> str:
    parts = _hflow(items, y=40, h=hbox, mid=mid)
    h = 40 + hbox + 20
    if cap:
        parts.append(_label(460, h + 8, cap, fs=14))
        h += 36
    return _svg(h, "\n".join(parts), mid)


def vflow(items: list[tuple[str, str | None]], cap: str, mid: str) -> str:
    n = len(items)
    box_h = 46 if n >= 5 else 52
    gap = 16 if n >= 5 else 20
    parts = _vflow(items, h=box_h, gap=gap, mid=mid)
    h = 16 + n * box_h + (n - 1) * gap + 16
    if cap:
        parts.append(_label(460, h - 4, cap, fs=14))
        h += 24
    return _svg(max(h, 200), "\n".join(parts), mid)


def table_d(headers: list[str], rows: list[tuple[str, ...]], mid: str, *, fs=14) -> str:
    parts = _table(headers, rows, fs=fs)
    h = 16 + 42 + 6 + len(rows) * 48 + 12
    return _svg(h, "\n".join(parts), mid)


def four(items: list[tuple[str, str | None]], cap: str, mid: str) -> str:
    coords = [(30, 24), (475, 24), (30, 130), (475, 130)]
    parts = []
    for i, ((t, s), (x, y)) in enumerate(zip(items, coords)):
        parts.append(_box(x, y, 415, 90, t, s, fs=16, sub_fs=13))
    h = 240
    if cap:
        parts.append(_label(460, 246, cap, fs=14))
        h = 270
    return _svg(h, "\n".join(parts), mid)


# --- custom layouts that need more than a factory ---

def c_anatomy(mid: str) -> str:
    parts = [
        _mono(460, 28, "db.orders.aggregate([ { $match }, { $group }, { $sort } ])", fs=15),
        *_hflow(
            [("Collection", "orders"), ("aggregate()", "method"), ("Pipeline []", "stages"), ("Output", "new docs")],
            y=50, h=100, box_w=175, mid=mid,
        ),
        _label(460, 178, "Expressions live inside stages. Order is the pipeline.", fs=15),
    ]
    return _svg(210, "\n".join(parts), mid)


def c_dataset(mid: str) -> str:
    parts = [_label(460, 24, "training_store — reporting collections", fs=17, fill=TEXT)]
    cols = [
        (30, "products", "category · price · active"),
        (255, "orders", "items[] · status · total"),
        (480, "customers", "name · province · status"),
        (705, "reviews", "sku · rating · createdAt"),
    ]
    for x, title, sub in cols:
        parts.append(_box(x, 48, 185, 110, title, sub, fs=17, sub_fs=12))
    parts.append(_label(460, 186, "13 paid orders · July–September 2026", fs=14))
    return _svg(215, "\n".join(parts), mid)


def c_unwind(mid: str) -> str:
    parts = [
        _box(40, 24, 380, 150, "One order", "items: [L100, A400]", fs=18, sub_fs=15),
        _arrow(420, 99, 500, 99, mid),
        _box(500, 24, 380, 66, "Doc 1", "items: { sku: L100 }", fs=16, sub_fs=13),
        _box(500, 108, 380, 66, "Doc 2", "items: { sku: A400 }", fs=16, sub_fs=13),
    ]
    return _svg(200, "\n".join(parts), mid)


def c_lookup(mid: str) -> str:
    parts = [
        _box(40, 36, 260, 130, "orders", "localField: customerId", fs=17, sub_fs=13),
        _arrow(300, 101, 380, 101, mid),
        _box(380, 36, 260, 130, "customers", "foreignField: _id", fs=17, sub_fs=13),
        _arrow(640, 101, 720, 101, mid),
        _box(720, 36, 160, 130, "as", "array", fs=18, sub_fs=14),
    ]
    return _svg(200, "\n".join(parts), mid)


def c_facet(mid: str) -> str:
    parts = [
        _box(310, 12, 300, 46, "Same input documents", header=True, fs=16),
        _box(24, 78, 210, 88, "Counts", "orderCount", fs=16, sub_fs=13),
        _box(244, 78, 210, 88, "By status", "$group", fs=16, sub_fs=13),
        _box(464, 78, 210, 88, "Top N", "$sort + $limit", fs=16, sub_fs=13),
        _box(684, 78, 210, 88, "Bands", "$bucket", fs=16, sub_fs=13),
        _label(460, 192, "One output document; each facet is an array", fs=15),
    ]
    return _svg(220, "\n".join(parts), mid)


def c_concept(mid: str) -> str:
    parts = [
        _box(310, 12, 300, 46, "Aggregation pipeline", header=True, fs=16),
        _box(24, 80, 165, 78, "$match", "Filter", fs=16),
        _box(204, 80, 165, 78, "$set", "Calculate", fs=16),
        _box(384, 80, 165, 78, "$group", "Summarize", fs=16),
        _box(564, 80, 160, 78, "$unwind", "Arrays", fs=16),
        _box(739, 80, 155, 78, "$facet", "Reports", fs=16),
        _label(460, 186, "Order changes meaning and performance", fs=15),
    ]
    return _svg(215, "\n".join(parts), mid)


def c_switch(mid: str) -> str:
    parts = [
        _box(40, 20, 200, 180, "total", "input", fs=18, sub_fs=14),
        _box(300, 20, 280, 50, ">= 1000", "HIGH", fs=16, sub_fs=13),
        _box(300, 85, 280, 50, ">= 500", "MEDIUM", fs=16, sub_fs=13),
        _box(300, 150, 280, 50, "default", "LOW", fs=16, sub_fs=13),
        _box(640, 70, 240, 80, "orderSize", "one label", fs=18, sub_fs=14),
    ]
    parts.append(_arrow(240, 110, 300, 45, mid))
    parts.append(_arrow(240, 110, 300, 110, mid))
    parts.append(_arrow(240, 110, 300, 175, mid))
    return _svg(220, "\n".join(parts), mid)


def c_cond(mid: str) -> str:
    parts = [
        _box(40, 50, 240, 120, "Condition", "$gte total 1000", fs=18, sub_fs=14),
        _box(360, 20, 240, 80, "true", "HIGH_VALUE", fs=18, sub_fs=14),
        _box(360, 120, 240, 80, "false", "STANDARD", fs=18, sub_fs=14),
        _arrow(280, 90, 360, 60, mid),
        _arrow(280, 130, 360, 160, mid),
        _box(660, 70, 220, 80, "$cond", "one result", fs=18, sub_fs=14),
    ]
    return _svg(230, "\n".join(parts), mid)


def c_boundary(mid: str) -> str:
    parts = _hflow(
        [("0 ≤ p < 50", "under 50"), ("50 ≤ p < 100", "mid"), ("100 ≤ p < 500", "high"), ("500 ≤ p < 2000", "premium")],
        y=40, h=110, box_w=175, mid=mid,
    )
    parts.append(_label(460, 178, "Lower bound inclusive · upper bound exclusive · 50 enters the 50 bucket", fs=14))
    return _svg(210, "\n".join(parts), mid)


def c_index_pos(mid: str) -> str:
    parts = [
        _box(40, 30, 400, 150, "items[0] L100", "index: 0", fs=18, sub_fs=15),
        _box(480, 30, 400, 150, "items[1] A400", "index: 1", fs=18, sub_fs=15),
        _label(460, 210, "includeArrayIndex keeps the original position", fs=15),
    ]
    return _svg(240, "\n".join(parts), mid)


# Catalog: (number, slug, kind, payload)
# kind: pair, trio, hflow, vflow, table, four, custom
# payload depends on kind

CATALOG: list[tuple] = [
    (1, "operational-query-vs-aggregation", "pair", (("Operational query", "Retrieve stored documents"), ("Aggregation pipeline", "Transform into results"), "find() looks up records; aggregate() calculates")),
    (2, "aggregation-pipeline-overview", "vflow", ([("Collection", "orders"), ("Ordered stages", "each transforms"), ("Result", "report documents")], "Output of one stage is input of the next")),
    (3, "aggregation-pipeline-anatomy", "custom", c_anatomy),
    (4, "how-documents-move", "hflow", ([("Stage 1 output", "becomes"), ("Stage 2 input", "then"), ("Stage 3", "then"), ("Result", "report")], "Documents flow forward only")),
    (5, "pipeline-funnel", "hflow", ([("Large input", "17 orders"), ("Filtered", "13 paid"), ("Transformed", "shaped fields"), ("Grouped", "statuses"), ("Report", "ranked")], "Each stage can shrink volume")),
    (6, "stage-order-matters", "pair", (("$match then $group", "Filters source documents"), ("$group then $match", "Filters grouped output"), "Same stages, different meaning and cost")),
    (7, "document-count-and-shape", "hflow", ([("17 orders", "source"), ("$match", "13 paid"), ("$group", "4 statuses"), ("$sort", "4 ranked")], "Count, fields, and shape can all change")),
    (8, "business-question-to-pipeline", "vflow", ([("Reporting requirement", "top products?"), ("Source collection", "orders"), ("Stages", "match unwind group"), ("Metrics + output", "SKU revenue")], "")),
    (9, "analytical-dataset", "custom", c_dataset),
    (10, "development-workflow", "hflow", ([("Sample", "first stage"), ("Inspect", "shape"), ("Add one", "next stage"), ("Verify", "then continue")], "Build pipelines incrementally")),
    (11, "match-stage", "pair", (("$match", "Filter pipeline documents"), ("Smaller set", "Only matching docs continue"), "Same query language as find()")),
    (12, "early-match-optimization", "hflow", ([("Large collection", "all orders"), ("Selective $match", "PAID"), ("Fewer docs", "later stages cheaper")], "Filter before expensive work")),
    (13, "source-vs-group-match", "pair", (("Before $group", "Filters individual orders"), ("After $group", "Filters summary documents"), "Both valid — different questions")),
    (14, "find-vs-match", "pair", (("find({ paymentStatus })", "Operational lookup"), ("$match: { paymentStatus }", "Same filter in a pipeline"), "Conditions transfer; placement is new")),
    (15, "match-comparison", "table", (["Operator", "Selects"], [(" $gte / $lte", "Numeric or date range"), ("$in / $nin", "List membership"), ("Decimal128", "Required for money")])),
    (16, "match-logical", "trio", ([("AND", "Comma or $and"), ("$or", "Any branch"), ("$nor", "None match")], "Logical branches control pipeline input")),
    (17, "date-range-filtering", "hflow", ([("Start", "ISODate 2026-07-01"), ("createdAt", "$gte and $lt"), ("End", "ISODate 2026-10-01")], "Inclusive start, exclusive end")),
    (18, "selective-vs-nonselective-match", "pair", (("Selective", "PAID — 13 of 17"), ("Nonselective", "Most documents pass"), "Selectivity decides whether an index helps")),
    (19, "project-stage", "trio", ([("Include", "name: 1"), ("Rename", 'code: "$sku"'), ("Calculate", "$add / $cond")], "$project lists the output shape")),
    (20, "inclusion-projection", "pair", (("Keep listed fields", "name, price, _id: 0"), ("Drop the rest", "tags, attributes gone"), "Inclusion builds a small report document")),
    (21, "exclusion-projection", "pair", (("Remove listed fields", "attributes: 0"), ("Keep everything else", "sku, name, price remain"), "Do not mix inclusion and exclusion except _id")),
    (22, "field-renaming", "hflow", ([("sku", "stored"), ("productCode", "report name"), ("price", "stored"), ("sellingPrice", "report name")], "$ prefix copies the value")),
    (23, "calculated-fields-project", "hflow", ([("subtotal", None), ("+", "tax"), ("calculatedTotal", "$add")], "New field — stored documents unchanged")),
    (24, "set-stage", "pair", (("$set / $addFields", "Add or replace fields"), ("Other fields remain", "No need to list them"), "Aliases for this course use")),
    (25, "project-vs-set", "pair", (("$project", "You list what remains"), ("$set", "Unspecified fields are kept"), "Use $project for the final report shape")),
    (26, "unset-stage", "pair", (("$unset", "Drop pipeline fields"), ("Stored data", "Unchanged"), "O5001 internalNotes is a live demo field")),
    (27, "nested-output", "pair", (("Flat source", "sku, name, price"), ("Nested report", "product { code, name }"), "Objects in $project become nested output")),
    (28, "data-shaping-flow", "hflow", ([("Operational doc", "full order"), ("Cleaned", "$set / $unset"), ("Report doc", "$project")], "Shape last, after the metrics exist")),
    (29, "expression-categories", "table", (["Category", "Examples"], [("Arithmetic", "$add $multiply $round"), ("String", "$concat $toUpper"), ("Date", "$year $dateToString"), ("Conditional", "$cond $switch $ifNull")])),
    (30, "field-reference-syntax", "pair", (("$fieldName", "Value from this document"), ('"sku"', "Literal string sku"), "Missing $ is Exercise 5.11’s classic bug")),
    (31, "pipeline-variable-syntax", "table", (["Form", "Means"], [("$field", "Current document field"), ("$$variable", "Named variable"), ("$$ROOT", "Whole document"), ("$$CURRENT", "Current context")])),
    (32, "arithmetic-expression-flow", "hflow", ([("quantity", None), ("×", "unitPrice"), ("lineRevenue", None)], "Calculate after $unwind on items")),
    (33, "order-total-calculation", "hflow", ([("subtotal", None), ("+ tax", None), ("+ shipping", "$ifNull 0"), ("total", None)], "Missing shippingFee must not null the sum")),
    (34, "string-expression-flow", "hflow", ([("name.first", None), ("+", '" "'), ("name.last", None), ("full name", "$concat")], "Null part nulls the whole concat")),
    (35, "date-expression-flow", "hflow", ([("createdAt", "Date"), ("$dateToString", "%Y-%m"), ("2026-09", "report key")], "Name a time zone in production")),
    (36, "conditional-classification", "hflow", ([("< 500", "LOW"), ("500–999", "MEDIUM"), (">= 1000", "HIGH_VALUE")], "Four paid high-value orders in this set")),
    (37, "cond-decision-flow", "custom", c_cond),
    (38, "switch-decision-flow", "custom", c_switch),
    (39, "ifnull-handling", "pair", (("Field present", "Use shippingFee"), ("Missing or null", "Decimal128 0.00"), "O6201, O6202, O6304 omit shippingFee")),
    (40, "type-conversion-flow", "hflow", ([("Source value", None), ("Type check", None), ("$toDecimal", None), ("Normalized", "analytics")], "Prefer storing consistent types")),
    (41, "group-stage", "hflow", ([("Many documents", None), ("Shared key", "_id"), ("One summary", "per group")], "Original fields are not kept automatically")),
    (42, "group-id", "table", (["_id", "Meaning"], [('"$category"', "One group per category"), ("null", "One group for all documents"), ("{ payment, fulfillment }", "One group per pair")])),
    (43, "group-all-documents", "pair", (("_id: null", "One bucket"), ("One document", "totalRevenue, orderCount"), "Whole-collection summary")),
    (44, "group-by-one-field", "hflow", ([("Products", None), ("_id: $category", None), ("LAPTOP, SHOE…", "one doc each")], "Active filter first — L190 is inactive")),
    (45, "group-by-multiple-fields", "pair", (("Compound _id", "payment + fulfillment"), ("Each unique pair", "one output document"), "PAID + SHIPPED is a high-revenue cell")),
    (46, "group-input-output-shape", "pair", (("Detailed orders", "many fields"), ("Summary docs", "key + accumulators"), "You invent new documents")),
    (47, "accumulator-operators", "table", (["Accumulator", "Use"], [("$sum / $avg", "Totals, counts, averages"), ("$min / $max", "Range"), ("$first / $last", "Preserve a value"), ("$push / $addToSet", "Collect arrays")])),
    (48, "counting-with-sum-1", "pair", (("$sum: 1", "Each doc adds one"), ("$sum: \"$total\"", "Adds the field"), "Both are $sum — different inputs")),
    (49, "summing-numeric-values", "hflow", ([("Order totals", "Decimal128"), ("$sum", None), ("Revenue by status", None)], "Do not mix Double and Decimal128")),
    (50, "average-calculation", "hflow", ([("Prices in group", None), ("$avg", None), ("averagePrice", "per category")], "Compatible numeric types only")),
    (51, "min-and-max-values", "trio", ([("$min price", "lowest"), ("$max price", "highest"), ("Category range", "both")], "LAPTOP range is wide on this catalog")),
    (52, "first-last-with-sorting", "vflow", ([("$sort first", "define order"), ("$group", "$first / $last"), ("Deterministic", "only if sorted")], "")),
    (53, "collecting-with-push", "pair", (("$push: \"$name\"", "Keeps duplicates"), ("Output array", "all values in group"), "Order follows grouping encounter unless sorted")),
    (54, "collecting-with-addtoset", "pair", (("$addToSet", "Unique values"), ("$addToSet: \"$tags\"", "Arrays of tag arrays"), "Flatten first for unique tag strings")),
    (55, "fields-lost-during-grouping", "pair", (("Before $group", "sku, name, price…"), ("After $group", "Only _id + accumulators"), "Preserve with $first, $push, or $addToSet")),
    (56, "grouped-sales-summary", "hflow", ([("Paid orders", None), ("$group", "status or month"), ("count · revenue · AOV", None)], "Lab 5.3 and Lab 5.6")),
    (57, "sort-stage", "pair", (("Ascending 1", "oldest / cheapest"), ("Descending -1", "highest first"), "Add a tiebreaker for stable results")),
    (58, "single-vs-multi-field-sort", "pair", (("One key", "{ revenue: -1 }"), ("Primary + secondary", "{ revenue: -1, sku: 1 }"), "Ties need a unique field")),
    (59, "deterministic-sorting", "hflow", ([("Business metric", "totalSpent"), ("Tiebreaker", "customerNumber"), ("Stable order", "repeatable demo")], "")),
    (60, "limit-stage", "pair", (("$limit: 5", "Keep five"), ("After $sort", "The true top five"), "Top-N pattern")),
    (61, "skip-stage", "pair", (("$skip: 10", "Bypass ten"), ("Then $limit", "Page window"), "Large skips are inefficient")),
    (62, "top-n-pattern", "vflow", ([("$group", "Compute the metric"), ("$sort", "Highest first"), ("$limit", "Keep N")], "")),
    (63, "sort-must-precede-limit", "pair", (("Sort then limit", "Correct top-N"), ("Limit then sort", "Wrong five documents"), "Exercise 5.1 and 5.11")),
    (64, "count-stage", "pair", (("$count: \"paidOrderCount\"", "One named field"), ("{ paidOrderCount: 13 }", "One document"), "After a filter, not instead of $sum in $group")),
    (65, "sortbycount-stage", "pair", (("$sortByCount: \"$category\"", "One stage"), ("$group + $sort", "Same idea by hand"), "Sugar for frequency ranking")),
    (66, "aggregation-pagination", "hflow", ([("$sort", "stable key"), ("$skip", "offset"), ("$limit", "page size")], "Prefer range paging for deep pages")),
    (67, "array-processing-overview", "pair", (("Keep one document", "$filter $map"), ("One doc per element", "$unwind"), "Choose based on the report grain")),
    (68, "unwind-stage", "custom", c_unwind),
    (69, "before-after-unwind", "custom", c_unwind),
    (70, "document-multiplication", "pair", (("1 order, 3 items", "input"), ("3 pipeline docs", "after $unwind"), "Counts follow array lengths")),
    (71, "preserving-empty-arrays", "pair", (("Default unwind", "Empty/null dropped"), ("preserveNullAndEmptyArrays", "Parent continues"), "Use when the parent still matters")),
    (72, "unwind-array-index", "custom", c_index_pos),
    (73, "filter-array-elements", "pair", (("$filter", "Keep matching elements"), ("Still one document", "Array shrinks in place"), "$$item is the current element")),
    (74, "filter-vs-unwind", "pair", (("$filter", "Stay on the order"), ("$unwind", "One row per item"), "Totals by SKU need unwind")),
    (75, "map-array-elements", "hflow", ([("items[]", None), ("$map", "$$item"), ("New array", "sku, qty only")], "Transform without exploding")),
    (76, "unwind-calculate-group", "hflow", ([("Orders", "paid"), ("$unwind", "items"), ("Line revenue", None), ("$group SKU", "rank")], "Demo 5.5 and Lab 5.4")),
    (77, "unwind-and-reassemble", "hflow", ([("Document", None), ("$unwind", None), ("Modify", None), ("$group + $push", "array back")], "Rebuild a cleaned array")),
    (78, "order-item-revenue-flow", "hflow", ([("qty × price", "per item"), ("$sum", "by SKU"), ("Product revenue", "L110 leads")], "Do not $sum order total after unwind")),
    (79, "lookup-stage", "custom", c_lookup),
    (80, "local-foreign-mapping", "pair", (("orders.customerId", "localField"), ("customers._id", "foreignField"), "Types must match — ObjectId to ObjectId")),
    (81, "orders-to-customers-lookup", "hflow", ([("Order", None), ("$lookup", "customers"), ("customer: [ … ]", "array")], "Names are not on the order document")),
    (82, "lookup-result-is-array", "trio", ([("0 matches", "[]"), ("1 match", "[ doc ]"), ("N matches", "[ … ]")], "Never treat as as an object")),
    (83, "lookup-then-unwind", "hflow", ([("customer: [ { } ]", "array"), ("$unwind", None), ("customer: { }", "object")], "Plain unwind drops empty arrays")),
    (84, "join-unwind-project", "vflow", ([("$lookup", "as: customer"), ("$unwind", "optional preserve"), ("$project", "readable fields")], "")),
    (85, "matched-vs-unmatched-lookup", "pair", (("Most orders", "customer array length 1"), ("O6499", "empty array"), "preserveNullAndEmptyArrays keeps O6499")),
    (86, "lookup-type-matching", "pair", (("ObjectId = ObjectId", "Match"), ("ObjectId vs string", "Empty array"), "Wrong type looks like a missing customer")),
    (87, "embedding-vs-lookup", "pair", (("Embedded snapshot", "Already on the order"), ("$lookup", "Fetch related collection"), "Module 3 chose the model; today we join names")),
    (88, "lookup-performance", "four", ([("Input count", "How many locals"), ("Foreign index", "On foreignField"), ("Match count", "Array size"), ("Joined size", "Fields returned")])),
    (89, "pipeline-lookup", "vflow", ([("let variables", "$$orderId"), ("Foreign pipeline", "$match $project"), ("Slim result", "only needed fields")], "Subpipeline lookup when equality is not enough")),
    (90, "replace-root", "pair", (("Nested customer", "inside the order"), ("$replaceRoot", "Customer becomes the doc"), "Parent fields disappear")),
    (91, "replace-with", "pair", (("$replaceWith", "Replace with expression"), ("$mergeObjects", "Keep selected parent fields"), "Safer than a bare replace")),
    (92, "merge-objects", "hflow", ([("customer fields", None), ("+", "orderTotal"), ("One document", None)], "Explicit merge is the only way to keep both")),
    (93, "root-replacement-risk", "pair", (("Forgotten merge", "Lost orderNumber"), ("$mergeObjects", "Keep what you need"), "Demo carefully — easy to drop totals")),
    (94, "bucket-stage", "custom", c_boundary),
    (95, "product-price-bands", "hflow", ([("< 50", "5 products"), ("50–100", "2"), ("100–500", "3"), ("500–2000", "2")], "Includes inactive L190 in 100–500")),
    (96, "bucket-boundary-behavior", "custom", c_boundary),
    (97, "default-bucket", "pair", (("Inside boundaries", "Named ranges"), ("Outside", "default: Other"), "None land in Other on this catalog")),
    (98, "bucket-metrics", "trio", ([("productCount", "$sum: 1"), ("averagePrice", "$avg"), ("productNames", "$push")], "output: { … } on $bucket")),
    (99, "bucketauto-stage", "pair", (("$bucketAuto", "buckets: 4"), ("MongoDB chooses", "Approximate edges"), "Exploratory — not business bands")),
    (100, "bucket-vs-bucketauto", "pair", (("$bucket", "You name edges"), ("$bucketAuto", "Engine names edges"), "Reports use $bucket")),
    (101, "facet-stage", "custom", c_facet),
    (102, "multi-metric-facet", "four", ([("Revenue", "$sum total"), ("Order count", "$sum: 1"), ("Top customers", "group sort limit"), ("By status", "$group")])),
    (103, "facet-input-sharing", "hflow", ([("Paid $match", "once"), ("Same docs", "every branch"), ("Independent", "sub-pipelines")], "Filter before $facet when all branches agree")),
    (104, "facet-output-structure", "pair", (("One document", "not twelve"), ("Each key is an array", "even a single total"), "API / report shape — not a UI widget")),
    (105, "ecommerce-executive-summary", "four", ([("Revenue", "paid"), ("Top products", "unwind"), ("Top customers", "group"), ("Fulfillment", "status")])),
    (106, "pagination-with-facet", "pair", (("Page branch", "$sort skip limit"), ("Count branch", "$count"), "One round trip for page + total")),
    (107, "date-based-reporting", "hflow", ([("Timestamp", "createdAt"), ("Period key", "%Y-%m"), ("$group", None), ("Chronological", "$sort")], "")),
    (108, "daily-sales", "hflow", ([("createdAt", None), ("%Y-%m-%d", None), ("Per day", "count + revenue")], "Use $dateTrunc unit: day")),
    (109, "monthly-sales", "hflow", ([("Paid orders", None), ("2026-07 · 08 · 09", None), ("Three rows", "Lab 5.6")], "YYYY-MM strings sort in order")),
    (110, "yearly-sales", "hflow", ([("Monthly groups", None), ("$year", None), ("Annual totals", None)], "Or $dateTrunc unit: year")),
    (111, "date-trunc", "pair", (("$dateTrunc", "Align to day/week/month"), ("Returns a Date", "Not a string"), "$dateToString is easier to read in mongosh")),
    (112, "timezone-aware-reporting", "pair", (("UTC stored", "createdAt"), ("timezone option", "America/Toronto"), "Production reports must name a zone")),
    (113, "date-range-then-period", "vflow", ([("$match createdAt", "range"), ("$set month", None), ("$group by month", None)], "Filter the window before grouping")),
    (114, "sales-summary-pipeline", "vflow", ([("$match paid", None), ("$set period", None), ("$group metrics", None), ("$sort chronological", None)], "")),
    (115, "product-performance-pipeline", "vflow", ([("$match paid", None), ("$unwind items", None), ("Line revenue", None), ("$group SKU · $sort · $limit", None)], "")),
    (116, "customer-activity-pipeline", "vflow", ([("$match paid", None), ("$group customerId", None), ("$lookup profile", None), ("$sort spending", None)], "")),
    (117, "revenue-by-fulfillment", "hflow", ([("NEW", None), ("PROCESSING", None), ("SHIPPED", "highest $"), ("DELIVERED", None)], "Paid only — PENDING excluded")),
    (118, "average-order-value", "hflow", ([("Paid totals", None), ("$sum / $sum:1", None), ("AOV", "$avg total")], "Or divide after grouping")),
    (119, "top-customers-by-spending", "vflow", ([("$group customerId", "spent"), ("$sort -1", None), ("$limit", None), ("$lookup name", "after group")], "")),
    (120, "top-products-by-units", "hflow", ([("$unwind", None), ("$sum quantity", None), ("$sort units", None), ("A410 among leaders", "4 units")], "")),
    (121, "top-products-by-revenue", "hflow", ([("qty × price", None), ("$group SKU", None), ("L110 first", "3799.98")], "Two units at 1899.99 beat two L100s")),
    (122, "product-category-summary", "hflow", ([("Active products", None), ("$group category", None), ("count avg min max", None), ("$sort avg", None)], "Lab 5.2")),
    (123, "review-rating-summary", "hflow", ([("reviews", None), ("$group sku", None), ("$avg rating", None), ("$sum: 1", "reviewCount")], "Separate collection keeps products bounded")),
    (124, "monthly-executive-report", "vflow", ([("Date $match", None), ("$facet", "several branches"), ("Month · products · customers · status", None)], "Lab 5.10 and Exercise 5.13")),
    (125, "optimization-overview", "hflow", ([("Correctness", "first"), ("Filter", "early"), ("Reduce", "docs/fields"), ("Index", "Module 6"), ("Explain", "plan shape")], "")),
    (126, "early-vs-late-match", "pair", (("Early $match", "Fewer docs later"), ("Late $match", "Processes then discards"), "Lab 5.9")),
    (127, "index-supported-match", "pair", (("IXSCAN", "Keys from the index"), ("COLLSCAN", "Every document"), "Helps when $match is first and selective")),
    (128, "index-supported-sorting", "pair", (("Sort from index", "No in-memory sort"), ("Blocking sort", "Must collect then order"), "Compound prefix must match sort keys")),
    (129, "compound-index-match-sort", "hflow", ([("Equality", "paymentStatus"), ("Sort field", "createdAt"), ("One index", "{ status: 1, createdAt: -1 }")], "ESR: equality, sort, range")),
    (130, "data-volume-reduction", "hflow", ([("17 orders", "full docs"), ("13 paid", "filter"), ("Summaries", "tiny"), ("Top 5", "output")], "Volume and size both matter")),
    (131, "unwind-explosion-risk", "pair", (("Small arrays", "2–3 items"), ("Huge arrays", "N× documents"), "Control unwind; filter first")),
    (132, "lookup-cost-factors", "four", ([("Local count", "after $match"), ("Foreign index", "required"), ("Matches each", "array length"), ("Projected fields", "keep small")])),
    (133, "explain-plan-overview", "vflow", ([("Pipeline", None), ("Query planner", None), ("Winning plan", None), ("executionStats", None)], "")),
    (134, "collscan-vs-ixscan", "pair", (("COLLSCAN", "Examine every doc"), ("IXSCAN", "Navigate the index"), "Seventeen docs will not look fast — read the shape")),
    (135, "examined-vs-returned", "pair", (("Documents examined", "Work done"), ("Documents returned", "Result size"), "Examined >> returned means a weak filter or missing index")),
    (136, "blocking-vs-streaming", "pair", (("Streaming", "$match $project $limit*"), ("Blocking", "$group $sort $facet"), "*$limit streams only after a sort it can skip")),
    (137, "optimization-checklist", "table", (["Practice", "Why"], [("Filter early", "Fewer documents later"), ("Index match/sort", "Module 6"), ("Control $unwind", "Arrays multiply rows"), ("Delay $lookup", "Join survivors only")])),
    (138, "troubleshooting-workflow", "vflow", ([("Sample source doc", None), ("Run stage 1", None), ("Add one; inspect shape", None), ("Manual sample then explain()", None)], "")),
    (139, "missing-dollar-reference", "pair", (("_id: \"items.sku\"", "Literal string group"), ("_id: \"$items.sku\"", "Field value"), "Without $ you group by one constant")),
    (140, "wrong-stage-order", "pair", (("Limit before sort", "Wrong top-N"), ("Group before unwind", "Cannot total SKUs"), "Order is meaning")),
    (141, "incorrect-group-key", "pair", (("Grouped on sku", "Missing $items."), ("One unexpected group", "or null _id"), "Check the path on a sample doc")),
    (142, "fields-lost-after-group", "pair", (("Wanted name", "Not in output"), ("Forgot $first", "Must accumulate"), "Same as diagram 55 — common lab bug")),
    (143, "numeric-type-mismatch", "table", (["Type", "Risk"], [("Double 1000", "Misses Decimal128 totals"), ("String \"49.99\"", "No arithmetic"), ("Decimal128", "Correct money")])),
    (144, "null-calculation-inputs", "pair", (("$add with missing field", "Result null"), ("$ifNull first", "Safe total"), "O6201 is the teaching order")),
    (145, "empty-lookup-result", "four", ([("Wrong collection", "from:"), ("Wrong field", "local/foreign"), ("Wrong type", "ObjectId vs string"), ("No foreign doc", "O6499")])),
    (146, "unexpected-multiplication", "pair", (("Expected 13 paid", None), ("Got 20+ rows", "$unwind items"), "Count after unwind is line count")),
    (147, "double-counting-after-unwind", "pair", (("$sum: \"$total\"", "Repeats order total"), ("$sum lineRevenue", "Correct product $"), "Exercise 5.12’s inefficient pipeline")),
    (148, "manual-metric-validation", "hflow", ([("Small sample", "July O6101–03"), ("Hand total", None), ("Pipeline", None), ("Match?", "Lab habit")], "")),
    (149, "ex-5-1-arrange-pipeline", "vflow", ([("1 $match", "Paid"), ("2 $unwind", "Items"), ("3 $set", "Line $"), ("4 $group", "SKU"), ("5 $sort + $limit", "Top 5")], "")),
    (150, "ex-5-2-build-match", "four", ([("PAID", "13 docs"), ("High-value", "4 orders"), ("Categories", "LAPTOP/ACCESSORY"), ("Provinces", "ON / QC")])),
    (151, "ex-5-3-reshape-project", "pair", (("Operational product", "sku name price"), ("Report", "productCode / nested"), "$ prefix and _id: 0")),
    (152, "ex-5-4-calculated-fields", "four", ([("Line $", "qty × price"), ("Shipping-safe", "$ifNull"), ("Full name", "$concat"), ("Month", "%Y-%m")])),
    (153, "ex-5-5-group-calculate", "hflow", ([("Active", "$match"), ("Category", "$group"), ("count avg min max", None), ("$sort avg", None)], "")),
    (154, "ex-5-6-multi-dimension", "pair", (("paymentStatus", None), ("fulfillmentStatus", None), "Compound _id — one doc per pair")),
    (155, "ex-5-7-array-analysis", "hflow", ([("Paid", None), ("$unwind", None), ("By SKU", "units + $"), ("L110 first", None)], "")),
    (156, "ex-5-8-top-n", "vflow", ([("$group", "metric"), ("$sort -1", None), ("$limit N", None)], "")),
    (157, "ex-5-9-join-collections", "hflow", ([("orders", "customerId"), ("$lookup", None), ("customers._id", None), ("O6499 empty", "preserve")], "")),
    (158, "ex-5-10-facet-design", "custom", c_facet),
    (159, "ex-5-11-broken-stage", "table", (["Defect", "Symptom"], [("Limit before sort", "Wrong top-N"), ("Missing $", "Literal group key"), ("No $unwind", "Cannot total items"), ("Lookup as object", "Empty projection")])),
    (160, "ex-5-12-optimize", "vflow", ([("Match paid first", None), ("Group then lookup", None), ("Do not unwind to sum totals", None)], "")),
    (161, "lab-5-1-verification", "hflow", ([("Counts", "6 / 12 / 17 / 6"), ("Types", "Decimal128 Date"), ("Arrays", "items"), ("13 paid", None)], "")),
    (162, "lab-5-2-product-summary", "hflow", ([("Active", None), ("$group category", None), ("Metrics", None), ("Rename category", None)], "")),
    (163, "lab-5-3-order-revenue", "hflow", ([("PAID", None), ("By fulfillment", None), ("count · $ · AOV", None), ("SHIPPED leads", None)], "")),
    (164, "lab-5-4-product-sales", "hflow", ([("Unwind", None), ("Line $", None), ("Top 5 SKU", None), ("L110 · L100 · A500", None)], "")),
    (165, "lab-5-5-customer-summary", "vflow", ([("Group customerId", None), ("$lookup names", None), ("C101 first", "Aisha Khan")], "")),
    (166, "lab-5-6-date-sales", "hflow", ([("%Y-%m", None), ("Three months", None), ("Chronological", "07 then 08 then 09")], "")),
    (167, "lab-5-7-price-bands", "custom", c_boundary),
    (168, "lab-5-8-multi-metric", "four", ([("13 paid", "totals"), ("By status", None), ("Top 3", "customers/products"), ("High-value 4", None)])),
    (169, "lab-5-9-performance", "hflow", ([("Late $match", "explain"), ("Early $match", "compare"), ("Index name", "Module 6")], "Plan shape, not milliseconds")),
    (170, "lab-5-10-integrated", "four", ([("Month", None), ("Revenue / AOV", None), ("Units + top SKU", None), ("By fulfillment", None)])),
    (171, "practical-challenge", "four", ([("Date range", "paid"), ("By month", None), ("By product", "unwind"), ("Top customers", "$lookup")])),
]


def _render(kind: str, payload, mid: str) -> str:
    if kind == "pair":
        left, right, cap = payload
        return pair(left, right, cap, mid)
    if kind == "trio":
        items, cap = payload
        return trio(items, cap, mid)
    if kind == "hflow":
        items, cap = payload
        return hflow(items, cap, mid)
    if kind == "vflow":
        items, cap = payload
        return vflow(items, cap, mid)
    if kind == "table":
        headers, rows = payload
        return table_d(headers, rows, mid)
    if kind == "four":
        items = payload[0] if isinstance(payload, tuple) and len(payload) == 1 else payload
        cap = ""
        if isinstance(payload, tuple) and len(payload) == 2 and isinstance(payload[1], str):
            items, cap = payload
        return four(list(items), cap, mid)
    if kind == "custom":
        return payload(mid)
    raise ValueError(kind)


def _filename(n: int, slug: str) -> str:
    return f"{n:03d}-{slug}.svg"


DIAGRAMS: dict[str, callable] = {}
for _n, _slug, _kind, _payload in CATALOG:
    _mid = f"m{_n:03d}"
    DIAGRAMS[_filename(_n, _slug)] = lambda kind=_kind, payload=_payload, mid=_mid: _render(kind, payload, mid)


# Backward-compatible names used by the first Module 5 slide pass
ALIASES: dict[str, str] = {
    "01-ops-vs-aggregation.svg": "001-operational-query-vs-aggregation.svg",
    "02-pipeline-flow.svg": "002-aggregation-pipeline-overview.svg",
    "03-pipeline-anatomy.svg": "003-aggregation-pipeline-anatomy.svg",
    "04-documents-through-pipeline.svg": "007-document-count-and-shape.svg",
    "05-stage-order.svg": "006-stage-order-matters.svg",
    "06-sample-dataset.svg": "009-analytical-dataset.svg",
    "07-match-stage.svg": "011-match-stage.svg",
    "08-project-stage.svg": "019-project-stage.svg",
    "09-set-vs-project.svg": "025-project-vs-set.svg",
    "10-expressions.svg": "029-expression-categories.svg",
    "11-group-stage.svg": "041-group-stage.svg",
    "12-group-id.svg": "042-group-id.svg",
    "13-accumulators.svg": "047-accumulator-operators.svg",
    "14-top-n-pattern.svg": "062-top-n-pattern.svg",
    "15-unwind.svg": "068-unwind-stage.svg",
    "16-unwind-group-reassemble.svg": "076-unwind-calculate-group.svg",
    "17-lookup.svg": "079-lookup-stage.svg",
    "18-local-foreign.svg": "080-local-foreign-mapping.svg",
    "19-bucket.svg": "094-bucket-stage.svg",
    "20-facet.svg": "101-facet-stage.svg",
    "21-date-reporting.svg": "107-date-based-reporting.svg",
    "22-sales-summary.svg": "114-sales-summary-pipeline.svg",
    "23-product-performance.svg": "115-product-performance-pipeline.svg",
    "24-customer-activity.svg": "116-customer-activity-pipeline.svg",
    "25-dev-workflow.svg": "010-development-workflow.svg",
    "26-optimization.svg": "125-optimization-overview.svg",
    "27-match-placement.svg": "013-source-vs-group-match.svg",
    "28-index-use.svg": "127-index-supported-match.svg",
    "29-common-mistakes.svg": "159-ex-5-11-broken-stage.svg",
    "30-troubleshooting.svg": "138-troubleshooting-workflow.svg",
    "31-module-5-concept-map.svg": "000-module-5-concept-map.svg",
    "32-demo-incremental.svg": "010-development-workflow.svg",
    "33-ex-5-1-stage-order.svg": "149-ex-5-1-arrange-pipeline.svg",
    "34-lab-product-summary.svg": "162-lab-5-2-product-summary.svg",
    "35-lab-product-sales.svg": "164-lab-5-4-product-sales.svg",
    "36-practical-challenge.svg": "171-practical-challenge.svg",
    "37-day2-agg-path.svg": "008-business-question-to-pipeline.svg",
    "38-null-handling.svg": "039-ifnull-handling.svg",
    "39-type-conversion.svg": "040-type-conversion-flow.svg",
    "40-replace-root.svg": "090-replace-root.svg",
    "41-filter-vs-unwind.svg": "074-filter-vs-unwind.svg",
    "42-count-sortbycount.svg": "065-sortbycount-stage.svg",
}


def write_all() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        path = ASSETS / name
        path.write_text(fn(), encoding="utf-8")
    (ASSETS / "000-module-5-concept-map.svg").write_text(c_concept("m000"), encoding="utf-8")
    for alias, target in ALIASES.items():
        src = ASSETS / target
        dst = ASSETS / alias
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Wrote {len(DIAGRAMS)} numbered diagrams + concept map + {len(ALIASES)} aliases")
    return len(DIAGRAMS)


if __name__ == "__main__":
    n = write_all()
    print(f"Done. {n} catalog diagrams.")

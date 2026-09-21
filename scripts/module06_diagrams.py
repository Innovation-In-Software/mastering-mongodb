"""Module 6 diagrams — Indexing and Query Performance.

Generates the full 185-diagram catalog (plus the 20 essential classroom set).

    python scripts/module06_diagrams.py
"""
from __future__ import annotations

import html
from pathlib import Path

from marp_svg_common import BORDER, FONT, HEADER_BG, MONO, MUTED, PANEL, RED, TEXT

BG_BOX = "#ffffff"
ASSETS = Path(__file__).resolve().parent.parent / "slides" / "assets" / "module-06"
W = 920

ESSENTIAL = {
    1, 2, 3, 7, 13, 19, 20, 21, 25, 24,
    39, 43, 47, 48, 72, 92, 98, 101, 131, 161,
}


def _esc(text: str) -> str:
    return html.escape(text, quote=True)


def _svg(height: int, body: str, marker_id: str) -> str:
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


def _box(x, y, w, h, title, sub=None, *, header=False, fs=17, sub_fs=13) -> str:
    fill = HEADER_BG if header else BG_BOX
    title_y = y + (h / 2 + fs * 0.35 if not sub else h * 0.36)
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{RED}" stroke-width="2"/>',
        f'<text x="{x + w / 2}" y="{title_y:.1f}" text-anchor="middle" font-family="{FONT}" font-size="{fs}" fill="{RED if header else TEXT}">{_esc(title)}</text>',
    ]
    if sub:
        parts.append(
            f'<text x="{x + w / 2}" y="{y + h * 0.74:.1f}" text-anchor="middle" font-family="{FONT}" font-size="{sub_fs}" fill="{MUTED}">{_esc(sub)}</text>'
        )
    return "\n".join(parts)


def _label(x, y, text, *, fs=15, fill=MUTED) -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="{fs}" fill="{fill}">{_esc(text)}</text>'
    )


def _arrow(x1, y1, x2, y2, mid: str) -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{RED}" '
        f'stroke-width="2" marker-end="url(#{mid})"/>'
    )


def _vflow(boxes, mid: str, *, x=200, y=16, w=520, h=48, gap=16) -> tuple[str, int]:
    parts: list[str] = []
    cy = y
    for i, item in enumerate(boxes):
        title, sub = item if isinstance(item, tuple) else (item, None)
        parts.append(_box(x, cy, w, h, title, sub, fs=16 if sub else 17, sub_fs=13))
        if i < len(boxes) - 1:
            parts.append(_arrow(x + w / 2, cy + h, x + w / 2, cy + h + gap - 4, mid))
        cy += h + gap
    return "\n".join(parts), cy + 8


def _hflow(boxes, mid: str, *, y=40, h=100, gap=24, x0=20) -> str:
    parts: list[str] = []
    n = len(boxes)
    usable = W - 40 - (n - 1) * gap
    box_w = max(120, usable // n)
    x = x0
    for i, item in enumerate(boxes):
        title, sub = item if isinstance(item, tuple) else (item, None)
        parts.append(_box(x, y, box_w, h, title, sub, fs=15, sub_fs=12))
        if i < n - 1:
            parts.append(_arrow(x + box_w, y + h / 2, x + box_w + gap - 4, y + h / 2, mid))
        x += box_w + gap
    return "\n".join(parts)


def _two(left, right, mid: str, *, caption=None) -> tuple[str, int]:
    lt, ls = left if isinstance(left, tuple) else (left, None)
    rt, rs = right if isinstance(right, tuple) else (right, None)
    parts = [
        _box(30, 24, 400, 150, lt, ls, fs=18, sub_fs=13),
        _box(490, 24, 400, 150, rt, rs, fs=18, sub_fs=13),
    ]
    h = 200
    if caption:
        parts.append(_label(460, 204, caption, fs=14))
        h = 230
    return "\n".join(parts), h


def _three(cells, mid: str, *, caption=None, y=28, h=110) -> tuple[str, int]:
    parts = [_hflow(cells, mid, y=y, h=h, gap=28)]
    height = y + h + 16
    if caption:
        parts.append(_label(460, height + 8, caption, fs=14))
        height += 28
    return "\n".join(parts), height + 10


def _table(headers, rows, *, row_h=44, header_h=42, fs=14) -> tuple[str, int]:
    n = len(headers)
    leftover = W - 40
    col_ws = [leftover // n] * n
    col_ws[-1] = leftover - sum(col_ws[:-1])
    parts: list[str] = []
    x = 20
    y0 = 14
    for i, h in enumerate(headers):
        parts.append(_box(x, y0, col_ws[i], header_h, h, header=True, fs=fs))
        x += col_ws[i]
    for r, row in enumerate(rows):
        y = y0 + header_h + 6 + r * (row_h + 4)
        x = 20
        for i, cell in enumerate(row):
            parts.append(_box(x, y, col_ws[i], row_h, cell, fs=fs))
            x += col_ws[i]
    height = y0 + header_h + 6 + len(rows) * (row_h + 4) + 8
    return "\n".join(parts), height


def _grid(cells, *, cols=2, caption=None) -> tuple[str, int]:
    parts: list[str] = []
    gap = 16
    box_w = (W - 40 - (cols - 1) * gap) // cols
    box_h = 90
    for i, item in enumerate(cells):
        title, sub = item if isinstance(item, tuple) else (item, None)
        col = i % cols
        row = i // cols
        x = 20 + col * (box_w + gap)
        y = 18 + row * (box_h + gap)
        parts.append(_box(x, y, box_w, box_h, title, sub, fs=15, sub_fs=12))
    rows = (len(cells) + cols - 1) // cols
    height = 18 + rows * (box_h + gap) + 6
    if caption:
        parts.append(_label(460, height + 6, caption, fs=14))
        height += 24
    return "\n".join(parts), height


def _render(n: int, kind: str, payload, caption: str | None) -> str:
    mid = f"m{n:03d}"
    if kind == "v":
        body, h = _vflow(payload, mid)
        if caption:
            body += "\n" + _label(460, h + 4, caption, fs=14)
            h += 24
        return _svg(max(h + 8, 180), body, mid)
    if kind == "h":
        body = _hflow(payload, mid)
        h = 170
        if caption:
            body += "\n" + _label(460, 162, caption, fs=14)
            h = 190
        return _svg(h, body, mid)
    if kind == "2":
        left, right = payload
        body, h = _two(left, right, mid, caption=caption)
        return _svg(h, body, mid)
    if kind == "3":
        body, h = _three(payload, mid, caption=caption)
        return _svg(h, body, mid)
    if kind == "t":
        headers, rows = payload
        body, h = _table(headers, rows)
        if caption:
            body += "\n" + _label(460, h + 2, caption, fs=14)
            h += 22
        return _svg(h, body, mid)
    if kind == "g":
        body, h = _grid(payload, cols=2, caption=caption)
        return _svg(h, body, mid)
    if kind == "g3":
        body, h = _grid(payload, cols=3, caption=caption)
        return _svg(h, body, mid)
    raise ValueError(f"Unknown kind {kind} for diagram {n}")


def fname(n: int, slug: str) -> str:
    return f"{n:03d}-{slug}.svg"


# (n, slug, kind, payload, caption)
CATALOG: list[tuple] = [
    # --- Core indexing concepts ---
    (1, "query-without-index", "v",
     [("Query", "category: ACCESSORY"), ("Document 1", "check"), ("Document 2", "check"),
      ("Document N", "check")], "No suitable index — inspect every document"),
    (2, "query-with-index", "v",
     [("Query", "category: ACCESSORY"), ("Index keys", "ACCESSORY range"),
      ("Candidate refs", "matching products"), ("Fetch matches", "return results")], None),
    (3, "collscan-vs-ixscan", "2",
     (("COLLSCAN", "Doc 1 → 2 → … → N"), ("IXSCAN", "Keys → selected documents")),
     "IXSCAN is not automatically efficient"),
    (4, "what-is-an-index", "t",
     (["Index key", "Document"],
      [("ACCESSORY | 29.99", "Document A"), ("ACCESSORY | 49.99", "Document B"),
       ("BOOK | 59.99", "Document C"), ("LAPTOP | 1299.99", "Document D")]), None),
    (5, "conceptual-index-structure", "3",
     [("Equality lookup", "Jump to a value"), ("Range traversal", "Walk adjacent keys"),
      ("Sorted retrieval", "Follow index order")], "Keep internals conceptual"),
    (6, "index-lookup-flow", "h",
     [("Query", None), ("Index search", None), ("Doc refs", None), ("Matches", None), ("Results", None)], None),
    (7, "index-benefits", "t",
     (["Benefit", "Helps"],
      [("Filter / range", "Find matching keys"), ("Sort / page", "Avoid extra SORT"),
       ("Uniqueness / TTL", "Integrity and expiry"), ("$lookup / $match", "Joins and early stages")]), None),
    (8, "index-costs", "t",
     (["Cost", "Effect"],
      [("Storage + memory", "Extra data to keep hot"), ("Insert / update / delete", "Each write may touch many indexes"),
       ("Backup / replication", "More bytes to copy"), ("Operations", "More objects to hide or drop")]), None),
    (9, "read-vs-write-cost", "2",
     (("Faster selected reads", "Seek instead of scan"), ("Slower writes", "Insert, update, delete tax")),
     "Index real query patterns, not every field"),
    (10, "index-lifecycle", "h",
     [("Identify", None), ("Design", None), ("Create", None), ("Measure", None), ("Revise", None)], None),
    # --- Default and single-field ---
    (11, "default-id-index", "2",
     (("Every _id", "Unique per collection"), ("Storage location", "Fast _id lookup")),
     "Created automatically; cannot normally drop"),
    (12, "business-id-vs-id", "2",
     (("_id index", "ObjectId lookups only"), ("Business key", "SKU · email · orderNumber")),
     "Business identifiers need their own indexes"),
    (13, "single-field-index", "2",
     (("{ category: 1 }", "Ordered key sequence"), ('find({ category: "LAPTOP" })', "Uses that sequence")), None),
    (14, "equality-lookup-sku", "v",
     [('find({ sku: "L100" })', None), ("SKU index key L100", None), ("One product document", None)], None),
    (15, "range-scan-price", "h",
     [("Lower bound", "100.00"), ("Scan price keys", "adjacent entries"), ("Upper bound", "500.00")], None),
    (16, "ascending-vs-descending", "2",
     (("Forward { createdAt: 1 }", "sort createdAt: 1"), ("Reverse traversal", "sort createdAt: -1")),
     "Single-field indexes usually travel both ways"),
    (17, "indexing-nested-field", "v",
     [("Customer document", "contact.email"), ('Index path "contact.email"', "quoted dot notation"),
      ('find({ "contact.email": "aisha@…" })', None)], None),
    (18, "listing-collection-indexes", "g",
     [("_id_", "default unique"), ("idx_products_sku", "single-field"),
      ("idx_category_active_price", "compound"), ("ttl_sessions_expires_at", "specialized")],
     "db.products.getIndexes()"),
    # --- Compound ---
    (19, "compound-index-structure", "v",
     [("category ACCESSORY", "then price 19.99"), ("category ACCESSORY", "then price 49.99"),
      ("category BOOK", "then price 59.99")], "Organized first by one field, then the next"),
    (20, "compound-field-order", "2",
     (("{ category: 1, price: 1 }", "By category, then price"), ("{ price: 1, category: 1 }", "Different prefixes")),
     "These are different indexes"),
    (21, "compound-index-prefixes", "v",
     [("category", "leading field"), ("category + price", "two-field prefix"),
      ("category + price + name", "full key")], None),
    (22, "usable-vs-nonusable-prefixes", "2",
     (("Usable", "Starts with the leading field"), ("Not a prefix", "price-only on a category-first index")), None),
    (23, "one-compound-many-shapes", "g",
     [("category", "prefix"), ("category + active", "prefix"),
      ("category + active + price", "full key"), ("active only", "not a prefix")], None),
    (24, "filter-and-sort-compound", "h",
     [("Equality", "category + active"), ("Ordered walk", "price keys"), ("Sorted results", "no extra SORT")], None),
    (25, "equality-sort-range", "h",
     [("Equality", "customerId"), ("Sort", "createdAt / total"), ("Range", "date or total")],
     "Guideline — validate with explain()"),
    (26, "classifying-esr-fields", "t",
     (["Field", "Role"],
      [("customerId", "Equality"), ("paymentStatus", "Equality"),
       ("createdAt sort", "Sort"), ("total $gte", "Range")]), None),
    (27, "esr-design-flow", "h",
     [("Query shape", None), ("Classify E/S/R", None), ("Arrange fields", None), ("explain()", None)], None),
    (28, "equality-before-range", "v",
     [("Equality", "Narrow to one customer"), ("Range", "Walk that customer's dates")],
     "Do not lead with a wide range"),
    (29, "sort-before-range", "v",
     [("Sort field in the key", "Index already ordered"), ("Then range", "Scan a slice of that order")],
     "Preserves sort support"),
    (30, "alternative-compound-designs", "2",
     (("{ customerId, createdAt }", "History page"), ("{ paymentStatus, createdAt }", "Paid reporting")),
     "Choose by workload, then measure"),
    (31, "compound-product-browsing", "h",
     [("category", "1"), ("active", "1"), ("price", "1")], "Catalog browse + sort by price"),
    (32, "compound-order-history", "h",
     [("customerId", "1"), ("createdAt", "-1")], "Newest orders for one customer"),
    (33, "compound-paid-orders", "h",
     [("paymentStatus", "1"), ("createdAt", "-1")], "Paid reporting by date"),
    (34, "compound-product-reviews", "h",
     [("productId", "1"), ("createdAt", "-1")], "Reviews newest first"),
    (35, "mixed-sort-directions", "2",
     (("{ category: 1, price: -1 }", "Supports that pair"), ("Complete reverse", "{ category: -1, price: 1 }")), None),
    (36, "unsupported-mixed-sort", "2",
     (("Index { category: 1, price: -1 }", None), ("sort category: 1, price: 1", "Extra SORT stage")),
     "Arbitrary mixed directions are not free"),
    # --- Specialized types ---
    (37, "index-types-overview", "g3",
     [("Single-field", None), ("Compound", None), ("Multikey", None),
      ("Unique", None), ("Partial / sparse", None), ("TTL", None),
      ("Text", None), ("Wildcard / geo", None), ("Hashed", None)], None),
    (38, "index-type-selection-map", "t",
     (["Requirement", "Candidate"],
      [("One-field lookup", "Single-field"), ("Filter + sort", "Compound"),
       ("Active subset", "Partial"), ("Expire sessions", "TTL"), ("Nearby stores", "Geospatial")]), None),
    (39, "multikey-index", "2",
     (('tags: ["wireless","accessories"]', "One document"), ("Two index entries", "One per array element")), None),
    (40, "querying-array-multikey", "v",
     [('find({ tags: "technology" })', None), ("Multikey tag entries", None), ("Matching products", "e.g. B300")], None),
    (41, "nested-array-multikey", "v",
     [("addresses[]", "array of documents"), ('Index "addresses.city"', None), ("May be multikey", "one key per city")], None),
    (42, "unique-index", "g",
     [("SKU", "products"), ("customerNumber", "customers"),
      ("orderNumber", "orders"), ("email", "when business requires")], None),
    (43, "unique-enforcement-flow", "h",
     [("Insert request", None), ("Uniqueness check", None), ("Accept", "or E11000 reject")], None),
    (44, "partial-index", "2",
     (("Filter", "active: true"), ("Indexed subset", "Inactive docs omitted")), None),
    (45, "active-products-partial", "2",
     (("Active products", "In the index"), ("L190 inactive", "Outside the index")),
     "Query generally needs active: true"),
    (46, "sparse-index", "2",
     (("Field present", "discountCode indexed"), ("Field missing", "Document omitted")), None),
    (47, "partial-vs-sparse", "2",
     (("Partial", "Explicit filter expression"), ("Sparse", "Indexed field exists")),
     "Prefer partial when you can state the subset"),
    (48, "ttl-index", "h",
     [("Date field", "expiresAt"), ("TTL monitor", "~60s interval"), ("Document removed", "asynchronous")], None),
    (49, "session-expiration-ttl", "v",
     [("Active session", "expiresAt in the future"), ("Timestamp reached", None),
      ("Async cleanup", "not exact-second")], None),
    (50, "text-index", "h",
     [("name / description", "strings"), ("Tokenize words", "language-aware"), ("$text query", None)], None),
    (51, "text-search-flow", "h",
     [("$search terms", "wireless keyboard"), ("Text index", None), ("Matching documents", None)], None),
    (52, "text-vs-advanced-search", "2",
     (("Text index", "Word matching"), ("Dedicated search", "Fuzzy, autocomplete, facets")), None),
    (53, "wildcard-index", "v",
     [("attributes vary by category", "laptop vs shoe vs book"),
      ('{ "attributes.$**": 1 }', None), ("Dynamic paths indexed", "write + storage cost")], None),
    (54, "targeted-vs-wildcard", "2",
     (("Targeted", "Known fields, ESR design"), ("Wildcard", "Unpredictable paths")),
     "Wildcard is not a substitute for query-shape design"),
    (55, "geospatial-index", "2",
     (("GeoJSON Point", "[lng, lat]"), ("2dsphere index", "Distance and containment")), None),
    (56, "nearby-store-search", "h",
     [("User location", None), ("2dsphere", None), ("Nearby stores", None)], None),
    (57, "hashed-index", "v",
     [("tenantId value", None), ("Hash of the value", None), ("Equality distribution", "hashed shard keys")], None),
    (58, "ordered-vs-hashed", "2",
     (("Ordered index", "Range + sort"), ("Hashed index", "Equality only; no range order")), None),
    # --- Filter and sorting ---
    (59, "index-equality-filter", "v",
     [("Exact SKU / orderNumber", None), ("Narrow key range", None), ("Few documents", None)], None),
    (60, "index-range-filter", "h",
     [("Min key", None), ("Consecutive keys", None), ("Max key", None)], None),
    (61, "index-supported-sort", "h",
     [("Index order", None), ("Traverse keys", None), ("Results already sorted", None)], None),
    (62, "in-memory-sort", "v",
     [("Match documents", None), ("Load into memory", None), ("SORT stage", "CPU + memory")], None),
    (63, "index-vs-inmemory-sort", "2",
     (("Index order", "No extra SORT"), ("Blocking SORT", "Index cannot provide order")), None),
    (64, "filter-sort-compatibility", "v",
     [("Predicates", "equality fields in the prefix"), ("Sort fields", "next in the key"),
      ("Compound index", "one scan")], None),
    (65, "sort-direction-compatibility", "2",
     (("Requested sort", "matches index pair"), ("Or complete reverse", "same index")),
     "Mismatched mixtures add SORT"),
    (66, "top-n-with-index", "h",
     [("Ordered IXSCAN", None), ("limit N", "stop early"), ("Top-N results", None)], None),
    (67, "pagination-compound-index", "h",
     [("Equality filter", None), ("Stable sort", None), ("limit page size", None)], None),
    (68, "offset-vs-range-pagination", "2",
     (("skip / offset", "Work grows with page depth"), ("Range after last key", "Continue from last _id/date")), None),
    (69, "prefix-regex-index", "2",
     (('name: /^Mongo/', "Anchored prefix"), ("Ordered string index", "Can narrow keys")), None),
    (70, "unanchored-regex-scan", "2",
     (('name: /Mongo/', "Anywhere in the field"), ("Broader examination", "Often no tight bounds")), None),
    # --- Covered queries ---
    (71, "covered-query-overview", "v",
     [("Filter fields in the index", None), ("Projected fields in the index", None),
      ("No FETCH of full documents", None)], None),
    (72, "covered-vs-noncovered", "2",
     (("Covered", "IXSCAN → projection"), ("Not covered", "IXSCAN → FETCH")), None),
    (73, "filter-fields-covered", "h",
     [("Predicate", "category"), ("Must be indexed", None), ("Else FETCH or COLLSCAN", None)], None),
    (74, "projection-fields-covered", "h",
     [("Returned fields", "name, price"), ("Must be indexed", None), ("tags would FETCH", None)], None),
    (75, "id-coverage-consideration", "2",
     (("_id included (default)", "FETCH unless _id is in the key"), ("{ _id: 0, name: 1, price: 1 }", "Coverage possible")), None),
    (76, "ixscan-projection-vs-fetch", "2",
     (("IXSCAN → projection", "Index-only"), ("IXSCAN → FETCH", "Full documents")), None),
    (77, "covered-product-summary", "v",
     [('find({ category: "BOOK" })', None), ("{ _id: 0, name: 1, price: 1 }", None),
      ("Index { category, price, name }", "Confirm with explain()")], None),
    # --- Selectivity and shapes ---
    (78, "high-vs-low-selectivity", "2",
     (("Higher", "SKU · email · orderNumber"), ("Lower", "active · few statuses")), None),
    (79, "selective-index-lookup", "2",
     (("Small key range", None), ("Small result set", "keys ≈ docs ≈ nReturned")), None),
    (80, "low-selectivity-scan", "2",
     (("Large index slice", "e.g. active: true"), ("Many documents examined", None)), None),
    (81, "selectivity-and-compound", "h",
     [("Low-selectivity status", "poor alone"), ("+ category or customerId", None), ("Useful compound / partial", None)], None),
    (82, "query-shape-anatomy", "g3",
     [("Filter fields", None), ("Operators", None), ("Sort", None),
      ("Projection", None), ("Collation", None), ("Options", None)], None),
    (83, "same-shape-different-values", "2",
     (('category: "ACCESSORY"', None), ('category: "LAPTOP"', None)),
     "Same shape → same index design"),
    (84, "workload-driven-design", "h",
     [("Repeated shapes", None), ("Candidate indexes", None), ("Measured explain()", None)], None),
    (85, "isolated-vs-workload", "2",
     (("One query faster", "Easy to over-index"), ("Whole workload", "Reads + writes + storage")), None),
    # --- Intersection and overlap ---
    (86, "index-intersection", "3",
     [("{ category: 1 }", None), ("{ active: 1 }", None), ("AND query", "May combine")], None),
    (87, "intersection-vs-compound", "2",
     (("Two single-field scans", "Intersection"), ("One compound scan", "More predictable with sort")), None),
    (88, "overlapping-indexes", "v",
     [("{ category: 1 }", "prefix"), ("{ category: 1, price: 1 }", "wider key")],
     "Compound may make the single-field redundant"),
    (89, "potentially-redundant-indexes", "t",
     (["Index", "Note"],
      [("{ category: 1 }", "Prefix of others"), ("{ category, price }", "Overlap"),
       ("{ category, price, name }", "Coverage of name"), ("{ price: 1 }", "Not a category prefix")]), None),
    (90, "redundancy-decision-flow", "h",
     [("Overlap", None), ("Usage", None), ("Hide", None), ("Retain or drop", None)], None),
    (91, "index-coverage-matrix", "t",
     (["Query shape", "Index"],
      [("SKU lookup", "uq_products_sku"), ("Catalog browse", "category+active+price"),
       ("Order history", "customerId+createdAt"), ("Paid report", "paymentStatus+createdAt")]), None),
    # --- Explain plans ---
    (92, "query-planning-flow", "h",
     [("Query", None), ("Candidates", None), ("Trial", None), ("Winning plan", None), ("Execute", None)], None),
    (93, "using-explain", "v",
     [("Query or aggregate", None), ('explain("executionStats")', None),
      ("Planner + examined counts", None)], None),
    (94, "explain-verbosity", "3",
     [("queryPlanner", "Winning + rejected"), ("executionStats", "Keys and docs"),
      ("allPlansExecution", "Candidate race")], "Training default: executionStats"),
    (95, "explain-output-map", "g",
     [("queryPlanner", "parsed query"), ("winningPlan", "chosen stages"),
      ("rejectedPlans", "not chosen"), ("executionStats", "nReturned / examined")], None),
    (96, "winning-and-rejected", "2",
     (("Winning plan", "Selected for this shape"), ("Rejected plans", "Eligible but not chosen")),
     "Rejected ≠ a bad index"),
    (97, "collscan-plan", "h",
     [("COLLSCAN", None), ("Filter", None), ("Returned docs", None)], None),
    (98, "ixscan-fetch-plan", "h",
     [("IXSCAN", "index keys"), ("FETCH", "documents"), ("Projection / result", None)], None),
    (99, "covered-ixscan-plan", "h",
     [("IXSCAN", None), ("Projection", None), ("Result", "no FETCH")], None),
    (100, "explain-before-after", "2",
     (("Before", "COLLSCAN · many docs examined"), ("After", "IXSCAN · keys ≈ returned")), None),
    (101, "keys-docs-returned", "3",
     [("totalKeysExamined", None), ("totalDocsExamined", None), ("nReturned", None)], None),
    (102, "efficient-examination-ratio", "h",
     [("Keys 10", None), ("Docs 10", None), ("Returned 10", None)], "Targeted access"),
    (103, "inefficient-examination-ratio", "2",
     (("Examined 100,000", None), ("Returned 10", None)), "High scan cost — redesign the key"),
    (104, "index-bounds", "2",
     (("Equality bound", 'category: "BOOK"'), ("Range bound", "price $gte / $lte")), None),
    (105, "in-memory-sort-in-plan", "v",
     [("FETCH / IXSCAN", None), ("SORT stage", "blocking"), ("Result", None)], None),
    (106, "index-supported-sort-plan", "h",
     [("IXSCAN in order", None), ("limit / project", None), ("No SORT stage", None)], None),
    (107, "explain-interpretation-workflow", "h",
     [("Winning stage", None), ("Index name", None), ("Examined counts", None), ("Sort?", None)], None),
    # --- Aggregation and lookup ---
    (108, "indexes-in-aggregation", "v",
     [("$match / $sort", "May use an index"), ("Later stages", "$group, $unwind, $facet"),
      ("In-memory after transform", None)], None),
    (109, "early-indexed-match", "h",
     [("Indexed $match", "PAID"), ("Fewer docs", None), ("$group / $unwind", None)], None),
    (110, "agg-with-without-index", "2",
     (("Without", "COLLSCAN into the pipeline"), ("With", "IXSCAN feeds $match/$sort")), None),
    (111, "indexed-sort-before-group", "h",
     [("IXSCAN sort", "createdAt -1"), ("$group", "fulfillmentStatus"), ("Totals", "still in memory")], None),
    (112, "index-support-ends", "v",
     [("Indexed prefix", "$match + $sort"), ("Then transformation", "$group $lookup $facet"),
      ("No index for those stages", None)], None),
    (113, "lookup-foreign-field-index", "2",
     (("localField", "orders.customerId"), ("foreignField indexed", "customers._id")), None),
    (114, "indexed-vs-unindexed-lookup", "2",
     (("Indexed foreign key", "Targeted lookups"), ("Unindexed foreign key", "Repeated scans")), None),
    (115, "orders-to-customers-lookup", "h",
     [("orders.customerId", None), ("$lookup", None), ("customers._id", "already indexed")], None),
    (116, "aggregation-explain-flow", "h",
     [("Cursor / $match", None), ("Index access", None), ("Remaining stages", None)], None),
    # --- Maintenance ---
    (117, "index-write-maintenance", "v",
     [("Document write", None), ("Collection data", None), ("Every affected index", None)], None),
    (118, "insert-with-multiple-indexes", "3",
     [("Document", None), ("_id index", "always"), ("Secondary indexes", "each key")], None),
    (119, "update-indexed-field", "h",
     [("Old index key", "remove"), ("Document update", None), ("New index key", "insert")], None),
    (120, "delete-with-multiple-indexes", "h",
     [("Delete document", None), ("Remove _id key", None), ("Remove secondary keys", None)], None),
    (121, "index-storage-growth", "v",
     [("More documents", None), ("Larger keys / arrays", None), ("Total index size grows", None)], None),
    (122, "index-working-set", "2",
     (("Hot pages in RAM", "Frequent keys"), ("Cold pages on disk", "Latency less predictable")), None),
    (123, "over-indexing-symptoms", "g",
     [("Slow writes", None), ("Storage growth", None), ("Memory pressure", None), ("Many similar indexes", None)], None),
    (124, "index-usage-monitoring", "h",
     [("Workload", None), ("$indexStats", None), ("Retain / redesign", None)],
     "Stats are process-lifetime — not month-end proof"),
    (125, "hidden-index-testing", "h",
     [("Active index", None), ("hideIndex", "planner skips"), ("Observe queries", None), ("unhide or drop", None)], None),
    (126, "hidden-vs-dropped", "2",
     (("Hidden", "Still stored and maintained"), ("Dropped", "Physically removed")),
     "Hide tests the planner, not write cost"),
    (127, "safe-index-removal", "h",
     [("Identify", None), ("Hide", None), ("Monitor", None), ("Remove", None), ("Validate", None)], None),
    (128, "safe-index-creation", "h",
     [("Baseline", None), ("Test", None), ("Build", None), ("Monitor", None), ("Document", None)], None),
    (129, "index-naming-convention", "t",
     (["Name", "Intent"],
      [("idx_orders_customer_created", "Regular query"), ("uq_products_sku", "Unique key"),
       ("ttl_sessions_expires_at", "Expiration"), ("geo_stores_location", "Geospatial")]), None),
    (130, "index-inventory", "t",
     (["Look at", "Question"],
      [("Purpose", "Which query shape?"), ("Usage", "$indexStats window"),
       ("Storage", "indexSizes"), ("Overlap", "shared prefixes")]), None),
    # --- Query tuning ---
    (131, "query-tuning-lifecycle", "h",
     [("Detect", None), ("Measure", None), ("explain", None), ("Design", None), ("Monitor", None)], None),
    (132, "performance-baseline", "g",
     [("Winning plan", None), ("Keys examined", None), ("Docs examined", None), ("nReturned + SORT?", None)], None),
    (133, "shape-to-candidate-index", "h",
     [("Filter fields", None), ("Sort fields", None), ("Index pattern", None)], None),
    (134, "candidate-index-evaluation", "2",
     (("Read benefit", "Examined counts, SORT gone"), ("Write / storage risk", "Extra keys on every write")), None),
    (135, "before-after-comparison", "2",
     (("Baseline", "COLLSCAN / extra SORT"), ("Indexed", "IXSCAN · closer ratios")), None),
    (136, "optimization-decision-tree", "g",
     [("Missing index", None), ("Wrong field order", None), ("Extra SORT", None), ("Huge result / RAM", None)], None),
    (137, "tuning-evidence-chain", "h",
     [("Business request", None), ("Query", None), ("explain", None), ("New plan", None)], None),
    (138, "index-recommendation-template", "g3",
     [("Query shape", None), ("Proposed index", None), ("Expected benefit", None),
      ("Write risk", None), ("Test plan", None), ("Rollback", None)], None),
    # --- Common mistakes ---
    (139, "index-every-field", "2",
     (("Many secondary indexes", None), ("Write path overloaded", None)), "Index recurring shapes"),
    (140, "wrong-compound-order", "2",
     (("Query prefix", "customerId then date"), ("Index leads with date", "Poor prefix fit")), None),
    (141, "range-field-too-early", "v",
     [("Range first", "wide key slice"), ("Later equality unused", None), ("ESR: equality first", None)], None),
    (142, "ignoring-sort-requirements", "2",
     (("Filter uses an index", None), ("Results still SORT", "Add sort fields to the key")), None),
    (143, "low-selectivity-alone", "2",
     (("{ active: 1 }", "Most products match"), ("Almost a COLLSCAN", "Use compound or partial")), None),
    (144, "duplicate-overlapping-indexes", "v",
     [("{ category: 1 }", None), ("{ category: 1, price: 1 }", None), ("Hide and measure first", None)], None),
    (145, "dev-data-vs-production", "2",
     (("12 products", "Plans look cheap"), ("Millions of docs", "Same COLLSCAN is expensive")),
     "training_store teaches the plan, not the stopwatch"),
    (146, "ixscan-not-always-fast", "2",
     (("Stage: IXSCAN", None), ("Keys examined: 50,000", "Returned: 10")), None),
    (147, "data-type-mismatch", "2",
     (("Number vs string", "Separate key ranges"), ("ObjectId vs string id", "Index unused")), None),
    (148, "indexing-without-measurement", "2",
     (("Assumed fix", "createIndex and hope"), ("explain() validation", "Compared examined counts")), None),
    (149, "dropping-without-testing", "2",
     (("Immediate dropIndex", "Risk of surprise COLLSCAN"), ("Hide → monitor → drop", "Rollback ready")), None),
    # --- E-commerce ---
    (150, "ecommerce-strategy-overview", "g",
     [("products", "SKU · browse · tags"), ("customers", "email"),
      ("orders", "number · history · paid"), ("reviews / sessions", "date · TTL")], None),
    (151, "product-lookup-by-sku", "v",
     [('sku: "L100"', None), ("uq_products_sku", None), ("One product", None)], None),
    (152, "product-browse-index", "h",
     [("category", None), ("active", None), ("price", "sort / range")], None),
    (153, "product-tag-multikey", "v",
     [("tags array", None), ("idx_products_tags", "multikey"), ("Matching products", None)], None),
    (154, "customer-email-index", "v",
     [("contact.email", None), ("idx_customers_contact_email", None), ("Customer C101", None)], None),
    (155, "order-number-unique", "2",
     (("Lookup O5001", None), ("uq_orders_order_number", "unique + seek")), None),
    (156, "customer-order-history-index", "h",
     [("customerId", None), ("createdAt -1", None), ("Newest first", None)], None),
    (157, "paid-order-reporting-index", "h",
     [("paymentStatus PAID", None), ("createdAt -1", None), ("Report input", None)], None),
    (158, "product-review-index", "h",
     [("productId", None), ("createdAt -1", None), ("Newest reviews", None)], None),
    (159, "session-ttl-index", "h",
     [("expiresAt", None), ("TTL index", None), ("Async cleanup", None)], None),
    (160, "dynamic-attribute-wildcard", "2",
     (("attributes.* vary", "by category"), ('attributes.$**', "controlled wildcard path")), None),
    (161, "ecommerce-query-index-matrix", "t",
     (["Operation", "Candidate index"],
      [("SKU lookup", "{ sku: 1 } unique"), ("Browse + price", "{ category, active, price }"),
       ("Tag search", "{ tags: 1 } multikey"), ("Order history", "{ customerId, createdAt: -1 }"),
       ("Sessions", "{ expiresAt: 1 } TTL")]), None),
    # --- Exercises ---
    (162, "ex-6-1-candidates", "t",
     (["Query", "Indexed fields"],
      [("Product by SKU", "sku"), ("Customer by email", "contact.email"),
       ("Newest customer orders", "customerId, createdAt"), ("Active by category/price", "category, active, price")]), None),
    (163, "ex-6-2-single-or-compound", "g",
     [("Single-field", "SKU lookup"), ("Compound", "browse + sort"),
      ("Specialized", "TTL sessions"), ("No new index", "one-time ad-hoc count")], None),
    (164, "ex-6-3-arrange-fields", "h",
     [("Equality cards", "customerId, PAID"), ("Sort card", "createdAt"), ("Range card", "total $gte")], None),
    (165, "ex-6-4-esr-classification", "3",
     [("E", "equality"), ("S", "sort"), ("R", "range")], "Label every field, then propose a key"),
    (166, "ex-6-5-prefix-challenge", "3",
     [("Full prefix", None), ("Partial prefix", None), ("Skipped prefix", "not supported")], None),
    (167, "ex-6-6-specialized-matching", "g3",
     [("Unique", "SKU"), ("Partial", "active only"), ("TTL", "sessions"),
      ("Wildcard", "attributes"), ("Geo", "nearby stores"), ("Hashed", "shard key")], None),
    (168, "ex-6-7-read-explain", "g",
     [("COLLSCAN or IXSCAN", None), ("Index name", None), ("Examined counts", None), ("Extra SORT?", None)], None),
    (169, "ex-6-8-covered-challenge", "v",
     [("Index fields", "category, price, name"), ("Filter + projection", None),
      ("_id excluded?", "Coverage yes or no")], None),
    (170, "ex-6-9-redundant", "v",
     [("{ category: 1 }", None), ("{ category, price }", None), ("{ category, price, name }", None),
      ("{ price: 1 }", "not a prefix")], None),
    (171, "ex-6-10-read-vs-write", "2",
     (("20% reads", "Need evidence"), ("80% writes · 14 indexes", "Insert latency rising")), None),
    (172, "ex-6-11-fix-antipattern", "3",
     [("Over-indexing", None), ("Wrong field order", None), ("Drop without hide", None)], None),
    (173, "ex-6-12-recommendation-canvas", "g3",
     [("Query / baseline", None), ("Candidate index", None), ("Evidence", None),
      ("Write risk", None), ("Validation", None), ("Rollback", None)], None),
    # --- Labs ---
    (174, "lab-6-1-baseline", "h",
     [("Query", None), ("explain", None), ("Record metrics", None), ("Keep baseline", None)], None),
    (175, "lab-6-2-single-field-test", "h",
     [("Baseline scan", None), ("SKU index", None), ("Re-explain", None), ("Compare", None)], None),
    (176, "lab-6-3-compound-test", "h",
     [("Browse query", None), ("Compound index", None), ("explain comparison", None)], None),
    (177, "lab-6-4-filter-sort-design", "h",
     [("Equality", "customerId"), ("Sort / range", "createdAt"), ("limit 10", None)], None),
    (178, "lab-6-5-nested-and-array", "2",
     (("contact.email", "nested scalar"), ("tags", "multikey array")), None),
    (179, "lab-6-6-unique-validation", "h",
     [("create unique", None), ("Accepted insert", None), ("Duplicate SKU", "E11000")], None),
    (180, "lab-6-7-partial-and-ttl", "2",
     (("Partial", "active products"), ("TTL", "sessions.expiresAt")), None),
    (181, "lab-6-8-covered-test", "v",
     [("Covering index", "category, price, name"), ("_id: 0 projection", None), ("No FETCH", None)], None),
    (182, "lab-6-9-agg-tuning", "h",
     [("Baseline pipeline", None), ("payment + createdAt index", None), ("explain again", None)], None),
    (183, "lab-6-10-audit-workflow", "h",
     [("Inventory", None), ("Overlap", None), ("hide test", None), ("Recommend", None)], None),
    (184, "lab-6-11-integrated", "2",
     (("Catalog page", "active · category · price"), ("Order history", "customer · PAID · newest 20")),
     "Baseline → ESR index → explain → write-cost note"),
    (185, "practical-challenge-review", "v",
     [("Ten query patterns", None), ("Minimal justified portfolio", None),
      ("Overlap + validation + rollback", None)], None),
]


def write_all() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    names: set[str] = set()
    if len(CATALOG) != 185:
        raise SystemExit(f"Expected 185 diagrams, found {len(CATALOG)}")
    seen_n: set[int] = set()
    for n, slug, kind, payload, caption in CATALOG:
        if n in seen_n:
            raise SystemExit(f"Duplicate diagram number {n}")
        seen_n.add(n)
        name = fname(n, slug)
        names.add(name)
        path = ASSETS / name
        path.write_text(_render(n, kind, payload, caption), encoding="utf-8")
    for extra in ASSETS.glob("*.svg"):
        if extra.name not in names:
            extra.unlink()
            print(f"Removed stale {extra.name}")
    print(f"Wrote {len(names)} diagrams ({len(ESSENTIAL)} essential classroom set)")
    return len(names)


if __name__ == "__main__":
    write_all()

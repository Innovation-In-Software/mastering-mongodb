"""Module 3 Marp diagrams — Mastering MongoDB (diagrams 1–111).

Style tokens from marp_svg_common. Run:

    python scripts/module03_diagrams.py
"""
from __future__ import annotations

import html
from pathlib import Path

from marp_svg_common import BORDER, FONT, HEADER_BG, MONO, MUTED, PANEL, RED, TEXT

BG_BOX = "#ffffff"
ASSETS = Path(__file__).resolve().parent.parent / "slides" / "assets" / "module-03"
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


def _box(x, y, w, h, title, sub=None, *, header=False, fs=20, sub_fs=16) -> str:
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
        parts.append(_box(x, y, bw, 90, t, fs=14 if len(t) > 18 else 16))
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
    parts.append(_box(30, y, 420, 180, lt, ls, header=headers, fs=18, sub_fs=15))
    parts.append(_box(470, y, 420, 180, rt, rs, header=headers, fs=18, sub_fs=15))
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
        parts.append(_box(x, y, bw, bh, t, s, fs=15 if s else 16, sub_fs=13))
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


def render_gauge(title: str, caption: str) -> str:
    parts = [
        _label(460, 28, title, fs=18, fill=TEXT),
        f'<rect x="80" y="90" width="760" height="48" rx="10" fill="{BG_BOX}" stroke="{RED}" stroke-width="2"/>',
        f'<rect x="80" y="90" width="620" height="48" rx="10" fill="{HEADER_BG}" stroke="{RED}" stroke-width="2"/>',
        _label(460, 122, "Typical order  →  approaching 16 MiB", fs=16, fill=TEXT),
        _label(80, 170, "0", fs=14, fill=MUTED, anchor="start"),
        _label(840, 170, "16 MiB max", fs=14, fill=RED, anchor="end"),
        _label(460, 210, caption, fs=15),
    ]
    return _svg(240, "\n".join(parts))


def d(kind: str, *args, **kwargs):
    return lambda: {
        "vflow": render_vflow,
        "hflow": render_hflow,
        "two": render_two,
        "grid": render_grid,
        "table": render_table,
        "gauge": render_gauge,
    }[kind](*args, **kwargs)


# --- Catalog 1–111 ----------------------------------------------------------

DIAGRAMS: dict[str, callable] = {
    "001-mongodb-data-hierarchy.svg": d(
        "vflow",
        "MongoDB data hierarchy",
        [
            ("MongoDB deployment", None),
            ("Database", None),
            ("Collection", None),
            ("Document", None),
            ("Field  ·  nested document  ·  array", None),
        ],
    ),
    "002-database-collection-document.svg": d(
        "grid",
        "training_store — one database, four collections",
        [
            ("products", "Catalog documents"),
            ("customers", "Buyer profiles"),
            ("orders", "Purchase aggregates"),
            ("reviews", "Independent comments"),
        ],
        cols=2,
        caption="Each collection holds related documents — not one collection per tiny table",
    ),
    "003-anatomy-of-a-document.svg": d(
        "grid",
        "Label every BSON shape in one document",
        [
            ("_id", "ObjectId"),
            ("sku / name", "String"),
            ("price", "Decimal128"),
            ("active", "Boolean"),
            ("createdAt", "Date"),
            ("tags [ ]", "Array"),
            ("specifications { }", "Embedded document"),
            ("quantity", "Int32"),
        ],
        cols=4,
    ),
    "004-bson-data-type-map.svg": d(
        "grid",
        "BSON type catalog",
        [
            ("ObjectId", "Unique id / reference"),
            ("String", "Name, SKU, status"),
            ("Int / Long", "Counts, quantity"),
            ("Double", "Approximate measure"),
            ("Decimal128", "Money"),
            ("Boolean", "Flags"),
            ("Date", "Timestamps"),
            ("Array", "Lists of values"),
            ("Document", "Nested object"),
            ("Binary", "Opaque bytes"),
            ("Null", "Intentional empty"),
            ("Timestamp", "Internal ops"),
        ],
        cols=4,
    ),
    "005-id-field-and-objectid.svg": d(
        "hflow",
        "How _id is assigned",
        ["Insert without _id", "MongoDB generates ObjectId", "Unique stored document"],
        caption="_id is required, unique in the collection, indexed, and treated as immutable",
    ),
    "006-embedded-document-structure.svg": d(
        "vflow",
        "Customer with owned nested objects",
        [
            ("customer  C101", None),
            ("name { first, last }", None),
            ("contact { email, phone }", None),
            ("address { street, city, country }", None),
        ],
        caption="Embed when the child belongs to the parent and stays bounded",
    ),
    "007-array-of-scalar-values.svg": d(
        "grid",
        "Scalar arrays on a product",
        [
            ('tags: ["wireless","keyboard"]', None),
            ('colors: ["Black","White"]', None),
            ("sizes: [7, 8, 9, 10]", None),
        ],
        cols=1,
        caption="Arrays of strings or numbers — still keep a predictable growth limit",
    ),
    "008-array-of-embedded-documents.svg": d(
        "vflow",
        "Order items as an array of documents",
        [
            ("order  O5001", None),
            ("items[0]  { sku, qty, unitPrice }", None),
            ("items[1]  { sku, qty, unitPrice }", None),
        ],
        caption="Each element is a snapshot of one purchased line",
    ),
    "009-flexible-schema-within-collection.svg": d(
        "grid",
        "One products collection — shared core, different attributes",
        [
            ("LAPTOP", "processor · memoryGB"),
            ("SHOE", "sizes · color · material"),
            ("BOOK", "author · isbn · language"),
        ],
        cols=3,
        caption="Shared: sku · name · category · price · active",
    ),
    "010-flexible-vs-inconsistent-schema.svg": d(
        "two",
        "Flexible schema is not chaos",
        ("Intentional variation", "category-specific attributes under a stable core"),
        ("Uncontrolled inconsistency", "price / productPrice / item_cost"),
        caption="Agree names, types, and required fields",
    ),
    "011-relational-vs-document-model.svg": d(
        "table",
        "Relational model vs document model",
        ["", "Relational", "Document"],
        [
            ("Start", "Normalize tables", "Access patterns"),
            ("Related data", "Join at read time", "Store together if used together"),
            ("Schema", "Table DDL", "Conventions + validation"),
            ("Relationships", "Foreign keys", "Embed or reference"),
        ],
    ),
    "012-tables-to-documents.svg": d(
        "hflow",
        "Tables become documents — not one collection per table",
        ["customers", "orders + items + address", "products", "reviews"],
        caption="Order items and shipping address usually fold into the order aggregate",
    ),
    "013-join-vs-document-retrieval.svg": d(
        "two",
        "How the application gets one order",
        ("Relational read", "JOIN customers, orders, order_items, products, addresses"),
        ("Document read", "find({ orderNumber: \"O5001\" })"),
        caption="The document is the business object the screen already needed",
    ),
    "014-normalization-vs-aggregates.svg": d(
        "two",
        "Divide by entity vs group by operation",
        ("Normalized entities", "Customer · Order · Item · Product · Address"),
        ("MongoDB aggregate", "One order document for checkout and order-detail"),
        caption="Start from the operation, then split only what must live apart",
    ),
    "015-collection-per-table-antipattern.svg": d(
        "two",
        "Do not copy every table as a collection",
        ("Anti-pattern", "customers, orders, order_items, addresses, products, payments…"),
        ("Redesigned model", "customers · products · orders · reviews"),
        caption="Tiny collections keep the joins and lose the document benefit",
    ),
    "016-access-pattern-driven-modeling.svg": d(
        "vflow",
        "Access-pattern-driven data modeling",
        [
            ("Application requirements", None),
            ("Access patterns", None),
            ("Relationships and ownership", None),
            ("Document boundaries", None),
            ("Collections", None),
        ],
    ),
    "017-read-and-write-access-patterns.svg": d(
        "two",
        "Reads and writes both shape the schema",
        ("Read", "frequency · filters · returned fields · latency"),
        ("Write", "which fields change · together? · array growth · concurrency"),
        caption="Optimizing one hot read can increase write complexity",
    ),
    "018-data-accessed-together.svg": d(
        "grid",
        "Data accessed together can often be stored together",
        [
            ("Order number", None),
            ("Purchased items", None),
            ("Purchase-time prices", None),
            ("Shipping address", None),
            ("Totals", None),
            ("Status", None),
        ],
        cols=3,
        caption="One order document — one read  (a signal, not an unconditional rule)",
    ),
    "019-data-that-changes-together.svg": d(
        "two",
        "Same lifecycle → embed",
        ("Order quantity + unit price", "Created, updated, and kept with the sale"),
        ("Current catalog description", "Different lifecycle — stays on the product"),
        caption="Created together, updated together, removed together",
    ),
    "020-access-pattern-to-document-shape.svg": d(
        "vflow",
        "From a sentence to a document",
        [
            ('“Retrieve a complete order by order number.”', None),
            ("Identity + customerId + items[] + address + totals + status", None),
            ("find({ orderNumber: \"O5001\" })", None),
        ],
    ),
    "021-application-query-map.svg": d(
        "table",
        "Application query map",
        ["User action", "Collection", "Shape"],
        [
            ("Product search / PDP", "products", "One product document"),
            ("Customer profile", "customers", "Embedded addresses"),
            ("Order details", "orders", "Embedded aggregate"),
            ("Order history", "orders", "Many docs by customerId"),
            ("Review browsing", "reviews", "Paginated child collection"),
        ],
    ),
    "022-read-optimization-vs-write-complexity.svg": d(
        "two",
        "Embedding is a tradeoff",
        ("Faster reads", "Fewer lookups · complete object in one round trip"),
        ("Harder writes", "Larger documents · duplication · bulk updates"),
        caption="Accept the write cost when the read is the business-critical path",
    ),
    "023-mongodb-relationship-types.svg": d(
        "hflow",
        "Cardinality changes the representation",
        ["1 : 1", "1 : few", "1 : many", "1 : squillions", "N : N"],
        caption="Also consider ownership, growth, access direction, and update frequency",
    ),
    "024-one-to-one-relationship.svg": d(
        "two",
        "One-to-one — usually embed",
        ("Customer", "C101"),
        ("Embedded contact", "email · phone"),
        caption="Embed when the child exists only as part of the parent",
        headers=False,
    ),
    "025-one-to-few-relationship.svg": d(
        "vflow",
        "One-to-few — bounded array",
        [
            ("Customer C101", None),
            ("addresses[ ]  (2–5 typical)", None),
            ("SHIPPING  ·  BILLING", None),
        ],
        caption="Addresses, product images, order items — embed if they stay small",
    ),
    "026-one-to-many-relationship.svg": d(
        "vflow",
        "One-to-many — separate collection",
        [
            ("Customer C101", None),
            ("orders.customerId  →  C101", None),
            ("O5001  ·  O5002  ·  O5…", None),
        ],
        caption="A lifetime of orders will not fit in the customer document",
    ),
    "027-one-to-squillions-relationship.svg": d(
        "two",
        "One-to-squillions — never embed the full set",
        ("Product or account", "Stable parent document"),
        ("reviews / events / transactions", "Own collection, paginated"),
        caption="High cardinality children are referenced, not appended forever",
    ),
    "028-many-to-many-relationship.svg": d(
        "grid",
        "Products ↔ categories",
        [
            ("Product P1001", "categoryIds: [C10, C12]"),
            ("Category C10", "many products"),
            ("Category C12", "many products"),
        ],
        cols=3,
        caption="Store ids on the side you navigate from — or accept $lookup",
    ),
    "029-relationship-cardinality-decision.svg": d(
        "vflow",
        "Cardinality decision flow",
        [
            ("How many child records — and will that grow?", None),
            ("One or few and bounded  →  embed", None),
            ("Many or unbounded  →  reference", None),
            ("Rare extremes  →  outlier / subset", None),
        ],
    ),
    "030-relationship-ownership.svg": d(
        "two",
        "Who owns the data?",
        ("Owned by the parent", "Address on a customer · items on an order"),
        ("Independently managed", "Customer master · current product · agent"),
        caption="Ownership is as important as cardinality",
    ),
    "031-embedding-related-data.svg": d(
        "vflow",
        "Embedding stores the child inside the parent",
        [
            ("Parent document", None),
            ("Nested object or bounded array", None),
            ("One read · one atomic update", None),
        ],
        caption="Risks: duplication, growth, harder bulk updates",
    ),
    "032-referencing-related-data.svg": d(
        "vflow",
        "Referencing stores another document’s _id",
        [
            ("orders.customerId", None),
            ("customers._id", None),
            ("Second query or $lookup if both are needed", None),
        ],
        caption="Independent lifecycle and high cardinality",
    ),
    "033-embedding-vs-referencing.svg": d(
        "table",
        "Embedding vs referencing",
        ["Consideration", "Embed", "Reference"],
        [
            ("Read together", "Strong candidate", "Another query"),
            ("Child count", "Small, bounded", "Large / unbounded"),
            ("Lifecycle", "Owned by parent", "Independent"),
            ("Atomic update", "Single document", "May span documents"),
            ("Duplication", "Accepted", "Reduced"),
        ],
    ),
    "034-embedding-decision-tree.svg": d(
        "vflow",
        "Embedding decision tree",
        [
            ("Read together?", None),
            ("Same lifecycle?", None),
            ("Bounded size?", None),
            ("Yes to all  →  embed    ·    otherwise reference", None),
        ],
    ),
    "035-customer-address-embedded.svg": d(
        "vflow",
        "Customer address — embedded model",
        [
            ("Customer C101", None),
            ("addresses[ ]  bounded", None),
            ("type, street, city, country", None),
        ],
    ),
    "036-customer-orders-referenced.svg": d(
        "two",
        "Customer orders — referenced model",
        ("customers", "C101 profile only"),
        ("orders", "customerId → C101"),
        caption="List a customer’s orders with a query on orders, not an array on the customer",
    ),
    "037-order-items-embedded.svg": d(
        "vflow",
        "Order items — embedded snapshots",
        [
            ("Order O5001", None),
            ("items[ ]  sku · name · qty · unitPrice", None),
            ("Purchase-time facts stay with the sale", None),
        ],
    ),
    "038-product-reviews-referenced.svg": d(
        "two",
        "Product reviews — referenced model",
        ("products", "sku · name · ratingSummary"),
        ("reviews", "productId · rating · body"),
        caption="The review set can grow without bound — keep it out of the product",
    ),
    "039-hybrid-embedding-and-referencing.svg": d(
        "table",
        "Hybrid order: reference people/catalog, embed the sale",
        ["On the order", "Choice"],
        [
            ("customerId", "Reference"),
            ("productId on each item", "Reference"),
            ("sku, name, unitPrice", "Embedded snapshot"),
            ("shippingAddress", "Embedded snapshot"),
        ],
    ),
    "040-single-document-atomicity.svg": d(
        "hflow",
        "Single-document atomicity",
        ["Update items + totals + status", "One write to one document", "All fields change together"],
        caption="Related fields in one document succeed or fail as one operation",
    ),
    "041-intentional-data-duplication.svg": d(
        "two",
        "Copy selected fields to speed reads",
        ("Source", "products.name · customers.tier"),
        ("Copy on the order", "item.name · customer.name / tier"),
        caption="Duplication is a design choice with an update policy",
    ),
    "042-historical-snapshot-modeling.svg": d(
        "grid",
        "Orders preserve purchase-time facts",
        [
            ("Product name", None),
            ("Unit price", None),
            ("Tax / discount", None),
            ("Ship-to address", None),
        ],
        cols=2,
        caption="A later catalog change must not rewrite history",
    ),
    "043-current-vs-historical-state.svg": d(
        "two",
        "Current catalog vs historical order",
        ("Product now", "price: 39.99"),
        ("Order O5001", "unitPrice: 49.99  (unchanged)"),
        caption="The order is a point-in-time record, not a live join to the catalog",
    ),
    "044-duplicated-data-sync-choices.svg": d(
        "grid",
        "How should the copy stay in sync?",
        [
            ("Snapshot", "Never update"),
            ("Synchronous", "Write both now"),
            ("Event-based", "Async update"),
            ("Periodic refresh", "Batch rebuild"),
            ("Eventual", "Accept lag"),
        ],
        cols=3,
        caption="For purchase-time price the answer is almost always snapshot",
    ),
    "045-denormalization-tradeoff.svg": d(
        "two",
        "Denormalization tradeoff",
        ("Gain", "Faster reads · fewer lookups"),
        ("Cost", "Duplication · update complexity"),
        caption="Denormalize stable or historical fields — not rapidly changing ones everywhere",
    ),
    "046-extended-reference-example.svg": d(
        "two",
        "Extended reference on an order",
        ("customers (full profile)", "email, addresses, preferences"),
        ("orders.customer { }", "customerId + name + tier"),
        caption="Display the order without a second query — copies may need sync",
    ),
    "047-bounded-vs-unbounded-arrays.svg": d(
        "two",
        "Bounded vs unbounded arrays",
        ("Bounded", "Customer addresses (few)"),
        ("Unbounded", "All product reviews ever"),
        caption="If you cannot name a practical max, do not embed the array",
    ),
    "048-unbounded-array-antipattern.svg": d(
        "vflow",
        "Anti-pattern: allReviews[ ] growing forever",
        [
            ("Product P1001", None),
            ("allReviews[ 0 … millions ]", None),
            ("Huge docs · expensive updates · 16 MiB risk", None),
        ],
    ),
    "049-unbounded-array-correction.svg": d(
        "two",
        "Move the growing set out",
        ("Before", "product.allReviews[ ]"),
        ("After", "reviews collection  productId → P1001"),
        caption="Optional: keep a small recent subset on the product",
    ),
    "050-16mib-bson-document-limit.svg": lambda: render_gauge(
        "Maximum BSON document size = 16 MiB",
        "The limit is a ceiling, not a target — stay comfortably smaller",
    ),
    "051-document-growth-over-time.svg": d(
        "hflow",
        "Embedded records accumulate",
        ["Small new document", "More nested arrays", "Slow updates + large reads"],
        caption="Even below 16 MiB, a frequently updated 2 MiB document is a problem",
    ),
    "052-document-growth-decision-flow.svg": d(
        "vflow",
        "Document growth decision flow",
        [
            ("Will this keep growing?", None),
            ("Bounded  →  embed is still viable", None),
            ("Unbounded  →  bucket, subset, archive, or reference", None),
        ],
    ),
    "053-large-binary-data-decision.svg": d(
        "two",
        "Keep large files out of the document",
        ("In the document", "Metadata, mime type, URL, checksum"),
        ("Outside the document", "Object storage or GridFS"),
        caption="Binary blobs are a common way to hit 16 MiB by accident",
    ),
    "054-ecommerce-data-model-overview.svg": d(
        "grid",
        "training_store relationships",
        [
            ("customers", "Referenced by orders"),
            ("products", "Referenced by items + reviews"),
            ("orders", "Embed items + address snapshot"),
            ("reviews", "productId + customerId"),
        ],
        cols=2,
    ),
    "055-product-document-model.svg": d(
        "two",
        "Product = shared core + flexible attributes",
        ("Core", "sku · name · category · price · active · createdAt"),
        ("attributes { }", "Varies by category"),
        caption="Polymorphic collection with a stable required core",
    ),
    "056-laptop-product-document.svg": d(
        "grid",
        "Laptop L100",
        [
            ("sku / name / category", "L100 · Business Laptop · LAPTOP"),
            ("price", "Decimal128 1299.99"),
            ("attributes.processor", "Intel Core i7"),
            ("attributes.memoryGB", "16"),
            ("attributes.storageGB", "512"),
            ("attributes.screenSizeInches", "14"),
        ],
        cols=2,
    ),
    "057-shoe-product-document.svg": d(
        "grid",
        "Shoe S200",
        [
            ("sku / name / category", "S200 · Running Shoe · SHOE"),
            ("price", "Decimal128 129.99"),
            ("attributes.sizes", "[7, 8, 9, 10]"),
            ("attributes.color", "Blue"),
            ("attributes.material", "Mesh"),
            ("tags", "running · sports"),
        ],
        cols=2,
    ),
    "058-book-product-document.svg": d(
        "grid",
        "Book B300",
        [
            ("sku / name / category", "B300 · MongoDB Fundamentals · BOOK"),
            ("price", "Decimal128 59.99"),
            ("attributes.author", "A. Trainer"),
            ("attributes.isbn", "978-0000000000"),
            ("attributes.language", "English"),
            ("tags", "database · technology"),
        ],
        cols=2,
    ),
    "059-customer-profile-document.svg": d(
        "grid",
        "Customer C101",
        [
            ("name { first, last }", "Aisha Khan"),
            ("contact { }", "email · phone"),
            ("addresses[ ] bounded", "SHIPPING · Toronto"),
            ("preferences / status", "newsletter · ACTIVE"),
        ],
        cols=2,
        caption="Orders are not an array on this document",
    ),
    "060-order-aggregate-document.svg": d(
        "grid",
        "Order O5001 aggregate",
        [
            ("customerId", "Reference"),
            ("items[ ] snapshots", "sku · name · qty · unitPrice"),
            ("shippingAddress", "Snapshot"),
            ("totals + statuses", "Decimal128 · PENDING / NEW"),
        ],
        cols=2,
    ),
    "061-product-and-order-relationship.svg": d(
        "two",
        "Live catalog vs purchase-time snapshot",
        ("products  L100", "Current name and price"),
        ("orders.items[ ]", "productId + copied name and unitPrice"),
        caption="The reference finds the product later; the snapshot is what was sold",
    ),
    "062-product-review-model.svg": d(
        "two",
        "Product summary + separate reviews",
        ("Product", "ratingSummary · optional 3 recent"),
        ("reviews collection", "Full history, paginated"),
        caption="Subset + computed patterns on the product; children live apart",
    ),
    "063-complete-ecommerce-read-model.svg": d(
        "table",
        "Screen → collection",
        ["Screen", "Primary read"],
        [
            ("Product page", "products (+ subset of reviews)"),
            ("Customer profile", "customers"),
            ("Order details", "orders (one document)"),
            ("Order history", "orders by customerId"),
            ("All reviews", "reviews by productId"),
        ],
    ),
    "064-ecommerce-access-pattern-map.svg": d(
        "table",
        "User action → query → structure",
        ["Action", "Query", "Structure"],
        [
            ("Find by SKU", "products.sku", "Single document"),
            ("Browse category", "products.category", "Flexible attributes"),
            ("Place order", "insert orders", "Embedded aggregate"),
            ("List my orders", "orders.customerId", "Referenced children"),
        ],
    ),
    "065-flexible-schema-with-validation.svg": d(
        "hflow",
        "Flexible documents with guardrails",
        ["Varied attributes OK", "$jsonSchema checks core", "Accept or reject write"],
        caption="Flexibility remains — required names and types are enforced",
    ),
    "066-schema-validation-flow.svg": d(
        "vflow",
        "Schema validation flow",
        [
            ("insert / update", None),
            ("Collection validator ($jsonSchema)", None),
            ("Accept document    or    return validation error", None),
        ],
    ),
    "067-required-fields-validation.svg": d(
        "grid",
        "Required product fields",
        [
            ("sku", "string"),
            ("name", "string"),
            ("category", "string"),
            ("price", "decimal ≥ 0"),
            ("active", "bool"),
            ("createdAt", "date"),
        ],
        cols=3,
    ),
    "068-bson-type-validation.svg": d(
        "table",
        "BSON type checks",
        ["Field", "Expected", "Rejected example"],
        [
            ("sku", "string", "101"),
            ("price", "decimal", '"49.99"'),
            ("active", "bool", '"yes"'),
            ("createdAt", "date", '"September 20"'),
        ],
    ),
    "069-valid-vs-invalid-product.svg": d(
        "two",
        "Valid insert vs rejected insert",
        ("Accepted", "Decimal128 price · active: true · Date"),
        ("Rejected", 'price: "39.99" · active: "yes" · missing createdAt'),
        caption="Read the validation error with the class — do not skip it",
    ),
    "070-nested-document-validation.svg": d(
        "vflow",
        "Validate the document and its nested objects",
        [
            ("Product object", None),
            ("properties.attributes  bsonType: object", None),
            ("Nested required keys only when that category needs them", None),
        ],
    ),
    "071-validation-level-and-action.svg": d(
        "table",
        "validationAction and validationLevel",
        ["Option", "error / strict", "warn / moderate"],
        [
            ("Action", "Reject the write", "Allow and log"),
            ("Level", "All inserts and updates", "Inserts + already-valid docs"),
        ],
        caption="Classroom labs use error + strict so mistakes are visible",
    ),
    "072-schema-evolution-timeline.svg": d(
        "hflow",
        "Schema evolution timeline",
        ["v1 document", "Add optional fields", "v2 structure", "Migrated document"],
    ),
    "073-backward-compatible-schema-change.svg": d(
        "two",
        "Backward-compatible change",
        ("Existing documents", "Still readable without the new field"),
        ("New documents", "May include an optional field"),
        caption="Add optional fields first — do not rename a required field overnight",
    ),
    "074-breaking-vs-nonbreaking-changes.svg": d(
        "two",
        "Breaking vs non-breaking",
        ("Non-breaking", "Add optional field · add a new status value"),
        ("Breaking", "Rename field · change required type"),
        caption="Breaking changes need readers that understand both shapes, then a migration",
    ),
    "075-schema-version-strategy.svg": d(
        "vflow",
        "schemaVersion on the document",
        [
            ("v1  price: Decimal128", None),
            ("v2  price: { amount, currency }  schemaVersion: 2", None),
            ("Application supports both until migration finishes", None),
        ],
    ),
    "076-incremental-data-migration.svg": d(
        "hflow",
        "Migrate one document at a time",
        ["Read old", "Transform", "Validate", "Save updated"],
        caption="No big-bang rewrite of every document on launch night",
    ),
    "077-reader-first-schema-evolution.svg": d(
        "vflow",
        "Reader-first evolution",
        [
            ("Update readers to understand the new shape", None),
            ("Introduce new writers", None),
            ("Migrate historical documents", None),
            ("Retire the old format", None),
        ],
    ),
    "078-schema-pattern-overview.svg": d(
        "grid",
        "Reusable approaches — not mandatory templates",
        [
            ("Attribute", None),
            ("Bucket", None),
            ("Subset", None),
            ("Extended ref", None),
            ("Computed", None),
            ("Outlier", None),
            ("Polymorphic", None),
        ],
        cols=4,
    ),
    "079-attribute-pattern.svg": d(
        "two",
        "Attribute pattern",
        ("Wide named fields", "color · size · material as top-level keys"),
        ("attributes: [ {name, value} ]", "Same shape — easier to index"),
        caption="Use when many similar optional attributes appear",
    ),
    "080-bucket-pattern.svg": d(
        "two",
        "Bucket pattern",
        ("Hour start", "sensorId + bucketStart"),
        ("readings[ ] bounded", "time + value pairs for that hour"),
        caption="Fewer documents, controlled growth — typical for time-series",
    ),
    "081-subset-pattern.svg": d(
        "two",
        "Subset pattern",
        ("Product document", "avg rating · 3 recent reviews"),
        ("reviews collection", "Complete history"),
        caption="Hot path reads a small subset; cold path reads the rest",
    ),
    "082-extended-reference-pattern.svg": d(
        "two",
        "Extended reference pattern",
        ("customers (full)", "Complete profile"),
        ("orders.customer { }", "id + name + tier"),
        caption="Copied fields may need synchronization",
    ),
    "083-computed-pattern.svg": d(
        "vflow",
        "Store the result instead of recomputing",
        [
            ("Source: reviews or line items", None),
            ("Computed: average, count, order total, CLV", None),
            ("Update the stored result when sources change", None),
        ],
    ),
    "084-outlier-pattern.svg": d(
        "two",
        "Do not distort the schema for rare extremes",
        ("Typical products", "< 100 reviews — subset in document"),
        ("Viral products", "Millions of reviews — separate store"),
        caption="Most documents follow the normal design",
    ),
    "085-polymorphic-pattern.svg": d(
        "two",
        "Different types, one collection",
        ('type: "BOOK"', "author · isbn"),
        ('type: "LAPTOP"', "processor · memoryGB"),
        caption="Shared workflows and a common core — type-specific fields vary",
    ),
    "086-schema-pattern-selection-matrix.svg": d(
        "table",
        "Requirement → pattern",
        ["Requirement", "Pattern"],
        [
            ("Many variable attributes", "Attribute"),
            ("High-volume time data", "Bucket"),
            ("Only recent items shown", "Subset"),
            ("Copied referenced fields", "Extended reference"),
            ("Expensive repeated calc", "Computed"),
            ("Rare huge records", "Outlier"),
            ("Related document types", "Polymorphic"),
        ],
    ),
    "087-combining-schema-patterns.svg": d(
        "grid",
        "One product document can combine patterns",
        [
            ("Polymorphic", "category / type"),
            ("Attribute", "flexible specs"),
            ("Computed", "ratingSummary"),
            ("Subset", "3 recent reviews"),
            ("Outlier", "viral SKUs elsewhere"),
        ],
        cols=3,
        caption="Patterns compose — they are not mutually exclusive",
    ),
    "088-schema-antipatterns-overview.svg": d(
        "grid",
        "Schema anti-patterns",
        [
            ("Unbounded arrays", None),
            ("Inconsistent types", None),
            ("Excessive nesting", None),
            ("Tiny extra collections", None),
            ("Uncontrolled duplication", None),
            ("No access patterns", None),
        ],
        cols=3,
    ),
    "089-numbers-stored-as-strings.svg": d(
        "two",
        "Money is not a string",
        ("Incorrect", 'price: "49.99"'),
        ("Correct", "price: Decimal128(\"49.99\")"),
        caption="String prices break sorting, comparison, and aggregation",
    ),
    "090-inconsistent-field-names.svg": d(
        "grid",
        "Three names for the same fact — three bugs",
        [("price", None), ("productPrice", None), ("item_cost", None)],
        cols=3,
        caption="Queries miss documents that used the other name",
    ),
    "091-over-normalized-mongodb-model.svg": d(
        "hflow",
        "A simple screen should not require this many lookups",
        ["customers", "orders", "order_items", "products", "addresses"],
        caption="Over-normalization recreates relational joins in application code",
    ),
    "092-oversized-document-antipattern.svg": d(
        "vflow",
        "One document accumulating unrelated or unlimited data",
        [
            ("Customer + all orders + all reviews + logs + files…", None),
            ("Slow reads, heavy updates, 16 MiB risk", None),
        ],
    ),
    "093-mixed-unrelated-data-antipattern.svg": d(
        "grid",
        "One collection is not a junk drawer",
        [
            ("customers", "do not mix"),
            ("orders", "do not mix"),
            ("app logs", "do not mix"),
            ("products", "do not mix"),
        ],
        cols=2,
        caption="Unrelated document types need separate collections — unless they share a workflow (polymorphic)",
    ),
    "094-deep-nesting-antipattern.svg": d(
        "vflow",
        "Needless deep nesting",
        [
            ("customer.profile.contact.home.address.geo.city", None),
            ("Complicated queries and updates", None),
            ("Flatten to the depth the access pattern needs", None),
        ],
    ),
    "095-antipattern-correction-flow.svg": d(
        "hflow",
        "Correction flow",
        ["Detect problem", "Identify access pattern", "Redesign boundary", "Validate new model"],
    ),
    "096-ex-3-1-label-the-document.svg": d(
        "grid",
        "Exercise 3.1 — label every component",
        [
            ("_id", "?"),
            ("Scalars", "?"),
            ("Embedded name", "?"),
            ("tags array", "?"),
            ("Boolean", "?"),
            ("Date", "?"),
        ],
        cols=3,
        caption="Then mark candidate required fields",
    ),
    "097-ex-3-2-access-pattern-worksheet.svg": d(
        "table",
        "Exercise 3.2 — access-pattern worksheet",
        ["Operation", "Frequency", "Required data", "Implication"],
        [
            ("Find product by SKU", "High", "Product details", "Single document"),
            ("Retrieve order", "High", "Items, totals, address", "Embed aggregate"),
            ("List customer orders", "Med", "Order summaries", "Reference + index"),
            ("Paginate reviews", "Med", "Review pages", "Separate collection"),
        ],
    ),
    "098-ex-3-3-embed-or-reference-board.svg": d(
        "table",
        "Exercise 3.3 — decision board",
        ["Relationship", "Likely choice"],
        [
            ("Primary contact", "Embed"),
            ("Complete order history", "Reference"),
            ("Order line items", "Embed"),
            ("Millions of reviews", "Reference"),
            ("Purchase-time price", "Embed snapshot"),
            ("Full transaction history", "Reference"),
        ],
    ),
    "099-ex-3-4-flexible-product-catalog.svg": d(
        "grid",
        "Exercise 3.4 — one collection, three types",
        [
            ("LAPTOP", "processor · memory"),
            ("SHOE", "size · color"),
            ("BOOK", "author · isbn"),
        ],
        cols=3,
        caption="Keep the core field names identical",
    ),
    "100-ex-3-5-build-an-order-aggregate.svg": d(
        "grid",
        "Exercise 3.5 — arrange the order",
        [
            ("Customer", "Reference"),
            ("Line items + prices", "Embed snapshot"),
            ("Ship-to address", "Embed snapshot"),
            ("Payment / fulfillment", "On the order"),
        ],
        cols=2,
    ),
    "101-ex-3-6-find-the-antipatterns.svg": d(
        "grid",
        "Exercise 3.6 — what is wrong?",
        [
            ('price: "49.99"', "string"),
            ('isActive: "yes"', "not Boolean"),
            ("allReviews[ ]", "unbounded"),
            ('created: "September 20"', "not Date"),
        ],
        cols=2,
    ),
    "102-ex-3-7-match-the-schema-pattern.svg": d(
        "table",
        "Exercise 3.7 — match the pattern",
        ["Requirement", "Pattern"],
        [
            ("Hourly sensor readings", "Bucket"),
            ("Latest three reviews", "Subset"),
            ("Stored average rating", "Computed"),
            ("Dynamic specifications", "Attribute"),
            ("Customer name on order", "Extended reference"),
            ("Viral review volume", "Outlier"),
            ("Multiple product types", "Polymorphic"),
        ],
    ),
    "103-ex-3-8-design-validation-rules.svg": d(
        "grid",
        "Exercise 3.8 — required + bsonType",
        [
            ("sku", "string"),
            ("name", "string"),
            ("category", "string"),
            ("price", "decimal ≥ 0"),
            ("active", "bool"),
            ("createdAt", "date"),
        ],
        cols=3,
    ),
    "104-lab-3-1-training-database-structure.svg": d(
        "grid",
        "Lab 3.1 — training_store",
        [
            ("products", None),
            ("customers", None),
            ("orders", None),
            ("reviews", None),
        ],
        cols=2,
        caption="createCollection each name, then show collections",
    ),
    "105-lab-3-2-product-dataset-structure.svg": d(
        "hflow",
        "Lab 3.2 — three products",
        ["L100 LAPTOP", "S200 SHOE", "B300 BOOK"],
        caption="Shared core + attributes  ·  Decimal128 prices",
    ),
    "106-lab-3-3-customer-dataset-structure.svg": d(
        "grid",
        "Lab 3.3 — customer C101",
        [
            ("name { }", None),
            ("contact { }", None),
            ("addresses[1]", None),
            ("preferences / status", None),
        ],
        cols=2,
    ),
    "107-lab-3-4-order-dataset-structure.svg": d(
        "grid",
        "Lab 3.4 — order O5001",
        [
            ("customerId", "reference"),
            ("items[ ]", "snapshot"),
            ("shippingAddress", "snapshot"),
            ("totals / status", "Decimal128"),
        ],
        cols=2,
    ),
    "108-lab-3-5-nested-field-query-paths.svg": d(
        "vflow",
        "Lab 3.5 — dot notation paths",
        [
            ('products  "attributes.memoryGB"', None),
            ('customers  "addresses.city"', None),
            ('orders  "items.sku"', None),
        ],
        caption="Quotes around dotted keys matter",
    ),
    "109-lab-3-6-validation-test-flow.svg": d(
        "hflow",
        "Lab 3.6 — validation test",
        ["Valid A100 insert", "Validator", "Invalid A101 rejected"],
        caption="Read the error: string price, text Boolean, missing createdAt",
    ),
    "110-lab-3-7-data-model-review-checklist.svg": d(
        "grid",
        "Lab 3.7 — review checklist",
        [
            ("Accessed together?", None),
            ("Arrays bounded?", None),
            ("Money / dates typed?", None),
            ("Embed vs ref deliberate?", None),
            ("Snapshots preserved?", None),
            ("Names consistent?", None),
        ],
        cols=3,
    ),
    "111-practical-challenge-support-ticket.svg": d(
        "hflow",
        "Support-ticket model",
        ["Customer", "Ticket", "Assigned agent", "Recent comments", "Full audit history"],
        caption="Embed bounded recent comments; store complete history separately",
    ),
}

# Keep a few extras still referenced by existing slides.
DIAGRAMS.update(
    {
        "000-why-data-modeling-matters.svg": d(
            "two",
            "A schema is a design, not a table dump",
            ("Good model", "Efficient reads · safer updates · useful indexes"),
            ("Poor model", "App-side joins · unbounded arrays · inconsistent fields"),
        ),
        "000-module-3-concept-map.svg": d(
            "grid",
            "Module 3 concept map",
            [
                ("Access patterns first", None),
                ("Embed bounded owned data", None),
                ("Reference the rest", None),
                ("Snapshots may not sync", None),
                ("Avoid unbounded arrays", None),
                ("Validate the contract", None),
            ],
            cols=3,
        ),
        "000-day1-result-path.svg": d(
            "hflow",
            "Day 1 result — ready for querying",
            ["NoSQL landscape", "Working instance", "Document model", "training_store data"],
        ),
        "000-time-series-events.svg": d(
            "vflow",
            "Event / time-series design",
            [
                ("source · type · timestamp · value", None),
                ("High write volume · retention · time queries", None),
                ("Often the Bucket pattern — not one document per event", None),
            ],
        ),
    }
)

# Backward-compatible aliases for the previous 56 filenames.
_ALIASES = {
    "01-why-data-modeling-matters.svg": "000-why-data-modeling-matters.svg",
    "02-mongodb-data-hierarchy.svg": "001-mongodb-data-hierarchy.svg",
    "03-databases-collections-documents.svg": "002-database-collection-document.svg",
    "04-anatomy-of-a-document.svg": "003-anatomy-of-a-document.svg",
    "05-bson-data-types.svg": "004-bson-data-type-map.svg",
    "06-objectid-and-id.svg": "005-id-field-and-objectid.svg",
    "07-nested-documents.svg": "006-embedded-document-structure.svg",
    "08-arrays-in-documents.svg": "007-array-of-scalar-values.svg",
    "09-flexible-schema.svg": "009-flexible-schema-within-collection.svg",
    "10-schema-conventions.svg": "010-flexible-vs-inconsistent-schema.svg",
    "11-relational-vs-document.svg": "011-relational-vs-document-model.svg",
    "12-model-around-access-patterns.svg": "016-access-pattern-driven-modeling.svg",
    "13-application-workloads.svg": "016-access-pattern-driven-modeling.svg",
    "14-read-write-access-patterns.svg": "017-read-and-write-access-patterns.svg",
    "15-data-accessed-together.svg": "018-data-accessed-together.svg",
    "16-data-changes-together.svg": "019-data-that-changes-together.svg",
    "17-relationship-types.svg": "023-mongodb-relationship-types.svg",
    "18-one-to-one.svg": "024-one-to-one-relationship.svg",
    "19-one-to-many.svg": "026-one-to-many-relationship.svg",
    "20-many-to-many.svg": "028-many-to-many-relationship.svg",
    "21-embedding.svg": "031-embedding-related-data.svg",
    "22-referencing.svg": "032-referencing-related-data.svg",
    "23-embed-vs-reference.svg": "033-embedding-vs-referencing.svg",
    "24-denormalization.svg": "041-intentional-data-duplication.svg",
    "25-historical-snapshots.svg": "042-historical-snapshot-modeling.svg",
    "26-product-catalog.svg": "055-product-document-model.svg",
    "27-customer-profile.svg": "059-customer-profile-document.svg",
    "28-order-aggregate.svg": "060-order-aggregate-document.svg",
    "29-time-series-events.svg": "000-time-series-events.svg",
    "30-unbounded-arrays.svg": "048-unbounded-array-antipattern.svg",
    "31-16mib-document-limit.svg": "050-16mib-bson-document-limit.svg",
    "32-document-growth.svg": "052-document-growth-decision-flow.svg",
    "33-schema-anti-patterns.svg": "088-schema-antipatterns-overview.svg",
    "34-schema-validation.svg": "065-flexible-schema-with-validation.svg",
    "35-json-schema-validation.svg": "066-schema-validation-flow.svg",
    "36-schema-evolution.svg": "072-schema-evolution-timeline.svg",
    "37-schema-patterns-overview.svg": "078-schema-pattern-overview.svg",
    "38-attribute-pattern.svg": "079-attribute-pattern.svg",
    "39-bucket-pattern.svg": "080-bucket-pattern.svg",
    "40-subset-pattern.svg": "081-subset-pattern.svg",
    "41-extended-reference-pattern.svg": "082-extended-reference-pattern.svg",
    "42-computed-pattern.svg": "083-computed-pattern.svg",
    "43-outlier-pattern.svg": "084-outlier-pattern.svg",
    "44-polymorphic-pattern.svg": "085-polymorphic-pattern.svg",
    "45-choosing-a-pattern.svg": "086-schema-pattern-selection-matrix.svg",
    "46-ecommerce-case-study.svg": "054-ecommerce-data-model-overview.svg",
    "47-module-3-concept-map.svg": "000-module-3-concept-map.svg",
    "48-ex-3-1-document-components.svg": "096-ex-3-1-label-the-document.svg",
    "49-ex-3-2-access-patterns.svg": "097-ex-3-2-access-pattern-worksheet.svg",
    "50-ex-3-3-embed-or-reference.svg": "098-ex-3-3-embed-or-reference-board.svg",
    "51-ex-3-7-select-pattern.svg": "102-ex-3-7-match-the-schema-pattern.svg",
    "52-lab-3-populate-flow.svg": "104-lab-3-1-training-database-structure.svg",
    "53-practical-challenge-ticket.svg": "111-practical-challenge-support-ticket.svg",
    "54-demo-embed-reference.svg": "039-hybrid-embedding-and-referencing.svg",
    "55-demo-schema-evolution.svg": "075-schema-version-strategy.svg",
    "56-day1-result-path.svg": "000-day1-result-path.svg",
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

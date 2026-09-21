"""Module 1 Marp diagrams — Mastering MongoDB.

Style tokens from marp_svg_common. Run:

    python scripts/module01_diagrams.py
"""
from __future__ import annotations

import html
from pathlib import Path

from marp_svg_common import BORDER, FONT, HEADER_BG, MONO, MUTED, PANEL, RED, TEXT

BG_BOX = "#ffffff"
ASSETS = Path(__file__).resolve().parent.parent / "slides" / "assets" / "module-01"
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
    title_y = y + (h / 2 + fs * 0.35 if not sub else h * 0.42)
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


def d01_landscape() -> str:
    body = "\n".join(
        [
            _box(30, 150, 230, 90, "Structured", "Tables · fixed schema"),
            _box(345, 150, 230, 90, "Semi-structured", "JSON · nested fields"),
            _box(660, 150, 230, 90, "Rapidly changing", "Variants · new attributes"),
            _arrow(260, 195, 345, 195),
            _arrow(575, 195, 660, 195),
            _label(460, 60, "Application data is no longer one rigid table shape", fs=20, fill=TEXT),
            _label(460, 100, "Traditional structured data  →  hierarchical, varied, continuously changing", fs=16),
            _label(460, 310, "Modern apps mix all three — the model must follow the access pattern", fs=16),
        ]
    )
    return _svg(360, body, "ae01")


def d02_data_categories() -> str:
    cols = [
        (24, "Structured", "Rows and columns", "SKU, price, quantity"),
        (318, "Semi-structured", "Nested JSON-like", "Product + specs + tags"),
        (612, "Unstructured", "No fixed fields", "Images, logs, video"),
    ]
    parts = [_label(460, 48, "Three data categories applications must store", fs=20, fill=TEXT)]
    for x, title, shape, example in cols:
        parts.append(_box(x, 80, 284, 70, title, header=True, fs=20))
        parts.append(_box(x, 160, 284, 80, shape, example, fs=18, sub_fs=16))
        parts.append(_box(x, 250, 284, 70, "Example", example, fs=16, sub_fs=16))
    return _svg(360, "\n".join(parts), "ae02")


def d03_relational_model() -> str:
    parts = [
        _box(300, 20, 320, 56, "Application", fs=20),
        _arrow(460, 76, 460, 108),
        _box(40, 120, 250, 70, "customers", "PK customer_id", fs=18),
        _box(335, 120, 250, 70, "orders", "PK order_id  FK customer_id", fs=18, sub_fs=14),
        _box(630, 120, 250, 70, "order_items", "FK order_id  FK product_id", fs=18, sub_fs=14),
        _box(335, 250, 250, 70, "products", "PK product_id", fs=18),
        _arrow(290, 155, 335, 155),
        _arrow(585, 155, 630, 155),
        _arrow(460, 190, 460, 250),
        _arrow(680, 190, 520, 250),
        _label(460, 360, "Normalized tables linked by primary and foreign keys", fs=16),
    ]
    return _svg(390, "\n".join(parts), "ae03")


def d04_relational_challenges() -> str:
    tables = ["customers", "addresses", "orders", "order_items", "payments"]
    parts = [_label(460, 40, "One business object split across many tables", fs=20, fill=TEXT)]
    for i, name in enumerate(tables):
        x = 30 + i * 178
        parts.append(_box(x, 70, 168, 64, name, fs=16))
        parts.append(_arrow(x + 84, 134, 460, 200))
    parts.append(_box(260, 210, 400, 80, "JOIN … JOIN … JOIN", "Reconstruct one complete order", fs=20))
    parts.append(_label(460, 330, "The application object and the stored shape diverge", fs=16))
    return _svg(360, "\n".join(parts), "ae04")


def d05_why_nosql() -> str:
    parts = [
        _box(310, 20, 300, 70, "Application growth", "Users · data variety · speed", fs=20),
        _box(30, 160, 200, 80, "Flexible schema", fs=18),
        _box(250, 160, 200, 80, "Horizontal scale", fs=18),
        _box(470, 160, 200, 80, "Availability", fs=18),
        _box(690, 160, 200, 80, "Faster delivery", fs=18),
        _arrow(400, 90, 130, 160),
        _arrow(430, 90, 350, 160),
        _arrow(490, 90, 570, 160),
        _arrow(520, 90, 790, 160),
        _label(460, 290, "NoSQL emerged to match how modern applications grow", fs=16),
    ]
    return _svg(330, "\n".join(parts), "ae05")


def d06_sql_vs_nosql() -> str:
    rows = [
        ("Schema", "Declared up front", "Flexible / evolving"),
        ("Storage", "Rows in tables", "Documents, keys, columns, graphs"),
        ("Relationships", "Joins on keys", "Embed, reference, or traverse"),
        ("Scaling", "Typically vertical", "Often horizontal"),
        ("Workloads", "Reporting, ledgers", "Apps, catalogs, events, graphs"),
    ]
    parts = [
        _box(24, 16, 220, 48, "Topic", header=True, fs=18),
        _box(244, 16, 328, 48, "SQL / relational", header=True, fs=18),
        _box(572, 16, 324, 48, "NoSQL family", header=True, fs=18),
    ]
    for i, (topic, sql, nosql) in enumerate(rows):
        y = 72 + i * 58
        parts.append(_box(24, y, 220, 50, topic, fs=16))
        parts.append(_box(244, y, 328, 50, sql, fs=16))
        parts.append(_box(572, y, 324, 50, nosql, fs=16))
    return _svg(370, "\n".join(parts), "ae06")


def d07_landscape() -> str:
    parts = [
        _box(330, 160, 260, 80, "NoSQL models", fs=20),
        _box(30, 30, 210, 80, "Document", "JSON-like records", fs=18),
        _box(680, 30, 210, 80, "Key-value", "Key → value", fs=18),
        _box(30, 280, 210, 80, "Column-family", "Sparse wide rows", fs=18),
        _box(680, 280, 210, 80, "Graph", "Nodes and edges", fs=18),
        _arrow(400, 160, 200, 110),
        _arrow(520, 160, 720, 110),
        _arrow(400, 240, 200, 280),
        _arrow(520, 240, 720, 280),
        _label(460, 390, "Four major models — pick from the access pattern, not the brand", fs=16),
    ]
    return _svg(420, "\n".join(parts), "ae07")


def d08_document_model() -> str:
    parts = [
        _box(40, 20, 840, 48, "Collection: products", header=True, fs=20),
        _box(40, 88, 400, 250, "", fs=16),
        _box(480, 88, 400, 250, "", fs=16),
        _label(240, 130, "Document A", fs=18, fill=TEXT),
        _label(80, 170, '{ _id, name, price,', fs=16, fill=TEXT, anchor="start"),
        _label(80, 198, "  specs: { ... },", fs=16, fill=TEXT, anchor="start"),
        _label(80, 226, "  colors: [ ... ] }", fs=16, fill=TEXT, anchor="start"),
        _label(240, 280, "Nested object + array", fs=16),
        _label(680, 130, "Document B", fs=18, fill=TEXT),
        _label(500, 170, '{ _id, name, price,', fs=16, fill=TEXT, anchor="start"),
        _label(500, 198, "  author, isbn }", fs=16, fill=TEXT, anchor="start"),
        _label(680, 250, "Different extra fields", fs=16),
    ]
    return _svg(360, "\n".join(parts), "ae08")


def d09_key_value() -> str:
    pairs = [
        ("session:98765", "{ userId, cartItems, expiresAt }"),
        ("cart:101", "[ { sku, qty }, { sku, qty } ]"),
        ("pref:101", "{ theme: dark, lang: en }"),
    ]
    parts = [_label(460, 40, "Unique key maps directly to a value", fs=20, fill=TEXT)]
    for i, (key, val) in enumerate(pairs):
        y = 70 + i * 90
        parts.append(_box(40, y, 280, 70, key, fs=18))
        parts.append(_arrow(320, y + 35, 380, y + 35))
        parts.append(_box(380, y, 500, 70, val, fs=16))
    return _svg(350, "\n".join(parts), "ae09")


def d10_column_family() -> str:
    parts = [
        _label(460, 36, "Rows with flexible columns, grouped by family", fs=20, fill=TEXT),
        _box(40, 60, 120, 260, "Row key", fs=16),
        _box(180, 60, 350, 260, "", fs=16),
        _box(550, 60, 330, 260, "", fs=16),
        _label(355, 95, "profile family", fs=18, fill=RED),
        _label(250, 140, "name", fs=16, fill=TEXT, anchor="start"),
        _label(250, 175, "email", fs=16, fill=TEXT, anchor="start"),
        _label(250, 210, "city   (row 2 only)", fs=16, fill=MUTED, anchor="start"),
        _label(715, 95, "metrics family", fs=18, fill=RED),
        _label(580, 140, "events_today", fs=16, fill=TEXT, anchor="start"),
        _label(580, 175, "last_seen", fs=16, fill=TEXT, anchor="start"),
        _label(460, 350, "Good for high-write, distributed, sparse workloads", fs=16),
    ]
    return _svg(380, "\n".join(parts), "ae10")


def d11_graph_model() -> str:
    parts = [
        _box(60, 140, 200, 80, "Customer", "Aisha", fs=18),
        _box(360, 40, 200, 80, "Customer", "Luis", fs=18),
        _box(360, 240, 200, 80, "Product", "Keyboard", fs=18),
        _box(660, 140, 200, 80, "Category", "Accessories", fs=18),
        _arrow(260, 160, 360, 100),
        _arrow(260, 200, 360, 260),
        _arrow(560, 280, 660, 200),
        _label(300, 120, "FOLLOWS", fs=14, fill=RED),
        _label(280, 250, "PURCHASED", fs=14, fill=RED),
        _label(620, 250, "BELONGS_TO", fs=14, fill=RED),
        _label(460, 360, "Nodes, relationships, and properties — the path is the query", fs=16),
    ]
    return _svg(390, "\n".join(parts), "ae11")


def d12_model_comparison() -> str:
    headers = ["", "Document", "Key-value", "Column-family", "Graph"]
    rows = [
        ("Structure", "JSON-like doc", "Key → value", "Wide sparse row", "Nodes + edges"),
        ("Access", "Query fields", "Lookup by key", "Column groups", "Traverse paths"),
        ("Use case", "Catalogs", "Sessions", "Telemetry", "Fraud / social"),
    ]
    xs = [16, 176, 362, 548, 734]
    ws = [160, 186, 186, 186, 170]
    parts = []
    for x, w, title in zip(xs, ws, headers):
        parts.append(_box(x, 16, w, 54, title or " ", header=True, fs=15))
    for r, row in enumerate(rows):
        y = 80 + r * 90
        for c, (x, w) in enumerate(zip(xs, ws)):
            parts.append(_box(x, y, w, 80, row[c], fs=15))
    return _svg(360, "\n".join(parts), "ae12")


def d13_decision_flow() -> str:
    parts = [
        _box(280, 16, 360, 56, "What does the workload need?", header=True, fs=18),
        _box(20, 120, 170, 90, "Connected paths", "Graph", fs=16),
        _box(200, 120, 170, 90, "Lookup by ID", "Key-value", fs=16),
        _box(380, 120, 170, 90, "Varied attributes", "Document", fs=16),
        _box(560, 120, 170, 90, "Strict transactions", "Relational", fs=16),
        _box(740, 120, 160, 90, "Massive writes", "Column-family", fs=16),
        _arrow(340, 72, 105, 120),
        _arrow(400, 72, 285, 120),
        _arrow(460, 72, 465, 120),
        _arrow(520, 72, 645, 120),
        _arrow(580, 72, 820, 120),
        _label(460, 250, "Start with relationships, flexibility, lookups, scale, and integrity", fs=16),
        _box(200, 280, 520, 56, "Then pick the product inside that model", fs=18),
    ]
    return _svg(360, "\n".join(parts), "ae13")


def d14_mongodb_in_landscape() -> str:
    parts = [
        _box(330, 150, 260, 80, "NoSQL models", fs=20),
        _box(20, 20, 250, 100, "Document", "MongoDB", header=True, fs=20),
        _box(650, 20, 250, 80, "Key-value", "Redis", fs=18),
        _box(20, 280, 250, 80, "Column-family", "Cassandra", fs=18),
        _box(650, 280, 250, 80, "Graph", "Neo4j", fs=18),
        _arrow(360, 160, 200, 120),
        _arrow(530, 160, 700, 100),
        _arrow(360, 230, 200, 280),
        _arrow(530, 230, 700, 280),
        _label(460, 400, "MongoDB is a general-purpose document database in this landscape", fs=16),
    ]
    return _svg(430, "\n".join(parts), "ae14")


def d15_hierarchy() -> str:
    labels = [
        "MongoDB server",
        "Database",
        "Collection",
        "Document",
        "Field  ·  nested object  ·  array",
    ]
    parts = []
    for i, label in enumerate(labels):
        y = 16 + i * 72
        parts.append(_box(180, y, 560, 56, label, fs=20 if i < 4 else 18))
        if i < len(labels) - 1:
            parts.append(_arrow(460, y + 56, 460, y + 72))
    return _svg(390, "\n".join(parts), "ae15")


def d16_terminology() -> str:
    rows = [
        ("Table", "Collection"),
        ("Row", "Document"),
        ("Column", "Field"),
        ("Primary key", "_id"),
        ("Join", "Embed, reference, or $lookup"),
    ]
    parts = [
        _box(40, 16, 400, 50, "Relational", header=True, fs=20),
        _box(480, 16, 400, 50, "MongoDB", header=True, fs=20),
    ]
    for i, (left, right) in enumerate(rows):
        y = 78 + i * 58
        parts.append(_box(40, y, 400, 50, left, fs=18))
        parts.append(_arrow(440, y + 25, 480, y + 25))
        parts.append(_box(480, y, 400, 50, right, fs=18))
    return _svg(380, "\n".join(parts), "ae16")


def d17_rows_vs_document() -> str:
    parts = [
        _box(24, 16, 420, 48, "Relational tables", header=True, fs=18),
        _box(476, 16, 420, 48, "One MongoDB document", header=True, fs=18),
        _box(54, 80, 360, 44, "customers", fs=16),
        _box(54, 136, 360, 44, "orders", fs=16),
        _box(54, 192, 360, 44, "order_items", fs=16),
        _box(54, 248, 360, 44, "addresses", fs=16),
        _label(234, 330, "Several joins to rebuild one order", fs=15),
        f'<rect x="476" y="80" width="420" height="212" rx="10" fill="{BG_BOX}" stroke="{RED}" stroke-width="2"/>',
        f'<text x="500" y="130" font-family="{MONO}" font-size="16" fill="{TEXT}">{{ _id: "O5001",</text>',
        f'<text x="500" y="162" font-family="{MONO}" font-size="16" fill="{TEXT}">  customer: {{ ... }},</text>',
        f'<text x="500" y="194" font-family="{MONO}" font-size="16" fill="{TEXT}">  items: [ {{ }}, {{ }} ],</text>',
        f'<text x="500" y="226" font-family="{MONO}" font-size="16" fill="{TEXT}">  total, status }}</text>',
        _label(686, 330, "One read for the same order", fs=15),
    ]
    return _svg(360, "\n".join(parts), "ae17")


def d18_anatomy() -> str:
    parts = [
        _box(40, 30, 520, 320, "", fs=16),
        f'<text x="64" y="80" font-family="{MONO}" font-size="18" fill="{TEXT}">{{</text>',
        f'<text x="64" y="112" font-family="{MONO}" font-size="18" fill="{TEXT}">  _id: ObjectId("…"),</text>',
        f'<text x="64" y="144" font-family="{MONO}" font-size="18" fill="{TEXT}">  name: "Aisha Khan",</text>',
        f'<text x="64" y="176" font-family="{MONO}" font-size="18" fill="{TEXT}">  total: 110.00,</text>',
        f'<text x="64" y="208" font-family="{MONO}" font-size="18" fill="{TEXT}">  paid: true,</text>',
        f'<text x="64" y="240" font-family="{MONO}" font-size="18" fill="{TEXT}">  createdAt: ISODate("…"),</text>',
        f'<text x="64" y="272" font-family="{MONO}" font-size="18" fill="{TEXT}">  customer: {{ city: "Toronto" }},</text>',
        f'<text x="64" y="304" font-family="{MONO}" font-size="18" fill="{TEXT}">  items: [ {{ sku, qty }} ]</text>',
        f'<text x="64" y="336" font-family="{MONO}" font-size="18" fill="{TEXT}">}}</text>',
        _box(590, 40, 300, 40, "_id  ObjectId", fs=16),
        _box(590, 90, 300, 40, "scalar string", fs=16),
        _box(590, 140, 300, 40, "number", fs=16),
        _box(590, 190, 300, 40, "Boolean", fs=16),
        _box(590, 240, 300, 40, "date", fs=16),
        _box(590, 290, 300, 40, "nested + array", fs=16),
        _arrow(400, 104, 590, 60),
        _arrow(400, 240, 590, 260),
        _arrow(400, 300, 590, 310),
    ]
    return _svg(380, "\n".join(parts), "ae18")


def d19_json_vs_bson() -> str:
    parts = [
        _box(24, 16, 430, 48, "JSON (application view)", header=True, fs=18),
        _box(466, 16, 430, 48, "BSON (MongoDB storage)", header=True, fs=18),
        _box(24, 80, 430, 250, "", fs=16),
        _box(466, 80, 430, 250, "", fs=16),
        f'<text x="48" y="130" font-family="{MONO}" font-size="16" fill="{TEXT}">{{ "name": "Aisha",</text>',
        f'<text x="48" y="162" font-family="{MONO}" font-size="16" fill="{TEXT}">  "total": 110.0,</text>',
        f'<text x="48" y="194" font-family="{MONO}" font-size="16" fill="{TEXT}">  "paid": true }}</text>',
        _label(239, 280, "Text · limited types", fs=16),
        f'<text x="490" y="130" font-family="{MONO}" font-size="16" fill="{TEXT}">_id: ObjectId</text>',
        f'<text x="490" y="162" font-family="{MONO}" font-size="16" fill="{TEXT}">total: Decimal128</text>',
        f'<text x="490" y="194" font-family="{MONO}" font-size="16" fill="{TEXT}">createdAt: UTC datetime</text>',
        _label(681, 280, "Binary · extra types", fs=16),
        _label(460, 360, "MongoDB displays JSON-like text and stores BSON", fs=16),
    ]
    return _svg(390, "\n".join(parts), "ae19")


def d20_flexible_schema() -> str:
    cards = [
        (24, "Laptop", "name, price, category", "processor, memory, screen"),
        (318, "Shoe", "name, price, category", "size, material, color"),
        (612, "Book", "name, price, category", "author, isbn, publisher"),
    ]
    parts = [_label(460, 40, "Same collection — shared core fields plus category-specific attributes", fs=18, fill=TEXT)]
    for x, title, core, extra in cards:
        parts.append(_box(x, 70, 284, 54, title, header=True, fs=18))
        parts.append(_box(x, 134, 284, 90, "Core", core, fs=16))
        parts.append(_box(x, 234, 284, 90, "Category fields", extra, fs=16))
    return _svg(350, "\n".join(parts), "ae20")


def d21_embed_vs_ref() -> str:
    parts = [
        _box(24, 16, 430, 48, "Embedding", header=True, fs=18),
        _box(466, 16, 430, 48, "Referencing", header=True, fs=18),
        _box(24, 80, 430, 220, "Order holds customer { }", "One read · possible staleness", fs=18),
        _box(466, 80, 430, 220, "Order holds customerId", "Two reads · always current", fs=18),
        _label(460, 340, "Store together what the application reads together", fs=16),
    ]
    return _svg(370, "\n".join(parts), "ae21")


def d22_architecture() -> str:
    layers = [
        "Client application",
        "MongoDB driver",
        "MongoDB server",
        "Database  →  collection  →  documents",
        "Storage engine + indexes",
    ]
    parts = []
    for i, label in enumerate(layers):
        y = 16 + i * 72
        parts.append(_box(160, y, 600, 56, label, fs=20))
        if i < len(layers) - 1:
            parts.append(_arrow(460, y + 56, 460, y + 72))
    return _svg(390, "\n".join(parts), "ae22")


def d23_request_flow() -> str:
    steps = [
        (16, "1. Query", "find(category)"),
        (198, "2. Driver", "Send command"),
        (380, "3. Planner", "Parse + plan"),
        (562, "4. Index", "Storage engine"),
        (744, "5. Results", "Matching docs"),
    ]
    parts = []
    for i, (x, title, sub) in enumerate(steps):
        parts.append(_box(x, 50, 160, 90, title, sub, fs=16, sub_fs=14))
        if i < len(steps) - 1:
            parts.append(_arrow(x + 160, 95, x + 198, 95))
    parts.append(_label(460, 180, "Schema, query, and indexes work together", fs=16))
    return _svg(220, "\n".join(parts), "ae23")


def d24_capabilities() -> str:
    spokes = [
        (40, 20, "Query"),
        (360, 20, "Aggregation"),
        (680, 20, "Indexing"),
        (40, 280, "Transactions"),
        (360, 280, "Replication"),
        (680, 280, "Sharding"),
    ]
    parts = [_box(310, 140, 300, 80, "MongoDB", fs=22)]
    for x, y, title in spokes:
        parts.append(_box(x, y, 200, 64, title, fs=18))
        parts.append(_arrow(x + 100, y + (64 if y < 140 else 0), 460, 160 if y < 140 else 220))
    return _svg(370, "\n".join(parts), "ae24")


def d25_deployment() -> str:
    parts = [
        _box(30, 80, 270, 160, "Local", "Developer laptop", fs=20),
        _box(325, 80, 270, 160, "Self-managed", "Your servers", fs=20),
        _box(620, 80, 270, 160, "Managed cloud", "Atlas", fs=20),
        _label(460, 40, "Same document model — three ways to run it", fs=20, fill=TEXT),
        _label(460, 280, "This course uses local or cloud; commands stay the same in mongosh", fs=16),
    ]
    return _svg(320, "\n".join(parts), "ae25")


def d26_use_case_map() -> str:
    items = [
        (24, 50, "Product catalogs"),
        (318, 50, "Customer profiles"),
        (612, 50, "Content management"),
        (24, 180, "IoT / events"),
        (318, 180, "Mobile / web apps"),
        (612, 180, "Operational data"),
    ]
    parts = [_label(460, 32, "Workloads that fit a document model", fs=20, fill=TEXT)]
    for x, y, title in items:
        parts.append(_box(x, y, 284, 100, title, fs=18))
    return _svg(310, "\n".join(parts), "ae26")


def d27_when_to_use() -> str:
    items = [
        "Flexible, hierarchical records",
        "Application-centered access",
        "Attributes that change often",
        "JSON APIs that match documents",
    ]
    parts = [_box(210, 16, 500, 50, "Use MongoDB when…", header=True, fs=20)]
    for i, item in enumerate(items):
        parts.append(_box(160, 84 + i * 64, 600, 54, item, fs=18))
    return _svg(360, "\n".join(parts), "ae27")


def d28_when_not() -> str:
    items = [
        "Complex relational reporting",
        "Specialized graph traversal",
        "Simple key-value cache only",
        "SQL-only tooling is mandatory",
    ]
    parts = [_box(160, 16, 600, 50, "MongoDB may not be the first choice when…", header=True, fs=18)]
    for i, item in enumerate(items):
        parts.append(_box(160, 84 + i * 64, 600, 54, item, fs=18))
    return _svg(360, "\n".join(parts), "ae28")


def d29_catalog_case() -> str:
    return d20_flexible_schema()


def d30_concept_map() -> str:
    nodes = [
        (40, 40, "NoSQL"),
        (250, 40, "Four models"),
        (460, 40, "Document DB"),
        (670, 40, "MongoDB"),
        (140, 200, "BSON"),
        (400, 200, "Collections"),
        (660, 200, "Documents"),
    ]
    parts = [_label(460, 20, "Module 1 path", fs=16)]
    for x, y, title in nodes:
        parts.append(_box(x, y + 20, 200, 70, title, fs=18))
    parts += [
        _arrow(240, 95, 250, 95),
        _arrow(450, 95, 460, 95),
        _arrow(660, 95, 670, 95),
        _arrow(740, 130, 740, 220),
        _arrow(500, 130, 500, 220),
        _arrow(770, 240, 660, 255),
        _arrow(460, 255, 340, 255),
        _label(460, 320, "NoSQL → models → document databases → MongoDB → BSON documents in collections", fs=15),
    ]
    return _svg(350, "\n".join(parts), "ae30")


def d31_ex11_cards() -> str:
    cards = [
        (24, "A Sessions", "Key-value?"),
        (178, "B Catalog", "Document?"),
        (332, "C Social", "Graph?"),
        (486, "D Ledger", "Relational?"),
        (640, "E Sensors", "Column-family?"),
        (794, "F CMS", "Document?"),
    ]
    # 6 cards of width 140 - 24+6*140 + gaps. Let me use 2 rows of 3.
    items = [
        (24, 70, "A  Sessions", "Lookup by session ID"),
        (318, 70, "B  Catalog", "Varied attributes"),
        (612, 70, "C  Social", "Traverse relationships"),
        (24, 200, "D  Ledger", "Strict transactions"),
        (318, 200, "E  Sensors", "High-volume writes"),
        (612, 200, "F  CMS", "Nested optional sections"),
    ]
    parts = [_label(460, 40, "Map each scenario to one model — justify from the access pattern", fs=18, fill=TEXT)]
    for x, y, title, sub in items:
        parts.append(_box(x, y, 284, 100, title, sub, fs=18))
    return _svg(330, "\n".join(parts), "ae31")


def d32_ex12_relational() -> str:
    parts = [
        _box(40, 40, 250, 80, "customers", "PK customer_id", fs=18),
        _box(335, 40, 250, 80, "orders", "PK order_id", fs=18),
        _box(630, 40, 250, 80, "order_items", "PK (order_id, product_id)", fs=16, sub_fs=14),
        _box(335, 220, 250, 80, "products", "PK product_id", fs=18),
        _arrow(290, 80, 335, 80),
        _arrow(585, 80, 630, 80),
        _arrow(460, 120, 460, 220),
        _arrow(700, 120, 520, 220),
        _label(460, 340, "Exercise 1.2 start: reconstruct order O5001 from these tables", fs=16),
    ]
    return _svg(370, "\n".join(parts), "ae32")


def d33_ex12_document() -> str:
    parts = [
        _box(160, 20, 600, 48, "orders document  _id: O5001", header=True, fs=18),
        _box(160, 88, 600, 70, "customer: { C101, Aisha Khan, email }", fs=16),
        _box(160, 174, 600, 110, "items: [ { P10 Keyboard }, { P22 Mouse } ]", fs=16),
        _box(160, 300, 290, 56, "status: PLACED", fs=16),
        _box(470, 300, 290, 56, "total: 110.00", fs=16),
    ]
    return _svg(380, "\n".join(parts), "ae33")


def d34_suitability() -> str:
    rows = [
        ("Varied product attrs", "Strong fit", "Document model"),
        ("Get order by id", "Strong fit", "One document read"),
        ("SQL-only reporting", "Weak fit", "Relational first"),
        ("Friend-of-friend graph", "Weak fit", "Graph first"),
    ]
    parts = [
        _box(20, 12, 300, 48, "Requirement", header=True, fs=16),
        _box(320, 12, 220, 48, "MongoDB fit", header=True, fs=16),
        _box(540, 12, 360, 48, "Why", header=True, fs=16),
    ]
    for i, (req, fit, why) in enumerate(rows):
        y = 70 + i * 62
        parts.append(_box(20, y, 300, 54, req, fs=16))
        parts.append(_box(320, y, 220, 54, fit, fs=16))
        parts.append(_box(540, y, 360, 54, why, fs=16))
    return _svg(330, "\n".join(parts), "ae34")


def d35_blank_callouts() -> str:
    parts = [
        _box(40, 30, 500, 300, "", fs=16),
        f'<text x="64" y="90" font-family="{MONO}" font-size="18" fill="{TEXT}">{{ _id, name, price,</text>',
        f'<text x="64" y="130" font-family="{MONO}" font-size="18" fill="{TEXT}">  inStock: true,</text>',
        f'<text x="64" y="170" font-family="{MONO}" font-size="18" fill="{TEXT}">  createdAt: ISODate,</text>',
        f'<text x="64" y="210" font-family="{MONO}" font-size="18" fill="{TEXT}">  specs: {{ }},</text>',
        f'<text x="64" y="250" font-family="{MONO}" font-size="18" fill="{TEXT}">  colors: [ ] }}</text>',
        _box(580, 40, 300, 48, "1. ________", fs=16),
        _box(580, 100, 300, 48, "2. ________", fs=16),
        _box(580, 160, 300, 48, "3. ________", fs=16),
        _box(580, 220, 300, 48, "4. ________", fs=16),
        _box(580, 280, 300, 48, "5. ________", fs=16),
        _label(460, 360, "Label: _id, scalar, Boolean, date, nested object, array", fs=16),
    ]
    return _svg(390, "\n".join(parts), "ae35")


def d36_flexible_products() -> str:
    return d20_flexible_schema()


def d37_training_store() -> str:
    parts = [
        _box(260, 16, 400, 56, "training_store", header=True, fs=20),
        _arrow(460, 72, 460, 104),
        _box(40, 110, 260, 160, "customers", "Buyer profiles", fs=20),
        _box(330, 110, 260, 160, "products", "Flexible catalog", fs=20),
        _box(620, 110, 260, 160, "orders", "Embedded items", fs=20),
        _label(460, 310, "Lab 1.3 dataset — one database, three collections", fs=16),
    ]
    return _svg(340, "\n".join(parts), "ae37")


def d38_navigation() -> str:
    steps = ["Connect", "show dbs", "use training_store", "show collections", "findOne()"]
    parts = []
    for i, label in enumerate(steps):
        x = 20 + i * 180
        parts.append(_box(x, 50, 168, 80, f"{i + 1}. {label}", fs=15))
        if i < len(steps) - 1:
            parts.append(_arrow(x + 168, 90, x + 180, 90))
    parts.append(_label(460, 170, "Connect → list databases → select → list collections → retrieve a document", fs=16))
    return _svg(210, "\n".join(parts), "ae38")


def d39_bson_types() -> str:
    return d18_anatomy()


def d40_challenge() -> str:
    steps = [
        (20, "Business need"),
        (250, "Access pattern"),
        (480, "Choose a model"),
        (710, "Sample document"),
    ]
    parts = []
    for i, (x, title) in enumerate(steps):
        parts.append(_box(x, 60, 190, 90, f"{i + 1}. {title}", fs=16))
        if i < len(steps) - 1:
            parts.append(_arrow(x + 190, 105, x + 250, 105))
    parts.append(_label(460, 190, "Module 1 practical path: requirements → pattern → model → document", fs=16))
    return _svg(230, "\n".join(parts), "ae40")


DIAGRAMS: dict[str, callable] = {
    "01-changing-application-data-landscape.svg": d01_landscape,
    "02-structured-semi-unstructured.svg": d02_data_categories,
    "03-relational-database-model.svg": d03_relational_model,
    "04-relational-data-challenges.svg": d04_relational_challenges,
    "05-why-nosql-emerged.svg": d05_why_nosql,
    "06-sql-vs-nosql.svg": d06_sql_vs_nosql,
    "07-nosql-database-landscape.svg": d07_landscape,
    "08-document-database-model.svg": d08_document_model,
    "09-key-value-database-model.svg": d09_key_value,
    "10-column-family-database-model.svg": d10_column_family,
    "11-graph-database-model.svg": d11_graph_model,
    "12-nosql-model-comparison.svg": d12_model_comparison,
    "13-database-selection-decision-flow.svg": d13_decision_flow,
    "14-mongodb-in-the-landscape.svg": d14_mongodb_in_landscape,
    "15-mongodb-data-hierarchy.svg": d15_hierarchy,
    "16-relational-to-mongodb-terminology.svg": d16_terminology,
    "17-rows-tables-vs-mongodb-document.svg": d17_rows_vs_document,
    "18-anatomy-of-a-mongodb-document.svg": d18_anatomy,
    "19-json-vs-bson.svg": d19_json_vs_bson,
    "20-flexible-schema-within-a-collection.svg": d20_flexible_schema,
    "21-embedding-vs-referencing-preview.svg": d21_embed_vs_ref,
    "22-mongodb-architecture-overview.svg": d22_architecture,
    "23-mongodb-request-flow.svg": d23_request_flow,
    "24-mongodb-core-capabilities.svg": d24_capabilities,
    "25-mongodb-deployment-options.svg": d25_deployment,
    "26-mongodb-use-case-map.svg": d26_use_case_map,
    "27-when-to-use-mongodb.svg": d27_when_to_use,
    "28-when-mongodb-may-not-fit.svg": d28_when_not,
    "29-ecommerce-product-catalog-case-study.svg": d29_catalog_case,
    "30-module-1-concept-map.svg": d30_concept_map,
    "31-ex-1-1-select-database-model.svg": d31_ex11_cards,
    "32-ex-1-2-relational-order-model.svg": d32_ex12_relational,
    "33-ex-1-2-mongodb-order-document.svg": d33_ex12_document,
    "34-ex-1-3-mongodb-suitability-matrix.svg": d34_suitability,
    "35-ex-1-4-document-component-identification.svg": d35_blank_callouts,
    "36-ex-1-5-flexible-product-schema.svg": d36_flexible_products,
    "37-lab-1-1-training-dataset-structure.svg": d37_training_store,
    "38-lab-1-1-mongodb-navigation-flow.svg": d38_navigation,
    "39-lab-1-1-bson-type-identification.svg": d39_bson_types,
    "40-module-1-practical-challenge.svg": d40_challenge,
}


def write_all() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        path = ASSETS / name
        path.write_text(fn(), encoding="utf-8")
        print(f"Wrote {path.relative_to(ASSETS.parent.parent.parent)}")
    return len(DIAGRAMS)


if __name__ == "__main__":
    n = write_all()
    print(f"Done. {n} diagrams.")

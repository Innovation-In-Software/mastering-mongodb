"""Module 8 Marp diagrams — Best Practices, Security, and Troubleshooting.

Style tokens from marp_svg_common. Run:

    python scripts/module08_diagrams.py
"""
from __future__ import annotations

import html
from pathlib import Path

from marp_svg_common import BORDER, FONT, HEADER_BG, MONO, MUTED, PANEL, RED, TEXT

BG_BOX = "#ffffff"
ASSETS = Path(__file__).resolve().parent.parent / "slides" / "assets" / "module-08"
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
        f'font-size="{fs}" fill="{TEXT if fill == TEXT else fill}">{_esc(text)}</text>'
    )


def _arrow(x1, y1, x2, y2, mid="ae") -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{RED}" '
        f'stroke-width="2" marker-end="url(#{mid})"/>'
    )


def _hflow(boxes: list[tuple[str, str | None]], *, y=60, h=90, gap=28, mid="ae", x0=20, box_w=160) -> list[str]:
    parts: list[str] = []
    x = x0
    n = len(boxes)
    if n > 1:
        usable = W - 40 - (n - 1) * gap
        box_w = min(box_w, usable // n)
    for i, (title, sub) in enumerate(boxes):
        parts.append(_box(x, y, box_w, h, title, sub, fs=15, sub_fs=13))
        if i < n - 1:
            parts.append(_arrow(x + box_w, y + h / 2, x + box_w + gap - 4, y + h / 2, mid))
        x += box_w + gap
    return parts


def _vflow(boxes: list[tuple[str, str | None]], *, x=260, y=20, w=400, h=52, gap=24, mid="ae") -> list[str]:
    parts: list[str] = []
    cy = y
    for i, (title, sub) in enumerate(boxes):
        parts.append(_box(x, cy, w, h, title, sub, fs=17 if sub else 18, sub_fs=14))
        if i < len(boxes) - 1:
            parts.append(_arrow(x + w / 2, cy + h, x + w / 2, cy + h + gap - 4, mid))
        cy += h + gap
    return parts


def _table(
    headers: list[str],
    rows: list[tuple[str, ...]],
    *,
    col_ws: list[int] | None = None,
    row_h=48,
    header_h=44,
    x0=20,
    y0=16,
    fs=15,
) -> list[str]:
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


def d01_module_map() -> str:
    parts = [
        _box(210, 12, 500, 44, "Production-ready MongoDB", header=True, fs=18),
        _box(20, 78, 140, 88, "Model", "Access patterns", fs=15, sub_fs=13),
        _box(172, 78, 140, 88, "Queries", "Indexes", fs=15, sub_fs=13),
        _box(324, 78, 140, 88, "Security", "Least privilege", fs=15, sub_fs=13),
        _box(476, 78, 140, 88, "Availability", "Replica / shard", fs=14, sub_fs=13),
        _box(628, 78, 130, 88, "Backup", "Tested restore", fs=15, sub_fs=13),
        _box(770, 78, 130, 88, "Ops", "Monitor + runbooks", fs=14, sub_fs=12),
        _label(460, 190, "Functional queries are necessary — not sufficient", fs=16),
    ]
    return _svg(210, "\n".join(parts), "ae01")


def d02_functional_vs_prod() -> str:
    rows = [
        ("Connects and stores", "Secure and least-privilege"),
        ("Queries return rows", "Available and scalable"),
        ("Demo on a laptop", "Observable, recoverable, tested"),
    ]
    return _svg(250, "\n".join(_table(["Functional", "Production-ready"], rows, col_ws=[430, 450], fs=16)), "ae02")


def d03_framework() -> str:
    rows = [
        ("1. Data model", "Access patterns, bounds, types"),
        ("2. Queries and indexes", "Explain evidence"),
        ("3. Security", "Identity, network, secrets"),
        ("4. Availability", "Replica set, shard plan"),
        ("5. Backup and recovery", "RPO, RTO, restore test"),
        ("6. Monitoring and ops", "Alerts, runbooks, owners"),
    ]
    return _svg(380, "\n".join(_table(["Review area", "Must show"], rows, col_ws=[300, 580], fs=15)), "ae03")


def d04_access_patterns() -> str:
    parts = _hflow(
        [
            ("Reads", "Filters + fields"),
            ("Writes", "Atomic unit"),
            ("Growth", "Arrays / size"),
            ("Retention", "History vs live"),
        ],
        y=40,
        h=110,
        box_w=200,
        gap=22,
        mid="ae04",
    )
    return _svg(190, "\n".join(parts), "ae04")


def d05_document_boundary() -> str:
    parts = [
        _box(40, 20, 400, 170, "Order aggregate", "items, prices, address snapshot, totals, status", fs=17, sub_fs=13),
        _box(480, 20, 400, 170, "Customer master", "independent lifecycle, reused, PII", fs=17, sub_fs=13),
        _arrow(440, 105, 476, 105, "ae05"),
        _label(460, 210, "Reference — do not copy live loyalty or password material onto the order", fs=14),
    ]
    return _svg(230, "\n".join(parts), "ae05")


def d06_embed_vs_ref() -> str:
    rows = [
        ("Owned, bounded, read together", "Embed"),
        ("Grows without a bound", "Reference"),
        ("Independent lifecycle", "Reference"),
        ("Need single-document atomicity", "Embed"),
        ("Widely shared master data", "Reference"),
    ]
    return _svg(330, "\n".join(_table(["When", "Choice"], rows, col_ws=[520, 360], fs=15)), "ae06")


def d07_unbounded() -> str:
    parts = _vflow(
        [
            ("Risky: all reviews on the product", None),
            ("Safer: reviews collection", None),
            ("Plus: subset, bucket, archive, TTL", None),
        ],
        x=180,
        y=16,
        w=560,
        h=48,
        gap=18,
        mid="ae07",
    )
    return _svg(220, "\n".join(parts), "ae07")


def d08_schema_evolution() -> str:
    parts = _hflow(
        [
            ("Compatible field", "Optional first"),
            ("Readers then writers", "Or dual-write"),
            ("Migrate old docs", "Monitor mix"),
            ("Tighten validation", "Then remove dead fields"),
        ],
        y=40,
        h=110,
        box_w=200,
        gap=18,
        mid="ae08",
    )
    return _svg(190, "\n".join(parts), "ae08")


def d09_snapshots() -> str:
    parts = [
        _box(40, 24, 400, 140, "Purchase-time facts", "name, price, address, tax, currency", fs=16, sub_fs=13),
        _box(480, 24, 400, 140, "Current catalog", "must not rewrite history", fs=16, sub_fs=13),
        _label(460, 190, "An order is a legal snapshot, not a live join to products", fs=15),
    ]
    return _svg(210, "\n".join(parts), "ae09")


def d10_anti_patterns() -> str:
    rows = [
        ("Relational copy-paste", "Unbounded arrays"),
        ("Mixed field types", "Oversized documents"),
        ("Deep unused nesting", "One collection, many entities"),
    ]
    return _svg(240, "\n".join(_table(["Smell", "Also a smell"], rows, col_ws=[440, 440], fs=16)), "ae10")


def d11_selective_filter() -> str:
    parts = [
        _mono(460, 36, "find({})   vs   customerId + PAID", fs=18),
        _box(40, 70, 400, 100, "Whole collection", "Server, network, client cost", fs=16, sub_fs=13),
        _box(480, 70, 400, 100, "Selective filter", "Indexed shape", fs=16, sub_fs=13),
    ]
    return _svg(200, "\n".join(parts), "ae11")


def d12_projection() -> str:
    parts = _hflow(
        [
            ("Full document", "Arrays + blobs"),
            ("Projection", "Needed fields"),
            ("Smaller payload", "Faster pages"),
        ],
        y=40,
        h=110,
        box_w=260,
        gap=30,
        mid="ae12",
    )
    return _svg(190, "\n".join(parts), "ae12")


def d13_bson_types() -> str:
    rows = [
        ("When", "BSON Date"),
        ("Money", "Decimal128"),
        ("Flag", "Boolean"),
        ("Quantity", "Int / Long"),
        ("Id", "ObjectId or stable business id"),
    ]
    return _svg(320, "\n".join(_table(["Data", "Type"], rows, col_ws=[300, 580], fs=15)), "ae13")


def d14_expensive() -> str:
    parts = [
        _box(20, 20, 280, 80, "Leading wildcard regex", None, fs=15),
        _box(320, 20, 280, 80, "Large skip pagination", None, fs=15),
        _box(620, 20, 280, 80, "Sort without index", None, fs=15),
        _box(20, 120, 280, 80, "Negative-only filters", None, fs=15),
        _box(320, 120, 280, 80, "Missing shard key", None, fs=15),
        _box(620, 120, 280, 80, "App-side joins", None, fs=15),
    ]
    return _svg(220, "\n".join(parts), "ae14")


def d15_early_match() -> str:
    parts = _vflow(
        [
            ("Large collection", None),
            ("Selective $match", None),
            ("Smaller working set", None),
            ("$unwind / $lookup / $group", None),
        ],
        x=210,
        y=12,
        w=500,
        h=42,
        gap=14,
        mid="ae15",
    )
    return _svg(250, "\n".join(parts), "ae15")


def d16_unwind() -> str:
    parts = [
        _box(80, 20, 320, 90, "100,000 orders", "10 items each", fs=16, sub_fs=14),
        _arrow(400, 65, 500, 65, "ae16"),
        _box(510, 20, 330, 90, "1,000,000 lines", "after $unwind", fs=16, sub_fs=14),
        _label(460, 140, "Filter and project first. Do not sum parent totals after unwind.", fs=15),
    ]
    return _svg(165, "\n".join(parts), "ae16")


def d17_lookup() -> str:
    parts = _hflow(
        [
            ("Need the join?", "Embed first?"),
            ("Index foreign field", "_id often yes"),
            ("Filter in pipeline", "Bound the array"),
        ],
        y=40,
        h=110,
        box_w=260,
        gap=30,
        mid="ae17",
    )
    return _svg(190, "\n".join(parts), "ae17")


def d18_validate_agg() -> str:
    parts = _hflow(
        [
            ("Tiny sample", "Hand totals"),
            ("Run pipeline", "Compare"),
            ("Nulls / TZ", "Unwind dupes"),
        ],
        y=40,
        h=110,
        box_w=260,
        gap=30,
        mid="ae18",
    )
    return _svg(190, "\n".join(parts), "ae18")


def d19_index_shape() -> str:
    parts = [
        _mono(460, 40, "customerId + PAID  sort createdAt -1", fs=18),
        _box(160, 80, 600, 80, "Index { customerId: 1, paymentStatus: 1, createdAt: -1 }", None, fs=16),
    ]
    return _svg(185, "\n".join(parts), "ae19")


def d20_index_cost() -> str:
    rows = [
        ("Faster selected reads", "Slower inserts/updates/deletes"),
        ("Covered queries", "More RAM, disk, backup, oplog"),
    ]
    return _svg(200, "\n".join(_table(["Benefit", "Cost"], rows, col_ws=[440, 440], fs=16)), "ae20")


def d21_redundant() -> str:
    parts = [
        _box(40, 24, 270, 90, "{ category: 1 }", "prefix", fs=16, sub_fs=13),
        _box(325, 24, 270, 90, "{ category: 1, price: 1 }", "covers prefix", fs=15, sub_fs=13),
        _box(610, 24, 270, 90, "Hide → monitor → drop", "never drop on sight", fs=14, sub_fs=13),
    ]
    return _svg(140, "\n".join(parts), "ae21")


def d22_explain() -> str:
    parts = _hflow(
        [
            ("COLLSCAN", "Whole collection"),
            ("IXSCAN", "Index keys"),
            ("FETCH / SORT", "Still count examined"),
        ],
        y=36,
        h=100,
        box_w=260,
        gap=30,
        mid="ae22",
    )
    return _svg(175, "\n".join(parts), "ae22")


def d23_security_layers() -> str:
    parts = [
        _box(20, 16, 170, 70, "Identity", None, fs=15),
        _box(200, 16, 170, 70, "Authn / Authz", None, fs=15),
        _box(380, 16, 170, 70, "Network", None, fs=15),
        _box(560, 16, 160, 70, "Encryption", None, fs=15),
        _box(730, 16, 170, 70, "Secrets", None, fs=15),
        _box(110, 106, 220, 70, "Audit", None, fs=15),
        _box(350, 106, 220, 70, "Patch", None, fs=15),
        _box(590, 106, 220, 70, "Backup + monitor", None, fs=15),
    ]
    return _svg(200, "\n".join(parts), "ae23")


def d24_least_privilege() -> str:
    rows = [
        ("Application", "readWrite app database"),
        ("Reporting", "read approved collections"),
        ("Backup", "backup privileges only"),
        ("Admin", "not in application code"),
    ]
    return _svg(280, "\n".join(_table(["Identity", "Ceiling"], rows, col_ws=[300, 580], fs=16)), "ae24")


def d25_network() -> str:
    parts = _vflow(
        [
            ("Private network / VPC", None),
            ("Allowlist + security groups", None),
            ("No public 27017", None),
            ("Split app vs admin paths", None),
        ],
        x=200,
        y=12,
        w=520,
        h=42,
        gap=14,
        mid="ae25",
    )
    return _svg(250, "\n".join(parts), "ae25")


def d26_encryption() -> str:
    parts = [
        _box(40, 24, 400, 130, "In transit (TLS)", "app, admins, replica members, backups", fs=17, sub_fs=13),
        _box(480, 24, 400, 130, "At rest", "disks, snapshots, exports, logs", fs=17, sub_fs=13),
    ]
    return _svg(180, "\n".join(parts), "ae26")


def d27_secrets() -> str:
    rows = [
        ("Never", "Source, images, slides, chat"),
        ("Instead", "Secret manager, rotation, per-env"),
    ]
    return _svg(190, "\n".join(_table(["Rule", "Detail"], rows, col_ws=[220, 660], fs=16)), "ae27")


def d28_sec_anti() -> str:
    parts = [
        _box(20, 20, 280, 80, "Auth disabled", None, fs=16),
        _box(320, 20, 280, 80, "Public port", None, fs=16),
        _box(620, 20, 280, 80, "Admin in the app", None, fs=16),
        _box(20, 120, 280, 80, "URI in Git", None, fs=16),
        _box(320, 120, 280, 80, "Open backups", None, fs=16),
        _box(620, 120, 280, 80, "Prod data in dev", None, fs=16),
    ]
    return _svg(220, "\n".join(parts), "ae28")


def d29_repl_vs_backup() -> str:
    rows = [
        ("Server failure", "Yes via failover", "No — need backup"),
        ("Drop / bad deploy", "Replicates the mistake", "Point-in-time restore"),
        ("Site loss", "If multi-region RS", "Offsite copies"),
    ]
    return _svg(250, "\n".join(_table(["Event", "Replica set", "Backup"], rows, col_ws=[250, 315, 315], fs=14)), "ae29")


def d30_rpo_rto() -> str:
    parts = [
        _box(40, 24, 400, 120, "RPO", "How much data loss is tolerable (time)", fs=20, sub_fs=14),
        _box(480, 24, 400, 120, "RTO", "How long restore may take", fs=20, sub_fs=14),
        _label(460, 170, "Backup frequency must beat RPO; procedure must beat RTO", fs=15),
    ]
    return _svg(195, "\n".join(parts), "ae30")


def d31_restore_test() -> str:
    parts = _hflow(
        [
            ("Backup job green", "Not enough"),
            ("Restore isolated", "Count + samples"),
            ("App can connect", "Indexes present"),
        ],
        y=36,
        h=110,
        box_w=260,
        gap=30,
        mid="ae31",
    )
    return _svg(185, "\n".join(parts), "ae31")


def d32_monitor() -> str:
    parts = [
        _box(20, 16, 210, 80, "Alive?", None, fs=16),
        _box(245, 16, 210, 80, "Fast enough?", None, fs=16),
        _box(470, 16, 210, 80, "Lag / disk?", None, fs=16),
        _box(695, 16, 205, 80, "Backup / auth?", None, fs=15),
        _label(460, 125, "Each tile must answer an on-call question", fs=16),
    ]
    return _svg(150, "\n".join(parts), "ae32")


def d33_alerts() -> str:
    rows = [
        ("Actionable", "Named owner + runbook"),
        ("Prioritized", "Critical is rare"),
        ("Quiet", "Thresholds vs baseline"),
    ]
    return _svg(230, "\n".join(_table(["Quality", "Meaning"], rows, col_ws=[280, 600], fs=16)), "ae33")


def d34_troubleshoot() -> str:
    parts = _vflow(
        [
            ("Symptom + when + blast radius", None),
            ("Recent change + metrics/logs", None),
            ("One hypothesis, one test", None),
            ("Verify + write the prevention", None),
        ],
        x=180,
        y=10,
        w=560,
        h=42,
        gap=14,
        mid="ae34",
    )
    return _svg(240, "\n".join(parts), "ae34")


def d35_slow_app() -> str:
    parts = _vflow(
        [
            ("Slow user request", None),
            ("App trace → DB op", None),
            ("Query shape + explain", None),
            ("Metrics → root cause", None),
        ],
        x=210,
        y=10,
        w=500,
        h=42,
        gap=14,
        mid="ae35",
    )
    return _svg(240, "\n".join(parts), "ae35")


def d36_safe_change() -> str:
    parts = _hflow(
        [
            ("Purpose + risk", "Baseline"),
            ("Test + backup", "Rollback"),
            ("Gradual apply", "Monitor"),
        ],
        y=36,
        h=110,
        box_w=260,
        gap=30,
        mid="ae36",
    )
    return _svg(185, "\n".join(parts), "ae36")


def d37_incident() -> str:
    parts = _hflow(
        [
            ("Detect", None),
            ("Stabilize", None),
            ("Diagnose", None),
            ("Recover", None),
            ("Review", None),
        ],
        y=40,
        h=100,
        box_w=150,
        gap=18,
        mid="ae37",
    )
    return _svg(180, "\n".join(parts), "ae37")


def d38_checklist() -> str:
    parts = [
        _box(20, 16, 210, 90, "Model", "Bounds + types", fs=16, sub_fs=13),
        _box(245, 16, 210, 90, "Perf", "Explain + baseline", fs=16, sub_fs=13),
        _box(470, 16, 210, 90, "Security", "Authn + network", fs=16, sub_fs=13),
        _box(695, 16, 205, 90, "Ops", "Backup + alerts", fs=16, sub_fs=13),
    ]
    return _svg(130, "\n".join(parts), "ae38")


def d39_architecture() -> str:
    parts = _vflow(
        [
            ("Application + secrets", None),
            ("TLS driver → replica set / mongos", None),
            ("products | customers | orders | reviews", None),
            ("Indexes, validation, backup, monitors", None),
        ],
        x=140,
        y=10,
        w=640,
        h=42,
        gap=14,
        mid="ae39",
    )
    return _svg(240, "\n".join(parts), "ae39")


def d40_course_map() -> str:
    parts = [
        _box(20, 20, 210, 80, "M1–3 Model", None, fs=16),
        _box(245, 20, 210, 80, "M4–5 Query/Agg", None, fs=16),
        _box(470, 20, 210, 80, "M6 Indexes", None, fs=16),
        _box(695, 20, 205, 80, "M7 HA / shard", None, fs=16),
        _box(210, 120, 500, 70, "M8 Production-ready operations", header=True, fs=17),
    ]
    return _svg(210, "\n".join(parts), "ae40")


def d41_demo_model() -> str:
    parts = [
        _box(40, 20, 400, 140, "Before", "string price, reviews[], mixed names", fs=18, sub_fs=14),
        _box(480, 20, 400, 140, "After", "Decimal128, reviews coll, validator", fs=18, sub_fs=14),
    ]
    return _svg(180, "\n".join(parts), "ae41")


def d42_lab_challenge() -> str:
    parts = _hflow(
        [
            ("Schema + validation", None),
            ("Pipeline + indexes", None),
            ("Security + backup", None),
            ("Alerts + runbook", None),
        ],
        y=36,
        h=110,
        box_w=200,
        gap=20,
        mid="ae42",
    )
    return _svg(185, "\n".join(parts), "ae42")


def d43_connection() -> str:
    parts = _vflow(
        [
            ("URI, DNS, port, TLS", None),
            ("Firewall / allowlist", None),
            ("Auth source + roles", None),
            ("Pool timeouts + discovery", None),
        ],
        x=200,
        y=12,
        w=520,
        h=42,
        gap=14,
        mid="ae43",
    )
    return _svg(250, "\n".join(parts), "ae43")


def d44_baseline() -> str:
    rows = [
        ("Latency + ops/s", "Normal Tuesday"),
        ("CPU, disk, connections", "Peak vs idle"),
        ("Lag, backup duration", "Growth trend"),
    ]
    return _svg(230, "\n".join(_table(["Signal", "Why record it"], rows, col_ws=[360, 520], fs=16)), "ae44")


def d45_day3_close() -> str:
    parts = _hflow(
        [
            ("Indexed shapes", "Module 6"),
            ("Replica / shard", "Module 7"),
            ("Ready to operate", "Module 8"),
        ],
        y=36,
        h=110,
        box_w=260,
        gap=30,
        mid="ae45",
    )
    return _svg(185, "\n".join(parts), "ae45")


DIAGRAMS = {
    "01-module-map.svg": d01_module_map,
    "02-functional-vs-prod.svg": d02_functional_vs_prod,
    "03-framework.svg": d03_framework,
    "04-access-patterns.svg": d04_access_patterns,
    "05-document-boundary.svg": d05_document_boundary,
    "06-embed-vs-ref.svg": d06_embed_vs_ref,
    "07-unbounded.svg": d07_unbounded,
    "08-schema-evolution.svg": d08_schema_evolution,
    "09-snapshots.svg": d09_snapshots,
    "10-anti-patterns.svg": d10_anti_patterns,
    "11-selective-filter.svg": d11_selective_filter,
    "12-projection.svg": d12_projection,
    "13-bson-types.svg": d13_bson_types,
    "14-expensive.svg": d14_expensive,
    "15-early-match.svg": d15_early_match,
    "16-unwind.svg": d16_unwind,
    "17-lookup.svg": d17_lookup,
    "18-validate-agg.svg": d18_validate_agg,
    "19-index-shape.svg": d19_index_shape,
    "20-index-cost.svg": d20_index_cost,
    "21-redundant.svg": d21_redundant,
    "22-explain.svg": d22_explain,
    "23-security-layers.svg": d23_security_layers,
    "24-least-privilege.svg": d24_least_privilege,
    "25-network.svg": d25_network,
    "26-encryption.svg": d26_encryption,
    "27-secrets.svg": d27_secrets,
    "28-sec-anti.svg": d28_sec_anti,
    "29-repl-vs-backup.svg": d29_repl_vs_backup,
    "30-rpo-rto.svg": d30_rpo_rto,
    "31-restore-test.svg": d31_restore_test,
    "32-monitor.svg": d32_monitor,
    "33-alerts.svg": d33_alerts,
    "34-troubleshoot.svg": d34_troubleshoot,
    "35-slow-app.svg": d35_slow_app,
    "36-safe-change.svg": d36_safe_change,
    "37-incident.svg": d37_incident,
    "38-checklist.svg": d38_checklist,
    "39-architecture.svg": d39_architecture,
    "40-course-map.svg": d40_course_map,
    "41-demo-model.svg": d41_demo_model,
    "42-lab-challenge.svg": d42_lab_challenge,
    "43-connection.svg": d43_connection,
    "44-baseline.svg": d44_baseline,
    "45-day3-close.svg": d45_day3_close,
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

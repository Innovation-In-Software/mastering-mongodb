"""Module 7 Marp diagrams — Replication and Sharding.

Style tokens from marp_svg_common. Run:

    python scripts/module07_diagrams.py
"""
from __future__ import annotations

import html
from pathlib import Path

from marp_svg_common import BORDER, FONT, HEADER_BG, MONO, MUTED, PANEL, RED, TEXT

BG_BOX = "#ffffff"
ASSETS = Path(__file__).resolve().parent.parent / "slides" / "assets" / "module-07"
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


def _vline(x, y1, y2, mid="ae") -> str:
    return _arrow(x, y1, x, y2, mid)


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
        _box(210, 12, 500, 48, "Replication and Sharding", header=True, fs=18),
        _box(20, 80, 280, 100, "Availability", "Replica sets, elections", fs=17, sub_fs=14),
        _box(320, 80, 280, 100, "Guarantees", "Read / write / lag", fs=17, sub_fs=14),
        _box(620, 80, 280, 100, "Scale", "Shards, keys, routing", fs=17, sub_fs=14),
        _label(460, 210, "Copy data for failover. Partition data for growth. Often both.", fs=15),
    ]
    return _svg(240, "\n".join(parts), "ae01")


def d02_requirements() -> str:
    rows = [
        ("Stay up during failure", "Availability"),
        ("Recover from outages", "Availability"),
        ("More data and requests", "Scale"),
        ("Users in many places", "Scale + placement"),
        ("Durability and latency", "Guarantees"),
    ]
    return _svg(330, "\n".join(_table(["Business need", "Architecture lens"], rows, col_ws=[460, 420], fs=15)), "ae02")


def d03_ha_vs_scale() -> str:
    parts = [
        _box(40, 20, 400, 150, "High availability", "Replica sets keep a primary writable", fs=20, sub_fs=14),
        _box(480, 20, 400, 150, "Horizontal scale", "Sharding spreads data and work", fs=20, sub_fs=14),
        _label(460, 200, "Same dataset copied  vs  different ranges on different shards", fs=15),
    ]
    return _svg(230, "\n".join(parts), "ae03")


def d04_vertical_horizontal() -> str:
    parts = [
        _box(40, 20, 400, 160, "Vertical", "Bigger CPU, RAM, disk on one host", fs=20, sub_fs=14),
        _box(480, 20, 400, 160, "Horizontal", "More hosts, more complexity", fs=20, sub_fs=14),
        _label(460, 210, "Vertical is simpler until hardware and cost hit a wall", fs=15),
    ]
    return _svg(240, "\n".join(parts), "ae04")


def d05_repl_vs_shard() -> str:
    rows = [
        ("Copies the dataset", "Partitions the dataset"),
        ("Failover and redundancy", "Storage and throughput"),
        ("Primary + secondaries", "Multiple shards"),
        ("Same data on members", "Different ranges per shard"),
    ]
    return _svg(300, "\n".join(_table(["Replication", "Sharding"], rows, col_ws=[440, 440], fs=15)), "ae05")


def d06_distributed() -> str:
    parts = [
        _box(310, 12, 300, 44, "Application + driver", header=True, fs=16),
        _arrow(460, 56, 460, 78, "ae06"),
        _box(310, 80, 300, 44, "mongos router", fs=16),
        _arrow(360, 124, 160, 156, "ae06"),
        _arrow(460, 124, 460, 156, "ae06"),
        _arrow(560, 124, 760, 156, "ae06"),
        _box(40, 158, 240, 80, "Shard A", "Replica set", fs=16, sub_fs=13),
        _box(340, 158, 240, 80, "Shard B", "Replica set", fs=16, sub_fs=13),
        _box(640, 158, 240, 80, "Shard C", "Replica set", fs=16, sub_fs=13),
        _label(460, 262, "Config servers hold routing metadata, not application documents", fs=14),
    ]
    return _svg(285, "\n".join(parts), "ae06")


def d07_replica_set() -> str:
    parts = [
        _box(40, 50, 220, 140, "Primary", "Writes + oplog", fs=18, sub_fs=14),
        _box(350, 20, 220, 100, "Secondary", "Replicates", fs=17, sub_fs=13),
        _box(350, 140, 220, 100, "Secondary", "Can be elected", fs=17, sub_fs=13),
        _arrow(260, 90, 350, 70, "ae07"),
        _arrow(260, 140, 350, 190, "ae07"),
        _box(650, 70, 240, 100, "Odd voters", "Majority elects", fs=17, sub_fs=13),
    ]
    return _svg(260, "\n".join(parts), "ae07")


def d08_members() -> str:
    rows = [
        ("Primary", "Accepts writes"),
        ("Secondary", "Copy; may be elected"),
        ("Hidden", "Not for app reads"),
        ("Delayed", "Intentional lag"),
        ("Arbiter", "Vote only; no data"),
    ]
    return _svg(330, "\n".join(_table(["Member", "Role"], rows, col_ws=[300, 580], fs=15)), "ae08")


def d09_primary() -> str:
    return _svg(
        280,
        "\n".join(
            _vflow(
                [
                    ("Accept application writes", None),
                    ("Apply locally and record oplog", None),
                    ("Serve primary-preference reads", None),
                    ("Only one primary at a time", None),
                ],
                x=210,
                y=16,
                w=500,
                h=46,
                gap=16,
                mid="ae09",
            )
        ),
        "ae09",
    )


def d10_secondary() -> str:
    parts = [
        _box(40, 30, 400, 140, "Copy + apply oplog", "In order, continuously", fs=18, sub_fs=14),
        _box(480, 30, 400, 140, "Election eligible", "Not a passive backup", fs=18, sub_fs=14),
        _label(460, 200, "May serve reads only when the read preference allows it", fs=15),
    ]
    return _svg(230, "\n".join(parts), "ae10")


def d11_oplog() -> str:
    return _svg(
        300,
        "\n".join(
            _vflow(
                [
                    ("Application write", None),
                    ("Primary applies + oplog entry", None),
                    ("Secondaries copy the entry", None),
                    ("Secondaries apply locally", None),
                ],
                x=210,
                y=12,
                w=500,
                h=50,
                gap=16,
                mid="ae11",
            )
        ),
        "ae11",
    )


def d12_repl_flow() -> str:
    parts = _hflow(
        [
            ("Driver", "Finds primary"),
            ("Primary", "Write + oplog"),
            ("Secondaries", "Copy + apply"),
            ("Ack", "Write concern"),
        ],
        y=50,
        h=120,
        box_w=190,
        gap=22,
        mid="ae12",
    )
    parts.append(_label(460, 200, "Acknowledgment timing depends on write concern", fs=15))
    return _svg(230, "\n".join(parts), "ae12")


def d13_heartbeats() -> str:
    parts = [
        _box(340, 20, 240, 60, "Members", header=True, fs=16),
        _arrow(360, 80, 160, 120, "ae13"),
        _arrow(460, 80, 460, 120, "ae13"),
        _arrow(560, 80, 760, 120, "ae13"),
        _box(40, 122, 240, 80, "Reachable?", None, fs=16),
        _box(340, 122, 240, 80, "Who is primary?", None, fs=16),
        _box(640, 122, 240, 80, "Elect now?", None, fs=16),
        _label(460, 230, "Heartbeats carry health, not application documents", fs=15),
    ]
    return _svg(255, "\n".join(parts), "ae13")


def d14_elections() -> str:
    rows = [
        ("Primary unavailable", "Eligible voters elect"),
        ("Primary steps down", "Controlled change"),
        ("Config / network change", "Majority still required"),
        ("Better candidate", "Priority can influence"),
    ]
    return _svg(280, "\n".join(_table(["Trigger", "What happens"], rows, col_ws=[400, 480], fs=15)), "ae14")


def d15_failover() -> str:
    return _svg(
        300,
        "\n".join(
            _vflow(
                [
                    ("Primary failure detected", None),
                    ("Election among eligible voters", None),
                    ("New primary accepts writes", None),
                    ("Drivers rediscover topology", None),
                ],
                x=210,
                y=12,
                w=500,
                h=50,
                gap=16,
                mid="ae15",
            )
        ),
        "ae15",
    )


def d16_app_failover() -> str:
    rows = [
        ("Replica-set URI", "Not a single host forever"),
        ("Supported driver", "SDAM + server selection"),
        ("Retryable ops", "Transient election window"),
        ("Idempotent writes", "Safe to retry"),
    ]
    return _svg(280, "\n".join(_table(["Application need", "Why"], rows, col_ws=[360, 520], fs=15)), "ae16")


def d17_majority() -> str:
    parts = [
        _box(40, 20, 270, 140, "Member A", "Votes", fs=18, sub_fs=14),
        _box(325, 20, 270, 140, "Member B", "Votes", fs=18, sub_fs=14),
        _box(610, 20, 270, 140, "Member C", "Isolated", fs=18, sub_fs=14),
        _label(460, 190, "A+B = majority. Isolated C cannot elect itself.", fs=16),
        _label(460, 218, "Protects against two writable primaries", fs=14),
    ]
    return _svg(245, "\n".join(parts), "ae17")


def d18_priority() -> str:
    parts = [
        _box(40, 30, 400, 140, "Higher priority", "Preferred primary DC", fs=18, sub_fs=14),
        _box(480, 30, 400, 140, "Priority 0", "Will not become primary", fs=18, sub_fs=14),
        _label(460, 200, "Priority is election preference, not a read router", fs=15),
    ]
    return _svg(230, "\n".join(parts), "ae18")


def d19_arbiter() -> str:
    parts = [
        _box(40, 20, 840, 50, "Arbiter votes but stores no application data", header=True, fs=16),
        _box(40, 90, 260, 100, "Cannot be primary", None, fs=16),
        _box(330, 90, 260, 100, "No extra copy", None, fs=16),
        _box(620, 90, 260, 100, "No extra reads", None, fs=16),
        _label(460, 220, "Prefer a data-bearing voting member when resources allow", fs=15),
    ]
    return _svg(250, "\n".join(parts), "ae19")


def d20_hidden() -> str:
    parts = [
        _box(40, 30, 400, 140, "Full data copy", "Backup / reporting node", fs=18, sub_fs=14),
        _box(480, 30, 400, 140, "Hidden from drivers", "Not selected for app reads", fs=18, sub_fs=14),
        _label(460, 200, "Hidden does not mean disconnected or unprotected", fs=15),
    ]
    return _svg(230, "\n".join(parts), "ae20")


def d21_delayed() -> str:
    parts = [
        _box(210, 16, 500, 50, "Primary now", header=True, fs=16),
        _arrow(460, 66, 460, 96, "ae21"),
        _box(210, 98, 500, 70, "Delayed secondary", "Applies after configured lag", fs=18, sub_fs=14),
        _label(460, 195, "Useful for some accidents — not a backup substitute", fs=15),
    ]
    return _svg(220, "\n".join(parts), "ae21")


def d22_read_pref() -> str:
    rows = [
        ("primary", "Current primary only"),
        ("primaryPreferred", "Primary, else secondary"),
        ("secondary", "Secondaries only"),
        ("secondaryPreferred", "Secondary, else primary"),
        ("nearest", "Lowest-latency eligible"),
    ]
    return _svg(330, "\n".join(_table(["Mode", "Who may serve reads"], rows, col_ws=[360, 520], fs=15)), "ae22")


def d23_write_concern() -> str:
    parts = [
        _box(40, 20, 270, 140, "Primary ack", "Faster, less confirmation", fs=17, sub_fs=13),
        _box(325, 20, 270, 140, "Majority", "Voting data-bearing majority", fs=17, sub_fs=13),
        _box(610, 20, 270, 140, "Numeric w", "N members acknowledge", fs=17, sub_fs=13),
        _label(460, 190, "Stronger acknowledgment usually costs latency", fs=15),
    ]
    return _svg(220, "\n".join(parts), "ae23")


def d24_three_settings() -> str:
    rows = [
        ("Read preference", "Which member serves the read?"),
        ("Read concern", "What visibility guarantee?"),
        ("Write concern", "What acknowledgment for a write?"),
    ]
    return _svg(240, "\n".join(_table(["Setting", "Question it answers"], rows, col_ws=[320, 560], fs=15)), "ae24")


def d25_lag() -> str:
    parts = [
        _box(40, 30, 360, 120, "Primary applied T0", None, fs=18),
        _arrow(400, 90, 520, 90, "ae25"),
        _box(520, 30, 360, 120, "Secondary applied T0+lag", None, fs=18),
        _label(460, 180, "Lag affects freshness, failover readiness, oplog window", fs=15),
    ]
    return _svg(210, "\n".join(parts), "ae25")


def d26_rollback() -> str:
    parts = [
        _box(40, 20, 400, 140, "Former primary", "Writes not on new history", fs=18, sub_fs=14),
        _box(480, 20, 400, 140, "Current primary", "Authoritative oplog", fs=18, sub_fs=14),
        _label(460, 190, "Majority write concern reduces rollback risk", fs=15),
    ]
    return _svg(220, "\n".join(parts), "ae26")


def d27_rs_status() -> str:
    parts = [
        _mono(460, 40, "rs.status()   rs.conf()", fs=20),
        _box(40, 80, 270, 90, "States", "PRIMARY / SECONDARY", fs=16, sub_fs=13),
        _box(325, 80, 270, 90, "Health", "Reachable members", fs=16, sub_fs=13),
        _box(610, 80, 270, 90, "Lag", "Optimes / timestamps", fs=16, sub_fs=13),
    ]
    return _svg(200, "\n".join(parts), "ae27")


def d28_failures() -> str:
    rows = [
        ("One secondary down", "Primary usually stays writable"),
        ("Primary down, majority up", "Election; brief write pause"),
        ("No voting majority", "No writable primary"),
    ]
    return _svg(240, "\n".join(_table(["Scenario", "Typical outcome"], rows, col_ws=[400, 480], fs=15)), "ae28")


def d29_sharding() -> str:
    parts = [
        _box(40, 40, 250, 140, "Shard A", "Range 1", fs=18, sub_fs=14),
        _box(335, 40, 250, 140, "Shard B", "Range 2", fs=18, sub_fs=14),
        _box(630, 40, 250, 140, "Shard C", "Range 3", fs=18, sub_fs=14),
        _label(460, 210, "One logical collection, partitioned storage", fs=16),
    ]
    return _svg(240, "\n".join(parts), "ae29")


def d30_components() -> str:
    parts = [
        _box(310, 12, 300, 44, "Application", header=True, fs=16),
        _arrow(460, 56, 460, 76, "ae30"),
        _box(310, 78, 300, 44, "mongos", fs=16),
        _arrow(360, 122, 180, 150, "ae30"),
        _arrow(560, 122, 740, 150, "ae30"),
        _box(40, 152, 340, 80, "Shards (replica sets)", "Application data", fs=16, sub_fs=13),
        _box(540, 152, 340, 80, "Config replica set", "Cluster metadata", fs=16, sub_fs=13),
    ]
    return _svg(255, "\n".join(parts), "ae30")


def d31_shards() -> str:
    parts = [
        _box(40, 30, 400, 140, "Subset of data", "Not the whole collection", fs=18, sub_fs=14),
        _box(480, 30, 400, 140, "Usually a replica set", "HA inside each partition", fs=18, sub_fs=14),
        _label(460, 200, "Shard failure is independent of other shards' primaries", fs=15),
    ]
    return _svg(230, "\n".join(parts), "ae31")


def d32_csrs() -> str:
    rows = [
        ("Sharded collections", "Which DBs and collections"),
        ("Shard keys", "How documents are placed"),
        ("Ranges / chunks", "What lives where"),
        ("Zones", "Placement rules"),
    ]
    return _svg(280, "\n".join(_table(["Metadata", "Purpose"], rows, col_ws=[360, 520], fs=15)), "ae32")


def d33_mongos() -> str:
    return _svg(
        280,
        "\n".join(
            _vflow(
                [
                    ("Accept client request", None),
                    ("Read routing metadata", None),
                    ("Target shard(s) and merge", None),
                    ("Return result — no app data stored", None),
                ],
                x=180,
                y=12,
                w=560,
                h=48,
                gap=14,
                mid="ae33",
            )
        ),
        "ae33",
    )


def d34_request_flow() -> str:
    parts = _hflow(
        [
            ("App", "Driver"),
            ("mongos", "Route"),
            ("Shard(s)", "Execute"),
            ("Merge", "Reply"),
        ],
        y=50,
        h=110,
        box_w=190,
        gap=22,
        mid="ae34",
    )
    return _svg(200, "\n".join(parts), "ae34")


def d35_shard_key() -> str:
    parts = [
        _mono(460, 36, "{ customerId: 1 }", fs=20),
        _mono(460, 68, '{ tenantId: 1, createdAt: 1 }', fs=16),
        _mono(460, 100, '{ customerId: "hashed" }', fs=16),
        _label(460, 150, "The most important sharding decision", fs=16),
        _label(460, 178, "No universally ideal key — workload decides", fs=14),
    ]
    return _svg(205, "\n".join(parts), "ae35")


def d36_cardinality() -> str:
    parts = [
        _box(40, 30, 400, 140, "Low", "NEW, PAID, SHIPPED", fs=20, sub_fs=15),
        _box(480, 30, 400, 140, "High", "customerId, orderId", fs=20, sub_fs=15),
        _label(460, 200, "Low cardinality cannot split work finely", fs=15),
    ]
    return _svg(230, "\n".join(parts), "ae36")


def d37_frequency() -> str:
    parts = [
        _box(40, 30, 520, 140, "Tenant A = 80% of traffic", "Hot shard risk", fs=18, sub_fs=14),
        _box(580, 30, 300, 140, "Others 20%", "Cold shards", fs=18, sub_fs=14),
        _label(460, 200, "High cardinality is not enough if values are skewed", fs=15),
    ]
    return _svg(230, "\n".join(parts), "ae37")


def d38_monotonic() -> str:
    parts = [
        _box(40, 20, 840, 50, "Increasing createdAt or sequence IDs", header=True, fs=16),
        _arrow(80, 90, 840, 90, "ae38"),
        _box(680, 110, 200, 70, "Hot max range", None, fs=15),
        _label(460, 210, "Ranged sharding can send all new writes to one chunk", fs=15),
    ]
    return _svg(240, "\n".join(parts), "ae38")


def d39_isolation() -> str:
    parts = [
        _mono(460, 36, 'db.orders.find({ customerId: "C101" })', fs=16),
        _box(40, 70, 400, 110, "Shard-key predicate", "Router can target", fs=18, sub_fs=14),
        _box(480, 70, 400, 110, "No shard-key field", "Often scatter-gather", fs=18, sub_fs=14),
    ]
    return _svg(210, "\n".join(parts), "ae39")


def d40_ranged() -> str:
    parts = [
        _box(40, 40, 260, 120, "A–F", "Shard A", fs=20, sub_fs=15),
        _box(330, 40, 260, 120, "G–M", "Shard B", fs=20, sub_fs=15),
        _box(620, 40, 260, 120, "N–Z", "Shard C", fs=20, sub_fs=15),
        _label(460, 190, "Preserves order and locality; can hotspot", fs=15),
    ]
    return _svg(220, "\n".join(parts), "ae40")


def d41_hashed() -> str:
    return _svg(
        260,
        "\n".join(
            _vflow(
                [
                    ("customerId value", None),
                    ("Hash function", None),
                    ("Hash range on a shard", None),
                ],
                x=230,
                y=16,
                w=460,
                h=52,
                gap=18,
                mid="ae41",
            )
        ),
        "ae41",
    )


def d42_zoned() -> str:
    parts = [
        _box(40, 30, 400, 140, "Canada ranges", "Canada zone / shards", fs=18, sub_fs=14),
        _box(480, 30, 400, 140, "Europe ranges", "Europe zone / shards", fs=18, sub_fs=14),
        _label(460, 200, "Residency and hardware tiers — operationally heavy", fs=15),
    ]
    return _svg(230, "\n".join(parts), "ae42")


def d43_ranged_vs_hashed() -> str:
    rows = [
        ("Order preserved", "Hashes scramble order"),
        ("Range queries target", "Range queries scatter"),
        ("Monotonic hotspot risk", "Spreads sequential writes"),
        ("Locality possible", "Locality lost"),
    ]
    return _svg(280, "\n".join(_table(["Ranged", "Hashed"], rows, col_ws=[440, 440], fs=15)), "ae43")


def d44_compound() -> str:
    parts = [
        _mono(460, 36, "{ tenantId: 1, orderId: 1 }", fs=20),
        _box(40, 70, 400, 110, "Prefix targeting", "Queries need tenantId", fs=18, sub_fs=14),
        _box(480, 70, 400, 110, "More cardinality", "Better split points", fs=18, sub_fs=14),
    ]
    return _svg(210, "\n".join(parts), "ae44")


def d45_chunks() -> str:
    parts = [
        _box(40, 40, 250, 120, "Range 1", "Shard A", fs=18, sub_fs=14),
        _box(335, 40, 250, 120, "Range 2", "Shard B", fs=18, sub_fs=14),
        _box(630, 40, 250, 120, "Range 3", "Shard C", fs=18, sub_fs=14),
        _label(460, 190, "App still sees one orders collection", fs=15),
    ]
    return _svg(220, "\n".join(parts), "ae45")


def d46_split() -> str:
    parts = [
        _box(210, 16, 500, 50, "Large range", header=True, fs=16),
        _arrow(360, 66, 220, 110, "ae46"),
        _arrow(560, 66, 700, 110, "ae46"),
        _box(40, 112, 360, 80, "Range A", None, fs=18),
        _box(520, 112, 360, 80, "Range B", None, fs=18),
        _label(460, 220, "Smaller units can move independently", fs=15),
    ]
    return _svg(245, "\n".join(parts), "ae46")


def d47_balancer() -> str:
    parts = [
        _box(40, 30, 260, 130, "Uneven shards", None, fs=17),
        _arrow(300, 95, 360, 95, "ae47"),
        _box(360, 30, 200, 130, "Balancer", header=True, fs=16),
        _arrow(560, 95, 620, 95, "ae47"),
        _box(620, 30, 260, 130, "Moved ranges", None, fs=17),
        _label(460, 190, "Also enforces zones; consumes cluster resources", fs=15),
    ]
    return _svg(220, "\n".join(parts), "ae47")


def d48_migration() -> str:
    return _svg(
        280,
        "\n".join(
            _vflow(
                [
                    ("Copy range to destination", None),
                    ("Catch up changes", None),
                    ("Update metadata, then cleanup", None),
                ],
                x=200,
                y=16,
                w=520,
                h=56,
                gap=20,
                mid="ae48",
            )
        ),
        "ae48",
    )


def d49_targeted() -> str:
    parts = [
        _box(310, 12, 300, 44, "mongos", header=True, fs=16),
        _arrow(460, 56, 180, 100, "ae49"),
        _box(40, 102, 280, 90, "Shard A", "customerId C101", fs=16, sub_fs=13),
        _box(340, 102, 240, 90, "Shard B", "not contacted", fs=16, sub_fs=13),
        _box(600, 102, 280, 90, "Shard C", "not contacted", fs=16, sub_fs=13),
        _label(460, 220, "Shard-key equality can stay on one shard", fs=15),
    ]
    return _svg(245, "\n".join(parts), "ae49")


def d50_scatter() -> str:
    parts = [
        _box(310, 12, 300, 44, "Query without shard key", header=True, fs=15),
        _arrow(360, 56, 160, 96, "ae50"),
        _arrow(460, 56, 460, 96, "ae50"),
        _arrow(560, 56, 760, 96, "ae50"),
        _box(40, 98, 240, 70, "A", None, fs=18),
        _box(340, 98, 240, 70, "B", None, fs=18),
        _box(640, 98, 240, 70, "C", None, fs=18),
        _label(460, 195, "Merge on mongos — more network, CPU, and latency", fs=15),
    ]
    return _svg(220, "\n".join(parts), "ae50")


def d51_hotspots() -> str:
    parts = [
        _box(40, 30, 250, 140, "Shard A", "Normal", fs=18, sub_fs=14),
        _box(325, 20, 270, 160, "Shard B HOT", "Writes + CPU + disk", fs=18, sub_fs=14),
        _box(630, 30, 250, 140, "Shard C", "Idle", fs=18, sub_fs=14),
        _label(460, 210, "Monotonic keys, celebrity tenants, skewed zones", fs=15),
    ]
    return _svg(240, "\n".join(parts), "ae51")


def d52_dist_writes() -> str:
    parts = _hflow(
        [
            ("mongos", "Route write"),
            ("Shard primary", "Apply + oplog"),
            ("Shard secondaries", "Replicate"),
            ("Ack", "Write concern"),
        ],
        y=40,
        h=120,
        box_w=190,
        gap=22,
        mid="ae52",
    )
    return _svg(200, "\n".join(parts), "ae52")


def d53_together() -> str:
    parts = [
        _box(310, 12, 300, 40, "mongos", header=True, fs=16),
        _arrow(200, 52, 140, 78, "ae53"),
        _arrow(460, 52, 460, 78, "ae53"),
        _arrow(720, 52, 780, 78, "ae53"),
        _box(40, 80, 260, 90, "Shard A", "P  S  S", fs=17, sub_fs=14),
        _box(330, 80, 260, 90, "Shard B", "P  S  S", fs=17, sub_fs=14),
        _box(620, 80, 260, 90, "Shard C", "P  S  S", fs=17, sub_fs=14),
        _label(460, 195, "Sharding partitions. Replication copies each partition.", fs=15),
    ]
    return _svg(220, "\n".join(parts), "ae53")


def d54_decision() -> str:
    rows = [
        ("Standalone", "Local learning / disposable tests"),
        ("Replica set", "Production availability"),
        ("Sharded cluster", "Measured horizontal scale"),
        ("Sharded replica sets", "Availability and scale together"),
    ]
    return _svg(280, "\n".join(_table(["Choose", "When"], rows, col_ws=[360, 520], fs=15)), "ae54")


def d55_ecommerce() -> str:
    rows = [
        ("Products", "Often replica set first"),
        ("Orders", "Shard when write volume requires"),
        ("Reports", "Expect scatter-gather cost"),
        ("Regions", "Zones only with evidence"),
    ]
    return _svg(280, "\n".join(_table(["Collection", "Distribution idea"], rows, col_ws=[280, 600], fs=15)), "ae55")


def d56_mistakes() -> str:
    rows = [
        ("Replication as sharding", "Copies do not add capacity"),
        ("Sharding as backup", "Partitions are not backups"),
        ("Low-cardinality key", "Cannot split the load"),
        ("Ignore write concern", "Rollback and durability risk"),
    ]
    return _svg(280, "\n".join(_table(["Mistake", "Why it hurts"], rows, col_ws=[400, 480], fs=15)), "ae56")


def d57_troubleshoot() -> str:
    parts = [
        _box(40, 20, 400, 160, "Replica set", "Primary? Majority? Lag? Oplog?", fs=18, sub_fs=14),
        _box(480, 20, 400, 160, "Sharded cluster", "mongos? CSRS? Targeted? Balancer?", fs=18, sub_fs=13),
    ]
    return _svg(210, "\n".join(parts), "ae57")


def d58_concept_map() -> str:
    parts = [
        _box(210, 12, 500, 44, "Distributed MongoDB", header=True, fs=16),
        _box(20, 80, 280, 90, "Copy", "Replica set + oplog", fs=16, sub_fs=13),
        _box(320, 80, 280, 90, "Elect", "Majority failover", fs=16, sub_fs=13),
        _box(620, 80, 280, 90, "Partition", "Shard key + chunks", fs=16, sub_fs=13),
        _label(460, 200, "Targeted queries beat frequent scatter-gather", fs=15),
    ]
    return _svg(230, "\n".join(parts), "ae58")


def d59_ex_choice() -> str:
    parts = [
        _box(40, 40, 200, 120, "Replication", None, fs=16),
        _box(260, 40, 200, 120, "Sharding", None, fs=16),
        _box(480, 40, 200, 120, "Both", None, fs=16),
        _box(700, 40, 180, 120, "Neither yet", None, fs=15),
        _label(460, 190, "Exercise 7.1 — match the requirement, not the buzzword", fs=15),
    ]
    return _svg(220, "\n".join(parts), "ae59")


def d60_challenge() -> str:
    parts = [
        _box(40, 20, 840, 48, "Scale the e-commerce order platform", header=True, fs=16),
        _box(40, 84, 200, 100, "Availability", "Replica set", fs=15, sub_fs=13),
        _box(255, 84, 200, 100, "Shard decision", "Evidence first", fs=15, sub_fs=13),
        _box(470, 84, 200, 100, "Shard key", "Score candidates", fs=15, sub_fs=13),
        _box(685, 84, 195, 100, "Operations", "Lag, backup, retry", fs=14, sub_fs=12),
    ]
    return _svg(210, "\n".join(parts), "ae60")


def d61_demo_rs() -> str:
    parts = [
        _mono(460, 40, "rs.status()", fs=22),
        _box(40, 80, 270, 90, "Name + states", None, fs=16),
        _box(325, 80, 270, 90, "Primary host", None, fs=16),
        _box(610, 80, 270, 90, "Optimes", None, fs=16),
    ]
    return _svg(200, "\n".join(parts), "ae61")


def d62_lab_health() -> str:
    parts = _hflow(
        [
            ("Connect RS URI", None),
            ("rs.status()", None),
            ("rs.conf()", None),
            ("Health notes", None),
        ],
        y=40,
        h=110,
        box_w=190,
        gap=22,
        mid="ae62",
    )
    return _svg(190, "\n".join(parts), "ae62")


DIAGRAMS = {
    "01-module-map.svg": d01_module_map,
    "02-requirements.svg": d02_requirements,
    "03-ha-vs-scale.svg": d03_ha_vs_scale,
    "04-vertical-horizontal.svg": d04_vertical_horizontal,
    "05-replication-vs-sharding.svg": d05_repl_vs_shard,
    "06-distributed-overview.svg": d06_distributed,
    "07-replica-set.svg": d07_replica_set,
    "08-members.svg": d08_members,
    "09-primary.svg": d09_primary,
    "10-secondary.svg": d10_secondary,
    "11-oplog.svg": d11_oplog,
    "12-replication-flow.svg": d12_repl_flow,
    "13-heartbeats.svg": d13_heartbeats,
    "14-elections.svg": d14_elections,
    "15-failover.svg": d15_failover,
    "16-app-failover.svg": d16_app_failover,
    "17-majority.svg": d17_majority,
    "18-priority.svg": d18_priority,
    "19-arbiter.svg": d19_arbiter,
    "20-hidden.svg": d20_hidden,
    "21-delayed.svg": d21_delayed,
    "22-read-pref.svg": d22_read_pref,
    "23-write-concern.svg": d23_write_concern,
    "24-three-settings.svg": d24_three_settings,
    "25-lag.svg": d25_lag,
    "26-rollback.svg": d26_rollback,
    "27-rs-status.svg": d27_rs_status,
    "28-failure-scenarios.svg": d28_failures,
    "29-what-is-sharding.svg": d29_sharding,
    "30-cluster-components.svg": d30_components,
    "31-shards.svg": d31_shards,
    "32-csrs.svg": d32_csrs,
    "33-mongos.svg": d33_mongos,
    "34-request-flow.svg": d34_request_flow,
    "35-shard-key.svg": d35_shard_key,
    "36-cardinality.svg": d36_cardinality,
    "37-frequency.svg": d37_frequency,
    "38-monotonic.svg": d38_monotonic,
    "39-query-isolation.svg": d39_isolation,
    "40-ranged.svg": d40_ranged,
    "41-hashed.svg": d41_hashed,
    "42-zoned.svg": d42_zoned,
    "43-ranged-vs-hashed.svg": d43_ranged_vs_hashed,
    "44-compound.svg": d44_compound,
    "45-chunks.svg": d45_chunks,
    "46-split.svg": d46_split,
    "47-balancer.svg": d47_balancer,
    "48-migration.svg": d48_migration,
    "49-targeted.svg": d49_targeted,
    "50-scatter-gather.svg": d50_scatter,
    "51-hotspots.svg": d51_hotspots,
    "52-distributed-writes.svg": d52_dist_writes,
    "53-together.svg": d53_together,
    "54-decision.svg": d54_decision,
    "55-ecommerce.svg": d55_ecommerce,
    "56-mistakes.svg": d56_mistakes,
    "57-troubleshoot.svg": d57_troubleshoot,
    "58-concept-map.svg": d58_concept_map,
    "59-ex-choice.svg": d59_ex_choice,
    "60-challenge.svg": d60_challenge,
    "61-demo-rs.svg": d61_demo_rs,
    "62-lab-health.svg": d62_lab_health,
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

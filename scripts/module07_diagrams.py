"""Module 7 diagrams (261). Run: python scripts/module07_diagrams.py"""
from __future__ import annotations

import html
from pathlib import Path

from marp_svg_common import BORDER, FONT, HEADER_BG, MONO, MUTED, PANEL, RED, TEXT

BG = "#ffffff"
ASSETS = Path(__file__).resolve().parent.parent / "slides" / "assets" / "module-07"
W = 920


def _esc(t: str) -> str:
    return html.escape(t, quote=True)


def _svg(h: int, body: str, mid: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">
<defs>
  <marker id="{mid}" viewBox="0 0 10 10" markerWidth="7" markerHeight="7" refX="9" refY="5" orient="auto" markerUnits="userSpaceOnUse">
    <path d="M0,1 L9,5 L0,9 Z" fill="{RED}"/>
  </marker>
</defs>
<rect width="{W}" height="{h}" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>
{body}
</svg>
'''


def _box(x, y, w, h, title, sub=None, *, header=False, fs=16, sfs=13) -> str:
    fill = HEADER_BG if header else BG
    ty = y + (h / 2 + fs * 0.35 if not sub else h * 0.38)
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{RED}" stroke-width="2"/>',
        f'<text x="{x + w / 2}" y="{ty:.1f}" text-anchor="middle" font-family="{FONT}" font-size="{fs}" fill="{RED if header else TEXT}">{_esc(title)}</text>',
    ]
    if sub:
        parts.append(
            f'<text x="{x + w / 2}" y="{y + h * 0.72:.1f}" text-anchor="middle" font-family="{FONT}" font-size="{sfs}" fill="{MUTED}">{_esc(sub)}</text>'
        )
    return "\n".join(parts)


def _label(x, y, text, *, fs=15, fill=MUTED) -> str:
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{FONT}" font-size="{fs}" fill="{fill}">{_esc(text)}</text>'


def _mono(x, y, text, *, fs=15) -> str:
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="{fs}" fill="{TEXT}">{_esc(text)}</text>'


def _arrow(x1, y1, x2, y2, mid) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{RED}" stroke-width="2" marker-end="url(#{mid})"/>'


def render(n: int, kind: str, spec: dict) -> str:
    mid = f"m{n:03d}"
    cap = spec.get("c", "")

    if kind == "compare":
        (lt, ls), (rt, rs) = spec["l"], spec["r"]
        parts = [
            _box(40, 20, 400, 150, lt, ls, fs=18, sfs=14),
            _box(480, 20, 400, 150, rt, rs, fs=18, sfs=14),
        ]
        h = 210
        if cap:
            parts.append(_label(460, 198, cap))
            h = 230
        return _svg(h, "\n".join(parts), mid)

    if kind == "vflow":
        boxes = spec["b"]
        x, y, w, hbox, gap = 200, 14, 520, 48, 16
        parts = []
        cy = y
        for i, item in enumerate(boxes):
            t, s = item if isinstance(item, tuple) else (item, None)
            parts.append(_box(x, cy, w, hbox, t, s, fs=16 if s else 17, sfs=13))
            if i < len(boxes) - 1:
                parts.append(_arrow(x + w / 2, cy + hbox, x + w / 2, cy + hbox + gap - 4, mid))
            cy += hbox + gap
        if cap:
            parts.append(_label(460, cy + 6, cap))
            cy += 28
        return _svg(int(cy + 16), "\n".join(parts), mid)

    if kind == "hflow":
        boxes = spec["b"]
        nbox = len(boxes)
        gap = 20
        y, hbox = 36, 110
        usable = W - 40 - (nbox - 1) * gap
        bw = min(200, usable // nbox)
        x0 = (W - (nbox * bw + (nbox - 1) * gap)) / 2
        parts = []
        x = x0
        for i, item in enumerate(boxes):
            t, s = item if isinstance(item, tuple) else (item, None)
            parts.append(_box(x, y, bw, hbox, t, s, fs=15, sfs=12))
            if i < nbox - 1:
                parts.append(_arrow(x + bw, y + hbox / 2, x + bw + gap - 4, y + hbox / 2, mid))
            x += bw + gap
        h = 170
        if cap:
            parts.append(_label(460, 168, cap))
            h = 190
        return _svg(h, "\n".join(parts), mid)

    if kind == "table":
        headers, rows = spec["h"], spec["r"]
        ncol = len(headers)
        leftover = W - 40
        col_ws = spec.get("cw") or [leftover // ncol] * ncol
        col_ws = list(col_ws)
        col_ws[-1] = leftover - sum(col_ws[:-1])
        rh, hh, fs = spec.get("rh", 46), 42, spec.get("fs", 14)
        parts, x = [], 20
        for i, hdr in enumerate(headers):
            parts.append(_box(x, 14, col_ws[i], hh, hdr, header=True, fs=fs))
            x += col_ws[i]
        for ri, row in enumerate(rows):
            y = 14 + hh + 6 + ri * (rh + 4)
            x = 20
            for i, cell in enumerate(row):
                parts.append(_box(x, y, col_ws[i], rh, cell, fs=fs))
                x += col_ws[i]
        yb = 14 + hh + 6 + len(rows) * (rh + 4)
        if cap:
            parts.append(_label(460, yb + 18, cap))
            yb += 36
        return _svg(int(yb + 12), "\n".join(parts), mid)

    if kind == "row":
        boxes = spec["b"]
        nbox = len(boxes)
        gap = 16
        usable = W - 40 - (nbox - 1) * gap
        bw = usable // nbox
        hbox = spec.get("bh", 130)
        y = 24
        parts = []
        x = 20
        for item in boxes:
            t, s = item if isinstance(item, tuple) else (item, None)
            parts.append(_box(x, y, bw, hbox, t, s, header=spec.get("hdr") == t, fs=15, sfs=12))
            x += bw + gap
        h = y + hbox + 20
        if cap:
            parts.append(_label(460, h + 4, cap))
            h += 28
        return _svg(int(h + 12), "\n".join(parts), mid)

    if kind == "fan":
        top, kids = spec["t"], spec["k"]
        parts = [_box(310, 12, 300, 44, top[0], top[1] if len(top) > 1 else None, header=True, fs=16)]
        nk = len(kids)
        gap = 16
        usable = W - 40 - (nk - 1) * gap
        bw = usable // nk
        x = 20
        cy = 108
        for i, item in enumerate(kids):
            t, s = item if isinstance(item, tuple) else (item, None)
            parts.append(_arrow(460, 56, x + bw / 2, cy - 4, mid))
            parts.append(_box(x, cy, bw, 90, t, s, fs=15, sfs=12))
            x += bw + gap
        h = 220
        if cap:
            parts.append(_label(460, 214, cap))
            h = 240
        return _svg(h, "\n".join(parts), mid)

    if kind == "code":
        lines = spec["lines"]
        parts = [_mono(460, 28 + i * 28, ln, fs=spec.get("fs", 16)) for i, ln in enumerate(lines)]
        y = 28 + len(lines) * 28 + 8
        extra = spec.get("b")
        if extra:
            nbox = len(extra)
            gap = 16
            bw = (W - 40 - (nbox - 1) * gap) // nbox
            x = 20
            for item in extra:
                t, s = item if isinstance(item, tuple) else (item, None)
                parts.append(_box(x, y, bw, 80, t, s, fs=15, sfs=12))
                x += bw + gap
            y += 96
        if cap:
            parts.append(_label(460, y + 8, cap))
            y += 28
        return _svg(int(y + 16), "\n".join(parts), mid)

    raise ValueError(kind)


def catalog() -> list[tuple[int, str, str, dict]]:
    C: list[tuple[int, str, str, dict]] = []

    def add(n, slug, kind, **spec):
        C.append((n, slug, kind, spec))

    # --- core ---
    add(1, "distributed-architecture", "vflow",
        b=[("Application", None), ("MongoDB driver", None), ("mongos routers", None),
           ("Shard replica sets", "A · B · C")],
        c="Distributed data and work; redundancy inside each shard")
    add(2, "ha-vs-horizontal-scale", "compare",
        l=("High availability", "Replica sets keep a primary writable"),
        r=("Horizontal scale", "Sharding spreads data and work"),
        c="Copy the dataset versus partition the dataset")
    add(3, "vertical-vs-horizontal", "compare",
        l=("Vertical", "More CPU, RAM, disk on one host"),
        r=("Horizontal", "More hosts, more complexity"),
        c="Vertical is simpler until hardware and cost hit a wall")
    add(4, "replication-vs-sharding", "table",
        h=["Replication", "Sharding"],
        r=[("Copies the dataset", "Partitions the dataset"),
           ("Failover / redundancy", "Storage and throughput"),
           ("Primary + secondaries", "Multiple shards"),
           ("Same data on members", "Different ranges per shard")])
    add(5, "replication-and-sharding-together", "fan",
        t=("mongos",),
        k=[("Shard A", "P  S  S"), ("Shard B", "P  S  S"), ("Shard C", "P  S  S")],
        c="Sharding partitions. Replication copies each partition.")
    add(6, "standalone-rs-sharded", "row",
        b=[("Standalone", "Learning / tests"),
           ("Replica set", "Production HA"),
           ("Sharded cluster", "Measured scale")],
        c="Production shards are replica sets")
    add(7, "deployment-decision-tree", "vflow",
        b=[("Local learning?", "Standalone is enough"),
           ("Must survive a server failure?", "Replica set"),
           ("One replica set cannot hold growth?", "Shard"),
           ("Need both?", "Sharded replica sets")])
    add(8, "requirements-map", "table",
        h=["Business need", "Mechanism"],
        r=[("Stay up during failure", "Replication"),
           ("More storage / writes", "Sharding"),
           ("Users in many places", "Scale + placement"),
           ("Durability and latency", "Write/read settings"),
           ("Availability and scale", "Both")])

    # --- replica-set architecture ---
    add(9, "replica-set-overview", "row",
        b=[("Primary", "Writes + oplog"), ("Secondary", "Replicates"), ("Secondary", "Can be elected")],
        c="Same logical dataset on every data-bearing member")
    add(10, "three-member-replica-set", "fan",
        t=("Replica set", "Heartbeats among all"),
        k=[("Primary", "Writes"), ("Secondary 1", "Oplog apply"), ("Secondary 2", "Oplog apply")],
        c="Replication arrows carry data; heartbeats carry health")
    add(11, "five-member-replica-set", "row",
        b=[("P", "Zone A"), ("S", "Zone B"), ("S", "Zone C"), ("S", "Zone A"), ("S", "Zone B")],
        bh=110, c="Spread voters across independent failure domains")
    add(12, "member-roles", "table",
        h=["Role", "What it does"],
        r=[("Primary", "Accepts writes"),
           ("Secondary", "Copy; may be elected"),
           ("Hidden", "Not for app reads"),
           ("Delayed", "Intentional lag"),
           ("Non-voting", "Data, no vote"),
           ("Arbiter", "Vote only; no data")])
    add(13, "primary-responsibilities", "vflow",
        b=[("Accept application writes", None), ("Apply locally and record oplog", None),
           ("Serve primary-preference reads", None), ("Only one primary at a time", None)])
    add(14, "secondary-responsibilities", "compare",
        l=("Copy + apply oplog", "In order, continuously"),
        r=("Election eligible", "Not a passive backup"),
        c="May serve reads only when read preference allows")
    add(15, "same-data-across-members", "row",
        b=[("Primary", "customers · products · orders"),
           ("Secondary", "same collections"),
           ("Secondary", "same collections")],
        c="Copies, not partitions")
    add(16, "replica-set-connection-string", "vflow",
        b=[("Application", None),
           ("mongodb://h1,h2,h3/?replicaSet=rs0", None),
           ("Driver discovers current primary", None)],
        c="Do not pin the client to one hostname forever")
    add(17, "driver-topology-discovery", "hflow",
        b=[("Seed host", None), ("hello / isMaster", None), ("Full member list", None), ("Server selection", None)],
        c="SDAM keeps the topology view current")
    add(18, "app-to-replica-set-flow", "hflow",
        b=[("App", None), ("Driver", None), ("Primary writes", None), ("Eligible reads", None)])

    # --- oplog ---
    add(19, "the-oplog", "vflow",
        b=[("Application write", None), ("Primary applies + oplog entry", None),
           ("Secondaries copy the entry", None), ("Secondaries apply locally", None)],
        c="Oplog is a capped collection of data-changing operations")
    add(20, "replicated-write-flow", "hflow",
        b=[("Driver", "Finds primary"), ("Primary", "Write + oplog"),
           ("Secondaries", "Copy + apply"), ("Ack", "Write concern")])
    add(21, "primary-write-processing", "vflow",
        b=[("Client request", None), ("Change local data", None),
           ("Record oplog entry", None), ("Acknowledge per write concern", None)])
    add(22, "secondary-replication-process", "vflow",
        b=[("Retrieve oplog entries", None), ("Apply in order", None), ("Update local dataset", None)])
    add(23, "oplog-timeline", "hflow",
        b=[("insert C101", None), ("update O5001", None), ("delete probe", None), ("… newest", None)],
        c="Order is the contract")
    add(24, "asynchronous-replication", "compare",
        l=("Primary at T0", "Write already applied"),
        r=("Secondary at T0−lag", "Still applying"),
        c="Acknowledgment timing depends on write concern")
    add(25, "replication-progress", "row",
        b=[("Primary", "optime newest"), ("Secondary A", "a few ms behind"), ("Secondary B", "catching up")])
    add(26, "oplog-window", "hflow",
        b=[("Oldest entry", "Window start"), ("History", "Capped collection"), ("Newest entry", "Now")],
        c="A member down longer than the window may need initial sync")
    add(27, "outside-oplog-window", "compare",
        l=("Oplog window", "Hours of history"),
        r=("Secondary offline too long", "Cannot catch up incrementally"),
        c="Then: initial sync, not oplog replay")
    add(28, "initial-sync-vs-catchup", "compare",
        l=("Initial sync", "Copy the full dataset"),
        r=("Oplog catch-up", "Apply recent operations"),
        c="Catch-up only works inside the oplog window")
    add(29, "data-vs-heartbeats", "compare",
        l=("Oplog traffic", "Copies application changes"),
        r=("Heartbeats", "Health and state only"),
        c="Two planes — do not draw them as one arrow")

    # --- elections ---
    add(30, "heartbeats", "fan",
        t=("Members",),
        k=[("Reachable?", None), ("Who is primary?", None), ("Elect now?", None)],
        c="Heartbeats do not copy documents")
    add(31, "healthy-replica-set-state", "row",
        b=[("PRIMARY", "health 1"), ("SECONDARY", "health 1"), ("SECONDARY", "health 1")],
        c="Small lag is normal when idle")
    add(32, "primary-failure-detection", "vflow",
        b=[("Heartbeats to primary fail", None), ("Members mark it unreachable", None),
           ("Eligible voters start an election", None)])
    add(33, "election-flow", "vflow",
        b=[("Failure detected", None), ("Candidate selection", None),
           ("Voting majority", None), ("New primary", None)])
    add(34, "failover-timeline", "vflow",
        b=[("Healthy primary", None), ("Failure / step-down", None),
           ("Election window", "Writes may pause"), ("New primary · resumed writes", None)])
    add(35, "before-after-failover", "compare",
        l=("Before", "A primary · B,C secondary"),
        r=("After", "B primary · A rejoins later as secondary"))
    add(36, "app-behavior-during-failover", "vflow",
        b=[("Transient errors", None), ("Driver rediscovers topology", None),
           ("Retry eligible operations", None), ("Writes hit the new primary", None)])
    add(37, "driver-reconnection", "hflow",
        b=[("Old primary gone", None), ("SDAM update", None), ("New primary selected", None), ("Writes rerouted", None)])
    add(38, "voting-majority", "row",
        b=[("Need majority to elect", None), ("Need majority to stay primary", None),
           ("Minority cannot write", None)])
    add(39, "three-member-majority", "row",
        b=[("A votes", None), ("B votes", None), ("C isolated", "Cannot elect itself")],
        c="A+B = majority. Protects against two primaries.")
    add(40, "five-member-majority", "row",
        b=[("3 of 5", "Majority"), ("2 of 5", "Cannot elect"), ("Spread zones", "Survive one DC")])
    add(41, "network-partition-majority", "compare",
        l=("Majority side", "Can elect / keep a primary"),
        r=("Minority side", "Read-only or no primary"),
        c="Partitions follow the voting majority")
    add(42, "split-brain-prevention", "compare",
        l=("Forbidden", "Two writable primaries"),
        r=("Rule", "Only a majority may accept writes"),
        c="Consistency over 'always writable'")
    add(43, "planned-step-down", "vflow",
        b=[("rs.stepDown()", None), ("Election", None), ("New primary", None), ("Former primary becomes secondary", None)])
    add(44, "unplanned-primary-failure", "vflow",
        b=[("Process / host / network dies", None), ("Heartbeats fail", None), ("Automatic election", None)])
    add(45, "election-candidate-priority", "table",
        h=["Factor", "Effect"],
        r=[("Priority", "Preferred primary"),
           ("Freshness", "Caught-up members preferred"),
           ("Priority 0", "Will not become primary")])
    add(46, "former-primary-recovery", "hflow",
        b=[("Old primary returns", None), ("Rollback if needed", None), ("Rejoins as SECONDARY", None)])

    # --- specialized members ---
    add(47, "member-priority", "compare",
        l=("Higher priority", "Preferred primary DC"),
        r=("Lower / 0", "Reporting node stays secondary"),
        c="Priority is election preference, not a read router")
    add(48, "priority-zero", "compare",
        l=("Data-bearing", "Full copy"),
        r=("priority: 0", "Cannot become primary"))
    add(49, "hidden-secondary", "compare",
        l=("Full data copy", "Backup / reporting"),
        r=("Hidden from drivers", "Not selected for app reads"),
        c="Hidden ≠ disconnected")
    add(50, "hidden-for-reporting", "hflow",
        b=[("App reads", "Primary / visible S"), ("Hidden member", "Reports / dumps"), ("Primary", "Unaffected OLTP")])
    add(51, "delayed-secondary", "vflow",
        b=[("Primary now", None), ("Configured delay", None), ("Delayed secondary applies later", None)],
        c="Useful for some accidents — not a backup")
    add(52, "delayed-recovery-window", "compare",
        l=("Primary", "Accidental drop already applied"),
        r=("Delayed member", "Still has the pre-drop data"))
    add(53, "delayed-vs-backup", "compare",
        l=("Delayed replica", "Limited, same-cluster copy"),
        r=("Backup", "Independent recovery point"),
        c="You still take backups")
    add(54, "arbiter-role", "row",
        b=[("Votes", None), ("No application data", None), ("Cannot be primary", None)],
        c="Adds a vote, not a copy")
    add(55, "arbiter-limitations", "row",
        b=[("No data copy", None), ("No extra reads", None), ("No durability copy", None)],
        c="Prefer a data-bearing voter when resources allow")
    add(56, "data-bearing-vs-arbiter", "compare",
        l=("Data-bearing voter", "Copy + vote + possible primary"),
        r=("Arbiter", "Vote only"))

    # --- read preferences ---
    add(57, "read-preference-overview", "table",
        h=["Mode", "Who may serve reads"],
        r=[("primary", "Current primary only"),
           ("primaryPreferred", "Primary, else secondary"),
           ("secondary", "Secondaries only"),
           ("secondaryPreferred", "Secondary, else primary"),
           ("nearest", "Lowest-latency eligible")])
    add(58, "primary-read-preference", "vflow",
        b=[("Client read", None), ("Driver selects PRIMARY", None), ("Freshest replica-set state", None)])
    add(59, "primary-preferred-flow", "vflow",
        b=[("Try primary", None), ("If unavailable, eligible secondary", None)],
        c="Failover reads may be stale")
    add(60, "secondary-read-preference", "vflow",
        b=[("Client read", None), ("Eligible SECONDARY only", None), ("Errors if none available", None)])
    add(61, "secondary-preferred-flow", "vflow",
        b=[("Prefer secondary", None), ("Fall back to primary", None)])
    add(62, "nearest-read-preference", "hflow",
        b=[("Ping samples", None), ("Lowest RTT eligible", None), ("May still be the primary", None)])
    add(63, "primary-vs-secondary-reads", "compare",
        l=("Primary reads", "Current primary state"),
        r=("Secondary reads", "May lag"))
    add(64, "secondary-read-staleness", "compare",
        l=("Write on primary T0", None),
        r=("Secondary read T0−lag", "Missing the write"))
    add(65, "reporting-on-secondary", "compare",
        l=("OLTP on primary", "Orders, checkout"),
        r=("Analytics on secondary", "Capacity + staleness cost"),
        c="Secondary work is not free")
    add(66, "read-concern-overview", "table",
        h=["Level", "Idea"],
        r=[("local / available", "What this member sees"),
           ("majority", "Majority-committed view"),
           ("linearizable", "Strong, primary, costly"),
           ("snapshot", "Transaction-consistent")])
    add(67, "read-pref-vs-read-concern", "compare",
        l=("Read preference", "Which member?"),
        r=("Read concern", "What visibility?"))
    add(68, "read-your-write-risk", "vflow",
        b=[("Write on primary", None), ("Immediate secondary read", None), ("May not see the write", None)])

    # --- write concern ---
    add(69, "write-concern-overview", "row",
        b=[("w: 1", "Primary ack"), ("w: majority", "Voting data-bearing majority"), ("w: N", "N members")])
    add(70, "primary-only-ack", "hflow",
        b=[("Write", None), ("Primary applies", None), ("Client success", None), ("Secondaries later", None)])
    add(71, "majority-write-concern", "hflow",
        b=[("Write", None), ("Primary", None), ("Majority durable ack", None), ("Client success", None)])
    add(72, "numeric-write-concern", "hflow",
        b=[("w: 2", None), ("Wait for 2 members", None), ("Then acknowledge", None)])
    add(73, "journal-acknowledgment", "vflow",
        b=[("Apply write", None), ("Journal per configured j", None), ("Then acknowledge", None)])
    add(74, "write-concern-latency", "compare",
        l=("Weaker ack", "Usually faster"),
        r=("Stronger ack", "More durability confidence"),
        c="Not a universal performance knob")
    add(75, "write-concern-timeout", "vflow",
        b=[("Write may be applied", None), ("wtimeout expires", None), ("Client sees an error", None)],
        c="Timeout ≠ automatic rollback of a applied write")
    add(76, "payment-majority-write", "vflow",
        b=[("Checkout write", None), ("Primary + majority ack", None), ("Client: payment recorded", None)])
    add(77, "three-settings", "table",
        h=["Setting", "Question"],
        r=[("Read preference", "Which member serves the read?"),
           ("Read concern", "What visibility guarantee?"),
           ("Write concern", "What acknowledgment for a write?")])

    # --- lag ---
    add(78, "replication-lag-overview", "hflow",
        b=[("Primary applied T0", None), ("Lag", None), ("Secondary applied T0+lag", None)])
    add(79, "healthy-vs-growing-lag", "compare",
        l=("Healthy", "Small, stable delay"),
        r=("Incident", "Delay keeps growing"))
    add(80, "causes-of-lag", "table",
        h=["Cause", "Check"],
        r=[("Slow disk", "iostat / Atlas disk"),
           ("CPU", "Secondary saturation"),
           ("Network", "DC RTT / drops"),
           ("Write burst", "Primary vs apply rate"),
           ("Secondary workload", "Reporting queries")])
    add(81, "lag-diagnostic-flow", "vflow",
        b=[("rs.status / optimes", None), ("Member CPU and disk", None),
           ("Network", None), ("Oplog window", None), ("Workload on the secondary", None)])
    add(82, "heavy-secondary-reads-lag", "compare",
        l=("Reporting query storm", None),
        r=("Apply lag grows", "Failover readiness drops"))
    add(83, "slow-disk-lag", "vflow",
        b=[("Oplog entries arrive", None), ("Disk cannot apply fast enough", None), ("Lag increases", None)])
    add(84, "network-lag", "hflow",
        b=[("Primary DC", None), ("High RTT / loss", None), ("Remote secondary", None)])
    add(85, "oplog-vs-recovery-time", "compare",
        l=("Downtime 20 min", "Inside window → catch-up"),
        r=("Downtime 2 days", "Outside window → initial sync"))
    add(86, "rollback-concept", "compare",
        l=("Former primary", "Writes not on new history"),
        r=("Current primary", "Authoritative oplog"))
    add(87, "rollback-risk-weak-ack", "vflow",
        b=[("w:1 success to client", None), ("Failover", None), ("Write may roll back", None)])
    add(88, "majority-rollback-protection", "vflow",
        b=[("majority write succeeds", None), ("Failover", None), ("Write is on the surviving history", None)])
    add(89, "replication-is-not-backup", "vflow",
        b=[("drop collection on primary", None), ("Oplog replicates the drop", None), ("Every member loses the data", None)])
    add(90, "replica-set-plus-backup", "compare",
        l=("Replica set", "Availability copies"),
        r=("Backups", "Independent restore"),
        c="You need both")

    # --- health ---
    add(91, "replica-set-health-dashboard", "table",
        h=["Member", "State / lag"],
        r=[("atlas-a", "PRIMARY · —"),
           ("atlas-b", "SECONDARY · 0s"),
           ("atlas-c", "SECONDARY · 1s")])
    add(92, "rs-status-concept-map", "code",
        lines=["rs.status()", "rs.conf()"],
        b=[("States", "PRIMARY / SECONDARY"), ("Health", "Reachable?"), ("Optimes", "Lag")])
    add(93, "healthy-three-member", "row",
        b=[("P", "up"), ("S", "up"), ("S", "up")], c="Majority intact")
    add(94, "one-secondary-failure", "row",
        b=[("P", "writable"), ("S", "up"), ("S", "down")],
        c="Primary continues; repair soon")
    add(95, "primary-failure-majority-up", "hflow",
        b=[("P down", None), ("2 voters remain", None), ("Election", None), ("New primary", None)])
    add(96, "loss-of-voting-majority", "row",
        b=[("No writable primary", None), ("Consistency wins", None), ("Fix network / members", None)])
    add(97, "secondary-too-stale", "compare",
        l=("Caught-up secondary", "Safe candidate"),
        r=("Far behind", "Unsafe / unelectable"))
    add(98, "multi-zone-placement", "row",
        b=[("Zone A", "P"), ("Zone B", "S"), ("Zone C", "S")],
        c="Independent failure domains")
    add(99, "poor-failure-domain", "row",
        b=[("Host / rack / AZ 1", "P + S + S")],
        c="One outage takes the whole set")
    add(100, "replica-set-ops-checklist", "table",
        h=["Check", "Why"],
        r=[("Odd voters / domains", "Elections"),
           ("Lag + oplog window", "Catch-up"),
           ("RS URI + backups", "App + restore"),
           ("Failover test", "Prove it")])

    # --- sharding architecture ---
    add(101, "sharded-cluster-overview", "vflow",
        b=[("Application", None), ("mongos", None), ("Shards + config RS", None)])
    add(102, "complete-sharded-architecture", "fan",
        t=("mongos · mongos",),
        k=[("Shard RS A", None), ("Shard RS B", None), ("Config RS", "Metadata")])
    add(103, "logical-vs-physical", "compare",
        l=("App sees", "db.orders"),
        r=("Cluster stores", "ranges on A, B, C"))
    add(104, "sharded-replica-sets", "row",
        b=[("Shard A", "P S S"), ("Shard B", "P S S"), ("Shard C", "P S S")])
    add(105, "three-component-roles", "row",
        b=[("Shards", "Application data"), ("mongos", "Route + merge"), ("Config RS", "Metadata")])
    add(106, "sharded-cluster-with-ha", "row",
        b=[("≥2 mongos", None), ("Each shard a RS", None), ("CSRS replicated", None)])
    add(107, "client-to-mongos", "vflow",
        b=[("Application / driver", None), ("mongos pool", None), ("Not a random shard as the only entry", None)])

    add(108, "shard-responsibilities", "compare",
        l=("Subset of data", "Not the whole collection"),
        r=("Local processing", "Queries and writes for its ranges"))
    add(109, "data-partitioned-across-shards", "row",
        b=[("Shard A", "orders 1"), ("Shard B", "orders 2"), ("Shard C", "orders 3")])
    add(110, "replica-set-inside-a-shard", "row",
        b=[("Shard primary", "Writes"), ("Shard secondaries", "HA copy")])
    add(111, "shard-level-failover", "vflow",
        b=[("Shard A primary fails", None), ("Shard A elects", None), ("Other shards keep serving", None)])
    add(112, "independent-shard-availability", "row",
        b=[("Shard A", "has primary"), ("Shard B", "electing"), ("Shard C", "has primary")])

    add(113, "config-server-replica-set", "row",
        b=[("CSRS P", None), ("CSRS S", None), ("CSRS S", None)],
        c="Metadata, not orders documents")
    add(114, "cluster-metadata-contents", "table",
        h=["Metadata", "Purpose"],
        r=[("Sharded collections", "What is sharded"),
           ("Shard keys", "How documents place"),
           ("Ranges / chunks", "What lives where"),
           ("Zones", "Placement rules")])
    add(115, "metadata-vs-app-data", "compare",
        l=("Config servers", "Routing map"),
        r=("Shards", "Business documents"))
    add(116, "mongos-metadata-lookup", "hflow",
        b=[("Request", None), ("Cached metadata", None), ("Target shard(s)", None)])
    add(117, "csrs-failure-impact", "vflow",
        b=[("CSRS unhealthy", None), ("Metadata changes stall", None), ("Treat as serious", None)])

    add(118, "mongos-query-router", "vflow",
        b=[("Accept client request", None), ("Read routing metadata", None),
           ("Target shards and merge", None), ("No app collection data stored", None)])
    add(119, "sharded-read-flow", "hflow",
        b=[("App", None), ("mongos", None), ("Targeted shards", None), ("Merge → client", None)])
    add(120, "sharded-write-flow", "hflow",
        b=[("mongos", None), ("Shard primary", None), ("Shard secondaries", None), ("Ack", None)])
    add(121, "multiple-mongos", "row",
        b=[("mongos 1", None), ("mongos 2", None), ("mongos 3", None)],
        c="Stateless routers; deploy more than one")
    add(122, "router-failure-recovery", "compare",
        l=("mongos A down", None),
        r=("Clients use mongos B", None))
    add(123, "result-merging", "fan",
        t=("mongos merge",),
        k=[("Shard A rows", None), ("Shard B rows", None), ("Shard C rows", None)])

    # --- shard keys ---
    add(124, "what-is-a-shard-key", "code",
        lines=["{ customerId: 1 }", '{ tenantId: 1, createdAt: 1 }', '{ customerId: "hashed" }'],
        c="The most important sharding decision")
    add(125, "shard-key-selection-framework", "row",
        b=[("Cardinality", None), ("Distribution", None), ("Writes", None), ("Targeting", None), ("Growth", None)])
    add(126, "good-vs-poor-shard-key", "compare",
        l=("Good", "High cardinality, even, query-aligned"),
        r=("Poor", "status / monotonic ranged createdAt"))
    add(127, "shard-key-cardinality", "compare",
        l=("Low", "NEW, PAID, SHIPPED"),
        r=("High", "customerId, orderId"))
    add(128, "low-cardinality-key", "row",
        b=[("PAID", "huge chunk"), ("PENDING", "small"), ("FAILED", "tiny")],
        c="Too few buckets to split work")
    add(129, "high-cardinality-key", "row",
        b=[("C101", None), ("C204", None), ("… C9xxx", None)],
        c="Still check frequency")
    add(130, "frequency-distribution", "compare",
        l=("Balanced values", "Even shards"),
        r=("One dominant value", "Hot shard"))
    add(131, "skewed-tenant", "row",
        b=[("Tenant A 80%", "Hot"), ("Others 20%", "Cold")],
        c="High cardinality is not enough")
    add(132, "monotonic-shard-key", "hflow",
        b=[("t=1", None), ("t=2", None), ("t=3", None), ("always max range", None)])
    add(133, "monotonic-write-hotspot", "row",
        b=[("Shard A", "old"), ("Shard B", "old"), ("Shard C HOT", "all new writes")])
    add(134, "query-isolation", "compare",
        l=("Shard-key predicate", "Router can target"),
        r=("No key field", "Often scatter-gather"))
    add(135, "compound-shard-key", "code",
        lines=["{ tenantId: 1, orderId: 1 }"],
        b=[("Prefix targeting", "Need tenantId"), ("More cardinality", "Better splits")])
    add(136, "compound-prefix", "compare",
        l=("Query has leading field", "May target"),
        r=("Missing leading field", "Poor isolation"))
    add(137, "shard-key-scorecard", "table",
        h=["Candidate", "Risk"],
        r=[("paymentStatus", "Low cardinality"),
           ("createdAt ranged", "Monotonic hotspot"),
           ("customerId", "Target history; tenant skew"),
           ("hashed customerId", "Even writes; range tax")])

    add(138, "ranged-sharding", "row",
        b=[("A–F", "Shard A"), ("G–M", "Shard B"), ("N–Z", "Shard C")])
    add(139, "ranged-sharding-example", "row",
        b=[("C101–C3xx", "A"), ("C4xx–C6xx", "B"), ("C7xx+", "C")])
    add(140, "range-query-routing", "hflow",
        b=[("customerId G–K", None), ("mongos", None), ("Shard B only", None)])
    add(141, "ranged-locality", "hflow",
        b=[("Nearby keys", None), ("Nearby ranges", None), ("Fewer shards for ranges", None)])
    add(142, "ranged-hotspot", "row",
        b=[("Cold ranges", None), ("Hot max range", "Sequential writes")])
    add(143, "hashed-sharding", "vflow",
        b=[("customerId value", None), ("Hash function", None), ("Hash range on a shard", None)])
    add(144, "hashed-distribution", "hflow",
        b=[("id 1,2,3…", None), ("Hashes scatter", None), ("Even shards", None)])
    add(145, "hashed-equality-routing", "hflow",
        b=[('find({ customerId: "C101" })', None), ("Hash", None), ("One shard", None)])
    add(146, "hashed-range-query", "fan",
        t=("createdAt range on hashed customerId",),
        k=[("A", None), ("B", None), ("C", None)],
        c="Natural order is gone")
    add(147, "ranged-vs-hashed", "table",
        h=["Ranged", "Hashed"],
        r=[("Order preserved", "Hashes scramble order"),
           ("Range queries target", "Range queries scatter"),
           ("Monotonic hotspot risk", "Spreads sequential writes"),
           ("Locality possible", "Locality lost")])
    add(148, "zoned-sharding", "compare",
        l=("Canada ranges", "Canada zone / shards"),
        r=("Europe ranges", "Europe zone / shards"))
    add(149, "geographic-zones", "row",
        b=[("CA customers", "CA shards"), ("EU customers", "EU shards")])
    add(150, "tenant-zones", "row",
        b=[("Enterprise tenant", "Dedicated zone"), ("Long tail", "Shared shards")])
    add(151, "hardware-tier-zones", "compare",
        l=("Hot recent ranges", "Fast hardware"),
        r=("Archival ranges", "Cheaper tier"))
    add(152, "ranged-hashed-zoned", "table",
        h=["Strategy", "Typical use"],
        r=[("Ranged", "Locality + range queries"),
           ("Hashed", "Even equality writes"),
           ("Zoned", "Residency / tiers")])

    # --- chunks ---
    add(153, "logical-data-ranges", "row",
        b=[("Range 1", "Shard A"), ("Range 2", "Shard B"), ("Range 3", "Shard C")])
    add(154, "collection-divided-into-ranges", "vflow",
        b=[("orders collection", None), ("Shard-key boundaries", None), ("Movable ranges", None)])
    add(155, "range-to-shard-mapping", "table",
        h=["Range", "Shard"],
        r=[("Min → M", "A"), ("M → T", "B"), ("T → Max", "C")])
    add(156, "range-splitting", "fan",
        t=("Large range",),
        k=[("Range A", None), ("Range B", None)])
    add(157, "before-after-split", "compare",
        l=("Before", "One oversized range"),
        r=("After", "Two movable ranges"))
    add(158, "the-balancer", "hflow",
        b=[("Uneven shards", None), ("Balancer", None), ("Moved ranges", None)])
    add(159, "balanced-cluster", "row",
        b=[("A ~33%", None), ("B ~33%", None), ("C ~34%", None)])
    add(160, "unbalanced-cluster", "row",
        b=[("A 10%", None), ("B 12%", None), ("C 78% HOT", None)])
    add(161, "chunk-migration-flow", "vflow",
        b=[("Copy range to destination", None), ("Catch up changes", None),
           ("Update metadata, then cleanup", None)])
    add(162, "migration-between-shards", "hflow",
        b=[("Overloaded A", None), ("Copy range", None), ("Shard B owns it", None)])
    add(163, "balancer-and-zones", "vflow",
        b=[("Need to rebalance", None), ("Respect zone constraints", None), ("Do not move CA data to EU", None)])
    add(164, "adding-a-new-shard", "hflow",
        b=[("Add empty shard D", None), ("Balancer moves ranges", None), ("Load spreads", None)])
    add(165, "removing-a-shard", "vflow",
        b=[("Move ranges off the shard", None), ("Confirm empty", None), ("Remove from cluster", None)])

    # --- routing ---
    add(166, "targeted-query", "fan",
        t=("mongos",),
        k=[("Shard A", "customerId C101"), ("Shard B", "not contacted"), ("Shard C", "not contacted")])
    add(167, "multi-shard-targeted", "fan",
        t=("Key range G–R",),
        k=[("A skip", None), ("B hit", None), ("C hit", None)])
    add(168, "scatter-gather", "fan",
        t=("Query without shard key",),
        k=[("A", None), ("B", None), ("C", None)],
        c="Merge on mongos — more network, CPU, latency")
    add(169, "targeted-vs-scatter-gather", "compare",
        l=("Targeted", "One or few shards"),
        r=("Scatter-gather", "Many/all + merge"))
    add(170, "query-routing-decision", "vflow",
        b=[("Contains shard key?", None), ("Yes → map ranges → target", None),
           ("No → broadcast", None)])
    add(171, "full-compound-key-query", "code",
        lines=["{ tenantId, orderId } both present"],
        c="Usually precise routing")
    add(172, "partial-compound-key-query", "compare",
        l=("Leading field present", "May target ranges"),
        r=("Only trailing field", "Usually broad"))
    add(173, "missing-leading-field", "vflow",
        b=[("Filter on orderId only", None), ("Compound key starts with tenantId", None),
           ("Cannot isolate shard", None)])
    add(174, "hashed-key-equality-routing", "hflow",
        b=[("Equality value", None), ("Hash", None), ("One shard", None)])
    add(175, "global-aggregation", "fan",
        t=("mongos merge",),
        k=[("Partial $group A", None), ("Partial $group B", None), ("Partial $group C", None)])
    add(176, "scatter-gather-cost", "row",
        b=[("Network", None), ("Shard CPU", None), ("Merge latency", None)])
    add(177, "customer-order-history-routing", "hflow",
        b=[("customerId C101", None), ("mongos", None), ("That customer's shard", None)])
    add(178, "global-monthly-report-routing", "fan",
        t=("Monthly revenue, no customerId",),
        k=[("A", None), ("B", None), ("C", None)])

    # --- hotspots ---
    add(179, "hot-shard-overview", "row",
        b=[("A normal", None), ("B HOT", "Writes + CPU + disk"), ("C idle", None)])
    add(180, "write-hotspot-sequential", "hflow",
        b=[("Increasing createdAt", None), ("Ranged max chunk", None), ("One shard takes writes", None)])
    add(181, "read-hotspot-tenant", "compare",
        l=("Celebrity tenant", "Most finds"),
        r=("That tenant's shard", "Saturated"))
    add(182, "popular-product-hotspot", "vflow",
        b=[("Viral SKU", None), ("Key routes to one shard", None), ("Cache may be the fix", None)])
    add(183, "storage-hotspot", "row",
        b=[("A 200 GB", None), ("B 210 GB", None), ("C 1.8 TB", None)])
    add(184, "hotspot-diagnosis-flow", "vflow",
        b=[("Compare traffic and size", None), ("Inspect key distribution", None),
           ("Check targeting vs scatter", None), ("Resource metrics", None)])
    add(185, "hotspot-mitigations", "row",
        b=[("Hashed / compound", None), ("Zones / isolate tenant", None), ("Cache / redesign", None)])

    # --- distributed ops ---
    add(186, "distributed-write-path", "hflow",
        b=[("mongos", None), ("Shard primary", None), ("Shard secondaries", None), ("Ack", None)])
    add(187, "write-concern-in-sharded", "vflow",
        b=[("Router sends write", None), ("Target shard RS acknowledges", None),
           ("Client success follows that shard's w", None)])
    add(188, "single-shard-transaction", "hflow",
        b=[("Txn ops", None), ("One shard", None), ("Local coordination", None)])
    add(189, "cross-shard-transaction", "fan",
        t=("Coordinator",),
        k=[("Shard A", None), ("Shard B", None), ("Shard C", None)])
    add(190, "single-vs-distributed-txn", "compare",
        l=("Single shard", "Cheaper"),
        r=("Multi-shard", "Network + coordination"))
    add(191, "distributed-txn-cost", "row",
        b=[("Latency", None), ("Failure complexity", None), ("Resource use", None)])
    add(192, "unique-in-sharded", "vflow",
        b=[("Unique index", None), ("Must be compatible with shard key", None),
           ("Confirm version rules", None)])
    add(193, "global-business-id", "compare",
        l=("Need unique orderNumber", None),
        r=("Design key + uniqueness together", None))
    add(194, "resharding-concept", "hflow",
        b=[("Old key", None), ("Redistribute", None), ("New key", None)])
    add(195, "before-after-resharding", "compare",
        l=("Before", "Hot ranged createdAt"),
        r=("After", "customerId-leading key"))
    add(196, "resharding-impact", "row",
        b=[("Copying", None), ("CPU / disk", None), ("Metadata", None), ("Monitor", None)])

    # --- cluster health ---
    add(197, "sharded-cluster-health", "row",
        b=[("mongos up?", None), ("CSRS healthy?", None), ("Shards have primaries?", None)])
    add(198, "sh-status-concept-map", "code",
        lines=["sh.status()"],
        b=[("Shards", None), ("Keys / ranges", None), ("Balancer", None)])
    add(199, "one-shard-member-failure", "vflow",
        b=[("One mongod on shard A down", None), ("Shard A RS still has a primary", None),
           ("Cluster continues", None)])
    add(200, "shard-primary-failure", "vflow",
        b=[("Shard B primary down", None), ("Ops targeting B wait", None), ("B elects", None)])
    add(201, "complete-shard-unavailability", "compare",
        l=("Queries for that shard's data", "Fail / error"),
        r=("Other shards", "Still serve their ranges"))
    add(202, "one-router-failure", "compare",
        l=("mongos 1 down", None),
        r=("mongos 2 continues", None))
    add(203, "csrs-availability-problem", "vflow",
        b=[("Config RS degraded", None), ("Routing updates / DDL suffer", None), ("Serious incident", None)])
    add(204, "balancer-activity-monitoring", "row",
        b=[("Migrations running?", None), ("Uneven still?", None), ("I/O impact?", None)])
    add(205, "sharded-ops-checklist", "table",
        h=["Check", "Look at"],
        r=[("Routers", "Pool / health"),
           ("Shards + CSRS", "Primaries"),
           ("Distribution", "Ranges / size"),
           ("Targeting", "explain"),
           ("Backups", "Whole cluster")])

    # --- case study ---
    add(206, "standalone-to-replica-set", "hflow",
        b=[("One mongod", None), ("Add members", None), ("Replica set", None)])
    add(207, "replica-set-to-sharded", "hflow",
        b=[("One RS", None), ("Add shards", None), ("Sharded RS cluster", None)])
    add(208, "capacity-growth-timeline", "hflow",
        b=[("Dev standalone", None), ("Prod replica set", None), ("Shard when measured", None)])
    add(209, "ecommerce-replica-set", "row",
        b=[("products", "copied"), ("customers", "copied"), ("orders", "copied")])
    add(210, "ecommerce-sharded-architecture", "fan",
        t=("mongos",),
        k=[("orders sharded", None), ("products maybe later", None), ("config RS", None)])
    add(211, "ecommerce-order-sharding", "row",
        b=[("customerId", None), ("hashed customerId", None), ("{tenantId, orderId}", None)])
    add(212, "collection-by-collection", "table",
        h=["Collection", "First move"],
        r=[("orders", "Shard when writes require"),
           ("products", "Replica set first"),
           ("customers", "Usually later"),
           ("reviews", "Measure"),
           ("sessions", "TTL; rarely shard first")])
    add(213, "order-processing-write-path", "hflow",
        b=[("Checkout", None), ("mongos", None), ("Order shard P", None), ("Replicate", None)])
    add(214, "customer-history-read-path", "hflow",
        b=[("customerId", None), ("mongos", None), ("Targeted shard", None)])
    add(215, "global-sales-report-path", "fan",
        t=("Analytics",),
        k=[("All shards", "Partial agg"), ("mongos", "Merge")])
    add(216, "regional-ecommerce", "compare",
        l=("Canada zone", "CA shards as RS"),
        r=("Europe zone", "EU shards as RS"))
    add(217, "complete-production-architecture", "fan",
        t=("Apps + monitoring + backups",),
        k=[("mongos pool", None), ("CSRS", None), ("Shard replica sets", None)])

    # --- mistakes ---
    add(218, "replication-is-not-sharding", "compare",
        l=("Replication", "Same data copied"),
        r=("Sharding", "Data partitioned"))
    add(219, "sharding-is-not-backup", "compare",
        l=("Shards", "Pieces of live data"),
        r=("Backups", "Independent restore"))
    add(220, "arbiter-is-not-a-copy", "compare",
        l=("Data-bearing member", "Has documents"),
        r=("Arbiter", "Vote only"))
    add(221, "one-host-connection", "compare",
        l=("Anti-pattern", "mongodb://primary-only"),
        r=("Correct", "Replica-set / SRV URI"))
    add(222, "all-members-one-domain", "row",
        b=[("Single AZ", "P+S+S")],
        c="One zone outage = no majority")
    add(223, "low-cardinality-antipattern", "row",
        b=[("status=PAID", "almost all writes")])
    add(224, "monotonic-key-antipattern", "hflow",
        b=[("createdAt++", None), ("Always last range", None), ("Hot shard", None)])
    add(225, "frequent-scatter-gather", "fan",
        t=("Hot-path query missing key",),
        k=[("A", None), ("B", None), ("C", None)])
    add(226, "premature-sharding", "vflow",
        b=[("Slow queries", None), ("Fix schema + indexes first", None), ("Shard only with evidence", None)])
    add(227, "secondary-reads-universal-fix", "vflow",
        b=[("App is slow", None), ("Move reads to secondaries?", None),
           ("Check lag, capacity, indexes first", None)])

    # --- troubleshooting ---
    add(228, "distributed-troubleshooting-flow", "hflow",
        b=[("App", None), ("Driver", None), ("mongos", None), ("RS / disk / net", None)])
    add(229, "replica-set-troubleshooting-flow", "vflow",
        b=[("Primary present?", None), ("Majority?", None), ("Lag?", None), ("Oplog / network?", None)])
    add(230, "no-primary-available", "row",
        b=[("No majority", None), ("Network split", None), ("All down", None)])
    add(231, "increasing-lag-branches", "row",
        b=[("Disk", None), ("CPU", None), ("Network", None), ("Writes", None), ("Reports", None)])
    add(232, "write-concern-timeout-diagnosis", "vflow",
        b=[("Primary applied?", None), ("Secondaries ack?", None), ("wtimeout point", None)])
    add(233, "stale-secondary-read-diagnosis", "vflow",
        b=[("Which read preference?", None), ("Which member?", None), ("How much lag?", None)])
    add(234, "sharded-query-troubleshooting", "vflow",
        b=[("mongos up?", None), ("Shard-key in filter?", None), ("Targeted shards?", None), ("Merge cost?", None)])
    add(235, "unexpected-scatter-gather", "row",
        b=[("Missing key", None), ("Wrong type", None), ("Broad range", None), ("Hashed range", None)])
    add(236, "uneven-distribution-diagnosis", "row",
        b=[("Key skew", None), ("Zones", None), ("Balancer off", None), ("Jumbo range", None)])
    add(237, "hot-shard-diagnosis", "vflow",
        b=[("High traffic on one shard", None), ("Key + queries", None), ("Dominant tenant/range", None)])
    add(238, "cluster-failure-isolation", "table",
        h=["Failure", "Blast radius"],
        r=[("One mongos", "Use another router"),
           ("Shard member", "Shard RS HA"),
           ("Shard primary", "That shard elects"),
           ("CSRS", "Metadata / DDL")])

    # --- exercises ---
    add(239, "ex-7-1-replication-or-sharding", "row",
        b=[("Replication", None), ("Sharding", None), ("Both", None), ("Neither yet", None)])
    add(240, "ex-7-2-label-replica-set", "fan",
        t=("App + driver",),
        k=[("Primary ?", None), ("Secondary ?", None), ("Oplog / HB ?", None)])
    add(241, "ex-7-3-trace-write", "hflow",
        b=[("Client", None), ("Primary", None), ("Oplog", None), ("Secondaries", None), ("Ack", None)])
    add(242, "ex-7-4-sequence-failover", "vflow",
        b=[("Unavailable", None), ("Detect", None), ("Vote", None), ("New primary", None), ("Retry", None)])
    add(243, "ex-7-5-select-settings", "table",
        h=["Operation", "Bias"],
        r=[("Payment", "Primary + majority"),
           ("Catalog", "Staleness OK?"),
           ("Analytics", "Secondary capacity")])
    add(244, "ex-7-6-diagnose-lag", "row",
        b=[("Disk", None), ("Network", None), ("Reports", None), ("Oplog", None)])
    add(245, "ex-7-7-label-cluster", "fan",
        t=("mongos ?",),
        k=[("Shards ?", None), ("CSRS ?", None), ("Metadata ?", None)])
    add(246, "ex-7-8-evaluate-keys", "table",
        h=["Key", "Score lens"],
        r=[("status", "Cardinality"),
           ("createdAt", "Monotonic"),
           ("customerId", "Targeting")])
    add(247, "ex-7-9-targeted-or-scatter", "compare",
        l=("Has shard key", "Targeted?"),
        r=("paymentStatus only", "Scatter-gather"))
    add(248, "ex-7-10-ranged-or-hashed", "compare",
        l=("History + ranges", "Ranged compound"),
        r=("UUID equality", "Hashed"))
    add(249, "ex-7-11-find-the-hotspot", "row",
        b=[("A quiet", None), ("B HOT", None), ("C quiet", None)])
    add(250, "ex-7-12-design-deployment", "row",
        b=[("HA", "Replica sets"), ("Scale", "Shard orders"), ("Residency", "Zones / regions")])

    # --- labs ---
    add(251, "lab-7-1-health-inspection", "hflow",
        b=[("RS URI", None), ("rs.status()", None), ("rs.conf()", None), ("Health notes", None)])
    add(252, "lab-7-2-replication-verification", "hflow",
        b=[("Insert", None), ("Oplog", None), ("Secondary copy", None), ("Delete probe", None)])
    add(253, "lab-7-3-failover-observation", "hflow",
        b=[("Record P", None), ("stepDown", None), ("Election", None), ("New P", None)])
    add(254, "lab-7-4-read-write-policy", "row",
        b=[("primary read", None), ("secondaryPreferred", None), ("w majority vs 1", None)])
    add(255, "lab-7-5-lag-investigation", "vflow",
        b=[("Optimes", None), ("Metrics", None), ("Oplog window", None), ("Actions", None)])
    add(256, "lab-7-6-cluster-inspection", "row",
        b=[("mongos", None), ("shards", None), ("CSRS", None), ("keys", None)])
    add(257, "lab-7-7-shard-training-collection", "vflow",
        b=[("Index", None), ("shardCollection", None), ("Insert sample", None), ("sh.status()", None)])
    add(258, "lab-7-8-query-routing-analysis", "row",
        b=[("Full key explain", None), ("Non-key explain", None), ("Scatter?", None)])
    add(259, "lab-7-9-distribution-review", "row",
        b=[("Ranges", None), ("Sizes", None), ("Balancer", None), ("Zones", None)])
    add(260, "lab-7-10-integrated-challenge", "row",
        b=[("Topology", None), ("Shard key", None), ("Routing", None), ("Monitor", None)])
    add(261, "practical-challenge-order-platform", "row",
        b=[("Availability", "Replica set"), ("Shard decision", "Evidence first"),
           ("Key", "Score candidates"), ("Ops", "Lag, backup, retry")])

    return C


LEGACY = {
    "01-module-map.svg": 7,
    "02-requirements.svg": 8,
    "03-ha-vs-scale.svg": 2,
    "04-vertical-horizontal.svg": 3,
    "05-replication-vs-sharding.svg": 4,
    "06-distributed-overview.svg": 1,
    "07-replica-set.svg": 9,
    "08-members.svg": 12,
    "09-primary.svg": 13,
    "10-secondary.svg": 14,
    "11-oplog.svg": 19,
    "12-replication-flow.svg": 20,
    "13-heartbeats.svg": 30,
    "14-elections.svg": 33,
    "15-failover.svg": 34,
    "16-app-failover.svg": 36,
    "17-majority.svg": 39,
    "18-priority.svg": 47,
    "19-arbiter.svg": 54,
    "20-hidden.svg": 49,
    "21-delayed.svg": 51,
    "22-read-pref.svg": 57,
    "23-write-concern.svg": 69,
    "24-three-settings.svg": 77,
    "25-lag.svg": 78,
    "26-rollback.svg": 86,
    "27-rs-status.svg": 92,
    "28-failure-scenarios.svg": 94,
    "29-what-is-sharding.svg": 103,
    "30-cluster-components.svg": 101,
    "31-shards.svg": 108,
    "32-csrs.svg": 113,
    "33-mongos.svg": 118,
    "34-request-flow.svg": 119,
    "35-shard-key.svg": 124,
    "36-cardinality.svg": 127,
    "37-frequency.svg": 130,
    "38-monotonic.svg": 132,
    "39-query-isolation.svg": 134,
    "40-ranged.svg": 138,
    "41-hashed.svg": 143,
    "42-zoned.svg": 148,
    "43-ranged-vs-hashed.svg": 147,
    "44-compound.svg": 135,
    "45-chunks.svg": 153,
    "46-split.svg": 156,
    "47-balancer.svg": 158,
    "48-migration.svg": 161,
    "49-targeted.svg": 166,
    "50-scatter-gather.svg": 168,
    "51-hotspots.svg": 179,
    "52-distributed-writes.svg": 186,
    "53-together.svg": 5,
    "54-decision.svg": 6,
    "55-ecommerce.svg": 212,
    "56-mistakes.svg": 218,
    "57-troubleshoot.svg": 228,
    "58-concept-map.svg": 5,
    "59-ex-choice.svg": 239,
    "60-challenge.svg": 261,
    "61-demo-rs.svg": 92,
    "62-lab-health.svg": 251,
}


def write_all() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    by_n: dict[int, str] = {}
    items = catalog()
    missing = [i for i in range(1, 262) if i not in {n for n, *_ in items}]
    if missing:
        raise SystemExit(f"Missing diagram numbers: {missing}")
    extra = [n for n, *_ in items if n < 1 or n > 261]
    if extra:
        raise SystemExit(f"Out of range: {extra}")
    if len(items) != 261:
        raise SystemExit(f"Expected 261 catalog rows, got {len(items)}")

    for n, slug, kind, spec in items:
        name = f"{n:03d}-{slug}.svg"
        svg = render(n, kind, spec)
        (ASSETS / name).write_text(svg, encoding="utf-8")
        by_n[n] = name
        print(f"Wrote slides/assets/module-07/{name}")

    for old, n in LEGACY.items():
        src = (ASSETS / by_n[n]).read_text(encoding="utf-8")
        (ASSETS / old).write_text(src, encoding="utf-8")
    print(f"Wrote {len(LEGACY)} legacy aliases")
    return len(items)


if __name__ == "__main__":
    n = write_all()
    print(f"Done. {n} diagrams.")

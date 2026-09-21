"""Module 2 Marp diagrams — Mastering MongoDB.

Numbered 01–76 to match the Module 2 diagram inventory.

    python scripts/module02_diagrams.py
"""
from __future__ import annotations

import html
from pathlib import Path

from marp_svg_common import BORDER, FONT, HEADER_BG, MONO, MUTED, PANEL, RED, TEXT

BG_BOX = "#ffffff"
ASSETS = Path(__file__).resolve().parent.parent / "slides" / "assets" / "module-02"
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
    title_color = RED if header else TEXT
    title_lines = [ln for ln in str(title).split("\n")] or [""]
    extra = 1 if sub else 0
    n = len(title_lines) + extra
    line_h = fs * 1.12
    block = n * line_h
    start = y + h / 2 - block / 2 + fs * 0.78
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{RED}" stroke-width="2"/>',
    ]
    for i, line in enumerate(title_lines):
        parts.append(
            f'<text x="{x + w / 2}" y="{start + i * line_h:.1f}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="{fs}" fill="{title_color}">{_esc(line)}</text>'
        )
    if sub:
        parts.append(
            f'<text x="{x + w / 2}" y="{start + len(title_lines) * line_h:.1f}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="{sub_fs}" fill="{MUTED}">{_esc(sub)}</text>'
        )
    return "\n".join(parts)


def _label(x, y, text, *, fs=16, fill=MUTED, anchor="middle") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" '
        f'font-size="{fs}" fill="{fill}">{_esc(text)}</text>'
    )


def _mono(x, y, text, *, fs=16, fill=TEXT, anchor="start") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" '
        f'font-size="{fs}" fill="{fill}">{_esc(text)}</text>'
    )


def _arrow(x1, y1, x2, y2, mid="ae") -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{RED}" '
        f'stroke-width="2" marker-end="url(#{mid})"/>'
    )


def _step(item) -> tuple[str, str | None]:
    if isinstance(item, tuple):
        return item[0], item[1] if len(item) > 1 else None
    return str(item), None


def _vflow(items, *, x=210, y=20, w=500, h=56, gap=22, mid="ae", fs=18) -> list[str]:
    parts: list[str] = []
    cy = y
    n = len(items)
    for i, item in enumerate(items):
        title, sub = _step(item)
        parts.append(_box(x, cy, w, h, title, sub, fs=fs if not sub else 16, sub_fs=13))
        if i < n - 1:
            parts.append(_arrow(x + w / 2, cy + h, x + w / 2, cy + h + gap - 4, mid))
        cy += h + gap
    return parts


def _hflow(items, *, y=70, h=72, gap=16, x0=20, mid="ae", fs=15) -> list[str]:
    n = len(items)
    usable = W - 40 - gap * (n - 1)
    bw = usable / n
    parts: list[str] = []
    for i, item in enumerate(items):
        title, sub = _step(item)
        x = x0 + i * (bw + gap)
        parts.append(_box(x, y, bw, h, title, sub, fs=fs, sub_fs=12))
        if i < n - 1:
            parts.append(_arrow(x + bw, y + h / 2, x + bw + gap - 3, y + h / 2, mid))
    return parts


def vdiag(items, *, title="", caption="", mid="ae", box_h=58, gap=20, x=200, w=520) -> str:
    top = 40 if title else 16
    bottom = 36 if caption else 16
    height = int(top + len(items) * box_h + (len(items) - 1) * gap + bottom)
    parts: list[str] = []
    if title:
        parts.append(_label(460, 28, title, fs=18, fill=TEXT))
    parts.extend(_vflow(items, x=x, y=top, w=w, h=box_h, gap=gap, mid=mid))
    if caption:
        parts.append(_label(460, height - 14, caption, fs=15))
    return _svg(height, "\n".join(parts), mid)


def hdiag(items, *, title="", caption="", mid="ae", y=64, h=80) -> str:
    height = 200 if caption or title else 170
    if caption:
        height = 220
    parts: list[str] = []
    if title:
        parts.append(_label(460, 28, title, fs=18, fill=TEXT))
    parts.extend(_hflow(items, y=y, h=h, mid=mid))
    if caption:
        parts.append(_label(460, height - 16, caption, fs=15))
    return _svg(height, "\n".join(parts), mid)


def compare2(left, right, *, title="", caption="", mid="ae", rows=None) -> str:
    """left/right: (header, [items]) or rows: list of (topic, a, b)."""
    parts: list[str] = []
    if rows:
        top = 50 if title else 16
        parts.append(_box(24, top, 200, 44, "Topic", header=True, fs=16))
        parts.append(_box(224, top, 336, 44, left, header=True, fs=16))
        parts.append(_box(560, top, 336, 44, right, header=True, fs=16))
        for i, (topic, a, b) in enumerate(rows):
            y = top + 52 + i * 50
            parts.append(_box(24, y, 200, 44, topic, fs=14))
            parts.append(_box(224, y, 336, 44, a, fs=14))
            parts.append(_box(560, y, 336, 44, b, fs=14))
        height = top + 52 + len(rows) * 50 + (28 if caption else 12)
        if title:
            parts.insert(0, _label(460, 28, title, fs=18, fill=TEXT))
        if caption:
            parts.append(_label(460, height - 12, caption, fs=15))
        return _svg(height, "\n".join(parts), mid)

    lh, litems = left
    rh, ritems = right
    n = max(len(litems), len(ritems))
    top = 50 if title else 16
    parts.append(_box(24, top, 430, 48, lh, header=True, fs=18))
    parts.append(_box(466, top, 430, 48, rh, header=True, fs=18))
    for i in range(n):
        y = top + 56 + i * 52
        lt = litems[i] if i < len(litems) else ""
        rt = ritems[i] if i < len(ritems) else ""
        parts.append(_box(24, y, 430, 46, lt, fs=15))
        parts.append(_box(466, y, 430, 46, rt, fs=15))
    height = top + 56 + n * 52 + (30 if caption else 12)
    if title:
        parts.insert(0, _label(460, 28, title, fs=18, fill=TEXT))
    if caption:
        parts.append(_label(460, height - 12, caption, fs=15))
    return _svg(height, "\n".join(parts), mid)


def cols4(headers, bodies, *, title="", caption="", mid="ae") -> str:
    parts: list[str] = []
    if title:
        parts.append(_label(460, 28, title, fs=18, fill=TEXT))
    top = 48 if title else 16
    for i, (h, b) in enumerate(zip(headers, bodies)):
        x = 20 + i * 225
        parts.append(_box(x, top, 210, 54, h, header=True, fs=15))
        yy = top + 62
        if isinstance(b, list):
            for line in b:
                parts.append(_box(x, yy, 210, 48, line, fs=13))
                yy += 54
        else:
            parts.append(_box(x, top + 62, 210, 90, b, fs=14))
            yy = top + 162
    height = max(yy + (28 if caption else 12), 200)
    if caption:
        parts.append(_label(460, height - 12, caption, fs=15))
    return _svg(int(height), "\n".join(parts), mid)


def grid(items, *, cols=4, title="", caption="", mid="ae", cell_h=72) -> str:
    parts: list[str] = []
    if title:
        parts.append(_label(460, 28, title, fs=18, fill=TEXT))
    top = 48 if title else 16
    gap = 12
    n = len(items)
    rows = (n + cols - 1) // cols
    cw = (W - 40 - gap * (cols - 1)) / cols
    for i, item in enumerate(items):
        r, c = divmod(i, cols)
        x = 20 + c * (cw + gap)
        y = top + r * (cell_h + gap)
        title_s, sub = _step(item)
        parts.append(_box(x, y, cw, cell_h, title_s, sub, fs=14, sub_fs=12))
    height = top + rows * (cell_h + gap) + (20 if caption else 8)
    if caption:
        parts.append(_label(460, height - 12, caption, fs=15))
    return _svg(int(height), "\n".join(parts), mid)


def uri_bar(segments, *, title="", caption="", mid="ae", unlabeled=False) -> str:
    """segments: list of (label, sample_text, width_frac)."""
    parts: list[str] = []
    if title:
        parts.append(_label(460, 28, title, fs=18, fill=TEXT))
    y = 56 if title else 24
    x = 24
    total = 872
    for label, sample, frac in segments:
        w = max(total * frac - 6, 70)
        shown = " " if unlabeled else sample
        parts.append(_box(x, y, w, 58, shown, fs=13))
        parts.append(_label(x + w / 2, y + 82, label if not unlabeled else "?", fs=13, fill=RED if unlabeled else MUTED))
        x += w + 6
    height = 180
    if caption:
        height = 200
        parts.append(_label(460, 188, caption, fs=15, fill=RED if "never" in caption.lower() or "password" in caption.lower() else MUTED))
    return _svg(height, "\n".join(parts), mid)


# --- 01–09 Core concept ---


def d01_environment_overview() -> str:
    return vdiag(
        [
            "Developer",
            ("mongosh, Compass, or driver", "Clients"),
            ("MongoDB server", "mongod"),
            "Database files",
        ],
        title="MongoDB environment overview",
        caption="Clients talk to one server; the server owns the files",
        mid="ae01",
    )


def d02_deployment_options() -> str:
    return cols4(
        ["Local", "Self-managed", "Container", "Managed cloud"],
        [
            ["Workstation install", "Labs and learning"],
            ["Org server or VM", "Direct control"],
            ["Disposable instance", "Tests and demos"],
            ["Provider cluster", "Shared / less ops"],
        ],
        title="Four common MongoDB deployment options",
        caption="Commands stay similar; operations ownership changes",
        mid="ae02",
    )


def d03_local_deployment() -> str:
    parts = [
        _label(460, 28, "Local MongoDB on the developer workstation", fs=18, fill=TEXT),
        _box(200, 48, 520, 48, "Developer workstation", header=True, fs=18),
        _box(40, 120, 200, 80, "mongod", "Server process", fs=18, sub_fs=14),
        _box(255, 120, 200, 80, "mongosh", "Shell client", fs=18, sub_fs=14),
        _box(470, 120, 200, 80, "Compass", "GUI client", fs=18, sub_fs=14),
        _box(685, 120, 200, 80, "Config file", fs=18),
        _box(150, 230, 280, 80, "Data directory", fs=18),
        _box(490, 230, 280, 80, "Log files", fs=18),
        _label(460, 340, "Default: localhost:27017  ·  internet usually not required", fs=15),
    ]
    return _svg(365, "\n".join(parts), "ae03")


def d04_managed_cloud() -> str:
    return vdiag(
        [
            "Developer workstation",
            ("Secure internet connection", "TLS"),
            ("Managed MongoDB cluster", "Provider operates infrastructure"),
        ],
        title="Managed cloud deployment",
        caption="You still create a database user and allow the client network",
        mid="ae04",
        box_h=70,
    )


def d05_containerized() -> str:
    return vdiag(
        [
            "Developer",
            ("Published port", "Host maps to container, e.g. 27017"),
            ("MongoDB container", "Image · env · lifecycle"),
            ("Persistent volume", "Data survives restart"),
        ],
        title="Containerized MongoDB",
        caption="Removing a container without a volume can delete the data",
        mid="ae05",
    )


def d06_self_managed() -> str:
    return vdiag(
        [
            "Client workstation",
            ("Organizational network", "Firewall and DNS you control"),
            ("MongoDB server or VM", "Your team patches and backs up"),
            "Attached storage",
        ],
        title="Self-managed server deployment",
        caption="Direct infrastructure control — and full operational responsibility",
        mid="ae06",
    )


def d07_local_vs_cloud() -> str:
    return compare2(
        "Local",
        "Managed cloud",
        title="Local vs. managed cloud",
        rows=[
            ("Setup", "Install on workstation", "Provision in a portal"),
            ("Infrastructure", "User manages", "Provider manages"),
            ("Internet", "Usually not required", "Required"),
            ("Scaling", "Manual", "Platform-supported"),
            ("Backups", "User responsibility", "Managed options"),
            ("Maintenance", "Patches and disks", "Provider operations"),
        ],
        caption="Database commands are similar; operations ownership differs",
        mid="ae07",
    )


def d08_decision_flow() -> str:
    parts = [
        _label(460, 28, "Choose a deployment from constraints, not habit", fs=18, fill=TEXT),
        _box(310, 48, 300, 54, "Primary use?", header=True, fs=18),
        _arrow(360, 102, 160, 140, "ae08"),
        _arrow(460, 102, 460, 140, "ae08"),
        _arrow(560, 102, 760, 140, "ae08"),
        _box(40, 142, 240, 70, "Offline / classroom lab", "Local install", fs=15, sub_fs=13),
        _box(340, 142, 240, 70, "Disposable tests", "Container", fs=15, sub_fs=13),
        _box(640, 142, 240, 70, "Shared or production", "See next question", fs=15, sub_fs=13),
        _arrow(760, 212, 760, 240, "ae08"),
        _box(40, 248, 400, 70, "Need direct infra control?", "Self-managed server or VM", fs=15, sub_fs=13),
        _box(480, 248, 400, 70, "Prefer less server ops?", "Managed cloud", fs=15, sub_fs=13),
        _label(460, 350, "Also weigh internet, admin rights, persistence, backups, and scale", fs=15),
    ]
    return _svg(375, "\n".join(parts), "ae08")


def d09_install_workflow() -> str:
    return hdiag(
        ["Choose", "Install or\nprovision", "Configure", "Start", "Connect", "Test", "Validate"],
        title="Installation and verification workflow",
        caption="Finish with a write-and-read — not only a successful ping",
        mid="ae09",
        h=86,
    )


# --- 10–17 Components ---


def d10_server_clients() -> str:
    parts = [
        _label(460, 28, "mongod is the server; everything else is a client or tool", fs=18, fill=TEXT),
        _box(310, 50, 300, 70, "mongod", "MongoDB server", fs=22, sub_fs=16),
        _box(20, 200, 200, 80, "mongosh", fs=18),
        _box(246, 200, 200, 80, "Compass", fs=18),
        _box(472, 200, 200, 80, "App driver", fs=18),
        _box(698, 200, 200, 80, "DB tools", "Import / export", fs=16, sub_fs=13),
        _arrow(200, 200, 400, 120, "ae10"),
        _arrow(346, 200, 430, 120, "ae10"),
        _arrow(572, 200, 490, 120, "ae10"),
        _arrow(720, 200, 540, 120, "ae10"),
    ]
    return _svg(310, "\n".join(parts), "ae10")


def d11_mongod_vs_mongosh() -> str:
    return compare2(
        ("mongod — server", ["Stores data", "Processes operations", "Manages files and indexes", "Writes logs", "Enforces security"]),
        ("mongosh — client", ["Sends commands", "Interactive JavaScript shell", "Not the database", "Same data as Compass", "Connects over the URI"]),
        title="mongod vs. mongosh",
        caption="A common misconception: mongosh is not the MongoDB server",
        mid="ae11",
    )


def d12_client_options() -> str:
    parts = [
        _label(460, 28, "Three clients — one MongoDB deployment", fs=18, fill=TEXT),
        _box(20, 56, 260, 80, "mongosh", "Shell", fs=20, sub_fs=14),
        _box(330, 56, 260, 80, "Compass", "GUI", fs=20, sub_fs=14),
        _box(640, 56, 260, 80, "Application driver", "Your code", fs=18, sub_fs=14),
        _arrow(150, 136, 460, 190, "ae12"),
        _arrow(460, 136, 460, 190, "ae12"),
        _arrow(770, 136, 460, 190, "ae12"),
        _box(260, 194, 400, 70, "MongoDB deployment", fs=20),
    ]
    return _svg(290, "\n".join(parts), "ae12")


def d13_environment_components() -> str:
    return vdiag(
        [
            "Client tools",
            "Network connection",
            ("Server process", "mongod"),
            "Storage engine",
            "Data and indexes",
        ],
        title="MongoDB environment components",
        caption="A failure can sit at any layer — not only “is MongoDB installed?”",
        mid="ae13",
        box_h=52,
        gap=16,
    )


def d14_storage_structure() -> str:
    return vdiag(
        [
            "MongoDB deployment",
            ("Database", "e.g. training_store"),
            ("Collection", "e.g. products"),
            "Document",
            "Field",
        ],
        title="Data storage structure",
        caption="Deployment → database → collection → document → field",
        mid="ae14",
        box_h=52,
        gap=16,
    )


def d15_filesystem() -> str:
    parts = [
        _label(460, 28, "File-system pieces of a local MongoDB", fs=18, fill=TEXT),
        _box(310, 50, 300, 64, "mongod process", fs=18),
        _box(20, 170, 210, 90, "Config file", "ports, paths, security", fs=16, sub_fs=13),
        _box(246, 170, 210, 90, "Data directory", "collections, indexes", fs=16, sub_fs=13),
        _box(472, 170, 210, 90, "Log directory", "startup, errors", fs=16, sub_fs=13),
        _box(698, 170, 200, 90, "Server process", "uses all three", fs=16, sub_fs=13),
        _arrow(460, 114, 125, 170, "ae15"),
        _arrow(460, 114, 351, 170, "ae15"),
        _arrow(460, 114, 577, 170, "ae15"),
        _arrow(460, 114, 798, 170, "ae15"),
    ]
    return _svg(290, "\n".join(parts), "ae15")


def d16_config_map() -> str:
    parts = [
        _label(460, 28, "Configuration file map", fs=18, fill=TEXT),
        _box(310, 48, 300, 54, "mongod config (YAML)", header=True, fs=16),
        _box(20, 140, 140, 80, "Storage", "dbPath", fs=15, sub_fs=13),
        _box(172, 140, 140, 80, "Logging", "log path", fs=15, sub_fs=13),
        _box(324, 140, 140, 80, "Network", "port, bindIp", fs=14, sub_fs=12),
        _box(476, 140, 140, 80, "Security", "auth", fs=15, sub_fs=13),
        _box(628, 140, 140, 80, "Replication", fs=14),
        _box(780, 140, 120, 80, "Process", fs=14),
        _arrow(460, 102, 90, 140, "ae16"),
        _arrow(460, 102, 242, 140, "ae16"),
        _arrow(460, 102, 394, 140, "ae16"),
        _arrow(460, 102, 546, 140, "ae16"),
        _arrow(460, 102, 698, 140, "ae16"),
        _arrow(460, 102, 840, 140, "ae16"),
        _label(460, 250, "Do not broaden bindIp without authentication and network controls", fs=15, fill=RED),
    ]
    return _svg(275, "\n".join(parts), "ae16")


def d17_data_log_flow() -> str:
    parts = [
        _label(460, 28, "Operations persist data; events persist in logs", fs=18, fill=TEXT),
        _box(20, 56, 200, 70, "Client operation", fs=16),
        _arrow(220, 91, 270, 91, "ae17"),
        _box(272, 56, 240, 70, "MongoDB server", fs=16),
        _arrow(512, 80, 580, 80, "ae17"),
        _arrow(512, 100, 580, 150, "ae17"),
        _box(584, 50, 300, 64, "Data files", fs=16),
        _box(584, 130, 300, 64, "Log files", "startup, auth, errors", fs=16, sub_fs=13),
        _label(460, 230, "If the server fails to start, inspect the server log first", fs=15),
    ]
    return _svg(255, "\n".join(parts), "ae17")


# --- 18–24 Install / provision ---


def d18_local_install() -> str:
    return hdiag(
        ["Download or\npackage repo", "Install server", "Configure\ndirectories", "Start service", "Verify"],
        title="Local installation process",
        caption="Steps vary by OS — follow the instructor install sheet",
        mid="ae18",
        h=88,
    )


def d19_cloud_provision() -> str:
    return hdiag(
        ["Project", "Deployment", "Database user", "Network access", "Connection string", "Connect"],
        title="Managed-cloud provisioning",
        caption="A user and an allowed network source are required before connecting",
        mid="ae19",
        h=86,
    )


def d20_container_setup() -> str:
    return hdiag(
        ["Image", "Environment", "Port mapping", "Container", "Persistent volume"],
        title="Container setup process",
        caption="Map the port and attach a volume before you treat it as durable",
        mid="ae20",
        h=80,
    )


def d21_service_lifecycle() -> str:
    return hdiag(
        ["Install", "Register service", "Start", "Running", "Stop", "Restart"],
        title="Operating-system service lifecycle",
        caption="Stop gracefully. Confirm state. Avoid force-kill unless recovering.",
        mid="ae21",
        h=78,
    )


def d22_startup() -> str:
    return vdiag(
        [
            "Read configuration",
            "Validate paths",
            "Open port",
            "Initialize storage",
            "Accept connections",
        ],
        title="MongoDB startup sequence",
        caption="A failure here usually shows in the server log, not in mongosh",
        mid="ae22",
        box_h=50,
        gap=16,
    )


def d23_shutdown() -> str:
    return vdiag(
        [
            "Stop request",
            "Finish in-flight operations",
            "Flush data",
            "Close files",
            "Stop service",
        ],
        title="MongoDB shutdown sequence",
        caption="Graceful stop protects data files; a kill can leave a recovery on next start",
        mid="ae23",
        box_h=50,
        gap=16,
    )


def d24_readiness_flow() -> str:
    return vdiag(
        [
            "Server running?",
            "Port available?",
            "Client installed?",
            "Authentication valid?",
            "Read/write successful?",
        ],
        title="Environment readiness flow",
        caption="Ping proves reachability. A write-and-read proves usable access.",
        mid="ae24",
        box_h=50,
        gap=16,
    )


# --- 25–35 Networking ---


def d25_basic_connection() -> str:
    return hdiag(
        ["User", "Client tool", "Host and port", "MongoDB server", "Response"],
        title="Basic connection flow",
        caption="The URI names the host, port, credentials, and options",
        mid="ae25",
        h=78,
    )


def d26_localhost() -> str:
    parts = [
        _label(460, 28, "Localhost: client and server on the same workstation", fs=18, fill=TEXT),
        _box(40, 70, 380, 120, "mongosh / Compass", "Client", fs=18, sub_fs=14),
        _box(500, 70, 380, 120, "mongod", "Server", fs=18, sub_fs=14),
        _arrow(420, 130, 500, 130, "ae26"),
        _label(460, 230, "mongodb://localhost:27017", fs=18, fill=TEXT),
        _label(460, 262, "No internet required for this path", fs=15),
    ]
    return _svg(290, "\n".join(parts), "ae26")


def d27_remote() -> str:
    return hdiag(
        ["Client", "Network or\ninternet", "Firewall", "MongoDB host", "Database"],
        title="Remote MongoDB connection",
        caption="A running database can still be unreachable on the network",
        mid="ae27",
        h=88,
    )


def d28_cloud_secure() -> str:
    return vdiag(
        [
            ("Approved client IP", "Network allowlist"),
            ("Encrypted connection", "TLS"),
            "Cloud deployment",
            ("Authenticated database user", "Username + password + auth DB"),
        ],
        title="Managed-cloud secure connection",
        caption="IP allowlist, TLS, and a database user are all required",
        mid="ae28",
    )


def d29_host_port() -> str:
    return grid(
        [
            ("Hostname", "db.example.net"),
            ("IP address", "Resolved by DNS"),
            ("Port", "Default 27017"),
            ("Network interface", "bindIp"),
            ("Firewall boundary", "May block 27017"),
            ("Localhost", "Loopback only"),
        ],
        cols=3,
        title="Host and port anatomy",
        caption="Wrong host, wrong port, or a closed firewall all look like “cannot connect”",
        mid="ae29",
        cell_h=84,
    )


def d30_network_path() -> str:
    return hdiag(
        ["Client", "DNS", "Network route", "Firewall or\nallowlist", "MongoDB\nlistener"],
        title="Network access path",
        caption="Timeouts often live on this path — not in the query language",
        mid="ae30",
        h=88,
    )


def d31_uri_anatomy() -> str:
    return uri_bar(
        [
            ("protocol", "mongodb://", 0.16),
            ("username", "user", 0.12),
            ("password", "****", 0.12),
            ("host", "host", 0.16),
            ("port", "27017", 0.12),
            ("database", "db", 0.14),
            ("options", "?…", 0.14),
        ],
        title="Connection string anatomy",
        caption="Never put a real password in slides, screenshots, or source code",
        mid="ae31",
    )


def d32_standard_uri() -> str:
    return uri_bar(
        [
            ("protocol", "mongodb://", 0.18),
            ("username", "username", 0.16),
            ("password", "password", 0.16),
            ("host", "host", 0.18),
            ("port", "27017", 0.14),
            ("database", "database", 0.16),
        ],
        title="Standard MongoDB URI",
        caption="mongodb://username:password@host:27017/database",
        mid="ae32",
    )


def d33_srv_uri() -> str:
    return uri_bar(
        [
            ("protocol", "mongodb+srv://", 0.24),
            ("username", "username", 0.18),
            ("password", "password", 0.18),
            ("cluster host", "cluster-host", 0.22),
            ("database", "database", 0.16),
        ],
        title="DNS seed-list URI",
        caption="mongodb+srv://username:password@cluster-host/database",
        mid="ae33",
    )


def d34_uri_vs_srv() -> str:
    return compare2(
        ("mongodb://", ["Lists host and port", "Direct connection", "Typical for local", "localhost:27017"]),
        ("mongodb+srv://", ["DNS seed list", "Discovers members", "Typical for managed clusters", "Port often omitted"]),
        title="mongodb:// vs. mongodb+srv://",
        caption="Same clients. Different discovery. Placeholders only in teaching materials.",
        mid="ae34",
    )


def d35_establish_seq() -> str:
    return vdiag(
        [
            "Parse URI",
            "Resolve host",
            "Establish network connection",
            "Negotiate security (TLS)",
            "Authenticate",
            "Select database",
        ],
        title="Connection establishment sequence",
        caption="Read the error: it usually names which step failed",
        mid="ae35",
        box_h=46,
        gap=14,
    )


# --- 36–41 Shell and Compass ---


def d36_connect_mongosh() -> str:
    return hdiag(
        ["Terminal", "Connection string", "MongoDB server", "Interactive shell"],
        title="Connecting with mongosh",
        caption='mongosh "mongodb://localhost:27017"',
        mid="ae36",
        h=78,
    )


def d37_shell_command_flow() -> str:
    return hdiag(
        ["User command", "Shell", "MongoDB server", "Operation result", "Terminal output"],
        title="MongoDB Shell command flow",
        caption="The shell is a client. The server executes the operation.",
        mid="ae37",
        h=78,
    )


def d38_connect_compass() -> str:
    return hdiag(
        ["Compass screen", "Connection string", "Server", "Database explorer"],
        title="Connecting with MongoDB Compass",
        caption="Paste the URI, review settings, then connect — same data as mongosh",
        mid="ae38",
        h=80,
    )


def d39_compass_workspace() -> str:
    parts = [
        _label(460, 28, "Compass workspace — one deployment, several views", fs=18, fill=TEXT),
        _box(20, 56, 200, 70, "Navigator", fs=16),
        _arrow(220, 91, 248, 91, "ae39"),
        _box(250, 56, 160, 70, "Database", fs=16),
        _arrow(410, 91, 438, 91, "ae39"),
        _box(440, 56, 160, 70, "Collection", fs=16),
        _box(640, 40, 260, 52, "Documents", fs=15),
        _box(640, 98, 260, 52, "Schema", fs=15),
        _box(640, 156, 260, 52, "Indexes", fs=15),
        _box(640, 214, 260, 52, "Aggregations", fs=15),
        _arrow(600, 91, 640, 66, "ae39"),
        _arrow(600, 91, 640, 124, "ae39"),
        _arrow(600, 91, 640, 182, "ae39"),
        _arrow(600, 91, 640, 240, "ae39"),
        _label(300, 200, "Explore the same MongoDB", fs=15),
    ]
    return _svg(290, "\n".join(parts), "ae39")


def d40_shell_vs_compass() -> str:
    parts = [
        _label(460, 28, "Two interfaces — one MongoDB", fs=18, fill=TEXT),
        _box(40, 56, 360, 90, "mongosh", "Command-line client", fs=22, sub_fs=16),
        _box(520, 56, 360, 90, "Compass", "Graphical client", fs=22, sub_fs=16),
        _arrow(220, 146, 460, 190, "ae40"),
        _arrow(700, 146, 460, 190, "ae40"),
        _box(260, 194, 400, 70, "Same MongoDB deployment", fs=18),
    ]
    return _svg(290, "\n".join(parts), "ae40")


def d41_driver() -> str:
    return vdiag(
        [
            "Application code",
            "MongoDB driver",
            ("Connection pool", "Reusable sockets"),
            "MongoDB server",
        ],
        title="Application driver connection",
        caption="Drivers use the same URI family as mongosh and Compass",
        mid="ae41",
    )


# --- 42–49 Database creation / verify ---


def d42_create_db() -> str:
    return vdiag(
        [
            'use training_store',
            "createCollection or insert",
            "Database persists and appears in show dbs",
        ],
        title="Creating the training database",
        caption="Selecting a database does not always create it on disk immediately",
        mid="ae42",
        box_h=64,
    )


def d43_explicit_implicit() -> str:
    return compare2(
        ("Explicit", ['db.createCollection("products")', "When options or validation matter", "Visible before first insert"]),
        ("Implicit", ["First insertOne on a new name", "Collection appears with the write", "Fast for a simple test"]),
        title="Explicit vs. implicit collection creation",
        caption="Both talk to the same server",
        mid="ae43",
    )


def d44_insert_flow() -> str:
    return vdiag(
        [
            "insertOne()",
            "Server validates the request",
            "Generate _id if missing",
            "Store the document",
            "Return acknowledgment",
        ],
        title="First document insert flow",
        caption="Acknowledged + _id means the write was accepted",
        mid="ae44",
        box_h=50,
        gap=16,
    )


def d45_objectid() -> str:
    parts = [
        _label(460, 28, "Automatic _id generation", fs=18, fill=TEXT),
        _box(40, 60, 360, 120, "Document without _id", '{ name: "Aisha Khan" }', fs=18, sub_fs=14),
        _arrow(400, 120, 520, 120, "ae45"),
        _box(520, 60, 380, 120, "Stored document", "_id: ObjectId(\"…\")", fs=18, sub_fs=14),
        _label(460, 220, "MongoDB assigns a unique ObjectId when you omit _id", fs=15),
    ]
    return _svg(250, "\n".join(parts), "ae45")


def d46_write_read() -> str:
    return hdiag(
        ["Insert test\ndocument", "Acknowledgment", "Query document", "Confirm data"],
        title="Write-and-read verification",
        caption="A successful install is proven by both a write and a read",
        mid="ae46",
        h=88,
    )


def d47_validation_pipeline() -> str:
    return hdiag(
        ["Connect", "Ping", "Select DB", "Create\ncollection", "Insert", "Retrieve", "Validate"],
        title="Environment validation pipeline",
        caption="Skip a step and you only think the environment is ready",
        mid="ae47",
        h=88,
    )


def d48_training_structure() -> str:
    parts = [
        _label(460, 28, "training_store — this course’s sample database", fs=18, fill=TEXT),
        _box(260, 50, 400, 54, "training_store", header=True, fs=18),
        _box(20, 140, 210, 80, "environment_check", "Module 2 lab", fs=15, sub_fs=13),
        _box(246, 140, 210, 80, "customers", "Module 3+", fs=16, sub_fs=13),
        _box(472, 140, 210, 80, "products", "Module 3+", fs=16, sub_fs=13),
        _box(698, 140, 200, 80, "orders", "Module 3+", fs=16, sub_fs=13),
        _arrow(300, 104, 125, 140, "ae48"),
        _arrow(400, 104, 351, 140, "ae48"),
        _arrow(520, 104, 577, 140, "ae48"),
        _arrow(620, 104, 798, 140, "ae48"),
        _label(460, 250, "Module 2 creates environment_check; later modules load the catalog data", fs=15),
    ]
    return _svg(280, "\n".join(parts), "ae48")


def d49_same_data() -> str:
    parts = [
        _label(460, 28, "Same document through two clients", fs=18, fill=TEXT),
        _box(40, 56, 240, 80, "mongosh insert", fs=16),
        _arrow(280, 96, 340, 96, "ae49"),
        _box(342, 56, 236, 80, "MongoDB stores it", fs=16),
        _arrow(578, 96, 638, 96, "ae49"),
        _box(640, 56, 240, 80, "Compass displays it", fs=16),
        _label(460, 170, "If Compass cannot see the insert, you are on a different URI or database", fs=15),
    ]
    return _svg(200, "\n".join(parts), "ae49")


# --- 50–56 Security ---


def d50_auth_vs_authz() -> str:
    return compare2(
        ("Authentication", ["Who are you?", "Username + password", "Authentication database", "Success: identity known"]),
        ("Authorization", ["What may you do?", "Roles and privileges", "Per database / action", "Failure: unauthorized"]),
        title="Authentication vs. authorization",
        caption="You can log in and still be forbidden to run a command",
        mid="ae50",
    )


def d51_access_control() -> str:
    return hdiag(
        ["User credentials", "Authentication", "Assigned roles", "Permitted operations"],
        title="Basic access-control flow",
        caption="Least privilege: grant only the roles the training user needs",
        mid="ae51",
        h=80,
    )


def d52_user_roles() -> str:
    parts = [
        _label(460, 28, "Database user and role mapping", fs=18, fill=TEXT),
        _box(40, 60, 240, 90, "Database user", fs=18),
        _arrow(280, 105, 340, 105, "ae52"),
        _box(342, 50, 200, 50, "read", fs=16),
        _box(342, 108, 200, 50, "readWrite", fs=16),
        _box(342, 166, 200, 50, "admin roles", fs=16),
        _arrow(542, 75, 620, 75, "ae52"),
        _arrow(542, 133, 620, 133, "ae52"),
        _arrow(542, 191, 620, 191, "ae52"),
        _box(622, 50, 270, 50, "Find on permitted DB", fs=14),
        _box(622, 108, 270, 50, "Insert / update", fs=14),
        _box(622, 166, 270, 50, "Users, cluster, backup", fs=14),
    ]
    return _svg(250, "\n".join(parts), "ae52")


def d53_least_privilege() -> str:
    return compare2(
        ("Too much", ["Root on the whole server", "Production + training mixed", "Shared admin password"]),
        ("Training user", ["Role limited to training_store", "No cluster admin", "Unique password"]),
        title="Least-privilege access",
        caption="Classroom users should not hold unrestricted server access",
        mid="ae53",
    )


def d54_secret_flow() -> str:
    return vdiag(
        [
            "Application",
            ("Environment variable or secret store", "Not source code"),
            "MongoDB driver",
            "Encrypted database connection",
        ],
        title="Secure credential flow",
        caption="The URI is assembled at runtime from protected secrets",
        mid="ae54",
    )


def d55_antipattern() -> str:
    return compare2(
        ("Anti-pattern", ["Password in source", "URI in a screenshot", "Committed .env with secrets", "Shared in chat"]),
        ("Secure practice", ["Secret store / env var", "Placeholder in slides", ".gitignore secrets", "Rotate if exposed"]),
        title="Credential anti-pattern vs. secure practice",
        caption="If a password appears on a projector, rotate it after class",
        mid="ae55",
    )


def d56_layered_security() -> str:
    return vdiag(
        [
            "Network allowlist",
            "TLS",
            "Authentication",
            "Authorization",
            "Database access",
        ],
        title="Layered MongoDB connection security",
        caption="Fix the layer the error names — do not disable them all to “just connect”",
        mid="ae56",
        box_h=50,
        gap=16,
    )


# --- 57–65 Troubleshooting ---


def d57_troubleshoot_workflow() -> str:
    return hdiag(
        ["Error", "Service", "Host/port", "Network", "Auth", "Logs", "Retest"],
        title="Troubleshooting workflow",
        caption="Change one variable at a time, then retest",
        mid="ae57",
        h=78,
    )


def d58_conn_refused() -> str:
    parts = [
        _label(460, 28, "Connection refused (ECONNREFUSED)", fs=18, fill=TEXT),
        _box(40, 56, 240, 80, "Client request", fs=16),
        _arrow(280, 96, 400, 96, "ae58"),
        _box(340, 150, 240, 70, "Blocked", header=True, fs=18),
        _box(620, 40, 270, 54, "Server stopped", fs=15),
        _box(620, 102, 270, 54, "Wrong port", fs=15),
        _box(620, 164, 270, 54, "Not listening", fs=15),
        _label(460, 250, "First check: is mongod running, and is the URI port 27017?", fs=15),
    ]
    return _svg(280, "\n".join(parts), "ae58")


def d59_timeout() -> str:
    return vdiag(
        [
            "Client",
            "DNS / network / firewall / allowlist",
            "MongoDB server never reached",
        ],
        title="Connection timeout diagnosis",
        caption="Timeout is usually path or allowlist — not a typo in find()",
        mid="ae59",
        box_h=64,
    )


def d60_auth_fail() -> str:
    return vdiag(
        [
            "Credentials presented",
            "Username / password check",
            "Authentication database check",
            "Role verification (after login)",
        ],
        title="Authentication failure diagnosis",
        caption="Wrong user, password, or authSource — not DNS",
        mid="ae60",
    )


def d61_unauthorized() -> str:
    return vdiag(
        [
            "Successful login",
            "Operation requested",
            "Role insufficient",
            "Authorization error",
        ],
        title="Unauthorized operation diagnosis",
        caption="Authenticated ≠ authorized. Grant the missing role, or use the right database.",
        mid="ae61",
    )


def d62_startup_fail() -> str:
    return vdiag(
        [
            "Start request",
            "Configuration validation",
            "Data-directory permissions",
            "Port conflict",
            "Read the server log",
        ],
        title="MongoDB startup failure diagnosis",
        caption="mongosh cannot help until mongod is actually running",
        mid="ae62",
        box_h=50,
        gap=16,
    )


def d63_by_layer() -> str:
    return vdiag(
        [
            "Client",
            "URI",
            "DNS",
            "Network",
            "Server",
            "Authentication",
            "Authorization",
            "Database operation",
        ],
        title="Troubleshooting by system layer",
        caption="Name the layer before changing a second setting",
        mid="ae63",
        box_h=40,
        gap=12,
        w=500,
        x=210,
    )


def d64_error_tree() -> str:
    parts = [
        _label(460, 28, "Read the error, then branch", fs=18, fill=TEXT),
        _box(310, 46, 300, 48, "What did the client say?", header=True, fs=16),
        _box(16, 120, 170, 80, "Refused", "Start server / fix port", fs=14, sub_fs=12),
        _box(196, 120, 170, 80, "Timeout", "Firewall / allowlist", fs=14, sub_fs=12),
        _box(376, 120, 170, 80, "Auth failed", "User / password / auth DB", fs=13, sub_fs=11),
        _box(556, 120, 170, 80, "Unauthorized", "Grant role", fs=14, sub_fs=12),
        _box(736, 120, 168, 80, "Bad URI", "Syntax / encoding", fs=14, sub_fs=12),
        _arrow(400, 94, 101, 120, "ae64"),
        _arrow(430, 94, 281, 120, "ae64"),
        _arrow(460, 94, 461, 120, "ae64"),
        _arrow(490, 94, 641, 120, "ae64"),
        _arrow(520, 94, 820, 120, "ae64"),
        _label(460, 230, "Then retest with the simplest client: mongosh ping", fs=15),
    ]
    return _svg(255, "\n".join(parts), "ae64")


def d65_logs() -> str:
    parts = [
        _label(460, 28, "Logs as a diagnostic source", fs=18, fill=TEXT),
        _box(40, 56, 200, 64, "Startup", fs=16),
        _box(40, 130, 200, 64, "Connections", fs=16),
        _box(40, 204, 200, 64, "Auth failures", fs=16),
        _box(40, 278, 200, 64, "Config errors", fs=16),
        _arrow(240, 88, 360, 180, "ae65"),
        _arrow(240, 162, 360, 190, "ae65"),
        _arrow(240, 236, 360, 200, "ae65"),
        _arrow(240, 310, 360, 210, "ae65"),
        _box(362, 150, 500, 100, "Server log file", "Administrator investigates here first", fs=20, sub_fs=15),
        _label(612, 290, "No mongosh session required to read a startup failure", fs=14),
    ]
    return _svg(370, "\n".join(parts), "ae65")


# --- 66–70 Exercises ---


def d66_ex21_matrix() -> str:
    rows = [
        ("1 Offline learner", "option + risk"),
        ("2 Temp tests", "option + risk"),
        ("3 Distributed team", "option + risk"),
        ("4 Direct control", "option + risk"),
        ("5 Minimal ops", "option + risk"),
        ("6 Restricted net", "option + risk"),
    ]
    parts = [_label(460, 28, "Exercise 2.1 — map the scenario, then name the risk", fs=18, fill=TEXT)]
    for i, (sc, rec) in enumerate(rows):
        x = 24 + (i % 3) * 298
        y = 50 + (i // 3) * 100
        parts.append(_box(x, y, 280, 84, sc, rec, fs=16, sub_fs=14))
    parts.append(_label(460, 270, "Fill option + justification + main risk before the debrief", fs=15))
    return _svg(295, "\n".join(parts), "ae66")


def d67_ex22_unlabeled() -> str:
    return uri_bar(
        [
            ("?", "mongodb://", 0.16),
            ("?", "trainingUser", 0.18),
            ("?", "password", 0.16),
            ("?", "db.example.net", 0.22),
            ("?", "27017", 0.12),
            ("?", "training", 0.14),
        ],
        title="Exercise 2.2 — label each segment",
        caption="mongodb://trainingUser:password@db.example.net:27017/training",
        mid="ae67",
        unlabeled=True,
    )


def d68_ex23_checklist() -> str:
    return grid(
        [
            "Server / cluster",
            "mongosh",
            "Compass",
            "URI stored safely",
            "Authentication",
            "Network access",
            "Ping ok: 1",
            "Insert",
            "Retrieve",
        ],
        cols=3,
        title="Exercise 2.3 — environment readiness checklist",
        caption="Tick only what you observed. No passwords on the page.",
        mid="ae68",
        cell_h=64,
    )


def d69_ex24_failures() -> str:
    parts = [
        _label(460, 28, "Exercise 2.4 — four broken paths", fs=18, fill=TEXT),
        _box(20, 56, 210, 100, "Server path", "Stopped / wrong port", fs=16, sub_fs=14),
        _box(244, 56, 210, 100, "Network path", "Timeout / allowlist", fs=16, sub_fs=14),
        _box(468, 56, 210, 100, "Credential path", "Auth failed", fs=16, sub_fs=14),
        _box(692, 56, 208, 100, "Permission path", "Unauthorized", fs=16, sub_fs=14),
        _label(460, 190, "Name the layer first. Then one fix. Then retest.", fs=15),
    ]
    return _svg(220, "\n".join(parts), "ae69")


def d70_ex25_order() -> str:
    parts = [
        _label(460, 28, "Exercise 2.5 — put the setup steps in order", fs=18, fill=TEXT),
        _box(20, 56, 210, 70, "Ping the server", fs=15),
        _box(244, 56, 210, 70, "Insert a document", fs=15),
        _box(468, 56, 210, 70, "Choose a path", fs=15),
        _box(692, 56, 208, 70, "Open Compass", fs=15),
        _box(20, 140, 210, 70, "Install / provision", fs=15),
        _box(244, 140, 210, 70, "Retrieve the doc", fs=15),
        _box(468, 140, 210, 70, "Connect mongosh", fs=15),
        _box(692, 140, 208, 70, "Create collection", fs=15),
        _label(460, 240, "Lab guide sequence: choose → install → connect → ping → write → read → Compass", fs=14),
    ]
    return _svg(265, "\n".join(parts), "ae70")


# --- 71–76 Labs ---


def d71_lab21_paths() -> str:
    parts = [
        _label(460, 28, "Lab 2.1 — three provisioning paths", fs=18, fill=TEXT),
        _box(310, 50, 300, 50, "Assigned environment", header=True, fs=16),
        _box(20, 140, 280, 90, "Path A  Local", "Install Community Edition", fs=18, sub_fs=14),
        _box(320, 140, 280, 90, "Path B  Managed cloud", "User + network + URI", fs=16, sub_fs=14),
        _box(620, 140, 280, 90, "Path C  Instructor URI", "Connect only", fs=16, sub_fs=14),
        _arrow(400, 100, 160, 140, "ae71"),
        _arrow(460, 100, 460, 140, "ae71"),
        _arrow(520, 100, 760, 140, "ae71"),
        _label(460, 260, "Complete one path; later mongosh steps are shared", fs=15),
    ]
    return _svg(285, "\n".join(parts), "ae71")


def d72_lab22_shell() -> str:
    return hdiag(
        ["Open terminal", "Run mongosh", "Authenticate", "Ping", "List databases"],
        title="Lab 2.2 — shell connection workflow",
        caption="Success: prompt appears and ping contains ok: 1",
        mid="ae72",
        h=80,
    )


def d73_lab23_create() -> str:
    return hdiag(
        ["use training_store", "createCollection", "show collections"],
        title="Lab 2.3 — training database creation",
        caption="environment_check should appear; db prints training_store",
        mid="ae73",
        h=80,
    )


def d74_lab24_lifecycle() -> str:
    return hdiag(
        ["Create", "Insert", "Retrieve", "Update", "Verify"],
        title="Lab 2.4 — test document lifecycle",
        caption="insertOne → findOne → updateOne → findOne again",
        mid="ae74",
        h=78,
    )


def d75_lab25_complete() -> str:
    return grid(
        [
            ("MongoDB server", "Operational"),
            ("mongosh", "Connected"),
            ("Compass", "Same data"),
            ("training_store", "Visible"),
            ("environment_check", "Collection exists"),
            ("Test document", "Write + read"),
        ],
        cols=3,
        title="Lab 2.5 — complete environment validation",
        caption="Insert validation: COMPLETE when every required box is observed",
        mid="ae75",
        cell_h=80,
    )


def d76_challenge() -> str:
    return hdiag(
        ["New developer", "Parse URI", "Shell + ping", "Write / read", "Compass", "READY"],
        title="Practical challenge — new developer setup",
        caption="Prove reachability, auth, permissions, and both clients independently",
        mid="ae76",
        h=80,
    )


DIAGRAMS: dict[str, callable] = {
    "01-environment-overview.svg": d01_environment_overview,
    "02-deployment-options.svg": d02_deployment_options,
    "03-local-deployment.svg": d03_local_deployment,
    "04-managed-cloud-deployment.svg": d04_managed_cloud,
    "05-containerized-deployment.svg": d05_containerized,
    "06-self-managed-server.svg": d06_self_managed,
    "07-local-vs-managed-cloud.svg": d07_local_vs_cloud,
    "08-deployment-decision-flow.svg": d08_decision_flow,
    "09-installation-workflow.svg": d09_install_workflow,
    "10-server-and-client-tools.svg": d10_server_clients,
    "11-mongod-vs-mongosh.svg": d11_mongod_vs_mongosh,
    "12-client-connection-options.svg": d12_client_options,
    "13-environment-components.svg": d13_environment_components,
    "14-data-storage-structure.svg": d14_storage_structure,
    "15-file-system-components.svg": d15_filesystem,
    "16-configuration-map.svg": d16_config_map,
    "17-data-and-log-flow.svg": d17_data_log_flow,
    "18-local-installation-process.svg": d18_local_install,
    "19-managed-cloud-provisioning.svg": d19_cloud_provision,
    "20-container-setup-process.svg": d20_container_setup,
    "21-os-service-lifecycle.svg": d21_service_lifecycle,
    "22-startup-sequence.svg": d22_startup,
    "23-shutdown-sequence.svg": d23_shutdown,
    "24-environment-readiness-flow.svg": d24_readiness_flow,
    "25-basic-connection-flow.svg": d25_basic_connection,
    "26-localhost-connection.svg": d26_localhost,
    "27-remote-connection.svg": d27_remote,
    "28-managed-cloud-secure-connection.svg": d28_cloud_secure,
    "29-host-and-port-anatomy.svg": d29_host_port,
    "30-network-access-path.svg": d30_network_path,
    "31-connection-string-anatomy.svg": d31_uri_anatomy,
    "32-standard-mongodb-uri.svg": d32_standard_uri,
    "33-dns-seed-list-uri.svg": d33_srv_uri,
    "34-mongodb-vs-mongodb-srv.svg": d34_uri_vs_srv,
    "35-connection-establishment-sequence.svg": d35_establish_seq,
    "36-connecting-with-mongosh.svg": d36_connect_mongosh,
    "37-shell-command-flow.svg": d37_shell_command_flow,
    "38-connecting-with-compass.svg": d38_connect_compass,
    "39-compass-workspace.svg": d39_compass_workspace,
    "40-shell-vs-compass.svg": d40_shell_vs_compass,
    "41-application-driver-connection.svg": d41_driver,
    "42-creating-training-database.svg": d42_create_db,
    "43-explicit-vs-implicit-collection.svg": d43_explicit_implicit,
    "44-first-document-insert-flow.svg": d44_insert_flow,
    "45-automatic-id-generation.svg": d45_objectid,
    "46-write-and-read-verification.svg": d46_write_read,
    "47-environment-validation-pipeline.svg": d47_validation_pipeline,
    "48-training-database-structure.svg": d48_training_structure,
    "49-same-data-two-clients.svg": d49_same_data,
    "50-authentication-vs-authorization.svg": d50_auth_vs_authz,
    "51-access-control-flow.svg": d51_access_control,
    "52-user-and-role-mapping.svg": d52_user_roles,
    "53-least-privilege-access.svg": d53_least_privilege,
    "54-secure-credential-flow.svg": d54_secret_flow,
    "55-credential-antipattern-vs-secure.svg": d55_antipattern,
    "56-layered-connection-security.svg": d56_layered_security,
    "57-troubleshooting-workflow.svg": d57_troubleshoot_workflow,
    "58-connection-refused-diagnosis.svg": d58_conn_refused,
    "59-connection-timeout-diagnosis.svg": d59_timeout,
    "60-authentication-failure-diagnosis.svg": d60_auth_fail,
    "61-unauthorized-operation-diagnosis.svg": d61_unauthorized,
    "62-startup-failure-diagnosis.svg": d62_startup_fail,
    "63-troubleshooting-by-layer.svg": d63_by_layer,
    "64-common-error-decision-tree.svg": d64_error_tree,
    "65-logs-as-diagnostic-source.svg": d65_logs,
    "66-ex-2-1-deployment-selection-matrix.svg": d66_ex21_matrix,
    "67-ex-2-2-connection-string-labeling.svg": d67_ex22_unlabeled,
    "68-ex-2-3-readiness-checklist.svg": d68_ex23_checklist,
    "69-ex-2-4-connection-failure-scenarios.svg": d69_ex24_failures,
    "70-ex-2-5-setup-steps-in-order.svg": d70_ex25_order,
    "71-lab-2-1-install-provision-paths.svg": d71_lab21_paths,
    "72-lab-2-2-shell-connection-workflow.svg": d72_lab22_shell,
    "73-lab-2-3-training-database-creation.svg": d73_lab23_create,
    "74-lab-2-4-test-document-lifecycle.svg": d74_lab24_lifecycle,
    "75-lab-2-5-complete-validation.svg": d75_lab25_complete,
    "76-practical-challenge-new-developer.svg": d76_challenge,
}


def write_all() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    keep = set(DIAGRAMS)
    for old in ASSETS.glob("*.svg"):
        if old.name not in keep:
            old.unlink()
            print(f"Removed stale {old.name}")
    for name, fn in DIAGRAMS.items():
        path = ASSETS / name
        path.write_text(fn(), encoding="utf-8")
        print(f"Wrote {path.relative_to(ASSETS.parent.parent.parent)}")
    return len(DIAGRAMS)


if __name__ == "__main__":
    n = write_all()
    print(f"Done. {n} diagrams.")

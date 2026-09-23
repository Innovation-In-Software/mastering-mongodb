"""Emit Module 7 Marp slides and append them to the course deck.

Run after lab guides and diagrams exist:

    python scripts/module07_diagrams.py
    python scripts/module07_labs.py
    python scripts/module07_slides.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from course_config import deck_md
from module07_labs import OUT as LAB_DIR

DECK = deck_md()
MARKER = "<!-- _header: 'Module 7 — Introduction to Replication and Sharding' -->"
NEXT_MARKERS = (
    "<!-- _header: 'Module 8 — Best Practices' -->",
    "<!-- _header: 'Module 8 — MongoDB Best Practices, Security, and Troubleshooting' -->",
)


def notes(title: str, script: str) -> str:
    body = script.strip()
    return f"<!--\n{body}\n\nThe slide title is: {title}.\n-->"


def split_slide(title: str, bullets: list[str], img: str, alt: str, script: str, *, fit: str = "") -> str:
    cls = f"split {fit}".strip()
    items = "\n".join(f"- {b}" for b in bullets)
    return f"""<!-- _class: {cls} -->

# {title}

<div class="cols">
<div class="col-text">

{items}

</div>
<div class="col-visual">

<img src="assets/module-07/{img}" alt="{alt}" width="720">

</div>
</div>

{notes(title, script)}
"""


def content_slide(title: str, body: str, script: str, *, fit: str = "fit-md") -> str:
    return f"""<!-- _class: content {fit} -->

# {title}

{body.strip()}

{notes(title, script)}
"""


def lead_slide(title: str, subtitle: str, script: str) -> str:
    return f"""<!-- _class: lead -->

# {title}

{subtitle}

{notes(title, script)}
"""


def parse_steps(prefix: str, num: int) -> list[tuple[str, str, str]]:
    matches = sorted(LAB_DIR.glob(f"{prefix}-7.{num}-*.md"))
    if not matches:
        return []
    text = matches[0].read_text(encoding="utf-8")
    start = text.find("## Steps from the training slides")
    if start < 0:
        return []
    section = text[start:]
    end = re.search(r"\n## (?!Steps)", section[10:])
    if end:
        section = section[: end.start() + 10]
    steps = []
    for m in re.finditer(
        r"### Step (\d+) — (.+?)\n\n\*\*Do this:\*\* (.*?)\n\n\*\*Expected result:\*\* (.*?)(?=\n---|\n### |\Z)",
        section,
        re.DOTALL,
    ):
        do = re.sub(r"\s+", " ", m.group(3)).strip()[:220]
        exp = re.sub(r"\s+", " ", m.group(4)).strip()[:160]
        steps.append((m.group(2).strip(), do, exp))
    return steps


def activity_block(
    kind: str,
    num: int,
    title: str,
    time: str,
    objective: str,
    img: str,
    alt: str,
    script: str,
) -> list[str]:
    prefix = "exercise" if kind == "exercise" else "lab"
    label = "Exercise" if kind == "exercise" else "Lab"
    lab = next(LAB_DIR.glob(f"{prefix}-7.{num}-*.md"))
    rel = lab.as_posix().split("slide-exercises/")[-1]
    heading_intro = f"{label} 7.{num} — {title}"
    intro = split_slide(
        heading_intro,
        [
            f"**Time:** {time}",
            objective,
            f"**Lab guide:** [`{label} 7.{num}`](../slide-exercises/{rel})",
        ],
        img,
        alt,
        script,
        fit="fit-md",
    )
    slides = [intro]
    steps = parse_steps(prefix, num)
    for i in range(0, len(steps), 2):
        pair = steps[i : i + 2]
        if len(pair) == 2:
            heading = f"## {label} 7.{num} — Steps {i + 1}–{i + 2}"
        else:
            heading = f"## {label} 7.{num} — Step {i + 1}"
        lines = ["<!-- _class: fit-md -->", "", heading, ""]
        if i == 0:
            lines.extend([f"**Lab guide:** [`{label} 7.{num}`](../slide-exercises/{rel})", ""])
        lines.extend(["**Follow along (Windows) — key steps:**", ""])
        for n, (st, do, exp) in enumerate(pair, start=i + 1):
            do_clean = do.replace("```javascript", "`").replace("```", "`").strip()
            lines += [
                f"**Step {n} — {st}**",
                f"- **Do:** {do_clean}",
                f"- **Expected:** {exp}",
                "",
            ]
        lines.append(
            notes(
                heading[3:],
                f"Time-box this pair of steps. Open the lab guide for full commands.\nInstructor script: {script[:220]}",
            )
        )
        slides.append("\n".join(lines))
    return slides


def build_slides() -> str:
    s: list[str] = []

    s.append(f"""{MARKER}

<!-- _class: lead -->

# Introduction to Replication and Sharding

Replication keeps data available. Sharding distributes data and work.

{notes("Introduction to Replication and Sharding", '''Day 3 after indexing. Start from business need: stay up versus grow. Replica sets copy; shards partition. Production usually does both.

Pacing for 3–3.5 hours: all concept slides, Demos 7.1, 7.3, 7.7, 7.8, Exercises 7.1, 7.5, 7.8, 7.9, Lab 7.1, and the practical challenge. Remaining demos, exercises, and labs are on-demand or homework.

Ask who has only used a single mongod. Atlas users already have a replica set even if they never thought about elections.
''')}
""")

    s.append(
        split_slide(
            "Module Learning Objectives",
            [
                "Distinguish availability from scalability",
                "Explain replica-set roles, oplog, and failover",
                "Select basic read and write settings",
                "Describe sharded-cluster components",
                "Evaluate shard keys and query routing",
                "Decide when to replicate, shard, or both",
            ],
            "007-deployment-decision-tree.svg",
            "Replication, guarantees, and scale map",
            "Read outcomes. The through-line is copy for failover, partition for growth, then measure before you shard.",
        )
    )

    s.append(
        content_slide(
            "Instructor pacing (3–3.5 hours)",
            """**Required in class**

- Concept slides through the decision framework
- Demos 7.1, 7.3, 7.7, 7.8
- Exercises 7.1, 7.5, 7.8, 7.9
- Lab 7.1 (Atlas replica set) and the practical challenge

**If time remains:** Demo 7.2, Exercise 7.12, Lab 7.6

**Homework / extra lab block:** remaining exercises, Labs 7.2–7.10

Failover and sharding commands run only on instructor-controlled disposable infrastructure.""",
            "Put this on the wall. Do not attempt every lab live. Atlas M0 is a replica set, not a sharded cluster.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Availability and Scalability Requirements",
            [
                "Remain available during server failure",
                "Recover from infrastructure problems",
                "Handle growing data and request volume",
                "Serve users in multiple locations",
                "Meet durability and latency objectives",
                "Start from business requirements, not hardware",
            ],
            "008-requirements-map.svg",
            "Business needs mapped to availability and scale",
            "Collect their actual pains: weekend outages, catalog growth, regional users. Architecture follows the need.",
        )
    )

    s.append(
        split_slide(
            "High Availability vs. Horizontal Scalability",
            [
                "**High availability:** service stays accessible during component failure",
                "MongoDB mechanism: **replica sets**",
                "**Horizontal scalability:** spread data and workload",
                "MongoDB mechanism: **sharding**",
                "Need both: **sharded replica sets**",
            ],
            "002-ha-vs-horizontal-scale.svg",
            "Replica sets for HA, sharding for scale",
            "Redundancy is not extra capacity. Three copies of 500 GB is still 500 GB of data, plus overhead.",
        )
    )

    s.append(
        content_slide(
            "Requirement to mechanism",
            """| Requirement | Main mechanism |
| --- | --- |
| Server redundancy | Replication |
| Automatic failover | Replication |
| More storage capacity | Sharding |
| More distributed throughput | Sharding |
| Availability and scale | Sharded replica sets |""",
            "Leave this table up while they do Exercise 7.1 later. Neither yet is a valid answer for local learning.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Vertical Scaling vs. Horizontal Scaling",
            [
                "**Vertical:** more CPU, RAM, disk, faster storage on one server",
                "Usually simpler — until the box or the bill stops you",
                "**Horizontal:** more servers, distributed work",
                "Broader growth, more operational complexity",
                "Indexing and schema work come before sharding",
            ],
            "003-vertical-vs-horizontal.svg",
            "Bigger box versus more boxes",
            "Remind them of Module 6: a missing index is not a sharding problem. Buy a bigger box or add indexes before you invent a shard key.",
        )
    )

    s.append(
        split_slide(
            "Replication vs. Sharding",
            [
                "Replication **copies** the same logical dataset",
                "Sharding **partitions** data across shards",
                "Replica set: primary + secondaries, failover",
                "Sharded cluster: multiple shards, distributed traffic",
                "Production shards are normally replica sets",
            ],
            "004-replication-vs-sharding.svg",
            "Copy versus partition",
            "Say it twice: sharding does not replace backups. Replication does not replace backups either.",
        )
    )

    s.append(
        split_slide(
            "MongoDB Distributed Architecture Overview",
            [
                "Application → driver → query router",
                "Router sends work to the right shard",
                "Each shard is typically a replica set",
                "Config servers hold cluster metadata",
                "Distributed data, distributed work, local redundancy",
            ],
            "001-distributed-architecture.svg",
            "App, mongos, three sharded replica sets",
            "This is the north-star picture. The rest of the module zooms into replica sets first, then the router and keys.",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            1,
            "Replication or Sharding?",
            "10 min",
            "Choose replication, sharding, both, or neither yet for six requirements.",
            "239-ex-7-1-replication-or-sharding.svg",
            "Four choice buckets",
            "Ten minutes. Reveal answers: survive failure and elect = replication; capacity and write spread = sharding; local dev = neither yet; production availability and scale = both.",
        )
    )

    s.append(
        split_slide(
            "What Is a Replica Set?",
            [
                "A group of `mongod` processes with the same dataset",
                "Common shape: one primary, two or more secondaries",
                "Odd number of voting members where practical",
                "Provides redundancy, election, failover, maintenance windows",
            ],
            "009-replica-set-overview.svg",
            "Primary and two secondaries",
            "Atlas free tier is already a replica set. Students who only used Compass on Atlas have been talking to a primary the whole course.",
        )
    )

    s.append(
        split_slide(
            "Three-Member Replica Set",
            [
                "Primary, Secondary 1, Secondary 2",
                "Replication copies data from the primary",
                "Heartbeats keep members informed of health",
                "Any two voting members form a majority",
            ],
            "010-three-member-replica-set.svg",
            "Primary and two secondaries with replication and heartbeats",
            "This is the classroom default. Draw the triangle: writes to primary, copies to secondaries, heartbeats on every edge.",
        )
    )

    s.append(
        split_slide(
            "Replica-Set Connection String",
            [
                "Connect to the **set**, not one fixed host",
                "Driver discovers members and follows the primary",
                "A one-host URI is an anti-pattern in production",
            ],
            "016-replica-set-connection-string.svg",
            "Application connecting through several replica-set hosts",
            "Their Atlas URI already lists replicaSet=. Point at it. Demo 7.1 can show db.hello() topology.",
        )
    )

    s.append(
        split_slide(
            "Replica-Set Members",
            [
                "Primary, secondary, hidden, delayed",
                "Non-voting members and (rarely) arbiters",
                "Not every member must serve application reads",
                "Roles are configuration, not personality",
            ],
            "012-member-roles.svg",
            "Member roles table",
            "Hidden and delayed still consume hardware. They are not free insurance.",
        )
    )

    s.append(
        split_slide(
            "Primary Member Responsibilities",
            [
                "Accepts application writes",
                "Applies writes and records the oplog",
                "Participates in elections",
                "Serves reads under `primary` read preference",
                "Only one primary at a time in the set",
            ],
            "013-primary-responsibilities.svg",
            "Primary write and oplog path",
            "If two primaries ever accepted conflicting writes, you have a split-brain story. Majority voting exists to prevent that.",
        )
    )

    s.append(
        split_slide(
            "Secondary Member Responsibilities",
            [
                "Maintains a copy of the data",
                "Copies and applies oplog operations in order",
                "Eligible secondaries can become primary",
                "May serve reads when read preference allows",
                "An active participant, not a tape backup",
            ],
            "014-secondary-responsibilities.svg",
            "Copy, apply, maybe elect",
            "Secondaries apply the same operations, not rsync of random files. Order matters.",
        )
    )

    s.append(
        split_slide(
            "The Replication Oplog",
            [
                "A capped collection of data-changing operations",
                "Primary writes an entry after applying the change",
                "Secondaries copy entries and apply them",
                "The oplog window must cover how long a member can be down",
            ],
            "019-the-oplog.svg",
            "Write, oplog, copy, apply",
            "If a member is down longer than the oplog window, it may need an initial sync. Size the oplog for real maintenance, not for a coffee break.",
        )
    )

    s.append(
        split_slide(
            "Oplog Window",
            [
                "Oldest available oplog entry through the newest",
                "A secondary down longer than the window cannot catch up incrementally",
                "Then: initial sync, not oplog replay",
            ],
            "026-oplog-window.svg",
            "Oldest through newest oplog entries",
            "Ask how long their longest planned maintenance is. That is the oplog-sizing question.",
        )
    )

    s.append(
        split_slide(
            "Data Replication vs. Heartbeats",
            [
                "Oplog copies application changes",
                "Heartbeats carry health and state",
                "Do not draw them as one arrow",
            ],
            "029-data-vs-heartbeats.svg",
            "Oplog traffic distinguished from health monitoring",
            "Exercise 7.2 fails if they merge these flows.",
        )
    )

    s.append(
        split_slide(
            "Replication Data Flow",
            [
                "Driver discovers the current primary",
                "Application write → primary apply → oplog",
                "Secondaries retrieve and apply",
                "Client acknowledgment follows **write concern**",
            ],
            "020-replicated-write-flow.svg",
            "Driver, primary, secondaries, ack",
            "Walk this with a finger. Pause on ack: w:1 can return before secondaries have the write.",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            2,
            "Label a Replica-Set Architecture",
            "10 min",
            "Label application, driver, members, oplog, heartbeats, and read/write paths.",
            "240-ex-7-2-label-replica-set.svg",
            "Replica-set diagram to label",
            "Watch for people drawing writes to a secondary. Heartbeats are not oplog.",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            3,
            "Trace a Replicated Write",
            "15 min",
            "Sequence a write from the client through oplog apply and write-concern ack.",
            "241-ex-7-3-trace-write.svg",
            "Write path to sequence",
            "If they put acknowledgment before secondary apply, ask which write concern they assumed.",
        )
    )

    s.append(
        split_slide(
            "Replica-Set Heartbeats",
            [
                "Members exchange regular health information",
                "Who is reachable, who is primary, who may vote",
                "Whether an election may be required",
                "Heartbeats do **not** copy application data",
            ],
            "030-heartbeats.svg",
            "Health checks among members",
            "Separate the control plane (heartbeats) from the data plane (oplog). People mix them.",
        )
    )

    s.append(
        split_slide(
            "Replica-Set Elections",
            [
                "Primary unavailable or steps down",
                "Network or config changes that affect majority",
                "A better eligible candidate (priority)",
                "Eligible voting members choose a new primary",
            ],
            "033-election-flow.svg",
            "Election triggers",
            "Elections are normal. Panic is optional. Applications must tolerate a short write pause.",
        )
    )

    s.append(
        split_slide(
            "Automatic Failover",
            [
                "Failure detected → election → new primary",
                "Writes may pause during the election",
                "Some reads may be affected",
                "Drivers rediscover topology; retries help",
            ],
            "034-failover-timeline.svg",
            "Failover sequence",
            "Demo 7.3 will show this. Set expectations: a few seconds of errors is success, not a broken database.",
        )
    )

    s.append(
        split_slide(
            "Application Behavior During Failover",
            [
                "Use a replica-set connection string",
                "Use a supported driver and sensible timeouts",
                "Retry eligible operations; handle transients",
                "Do not pin forever to one hostname",
                "Make critical writes idempotent",
            ],
            "036-app-behavior-during-failover.svg",
            "Application requirements during failover",
            "Database HA does not cancel application design. A script that connects to localhost:27017 only will miss the new primary.",
        )
    )

    s.append(
        split_slide(
            "Majority and Voting Concepts",
            [
                "Need a voting majority to elect and keep a primary",
                "Three voters: two are a majority",
                "One isolated member cannot elect itself",
                "Partitions follow the majority side — avoids two primaries",
            ],
            "039-three-member-majority.svg",
            "Two of three form a majority",
            "Draw a network split. The lonely primary steps down. That is a feature.",
        )
    )

    s.append(
        split_slide(
            "Network Partition and Majority Protection",
            [
                "Majority side can elect or keep a primary",
                "Minority side cannot accept writes",
                "This prevents two writable primaries",
            ],
            "041-network-partition-majority.svg",
            "Majority side writable; minority cannot elect",
            "Essential diagram. HA does not mean writable during a split.",
        )
    )

    s.append(
        split_slide(
            "Split-Brain Prevention",
            [
                "Two writable primaries would fork the dataset",
                "Voting rules allow only one majority primary",
                "Consistency over “always writable”",
            ],
            "042-split-brain-prevention.svg",
            "Voting rules preventing two writable primaries",
            "Tie back to majority write concern for what the client was promised.",
        )
    )

    s.append(
        split_slide(
            "Replica-Set Member Priorities",
            [
                "Priority influences who becomes primary",
                "Prefer a member in the primary data center",
                "Keep a reporting node from becoming primary",
                "Not a performance router for ordinary reads",
            ],
            "047-member-priority.svg",
            "Priority versus priority 0",
            "Priority 0 means cannot be primary. Hidden reporting nodes often use this. Reads still need read preference, not priority.",
        )
    )

    s.append(
        split_slide(
            "Arbiter Overview and Limitations",
            [
                "Votes in elections; stores **no** application data",
                "Cannot become primary; adds no copy and no read capacity",
                "Use only after understanding durability and security tradeoffs",
                "A data-bearing voter is usually more valuable",
            ],
            "054-arbiter-role.svg",
            "Arbiter cannot store data",
            "PSA (primary-secondary-arbiter) is a common cost shortcut with majority-write pain. Do not sell it as three copies.",
        )
    )

    s.append(
        split_slide(
            "Hidden Members",
            [
                "Full data copy, hidden from normal application reads",
                "Dedicated backup or reporting arrangements",
                "Can be blocked from becoming primary",
                "Hidden ≠ disconnected or unprotected",
            ],
            "049-hidden-secondary.svg",
            "Hidden member still has data",
            "Drivers with default read preference will not send app reads there. You still back it up and patch it.",
        )
    )

    s.append(
        split_slide(
            "Delayed Members",
            [
                "Applies operations after a configured delay",
                "Can help recover from some accidental changes",
                "Not a substitute for backups; intentionally stale",
                "Needs oplog history; must not become primary by accident",
            ],
            "051-delayed-secondary.svg",
            "Delayed apply behind the primary",
            "A delayed member that becomes primary is a disaster. Priority 0 and votes carefully. Still take backups.",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            4,
            "Sequence a Failover",
            "15 min",
            "Arrange detection, election, driver discovery, and application retry.",
            "242-ex-7-4-sequence-failover.svg",
            "Failover sequence to order",
            "If they put retry before election, the write has nowhere to go yet.",
        )
    )

    s.append(
        split_slide(
            "Demo 7.1 — Inspect a Replica Set",
            [
                "**15 min** · instructor-controlled cluster or Atlas",
                "`rs.status()` — name, states, health, optimes",
                "`rs.conf()` — votes and priorities",
                "Identify primary and secondaries together",
            ],
            "092-rs-status-concept-map.svg",
            "rs.status and rs.conf",
            "Project the live output. Circle setName, members[].stateStr, health, optimeDate. Then open rs.conf for votes.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Demo 7.2 — Observe Replication",
            [
                "**15 min** · disposable training infrastructure",
                "Insert on the primary; confirm the write",
                "Inspect a secondary **safely**",
                "Confirm the document after replication",
                "Discuss staleness if you read too soon",
            ],
            "252-lab-7-2-replication-verification.svg",
            "Insert, oplog, secondary copy, verify",
            "One insert is enough. Use a documented read preference or an instructor secondary shell.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Demo 7.3 — Simulate Primary Failover",
            [
                "**20 min** · **disposable** replica set only",
                "Record primary → `rs.stepDown()`",
                "Watch the election; identify the new primary",
                "Note application retry; restore as secondary",
                "Never step down a shared classroom Atlas cluster",
            ],
            "253-lab-7-3-failover-observation.svg",
            "Step-down, election, new primary",
            "Narrate the error window as expected. Restore before the break.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Read Preferences",
            [
                "`primary` · `primaryPreferred` · `secondary`",
                "`secondaryPreferred` · `nearest`",
                "Affects availability, latency, freshness, load",
                "Does not replace read concern",
            ],
            "057-read-preference-overview.svg",
            "Read preference modes",
            "Default for most drivers is primary. Changing this is an application decision, not a server-wide magic switch.",
        )
    )

    s.append(
        split_slide(
            "Primary Read Preference",
            [
                "`primary` sends reads to the current primary",
                "Sees the primary’s current state — simplest consistency story",
                "Default for many workloads",
                "Reads share primary resources with writes",
                "Reads can pause briefly during elections",
            ],
            "058-primary-read-preference.svg",
            "Reads routed to the current primary",
            "Order-status right after pay: stay on primary unless they can explain stale as acceptable.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Secondary Read Preferences",
            [
                "May help reporting, geo-local reads, or shedding primary read load",
                "Data may be behind the primary",
                "Stale results can be wrong for the business",
                "Secondary capacity is not free",
                "Not an automatic system-wide speedup",
            ],
            "063-primary-vs-secondary-reads.svg",
            "Fresher primary state versus potentially stale secondary",
            "If analytics saturates a secondary, lag grows and failover readiness drops.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Write Concern",
            [
                "How many members must acknowledge a write?",
                "Number of acks, majority, journal, timeout",
                "Controls durability confidence vs latency",
                "Not the same question as read preference",
            ],
            "069-write-concern-overview.svg",
            "Primary, majority, numeric w",
            "Write concern is the client’s success definition. Show wtimeout so they do not hang forever.",
        )
    )

    s.append(
        split_slide(
            "Common Write-Concern Levels",
            [
                "**`w: 1`:** primary ack — faster, less confirmation",
                "**majority:** voting data-bearing majority",
                "**`w: N`:** wait for N members",
                "Stronger ack usually costs latency",
                "Do not treat `w: 1` as a universal performance solution",
            ],
            "074-write-concern-latency.svg",
            "Faster acknowledgment versus stronger confirmation",
            "For payments, majority is the teaching default.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Majority Write Concern",
            [
                "Acknowledged after the required voting majority confirms",
                "Teaching default for payments and other durable records",
                "Protects against rollback if the original primary never returns",
                "Costs more latency than `w: 1`",
            ],
            "076-payment-majority-write.svg",
            "Payment flowing through primary and replicas before success",
            "Walk the payment: client waits until majority of data-bearing voters have the write. That is the durability story.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Read Concern",
            [
                "Visibility and isolation of the read",
                "`local` · `available` · `majority` · `linearizable` · `snapshot`",
                "Not the same knob as read preference",
                "Pair majority reads with majority writes when “read what I just wrote” matters",
                "Exact guarantees depend on version and topology",
            ],
            "066-read-concern-overview.svg",
            "Read-concern visibility models",
            "Teach the idea. Confirm docs for production.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Read Preference, Read Concern, and Write Concern",
            [
                "**Read preference:** which member may serve the read?",
                "**Read concern:** what visibility guarantee?",
                "**Write concern:** what acknowledgment for a write?",
                "Three knobs. Not interchangeable.",
            ],
            "077-three-settings.svg",
            "Three settings, three questions",
            "Quiz them live: secondary + local read is a freshness choice. Majority write is a durability choice. Mixing the words is the most common muddle.",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            5,
            "Select Read and Write Settings",
            "20 min",
            "Choose settings for payment, catalog, reporting, and reconciliation; justify staleness and durability.",
            "243-ex-7-5-select-settings.svg",
            "Three settings for business ops",
            "Push back if payment confirmation is secondaryPreferred. Analytics may be stale on purpose.",
        )
    )

    s.append(
        split_slide(
            "Demo 7.4 — Compare Write Concerns",
            [
                "**15 min** · controlled environment",
                "Same insert, different acknowledgment requirements",
                "Discuss latency, confirmation, `wtimeout`, durability",
                "Avoid “just use `w: 1` to go faster”",
            ],
            "254-lab-7-4-read-write-policy.svg",
            "Write-concern comparison",
            "If times are similar on an idle three-node Atlas set, say so. The lesson is the contract, not a benchmark.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Demo 7.5 — Compare Read Preferences",
            [
                "**15 min**",
                "Compare `primary`, `primaryPreferred`, `secondaryPreferred`, `nearest`",
                "Observe which member is selected; discuss freshness",
                "`nearest` is latency, not a geographic data guarantee",
            ],
            "057-read-preference-overview.svg",
            "Read preference options",
            "Show db.hello() / connection handshake. nearest can still be the primary if it is closest.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Replication Lag",
            [
                "Delay between apply on primary and apply on a secondary",
                "Affects secondary-read freshness",
                "Affects failover readiness",
                "Affects recovery and oplog-window planning",
            ],
            "078-replication-lag-overview.svg",
            "Primary T0 versus secondary T0 plus lag",
            "A few seconds idle is normal. Growing lag is an incident. Zero lag is not a promise under load.",
        )
    )

    s.append(
        split_slide(
            "Causes of Replication Lag",
            [
                "Slow disks, network, insufficient CPU",
                "Heavy writes or large operations",
                "Secondary-specific reporting load",
                "Oplog window too small for downtime",
                "Lag is a symptom — collect evidence before rebuild",
            ],
            "080-causes-of-lag.svg",
            "Disk, CPU, network, writes, and reporting load",
            "Reporting on a secondary is a classic self-inflicted lag.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Rollback Concepts",
            [
                "Former primary has writes not on the new authoritative history",
                "MongoDB reconciles that member with the current primary",
                "Reduce risk: majority writes, stable networks, correct drivers",
                "Rollback is not “the database randomly deletes orders for fun”",
            ],
            "086-rollback-concept.svg",
            "Former primary versus current history",
            "w:1 + failover is the story. Majority writes that completed are the ones you designed to keep.",
        )
    )

    s.append(
        split_slide(
            "Replication Is Not Backup",
            [
                "A drop or bad update replicates to every member",
                "Availability copies are not a restore point",
                "Delayed members help only some accidents",
                "Keep independent backups",
            ],
            "089-replication-is-not-backup.svg",
            "Accidental deletion copied to every replica",
            "Essential diagram. If they remember one ops sentence: replica set plus backups.",
        )
    )

    s.append(
        split_slide(
            "Replica Set Plus Backup Strategy",
            [
                "Replica set: stay up when a node dies",
                "Backup: restore yesterday’s data",
                "You need both in production",
            ],
            "090-replica-set-plus-backup.svg",
            "Availability copies combined with independent backups",
            "Sharding does not replace this picture either.",
        )
    )

    s.append(
        split_slide(
            "Replica-Set Status and Health",
            [
                "`rs.status()` — states, health, optimes, elections",
                "`rs.conf()` — topology and votes",
                "`rs.printSecondaryReplicationInfo()` — lag",
                "Presentation depends on environment and privileges",
            ],
            "092-rs-status-concept-map.svg",
            "Status commands",
            "Lab 7.1 is this slide in the shell. Atlas UI is allowed as a complement, not a replacement for rs.status().",
        )
    )

    s.append(
        split_slide(
            "Replica-Set Operational Practices",
            [
                "Odd number of voting members where practical",
                "Independent failure domains",
                "Monitor lag and oplog window",
                "Replica-set URIs, failover tests, backups",
                "Secure member and client traffic",
            ],
            "100-replica-set-ops-checklist.svg",
            "Topology, health, lag, oplog, backups, failover tests",
            "Backups still required. Replication is HA, not a backup product.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Replica-Set Failure Scenarios",
            [
                "**One secondary down:** primary usually stays writable; repair soon",
                "**Primary down, majority up:** election; brief write pause",
                "**Majority unavailable:** no writable primary — consistency wins",
                "Administrator intervention may be required in the last case",
            ],
            "094-one-secondary-failure.svg",
            "Three failure outcomes",
            "Losing majority is designed to stop writes. That surprises people who wanted HA to mean 'always writable even if the network is in pieces.'",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            6,
            "Diagnose Replication Lag",
            "15 min",
            "Match lag symptoms to cause, impact, evidence, and first action.",
            "244-ex-7-6-diagnose-lag.svg",
            "Lag diagnosis",
            "If every answer is 'restart MongoDB,' send them back to metrics.",
        )
    )

    s.append(
        split_slide(
            "Demo 7.6 — Inspect Replication Lag",
            [
                "**10 min**",
                "Compare member replication times",
                "Normal small delay vs continuously growing lag",
                "Tie to disk, network, write bursts, secondary load",
            ],
            "078-replication-lag-overview.svg",
            "Primary timestamp versus secondary apply times",
            "Show printSecondaryReplicationInfo. If lag is zero, still describe what 45 seconds would mean for secondary reads.",
            fit="fit-md",
        )
    )

    s.extend(
        activity_block(
            "lab",
            1,
            "Verify Replica-Set Health",
            "20 min",
            "Inspect name, states, votes, and timestamps; write a health report.",
            "251-lab-7-1-health-inspection.svg",
            "Health inspection flow",
            "Required lab on Atlas. Walk the room for standalone users and switch their URI.",
        )
    )

    s.extend(
        activity_block(
            "lab",
            2,
            "Write and Verify Replication",
            "20 min",
            "Insert through the replica-set URI, confirm ack, observe replication, delete the probe.",
            "252-lab-7-2-replication-verification.svg",
            "Insert and replicate",
            "Optional if time is short. Must use replica-set URI. Delete the lab documents.",
        )
    )

    s.extend(
        activity_block(
            "lab",
            3,
            "Observe Election and Failover",
            "25 min",
            "Watch a controlled step-down on a disposable set; document old/new primary and app behavior.",
            "253-lab-7-3-failover-observation.svg",
            "Election lab",
            "Instructor-led. Students observe and record. Do not let twelve people stepDown one Atlas cluster.",
        )
    )

    s.extend(
        activity_block(
            "lab",
            4,
            "Test Read Preference and Write Concern",
            "25 min",
            "Compare serving members and assigned write concerns; map them to business operations.",
            "254-lab-7-4-read-write-policy.svg",
            "Read and write concern lab",
            "Optional / extra block. SecondaryPreferred needs instructor permission on shared clusters.",
        )
    )

    s.extend(
        activity_block(
            "lab",
            5,
            "Investigate Replication Lag",
            "20 min",
            "Compare optimes and oplog window; propose ordered corrective actions.",
            "255-lab-7-5-lag-investigation.svg",
            "Lag investigation lab",
            "Even with zero lag, they must write a production checklist.",
        )
    )

    s.append(
        split_slide(
            "What Is Sharding?",
            [
                "Partitions a collection across multiple shards",
                "Each shard stores only part of the sharded dataset",
                "Supports storage, query, and write scale",
                "Adds significant operational complexity",
            ],
            "103-logical-vs-physical.svg",
            "Three shards holding ranges",
            "Sharding is not the default for training_store. Seventeen orders do not need three shards.",
        )
    )

    s.append(
        split_slide(
            "Why Applications Need Sharding",
            [
                "Dataset or throughput beyond one replica set",
                "Working set no longer fits",
                "Geographic placement required",
                "Vertical scaling no longer sustainable",
                "Shard to a measured need, not a conference slide",
            ],
            "208-capacity-growth-timeline.svg",
            "Development to replica set to sharded production",
            "Ask what evidence they have: disk, CPU, working set, write latency.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Sharded-Cluster Components",
            [
                "Shards (data)",
                "Config server replica set (metadata)",
                "One or more `mongos` routers",
                "Client applications and drivers",
            ],
            "101-sharded-cluster-overview.svg",
            "mongos, shards, config RS",
            "Three moving parts to health-check. Losing CSRS is not 'just metadata.'",
        )
    )

    s.append(
        split_slide(
            "Shards",
            [
                "Each shard holds a subset of sharded data",
                "Production shard = replica set",
                "Partitioned data plus redundancy inside the partition",
                "Independent failover for that shard’s members",
            ],
            "108-shard-responsibilities.svg",
            "Shard as replica set",
            "A shard primary election only blocks operations that need that shard.",
        )
    )

    s.append(
        split_slide(
            "Configuration Server Replica Set",
            [
                "Stores cluster metadata: collections, keys, ranges, zones",
                "Critical infrastructure — availability and backups matter",
                "Not where `orders` documents live",
            ],
            "113-config-server-replica-set.svg",
            "Config metadata kinds",
            "Treat CSRS like the map of the city. Without the map, routers cannot route new metadata operations.",
        )
    )

    s.append(
        split_slide(
            "The `mongos` Query Router",
            [
                "Accepts client requests and reads metadata",
                "Targets shards; merges results when needed",
                "Does **not** store application collection data",
                "Deploy more than one router for applications",
            ],
            "118-mongos-query-router.svg",
            "mongos routing steps",
            "Applications connect to mongos (or a load-balanced mongos pool), not to a shard as the only entry.",
        )
    )

    s.append(
        split_slide(
            "Sharded Request Flow",
            [
                "App → `mongos` interprets the query",
                "`mongos` consults routing metadata",
                "Relevant shard or shards execute",
                "Merge if required, then reply",
            ],
            "119-sharded-read-flow.svg",
            "Request flow through mongos",
            "Targeted is cheap. Scatter-gather is a broadcast. They will see this in explain.",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            7,
            "Label a Sharded Cluster",
            "10 min",
            "Label mongos, config servers, shards as replica sets, metadata, and query flow.",
            "245-ex-7-7-label-cluster.svg",
            "Cluster diagram to label",
            "Catch anyone putting orders on the config servers.",
        )
    )

    s.append(
        split_slide(
            "Demo 7.7 — Inspect a Sharded Cluster",
            [
                "**15 min** · instructor `mongos`",
                "`sh.status()` — shards, keys, ranges, balancer",
                "Identify CSRS, sharded collections, distribution",
                "Atlas M0 will not substitute; project yours if needed",
            ],
            "198-sh-status-concept-map.svg",
            "sh.status concept map",
            "Read the output slowly. Shard ids, then collections, then chunks. Do not skip CSRS.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "What Is a Shard Key?",
            [
                "Field or fields used to distribute documents",
                "`{ customerId: 1 }`",
                "`{ tenantId: 1, createdAt: 1 }`",
                '`{ customerId: "hashed" }`',
                "One of the most important sharding decisions",
            ],
            "124-what-is-a-shard-key.svg",
            "Example shard keys",
            "Immutable enough, present on every document, aligned with queries. Changing later is resharding, not a rename.",
        )
    )

    s.append(
        split_slide(
            "Shard-Key Characteristics",
            [
                "Cardinality and frequency",
                "Write distribution and query targeting",
                "Growth, divisibility, locality",
                "No universally ideal shard key",
            ],
            "125-shard-key-selection-framework.svg",
            "Cardinality, distribution, writes, targeting, growth",
            "Score keys; do not hunt for a perfect field. training_store paymentStatus fails almost every column.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Cardinality",
            [
                "**Low:** NEW, PAID, SHIPPED — too few buckets",
                "**High:** customerId, orderId, deviceId",
                "Higher cardinality enables finer distribution",
                "Still check frequency — one celebrity customer",
            ],
            "127-shard-key-cardinality.svg",
            "Low versus high cardinality",
            "Status as shard key is the canonical bad example. Use it in Exercise 7.8.",
        )
    )

    s.append(
        split_slide(
            "Frequency and Value Distribution",
            [
                "High cardinality can still skew",
                "Tenant A = 80% of traffic → hot shard",
                "Uneven storage and request load",
                "Use real workload patterns, not unique-count only",
            ],
            "131-skewed-tenant.svg",
            "Skewed tenant traffic",
            "Enterprise tenants in the challenge are this slide. Compound keys and isolation are mitigations, not magic.",
        )
    )

    s.append(
        split_slide(
            "Monotonic Shard Keys",
            [
                "Increasing timestamps, sequences, counters",
                "Ranged sharding sends new writes to the high end",
                "Creates a write hotspot on one chunk/shard",
                "Mitigate: hashed, compound, other distribution, careful zones",
            ],
            "132-monotonic-shard-key.svg",
            "Writes piling on the max range",
            "createdAt as a ranged key is the second canonical failure. Hashed createdAt is rarely what they wanted for date-range reports either.",
        )
    )

    s.append(
        split_slide(
            "Query Isolation",
            [
                "A query is targeted when the router can pick shard(s) from the key",
                '`find({ customerId: "C101" })` if customerId is the key',
                "Without a usable key predicate, the query goes broadly",
            ],
            "134-query-isolation.svg",
            "Targeted versus untargeted find",
            "This is why modeling access patterns in Module 3 still matters. You shard for the queries you actually run.",
        )
    )

    s.append(
        split_slide(
            "Ranged Sharding",
            [
                "Contiguous key ranges: A–F, G–M, N–Z",
                "Efficient range targeting and locality",
                "Risks: uneven values, monotonic write hotspots",
            ],
            "138-ranged-sharding.svg",
            "Alphabet ranges on three shards",
            "Great for customerId prefixes and date ranges **inside** a customer. Poor for global increasing dates.",
        )
    )

    s.append(
        split_slide(
            "Hashed Sharding",
            [
                "Hash the key, then range the hashes",
                "Even distribution for many equality workloads",
                "Reduces monotonic concentration",
                "Range queries often hit many shards; locality lost",
            ],
            "143-hashed-sharding.svg",
            "Value to hash to shard",
            "Hashed is not 'better sharding.' It is a distribution strategy with a range-query tax.",
        )
    )

    s.append(
        split_slide(
            "Zoned Sharding",
            [
                "Associate key ranges with particular shards",
                "Geo placement, residency, hardware tiers, tenants",
                "Canada ranges → Canada zone; Europe → Europe zone",
                "Requires careful operational planning",
            ],
            "148-zoned-sharding.svg",
            "Canada and Europe zones",
            "Zones do not fix a 90% Canada user base. They put 90% of the work on the Canada shards — which may be correct for law, not for load.",
        )
    )

    s.append(
        split_slide(
            "Ranged vs. Hashed Sharding",
            [
                "Ranged: order, range queries, locality, hotspot risk",
                "Hashed: even spread, sequential-write relief, scatter ranges",
                "Pick from the query mix, not from fashion",
            ],
            "147-ranged-vs-hashed.svg",
            "Ranged versus hashed comparison",
            "Exercise 7.10 is this table applied to two workloads.",
        )
    )

    s.append(
        split_slide(
            "Compound Shard Keys",
            [
                "`{ tenantId: 1, orderId: 1 }`",
                "Tenant targeting, more cardinality, better splits",
                "Queries missing the leading field target poorly",
                "Leading field must match the important filter",
            ],
            "135-compound-shard-key.svg",
            "Compound tenant and orderId",
            "Same ESR intuition as indexes: the prefix you query is the prefix you shard.",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            8,
            "Evaluate Shard-Key Candidates",
            "20 min",
            "Score six order-key candidates; recommend one and name remaining risks.",
            "246-ex-7-8-evaluate-keys.svg",
            "Shard-key candidates",
            "Required exercise. Reject status. Flag createdAt. Make them pick and live with a risk.",
        )
    )

    s.append(
        split_slide(
            "Demo 7.10 — Evaluate Shard-Key Candidates",
            [
                "**20 min** · whiteboard discussion for `orders`",
                "`status` · `createdAt` · `customerId` · hashed `customerId`",
                "`{ tenantId, orderId }` · `{ customerId, createdAt }`",
                "Score cardinality, distribution, targeting, hotspot risk",
            ],
            "246-ex-7-8-evaluate-keys.svg",
            "Shard-key candidate scorecard",
            "Can merge with Exercise 7.8 if time is tight. Use training_store field names they already know.",
            fit="fit-md",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            10,
            "Compare Ranged and Hashed Sharding",
            "15 min",
            "Evaluate both strategies for equality, ranges, sequential writes, locality, and complexity.",
            "248-ex-7-10-ranged-or-hashed.svg",
            "Ranged versus hashed",
            "Two workloads, two answers. UUID equality vs customer history.",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            11,
            "Diagnose Hotspot Risks",
            "15 min",
            "Review five hotspot patterns and propose a mitigation for each.",
            "249-ex-7-11-find-the-hotspot.svg",
            "Hot shard among three",
            "Celebrity product is often a cache problem, not a new shard key.",
        )
    )

    s.append(
        split_slide(
            "Chunks and Data Distribution",
            [
                "Logical ranges of shard-key values",
                "Ranges live on shards; the app sees one collection",
                "Balance is about ranges and data size, not 'feel'",
            ],
            "153-logical-data-ranges.svg",
            "Ranges on three shards",
            "Chunk is the teaching word. Newer versions talk ranges — same idea: a movable piece of key space.",
        )
    )

    s.append(
        split_slide(
            "Chunk Splitting",
            [
                "A large range can split into smaller ranges",
                "Split point selected → Range A + Range B",
                "Smaller units migrate independently",
            ],
            "156-range-splitting.svg",
            "One range splitting into two",
            "Splits enable movement. They are not themselves a rebalance.",
        )
    )

    s.append(
        split_slide(
            "The Balancer",
            [
                "Redistributes ranges across shards",
                "Responds to uneven data, new shards, zones",
                "Consumes resources — monitor it",
                "Can be a surprise I/O storm if ignored",
            ],
            "158-the-balancer.svg",
            "Balancer moving ranges",
            "Do not turn the balancer off forever as a performance hack without a plan.",
        )
    )

    s.append(
        split_slide(
            "Chunk Migration",
            [
                "Copy range → catch up changes → update metadata",
                "Then clean up the donor",
                "Applications keep using `mongos` during the move",
            ],
            "161-chunk-migration-flow.svg",
            "Migration steps",
            "Migrations are online. They are not free. Jumbo chunks that cannot split/move are an ops ticket.",
        )
    )

    s.append(
        split_slide(
            "Targeted Queries",
            [
                "Enough shard-key information to pick shard(s)",
                "Example: customerId + orderNumber when customerId leads the key",
                "Usually less network, less merge, lower latency",
            ],
            "166-targeted-query.svg",
            "mongos contacting one shard",
            "This is the OLTP happy path. Design the key so the happy path exists.",
        )
    )

    s.append(
        split_slide(
            "Scatter-Gather Queries",
            [
                "Sent to many or all shards, then merged",
                "More network, latency, shard CPU, merge work",
                "Not always avoidable — keep them off the hot path",
            ],
            "168-scatter-gather.svg",
            "Query fanning out to all shards",
            "Monthly global revenue is the honest example. Do not pretend a clever shard key makes every report single-shard.",
        )
    )

    s.append(
        split_slide(
            "Targeted vs. Scatter-Gather",
            [
                "Targeted: shard-key condition picks shard(s)",
                "Scatter-gather: no useful key — broadcast then merge",
                "Keep scatter-gather off the hot path",
            ],
            "169-targeted-vs-scatter-gather.svg",
            "One-shard request compared with distributed merge",
            "Essential diagram. Monthly global revenue is honest scatter-gather.",
        )
    )

    s.append(
        split_slide(
            "Shard-Key Queries",
            [
                "Full shard key → usually targeted",
                "Leading compound fields → may target selected ranges",
                "Non-key fields only → often scatter-gather",
                "Hashed equality → targeted; hashed range → broad",
            ],
            "170-query-routing-decision.svg",
            "Contains shard key? Target or broadcast",
            "Exercise 7.9 uses this. Partial compound keys that skip the prefix are the trick question.",
            fit="fit-md",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            9,
            "Targeted or Scatter-Gather?",
            "15 min",
            "Classify queries as targeted, multi-shard, scatter-gather, or insufficient information.",
            "247-ex-7-9-targeted-or-scatter.svg",
            "Scatter-gather versus targeted",
            "Required. paymentStatus-only is scatter-gather. Full customerId prefix is targeted.",
        )
    )

    s.append(
        split_slide(
            "Demo 7.8 — Route Targeted and Scatter-Gather Queries",
            [
                "**20 min**",
                "`explain` a query **with** the shard key and one **without**",
                "Compare targeted shards, work, merge, latency",
                "Evidence behind Exercise 7.9",
            ],
            "169-targeted-vs-scatter-gather.svg",
            "One-shard request compared with broadcast merge",
            "Required demo if a mongos exists. Otherwise walk a printed explain. Do not fake targeting on an unsharded collection.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Demo 7.9 — Observe Shard Distribution",
            [
                "**15 min**",
                "Counts or data size per shard; range counts; balancer",
                "Zones if configured",
                "Tiny training data may sit on one shard — say that out loud",
            ],
            "159-balanced-cluster.svg",
            "Ranges distributed across shards",
            "Optional. Combine with Lab 7.9 if you run the extra lab block. Nobody 'fixes' uneven tiny data with random inserts.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Hot Shards and Hotspots",
            [
                "One shard takes disproportionate writes, reads, growth, CPU, or network",
                "Causes: monotonic keys, dominant tenants, skew, bad routing, zones, recent-data concentration",
            ],
            "179-hot-shard-overview.svg",
            "One hot shard",
            "Adding shards does not help if 80% of writes still hash or range to the same place.",
        )
    )

    s.append(
        split_slide(
            "Distributed Writes",
            [
                "Client → `mongos` → destination shard primary",
                "That replica set replicates the oplog",
                "Ack follows write concern",
                "Sharding and replication share the write path",
            ],
            "186-distributed-write-path.svg",
            "Write path through mongos and shard RS",
            "A sharded write can still roll back on that shard if write concern is weak. Two mechanisms, one client ack.",
        )
    )

    s.append(
        split_slide(
            "Unique Constraints in Sharded Collections",
            [
                "Uniqueness must be compatible with the shard key",
                "Design business identifiers together with the key",
                "Do not assume `orderNumber` unique works like on a replica set",
                "Confirm version-specific rules",
            ],
            "192-unique-in-sharded.svg",
            "Uniqueness aligned with shard-key design",
            "Foot-gun slide. Point at docs; do not invent a unique-index recipe for every version.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Transactions in Sharded Clusters",
            [
                "Can span shards — extra network and coordination",
                "Higher latency and failure complexity",
                "Prefer single-document or single-shard updates",
                "Good modeling reduces cross-shard transactions",
            ],
            "190-single-vs-distributed-txn.svg",
            "Local coordination compared with multi-shard coordination",
            "Tie to Module 3 order aggregate: one order document often avoids a cross-shard transaction.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Resharding Concepts",
            [
                "Workloads evolve; a key can hotspot later",
                "Resharding redistributes to a new key",
                "Major ops: capacity, monitoring, rollback planning",
                "Choosing carefully the first time is cheaper",
            ],
            "194-resharding-concept.svg",
            "Old key through redistribution to a new key",
            "Concept only in this intro. Do not demo live resharding in 3.5 hours.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Sharded-Cluster Status",
            [
                "Shards, sharded DBs/collections, keys, ranges",
                "Balancer and zones",
                "`sh.status()` on `mongos`",
                "Wrong topology is a teaching moment",
            ],
            "198-sh-status-concept-map.svg",
            "sh.status concept map",
            "Lab 7.6. If someone runs this on a replica set, use the error as a teaching moment.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Sharding Operational Practices",
            [
                "Choose keys from measured workload",
                "Replica-set shards; redundant `mongos`",
                "Protect config servers",
                "Monitor routing, distribution, balancer",
                "Back up the distributed deployment",
            ],
            "205-sharded-ops-checklist.svg",
            "Router, shard, metadata, distribution, targeting, backup",
            "Backups of one shard are not a cluster backup story.",
            fit="fit-md",
        )
    )

    s.append(
        split_slide(
            "Sharded-Cluster Failure Scenarios",
            [
                "One shard member: shard RS may stay available",
                "Shard primary down: ops for that shard wait on election",
                "One `mongos` down: use another router",
                "CSRS problems: metadata / DDL suffer — serious",
            ],
            "238-cluster-failure-isolation.svg",
            "Router, shard, member, and config-service blast radius",
            "Partial availability is possible: other shards still work.",
            fit="fit-md",
        )
    )

    s.extend(
        activity_block(
            "lab",
            6,
            "Inspect Sharded-Cluster Components",
            "20 min",
            "Identify mongos, shards, CSRS, sharded collections, and keys.",
            "256-lab-7-6-cluster-inspection.svg",
            "Inspect cluster components",
            "Extra block unless you have mongos for everyone. Sample output is an acceptable substitute.",
        )
    )

    s.extend(
        activity_block(
            "lab",
            7,
            "Shard a Training Collection",
            "25 min",
            "On a disposable cluster, index, shard, insert, and confirm the key.",
            "257-lab-7-7-shard-training-collection.svg",
            "Shard a training collection",
            "Instructor-only cluster. Commands vary by version — you dictate the exact sequence.",
        )
    )

    s.extend(
        activity_block(
            "lab",
            8,
            "Analyze Query Routing",
            "25 min",
            "Explain targeted versus scatter-gather plans for key and non-key queries.",
            "258-lab-7-8-query-routing-analysis.svg",
            "Explain routing lab",
            "Pairs with Demo 7.8. Skip if no mongos.",
        )
    )

    s.extend(
        activity_block(
            "lab",
            9,
            "Review Chunk Distribution",
            "20 min",
            "Assess range distribution, balancer, zones, and hotspot indicators.",
            "259-lab-7-9-distribution-review.svg",
            "Chunk distribution lab",
            "Tiny data looks uneven. Grade the interpretation, not perfect balance.",
        )
    )

    s.append(
        split_slide(
            "Replication and Sharding Together",
            [
                "Sharding partitions the data",
                "Replication copies each partition",
                "Each shard handles part of the data",
                "Each replica set protects its shard",
            ],
            "005-replication-and-sharding-together.svg",
            "mongos over three replica-set shards",
            "This is the production picture they should remember on the exit ticket.",
        )
    )

    s.append(
        split_slide(
            "Deployment Decision Framework",
            [
                "**Standalone:** local learning, disposable tests",
                "**Replica set:** production availability and failover",
                "**Sharded cluster:** measured horizontal scale",
                "**Sharded replica sets:** availability and scale together",
            ],
            "006-standalone-rs-sharded.svg",
            "Standalone, replica set, shard choices",
            "training_store on one mongod was correct for Days 1–2. Production orders are not a standalone.",
        )
    )

    s.append(
        split_slide(
            "E-Commerce Scaling Case Study",
            [
                "Products browsed globally; orders written continuously",
                "History by customer; recent orders hot; global reports",
                "Replica sets for availability first",
                "Shard orders with a customer/tenant-oriented key when needed",
                "Products may wait; analytics isolated; reports costed",
            ],
            "212-collection-by-collection.svg",
            "Per-collection distribution ideas",
            "Different collections, different strategies. That is the key message.",
        )
    )

    s.append(
        split_slide(
            "Common Architecture Mistakes",
            [
                "Treating replication as sharding — or sharding as backup",
                "Low-cardinality or monotonic ranged keys without analysis",
                "Ignoring routing; dumping all reports on secondaries",
                "Arbiter as a 'copy'; single-host URIs; ignoring write concern",
                "Adding shards before fixing schema and indexes",
            ],
            "218-replication-is-not-sharding.svg",
            "Common mistakes",
            "Read this as a checklist. Module 6 belongs here: shard last among performance tools.",
        )
    )

    s.append(
        split_slide(
            "Premature Sharding",
            [
                "Do not shard to hide schema, query, or index problems",
                "Fix the working set, indexes, and hot queries first",
                "Sharding adds routers, metadata, and operational cost",
                "Evidence first: disk, CPU, working set, write latency",
            ],
            "226-premature-sharding.svg",
            "Schema and indexes before adding shards",
            "Conference-slide sharding is the anti-pattern. Module 6 tools come first.",
        )
    )

    s.append(
        split_slide(
            "Troubleshooting Distributed MongoDB",
            [
                "**Replica set:** primary? majority? lag? oplog? election?",
                "**Cluster:** mongos? shards? CSRS? targeted? balancer? hotspot?",
                "Start with topology health, then the query shape",
            ],
            "228-distributed-troubleshooting-flow.svg",
            "Replica set versus cluster checks",
            "Do not tune a shard key while the replica set has no primary.",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            12,
            "Design a Scalable Deployment",
            "25 min",
            "Design 24/7 availability, order growth, lookups, reports, and residency.",
            "250-ex-7-12-design-deployment.svg",
            "Deployment design",
            "If time remains. Residency must be explicit. Otherwise assign as homework before the challenge.",
        )
    )

    s.extend(
        activity_block(
            "lab",
            10,
            "Integrated Availability and Scaling Challenge",
            "40–45 min",
            "End-to-end design: topology, key, routing, settings, failover, monitoring.",
            "260-lab-7-10-integrated-challenge.svg",
            "Integrated challenge",
            "Overlaps the practical challenge. Run one, not both, live.",
        )
    )

    s.append(
        split_slide(
            "Module Summary",
            [
                "Replication: redundancy and failover via the oplog",
                "Sharding: distribute data and work via a shard key",
                "Writes go to a primary; elections need majority",
                "Preference, concern, and write concern are different knobs",
                "Targeted queries beat frequent scatter-gather",
                "Production shards are replica sets",
            ],
            "217-complete-production-architecture.svg",
            "Copy, elect, partition",
            "Restate the opener. Then knowledge check.",
        )
    )

    s.append(
        content_slide(
            "Module Knowledge Check",
            """1. Main purpose of replication? Of sharding?
2. Primary vs secondary? What is the oplog?
3. What causes an election? Why majority?
4. What is replication lag?
5. Read preference vs read concern vs write concern?
6. Role of `mongos`? What do config servers store?
7. What is a shard key? Why is low cardinality a problem?
8. Why can a monotonic ranged key hotspot?
9. Ranged vs hashed? Targeted vs scatter-gather?
10. Why is each production shard a replica set?
11. Is replication a backup? Shard before fixing indexes?""",
            "Use as oral quiz or silent write. Full twenty questions are on the exit ticket.",
            fit="fit-xs",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            13,
            "Scale the E-Commerce Order Platform",
            "30–45 min",
            "Availability design, sharding decision, key comparison, routing analysis, and ops plan — starting from one standalone server.",
            "261-practical-challenge-order-platform.svg",
            "Practical challenge",
            "Capstone. Rubric: replica set first, evidence before sharding, reject status/monotonic-only keys, cost global reports, backups plus HA.",
        )
    )

    s.append(
        content_slide(
            "Module 7 Exit Ticket",
            """1. Main purpose of replication?
2. Main purpose of sharding?
3. Primary vs secondary?
4. What is the oplog?
5. What causes an election?
6. Why is a voting majority important?
7. What is replication lag?
8. Read preference vs read concern?
9. What does write concern control?
10. Role of `mongos`?
11. What do config servers store?
12. What is a shard key?
13. Why is low cardinality usually problematic?
14. Why can a monotonic ranged key hotspot?
15. Ranged vs hashed sharding?
16. What is a targeted query?
17. What is a scatter-gather query?
18. Why is each production shard a replica set?
19. Is replication a replacement for backups?
20. Shard before fixing schema and indexes?""",
            "Collect if you use tickets for attendance. Questions 19–20 are the culture bar.",
            fit="fit-xs",
        )
    )

    s.append(
        content_slide(
            "Module Completion Checklist",
            """Participants can:

- [ ] Distinguish replication from sharding
- [ ] Explain replica-set architecture and a replicated write
- [ ] Describe elections, failover, and majority
- [ ] Explain read preference, read concern, and write concern
- [ ] Identify replication-lag risks
- [ ] Name mongos, shards, and config servers
- [ ] Evaluate basic shard-key candidates
- [ ] Compare ranged, hashed, and zoned sharding
- [ ] Identify targeted vs scatter-gather queries
- [ ] Explain chunks and balancing
- [ ] Sketch a highly available, scalable deployment""",
            "Gaps become homework on the lab guides. Module 8 is production habits, not more topology.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Questions and Answers",
            """Open floor.

Parking-lot prompts:

- When would you keep products unsharded but shard orders?
- What does an application see during `rs.stepDown()`?
- Why might hashed `customerId` hurt a date-range report?

Capture unanswered items for Module 8.""",
            "Do not start security or backup how-tos here. Point at Module 8.",
        )
    )

    s.append(
        content_slide(
            "Transition to Module 8: Best Practices",
            """Module 8 consolidates the course:

- Sustainable data modeling
- Query and index optimization
- Security controls
- Backup and recovery
- Monitoring and alerting
- Operational troubleshooting
- Deployment readiness
- Final hands-on challenge and wrap-up

You now have a replica-set and sharding vocabulary. Module 8 asks what you will actually run in production.""",
            "If the day is slipping, Module 8 still needs security and backup time. Do not steal it for another shard-key debate.",
            fit="fit-sm",
        )
    )

    return "\n\n---\n\n".join(x.strip() + "\n" for x in s)


def append_to_deck(fragment: str) -> None:
    text = DECK.read_text(encoding="utf-8")
    if MARKER in text:
        start = text.find(MARKER)
        prefix = text[:start].rstrip()
        if prefix.endswith("---"):
            prefix = prefix[: -3].rstrip()
        rest = text[start + len(MARKER) :]
        nxt = None
        for marker in NEXT_MARKERS:
            pos = rest.find(marker)
            if pos >= 0:
                nxt = rest[pos:]
                break
        suffix = ("\n\n---\n\n" + nxt.lstrip()) if nxt else ""
        DECK.write_text(prefix + "\n\n---\n\n" + fragment.strip() + suffix, encoding="utf-8")
        print(f"Replaced existing Module 7 in {DECK}")
        return
    insert_at = None
    for marker in NEXT_MARKERS:
        pos = text.find(marker)
        if pos >= 0:
            insert_at = pos
            break
    if insert_at is not None:
        prefix = text[:insert_at].rstrip()
        if prefix.endswith("---"):
            prefix = prefix[: -3].rstrip()
        DECK.write_text(
            prefix + "\n\n---\n\n" + fragment.strip() + "\n\n---\n\n" + text[insert_at:].lstrip(),
            encoding="utf-8",
        )
        print(f"Inserted Module 7 before the next module in {DECK}")
        return
    DECK.write_text(text.rstrip() + "\n\n---\n\n" + fragment.strip() + "\n", encoding="utf-8")
    print(f"Appended Module 7 to {DECK}")


if __name__ == "__main__":
    if not any(LAB_DIR.glob("exercise-7.1-*.md")):
        raise SystemExit("Lab guides missing. Run python scripts/module07_labs.py first.")
    fragment = build_slides()
    append_to_deck(fragment)
    print(f"Module 7 fragment length: {len(fragment):,} chars")

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
            "01-module-map.svg",
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
            "02-requirements.svg",
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
            "03-ha-vs-scale.svg",
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
            "04-vertical-horizontal.svg",
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
            "05-replication-vs-sharding.svg",
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
            "06-distributed-overview.svg",
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
            "59-ex-choice.svg",
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
            "07-replica-set.svg",
            "Primary and two secondaries",
            "Atlas free tier is already a replica set. Students who only used Compass on Atlas have been talking to a primary the whole course.",
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
            "08-members.svg",
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
            "09-primary.svg",
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
            "10-secondary.svg",
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
            "11-oplog.svg",
            "Write, oplog, copy, apply",
            "If a member is down longer than the oplog window, it may need an initial sync. Size the oplog for real maintenance, not for a coffee break.",
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
            "12-replication-flow.svg",
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
            "07-replica-set.svg",
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
            "12-replication-flow.svg",
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
            "13-heartbeats.svg",
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
            "14-elections.svg",
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
            "15-failover.svg",
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
            "16-app-failover.svg",
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
            "17-majority.svg",
            "Two of three form a majority",
            "Draw a network split. The lonely primary steps down. That is a feature.",
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
            "18-priority.svg",
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
            "19-arbiter.svg",
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
            "20-hidden.svg",
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
            "21-delayed.svg",
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
            "15-failover.svg",
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
            "61-demo-rs.svg",
            "rs.status and rs.conf",
            "Project the live output. Circle setName, members[].stateStr, health, optimeDate. Then open rs.conf for votes.",
            fit="fit-md",
        )
    )

    s.append(
        content_slide(
            "Demo 7.2 — Observe Replication",
            """**15 min** · disposable training infrastructure

1. Insert a document on the primary
2. Confirm the write
3. Inspect a secondary **safely** (instructor method)
4. Confirm the document after replication
5. Discuss staleness if you read too soon

Do not send the class to `rs.slaveOk()` folklore. Use a documented read preference or an instructor secondary shell.""",
            "One insert is enough. The point is the copy, not load testing.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Demo 7.3 — Simulate Primary Failover",
            """**20 min** · **disposable** replica set only

1. Record the current primary
2. Controlled `rs.stepDown()` or stop the process
3. Watch the election
4. Identify the new primary
5. Note application reconnect / retry
6. Restore the former member as a secondary

Never step down a shared classroom Atlas cluster unless you declared it disposable.""",
            "Narrate the error window as expected. Then show hello() flipping. Restore before the break.",
            fit="fit-sm",
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
            "22-read-pref.svg",
            "Read preference modes",
            "Default for most drivers is primary. Changing this is an application decision, not a server-wide magic switch.",
        )
    )

    s.append(
        content_slide(
            "Primary Read Preference",
            """`primary` sends reads to the current primary.

**Advantages**

- Sees the primary’s current state
- Simplest consistency story
- Default for many workloads

**Tradeoff**

- Reads share primary resources with writes
- Reads can pause briefly during elections""",
            "Order-status right after pay: stay on primary unless they can explain stale as acceptable.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Secondary Read Preferences",
            """Secondary reads may help reporting, geo-local reads, or shedding some primary read load.

**Tradeoffs**

- Data may be behind the primary
- Stale results can be wrong for the business
- Secondary capacity is not free

Sending reads to secondaries does **not** automatically make the whole system faster.""",
            "If analytics saturates a secondary, lag grows and failover readiness drops. Module 6 lesson: extra work still costs hardware.",
            fit="fit-sm",
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
            "23-write-concern.svg",
            "Primary, majority, numeric w",
            "Write concern is the client’s success definition. Show wtimeout so they do not hang forever.",
        )
    )

    s.append(
        content_slide(
            "Common Write-Concern Levels",
            """**Primary acknowledgment (`w: 1`)**  
Lower latency, less replica-set confirmation.

**Majority**  
A majority of voting data-bearing members have acknowledged per configured semantics.

**Custom numeric `w`**  
Wait for N members.

Stronger acknowledgment usually increases durability confidence and can increase latency. Do not present `w: 0` / `w: 1` as a universal performance solution.""",
            "For payments, majority is the teaching default. Custom w=3 on a 3-node set can be stricter than majority depending on config — keep it conceptual.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Read Concern",
            """Influences visibility and isolation of reads.

Common levels: `local` · `available` · `majority` · `linearizable` · `snapshot`

Choose based on transactions, staleness tolerance, performance, deployment, and application semantics.

This module teaches the **idea**. Exact guarantees depend on version and topology — confirm in docs for production.""",
            "Do not pretend to finish causal consistency in five minutes. Pair with write concern majority for 'I need to read what I just majority-wrote' stories.",
            fit="fit-sm",
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
            "24-three-settings.svg",
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
            "24-three-settings.svg",
            "Three settings for business ops",
            "Push back if payment confirmation is secondaryPreferred. Analytics may be stale on purpose.",
        )
    )

    s.append(
        content_slide(
            "Demo 7.4 — Compare Write Concerns",
            """**15 min** · controlled environment

Write the same insert with different acknowledgment requirements.

Discuss latency, confirmation, failure/`wtimeout` behavior, and durability.

Avoid “just use `w: 1` to go faster” as architecture advice.""",
            "If times are similar on an idle three-node Atlas set, say so. The lesson is the contract, not a benchmark.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Demo 7.5 — Compare Read Preferences",
            """**15 min**

Compare `primary`, `primaryPreferred`, `secondaryPreferred`, `nearest`.

Observe which member is selected. Discuss freshness.

`nearest` is latency, not “the secondary in Europe that has yesterday’s data I wanted.”""",
            "Show db.hello() / connection handshake. nearest can still be the primary if it is closest.",
            fit="fit-sm",
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
            "25-lag.svg",
            "Primary T0 versus secondary T0 plus lag",
            "A few seconds idle is normal. Growing lag is an incident. Zero lag is not a promise under load.",
        )
    )

    s.append(
        content_slide(
            "Causes of Replication Lag",
            """- Slow disks, network latency, insufficient CPU
- Heavy write volume or large operations
- Index differences and resource contention
- Maintenance and secondary-specific workloads
- Oplog window too small for an interrupted member

Lag is a **symptom**. Collect disk, CPU, network, currentOps, and oplog window before you rebuild a node.""",
            "Tie to Exercise 7.6. Reporting on a secondary is a classic self-inflicted lag.",
            fit="fit-sm",
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
            "26-rollback.svg",
            "Former primary versus current history",
            "w:1 + failover is the story. Majority writes that completed are the ones you designed to keep.",
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
            "27-rs-status.svg",
            "Status commands",
            "Lab 7.1 is this slide in the shell. Atlas UI is allowed as a complement, not a replacement for rs.status().",
        )
    )

    s.append(
        content_slide(
            "Replica-Set Operational Practices",
            """- Odd number of voting members where practical
- Independent failure domains
- Monitor lag and oplog window
- Replica-set connection strings
- Test failover; keep backups
- Appropriate read and write concerns
- Consistent member config; secure member and client traffic""",
            "Backups still required. Replication is HA, not a backup product.",
            fit="fit-sm",
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
            "28-failure-scenarios.svg",
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
            "25-lag.svg",
            "Lag diagnosis",
            "If every answer is 'restart MongoDB,' send them back to metrics.",
        )
    )

    s.append(
        content_slide(
            "Demo 7.6 — Inspect Replication Lag",
            """**10 min**

Compare member replication times. Discuss normal small delay vs growing lag.

Tie to disk, network, write bursts, and secondary workloads.""",
            "Show printSecondaryReplicationInfo. If lag is zero, still describe what 45 seconds would mean for secondary reads.",
            fit="fit-sm",
        )
    )

    s.extend(
        activity_block(
            "lab",
            1,
            "Verify Replica-Set Health",
            "20 min",
            "Inspect name, states, votes, and timestamps; write a health report.",
            "62-lab-health.svg",
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
            "12-replication-flow.svg",
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
            "15-failover.svg",
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
            "24-three-settings.svg",
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
            "25-lag.svg",
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
            "29-what-is-sharding.svg",
            "Three shards holding ranges",
            "Sharding is not the default for training_store. Seventeen orders do not need three shards.",
        )
    )

    s.append(
        content_slide(
            "Why Applications Need Sharding",
            """Consider sharding when:

- Dataset exceeds one replica set’s practical capacity
- Read or write demand exceeds one replica set
- Working set no longer fits effectively
- Geographic placement is required
- Vertical scaling is no longer sustainable

**Warning:** shard to a measured need, not a slide from a conference.""",
            "Ask what evidence they have: disk forecasts, CPU, working set, write latency. No evidence, no shard key.",
            fit="fit-sm",
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
            "30-cluster-components.svg",
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
            "31-shards.svg",
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
            "32-csrs.svg",
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
            "33-mongos.svg",
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
            "34-request-flow.svg",
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
            "30-cluster-components.svg",
            "Cluster diagram to label",
            "Catch anyone putting orders on the config servers.",
        )
    )

    s.append(
        content_slide(
            "Demo 7.7 — Inspect a Sharded Cluster",
            """**15 min** · instructor `mongos`

```javascript
sh.status()
```

Identify shards, config database, sharded collections, shard keys, ranges, distribution.

If the room has no mongos, project yours. Atlas M0 will not substitute.""",
            "Read the output slowly. Shard ids, then collections, then chunks. Do not skip CSRS.",
            fit="fit-sm",
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
            "35-shard-key.svg",
            "Example shard keys",
            "Immutable enough, present on every document, aligned with queries. Changing later is resharding, not a rename.",
        )
    )

    s.append(
        content_slide(
            "Shard-Key Characteristics",
            """Evaluate:

- Cardinality and frequency distribution
- Write distribution and query targeting
- Growth pattern and divisibility
- Locality and long-term application behavior

There is **no** universally ideal shard key.""",
            "Score keys; do not hunt for a perfect field. Training_store paymentStatus fails almost every column.",
            fit="fit-sm",
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
            "36-cardinality.svg",
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
            "37-frequency.svg",
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
            "38-monotonic.svg",
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
            "39-query-isolation.svg",
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
            "40-ranged.svg",
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
            "41-hashed.svg",
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
            "42-zoned.svg",
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
            "43-ranged-vs-hashed.svg",
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
            "44-compound.svg",
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
            "35-shard-key.svg",
            "Shard-key candidates",
            "Required exercise. Reject status. Flag createdAt. Make them pick and live with a risk.",
        )
    )

    s.append(
        content_slide(
            "Demo 7.10 — Evaluate Shard-Key Candidates",
            """**20 min** · discussion at the whiteboard

Compare for `orders`:

- `status` / `paymentStatus`
- `createdAt`
- `customerId`
- hashed `customerId`
- `{ tenantId, orderId }`
- `{ customerId, createdAt }`

Score cardinality, distribution, targeting, monotonic behavior, tenant concentration.""",
            "Can merge with Exercise 7.8 if time is tight. Use training_store field names they already know.",
            fit="fit-sm",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            10,
            "Compare Ranged and Hashed Sharding",
            "15 min",
            "Evaluate both strategies for equality, ranges, sequential writes, locality, and complexity.",
            "43-ranged-vs-hashed.svg",
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
            "51-hotspots.svg",
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
            "45-chunks.svg",
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
            "46-split.svg",
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
            "47-balancer.svg",
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
            "48-migration.svg",
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
            "49-targeted.svg",
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
            "50-scatter-gather.svg",
            "Query fanning out to all shards",
            "Monthly global revenue is the honest example. Do not pretend a clever shard key makes every report single-shard.",
        )
    )

    s.append(
        content_slide(
            "Shard-Key Queries",
            """| Query includes | Routing behavior |
| --- | --- |
| Full shard key | Usually targeted |
| Leading fields of a compound ranged key | May target selected ranges |
| Non-shard-key fields only | Often scatter-gather |
| Broad shard-key range | May hit multiple shards |
| Hashed key equality | Targeted |
| Hashed key range | Usually broadly distributed |

Exact routing depends on metadata and predicates.""",
            "Exercise 7.9 uses this table. Partial compound keys that skip the prefix are the trick question.",
            fit="fit-sm",
        )
    )

    s.extend(
        activity_block(
            "exercise",
            9,
            "Targeted or Scatter-Gather?",
            "15 min",
            "Classify queries as targeted, multi-shard, scatter-gather, or insufficient information.",
            "50-scatter-gather.svg",
            "Scatter-gather versus targeted",
            "Required. paymentStatus-only is scatter-gather. Full customerId prefix is targeted.",
        )
    )

    s.append(
        content_slide(
            "Demo 7.8 — Route Targeted and Scatter-Gather Queries",
            """**20 min**

`explain` a query **with** the shard key and one **without**.

Compare targeted shards, work, merge, potential latency.

This demo is the evidence behind Exercise 7.9.""",
            "Required demo if a mongos exists. Otherwise walk a printed explain. Do not fake targeting on an unsharded collection.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Demo 7.9 — Observe Shard Distribution",
            """**15 min**

Inspect document counts or data size per shard, range counts, balancer activity, zones if configured.

Tiny training data may sit on one shard. Say that out loud so nobody 'fixes' it with random inserts without a plan.""",
            "Optional. Combine with Lab 7.9 if you run the extra lab block.",
            fit="fit-sm",
        )
    )

    s.append(
        split_slide(
            "Hot Shards and Hotspots",
            [
                "One shard takes disproportionate writes, reads, growth, CPU, or network",
                "Causes: monotonic keys, dominant tenants, skew, bad routing, zones, recent-data concentration",
            ],
            "51-hotspots.svg",
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
            "52-distributed-writes.svg",
            "Write path through mongos and shard RS",
            "A sharded write can still roll back on that shard if write concern is weak. Two mechanisms, one client ack.",
        )
    )

    s.append(
        content_slide(
            "Unique Constraints in Sharded Collections",
            """Unique indexes on sharded collections need the uniqueness pattern to be compatible with the shard key.

Design business identifiers **together** with the shard key when global uniqueness is required.

Confirm version- and deployment-specific rules before a production unique index. Do not assume `orderNumber` unique works the same as on a replica set.""",
            "This is a foot-gun slide. Point at docs; do not invent a unique-index recipe for every version.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Transactions in Sharded Clusters",
            """Multi-document transactions can span shards. Cost:

- Extra network and coordination
- Higher latency and failure complexity
- More resource use

Good modeling and shard keys reduce **unnecessary** cross-shard transactions. Prefer single-document or single-shard updates when the domain allows.""",
            "Tie to Module 3 order aggregate: one order document often avoids a cross-shard transaction for line items.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Resharding Concepts",
            """Workloads evolve. A key that once distributed well may hotspot or scatter later.

Resharding changes distribution to a new key. It is a major operational activity: capacity, compatibility, monitoring, performance tests, failure and rollback planning.

Choosing carefully the first time is cheaper than resharding under pressure.""",
            "Do not demo live resharding in a 3.5 hour intro unless you have a dedicated extra lab. Concept only.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Sharded-Cluster Status",
            """Useful views: shards, sharded DBs/collections, keys, distribution, balancer, zones.

```javascript
sh.status()
```

Availability depends on privileges and whether you are actually on `mongos`.""",
            "Lab 7.6. If someone runs this on a replica set, use the error as a teaching moment.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Sharding Operational Practices",
            """- Choose keys from measured workload
- Replica sets for shards; redundant `mongos`
- Protect config servers
- Monitor routing, distribution, balancer
- Test shard failure
- Avoid uncontrolled scatter-gather on the hot path
- Back up the **distributed** deployment""",
            "Backups of one shard are not a cluster backup story.",
            fit="fit-sm",
        )
    )

    s.append(
        content_slide(
            "Sharded-Cluster Failure Scenarios",
            """**One shard member fails** — the shard replica set may stay available if it keeps a primary.

**Shard loses primary** — operations that need that shard wait on election.

**One `mongos` fails** — clients use another router if configured.

**Config-server problems** — metadata and management suffer; this is serious.""",
            "Contrast with replica-set-only failure. Partial availability is possible: other shards still work.",
            fit="fit-sm",
        )
    )

    s.extend(
        activity_block(
            "lab",
            6,
            "Inspect Sharded-Cluster Components",
            "20 min",
            "Identify mongos, shards, CSRS, sharded collections, and keys.",
            "30-cluster-components.svg",
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
            "35-shard-key.svg",
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
            "49-targeted.svg",
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
            "45-chunks.svg",
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
            "53-together.svg",
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
            "54-decision.svg",
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
            "55-ecommerce.svg",
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
            "56-mistakes.svg",
            "Common mistakes",
            "Read this as a checklist. Module 6 belongs here: shard last among performance tools.",
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
            "57-troubleshoot.svg",
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
            "54-decision.svg",
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
            "60-challenge.svg",
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
            "58-concept-map.svg",
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
            "60-challenge.svg",
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

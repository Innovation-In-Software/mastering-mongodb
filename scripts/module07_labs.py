"""Write Module 7 lab guides. Run: python scripts/module07_labs.py"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "slide-exercises" / "module-07"

ENV_MONGO = """## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected with a **replica-set URI**.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

**Replica-set labs:** Atlas (`mongodb+srv://`) is a replica set. A local standalone `mongod` is not. If `rs.status()` reports that the process is not running with `--replSet`, switch to the instructor Atlas URI.

**Failover and sharding labs:** Use only an instructor-controlled disposable cluster. Do **not** step down or shard a shared classroom Atlas deployment unless the instructor says it is disposable.

```javascript
use training_store
```
"""

ENV_DISCUSSION = """## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may inspect `training_store` or `rs.status()` to test ideas. Reasoning is the deliverable unless a step asks you to run a command.
"""

ENV_SHARD = """## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell · `mongosh` against the **instructor sharded training cluster** when provided.

| Task | Windows | Where |
|------|---------|-------|
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| Connect | Instructor `mongos` URI | Same terminal |

Atlas M0 is a replica set, **not** a sharded cluster. If no `mongos` URI is available, complete the steps using the sample output in this guide and the instructor demonstration.

Do **not** enable sharding on a shared production-like database.
"""


def js(code: str) -> str:
    return f"```javascript\n{code.strip()}\n```"


def guide(
    kind: str,
    num: int,
    slug: str,
    title: str,
    time: str,
    difficulty: str,
    objective: str,
    steps: list[tuple[str, str, str]],
    success: list[str],
    *,
    discussion: bool = False,
    sharded: bool = False,
    extra: str = "",
) -> tuple:
    env = ENV_DISCUSSION if discussion else (ENV_SHARD if sharded else ENV_MONGO)
    label = "Exercise" if kind == "exercise" else "Lab"
    step_md = []
    for i, (stitle, do, exp) in enumerate(steps, 1):
        step_md.append(f"### Step {i} — {stitle}\n\n**Do this:** {do}\n\n**Expected result:** {exp}\n")
    steps_block = "\n---\n\n".join(step_md)
    checks = "\n".join(f"- [ ] {c}" for c in success)
    extra_block = f"\n{extra.strip()}\n" if extra else ""
    md = f"""# {label} 7.{num}: {title}

**Module 7:** Introduction to Replication and Sharding  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 7)  
**Time:** {time}  
**Difficulty:** {difficulty}

**Objective:** {objective}

---

{env}

---

## Steps from the training slides

Follow these steps in order.

{steps_block}
---
{extra_block}
## Success criteria

{checks}

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
"""
    return (kind, num, slug, title, time, "discussion" if discussion else "hands-on", objective, md)


GUIDES: list[tuple] = []

GUIDES.append(
    guide(
        "exercise",
        1,
        "replication-or-sharding",
        "Replication or Sharding?",
        "10 min",
        "Beginner",
        "Choose replication, sharding, both, or neither yet for six architecture requirements.",
        [
            (
                "Classify six requirements",
                "For each item, write **Replication**, **Sharding**, **Both**, or **Neither yet**: (1) survive one server failure, (2) increase total data capacity, (3) automatically elect a replacement primary, (4) distribute write load, (5) create a local development database, (6) provide production availability and scale.",
                "1 Replication. 2 Sharding. 3 Replication. 4 Sharding. 5 Neither yet (standalone is enough). 6 Both (sharded replica sets).",
            ),
            (
                "Defend one borderline case",
                "In two sentences, explain why copying data to secondaries does **not** increase total storage capacity for the application dataset.",
                "Each member stores the same logical dataset. Extra members add redundancy, not a larger working set.",
            ),
        ],
        [
            "Six classifications match the intended mechanisms",
            "Local development is not forced into a replica set or shard",
            "Capacity is not confused with redundancy",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        2,
        "label-a-replica-set",
        "Label a Replica-Set Architecture",
        "10 min",
        "Beginner",
        "Label application, driver, primary, secondaries, oplog flow, heartbeats, and read/write paths.",
        [
            (
                "Label members and clients",
                "On the replica-set diagram, mark Application, Driver, Primary, and two Secondaries.",
                "One primary, two secondaries, client path through the driver — not a raw single-host arrow to a secondary for writes.",
            ),
            (
                "Label flows",
                "Draw oplog flow (primary → secondaries), heartbeats (all members), write path (app → primary), and a primary-preference read path.",
                "Writes hit the primary. Heartbeats are separate from oplog copy. Reads to secondaries are not the default write path.",
            ),
        ],
        [
            "Primary is unique",
            "Oplog and heartbeats are not the same arrow",
            "Writes are not drawn to a secondary",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        3,
        "trace-a-replicated-write",
        "Trace a Replicated Write",
        "15 min",
        "Beginner",
        "Sequence a write from the client through oplog application and write-concern acknowledgment.",
        [
            (
                "Order the seven events",
                "Number these 1–7: client sends write; driver selects primary; primary applies write; oplog entry is created; secondaries copy the operation; secondaries apply it; acknowledgment returns based on write concern.",
                "That listed order is the teaching sequence. Acknowledgment is last and depends on `w`.",
            ),
            (
                "Change one setting",
                "State what changes if write concern is majority instead of primary-only acknowledgment.",
                "The client waits until a majority of voting data-bearing members have durably acknowledged, so latency can increase and durability confidence increases.",
            ),
        ],
        [
            "The seven-step order is correct",
            "Write concern is not treated as read preference",
            "Secondaries apply after they copy oplog entries",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        4,
        "sequence-a-failover",
        "Sequence a Failover",
        "15 min",
        "Beginner",
        "Arrange detection, election, new primary, driver discovery, and application retry.",
        [
            (
                "Arrange the sequence",
                "Order: primary becomes unavailable; members detect failure; election starts; eligible members vote; new primary is selected; driver discovers new topology; application retries eligible operations.",
                "That order. Detection uses heartbeats. Writes pause during the election window.",
            ),
            (
                "Name an application requirement",
                "Write two application behaviors that make failover survivable.",
                "Replica-set connection string (not a pinned host) and retryable / idempotent operations with sensible timeouts.",
            ),
        ],
        [
            "Election happens before a new primary accepts writes",
            "Driver discovery is after the new primary exists",
            "Application retry is part of the story",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        5,
        "select-read-and-write-settings",
        "Select Read and Write Settings",
        "20 min",
        "Intermediate",
        "Choose read preference, read concern, and write concern for six business operations and justify staleness versus durability.",
        [
            (
                "Critical money paths",
                "For **payment confirmation** and **financial reconciliation**, choose read preference, read concern, and write concern. State what you refuse to trade away.",
                "Payment: read `primary` (or primaryPreferred only with a documented reason), write concern `majority`, read concern `majority` or `snapshot` in a transaction. Reconciliation: same freshness/durability bias — not secondary reads of unpaid lag.",
            ),
            (
                "Catalog, status, reporting",
                "For **product-catalog browsing**, **customer order status**, **operational reporting**, and **noncritical analytics**, choose settings and one sentence on staleness.",
                "Catalog: `primaryPreferred` or `nearest` with local/available reads is often acceptable. Order status: prefer primary or majority if the customer just paid. Reporting/analytics: `secondaryPreferred` can be fine if the report may be minutes behind and the secondary has capacity.",
            ),
        ],
        [
            "Payment is not served from a lagging secondary as truth",
            "The three settings are not treated as interchangeable",
            "Analytics may accept staleness explicitly",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        6,
        "diagnose-replication-lag",
        "Diagnose Replication Lag",
        "15 min",
        "Intermediate",
        "Match lag symptoms to cause, impact, evidence, and a first corrective action.",
        [
            (
                "Map five symptoms",
                "For each: high disk latency; heavy reporting on a secondary; network congestion; rapid write growth; small oplog window — write likely cause, impact, evidence to collect, and first action.",
                "Disk: storage saturation → growing lag → iostat/Atlas metrics → faster disks or less write amplification. Reporting: secondary CPU/IO → lag + stale reads → isolate analytics. Network: delayed oplog fetch. Write burst: primary faster than apply. Small oplog: member may fall off and need initial sync.",
            ),
            (
                "Pick the first metric",
                "If a secondary is 90 seconds behind and reporting dashboards look empty, which two checks do you run first?",
                "`rs.printSecondaryReplicationInfo()` / member optimes, and secondary CPU, disk, and current operations — not an immediate rebuild.",
            ),
        ],
        [
            "Each symptom has a distinct first check",
            "Oplog window is treated as a recovery risk",
            "Reporting load is not ignored as free capacity",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        7,
        "label-a-sharded-cluster",
        "Label a Sharded Cluster",
        "10 min",
        "Beginner",
        "Label application, driver, mongos, configuration servers, shards, replica-set members, metadata, and query flow.",
        [
            (
                "Label components",
                "On the cluster diagram, mark Application, Driver, `mongos`, config replica set, and three shards each drawn as a replica set.",
                "Clients talk to `mongos`, not directly to a random shard primary as the only entry. Config servers are separate from shards.",
            ),
            (
                "Label the two flows",
                "Draw query/write flow (app → mongos → targeted shard) and metadata flow (mongos ↔ config servers).",
                "Metadata is not application documents. `mongos` stores no collection data.",
            ),
        ],
        [
            "Config servers are not a shard of orders",
            "`mongos` is on the client path",
            "Each shard shows P/S members",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        8,
        "evaluate-shard-key-candidates",
        "Evaluate Shard-Key Candidates",
        "20 min",
        "Intermediate",
        "Score order-collection shard-key candidates from 1–5 for cardinality, distribution, write scale, targeting, hotspot risk, locality, and growth.",
        [
            (
                "Score six candidates",
                "Score `status` / `paymentStatus`, `createdAt`, `customerId`, hashed `customerId`, `{tenantId, orderId}`, `{customerId, createdAt}` for the seven criteria. Use `training_store.orders` as the mental model (few statuses, many customers, monotonic dates).",
                "status: low cardinality, hotspot, poor targeting. createdAt ranged: monotonic write hotspot. customerId: good targeting for history, possible tenant skew. hashed customerId: even writes, weak range locality. compound tenant+order: targeting if queries lead with tenant. customerId+createdAt: history queries target; ranged writes per customer are usually fine.",
            ),
            (
                "Recommend one for orders",
                "Pick one candidate for customer-order lookup plus high write volume. List two risks you still monitor.",
                "A defensible pick is `{ customerId: 1, createdAt: 1 }` or hashed `customerId` depending on whether range-by-date across customers matters. Risks: celebrity customers, scatter-gather global reports.",
            ),
        ],
        [
            "Low-cardinality status is rejected as a standalone key",
            "Monotonic ranged `createdAt` is flagged for hotspots",
            "The recommendation names a remaining risk",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        9,
        "targeted-or-scatter-gather",
        "Targeted or Scatter-Gather?",
        "15 min",
        "Intermediate",
        "Classify queries as single-shard targeted, multi-shard targeted, scatter-gather, or insufficient information.",
        [
            (
                "Assume ranged `{ customerId: 1, createdAt: 1 }`",
                "Classify: (A) `{ customerId: C101._id }`, (B) `{ customerId: C101._id, createdAt: { $gte: start } }`, (C) `{ paymentStatus: \"PAID\" }`, (D) `{ createdAt: { $gte: start } }`, (E) hashed-key range on `createdAt` if the key were hashed customerId.",
                "A targeted (one or few chunks for that customer). B targeted range within the customer prefix. C scatter-gather. D multi-shard or scatter depending on how dates map — usually many shards. E hashed customerId range on createdAt is scatter-gather.",
            ),
            (
                "Name one redesign",
                "If monthly global revenue must stay fast, is a better shard key the fix, or a different reporting design?",
                "Usually a different design: pre-aggregated reports, an analytics replica/cluster, or accepting scatter-gather for a rare job — not a shard key that hurts the OLTP path.",
            ),
        ],
        [
            "Non-shard-key filters are classified as scatter-gather",
            "Prefix equality can target",
            "Global reports are not assumed to be single-shard",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        10,
        "compare-ranged-and-hashed",
        "Compare Ranged and Hashed Sharding",
        "15 min",
        "Beginner",
        "Evaluate ranged versus hashed sharding for equality, range queries, sequential writes, locality, even distribution, and operational complexity.",
        [
            (
                "Fill the comparison",
                "For equality queries, range queries, sequential writes, geographic locality, even distribution, and operational complexity, mark which strategy is usually stronger (or “depends”).",
                "Equality: both can target. Range: ranged wins. Sequential writes: hashed usually spreads. Locality: ranged. Even distribution: hashed often easier. Complexity: similar conceptually; zones add complexity on ranged designs.",
            ),
            (
                "Pick for this workload",
                "Customer history by `customerId` plus newest-first `createdAt`, versus random UUID inserts with only equality lookups. Which strategy for each?",
                "History: ranged compound `{ customerId: 1, createdAt: 1 }`. UUID equality-only: hashed (or ranged UUID if already random).",
            ),
        ],
        [
            "Range queries are not claimed to be efficient on hashed keys",
            "Monotonic ranged keys are not recommended blindly",
            "Two workloads can justify two strategies",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        11,
        "diagnose-hotspot-risks",
        "Diagnose Hotspot Risks",
        "15 min",
        "Intermediate",
        "Review five hotspot patterns and propose a mitigation for each.",
        [
            (
                "Name the hotspot",
                "For timestamp shard key; dominant tenant; low-cardinality status; region zones with 90% of users in one region; celebrity product receiving most traffic — state what becomes hot.",
                "Timestamp: max chunk / one shard writes. Tenant: one shard’s CPU and storage. Status: few chunks ever receive writes. Zone: the popular region’s shards. Product: one document/range if productId is the key, or one catalog shard.",
            ),
            (
                "Propose mitigations",
                "Write one mitigation per case (hashed key, compound key, isolate tenant, split collection, cache, zone redesign, or not sharding that collection).",
                "Timestamp → hash or compound with high-cardinality leading field. Dominant tenant → isolate or further shard inside tenant. Status → do not use as key. Region skew → more shards in that zone or accept it. Celebrity product → cache, not a new shard key by itself.",
            ),
        ],
        [
            "Each pattern has a distinct mitigation",
            "Zones are not treated as a free locality win",
            "Low-cardinality keys are rejected",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "exercise",
        12,
        "design-a-scalable-deployment",
        "Design a Scalable Deployment",
        "25 min",
        "Intermediate",
        "Design availability, sharding, shard key, routing, and residency for a 24/7 order platform.",
        [
            (
                "Availability and placement",
                "Specify replica-set size, failure-domain placement, and how Canada vs Europe data-residency could be met (zones vs separate clusters). Assume 24/7 order writes.",
                "At least three data-bearing voters across failure domains. Residency: zoned sharding on a residency field **or** separate regional clusters — not an afterthought on `createdAt`.",
            ),
            (
                "Orders versus products",
                "State which collection you shard first, a candidate order shard key, which queries stay targeted, and which monthly global reports become scatter-gather.",
                "Orders first under write growth. Products often wait. Targeted: customer/tenant order history. Scatter-gather: monthly global revenue unless pre-aggregated.",
            ),
        ],
        [
            "Standalone is rejected for production",
            "Residency is explicit",
            "Global reports are costed as scatter-gather or redesigned",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        "lab",
        1,
        "verify-replica-set-health",
        "Verify Replica-Set Health",
        "20 min",
        "Beginner",
        "Inspect replica-set name, member states, health, votes, and replication timestamps, then write a short health report.",
        [
            (
                "Confirm you are on a replica set",
                "Connect with the replica-set / Atlas URI, then run:\n\n"
                + js(
                    """rs.status()
rs.conf()"""
                ),
                "A replica-set name, one `PRIMARY`, one or more `SECONDARY` members, `health: 1` on reachable members. If you see a standalone error, stop and switch URI.",
            ),
            (
                "Record identity and votes",
                "From `rs.status()` and `rs.conf()`, write: set name, primary host, secondary hosts, each member’s `votes` and `priority`. Note any arbiter.",
                "A table of members with state, votes, and priority. Atlas typically shows three data-bearing members and no arbiter.",
            ),
            (
                "Record replication timestamps",
                "Run:\n\n"
                + js("rs.printSecondaryReplicationInfo()"),
                "Each secondary shows how far behind the primary (often 0–2 seconds when idle). Record the values even if they are zero.",
            ),
            (
                "Write the health report",
                "One short paragraph: is a primary present? Is a majority reachable? Is lag concerning? Any config smell (arbiter-only durability, priority 0 on the only nearby member)?",
                "A report that would make sense to another operator. No unexplained red states.",
            ),
        ],
        [
            "Primary is identified",
            "Voting configuration is recorded",
            "Lag is measured, not guessed",
            "Concerns are listed even if the set is healthy",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        2,
        "write-and-verify-replication",
        "Write and Verify Replication",
        "20 min",
        "Beginner",
        "Insert a test document through the replica set, confirm acknowledgment, and observe it after replication.",
        [
            (
                "Insert through the replica-set URI",
                "Use the replica-set connection string (not a single secondary host). Run:\n\n"
                + js(
                    """use training_store
db.repl_lab.insertOne({
  lab: "7.2",
  note: "replication check",
  createdAt: new Date()
})"""
                ),
                "`acknowledged: true` and an `_id`. You are talking to the current primary.",
            ),
            (
                "Read it back on primary preference",
                "Run:\n\n"
                + js(
                    """db.repl_lab.find({ lab: "7.2" })
rs.printSecondaryReplicationInfo()"""
                ),
                "The document is visible. Lag remains small after a single insert.",
            ),
            (
                "Discuss secondary inspection",
                "If the instructor provides a safe secondary read (read preference `secondary` in a disposable cluster), run the same `find`. Otherwise write why secondary reads can be stale even when this insert already appears.",
                "Either the document is visible on a secondary, or a written explanation of replication delay and read preference.",
            ),
            (
                "Remove the temporary record",
                "Run:\n\n"
                + js('db.repl_lab.deleteMany({ lab: "7.2" })'),
                "`deletedCount` matches what you inserted. Collection may remain empty.",
            ),
        ],
        [
            "Write used a replica-set URI",
            "Acknowledgment was recorded",
            "Temporary document was deleted",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        3,
        "observe-election-and-failover",
        "Observe Election and Failover",
        "25 min",
        "Intermediate",
        "Watch a controlled step-down, record the interruption, identify the new primary, and confirm the old primary returns as a secondary.",
        [
            (
                "Record the current primary",
                "On the **instructor disposable replica set**, run `rs.status()` and write the current primary host. Do **not** run this lab against a shared Atlas class cluster unless the instructor confirms it is disposable.",
                "One hostname/port labeled PRIMARY.",
            ),
            (
                "Observe the step-down",
                "Watch the instructor run a controlled `rs.stepDown()` (or stop the primary process). Note the time writes pause. Then run `rs.status()` again.",
                "A different member is PRIMARY, or you recorded the election window from the instructor’s screen if students cannot reconnect yet.",
            ),
            (
                "Verify writes resume",
                "After a primary exists, insert a one-document probe and read it back. Then confirm the former primary’s state when it rejoins.",
                "Insert succeeds. Former primary is SECONDARY (not still claiming PRIMARY).",
            ),
            (
                "Document application behavior",
                "Write what a well-behaved driver should do: rediscover topology, retry eligible operations, surface errors if retry is exhausted.",
                "Notes mention replica-set URI, transient errors, and retry — not “the application must be restarted by hand.”",
            ),
        ],
        [
            "Old and new primary are recorded",
            "Write pause is acknowledged",
            "Former primary rejoins as secondary",
            "No student stepped down a shared cluster without permission",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        4,
        "test-read-preference-and-write-concern",
        "Test Read Preference and Write Concern",
        "25 min",
        "Intermediate",
        "Compare serving members for primary versus secondary-preferred reads and perform writes with assigned write concerns.",
        [
            (
                "Primary read",
                "In `mongosh` connected to the replica set, run a `find` with default (primary) read preference on `training_store.products` and note which member you are on:\n\n"
                + js(
                    """db.hello()
db.products.find({ sku: "L100" }).limit(1)"""
                ),
                "`db.hello()` shows `isWritablePrimary: true` (or equivalent) for the default connection. The product document returns.",
            ),
            (
                "Secondary-preferred read (if permitted)",
                "If the instructor allows, start a second shell with read preference `secondaryPreferred` (connection string `readPreference=secondaryPreferred` or `db.getMongo().setReadPref(\"secondaryPreferred\")`) and run the same find. Compare `db.hello()`.",
                "You either hit a secondary (`secondary: true`) or fell back to primary. Staleness risk is written down even if data matched.",
            ),
            (
                "Compare write concerns",
                "Insert two probe documents with different write concerns:\n\n"
                + js(
                    """db.repl_lab.insertOne(
  { lab: "7.4", wc: "majority" },
  { writeConcern: { w: "majority", wtimeout: 5000 } }
)
db.repl_lab.insertOne(
  { lab: "7.4", wc: "1" },
  { writeConcern: { w: 1, wtimeout: 5000 } }
)"""
                ),
                "Both acknowledge in a healthy set. Record approximate duration if the shell shows it. Majority should not be described as “always slower enough to skip.”",
            ),
            (
                "Map to business operations",
                "State which pair of settings you would use for payment confirmation versus product-catalog browsing. Delete probes: `db.repl_lab.deleteMany({ lab: \"7.4\" })`.",
                "Payment: primary reads + majority writes. Catalog: primaryPreferred/nearest and `w: majority` still preferred in production; secondary reads only if staleness is acceptable.",
            ),
        ],
        [
            "Primary versus secondary-preferred serving member is compared",
            "Two write concerns were attempted",
            "Business mapping is written",
            "Probe documents were removed",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        5,
        "investigate-replication-lag",
        "Investigate Replication Lag",
        "20 min",
        "Intermediate",
        "Compare replication timestamps, consider secondary load and oplog window, and propose corrective actions.",
        [
            (
                "Capture member optimes",
                "Run:\n\n"
                + js(
                    """rs.status()
rs.printSecondaryReplicationInfo()"""
                ),
                "A table of members and lag. In a quiet training set, lag may be ~0. Still record it as a baseline.",
            ),
            (
                "Inspect oplog window",
                "Run:\n\n"
                + js(
                    """use local
db.oplog.rs.stats()
rs.printReplicationInfo()"""
                ),
                "You can state that the oplog is a capped collection in `local.oplog.rs` and note size / time window if printed. Command names can vary slightly by version — record what your shell returned.",
            ),
            (
                "Review causes against this lab",
                "If the instructor injected lag (heavy secondary query, paused member), list the likely cause. If not, write the five causes you would check in production: disk, CPU, network, write burst, secondary workload.",
                "A cause list tied to evidence, not a guess-only paragraph.",
            ),
            (
                "Propose actions",
                "Write two actions you would take if lag were growing (for example 30s, then minutes) and one action you would **not** take first (panic rebuild).",
                "First: reduce secondary load / check disk. Not first: delete the replica and hope.",
            ),
        ],
        [
            "Timestamps were compared",
            "Oplog is identified as the replication log",
            "Corrective actions are ordered sanely",
        ],
    )
)

GUIDES.append(
    guide(
        "lab",
        6,
        "inspect-sharded-cluster-components",
        "Inspect Sharded-Cluster Components",
        "20 min",
        "Beginner",
        "Identify mongos, shards, shard replica sets, the config replica set, sharded collections, and shard keys.",
        [
            (
                "Connect to mongos",
                "Using the instructor `mongos` URI (or the sample `sh.status()` the instructor pastes), run:\n\n"
                + js("sh.status()"),
                "Output lists shards, a config server replica set, and optionally sharded databases/collections. On a replica set without sharding, this command is not the right topology — use the sample output instead.",
            ),
            (
                "List shards and config",
                "Write the shard names and the config replica-set name. Note that each shard should itself be a replica set in production.",
                "At least one shard id and a config RS name are recorded.",
            ),
            (
                "List sharded collections",
                "From `sh.status()` (or `db.getSiblingDB(\"config\").collections.find()` on mongos), record each sharded collection and its shard key.",
                "A table: database.collection → shard key. Empty is acceptable on a fresh training cluster.",
            ),
            (
                "Describe data placement",
                "If chunks/ranges are shown, note whether they look even. If none, write “unsharded / not yet chunked.”",
                "A one-sentence distribution comment.",
            ),
        ],
        [
            "`mongos` is distinguished from shard mongod",
            "Config servers are named",
            "Shard keys are copied from status, not invented",
        ],
        sharded=True,
    )
)

GUIDES.append(
    guide(
        "lab",
        7,
        "shard-a-training-collection",
        "Shard a Training Collection",
        "25 min",
        "Intermediate",
        "On a disposable sharded cluster, create a supporting index, shard a training collection, insert sample documents, and inspect the key.",
        [
            (
                "Use only a disposable cluster",
                "Confirm with the instructor that this is a throwaway sharded cluster. Create a training database namespace they specify (example `training_shard`).",
                "You are not connected to the shared Atlas class replica set as if it were mongos.",
            ),
            (
                "Create the shard-key index and enable sharding",
                "Commands vary by MongoDB version. A typical training sequence:\n\n"
                + js(
                    """use training_shard
db.orders_lab.createIndex({ customerId: 1, createdAt: 1 })
sh.enableSharding("training_shard")
sh.shardCollection(
  "training_shard.orders_lab",
  { customerId: 1, createdAt: 1 }
)"""
                )
                + "\nIf `enableSharding` is unnecessary on your version, follow the instructor’s exact commands.",
                "Collection is sharded. Errors about existing keys or already-sharded collections are resolved with the instructor, not by dropping unknown data.",
            ),
            (
                "Insert sample documents",
                "Insert several documents with different `customerId` values and `createdAt` dates. Then `sh.status()` and confirm the shard key.",
                "Documents insert. Status shows `{ customerId: 1, createdAt: 1 }` (or the assigned key).",
            ),
            (
                "Inspect distribution",
                "Note chunk/range counts per shard. Small samples may still sit on one shard — write that down; do not force-balance unless instructed.",
                "A distribution note that does not assume instant perfect balance on a handful of documents.",
            ),
        ],
        [
            "Supporting index exists",
            "Shard key is confirmed in status",
            "Sample inserts succeeded",
            "No shared classroom cluster was sharded without permission",
        ],
        sharded=True,
    )
)

GUIDES.append(
    guide(
        "lab",
        8,
        "analyze-query-routing",
        "Analyze Query Routing",
        "25 min",
        "Intermediate",
        "Explain targeted versus scatter-gather plans for shard-key equality, ranges, partial compound keys, and non-key filters.",
        [
            (
                "Full shard-key equality",
                "On the sharded training collection, run `explain` for a find that includes the full shard key (or leading equality + range the instructor specifies). Record `shards` / `winningPlan` targeting.",
                "The plan indicates one (or a small set of) targeted shards, not all shards, when the key is present.",
            ),
            (
                "Non-shard-key equality",
                "Explain a find on `paymentStatus` (or another non-key field) only. Record whether mongos scatters.",
                "Scatter-gather / query all shards is expected.",
            ),
            (
                "Partial compound key and global aggregation",
                "Explain a filter that uses only the trailing field of a compound key, and a simple `$count` / `$group` with no shard-key `$match`. Record merge behavior.",
                "Trailing-only predicates usually cannot target. Aggregations without a targeted `$match` merge across shards.",
            ),
            (
                "Summarize for the app team",
                "Write which of the five query shapes (full key, key range, partial compound, non-key, global agg) must stay rare in the hot path.",
                "Non-key finds and global aggregations are called out as expensive when frequent.",
            ),
        ],
        [
            "At least two explain outputs are recorded",
            "Scatter-gather is identified by evidence",
            "Hot-path advice is written",
        ],
        sharded=True,
    )
)

GUIDES.append(
    guide(
        "lab",
        9,
        "review-chunk-distribution",
        "Review Chunk Distribution",
        "20 min",
        "Beginner",
        "Examine data and range distribution, balancer state, zones, and hotspot indicators, then write a distribution-health assessment.",
        [
            (
                "Inspect status",
                "Run `sh.status()` (or instructor sample). Record shards, chunk/range counts, and whether the balancer is enabled/running.",
                "A small table: shard → chunk count. Balancer state is noted.",
            ),
            (
                "Look for imbalance",
                "If one shard owns most ranges, write whether that is expected (new cluster, hashed vs ranged, tiny dataset) or a hotspot smell.",
                "An interpretation, not only raw counts. Tiny training data often looks “imbalanced.”",
            ),
            (
                "Zones and hotspots",
                "Note any tags/zones. List hotspot indicators: monotonic key, jumbo chunks, one shard’s data size far ahead.",
                "Zones listed or “none.” At least one hotspot indicator is considered.",
            ),
            (
                "Write the assessment",
                "Five to eight sentences: healthy / watch / action. Include what you would monitor next week.",
                "A short distribution-health assessment suitable to paste into an ops channel.",
            ),
        ],
        [
            "Balancer state is recorded",
            "Imbalance is interpreted in context",
            "A written assessment exists",
        ],
        sharded=True,
    )
)

GUIDES.append(
    guide(
        "lab",
        10,
        "integrated-availability-and-scaling",
        "Integrated Availability and Scaling Challenge",
        "40–45 min",
        "Intermediate",
        "Design replication, sharding, shard key, routing, read/write settings, failover, and monitoring for the e-commerce order platform.",
        [
            (
                "Collections and topology",
                "Decide which collections stay replica-set only versus shard candidates. Design a three-member (or more) replica-set topology per shard with failure domains.",
                "Orders are the first shard candidate under write growth. Products/customers often remain unsharded initially. Each shard is a replica set.",
            ),
            (
                "Shard key and routing",
                "Select a candidate order shard key. Compare ranged, hashed, and compound. List targeted queries vs unavoidable scatter-gather reports.",
                "A scored key (not `paymentStatus`). Customer history targeted. Monthly global revenue scatter-gather or redesigned.",
            ),
            (
                "Read/write and failover",
                "Recommend read preference and write concern for order placement vs catalog browse. Describe what the app sees during a primary election.",
                "Order placement: primary + majority. Catalog may use primaryPreferred. Election: brief write errors, driver rediscovery, retries.",
            ),
            (
                "Monitoring",
                "List monitoring for lag, oplog window, chunk distribution, balancer, mongos availability, and CSRS health.",
                "A checklist with owners/thresholds sketched, not “we will watch the dashboard.”",
            ),
        ],
        [
            "Replication and sharding are both addressed",
            "Shard-key risks are explicit",
            "Settings differ by operation",
            "Monitoring covers replica set and cluster",
        ],
        discussion=True,
        extra="""## Scenario (keep this visible)

E-commerce requires continuous order processing, server-failure resilience, customer-order lookup, high order-write volume, regional data placement, and global sales reporting.
""",
    )
)

GUIDES.append(
    guide(
        "exercise",
        13,
        "scale-the-order-platform",
        "Scale the E-Commerce Order Platform",
        "30–45 min",
        "Intermediate",
        "Produce an availability design, sharding decision, shard-key comparison, query-routing analysis, and operational plan for a growing order platform currently on one standalone server.",
        [
            (
                "Availability design",
                "Specify member count, roles, failure-domain placement, election behavior, read preference, write concern, and monitoring. Start from today’s standalone server.",
                "Move to a replica set of at least three data-bearing voters across failure domains. Default app reads primary; writes majority. Monitor lag, elections, disk, and connections.",
            ),
            (
                "Sharding decision and key comparison",
                "Say whether sharding is required **today** vs after evidence. Which collection first? Compare `status`, `createdAt`, `customerId`, hashed `customerId`, `{tenantId, orderId}`, `{tenantId, createdAt}`.",
                "Do not shard before measuring. Orders first if a replica set cannot hold write/storage growth. Reject `status`. Flag monotonic `createdAt`. Prefer a customer/tenant-leading key.",
            ),
            (
                "Routing and operations",
                "Classify: lookup by full shard key; customer-order history; recent orders across all customers; monthly global revenue; tenant-specific reporting. Then list failover tests, backups, lag, distribution, balancer, app retries, and capacity thresholds.",
                "Full key and customer history: targeted if the key leads with customer/tenant. Recent global and monthly revenue: scatter-gather. Tenant reports: targeted if tenant is the leading field. Ops plan includes backups **and** replica sets (not either/or).",
            ),
        ],
        [
            "Standalone is replaced for production availability",
            "Sharding is evidence-based",
            "Six key candidates are compared",
            "Query routing and an ops plan exist",
        ],
        discussion=True,
        extra="""## Current situation

- One standalone MongoDB server
- Increasing order volume
- Maintenance downtime
- Customer-order queries and recent-order dashboards
- Global analytical reports
- Several large enterprise tenants
- Continuous operation required
""",
    )
)


def write_all() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for kind, num, slug, title, time, typ, objective, md in GUIDES:
        prefix = "exercise" if kind == "exercise" else "lab"
        path = OUT / f"{prefix}-7.{num}-{slug}.md"
        path.write_text(md.strip() + "\n", encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)} ({typ}, {time}) — {title}")
    print(f"Done. {len(GUIDES)} lab guides.")


if __name__ == "__main__":
    write_all()

"""Diagram lists and ChatGPT prompts for Mastering MongoDB.

Same visual contract as MD287 new PPT diagrams: 16:9 HD, diagram only,
navy / crimson / teal / sage, training_store as the standing case study.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
TITLES = json.loads((HERE / "titles.json").read_text(encoding="utf-8"))

PROMPT = """Generate ONE 16:9 HD (1920×1080) architecture diagram image. Output ONLY the diagram.

Topic: {title}

Case study (use this domain on every diagram, do not switch examples):
training_store e-commerce: products, customers, orders, reviews.
MongoDB hierarchy: database → collection → document → field.
Clients: mongosh and MongoDB Compass. Server: mongod.

What the diagram must show:
{show}

STRICT RULES:
- Draw ONLY the architecture diagram. Nothing else.
- No slide header bar, no course name, no module badge, no breadcrumb, no page number.
- No footer, no copyright, no watermark, no "ChatGPT", no takeaway bar, no side rail.
- No extra checklist panels, no "key concepts" boxes, no speaker notes, no logos.
- Do not put a large title banner across the top. The PowerPoint slide already has the title. Small labels on boxes and arrows are required.
- Solid white background. No transparency.
- Clean enterprise teaching diagram: labeled boxes, arrows, icons inside components. Readable sans-serif text from 10 feet.
- Flat professional colors: navy #0B1F3A, crimson #B42318, teal #0F766E, sage #2F6F5E, plus warm neutrals. Soft contact shadows only.
- No 3D isometric city, no photoreal people, no purple-pink AI gradients, no glow, no comic toy towns.
- One idea. One diagram. 16:9 HD PNG. Labels must not overlap.
"""

# Hand-written shows for Module 1 — same density as the MD287 Module 1 list.
MODULE01_SHOW: dict[str, str] = {
    "The Changing Application Data Landscape": (
        "Left-to-right journey of three data shapes, connected by arrows: "
        "(1) Structured — tables, fixed schema, SKU/price/qty; "
        "(2) Semi-structured — nested JSON product with specs and tags; "
        "(3) Rapidly changing — variants and new attributes. "
        "A caption under the row: modern apps mix all three. Do not add a fourth stage."
    ),
    "Structured vs Semi-Structured vs Unstructured": (
        "Three equal columns. LEFT Structured: rows and columns, example SKU/price/quantity. "
        "MIDDLE Semi-structured: nested JSON-like product + specs + tags. "
        "RIGHT Unstructured: images, logs, video with no fixed fields. "
        "Same visual weight. No extra columns."
    ),
    "Where Relational Databases Work Well": (
        "A clean relational model for training_store: customers, orders, order_items, products "
        "as tables linked by primary/foreign keys. Application box above. "
        "Emphasize well-known joins and declared schema. Not a NoSQL diagram."
    ),
    "Challenges with Traditional Relational Models": (
        "One complete order split across many tables: customers, addresses, orders, order_items, "
        "payments. Arrows reconstruct the order through JOIN JOIN JOIN. "
        "Make the reconstruction cost obvious. No MongoDB document in this diagram."
    ),
    "What Does NoSQL Mean?": (
        "Simple visual: Not Only SQL. A SQL table on the left and four NoSQL model icons "
        "on the right (document, key-value, column-family, graph). "
        "Not a replacement banner — both exist. Short labels only."
    ),
    "Why Organizations Adopt NoSQL": (
        "Hub 'Application growth' with four equal surrounding nodes: Flexible schema, "
        "Horizontal scale, Availability, Faster delivery. Hub-and-spoke. No extra nodes."
    ),
    "The Four Major NoSQL Database Types": (
        "2×2 equal cards: Document (JSON-like aggregates), Key-Value (opaque value by key), "
        "Column-family (wide rows / columns), Graph (nodes and relationships). "
        "One example each from commerce if space allows. Equal visual weight."
    ),
    "Document Databases": (
        "One product document as a labeled nested object: _id, sku, name, price, tags[], "
        "specifications{}. Show that related data lives together in one document. "
        "training_store products collection."
    ),
    "Key-Value Databases": (
        "Simple key → value store. Keys like session:abc, cart:42. Values are opaque blobs. "
        "Lookup by exact key only. Contrast is implied, not a second panel of MongoDB."
    ),
    "Column-Family Databases": (
        "Wide-row visual: row key (customerId) with sparse column families "
        "(profile, orders, activity). Empty cells allowed. Short labels."
    ),
    "Graph Databases": (
        "Small graph: Customer —PURCHASED→ Order —CONTAINS→ Product, plus Product —RELATED→ Product. "
        "Nodes and relationship labels. training_store names. Not a table."
    ),
    "Choosing the Right Database Model": (
        "Decision visual: workload question in the center with four outgoing arrows to "
        "Document / Key-Value / Column-family / Graph. Short matching criteria on each arrow. "
        "One idea: pick the model from the access pattern."
    ),
    "Database Selection Decision Flow": (
        "Left-to-right decision flow: Access pattern → Relationships? → Query style → "
        "Scale need → Chosen model. End boxes: Relational, Document, Key-Value, Graph. "
        "One path with branches, not a paragraph of text."
    ),
    "Introducing MongoDB": (
        "MongoDB as a document database in the NoSQL landscape. Center: MongoDB. "
        "Around it: documents, collections, flexible schema, indexes, replica sets. "
        "Hub-and-spoke. Short labels. Not a full architecture."
    ),
    "MongoDB Data Hierarchy": (
        "Vertical stack, largest to smallest: Deployment → Database (training_store) → "
        "Collection (products) → Document → Field. One column. Clear containment."
    ),
    "Relational-to-MongoDB Terminology": (
        "True side-by-side mapping table as cards. LEFT relational: Database, Schema, Table, "
        "Row, Column, Primary key, JOIN. RIGHT MongoDB: Database, implicit, Collection, "
        "Document, Field, _id, embed/reference. VS divider. Same order both sides."
    ),
    "From Rows to Documents": (
        "LEFT: normalized tables customers + orders + order_items. RIGHT: one Order document "
        "with embedded items[] and customer snapshot. Arrow from left to right labeled "
        "'aggregate'. Same order, two shapes."
    ),
    "Understanding BSON Documents": (
        "JSON text on the left becoming BSON typed fields on the right: ObjectId, Date, "
        "Decimal128, Boolean, Array, Embedded document. Show types, not a binary dump."
    ),
    "Anatomy of a MongoDB Document": (
        "One product document with callouts on every shape: _id ObjectId, sku String, "
        "price Decimal128, active Boolean, createdAt Date, tags Array, specifications embedded. "
        "training_store product. Labels must not overlap."
    ),
    "Flexible Schema Within a Collection": (
        "One products collection containing two valid documents side by side: a Laptop with "
        "cpu/ram specs and a Book with isbn/pages. Same collection, different fields. "
        "Caption: schema follows the product, not a single table shape."
    ),
    "Embedding vs Referencing Preview": (
        "Two equal panels. LEFT Embedding: Customer document contains addresses[]. "
        "RIGHT Referencing: Order document stores customerId pointing at customers. "
        "VS divider. training_store names. No extra patterns."
    ),
    "MongoDB Architecture Overview": (
        "Client (mongosh / Compass / driver) → mongod → storage engine → data files. "
        "Optional replica-set silhouette in the background, not a full HA deep-dive. "
        "One request path. Short labels."
    ),
    "MongoDB Deployment Options": (
        "Three equal options: Local mongod, Container (Docker), Managed cloud (Atlas-style). "
        "Each with a one-line use. Same training_store app connecting to each. No winner banner."
    ),
    "How a MongoDB Request Is Processed": (
        "Left-to-right: Client → Network → mongod → Query planner / index → Fetch documents → "
        "Result to client. One path. products.find example implied by labels, not a code dump."
    ),
    "Core MongoDB Features": (
        "Hub MongoDB with six surrounding feature nodes: Flexible documents, Indexes, "
        "Aggregation, Replication, Sharding, Drivers. Equal weight. Hub-and-spoke."
    ),
    "MongoDB Use Cases": (
        "Six use-case cards around MongoDB: Product catalog, Customer profile, Order history, "
        "Content, IoT/events, Personalization. training_store catalog highlighted. Short labels."
    ),
    "When to Use MongoDB": (
        "A fit checklist as five equal 'yes' cards: varied attributes, data accessed together, "
        "evolving schema, document aggregates, horizontal growth. Green/teal positive cards. "
        "No anti-pattern panel on this diagram."
    ),
    "When MongoDB May Not Be the Best Choice": (
        "Five caution cards: heavy multi-row transactions across many entities, "
        "strict tabular reporting, tiny rows with no aggregate, graph-first traversal, "
        "pure key-value cache. Crimson/navy caution styling. Not a 'never use MongoDB' poster."
    ),
    "Scenario: Modernizing an Application": (
        "Left-to-right modernization: Relational catalog (many JOINs) → Product document model → "
        "MongoDB products collection → Same catalog API. training_store. One path."
    ),
    "Module Summary": (
        "Concept map: Why NoSQL → Four models → MongoDB documents → Hierarchy → "
        "Embed vs reference → Architecture. Hub 'Module 1'. Short labels. One map, no paragraphs."
    ),
}

MODULE02_SHOW: dict[str, str] = {
    "MongoDB Environment Components": (
        "Four components in a row: mongod (server), data files, mongosh (shell), Compass (GUI). "
        "Arrows from both clients into mongod, mongod into data files. training_store. "
        "No cloud or containers in this diagram."
    ),
    "Environment Layers": (
        "Vertical stack: OS / host → mongod process → databases → collections → documents. "
        "Clients (mongosh, Compass) attach from the side to mongod. Clear layers."
    ),
    "MongoDB Deployment Options": (
        "Three equal cards: Local mongod, Docker container, Managed cloud. "
        "Same training_store app connecting to each. One-line use under each. No winner."
    ),
    "Local MongoDB Deployment": (
        "Laptop/host box containing mongod + data directory + mongosh on localhost:27017. "
        "One machine. Label bindIp localhost. Simple local picture."
    ),
    "Managed Cloud Deployment": (
        "Developer laptop on the left. Secure URI over TLS to a managed MongoDB cluster "
        "(replica-set silhouette) in the cloud. Atlas-style. No credentials printed."
    ),
    "Cloud Provisioning Process": (
        "Left-to-right: Create project → Deploy cluster → Network access / IP allowlist → "
        "Database user → Connection string → Connect from mongosh. One path."
    ),
    "Containerized MongoDB": (
        "Docker/container box running mongod, volume mounted for /data/db, port 27017 published "
        "to the host. mongosh on the host talks to localhost:27017. Short labels."
    ),
    "Self-Managed Server": (
        "Linux server box: mongod as a service, config file, data dir, log dir, firewall port 27017. "
        "Operator owns the VM. Not Atlas."
    ),
    "Local vs. Managed Cloud": (
        "True side-by-side. LEFT local: you run mongod, you own files, localhost. "
        "RIGHT managed: vendor runs cluster, TLS URI, backups included. VS divider."
    ),
    "Choosing a Deployment Option": (
        "Decision flow: Classroom laptop? → Local/Docker. Shared team / production-like? → "
        "Managed cloud. Need OS control? → Self-managed. Three end boxes. Short labels."
    ),
    "MongoDB Installation Workflow": (
        "Install mongod → create data and log dirs → start service → mongosh ping → Compass connect → "
        "insert test document. One left-to-right path."
    ),
    "MongoDB Server and Client Tools": (
        "Center mongod. Three clients around it: mongosh, Compass, application driver. "
        "All talk to the same port 27017. Hub-and-spoke."
    ),
    "`mongod` vs. `mongosh`": (
        "LEFT mongod: the database server process, stores data. "
        "RIGHT mongosh: the shell client, sends commands. Arrow client → server. VS divider."
    ),
    "Three Clients, One Deployment": (
        "One mongod in the center. Three equal clients: mongosh, Compass, Node/Java driver. "
        "All read/write the same training_store. Same data, three tools."
    ),
    "MongoDB Configuration File": (
        "A mongod.conf card with four short keys only: storage.dbPath, systemLog.path, "
        "net.port, net.bindIp. Arrow into a running mongod. No wall of YAML."
    ),
    "Data and Log Directories": (
        "Host disk: /data/db (WiredTiger files) and /var/log/mongodb/mongod.log. "
        "mongod reads/writes data dir and appends the log. Two folders, one process."
    ),
    "Data and Log Flow": (
        "Client write → mongod → data files; same mongod → log file. "
        "Two outgoing arrows from mongod. Short labels."
    ),
    "Starting and Stopping MongoDB": (
        "Service lifecycle: start mongod → listening 27017 → clients connect. "
        "Stop: clients disconnect → mongod clean shutdown → port closed. Two small sequences."
    ),
    "Startup and Shutdown": (
        "LEFT startup: config → open dbPath → listen 27017 → ready. "
        "RIGHT shutdown: drain → flush → close files → exit. VS or two columns."
    ),
    "Verifying the MongoDB Service": (
        "Checklist visual as a flow: port 27017 open → mongosh hello → db.runCommand ping → "
        "show dbs. Green pass marks. One verification path."
    ),
    "Hosts and Ports": (
        "Anatomy: host (localhost or cluster host) + port 27017. "
        "Arrow from Compass/mongosh URI into that host:port. Short labels."
    ),
    "Localhost vs. Remote Connection": (
        "LEFT localhost: client and mongod on one machine, 127.0.0.1:27017. "
        "RIGHT remote: client laptop → TLS → remote mongod host:27017. VS divider."
    ),
    "Understanding Connection Strings": (
        "One URI bar labeled in pieces: mongodb:// user:auth @ host:port / database ? options. "
        "Callouts on each piece. No giant text block."
    ),
    "Standard Connection-String Format": (
        "mongodb://user:pass@host1:27017,host2:27017/training_store?authSource=admin "
        "shown as labeled segments. Replica-set hint optional. Callouts, not a screenshot."
    ),
    "DNS Seed-List Connection Strings": (
        "mongodb+srv:// URI. DNS SRV lookup → several mongod hosts. "
        "Client on the left, DNS in the middle, cluster on the right. One path."
    ),
    "Connection Establishment": (
        "Client → TCP connect → TLS (if any) → auth → hello handshake → ready session. "
        "Left-to-right. Short stage labels."
    ),
    "Connecting with `mongosh`": (
        "Terminal-style: mongosh \"mongodb://localhost:27017\" → connected → "
        "use training_store → db.products.findOne(). Three small steps, not a code dump wall."
    ),
    "Connecting with MongoDB Compass": (
        "Compass New Connection → paste URI → Connect → see training_store databases/collections. "
        "GUI flow. Four boxes."
    ),
    "Databases and Collections": (
        "training_store database containing four collections: products, customers, orders, reviews. "
        "Containment diagram. No documents expanded."
    ),
    "Creating Your First Database": (
        "use training_store → database appears after first write. "
        "Empty name → first insert creates it. Two-step visual."
    ),
    "Creating Your First Collection": (
        "db.createCollection('products') OR first insert into db.products. "
        "Two paths into the same products collection box."
    ),
    "Inserting Your First Document": (
        "mongosh → insertOne product {sku, name, price} → products collection gains one document. "
        "Left-to-right write path."
    ),
    "Automatic `_id` Generation": (
        "Insert without _id → MongoDB assigns ObjectId → document stored with _id. "
        "Show the generated _id callout. One path."
    ),
    "Retrieving and Verifying Data": (
        "insertOne → find / findOne → Compass refresh shows the same product. "
        "Write then read verification. One loop."
    ),
    "Same Data Through Two Clients": (
        "One products document in mongod. LEFT mongosh findOne. RIGHT Compass document view. "
        "Same sku. Two clients, one document."
    ),
    "Basic Authentication Concepts": (
        "User + password → authenticate against authSource → authorized roles → allowed actions. "
        "Simple identity chain into mongod. Not a full RBAC deep-dive."
    ),
    "Layered Connection Security": (
        "Layers: network / TLS → authentication → authorization (roles) → encryption at rest. "
        "Vertical stack around mongod. Short labels."
    ),
    "Safe Credential Practices": (
        "LEFT anti-pattern: password in a chat screenshot / plaintext script (crimson). "
        "RIGHT: env var / password prompt / secret store (teal). VS divider."
    ),
    "Common Installation Problems": (
        "Four problem cards pointing at mongod: wrong dbPath, port in use, service not started, "
        "bindIp mismatch. Center mongod. Short labels."
    ),
    "Common Connection Problems": (
        "Four client-side failures: connection refused, timeout, auth failed, IP not allowed. "
        "Client → X → mongod. Mark the break."
    ),
    "Troubleshooting Workflow": (
        "Symptom → Is mongod running? → Port / bindIp? → Auth? → Network/TLS? → Fix. "
        "Left-to-right diagnostic path with a pass/fail gate."
    ),
    "Environment Readiness Checklist": (
        "Five equal ready cards: mongod up, ping ok, auth works, Compass connected, "
        "test write/read in training_store. Green checks. Not a paragraph list."
    ),
    "Module Summary": (
        "Concept map hub 'Module 2': Deploy → Install mongod → Connect (URI / mongosh / Compass) → "
        "First write/read → Secure and troubleshoot. Short labels."
    ),
}


def show_for(module: str, title: str) -> str:
    overrides = {
        "01": MODULE01_SHOW,
        "02": MODULE02_SHOW,
    }
    override = overrides.get(module, {}).get(title)
    if override:
        return override
    t = title.lower()
    bits = [
        f"Clean enterprise teaching diagram of: {title}.",
        "Use training_store (products, customers, orders, reviews) whenever a domain example helps.",
        "Short labels on boxes and arrows. One idea only.",
    ]
    if " vs" in t or "versus" in t or " vs." in t:
        bits.append(
            "True side-by-side comparison. LEFT vs RIGHT. Clear VS divider. "
            "Same example on both sides. Equal visual weight."
        )
    elif any(w in t for w in ("flow", "workflow", "sequence", "process", "pipeline")):
        bits.append(
            "Left-to-right flow. Labeled stages connected by arrows. One path. "
            "No extra branches unless the topic is troubleshooting."
        )
    elif any(w in t for w in ("architecture", "overview", "map", "components", "layers")):
        bits.append(
            "Architecture / component diagram. Labeled boxes, arrows, containment. "
            "Readable from 10 feet."
        )
    elif "decision" in t or "choosing" in t or "choose" in t:
        bits.append(
            "Decision flow or decision tree. Question → criteria → outcome boxes. "
            "Short labels, not paragraphs."
        )
    elif "anatomy" in t or "anatomy" in t:
        bits.append("Labeled anatomy with callouts on each part. No overlapping labels.")
    elif "troubleshoot" in t or "problem" in t or "failure" in t:
        bits.append(
            "Diagnostic flow: symptom → layer → cause → fix. Mark the failure point. "
            "One troubleshooting path."
        )
    elif "anti-pattern" in t or "antipattern" in t or "mistakes" in t:
        bits.append(
            "LEFT anti-pattern (crimson) vs RIGHT correct pattern (teal). VS divider."
        )
    return " ".join(bits)


def diagrams_for(module: str | int) -> list[dict]:
    key = f"{int(module):02d}"
    titles = TITLES[key]
    items = []
    for i, title in enumerate(titles, start=3):
        items.append({"slide": i, "title": title, "show": show_for(key, title)})
    return items

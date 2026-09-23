#!/usr/bin/env python3
"""Build the new-content Module 2 deck: Installation and Setup.

Content comes from scripts/module02_content_source.md, the Module 2 manifest,
the official Exercises 2.1-2.4, the Day 1 Lab 1 guide and the training_store
sample database. Styling reuses the house kit through mdb_deck_kit (read-only):
title block, red/black rail, footer, page numbers, key-takeaway bar, fonts and
colours. Hand-drawn visuals are native, editable PowerPoint shapes; concept
diagrams come from scripts/new_content/diagrams/module02/.

Writes decks/pptx_new/MongoDB_Module02_Installation_and_Setup.pptx and never
touches decks/pptx/.

    python scripts/new_content/build_module02_new.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from pptx.enum.text import MSO_ANCHOR  # noqa: E402

import mdb_deck_kit as K  # noqa: E402
import mdb_flow_slides as F  # noqa: E402
import mdb_speaker_notes as SN  # noqa: E402
import mdb_visuals as V  # noqa: E402
from mdb_visuals import (  # noqa: E402
    BLACK, GREEN, LEFT, NAVY, ORANGE, PURPLE, RED, TEAL, WIDTH,
)
from module02_notes import NOTES  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "decks" / "pptx_new" / "MongoDB_Module02_Installation_and_Setup.pptx"
MODULE_LABEL = "MODULE 2"


def notes(n: int) -> str:
    return SN.compose(NOTES[n])


def new(prs, layout, n, title, subtitle):
    return V.content_slide(prs, layout, number=n, title=title, subtitle=subtitle)


def done(slide, n, takeaway):
    V.finish(slide, number=n, takeaway=takeaway, notes=notes(n))


# ---------------------------------------------------------------------------
def s01(prs, layout):
    slide = K._chapter_slide(
        prs, layout, tag=MODULE_LABEL, title="Installation and Setup",
        subtitle="Choose a deployment, install or provision MongoDB, connect with mongosh and "
                 "Compass, and prove the environment with a write and a read.",
        quote='"Ping, write, read — then trust it."',
        module_label=MODULE_LABEL,
    )
    V.set_slide_label("slide 1")
    topics = [
        ("Choose a deployment", NAVY),
        ("Install and run", PURPLE),
        ("Connect", TEAL),
        ("First commands", GREEN),
        ("Secure and troubleshoot", ORANGE),
    ]
    w, gap = 2.34, 0.15
    for i, (label, fill) in enumerate(topics):
        x = LEFT + i * (w + gap)
        V.box(slide, x, 5.15, w, 0.95, label, fill=fill, size=15, radius=0.12, margin=0.14)
    K.set_notes(slide, notes(1))


def s02(prs, layout):
    n = 2
    slide, top = new(prs, layout, n, "Learning Objectives",
                     "What you will be able to do by the end of this module.")
    V.panel(slide, LEFT, top + 0.05, 5.9, "By the end of this module, you can", [
        "1. Choose local, container, self-managed or cloud",
        "2. Explain mongod, mongosh, Compass and drivers",
        "3. Install or provision MongoDB and start it",
        "4. Read and build a connection string",
        "5. Create training_store and run CRUD checks",
        "6. Protect credentials and diagnose failures",
    ], icon="🎯", badge_color=RED, size=16)

    x = 6.75
    y = V.section(slide, x, top + 0.05, 6.05, "Six questions this module answers", icon="❓",
                  fill=NAVY)
    questions = [
        ("WHERE", "should MongoDB run for this course?", NAVY),
        ("HOW", "do I install and start mongod?", PURPLE),
        ("HOW", "does a client find the server?", TEAL),
        ("WHAT", "proves the environment really works?", GREEN),
        ("HOW", "do I keep passwords out of sight?", ORANGE),
        ("WHAT", "do I check when it won't connect?", RED),
    ]
    row_h, gap = 0.50, 0.09
    for i, (word, rest, fill) in enumerate(questions):
        ry = y + i * (row_h + gap)
        V.box(slide, x, ry, 2.05, row_h, word, fill=fill, size=13)
        V.text(slide, x + 2.2, ry, 3.85, row_h, rest, size=14, anchor=MSO_ANCHOR.MIDDLE)

    V.section(slide, LEFT, 5.02, WIDTH, "Module roadmap", icon="🗺️", fill=PURPLE)
    V.chevrons(slide, LEFT, 5.50, WIDTH, 0.80,
               ["Deploy", "Install", "Start", "Connect", "First data", "Secure",
                "Troubleshoot"],
               [NAVY, PURPLE, TEAL, ORANGE, RED, GREEN, BLACK], size=13)
    done(slide, n, "A setup is finished only when a ping, a write and a read all succeed.")


# Hand-drawn slides, by topic number (see module02_flow.steps for the order).
SLIDES = {1: s01, 2: s02}


# ---------------------------------------------------------------------------
# Diagram slides: each diagram image is merged with the slide that explains it.
# Images live in scripts/new_content/diagrams/module02/ ("NN - Title.png"),
# copied from scripts/chatgpt_diagrams/diagrams/module02/ ("0NN - Title.png").
# ---------------------------------------------------------------------------
DIAGRAM_DIR = HERE / "diagrams" / "module02"

import mdb_diagram_slides as DS  # noqa: E402

_tp = DS.tp


DIAGRAMS: dict[int, tuple[str, str, list[dict]]] = {
    5: ("MongoDB Deployment Options",
        "Local mongod, a Docker container or a managed cloud service.",
        [_tp("What it shows",
             "The training_store application connecting to three kinds of deployment: a local "
             "mongod on the developer machine, a containerized mongod, and a hosted MongoDB "
             "service."),
         _tp("How to read it",
             "Each box holds the same training_store database with products, customers, orders "
             "and reviews. Only the Use line at the bottom changes."),
         _tp("Key point",
             "The database is the same everywhere; who runs the server is what changes.")]),
    6: ("Local MongoDB Deployment",
        "mongosh, mongod and the data directory on one machine.",
        [_tp("What it shows",
             "A developer laptop running all three pieces: mongosh, mongod and the data "
             "directory, dbPath, that holds training_store."),
         _tp("How to read it",
             "mongosh reaches mongod on localhost:27017. The bindIp: localhost label means "
             "only this machine can connect. mongod reads and writes the data directory."),
         _tp("Key point",
             "A local install is private by default, because it listens on localhost only.")]),
    7: ("Managed Cloud Deployment",
        "A managed replica set reached through a secure connection URI.",
        [_tp("What it shows",
             "mongosh and Compass on a developer laptop connecting over a TLS-encrypted "
             "connection URI to a managed MongoDB cluster."),
         _tp("How to read it",
             "Inside the cloud: a replica set with one primary and two secondaries, the "
             "training_store database, and the backups, monitoring and scaling the service "
             "provides."),
         _tp("Key point",
             "In the cloud you manage users, network access and the URI; the vendor runs the "
             "servers.")]),
    8: ("Cloud Provisioning Process",
        "Project, cluster, network access, database user, connection string, connect.",
        [_tp("What it shows",
             "Six steps to a working Atlas-style deployment, from creating the training_store "
             "project to opening a mongosh session."),
         _tp("How to read it",
             "Steps 3 and 4 are the two gates: allow a trusted client IP, and create a "
             "least-privilege database user. Step 5 copies the secure SRV URI."),
         _tp("Key point",
             "A cluster is not reachable until both the IP allowlist and the database user "
             "exist.")]),
    9: ("Containerized MongoDB",
        "mongod in a container, a published port and a named volume.",
        [_tp("What it shows",
             "A MongoDB container on the developer host. mongosh on the host reaches it at "
             "localhost:27017 through the published port 27017:27017."),
         _tp("How to read it",
             "The container's /data/db is mounted on a named volume, so the data lives outside "
             "the container."),
         _tp("Key point",
             "Without the volume, removing the container would remove training_store with "
             "it.")]),
    11: ("Local vs. Managed Cloud",
         "You run mongod — or the vendor runs the cluster.",
         [_tp("What it shows",
              "The same clients and the same training_store hierarchy on both sides: "
              "collections, documents and fields."),
          _tp("How to read it",
              "Local: clients reach localhost:27017, you own the files and you run mongod. "
              "Managed cloud: clients use a TLS URI, backups are included and the vendor runs "
              "the cluster."),
          _tp("Key point",
              "The data model and the commands are the same; the operating responsibility "
              "moves.")]),
    12: ("Choosing a Deployment Option",
         "Three questions lead to local, self-managed or managed cloud.",
         [_tp("What it shows",
              "A decision flow. Classroom laptop? Yes leads to Local or Docker. Otherwise: "
              "shared team or production-like? Yes leads to Managed cloud."),
          _tp("How to read it",
              "If neither, ask whether you need control of the operating system. Yes leads to "
              "Self-managed, where you run mongod. No sends you back to recheck your needs."),
          _tp("Key point",
              "Every path ends with the same training_store; only the operations work "
              "differs.")]),
    13: ("MongoDB Installation Workflow",
         "Six steps from download to a first test document.",
         [_tp("What it shows",
              "The local install path: install mongod, create the data and log directories, "
              "start the service, ping from mongosh, connect Compass, insert a test document."),
          _tp("How to read it",
              "Steps 1 to 3 are on the server side; steps 4 to 6 prove it from the client "
              "side."),
          _tp("Key point",
              "Installing is only half the job; the last three steps prove it works.")]),
    15: ("mongod vs. mongosh",
         "The server that stores data and the shell that sends commands.",
         [_tp("What it shows",
              "mongod on the left, running on localhost:27017 and storing training_store. "
              "mongosh on the right, a command-line client sending use training_store."),
          _tp("How to read it",
              "Commands travel from mongosh to mongod on port 27017; results travel back."),
          _tp("Key point",
              "Two separate programs: closing the shell never stops the server.")]),
    16: ("Three Clients, One Deployment",
         "mongosh, Compass and a driver share the same data.",
         [_tp("What it shows",
              "One mongod on port 27017 with training_store, read and written by three "
              "clients: mongosh, MongoDB Compass and a Node or Java driver."),
          _tp("How to read it",
              "Every arrow says Read / Write; the green bar says Same data."),
          _tp("Key point",
              "A different client is a different window, not a different database.")]),
    17: ("MongoDB Configuration File",
         "Four settings mongod loads when it starts.",
         [_tp("What it shows",
              "A mongod.conf with four essential settings, storage.dbPath, systemLog.path, "
              "net.port and net.bindIp, loaded by a running mongod."),
          _tp("How to read it",
              "Each setting becomes one runtime property: data directory, log file, port 27017 "
              "and bind address."),
          _tp("Key point",
              "When mongod won't start or can't be reached, read the config file first.")]),
    20: ("Starting and Stopping MongoDB",
         "Start, listen, connect — disconnect, clean shutdown, port closed.",
         [_tp("What it shows",
              "Two rows. Start: start mongod, it listens on port 27017, and mongosh and "
              "Compass connect. Stop: clients disconnect, mongod shuts down cleanly and the "
              "port closes."),
          _tp("How to read it",
              "Follow the arrows left to right in each row."),
          _tp("Key point",
              "Stop MongoDB with its service manager, so it shuts down cleanly.")]),
    22: ("Verifying the MongoDB Service",
         "Port open, shell connected, ping ok, databases listed.",
         [_tp("What it shows",
              "Four checks in order: port 27017 open, mongosh connected to mongod, "
              "db.runCommand ping returning ok: 1, and show dbs listing training_store."),
          _tp("How to read it",
              "Each check needs the one before it; the green ticks mean each step passed."),
          _tp("Key point",
              "Check in order, so the first failure tells you which layer is broken.")]),
    24: ("Localhost vs. Remote Connection",
         "One machine — or a client laptop and a remote server.",
         [_tp("What it shows",
              "Localhost: mongosh, Compass and mongod on one machine at 127.0.0.1:27017. "
              "Remote: a client laptop reaching a remote mongod at host:27017 over TLS."),
          _tp("How to read it",
              "The lock on the right side marks the extra protection a network connection "
              "needs."),
          _tp("Key point",
              "Leaving localhost adds network, TLS and authentication to the checklist.")]),
    26: ("Standard Connection-String Format",
         "Scheme, credentials, hosts, database and options.",
         [_tp("What it shows",
              "A standard mongodb:// URI split into parts: scheme, credentials, two "
              "replica-set hosts, the training_store database and ?authSource=admin."),
          _tp("How to read it",
              "user:pass@ are placeholders. host1 and host2 are both replica-set members, each "
              "on port 27017. authSource names the authentication database."),
          _tp("Key point",
              "Read a URI left to right: how, who, where, which database, which options.")]),
    27: ("DNS Seed-List Connection Strings",
         "mongodb+srv:// asks DNS for the member list.",
         [_tp("What it shows",
              "A client with a mongodb+srv:// URI asks DNS for the seed list. The SRV lookup "
              "returns hostnames and ports, and the client connects to the discovered "
              "mongod 1, 2 and 3."),
          _tp("How to read it",
              "The URI names one cluster host; DNS supplies the members and their ports."),
          _tp("Key point",
              "SRV strings are short and survive cluster changes; they need working DNS.")]),
    30: ("Connecting with MongoDB Compass",
         "New connection, paste the URI, connect, browse.",
         [_tp("What it shows",
              "Four Compass steps: New Connection, paste mongodb://localhost:27017, Connect, "
              "and browse training_store with its four collections."),
          _tp("How to read it",
              "Follow the numbers left to right."),
          _tp("Key point",
              "Compass takes the same connection string as mongosh.")]),
    33: ("Creating Your First Collection",
         "Explicit createCollection — or the first insert.",
         [_tp("What it shows",
              "Two ways to create a collection in training_store: explicitly with "
              "db.createCollection, or implicitly with the first insertOne."),
          _tp("How to read it",
              "Both arrows end at the same result: the collection exists. The top one creates "
              "it empty; the bottom one creates it with its first document."),
          _tp("Key point",
              "Collections and databases appear on the first write; use alone creates "
              "nothing.")]),
    38: ("Basic Authentication Concepts",
         "Credentials, authentication, roles, allowed actions.",
         [_tp("What it shows",
              "The user trainer_app signs in with a hidden password. mongod authenticates the "
              "user against authSource admin, applies the readWrite role on training_store, "
              "and allows find, insert and update."),
          _tp("How to read it",
              "Left to right: who you are, proof, what you may do, the request allowed."),
          _tp("Key point",
              "Authentication proves identity; authorization decides the allowed actions.")]),
    40: ("Safe Credential Practices",
         "Unsafe: passwords in chat or scripts. Safe: env vars, prompts, secret stores.",
         [_tp("What it shows",
              "Unsafe on the left: a password shared in a chat screenshot and a URI with a "
              "hard-coded password. Safe on the right: an environment variable, a password "
              "prompt and a secret store."),
          _tp("How to read it",
              "The password on the unsafe side is a made-up example of what never to do."),
          _tp("Key point",
              "The secret should reach mongod without ever appearing on a screen or in "
              "code.")]),
    42: ("Common Connection Problems",
         "Refused, timed out, bad credentials, address blocked.",
         [_tp("What it shows",
              "Four failed connections from mongosh or Compass to mongod: connection refused "
              "(port closed), timeout (no response), auth failed (bad credentials) and IP not "
              "allowed (address blocked)."),
          _tp("How to read it",
              "Each red cross sits at a different layer between the client and the server."),
          _tp("Key point",
              "The exact error message points to the layer; read it before changing "
              "anything.")]),
    43: ("Troubleshooting Workflow",
         "Four checks, in order, until the fix is confirmed.",
         [_tp("What it shows",
              "From a connection symptom through four checks: is mongod running, is the port "
              "and bindIp correct, is authentication valid, is network and TLS OK."),
          _tp("How to read it",
              "PASS moves right. FAIL drops to a fix: start mongod, correct the port or "
              "bindIp, verify user, password and authSource, allow the IP or repair TLS. Then "
              "recheck."),
          _tp("Key point",
              "Fix one layer, retest, and only then move on.")]),
    45: ("Module 2 at a Glance",
         "Deploy, install, connect, first write and read, secure and troubleshoot.",
         [_tp("What it shows",
              "Module 2 as five steps: deploy, install mongod, connect with a URI, mongosh and "
              "Compass, a first write and read in training_store, then secure and "
              "troubleshoot."),
          _tp("How to use it",
              "Point to each box and ask the class for the one command or check that proves "
              "it."),
          _tp("Key point",
              "These five steps are the setup every later lab assumes.")]),
}


def main() -> None:
    prs = K.new_presentation()
    layout = K.blank_layout(prs)
    from module02_flow import steps

    F.build_sequence(prs, layout, steps(SLIDES, NOTES, DIAGRAMS, DIAGRAM_DIR))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    K.save_presentation(prs, OUT)
    print(f"Wrote {len(prs.slides)} slides -> {OUT.relative_to(ROOT)}")
    for w in V.WARNINGS:
        print("  WARN", w)


if __name__ == "__main__":
    main()

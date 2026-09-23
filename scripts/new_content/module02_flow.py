#!/usr/bin/env python3
"""Slide order for the Module 2 deck: from choosing a deployment to a proven environment.

Every concept diagram is merged with the slide that explains it (diagram plus the
points only that slide adds), so no idea appears twice. Part openers, mongosh
commands and outputs on the training_store sample database, in-flow practice
exercises, a knowledge check, the official Exercises 2.1-2.4, Day 1 Lab 1 and a
hand-off to Module 3 connect the ideas.
"""
from __future__ import annotations

import mdb_diagram_slides as DS
import mdb_flow_slides as F
import mdb_glossary as G
from mdb_flow_slides import tp
from mdb_visuals import GREEN, NAVY, ORANGE, PURPLE, RED, TEAL

PARTS = ["Part 1\nChoose a deployment", "Part 2\nInstall and run", "Part 3\nConnect",
         "Part 4\nFirst commands", "Part 5\nSecure and troubleshoot"]


# ---------------------------------------------------------------------------
# Sequence
# ---------------------------------------------------------------------------
def steps(S, NOTES, DIAGRAMS, DIAGRAM_DIR):
    def img(n):
        return DS.diagram_file(DIAGRAM_DIR, n)

    def dn(n, *extra):
        return F.merge_units(NOTES[n], DIAGRAMS[n][2], *extra)

    return [
        S[1],
        S[2],
        *G.intro("module02"),
        F.story("From Module 1 to Module 2",
                "The ideas are in place — now we build the environment.",
                gave_title="Module 1 gave us",
                gave=["NoSQL is a family of data models",
                      "Documents, collections and BSON",
                      "mongod serves mongosh and Compass",
                      "The training_store sample database",
                      "Exercise 1.3 on the instructor's server"],
                now=("Now", "Run your own MongoDB — and prove that it works."),
                path_title="The path through Module 2",
                path=[("Choose where MongoDB runs", "Part 1", NAVY),
                      ("Install, configure and start mongod", "Part 2", PURPLE),
                      ("Connect with a connection string", "Part 3", TEAL),
                      ("Create training_store; write and read", "Part 4", GREEN),
                      ("Protect credentials; troubleshoot", "Part 5", ORANGE),
                      ("Prove it: Exercises 2.1–2.4, Lab 1", "Checkpoints", RED)],
                takeaway="Module 1 explained what MongoDB is; Module 2 gives every learner a "
                         "running, verified copy of it.",
                notes=[tp("Bridge from Module 1",
                          "Module 1 explained NoSQL, MongoDB's document model and the basic "
                          "architecture: clients such as mongosh and Compass talk to the mongod "
                          "server. Exercise 1.3 explored training_store on the instructor's "
                          "server."),
                       tp("What changes now",
                          "In Module 2 every learner gets their own environment, or a verified "
                          "connection to a shared one, and proves it with a ping, a write and "
                          "a read."),
                       tp("The path",
                          "Part 1 chooses where MongoDB runs. Part 2 installs and starts it. "
                          "Part 3 connects. Part 4 creates training_store and runs the first "
                          "commands. Part 5 covers credentials and troubleshooting. The "
                          "official Exercises 2.1 to 2.4 and Day 1 Lab 1 close the module."),
                       tp("Promise from Module 1",
                          "Module 1 ended with three questions: local MongoDB or Atlas, how to "
                          "install and start mongod and mongosh, and how to connect and load "
                          "training_store. This module answers all three.")]),

        # Part 1 ------------------------------------------------------------
        F.bridge(PARTS, 0, "Part 1: Choosing a Deployment",
                 "Before installing anything, decide where MongoDB should run.",
                 so_far=["Module 1 explained documents and mongod",
                         "training_store is our running example"],
                 question="Where should MongoDB run — on my laptop, in a container, on a "
                          "server, or in the cloud?",
                 covers=["Four deployment options", "Local Community Edition",
                         "Containerized MongoDB", "Managed cloud: MongoDB Atlas",
                         "Local versus managed cloud", "Choosing an option"],
                 notes=[tp("Why start here",
                           "The installation steps, the connection string and the security "
                           "work all depend on where MongoDB runs. So we decide that first."),
                        tp("What this part answers",
                           "We compare local, container, self-managed and managed-cloud "
                           "deployments, then use a simple decision flow. Exercise 2.1 "
                           "practises exactly this choice.")]),
        F.diagram(img(5), "MongoDB Deployment Options",
                  "The same training_store database — three places to run it.",
                  items=[("Local mongod", "Community Edition on your own machine — learning "
                                          "and development."),
                         ("Docker container", "Portable and isolated, easy to remove — tests "
                                              "and demos."),
                         ("Managed cloud", "MongoDB Atlas runs the cluster — teams and "
                                           "production."),
                         {"callout": ("Fourth option", "A self-managed server or VM — see the "
                                                       "decision flow.")}],
                  takeaway="Choose the deployment by who should run the server — the database "
                           "and the commands stay the same.",
                  notes=dn(5)),
        F.diagram(img(6), "Local Deployment: MongoDB Community Edition",
                  "mongosh, mongod and the data directory on one machine.",
                  items=[("Community Edition", "The free server, installed from MongoDB's "
                                               "official packages."),
                         ("localhost:27017", "The default address; bindIp: localhost keeps it "
                                             "private."),
                         ("dbPath", "The data directory where mongod stores training_store."),
                         {"callout": ("Auth is off by default",
                                      "Fine on localhost only — never expose it.")}],
                  takeaway="A local server is private by default — keep bindIp on localhost "
                           "while authentication is off.",
                  notes=dn(6)),
        F.diagram(img(9), "Containerized MongoDB",
                  "mongod in a container, a published port and a named volume.",
                  items=[{"code": "docker run -d --name mongo `\n"
                                  "  -p 127.0.0.1:27017:27017 `\n"
                                  "  -v mongo-data:/data/db `\n"
                                  "  mongodb/mongodb-community-server",
                          "label": "Start it (PowerShell)", "size": 11},
                         ("Published port", "Host 27017 → container 27017; 127.0.0.1 keeps it "
                                            "on this machine."),
                         ("Named volume", "mongo-data outlives the container — so does "
                                          "training_store.")],
                  takeaway="A container is quick to create and remove — mount a volume so the "
                           "data survives.",
                  notes=dn(9, [tp("Line breaks",
                                  "The command uses PowerShell's backtick to continue lines. In "
                                  "bash or zsh, end each line with a backslash instead.")])),
        F.diagram(img(7), "Managed Cloud: MongoDB Atlas",
                  "A managed replica set, reached through a secure connection URI.",
                  items=[("MongoDB Atlas", "MongoDB's managed cloud: servers, patches, backups "
                                           "and scaling."),
                         ("Replica set included", "One primary and two secondaries from the "
                                                  "start."),
                         ("TLS required", "Clients connect with an encrypted connection URI."),
                         {"callout": ("You still own", "Database users, the IP access list and "
                                                       "the secret URI.")}],
                  takeaway="Atlas runs the servers for you — you still decide who may connect, "
                           "and from where.",
                  notes=dn(7)),
        F.diagram(img(11), "Local vs. Managed Cloud",
                  "You run mongod — or the vendor runs the cluster.",
                  items=[("Internet", "Local: not after installation · Atlas: always."),
                         ("Who runs it", "Local: you run mongod · Atlas: the vendor runs the "
                                         "cluster."),
                         ("Address", "Local: localhost:27017 · Atlas: a TLS connection URI."),
                         ("Best use", "Local: learning, local development · Atlas: team and "
                                      "cloud projects.")],
                  takeaway="Same documents, same commands — local gives you control, the cloud "
                           "takes the operations work.",
                  notes=dn(11)),
        F.diagram(img(12), "Choosing a Deployment Option",
                  "Three questions lead to local, self-managed or managed cloud.",
                  items=[("Classroom laptop?", "Local or Docker on localhost."),
                         ("Shared team or production-like?", "Managed cloud with a TLS URI."),
                         ("Need control of the OS?", "Self-managed server or VM — you run "
                                                     "mongod."),
                         {"callout": ("Exercise 2.1", "You'll justify six choices like "
                                                      "these.")}],
                  takeaway="Start from the constraint — offline, disposable, shared or "
                           "controlled — then pick the option that fits it.",
                  notes=dn(12)),

        # Part 2 ------------------------------------------------------------
        F.bridge(PARTS, 1, "Part 2: Installing and Running MongoDB",
                 "Install the server and the shell, configure them and start the service.",
                 so_far=["Four deployment options, one database",
                         "Local for learning; Atlas for teams",
                         "The operating responsibility is what changes"],
                 question="How do I install MongoDB, configure it and start it — or provision "
                          "it in the cloud?",
                 covers=["The installation workflow", "mongod versus mongosh",
                         "Installing on Windows, macOS and Linux", "The configuration file",
                         "Starting and stopping MongoDB", "Provisioning in Atlas"],
                 notes=[tp("Connecting the parts",
                           "Part 1 chose where MongoDB runs. Part 2 makes it run: the local "
                           "install on each operating system, and the Atlas path for the "
                           "cloud."),
                        tp("Watch for",
                           "Keep two programs apart: mongod, the server, and mongosh, the "
                           "client. Most setup confusion comes from mixing them up.")]),
        F.diagram(img(13), "The MongoDB Installation Workflow",
                  "Six steps from download to a first test document.",
                  items=[("Server side", "Install mongod, check the data and log directories, "
                                         "start the service."),
                         ("Client side", "Ping from mongosh, connect Compass, insert a test "
                                         "document."),
                         ("What you install", "Community Server, mongosh, optional Compass and "
                                              "Database Tools."),
                         {"callout": ("Official docs", "Follow MongoDB's install page for your "
                                                       "OS and version.")}],
                  takeaway="Installing is only half the job — the last three steps prove the "
                           "server works.",
                  notes=dn(13)),
        F.diagram(img(15), "mongod vs. mongosh",
                  "The server that stores the data and the shell that sends commands.",
                  items=[("mongod", "The server: stores the data and listens on port 27017."),
                         ("mongosh", "The shell: sends commands and prints the results."),
                         ("Separate programs", "Closing mongosh never stops the database."),
                         {"callout": ("No server, no shell",
                                      "If mongod isn't running, mongosh can't connect.")}],
                  takeaway="mongod is the database; mongosh is only a window onto it.",
                  notes=dn(15)),
        F.code("Installing MongoDB on Windows, macOS and Linux",
               "Use MongoDB's official packages for your operating system.",
               [{"label": "Windows (PowerShell)", "kind": "info", "code":
                 "# MSI installer: Complete,\n"
                 "# run as a Windows service,\n"
                 "# optionally add Compass.\n"
                 "# Add mongosh if not included.\n"
                 "Get-Service MongoDB\n"
                 "mongosh --version"},
                {"label": "macOS (Homebrew)", "kind": "info", "code":
                 "brew tap mongodb/brew\n"
                 "brew install mongodb-community\n"
                 "brew services start mongodb-community\n"
                 "mongod --version\n"
                 "mongosh --version"},
                {"label": "Linux (MongoDB's repository)", "kind": "info", "code":
                 "# add MongoDB's repository for\n"
                 "# your distribution, then:\n"
                 "sudo systemctl start mongod\n"
                 "sudo systemctl status mongod\n"
                 "sudo systemctl enable mongod"}],
               points=[("Windows", "The MSI installs mongod as the MongoDB service."),
                       ("macOS", "The formula comes from MongoDB's own Homebrew tap."),
                       ("Linux", "Use MongoDB's repository, not the distribution's default "
                                 "package.")],
               takeaway="Install from MongoDB's official source, then confirm both the service "
                        "and the shell before moving on.",
               notes=[tp("Windows",
                         "Download MongoDB Community Server from the official website and run "
                         "the MSI. Choose Complete, install MongoDB as a Windows service, and "
                         "optionally install Compass. If mongosh isn't included in the package "
                         "you chose, install it separately. Then check the service in Windows "
                         "Services or with Get-Service MongoDB."),
                      tp("macOS",
                         "Homebrew uses MongoDB's own tap. The exact formula name can change "
                         "with the version, so follow MongoDB's current macOS page. brew "
                         "services start runs mongod in the background."),
                      tp("Linux",
                         "Add MongoDB's official repository for your distribution; the "
                         "distribution's default package is often old or not MongoDB's. "
                         "systemctl starts mongod, status shows whether it is running, and "
                         "enable starts it again after a reboot."),
                      tp("Verify the tools",
                         "mongosh --version prints the shell version. On Windows, mongod.exe is "
                         "in the server's bin folder and usually not on the PATH, so check the "
                         "service instead of running mongod --version.")]),
        F.diagram(img(17), "The MongoDB Configuration File",
                  "Four settings mongod loads when it starts.",
                  items=[{"code": "storage:\n"
                                  "  dbPath: /var/lib/mongodb\n"
                                  "systemLog:\n"
                                  "  destination: file\n"
                                  "  path: /var/log/mongodb/mongod.log\n"
                                  "net:\n"
                                  "  port: 27017\n"
                                  "  bindIp: 127.0.0.1",
                          "label": "mongod.conf (Linux example)", "size": 11},
                         ("bindIp 127.0.0.1", "This machine only — keep it for learning."),
                         {"callout": ("Warning", "0.0.0.0 exposes mongod to every network — "
                                                 "only with auth, TLS and a firewall.")}],
                  takeaway="The config file decides where data and logs go and who can reach "
                           "the port — read it first when something breaks.",
                  notes=dn(17)),
        F.diagram(img(20), "Starting and Stopping MongoDB",
                  "Start, listen, connect — then disconnect, shut down cleanly, close the port.",
                  items=[{"code": "Start-Service MongoDB\nStop-Service MongoDB",
                          "label": "Windows (admin PowerShell)", "size": 11},
                         {"code": "brew services start mongodb-community\n"
                                  "brew services stop mongodb-community",
                          "label": "macOS", "size": 11},
                         {"code": "sudo systemctl start mongod\nsudo systemctl stop mongod",
                          "label": "Linux", "size": 11},
                         {"callout": ("Clean shutdown", "Use the service manager — don't kill "
                                                        "the process.")}],
                  takeaway="Start and stop mongod through its service manager, so every "
                           "shutdown is clean.",
                  notes=dn(20)),
        F.diagram(img(8), "Provisioning MongoDB Atlas",
                  "Project, cluster, network access, database user, connection string, "
                  "connect.",
                  items=[("Project and cluster", "Pick a free or paid tier, a provider and a "
                                                 "region."),
                         ("IP access list", "Allow only the client addresses that need "
                                            "access."),
                         ("Database user", "Least privilege — not your Atlas login."),
                         ("Connection string", "Copy the SRV URI from the Connect dialog.")],
                  takeaway="An Atlas cluster is reachable only after you allow an IP address "
                           "and create a database user.",
                  notes=dn(8)),
        F.exercise("Exercise: Is the Server Running?",
                   "Read the evidence before you change anything.",
                   scenario="A learner installed MongoDB on Windows. mongosh reports connection "
                            "refused on localhost:27017.",
                   scenario_code="PS> Get-Service MongoDB\n\n"
                                 "Status   Name     DisplayName\n"
                                 "------   ----     -----------\n"
                                 "Stopped  MongoDB  MongoDB Server (MongoDB)",
                   tasks=["Name the layer that failed",
                          "Give the command that fixes it",
                          "Say how you'll prove the fix",
                          "Name a cause if it won't start"],
                   expected=["The server process: mongod is stopped",
                             "Start-Service MongoDB, as Administrator",
                             "mongosh, then db.runCommand({ ping: 1 })",
                             "Check the log: bad dbPath or port in use"],
                   minutes=5,
                   takeaway="Connection refused usually means nothing is listening — check the "
                            "server before the client.",
                   notes=[tp("How to run it",
                             "Individually for three minutes, then discuss. Ask for the layer "
                             "first, before anyone suggests a fix."),
                          tp("The layer",
                             "The service status is Stopped, so nothing listens on port 27017. "
                             "That is why mongosh gets connection refused rather than a "
                             "timeout."),
                          tp("The fix and the proof",
                             "Start-Service MongoDB in an Administrator PowerShell. Then run "
                             "mongosh and db.runCommand({ ping: 1 }); ok: 1 proves the fix."),
                          tp("If it won't start",
                             "Read the server log named by systemLog.path. Typical startup "
                             "errors are a missing or unwritable dbPath and port 27017 already "
                             "in use by another process.")]),

        # Part 3 ------------------------------------------------------------
        F.bridge(PARTS, 2, "Part 3: Connecting to MongoDB",
                 "Every client needs to know where the server is — and who is asking.",
                 so_far=["mongod is installed and running",
                         "Its config sets dbPath, log, port and bindIp",
                         "Atlas needs a user and an IP allowlist"],
                 question="How does a client find the server, prove who it is, and confirm "
                          "the connection works?",
                 covers=["Three clients, one deployment", "Localhost versus remote",
                         "Standard connection strings", "SRV connection strings",
                         "Connecting with mongosh", "Connecting with Compass",
                         "Verifying the connection"],
                 notes=[tp("Connecting the parts",
                           "The server is running. Now we connect to it from mongosh and "
                           "Compass, locally and in the cloud."),
                        tp("What to watch",
                           "The connection string is the key idea. Once learners can read one "
                           "left to right, most connection errors become easy to place.")]),
        F.diagram(img(16), "Three Clients, One Deployment",
                  "mongosh, Compass and application drivers share the same data.",
                  items=[("mongosh", "The command-line shell for queries and "
                                     "administration."),
                         ("MongoDB Compass", "The graphical client to browse and edit "
                                             "documents."),
                         ("Drivers", "Libraries for application code — Node.js, Java and "
                                     "more."),
                         {"callout": ("Same data",
                                      "A different window, not a different database.")}],
                  takeaway="Every client reads and writes the same deployment — pick the one "
                           "that suits the task.",
                  notes=dn(16)),
        F.diagram(img(24), "Localhost vs. Remote Connections",
                  "One machine — or a client laptop and a remote server.",
                  items=[("Localhost", "127.0.0.1:27017 — traffic never leaves the machine."),
                         ("Remote", "host:27017 across a network: TLS, authentication and an "
                                    "open firewall port."),
                         {"callout": ("bindIp decides",
                                      "mongod answers only on the addresses it binds to.")}],
                  takeaway="Leaving localhost adds three requirements: a reachable port, TLS "
                           "and authentication.",
                  notes=dn(24)),
        F.diagram(img(26), "Standard Connection-String Format",
                  "Scheme, credentials, hosts, database and options.",
                  items=[{"code": "mongodb://localhost:27017\n"
                                  "mongodb://localhost:27017/training_store",
                          "label": "Local examples", "size": 10},
                         ("Read it left to right", "Scheme, credentials, host:port list, "
                                                   "database, then ?options."),
                         ("authSource and encoding", "authSource names the user's database. "
                                                     "Percent-encode special characters in "
                                                     "passwords.")],
                  takeaway="A connection string answers five questions: how, who, where, which "
                           "database and which options.",
                  notes=dn(26, [tp("The local examples",
                                   "The first string reaches the default local server. The "
                                   "second adds /training_store, so mongosh opens that "
                                   "database directly.")])),
        F.diagram(img(27), "DNS Seed-List (SRV) Connection Strings",
                  "mongodb+srv:// asks DNS for the member list.",
                  items=[{"code": "mongodb+srv://\n"
                                  "  <username>:<password>@\n"
                                  "  <cluster-host>/",
                          "label": "Atlas pattern — placeholders only", "size": 11},
                         ("Seed list", "DNS returns the members and ports — no port in the "
                                       "URI."),
                         ("TLS on", "SRV strings turn TLS on by default."),
                         {"callout": ("Exercise 2.2", "Compare mongodb:// and "
                                                      "mongodb+srv://.")}],
                  takeaway="mongodb:// lists the hosts; mongodb+srv:// lets DNS supply them.",
                  notes=dn(27)),
        F.code("Connecting with mongosh",
               "Local defaults, a named database, and a password prompt.",
               [{"label": "Local server (PowerShell)", "kind": "info", "code":
                 "mongosh\n"
                 "# same as:\n"
                 "mongosh \"mongodb://localhost:27017\"\n"
                 "\n"
                 "# open training_store directly:\n"
                 "mongosh \"mongodb://localhost:27017/training_store\""},
                {"label": "With a user: mongosh prompts for the password", "kind": "good",
                 "code":
                 "mongosh \"mongodb://localhost:27017/training_store\" `\n"
                 "  --username trainingUser\n"
                 "\n"
                 "# Atlas: copy the host from Connect → Shell\n"
                 "mongosh \"mongodb+srv://cluster0.example.mongodb.net/\" `\n"
                 "  --username trainingUser\n"
                 "Enter password: ********"}],
               points=[("mongosh on its own", "Connects to localhost:27017 — the default."),
                       ("--username", "mongosh prompts for the password: nothing lands in "
                                      "history."),
                       {"callout": ("Atlas", "Copy the exact command from Connect → Shell.")}],
               takeaway="Give mongosh a connection string and a username — and let it ask for "
                        "the password.",
               notes=[tp("Local",
                         "If MongoDB runs locally on the standard port, mongosh on its own "
                         "connects to mongodb://localhost:27017. Adding /training_store to the "
                         "URI selects that database as soon as the shell opens."),
                      tp("With authentication",
                         "Pass --username and leave the password out. mongosh prompts for it, "
                         "so it never appears in the command, in the shell history or on a "
                         "shared screen."),
                      tp("Atlas",
                         "In Atlas, open the deployment, select Connect, choose Shell and copy "
                         "the generated command, because the cluster hostname is specific to "
                         "your deployment. cluster0.example.mongodb.net is a placeholder."),
                      tp("Line breaks",
                         "The backtick continues a PowerShell line. In bash or zsh, use a "
                         "backslash instead, as MongoDB's documentation does.")]),
        F.diagram(img(30), "Connecting with MongoDB Compass",
                  "New connection, paste the URI, connect, browse.",
                  items=[("Same URI", "Paste the connection string you used in mongosh."),
                         ("Password field", "Type it there — never in a shared screenshot."),
                         ("Browse", "Databases → collections → documents; refresh to see new "
                                    "writes.")],
                  takeaway="Compass is a graphical window onto the same deployment, opened with "
                           "the same connection string.",
                  notes=dn(30)),
        F.diagram(img(22), "Verifying the Connection",
                  "Port open, shell connected, ping ok, databases listed.",
                  items=[{"code": "test> db.runCommand({ ping: 1 })\n"
                                  "{ ok: 1 }\n"
                                  "test> db.version()\n"
                                  "8.0.4",
                          "label": "Is the server answering?", "size": 11},
                         {"code": "test> db\n"
                                  "test\n"
                                  "test> show dbs\n"
                                  "admin   40.00 KiB\n"
                                  "config  60.00 KiB\n"
                                  "local   40.00 KiB",
                          "label": "Where am I?", "size": 11},
                         ("Reading the results", "ok: 1 = reachable. A new server lists only "
                                                 "admin, config and local; training_store "
                                                 "joins after its first write.")],
                  takeaway="A ping that returns ok: 1 proves the server answers — the next part "
                           "proves you can write.",
                  notes=dn(22, [tp("Versions and sizes",
                                   "8.0.4 is an example; print your own with db.version(). "
                                   "The sizes after show dbs vary from machine to machine."),
                                tp("About the diagram",
                                   "The diagram's last box shows show dbs listing "
                                   "training_store. That is the state after training_store "
                                   "holds data; on a brand-new server you see only admin, "
                                   "config and local.")])),
        F.exercise("Exercise: Build the Connection String",
                   "Write what each learner needs — with no password on the page.",
                   scenario="Three learners need to connect. Write the connection string or "
                            "mongosh command for each one.",
                   scenario_code="A  Local server, default port\n"
                                 "B  Local server, open training_store\n"
                                 "C  Atlas: cluster0.example.mongodb.net\n"
                                 "   as database user trainingUser",
                   tasks=["Write learner A's URI",
                          "Add the database for learner B",
                          "Write learner C's mongosh command",
                          "Say where C's password goes"],
                   expected=["A: mongodb://localhost:27017",
                             "B: add /training_store after the port",
                             "C: the mongodb+srv:// URI plus --username",
                             "Typed at the prompt — never in the URI"],
                   minutes=10,
                   takeaway="If you can write the connection string, you can place most "
                            "connection errors.",
                   notes=[tp("How to run it",
                             "Individually for five minutes, then compare in pairs. Collect one "
                             "answer per learner on the board, without any password."),
                          tp("A and B",
                             "A is mongodb://localhost:27017, which is also what mongosh uses "
                             "with no arguments. B is "
                             "mongodb://localhost:27017/training_store."),
                          tp("C",
                             "mongosh \"mongodb+srv://cluster0.example.mongodb.net/\" "
                             "--username trainingUser. No port: the SRV lookup supplies the "
                             "members and ports, and TLS is on by default."),
                          tp("The password",
                             "mongosh prompts for it. In an application, it comes from an "
                             "environment variable or a secret store, never from source "
                             "code.")]),

        # Part 4 ------------------------------------------------------------
        F.bridge(PARTS, 3, "Part 4: First Commands on training_store",
                 "Prove the environment: create, read, update and delete.",
                 so_far=["Clients reach mongod through a connection string",
                         "SRV strings let DNS find the cluster",
                         "A ping proves the server answers"],
                 question="How do I create training_store — and prove I can write, read, "
                          "update and delete?",
                 covers=["Selecting a database and creating a collection",
                         "Inserting and reading a test document",
                         "Update and delete with a probe document",
                         "Loading the full training_store dataset",
                         "Predicting shell output"],
                 notes=[tp("Why this part",
                           "A ping proves the server answers. It doesn't prove you can write. "
                           "This part runs the four CRUD operations as a readiness test."),
                        tp("Two probe documents",
                           "Day 1 Lab 1 uses two: the environment_check collection and the "
                           "LAB1 probe product. Neither clashes with the real "
                           "training_store catalog, which is loaded at the end of the part.")]),
        F.diagram(img(33), "Selecting a Database and Creating a Collection",
                  "use switches context; the first write creates the collection.",
                  items=[{"code": "test> use training_store\n"
                                  "switched to db training_store\n"
                                  "training_store> db.createCollection(\n"
                                  "  \"products\")\n"
                                  "{ ok: 1 }",
                          "label": "Explicit creation (Lab 1)", "size": 11},
                         ("Implicit creation", "The first insertOne creates the collection — "
                                               "no createCollection needed."),
                         {"callout": ("use creates nothing",
                                      "show dbs lists training_store only after the first "
                                      "write.")}],
                  takeaway="use only selects a name — a database and its collections appear "
                           "with the first write.",
                  notes=dn(33)),
        F.code("Inserting and Reading a Test Document",
               "Lab 1's READY document in the environment_check collection.",
               [{"label": "Insert — MongoDB adds the _id", "kind": "info", "code":
                 "db.environment_check.insertOne({\n"
                 "  participant: \"Student\",\n"
                 "  environment: \"training\",\n"
                 "  shellConnected: true,\n"
                 "  status: \"READY\",\n"
                 "  checkedAt: new Date()\n"
                 "})\n"
                 "// result\n"
                 "{ acknowledged: true,\n"
                 "  insertedId: ObjectId('…') }"},
                {"label": "Read it back", "kind": "good", "code":
                 "db.environment_check.findOne({\n"
                 "  status: \"READY\"\n"
                 "})\n"
                 "// result\n"
                 "{ _id: ObjectId('…'),\n"
                 "  participant: 'Student',\n"
                 "  environment: 'training',\n"
                 "  shellConnected: true,\n"
                 "  status: 'READY',\n"
                 "  checkedAt: ISODate('…') }"}],
               points=[("insertedId", "An ObjectId, generated because we didn't supply an "
                                      "_id."),
                       ("checkedAt", "new Date() is stored as a BSON date; mongosh prints "
                                     "ISODate."),
                       {"callout": ("Proof", "A write and a read = usable access.")}],
               takeaway="An acknowledged insert and a matching read prove more than any ping.",
               notes=[tp("The insert",
                         "insertOne sends one document. We didn't include _id, so MongoDB adds "
                         "one: a new ObjectId, unique in the collection. The result says "
                         "acknowledged: true and shows that insertedId."),
                      tp("The read",
                         "findOne with status READY returns the same document, now including "
                         "_id. The date comes back as ISODate: a real BSON date, not a "
                         "string."),
                      tp("Output style",
                         "mongosh prints strings with single quotes and shortens nothing; the "
                         "ellipses on the slide stand for your own ObjectId and date."),
                      tp("Link to the lab",
                         "This is Step 7 of Day 1 Lab 1. Step 8 adds three component "
                         "documents with insertMany, counts at least 4 documents, and updates "
                         "the participant name.")]),
        F.code("Update, Delete and the Probe Document",
               "Day 1 Lab 1 proves all four CRUD operations with sku LAB1.",
               [{"label": "Create and read", "kind": "info", "code":
                 "db.products.insertOne({\n"
                 "  sku: \"LAB1\",\n"
                 "  name: \"Connectivity Probe\",\n"
                 "  category: \"ACCESSORY\",\n"
                 "  active: true\n"
                 "})\n"
                 "db.products.find({ sku: \"LAB1\" })"},
                {"label": "Update and delete", "kind": "info", "code":
                 "db.products.updateOne(\n"
                 "  { sku: \"LAB1\" },\n"
                 "  { $set: { verified: true } }\n"
                 ")\n"
                 "// matchedCount: 1, modifiedCount: 1\n"
                 "db.products.deleteOne({ sku: \"LAB1\" })\n"
                 "// { acknowledged: true, deletedCount: 1 }\n"
                 "db.products.find({ sku: \"LAB1\" })\n"
                 "// no result"}],
               points=[("Create · Read", "insertOne() returns an insertedId; find() shows the "
                                         "probe."),
                       ("Update · Delete", "updateOne() matches 1 document; deleteOne() "
                                           "deletes 1."),
                       {"callout": ("Remove LAB1", "Delete it before Lab 2 — it isn't a catalog "
                                                   "SKU.")}],
               takeaway="insertOne, find, updateOne and deleteOne — four operations, four "
                        "results you can check.",
               notes=[tp("The probe",
                         "Day 1 Lab 1 inserts one probe product, sku LAB1, named Connectivity "
                         "Probe. It uses the real ACCESSORY category, but it is not part of the "
                         "catalog, which is why the lab deletes it at the end."),
                      tp("Update",
                         "updateOne finds the probe by sku and $set adds verified: true. "
                         "matchedCount 1 means the filter found it; modifiedCount 1 means it "
                         "changed."),
                      tp("Delete",
                         "deleteOne removes it and reports deletedCount 1. The final find "
                         "returns nothing, which is the proof."),
                      tp("A note on the sources",
                         "The module's source text inserts a Wireless Mouse under Electronics "
                         "at 39.99, and MongoDB Fundamentals under Books at 49.99. In "
                         "training_store the Wireless Mouse is A410, ACCESSORY, 19.99, and "
                         "MongoDB Fundamentals is B300, BOOK, 59.99, both stored as Decimal128. "
                         "So the deck uses the LAB1 probe instead of inventing conflicting "
                         "products."),
                      tp("On a loaded database",
                         "Lab 1 Step 9 also runs db.createCollection(\"products\"). On an "
                         "empty server that returns ok: 1. If training_store is already loaded, it fails "
                         "with Collection already exists; skip it, the rest of the lab works "
                         "the same.")]),
        F.code("Loading the Full training_store Dataset",
               "Module 3's Lab 2 runs this — here is what to expect.",
               [{"label": "From the course folder, not inside mongosh", "kind": "info",
                 "code":
                 "mongosh \"mongodb://localhost:27017\" `\n"
                 "  .\\datasets\\training_store\\load.js\n"
                 "\n"
                 "// prints\n"
                 "Loaded training_store\n"
                 "customers: 6\n"
                 "products: 13\n"
                 "orders: 17\n"
                 "reviews: 6\n"
                 "paid orders: 13"},
                {"label": "Then verify in mongosh", "kind": "good", "code":
                 "use training_store\n"
                 "show collections\n"
                 "// customers, environment_check,\n"
                 "// orders, products, reviews\n"
                 "db.products.countDocuments()\n"
                 "// 13\n"
                 "db.products.findOne(\n"
                 "  { sku: \"B300\" },\n"
                 "  { name: 1, price: 1, _id: 0 })\n"
                 "// { name: 'MongoDB Fundamentals',\n"
                 "//   price: Decimal128('59.99') }"}],
               points=[("Drops, then reloads", "customers, products, orders and reviews start "
                                               "clean each time."),
                       ("Leaves the rest", "environment_check isn't touched — it stays in the "
                                           "list."),
                       {"callout": ("Module 3", "Lab 2 starts from exactly this state.")}],
               takeaway="One script gives everyone the same training_store — the starting point "
                        "for every later lab.",
               notes=[tp("When to run it",
                         "Module 3's Lab 2, Path A, runs this script. Learners taking the "
                         "hand-insert path build the core documents first and run it at the "
                         "start of Day 2. Run it now only if the instructor asks."),
                      tp("What it does",
                         "load.js drops and reloads customers, products, orders and reviews, "
                         "then creates unique indexes on sku, customerNumber, orderNumber and "
                         "contact.email. It prints the counts: 6 customers, 13 products, 17 "
                         "orders, 6 reviews, and 13 paid orders."),
                      tp("Verify",
                         "show collections lists the four collections plus environment_check, "
                         "which load.js doesn't drop. countDocuments on products returns 13. "
                         "B300 is MongoDB Fundamentals at Decimal128 59.99."),
                      tp("Other paths",
                         "For Atlas or an instructor URI, replace the local string with your "
                         "own connection string and add --username; mongosh prompts for the "
                         "password before running the script."),
                      tp("A note on the sources",
                         "Lab 1 says the sample data is loaded in Module 3, and that is "
                         "where the lab runs it. This slide shows the command early because "
                         "Module 1 promised that Module 2 would show how.")]),
        F.exercise("Exercise: Predict the Shell Output",
                   "Say what mongosh prints — before you press Enter.",
                   scenario="A brand-new local server. Nothing has been created yet.",
                   scenario_code="show dbs\n"
                                 "use training_store\n"
                                 "show dbs\n"
                                 "db.environment_check.insertOne(\n"
                                 "  { status: \"READY\" })\n"
                                 "show dbs\n"
                                 "show collections",
                   tasks=["Predict the first show dbs",
                          "Say what use prints — and creates",
                          "Predict show dbs after the insert",
                          "Predict show collections"],
                   expected=["admin, config and local only",
                             "switched to db training_store; nothing on disk",
                             "training_store now appears",
                             "environment_check"],
                   minutes=5,
                   takeaway="Databases and collections appear on the first write — predicting "
                            "that saves a lot of confusion.",
                   notes=[tp("How to run it",
                             "Two minutes to write predictions, then run the commands on the "
                             "instructor screen, one at a time."),
                          tp("Before the insert",
                             "show dbs lists admin, config and local. use prints switched to db "
                             "training_store but creates nothing, so the second show dbs is "
                             "unchanged."),
                          tp("After the insert",
                             "The insert creates the collection and the database together. "
                             "show dbs now includes training_store, and show collections lists "
                             "environment_check."),
                          tp("Why it matters",
                             "Learners often think a typo in use created a new database. It "
                             "didn't; nothing exists until the first write.")]),

        # Part 5 ------------------------------------------------------------
        F.bridge(PARTS, 4, "Part 5: Security and Troubleshooting",
                 "Keep credentials safe — and fix connections layer by layer.",
                 so_far=["training_store exists on your server",
                         "Insert, find, update and delete all work",
                         "The full dataset loads with one script"],
                 question="How do I keep credentials safe — and what do I check when a "
                          "connection fails?",
                 covers=["Authentication and authorization", "Safe credential practices",
                         "Common connection problems", "A troubleshooting workflow",
                         "Setup misconceptions"],
                 notes=[tp("Why this part",
                           "A working environment can still leak a password or be open to the "
                           "internet. And when a connection fails, guessing wastes time."),
                        tp("Outcome",
                           "By the end, learners handle credentials safely and diagnose a "
                           "failure by asking one question per layer. Exercise 2.3 practises "
                           "it.")]),
        F.diagram(img(38), "Authentication and Authorization",
                  "Credentials, authentication, roles, allowed actions.",
                  items=[("Authentication", "Who are you? Username, password and authSource."),
                         ("Authorization", "What may you do? Roles such as readWrite."),
                         ("Local default", "Access control is off — tolerable on localhost "
                                           "only."),
                         ("Least privilege", "Give each user only the roles it needs.")],
                  takeaway="Authentication proves who you are; authorization decides what you "
                           "may do.",
                  notes=dn(38)),
        F.diagram(img(40), "Safe Credential Practices",
                  "Keep passwords out of chat, screenshots, scripts and Git.",
                  items=[{"code": "# prompt instead of typing it\n"
                                  "mongosh \"<connection-string>\" `\n"
                                  "  --username <username>",
                          "label": "Let mongosh prompt", "kind": "good", "size": 11},
                         ("Store it safely", "A password manager, a secret store or an "
                                             "environment variable."),
                         {"callout": ("0.0.0.0/0", "Opens Atlas to the whole internet — avoid "
                                                   "it; never in production.")}],
                  takeaway="A password shown once must be treated as leaked — keep it out of "
                           "every screen and file.",
                  notes=dn(40)),
        F.diagram(img(42), "Common Connection Problems",
                  "Refused, timed out, bad credentials, address blocked.",
                  items=[("Connection refused", "Nothing listening: mongod stopped, wrong port "
                                                "or bindIp."),
                         ("Timeout", "No answer: firewall, routing or the Atlas IP access "
                                     "list."),
                         ("Auth failed", "User, password, authSource or unencoded "
                                         "characters."),
                         ("IP not allowed", "Add your current IP — not 0.0.0.0/0.")],
                  takeaway="Each error names a different layer — read the message before "
                           "changing anything.",
                  notes=dn(42)),
        F.diagram(img(43), "A Troubleshooting Workflow",
                  "Four checks, in order, until the fix is confirmed.",
                  items=[("1 · Process", "Is mongod running? Service status and log."),
                         ("2 · Port and bindIp", "Port 27017? Listening on your address?"),
                         ("3 · Credentials", "User, password and authSource."),
                         ("4 · Network and TLS", "IP allowlist, firewall and TLS settings.")],
                  takeaway="Change one thing, retest with a ping, then move to the next layer.",
                  notes=dn(43)),
        F.myths("Setup Misconceptions",
                "Beliefs that waste the first hour of a lab.",
                [("Closing mongosh stops MongoDB",
                  "mongod keeps running — it is a separate process"),
                 ("use training_store creates it",
                  "The database appears with the first write"),
                 ("A ping means I can write",
                  "Ping proves reachability — test a write and a read"),
                 ("Compass shows a different copy",
                  "Same deployment, same documents — refresh"),
                 ("0.0.0.0 makes connecting easier",
                  "It exposes the server — keep localhost or an allowlist")],
                ["Passwords in URIs, scripts or Git",
                 "Screenshots of the connection dialog",
                 "An Atlas login reused as a database user",
                 "Changing three settings at once",
                 "Killing mongod instead of stopping it"],
                remember=("Remember", "Prove each layer: running, reachable, authenticated, "
                                      "writable."),
                takeaway="Most setup problems come from confusing the client with the server, "
                         "or reachability with access.",
                notes=[tp("Why this slide",
                          "Before the checks, clear away the beliefs that cause the most "
                          "trouble in setup labs."),
                       tp("Client versus server",
                          "mongosh and Compass are clients. Closing them never stops mongod, "
                          "and Compass shows the same documents as mongosh after a refresh."),
                       tp("Reachability versus access",
                          "use creates nothing, and a ping doesn't prove write permission. "
                          "Only a write and a read prove usable access."),
                       tp("Anti-patterns",
                          "Passwords in URIs, scripts or Git; screenshots of connection "
                          "dialogs; reusing an Atlas login as a database user; changing "
                          "several settings at once; and killing mongod instead of stopping "
                          "it cleanly. Binding to 0.0.0.0 or allowing 0.0.0.0/0 without "
                          "authentication exposes the data to anyone.")]),
        F.diagram(img(45), "Module 2 at a Glance",
                  "Deploy, install, connect, first write and read, secure and troubleshoot.",
                  takeaway="A proven environment — running, reachable, authenticated and "
                           "writable — is what every later lab needs.",
                  notes=dn(45)),

        # Wrap-up ------------------------------------------------------------
        F.knowledge("Knowledge Check", "Answer in your own words — then compare with a partner.",
                    ["What is the role of mongod?",
                     "What is the role of mongosh?",
                     "What is MongoDB Compass?",
                     "What is MongoDB's default port?",
                     "How do mongodb:// and mongodb+srv:// differ?",
                     "What does db.runCommand({ ping: 1 }) verify?",
                     "Why might show dbs omit a database you just selected?",
                     "What commonly causes connection refused?",
                     "What commonly causes authentication failed?",
                     "Why not put credentials in source code?"],
                    notes=[tp("1. mongod",
                              "The database server process. It stores the data, listens on a "
                              "port and answers requests."),
                           tp("2. mongosh",
                              "The interactive command-line shell. It sends commands to mongod "
                              "and prints the results; closing it doesn't stop the server."),
                           tp("3. Compass",
                              "MongoDB's graphical client, connected with the same connection "
                              "string, showing the same data."),
                           tp("4. Default port",
                              "27017. A local server is usually at localhost:27017."),
                           tp("5. mongodb:// and mongodb+srv://",
                              "mongodb:// lists the hosts and optional ports. mongodb+srv:// "
                              "gives one hostname and uses a DNS SRV lookup to find the members; "
                              "it turns TLS on by default. Atlas provides the +srv form."),
                           tp("6. Ping",
                              "That the server is reachable and answering. It does not prove "
                              "write permission."),
                           tp("7. show dbs",
                              "use only switches context. A database appears in show dbs once "
                              "it holds data, after the first write."),
                           tp("8. Connection refused",
                              "Nothing is listening: mongod is stopped, the port is wrong, or "
                              "bindIp doesn't include the address."),
                           tp("9. Authentication failed",
                              "Wrong username or password, the wrong authSource, or special "
                              "characters that weren't percent-encoded."),
                           tp("10. Credentials in code",
                              "Code is shared, copied and committed to Git, so the password "
                              "leaks. Use environment variables, a secret store or a prompt.")]),
        F.exercise("Exercise 2.1 — Select a Deployment Option",
                   "Module 2 checkpoint A: match six scenarios to a deployment, with a risk.",
                   kind="OFFICIAL CHECKPOINT A", minutes=10,
                   worksheet="labs/day-01/exercises/exercise-2.1-select-a-deployment-option.md",
                   scenario="Pick one option — local, self-managed server or VM, container, or "
                            "managed cloud. Justify it and name the main risk.",
                   scenario_code="1  Offline learning environment\n"
                                 "2  Temporary automated tests\n"
                                 "3  Distributed team, shared data\n"
                                 "4  Regulated: direct control\n"
                                 "5  Startup: no servers to manage\n"
                                 "6  Classroom: restricted internet",
                   tasks=["Name one good fit for each option",
                          "Classify scenarios 1–3",
                          "Classify scenarios 4–6",
                          "Defend one row against an alternative"],
                   expected=["1 local · 2 container", "3 managed cloud",
                             "4 self-managed server or VM", "5 managed cloud",
                             "6 local or a local server"],
                   expected_title="Solution (after debrief)",
                   takeaway="The commands barely change between options — the infrastructure "
                            "responsibility does.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 2.1 for Module 2. The worksheet is "
                             "labs/day-01/exercises/exercise-2.1-select-a-deployment-option.md; "
                             "the answer key is in the solution folder next to it. No MongoDB "
                             "is needed; work in pairs."),
                          tp("Running it",
                             "Eight minutes of pair work, then a two-minute debrief. Reveal the "
                             "solution column only after pairs share one controversial row."),
                          tp("What to listen for",
                             "Each justification names a constraint: offline, disposable, "
                             "shared, control, operations load or network. A product name "
                             "alone doesn't count."),
                          tp("Typical risks",
                             "Local: data lost with the laptop and no shared access. Container: "
                             "data lost without a volume. Managed cloud: needs internet, and "
                             "the IP allowlist and credentials must be managed. Self-managed: "
                             "you own patching, backups and monitoring.")]),
        F.exercise("Exercise 2.2 — Interpret a Connection String",
                   "Module 2 checkpoint B: label every part, and keep the password secret.",
                   kind="OFFICIAL CHECKPOINT B", minutes=10,
                   worksheet="labs/day-01/exercises/exercise-2.2-interpret-a-connection-string"
                             ".md",
                   scenario="Label each part of this URI. It is one line, split to fit; the "
                            "password is a placeholder.",
                   scenario_code="mongodb://\n"
                                 "trainingUser:<password>@\n"
                                 "db.example.net:27017\n"
                                 "/training",
                   tasks=["Label protocol, user, password, host, port, database",
                          "Answer the four security questions",
                          "Contrast mongodb:// with mongodb+srv://",
                          "Check labels without reading secrets aloud"],
                   expected=["mongodb:// · trainingUser", "Password: placeholder only",
                             "db.example.net · 27017 · training",
                             "Secrets: env variable or secret store",
                             "+srv: DNS discovers the hosts"],
                   expected_title="Solution (after debrief)",
                   takeaway="Parse a URI aloud — without ever reading the password onto a "
                            "shared screen.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 2.2. The worksheet is "
                             "labs/day-01/exercises/exercise-2.2-interpret-a-connection-"
                             "string.md. No live connection is needed."),
                          tp("The placeholder",
                             "The worksheet and the slide both show the password as "
                             "<password>, a placeholder, so that no credential-looking value "
                             "appears on screen."),
                          tp("The database name",
                             "The sample's default database is training, not training_store. "
                             "That is deliberate: it is a generic example host, not our "
                             "class server."),
                          tp("Security answers",
                             "Never screenshot the password. Store the username and password in "
                             "environment variables or a secret store. Typical failures: wrong "
                             "password, host not found, port blocked, special characters not "
                             "encoded, TLS mismatch.")]),
        F.exercise("Exercise 2.3 — Diagnose Connection Failures",
                   "Module 2 checkpoint C: six failures, one layer at a time.",
                   kind="OFFICIAL CHECKPOINT C", minutes=15,
                   worksheet="labs/day-01/exercises/exercise-2.3-diagnose-connection-"
                             "failures.md",
                   scenario="For each case: likely cause, first check, log or setting, fix and "
                            "the command that verifies it.",
                   scenario_code="1  ECONNREFUSED\n"
                                 "2  Authentication failed\n"
                                 "3  Server-selection timeout\n"
                                 "4  DNS lookup failure\n"
                                 "5  Unauthorized command\n"
                                 "6  Invalid URI format",
                   tasks=["Diagnose cases 1 and 2",
                          "Diagnose cases 3 and 4",
                          "Diagnose cases 5 and 6",
                          "Share one case: change one thing, retest"],
                   expected=["1 server stopped or wrong port",
                             "2 user, password or authSource",
                             "3 firewall, routing or allowlist",
                             "4 hostname or DNS",
                             "5 role too weak · 6 syntax or encoding",
                             "Verify with a ping: ok: 1"],
                   expected_title="Solution (after debrief)",
                   takeaway="Timeout is not refused, and unauthorized is not unauthenticated — "
                            "name the layer first.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 2.3. The worksheet is "
                             "labs/day-01/exercises/exercise-2.3-diagnose-connection-"
                             "failures.md. Don't break a working classroom cluster unless the "
                             "instructor has set up a sandbox."),
                          tp("Cases 1 and 2",
                             "Refused: is mongod running, on port 27017? Check the service and "
                             "net.port. Authentication failed: retry with a known-good user; "
                             "the mongod log shows the failure; fix the credentials or "
                             "authSource."),
                          tp("Cases 3 and 4",
                             "Timeout: can you reach host and port? Check the Atlas IP access "
                             "list and local firewall. DNS failure: resolve the hostname; fix "
                             "it or check the VPN."),
                          tp("Cases 5 and 6",
                             "Unauthorized: the user authenticated but lacks the role; grant "
                             "it and retry. Invalid URI: read the whole string, fix the scheme "
                             "or @, and percent-encode the password."),
                          tp("The habit",
                             "Change one variable, then retest with the simplest client: "
                             "mongosh and db.runCommand({ ping: 1 }). Learners come back to "
                             "this table if a step of Lab 1 fails.")]),
        F.exercise("Exercise 2.4 — Environment Readiness Checklist",
                   "Module 2 checkpoint D: tick only what you have seen.",
                   kind="OFFICIAL CHECKPOINT D", minutes=10,
                   worksheet="labs/day-01/exercises/exercise-2.4-environment-readiness-"
                             "checklist.md",
                   scenario="Fill it in during or right after Lab 1, the next slide. No "
                            "passwords on the page.",
                   scenario_code="[ ] MongoDB installed or provisioned\n"
                                 "[ ] Server or cluster available\n"
                                 "[ ] mongosh and Compass available\n"
                                 "[ ] URI stored securely\n"
                                 "[ ] Network access configured\n"
                                 "[ ] Ping returns ok: 1\n"
                                 "[ ] Test insert and test read",
                   tasks=["Record your path, host and port",
                          "Confirm mongosh --version and Compass",
                          "Tick ping, insert and read — if seen",
                          "List each gap: symptom, layer, next step"],
                   expected=["Path recorded, no secrets",
                             "Only observed boxes ticked",
                             "Every gap has a next step",
                             "Ready for Module 3"],
                   takeaway="An honest checklist is worth more than a full one — never tick a "
                            "box you didn't prove.",
                   notes=[tp("Official checkpoint",
                             "This is the official Exercise 2.4. The worksheet is "
                             "labs/day-01/exercises/exercise-2.4-environment-readiness-"
                             "checklist.md. Introduce it now; learners complete it during or "
                             "right after Lab 1, because it records what Lab 1 proves."),
                          tp("What to record",
                             "Local, container, managed cloud or instructor-provided; the "
                             "hostname or cluster name; and the port if it isn't 27017. No "
                             "password and no full connection string."),
                          tp("The worksheet rows",
                             "The worksheet has ten rows. The slide groups a few: mongosh and "
                             "Compass share a line, credentials sit with the stored URI, and "
                             "insert and read share a line."),
                          tp("Gaps",
                             "For each unchecked item, write the symptom, the likely layer, "
                             "process, network, credentials or permission, and the next check. "
                             "Exercise 2.3's table gives the first check. Report it without "
                             "exposing credentials.")]),
        F.exercise("Lab 1 — Install, Connect and Verify",
                   "Day 1 hands-on: provision MongoDB, connect, and prove write and read.",
                   kind="OFFICIAL LAB", minutes=40,
                   worksheet="labs/day-01/lab1/LAB-1-GUIDE.md",
                   scenario="One path: A local Community Edition, B managed cloud, C an "
                            "instructor URI. The mongosh steps are the same.",
                   scenario_code="db.runCommand({ ping: 1 })\n"
                                 "use training_store\n"
                                 "db.createCollection(\n"
                                 "  \"environment_check\")\n"
                                 "db.environment_check.insertOne(\n"
                                 "  { participant: \"Student\",\n"
                                 "    status: \"READY\",\n"
                                 "    checkedAt: new Date() })\n"
                                 "db.environment_check.findOne(\n"
                                 "  { status: \"READY\" })",
                   tasks=["Install or provision on your path",
                          "Connect with mongosh and ping",
                          "Create environment_check; insert and find",
                          "insertMany, count, update your name",
                          "LAB1 probe: insert, find, update, delete",
                          "Compass, then the COMPLETE document"],
                   expected=["Ping returns ok: 1",
                             "Insert acknowledged, _id assigned",
                             "Count is 4; your name shows",
                             "LAB1 deleted: find returns nothing",
                             "Compass shows the same document",
                             "No password shared anywhere"],
                   takeaway="The lab is finished when the Exercise 2.4 checklist matches what "
                            "you actually saw.",
                   notes=[tp("Official lab",
                             "This is Day 1 Lab 1, labs/day-01/lab1/LAB-1-GUIDE.md, and it "
                             "closes Module 2. The instructor answer key is "
                             "labs/day-01/lab1/solution/LAB-1-SOLUTION.md. Learners fill in "
                             "the Exercise 2.4 checklist as they go."),
                          tp("Paths",
                             "Path A installs Community Edition and notes the config file. "
                             "Path B signs in, creates a database user, allows the current IP "
                             "and copies the URI. Path C uses an instructor-provided URI, "
                             "shared securely, never in chat."),
                          tp("The trimmed code",
                             "The slide trims the READY document. The full Step 7 document also "
                             "has environment: training and shellConnected: true, as on the "
                             "earlier insert slide."),
                          tp("Later steps",
                             "Step 8 inserts three component documents, counts 4 on a first "
                             "run, and updates participant to the learner's name. Step 9 runs "
                             "the LAB1 probe in products: insert, find, update, delete; skip "
                             "its createCollection if products already exists. Step 10 opens "
                             "the same document in Compass. Step 11 inserts module: 2, "
                             "validation: COMPLETE."),
                          tp("Before Module 3",
                             "Make sure LAB1 is gone before Module 3's Lab 2, and that every "
                             "unticked checklist box has a next step.")]),
        F.wrapup("Module 2 Summary and What's Next",
                 "From choosing a deployment to a proven environment.",
                 can=["Choose a deployment option and justify it",
                      "Explain mongod, mongosh, Compass and drivers",
                      "Install, configure, start and stop MongoDB",
                      "Read and build connection strings",
                      "Create training_store and prove CRUD",
                      "Protect credentials; troubleshoot by layer"],
                 next_title="Next: Module 3 — Data Modeling with MongoDB",
                 questions=["How do I load and inspect training_store?",
                            "When do I embed, and when do I reference?",
                            "How do BSON types and validation help?"],
                 bring=("Bring along", "Your working connection, your Exercise 2.4 checklist "
                                       "and your Exercise 2.1 table."),
                 takeaway="Your environment is proven — Module 3 loads training_store and starts "
                          "designing documents.",
                 notes=[tp("Recap",
                           "We chose a deployment, installed and started MongoDB, connected "
                           "with connection strings from mongosh and Compass, proved CRUD in "
                           "training_store, and learned to protect credentials and "
                           "troubleshoot by layer."),
                        tp("Next module",
                           "Module 3, Data Modeling with MongoDB, loads the full training_store "
                           "and uses it to decide when to embed and when to reference, which "
                           "BSON types to use, and how validation keeps data clean."),
                        tp("Bring along",
                           "A working connection, the Exercise 2.4 checklist and the Exercise "
                           "2.1 table. Anyone with an unresolved checklist item should see the "
                           "instructor before Module 3's first lab.")]),
    ]

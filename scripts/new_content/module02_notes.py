#!/usr/bin/env python3
"""Speaker notes for the new Module 2 deck (Installation and Setup).

Written from scripts/module02_content_source.md, the Module 2 manifest, the
official Exercises 2.1-2.4, the Day 1 Lab 1 guide and the training_store dataset, in
plain short sentences. Composed into the notes pane by mdb_speaker_notes.compose(),
so the layout matches the day decks: KEY TALKING POINTS / REAL-WORLD EXAMPLES /
USE-CASE SCENARIO.

Keys are topic numbers. Diagram topics (see build_module02_new.DIAGRAMS) are
merged with the diagram's own "what it shows" notes on the same slide.
"""
from __future__ import annotations


def tp(point: str, explain: str) -> dict:
    return {"point": point, "explain": explain}


NOTES: dict[int, dict] = {
    1: {
        "talking_points": [
            tp("Why this module matters",
               "Every later lab needs a working MongoDB and a client that can reach it. "
               "This module builds that environment and, just as important, proves it works."),
            tp("What this module does",
               "We choose where MongoDB runs, install or provision it, start it, connect with "
               "mongosh and Compass, run our first commands in training_store, and finish "
               "with security basics and troubleshooting."),
            tp("The quote",
               "A shell prompt is not proof. A ping proves the server answers; a write and a "
               "read prove the environment is usable. That is the standard for this module."),
            tp("Where the course goes next",
               "Module 3, Data Modeling with MongoDB, starts by loading the full training_store "
               "dataset on the environment you build today."),
        ],
        "real_world_examples": [
            "A new developer joins a team and gets a connection string on day one. "
            "Before touching application code, they connect, ping, and write and read a test "
            "document. That ten-minute check avoids hours of debugging the wrong layer later.",
        ],
    },
    2: {
        "talking_points": [
            tp("By the end of this module",
               "Walk through the six objectives on the left. "
               "Learners choose a deployment option and explain the roles of mongod, mongosh, "
               "Compass and drivers. "
               "They install or provision MongoDB, start it and connect with a connection "
               "string. "
               "They create training_store, run insert, find, update and delete checks, "
               "protect credentials and diagnose common failures."),
            tp("Six questions this module answers",
               "Where should MongoDB run? How do I install and start mongod? How does a client "
               "find the server? What proves the environment works? How do I keep passwords "
               "out of sight? And what do I check when it won't connect?"),
            tp("Set the expectation",
               "The roadmap at the bottom is also the order of the hands-on lab. "
               "The standard is proof: ping, write and read."),
        ],
    },
    5: {
        "talking_points": [
            tp("Four options, one database",
               "MongoDB can run locally with Community Edition, in a container, on a "
               "self-managed server or virtual machine, or as a managed cloud service such as "
               "MongoDB Atlas. This diagram shows three of them; the self-managed server "
               "appears in the decision flow at the end of this part."),
            tp("What stays the same",
               "The commands you type in mongosh, the documents and the training_store "
               "collections are the same in every option."),
            tp("What changes",
               "Who installs, patches, backs up, secures and scales the server. "
               "That responsibility is the real difference between the options."),
        ],
    },
    6: {
        "talking_points": [
            tp("What local means",
               "MongoDB Community Edition runs directly on the learner's computer. "
               "No internet is needed after installation."),
            tp("Best for",
               "Classroom exercises, offline development, learning administration commands, "
               "testing applications locally, and understanding the mongod server process."),
            tp("The safe default",
               "A fresh local install listens on localhost only, and access control is off by "
               "default. That is acceptable only because nobody else can reach the port. "
               "Never widen bindIp without first enabling authentication."),
        ],
    },
    7: {
        "talking_points": [
            tp("What Atlas is",
               "MongoDB Atlas is MongoDB's managed cloud platform. "
               "Atlas handles much of the infrastructure, maintenance and configuration."),
            tp("Best for",
               "Team projects, remote access, cloud application development, high "
               "availability and production-style practice."),
            tp("What you still own",
               "You still create the database users, choose which IP addresses may connect, "
               "and keep the connection string secret. Atlas requires TLS on every connection."),
        ],
    },
    8: {
        "talking_points": [
            tp("The process",
               "Sign in to Atlas, use or create an organization and a project, and create a "
               "deployment. Pick a free or paid tier, a cloud provider and a region."),
            tp("The two gates",
               "Add your current IP address to the IP access list, and create a database user "
               "with only the roles it needs. The source list gives these two steps in either "
               "order; both must exist before any client can connect."),
            tp("Two different identities",
               "An Atlas user signs in to the Atlas website. A database user authenticates "
               "when a client connects to the cluster. Don't reuse your Atlas login password "
               "as a database password."),
            tp("The connection string",
               "Copy it from the Connect dialog, because the cluster hostname is specific to "
               "your deployment. It is an SRV string, which we unpack in Part 3."),
        ],
        "use_case_scenario":
            "A distributed team needs a shared training database. The instructor creates one "
            "Atlas project, one cluster, one least-privilege database user per learner, and "
            "adds the classroom's public IP range to the access list, rather than opening the "
            "cluster to the whole internet.",
    },
    9: {
        "talking_points": [
            tp("Why containers",
               "A container gives a portable, isolated MongoDB that can be created and removed "
               "in seconds. That suits temporary test environments and CI pipelines."),
            tp("The published port",
               "The diagram's 27017:27017 maps host port 27017 to the container. "
               "By default Docker publishes that port on every network interface of the host. "
               "Our command adds 127.0.0.1 so only this machine can reach an unauthenticated "
               "server."),
            tp("The volume",
               "The named volume mongo-data is mounted at /data/db. "
               "Without it, docker rm deletes the data along with the container."),
            tp("The image",
               "mongodb/mongodb-community-server is MongoDB's own Community image. The Docker "
               "Official Image, mongo, works the same way. Pin a version tag in real projects "
               "instead of latest."),
        ],
    },
    11: {
        "talking_points": [
            tp("Internet and management",
               "Local needs no internet after installation, and you manage it yourself. "
               "Atlas needs internet, and Atlas manages the infrastructure."),
            tp("Setup and address",
               "Local setup is a software installation, reached at localhost:27017. "
               "Atlas setup is a cloud account and a cluster, reached through an Atlas "
               "connection URI."),
            tp("Remote access and best use",
               "Local remote access requires configuration; Atlas has it built in, behind "
               "access controls. Local is best for learning and local development; Atlas for "
               "cloud and team projects."),
        ],
    },
    12: {
        "talking_points": [
            tp("Walk the flow",
               "Start at the top: a classroom laptop points to local or Docker. "
               "A shared or production-like need points to managed cloud. "
               "A need for direct control of the operating system points to self-managed."),
            tp("The fourth option",
               "Self-managed means you install and operate mongod yourself on a server or "
               "virtual machine. Regulated organizations often choose it for direct control, "
               "at the cost of patching, backups and monitoring."),
            tp("Link to Exercise 2.1",
               "Exercise 2.1 gives six scenarios. Each answer must name the constraint: "
               "offline, disposable, shared, control, operations load or network."),
        ],
    },
    13: {
        "talking_points": [
            tp("The six steps",
               "Install the MongoDB Server, make sure the data and log directories exist, "
               "start the service, ping it from mongosh, connect Compass, and insert a test "
               "document."),
            tp("What a local environment contains",
               "MongoDB Community Server runs the database. mongosh is the command-line "
               "client. Compass is an optional graphical interface. The MongoDB Database Tools "
               "are optional import, export and backup utilities."),
            tp("Follow the official page",
               "MongoDB publishes install instructions for each operating system and version. "
               "Use them instead of copying commands from old blog posts."),
        ],
    },
    15: {
        "talking_points": [
            tp("mongod",
               "mongod is the database server process. It stores the data, listens on port "
               "27017 by default and does the actual work."),
            tp("mongosh",
               "mongosh is the interactive shell. It only sends commands and prints results."),
            tp("Two consequences",
               "Stopping mongosh does not stop the database. And if mongod is not running, the "
               "shell cannot connect, however correct the command is."),
        ],
    },
    16: {
        "talking_points": [
            tp("Three clients",
               "mongosh is the command-line shell, Compass is the graphical interface, and "
               "drivers are the libraries application code uses, for example the Node.js or "
               "Java driver."),
            tp("One deployment",
               "All three connect to the same mongod on the same port and see the same "
               "training_store data. A document inserted in mongosh appears in Compass after "
               "a refresh."),
            tp("What mongosh can do",
               "Create databases and collections, insert and query documents, create indexes, "
               "run aggregation pipelines, inspect server information and run administrative "
               "commands."),
        ],
    },
    17: {
        "talking_points": [
            tp("Where the file lives",
               "On Linux it is usually /etc/mongod.conf, and Homebrew on macOS puts one under "
               "its etc folder. The Windows installer writes mongod.cfg in the server's bin "
               "folder. The format is YAML in every case."),
            tp("The four settings",
               "storage.dbPath is the data directory. systemLog.path is the log file. "
               "net.port is the port, 27017 by default. net.bindIp is the address mongod "
               "listens on."),
            tp("Paths vary",
               "Package installs pick their own default paths, such as /var/lib/mongodb on "
               "Ubuntu or a data folder under Program Files on Windows. That is why the lab "
               "asks you to note the configuration file location."),
            tp("bindIp is a security setting",
               "Keep 127.0.0.1 for a local learning server. Binding to 0.0.0.0 exposes mongod "
               "to every network the machine is on. Only do that behind a firewall, with "
               "authentication and TLS enabled."),
        ],
    },
    20: {
        "talking_points": [
            tp("Start",
               "When mongod starts, it reads its configuration, opens the data directory, "
               "listens on port 27017 and is then ready for mongosh and Compass."),
            tp("Stop",
               "A clean shutdown lets clients disconnect, flushes data from memory to disk, "
               "closes the files and exits. After that the port is closed."),
            tp("Use the service manager",
               "Use Stop-Service on Windows, brew services on macOS and systemctl on Linux. "
               "Killing the process risks an unclean shutdown."),
            tp("Admin rights",
               "Start-Service and Stop-Service need an Administrator PowerShell; systemctl "
               "needs sudo. enable makes mongod start again after a reboot."),
        ],
    },
    22: {
        "talking_points": [
            tp("The prompt",
               "After connecting, the shell shows a prompt like test>. "
               "The word test is the currently selected database."),
            tp("Versions",
               "mongosh --version runs in the operating-system terminal and prints the shell "
               "version. db.version() runs inside mongosh and prints the server version. "
               "They are two different programs, so the numbers differ."),
            tp("Ping",
               "db.runCommand({ ping: 1 }) returns ok: 1 when the server answers. "
               "Ping proves reachability, not permission to write."),
            tp("Connection details",
               "db shows the current database. db.getMongo() shows the connection the shell "
               "is using. show dbs lists only databases that hold data, so training_store "
               "appears there once it has a document."),
        ],
    },
    24: {
        "talking_points": [
            tp("Localhost",
               "localhost and 127.0.0.1 mean this machine. Traffic never leaves it, which is "
               "why a local learning server can run without TLS."),
            tp("Remote",
               "A remote mongod is reached by hostname and port across a network. "
               "It needs the port open in firewalls, TLS on the wire, and authentication."),
            tp("The configuration link",
               "A remote client can reach mongod only if bindIp includes an address on that "
               "network. Widening bindIp without authentication and a firewall is how "
               "databases end up exposed on the internet."),
        ],
    },
    26: {
        "talking_points": [
            tp("Why connection strings",
               "Every client, mongosh, Compass or a driver, needs the same facts: which "
               "protocol, which user, which hosts and ports, which database and which options. "
               "The connection string holds all of them in one line."),
            tp("The standard format",
               "mongodb:// lists every host explicitly, each with an optional port. "
               "The port defaults to 27017."),
            tp("authSource",
               "authSource names the database that stores the user's credentials, often "
               "admin. A wrong authSource is a common cause of authentication failed."),
            tp("Special characters",
               "If a password contains characters such as @, colon or slash, it must be "
               "percent-encoded in the URI. Better still, don't put it in the URI at all."),
        ],
    },
    27: {
        "talking_points": [
            tp("How SRV works",
               "mongodb+srv:// gives one hostname. The client looks up the DNS SRV record "
               "_mongodb._tcp plus that hostname and gets the list of members and ports."),
            tp("Why cloud services use it",
               "Atlas connection strings use this form. The string stays short, and members "
               "can change without editing every application's configuration."),
            tp("Defaults",
               "An SRV string turns TLS on by default and never includes a port. "
               "If DNS can't resolve the name, the connection fails before it reaches "
               "MongoDB."),
        ],
    },
    30: {
        "talking_points": [
            tp("Same string, different client",
               "Compass takes the same connection string as mongosh. Paste it, connect, and "
               "browse databases, collections and documents."),
            tp("Keep the secret out of sight",
               "When the URI includes a password, never screenshot or project the connection "
               "dialog. Use the separate password field, and don't save the password on a "
               "shared machine."),
            tp("Four collections later",
               "The diagram shows the full training_store with products, customers, orders "
               "and reviews. On a new server you will see only what you have created; the "
               "four collections arrive when the dataset is loaded."),
        ],
    },
    33: {
        "talking_points": [
            tp("use changes context only",
               "use training_store switches the current database. It does not create anything "
               "on disk, so show dbs does not list training_store yet."),
            tp("Explicit or implicit",
               "db.createCollection creates an empty collection and returns ok: 1. Or skip it: "
               "the first insertOne creates both the collection and the database."),
            tp("Lab 1",
               "Day 1 Lab 1 creates environment_check explicitly in Step 6, and products "
               "explicitly in Step 9, exactly as in the top half of the diagram, on an empty "
               "server. The Predict the Shell Output exercise shows the implicit way: the "
               "first insertOne creates environment_check."),
            tp("The diagram's TS-001",
               "The diagram's implicit example inserts a throwaway SKU, TS-001. It is not a "
               "training_store product, so we don't insert it; Lab 1 uses its own probe, LAB1, "
               "and deletes it."),
            tp("On a loaded database",
               "If training_store is already loaded, for example on an instructor-provided "
               "server, createCollection on an existing name such as products fails with "
               "Collection already exists. That is expected; the collection is already there."),
        ],
    },
    38: {
        "talking_points": [
            tp("Authentication",
               "Authentication proves identity. The client sends a username and password; "
               "mongod checks them against the authentication database named by authSource."),
            tp("Authorization",
               "Authorization applies roles. Here readWrite on training_store allows find, "
               "insert and update in that database, and nothing else."),
            tp("Local defaults",
               "A fresh local Community install has access control turned off, which is "
               "tolerable only on localhost. Atlas always requires a database user."),
            tp("Prompt for the password",
               "Pass --username and let mongosh prompt for the password, so it never appears "
               "in the command line or shell history."),
        ],
    },
    40: {
        "talking_points": [
            tp("Unsafe",
               "Passwords pasted into chat or screenshots, and URIs with passwords hard-coded "
               "in scripts or committed to Git. Once shared, a password must be treated as "
               "leaked."),
            tp("Safe",
               "Keep the URI in an environment variable, let mongosh prompt for the password, "
               "or fetch the secret from a secret store at runtime."),
            tp("Network access",
               "For a temporary learning cluster, people sometimes allow 0.0.0.0/0. That opens "
               "the cluster to every address on the internet. Prefer your own IP or the "
               "classroom range; if you must use it, pair it with strong credentials, never "
               "use it in production, and remove it after class."),
            tp("Environment variables and history",
               "Setting the variable with the password typed inline still records it in the "
               "shell history. Prefer a prompt or a secret store."),
        ],
    },
    42: {
        "talking_points": [
            tp("mongosh: command not found",
               "Before any of these: mongosh is not installed, its folder is not on the PATH, "
               "or the terminal was not reopened after installation."),
            tp("Connection refused",
               "Nothing is listening: the mongod service is stopped, it uses a different port, "
               "its bindIp excludes your address, or something blocks the port."),
            tp("Timeout",
               "No answer at all: a firewall, routing, a corporate proxy or the Atlas IP "
               "access list. A refused connection answers quickly; a timeout waits."),
            tp("Authentication failed",
               "Check the database username, the password, authSource, and special characters "
               "that need encoding. An Atlas login is not a database user."),
        ],
    },
    43: {
        "talking_points": [
            tp("Work in order",
               "Is mongod running? Is the port and bindIp right? Are the credentials valid? "
               "Is the network and TLS path open? Each check depends on the one before."),
            tp("One change at a time",
               "Change one variable, then retest with the simplest client: mongosh and a ping. "
               "Changing three settings at once hides which one fixed it."),
            tp("Where to look",
               "The server log, set by systemLog.path, records startup errors such as a "
               "missing dbPath or a port already in use. The client's error message names the "
               "layer."),
        ],
        "use_case_scenario":
            "A learner's Compass says connection refused. The instructor asks one question at "
            "a time: Get-Service MongoDB shows Stopped. Start-Service fixes the first layer, a "
            "ping returns ok: 1, and Compass connects without any other change.",
    },
    45: {
        "talking_points": [
            tp("Deploy and install",
               "Local, container, self-managed or managed cloud. Install mongod, or provision "
               "a cluster with a user and an IP allowlist."),
            tp("Connect",
               "A connection string tells mongosh, Compass and drivers where the server is."),
            tp("First write and read",
               "Ping proves reachability; a write and a read in training_store prove the "
               "environment is usable."),
            tp("Secure and troubleshoot",
               "Keep credentials out of code and screens, and diagnose failures layer by "
               "layer."),
        ],
    },
}

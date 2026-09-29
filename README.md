# Mastering MongoDB

Instructor-led course, 3 days. Innovation In Software Corporation.

This repository is the class copy: the slide PDFs and the hands-on guides. Start with the lab index, not this file.

| | |
| --- | --- |
| **Duration** | 3 days |
| **Level** | Introductory to intermediate |
| **Your laptop** | Windows 10 or 11, MongoDB on `localhost:27017` |
| **Labs** | [labs/README.md](labs/README.md) |

---

## Before Day 1

Install on each participant laptop, and on the instructor demo laptop, using [labs/WINDOWS-LAB-SETUP.md](labs/WINDOWS-LAB-SETUP.md):

| Software | Version |
| --- | --- |
| MongoDB Community Server | **8.3.11**, as a Windows service |
| MongoDB Compass | The copy bundled with the server installer |
| MongoDB Shell (`mongosh`) | **2.12.0** |
| MongoDB Database Tools | **100.19.0** (`mongodump`, `mongorestore`) |

The server listens on `127.0.0.1` port `27017`. Access control stays off. The laptop is a standalone server, not a replica set.

The lab technician's job list, including the class replica set for Lab 6, is [labs/LAB-TECHNICIAN-README.md](labs/LAB-TECHNICIAN-README.md).

---

## Slides

One PDF per module, in teaching order.

| Day | Deck |
| --- | --- |
| — | [Course introduction](slides/MongoDB_Course_Introduction.pdf) |
| 1 | [Module 1 — Introduction to NoSQL Databases](slides/MongoDB_Module01_Introduction_to_NoSQL_Databases.pdf) |
| 1 | [Module 2 — Installation and Setup](slides/MongoDB_Module02_Installation_and_Setup.pdf) |
| 1 | [Module 3 — Data Modeling with MongoDB](slides/MongoDB_Module03_Data_Modeling_with_MongoDB.pdf) |
| 2 | [Module 4 — The MongoDB Query Language](slides/MongoDB_Module04_The_MongoDB_Query_Language.pdf) |
| 2 | [Module 5 — The Aggregation Framework](slides/MongoDB_Module05_The_Aggregation_Framework.pdf) |
| 3 | [Module 6 — Indexing and Query Performance](slides/MongoDB_Module06_Indexing_and_Query_Performance.pdf) |
| 3 | [Module 7 — Introduction to Replication and Sharding](slides/MongoDB_Module07_Introduction_to_Replication_and_Sharding.pdf) |
| 3 | [Module 8 — Best Practices, Security, and Troubleshooting](slides/MongoDB_Module08_Best_Practices_Security_and_Troubleshooting.pdf) |

---

## Labs

Full sequence, worksheets, and answer-key locations: [labs/README.md](labs/README.md). Indexes: [exercises](labs/EXERCISES-INDEX.md) · [labs](labs/LABS-INDEX.md).

| Day | Lab | Where it runs |
| --- | --- | --- |
| 1 | [Lab 1 — Install, connect, and verify](labs/day-01/lab1/LAB-1-GUIDE.md) | Participant laptop |
| 1 | [Lab 2 — Create and populate `training_store`](labs/day-01/lab2/LAB-2-GUIDE.md) | Participant laptop |
| 2 | [Lab 3 — Complex queries and updates](labs/day-02/lab3/LAB-3-GUIDE.md) | Participant laptop |
| 2 | [Lab 4 — Aggregation pipeline](labs/day-02/lab4/LAB-4-GUIDE.md) | Participant laptop |
| 3 | [Lab 5 — Index and explain](labs/day-03/lab5/LAB-5-GUIDE.md) | Participant laptop |
| 3 | [Lab 6 — Replication and sharding](labs/day-03/lab6/LAB-6-GUIDE.md) | Steps 1–3 on paper or the laptop. Steps 4–7 on the class replica set. |
| 3 | [Lab 7 — Production readiness](labs/day-03/lab7/LAB-7-GUIDE.md) | Participant laptop |

The sample loader, `datasets/training_store/load.js`, comes in the course folder the instructor distributes. It is not in this repository. From that folder, reload before a lab that needs a fresh `training_store`:

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

A fresh load prints 6 customers, 13 products, 17 orders, 6 reviews, and 13 paid orders.

Solution folders (`exercises/solution/`, `labN/solution/`) are for the instructor. Participant machines get the guides and the loader.

---

## Two environments

| Environment | Used for |
| --- | --- |
| Participant laptop, `mongodb://localhost:27017` | Labs 1–5, Lab 6 Steps 1–3, Lab 7 |
| One shared class replica set | Lab 6 Steps 4–7 only |

The instructor gives the replica-set host and the class username in class. Type the password at the `mongosh` prompt. Do not put a password, or a URI that contains a password, in a slide, a worksheet, chat, or this repository.

Lab 7 dump and restore stay on the laptop. Do not point `mongodump` or `mongorestore` at the class replica set.

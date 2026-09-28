# Labs and exercises

Everything learners do hands-on, in the order it happens in the module decks (`decks/pptx_new/`). Indexes: [EXERCISES-INDEX.md](EXERCISES-INDEX.md) · [LABS-INDEX.md](LABS-INDEX.md).

**Before Day 1:** [Windows lab setup](WINDOWS-LAB-SETUP.md) — Community Server **8.3.11** as a service, Compass connected to `localhost:27017`, `mongosh` **2.12.0**, and Database Tools **100.19.0** on a Windows 10/11 laptop. The job list for the lab technician, including the class replica set for Lab 6, is [LAB-TECHNICIAN-README.md](LAB-TECHNICIAN-README.md).

```text
labs/
  day-01/  exercises/ (1.x-3.x)  exercises/solution/  lab1/  lab2/
  day-02/  exercises/ (4.x-5.x)  exercises/solution/  lab3/  lab4/
  day-03/  exercises/ (6.x-8.x)  exercises/solution/  lab5/  lab6/  lab7/
  practice-exercises/            module-01-README.md ... module-08-README.md
```

## Sequence by day

### Day 1

- **Module 1 — Introduction to NoSQL Databases** (`decks/pptx_new/MongoDB_Module01_Introduction_to_NoSQL_Databases.pptx`)
  - Exercises: 1.1 Choose the Appropriate Data Model · 1.2 Convert Relational Rows into a Document · 1.3 Explore a MongoDB Dataset
- **Module 2 — Installation and Setup** (`decks/pptx_new/MongoDB_Module02_Installation_and_Setup.pptx`)
  - Exercises: 2.1 Select a Deployment Option · 2.2 Interpret a Connection String · 2.3 Diagnose Connection Failures · 2.4 Environment Readiness Checklist
  - Then **Lab 1 — Install, Connect and Verify**: [day-01/lab1/LAB-1-GUIDE.md](day-01/lab1/LAB-1-GUIDE.md)
- **Module 3 — Data Modeling with MongoDB** (`decks/pptx_new/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx`)
  - Exercises: 3.1 Identify Document Components · 3.2 Discover Application Access Patterns · 3.3 Embed or Reference? · 3.4 Model a Product Catalog · 3.5 Model an Order Document · 3.6 Find and Correct Schema Anti-Patterns · 3.7 Select a Schema Design Pattern · 3.8 Design Collection Validation · 3.9 Design a Support-Ticket Data Model
  - Then **Lab 2 — Create and Populate training_store**: [day-01/lab2/LAB-2-GUIDE.md](day-01/lab2/LAB-2-GUIDE.md)

### Day 2

- **Module 4 — The MongoDB Query Language** (`decks/pptx_new/MongoDB_Module04_The_MongoDB_Query_Language.pptx`)
  - Exercises: 4.1 Build Comparison Filters · 4.2 Query Arrays of Documents · 4.3 Perform an Upsert · 4.4 Correct Unsafe Operations
  - Then **Lab 3 — Complex Queries and Updates**: [day-02/lab3/LAB-3-GUIDE.md](day-02/lab3/LAB-3-GUIDE.md)
- **Module 5 — The Aggregation Framework** (`decks/pptx_new/MongoDB_Module05_The_Aggregation_Framework.pptx`)
  - Exercises: 5.1 Arrange Pipeline Stages · 5.2 Build a Top-N Report · 5.3 Join Related Collections · 5.4 Correct a Broken Pipeline
  - Then **Lab 4 — Aggregation Pipeline**: [day-02/lab4/LAB-4-GUIDE.md](day-02/lab4/LAB-4-GUIDE.md)

### Day 3

- **Module 6 — Indexing and Query Performance** (`decks/pptx_new/MongoDB_Module06_Indexing_and_Query_Performance.pptx`)
  - Exercises: 6.1 Apply Equality–Sort–Range · 6.2 Identify Covered Queries · 6.3 E-Commerce Index Review
  - Then **Lab 5 — Index and Explain**: [day-03/lab5/LAB-5-GUIDE.md](day-03/lab5/LAB-5-GUIDE.md)
- **Module 7 — Introduction to Replication and Sharding** (`decks/pptx_new/MongoDB_Module07_Introduction_to_Replication_and_Sharding.pptx`)
  - Exercises: 7.1 Replication or Sharding? · 7.2 Select Read and Write Settings · 7.3 Evaluate Shard-Key Candidates · 7.4 Targeted or Scatter-Gather?
  - Then **Lab 6 — Replication and Sharding**: [day-03/lab6/LAB-6-GUIDE.md](day-03/lab6/LAB-6-GUIDE.md)
- **Module 8 — MongoDB Best Practices, Security, and Troubleshooting** (`decks/pptx_new/MongoDB_Module08_Best_Practices_Security_and_Troubleshooting.pptx`)
  - Exercises: 8.1 Review a Query and Projection · 8.2 Design Least-Privilege Roles · 8.3 Define RPO and RTO
  - Then **Lab 7 — Production Readiness**: [day-03/lab7/LAB-7-GUIDE.md](day-03/lab7/LAB-7-GUIDE.md)

## Conventions

- **Participant worksheets** (`exercises/exercise-M.N-*.md`) state the scenario, tasks, time and deliverable — no answers.
- **Answer keys** (`exercises/solution/`) and **lab solutions** (`labN/solution/`) are for instructors; keep them out of the participant hand-out.
- Every command, value and expected result matches `datasets/training_store/load.js` on a fresh load. Expected outputs were worked out from the dataset; run the key examples once in mongosh before class.
- Never type a real password into a slide, worksheet, URI or chat: let `mongosh` prompt, or use `<password>` placeholders.

# Labs — one hands-on lab per module block

Seven sequenced labs run on the shared `training_store` dataset ([`datasets/training_store/load.js`](../datasets/training_store/load.js)). Each lab is the last official slide of the module it follows. Every lab has a participant guide and an instructor solution with the expected output of each step.

| Lab | Day | After module | Guide | Solution |
| --- | --- | ------------ | ----- | -------- |
| 1 | 1 | 2 Installation and Setup | [Install, Connect and Verify](day-01/lab1/LAB-1-GUIDE.md) | [solution](day-01/lab1/solution/LAB-1-SOLUTION.md) |
| 2 | 1 | 3 Data Modeling with MongoDB | [Create and Populate training_store](day-01/lab2/LAB-2-GUIDE.md) | [solution](day-01/lab2/solution/LAB-2-SOLUTION.md) |
| 3 | 2 | 4 The MongoDB Query Language | [Complex Queries and Updates](day-02/lab3/LAB-3-GUIDE.md) | [solution](day-02/lab3/solution/LAB-3-SOLUTION.md) |
| 4 | 2 | 5 The Aggregation Framework | [Aggregation Pipeline](day-02/lab4/LAB-4-GUIDE.md) | [solution](day-02/lab4/solution/LAB-4-SOLUTION.md) |
| 5 | 3 | 6 Indexing and Query Performance | [Index and Explain](day-03/lab5/LAB-5-GUIDE.md) | [solution](day-03/lab5/solution/LAB-5-SOLUTION.md) |
| 6 | 3 | 7 Introduction to Replication and Sharding | [Replication and Sharding](day-03/lab6/LAB-6-GUIDE.md) | [solution](day-03/lab6/solution/LAB-6-SOLUTION.md) |
| 7 | 3 | 8 MongoDB Best Practices, Security, and Troubleshooting | [Production Readiness](day-03/lab7/LAB-7-GUIDE.md) | [solution](day-03/lab7/solution/LAB-7-SOLUTION.md) |

Reload `training_store` at the start of Day 2 and Day 3 (and whenever a lab's *Before you start* section asks):

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

Superseded day-lab files from the earlier layout are in [`../archive/labs/`](../archive/labs/).

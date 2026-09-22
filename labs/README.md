# Mastering MongoDB — Student Labs

These are the **day labs** named in [`Mastering_MongoDB_Course_Outline.docx`](../Mastering_MongoDB_Course_Outline.docx). They run against the shared `training_store` dataset and match the PowerPoint module decks in `decks/pptx/`.

In-class micro-exercises (discussion plus short keyboard work) stay in [`slide-exercises/`](../slide-exercises/). Use this folder when you want one sequenced lab per teaching block.

| | |
|---|---|
| **Environment** | Windows 10/11 · PowerShell · `mongosh` |
| **Database** | `training_store` (`products`, `customers`, `orders`, `reviews`) |
| **Load script** | [`datasets/training_store/load.js`](../datasets/training_store/load.js) |
| **Do not use** | SKUs such as `ELEC-1001`, categories `Electronics` / `Furniture`, field `stock`, or order status `Processing` — those names appear on some concept slides as generic examples. The live dataset uses the names in the tables below. |

---

## Field map (slides → live dataset)

| Concept on some PPT examples | Live `training_store` field |
|------------------------------|-----------------------------|
| `category: "Electronics"` | `LAPTOP`, `SHOE`, `BOOK`, `ACCESSORY` |
| `sku: "ELEC-1001"` | `L100`, `A410`, `P1001`, … |
| `stock` | Catalog products have **no** stock field. Lab 3 adds `stockQuantity` on one SKU for the inventory step only. |
| `status: "Processing"` (orders) | `paymentStatus` (`PAID` / `PENDING` / `FAILED`) and `fulfillmentStatus` (`NEW` / `PROCESSING` / `SHIPPED` / `DELIVERED`) |
| `orderedAt` | `createdAt` |
| `firstName` / `lastName` / `email` | `name.first`, `name.last`, `contact.email` |
| `reviewText` / `comment` | `body` |

After a fresh load: **13 products, 6 customers, 17 orders (13 PAID), 6 reviews**.

---

## Lab sequence

| Day | Lab | Outline hands-on | PPT deck | Time |
|-----|-----|------------------|----------|------|
| 1 | [Lab 1 — Install, connect, and verify](day-01-lab-01-install-connect-verify.md) | Module 2 practical lab | `MongoDB_Module02_Installation_and_Setup.pptx` | 40 min |
| 1 | [Lab 2 — Model and populate](day-01-lab-02-model-and-populate.md) | Creating and populating collections | `MongoDB_Module03_Data_Modeling_with_MongoDB.pptx` | 50–90 min |
| 2 | [Lab 3 — Complex queries and updates](day-02-lab-03-complex-queries-and-updates.md) | Constructing complex queries and data manipulations | `MongoDB_Module04_The_MongoDB_Query_Language.pptx` | 60–75 min |
| 2 | [Lab 4 — Aggregation pipeline](day-02-lab-04-aggregation-pipeline.md) | Building an aggregation pipeline | `MongoDB_Module05_The_Aggregation_Framework.pptx` | 45–60 min |
| 3 | [Lab 5 — Index and explain](day-03-lab-05-index-and-explain.md) | Tuning the pipeline with indexes | `MongoDB_Module06_Indexing_and_Query_Performance.pptx` | 40–50 min |
| 3 | [Lab 6 — Replication and sharding](day-03-lab-06-replication-and-sharding.md) | High availability vs scale (discussion + inspect) | `MongoDB_Module07_Introduction_to_Replication_and_Sharding.pptx` | 30–40 min |
| 3 | [Lab 7 — Production readiness](day-03-lab-07-production-readiness.md) | Best practices close | `MongoDB_Module08_MongoDB_Best_Practices_Security_and_Troubleshooting.pptx` | 45–60 min |

**Connect an application** (course objective, not a numbered outline lab): [`sample-app/README.md`](../sample-app/README.md). Run it after Lab 1.

---

## Time-boxed track (3-day package)

Complete **Labs 1, 2 (load.js path), 3, 4, 5, and 7**. Lab 6 uses an Atlas replica set if available; otherwise do the discussion tables only.

## Full track

Also complete the matching guides in `slide-exercises/module-NN/` (Labs 3.1–3.7, 4.1–4.10, 5.1–5.10, 6.1–6.11, 7.1–7.10, 8.1–8.11).

---

## Start of each day

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

Atlas: replace the URI. Reload at the start of Day 2 and Day 3 if earlier writes remain.

---

## Success bar

You can leave the course if you can: connect, explain the document model, write filters and updates, build a multi-stage pipeline, read `explain()` plan shape, and say whether `training_store` is production-ready (it is not — and you can name why).

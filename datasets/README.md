# training_store — shared sample application dataset

All three days use this one catalog. Do not invent a second application for later modules.

| Collection | Role |
|------------|------|
| `products` | Catalog with category-specific `attributes` (laptop, shoe, book, accessory) |
| `customers` | Nested name/contact and a bounded `addresses` array |
| `orders` | Line-item **snapshots** plus a **customer reference** |
| `reviews` | Stored separately so product documents stay bounded |

## Load

MongoDB must already be running. From the course repository root:

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

Atlas:

```powershell
mongosh "<your-atlas-connection-string>" .\datasets\training_store\load.js
```

The script **drops** the four collections, then inserts the teaching set and unique indexes on `sku`, `customerNumber`, and `orderNumber`. Reload at the start of Day 2 and Day 3 if lab writes remain.

Details, fixtures, and expected analytical facts: [`training_store/README.md`](training_store/README.md).

## Counts after a fresh load

| Collection | Documents |
|------------|-----------|
| `customers` | 6 |
| `products` | 13 |
| `orders` | 17 (13 PAID) |
| `reviews` | 6 |

## Student labs

Day labs that use this data: [`labs/README.md`](../labs/README.md).

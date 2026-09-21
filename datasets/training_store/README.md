# training_store dataset

Sample application data for Module 1 Lab 1.3, Module 3 labs, and Days 2–3. Collections: `customers`, `products`, `orders`, `reviews`.

Products use **different category-specific `attributes`** so learners see flexible schema in one collection. Orders **embed** line-item snapshots and **reference** the customer.

## Load (instructor, before class or to catch up)

MongoDB must already be running. From the course repository root:

```powershell
mongosh "mongodb://localhost:27017" .\datasets\training_store\load.js
```

Atlas:

```powershell
mongosh "<your-atlas-connection-string>" .\datasets\training_store\load.js
```

Expected counts after the full loader:

| Collection | Documents | Notes |
|------------|-----------|--------|
| `customers` | 6 | C101, C204, C310, C412, C515 (INACTIVE), C620 |
| `products` | 13 | Four categories; `L190` inactive; `XBAD` has a string `price` for `$type` labs |
| `orders` | 17 | **13 PAID**; O5001/O6401/O6499 PENDING; O6402 FAILED. O5001 is the `$elemMatch` trap (L100 qty 1 + A410 qty 2); O6401 has L100 qty 2 |
| `reviews` | 6 | Ratings 3–5 across July–September 2026 |

Module 3 Labs 3.1–3.4 still build a smaller core by hand (three products, customer C101, order O5001). Reload `load.js` at the start of Day 2 so Modules 4–5 have the analytical volume. Reload again at the start of Day 3 if writes remain; Module 6 then creates indexes on this same data (the set is small — teach `explain()` plan shape, not wall-clock time).

O6499 uses a non-matching `customerId` so Module 5 `$lookup` labs can practice unmatched joins. Several paid orders omit `shippingFee` so `$ifNull` has a real missing field.

Module 4 teaching fixtures (do not remove):

| Need | Fixture |
|------|---------|
| `$elemMatch` trap | `O5001` has L100 qty 1 **and** A410 qty 2; `O6401` has L100 qty 2 |
| Null vs missing phone | `C204.contact.phone` is BSON null; `C515` has no `phone` field |
| String price | `XBAD` |
| `$exists` discount | `P1001`, `B310` |
| `$unset` leftover | `A410.temporaryNote` |
| `$rename` leftover | `L190.legacyName` |
| Discontinued tag | `L190` |
| Lab insert SKUs | `A610`–`A612`, `A620`, `A700`, `A800`, `A900`, `TEMP-*` |

## Collections

| Collection | Role |
|------------|------|
| `customers` | Buyer profiles with nested name, contact, and a bounded `addresses` array |
| `products` | Catalog with laptop, shoe, book, and accessory `attributes` |
| `orders` | Order aggregate: customer reference, embedded items and shipping snapshot |
| `reviews` | Product reviews stored separately (not an unbounded array on the product) |

## Analytical facts instructors can use in Module 5

- Paid-order count: **13**
- Highest-revenue SKU on paid orders: **L110** (2 × 1899.99)
- Top customer by paid `total`: **C101** (Aisha Khan)
- Paid months present: **2026-07, 2026-08, 2026-09**
- High-value paid orders (`total` ≥ 1000): O6101, O6202, O6301, O6304

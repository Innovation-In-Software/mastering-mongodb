# Exercise 6.3 — solution (instructor)

**Module 6** · Day 3 · Checkpoint C (practical challenge)  
**Type:** design review · **Do not hand this sheet to participants.**

Worksheet: [`../exercise-6.3-e-commerce-index-review.md`](../exercise-6.3-e-commerce-index-review.md) · Deck slide 48

## Running it

Allow 30 to 45 minutes. Small groups fill the ten-row table, then each group presents two rows and its overlap. Reveal the table below only after the groups share.

## Tasks 1 and 2 — Solution table

| # | Query shape | Index key | Type | Name | After `load.js` |
| --- | --- | --- | --- | --- | --- |
| 1 | `find({ sku })` | `{ sku: 1 }` | single-field, **unique** | `sku_unique` (Lab 5, Step 9 rebuilds it as `uq_products_sku`) | **Exists** |
| 2 | `find({ category, active: true }).sort({ price: 1 })`, optional price range | `{ category: 1, active: 1, price: 1 }` — or `{ category: 1, price: 1 }` **partial** on `active: true` if every browse asks for active products | compound (or compound + partial) | `idx_products_category_active_price` / `idx_active_products_category_price` | Create |
| 3 | `find({ tags: "wireless" })` | `{ tags: 1 }` | **multikey** (automatic: `tags` is an array) | `idx_products_tags` | Create |
| 4 | `find({ "contact.email": … })` | `{ "contact.email": 1 }` | single-field, **unique** | `email_unique` | **Exists** — optional extra: case-insensitive `uq_customers_email_ci` with collation strength 2 |
| 5 | `find({ orderNumber })` | `{ orderNumber: 1 }` | single-field, **unique** | `orderNumber_unique` | **Exists** |
| 6 | `find({ customerId }).sort({ createdAt: -1 })` | `{ customerId: 1, createdAt: -1 }` | compound | `idx_orders_customer_date` | Create |
| 7 | `find({ paymentStatus: "PAID", createdAt: { $gte } }).sort({ createdAt: -1 })` | `{ paymentStatus: 1, createdAt: -1 }` | compound | `idx_orders_payment_created` | Create |
| 8 | `db.reviews.find({ productId }).sort({ createdAt: -1 })` | `{ productId: 1, createdAt: -1 }` | compound | `idx_reviews_product_created` | Create |
| 9 | the server deletes sessions whose `expiresAt` has passed | `{ expiresAt: 1 }`, `expireAfterSeconds: 0` | **TTL** on `sessions` | `ttl_sessions_expires_at` | Create (`sessions` isn't in `load.js`) |
| 10 | `find({ "attributes.connection": "Bluetooth" })`, other paths per category | `{ "attributes.$**": 1 }` | **wildcard** | `idx_products_attributes_wildcard` | Create |

Slide summary: a ten-row table · `uq_products_sku`, `idx_products_tags` · TTL on sessions · wildcard attributes · overlap: category vs category + active + price · baseline → create → explain → rollback.

**Not specialized:** workloads 6, 7 and 8 are plain compound indexes. Nothing here needs text, 2dsphere or hashed. TTL goes on `sessions` only — never `orders`, which must be kept.

**Duplicates are rejected.** Rows 1, 4 and 5 already exist. `createIndex({ sku: 1 }, { unique: true, name: "uq_products_sku" })` on a fresh load fails because `sku_unique` covers the same key; drop `sku_unique` first if the course name is wanted (Lab 5, Step 9). Row 4's case-insensitive index is allowed alongside `email_unique` only because its collation differs.

## Task 3 — ESR roles and cost notes

| # | Equality | Sort | Range | Cost note |
| --- | --- | --- | --- | --- |
| 2 | `category`, `active` | `price` | optional `price` range | Maintained on every product insert and every price or `active` change. The partial version holds 12 of 13 products (not L190), so it is slightly smaller. |
| 6 | `customerId` | `createdAt` | optional `createdAt` range | One key per order; every order insert now updates `_id_`, `orderNumber_unique` and this index. |
| 7 | `paymentStatus` | `createdAt` | `createdAt` ≥ start | Every payment-status change rewrites its key. `paymentStatus` has only 3 values, but it is equality, so it still leads. |
| 8 | `productId` | `createdAt` | — | Small: 6 reviews. Grows with every review written. |

Single-field and specialized costs worth saying out loud: the tags index holds **26 keys for 13 products** (one per array value); a wildcard index adds a key for every attribute path value — shoe `sizes` arrays add one per element — so it is the most expensive index on products per write. Use it only if the dynamic-attribute search really is a recurring workload.

## Task 4 — Overlap, validation and rollback

**Overlap.** A single `{ category: 1 }` index overlaps with every category-leading compound (`idx_products_category_active_price`, and in the lab also `idx_active_products_category_price` and `idx_products_category_price_name`): every category-only query can use the compound's prefix. Plan: `hideIndex` the candidate, run the catalog queries with `explain()`, watch `$indexStats`, then decide retain / redesign / remove. Drop only when the queries stay healthy.

**Validation (fresh `training_store`).**

| Index | Baseline (before) | After |
| --- | --- | --- |
| Catalog `idx_products_category_active_price` — `find({ category: "ACCESSORY", active: true }).sort({ price: 1 })` | `SORT` ← `COLLSCAN` · 0 keys · 13 docs · 5 returned | `FETCH` ← `IXSCAN` · 5 · 5 · 5 · no `SORT` |
| History `idx_orders_customer_date` — C101, `sort({ createdAt: -1 })` | `SORT` ← `COLLSCAN` · 0 keys · 17 docs · 5 returned | `FETCH` ← `IXSCAN` · 5 · 5 · 5 · no `SORT` |

Steps: record the baseline `explain("executionStats")` → `createIndex` with a name (in a change window, watching CPU, I/O and latency) → explain again → compare examined with returned and check that `SORT` is gone.

**Rollback.** `db.<collection>.dropIndex("<name>")`, with the original `createIndex` command saved so it can be rebuilt. For a removal, hide first — `unhideIndex` is instant, a drop means a rebuild.

## What to listen for

- A new unique index on `sku`, `contact.email` or `orderNumber` without checking what `load.js` built.
- TTL on `orders` "to clean up old orders" — never.
- A wildcard or text index "just in case" on every collection.
- `{ createdAt: -1, customerId: 1 }` for history — range/sort field first; customerId must lead.
- `email` instead of `contact.email`, `orderedAt` instead of `createdAt`, `status` instead of `paymentStatus` / `fulfillmentStatus`.

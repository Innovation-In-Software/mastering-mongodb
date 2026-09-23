# Module 3 — Practice exercise solutions

**Deck:** `decks/pptx_new/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx`  
**Dataset:** `training_store` ([`datasets/training_store/load.js`](../../datasets/training_store/load.js))  
Attempt the slide activity first, then compare your answers here.

Official numbered checkpoints for this module: [Exercises 3.1–3.9](../day-01/exercises/) (slides 42–50) and [Lab 2](../day-01/lab2/LAB-2-GUIDE.md) (slide 51).

---

## Exercise: Classify the training_store Relationships

**Slide 17** · **Time:** 10 minutes · **How to run:** pairs, five minutes, then compare. Each pair justifies one answer out loud.

### Scenario

Five relationships from the dataset. For each, decide how many sit on the many side and whether it grows without limit.

```text
1  customer → addresses
2  order → line items
3  customer → orders
4  product → reviews
5  orders ↔ products
```

### Tasks

1. Name each relationship's type.
2. Say bounded or unbounded, and why.
3. Decide: embed or reference.
4. Find the field that links each pair.

### Solution

| # | Relationship | Type | Growth | Model | Linking field in training_store |
| --- | --- | --- | --- | --- | --- |
| 1 | customer → addresses | One-to-few | Bounded | **Embed** | `customers.addresses[]` |
| 2 | order → line items | One-to-few | Bounded | **Embed** | `orders.items[]` |
| 3 | customer → orders | One-to-many | Grows over time | **Reference** | `orders.customerId` |
| 4 | product → reviews | One-to-many | Grows without limit | **Reference** | `reviews.productId` |
| 5 | orders ↔ products | Many-to-many | — | **Reference** + snapshot | `orders.items[].productId` (plus copied `sku`, `name`, `unitPrice`) |

### Why this is the answer

- A customer has a few addresses and an order has a few items. Both are bounded and read with their parent, so they are embedded.
- A customer's order history keeps growing, so each order stores `customerId` instead of the customer holding an array of orders. Reviews can grow without limit, so each review stores `productId`.
- One order contains many products and one product appears in many orders. `training_store` links them through `items[].productId`, plus a snapshot of `sku`, `name` and `unitPrice` so the order keeps what was bought.

**Growth, not nesting, decides.** Cardinality and growth decide the model — the same question works for any relationship.

---

## Exercise: Predict the Nested Query Results

**Slide 39** · **Time:** 10 minutes · **How to run:** two minutes to write predictions, then run each query on the instructor screen **after `load.js`**.

### Scenario

Use the dataset facts: shoe sizes, accessory connections, customer countries and order items.

```javascript
db.products.find(
  { "attributes.sizes": 11 })
db.products.find(
  { "attributes.connection": "USB-C" })
db.customers.find(
  { "addresses.country": "USA" })
db.orders.countDocuments(
  { "items.sku": "A410" })
```

### Tasks

1. Predict each query's result.
2. Name the embedded path it follows.
3. Say where an array is crossed.
4. Check on the instructor's screen.

### Solution

| Query | Result | Path followed | Array crossed? |
| --- | --- | --- | --- |
| `"attributes.sizes": 11` | **Trail Shoe (S210)** | `attributes` → `sizes` | Yes — `sizes` |
| `"attributes.connection": "USB-C"` | **USB Hub (A400), Docking Station (A500)** | `attributes` → `connection` | No |
| `"addresses.country": "USA"` | **Luis Romero (C204), Maya Chen (C620)** | `addresses` → `country` | Yes — `addresses` |
| `countDocuments({ "items.sku": "A410" })` | **3** (O5001, O6201, O6305) | `items` → `sku` | Yes — `items` |

### Why this is the answer

- `"attributes.sizes": 11` walks into `attributes` and then matches any element of the `sizes` array. Only the Trail Shoe, S210, with sizes 8 to 11, has an 11 (S200 has 7–10, S290 has 7–9).
- Two accessories use USB-C: the USB Hub, A400, and the Docking Station, A500. The keyboard (P1001) and the mouse (A410) are Bluetooth.
- Two customers ship to the USA: Luis Romero, C204, in Austin, and Maya Chen, C620, in San Francisco. The other four are in Canada.
- The Wireless Mouse, A410, appears in O5001, O6201 and O6305, so `countDocuments` returns 3.

Dot notation follows the document's shape — arrays and embedded documents alike. On the hand-built core from Lab 2 Steps 1–4 these queries return nothing (no S210, accessories, US customers or A410), which is why the exercise runs after `load.js`.

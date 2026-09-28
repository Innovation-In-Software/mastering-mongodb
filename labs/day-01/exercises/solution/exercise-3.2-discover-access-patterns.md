# Exercise 3.2 — solution (instructor)

**Module 3** · Day 1 · Checkpoint B · slide 43  
**Type:** design · **Do not hand this sheet to participants.**

## Answer

### 1–2. The three most frequent reads

| Read | Returned together |
| --- | --- |
| Find product by SKU | The whole product: sku, name, category, price, attributes, tags, active |
| Retrieve order by order number | Items (sku, name, quantity, unitPrice), subtotal, tax, total, shipping address, paymentStatus, fulfillmentStatus |
| Load customer profile | Name, contact, addresses, preferences |

Inventory display and review lists are medium frequency.

### 3–4. Access-pattern table

This is the table on the "training_store Access Patterns" slide (slide 14), which is the reference answer:

| Access pattern | Frequency | Returned together | Modeling implication |
| --- | --- | --- | --- |
| Find product by SKU | High | The whole product | One product document |
| Browse category and price | High | Name, price | Shared core fields |
| Show customer profile | High | Name, contact, addresses | **Embed** addresses |
| Show one order | High | Items, totals, address | **Embed** items, **snapshot** |
| Customer order history | Medium | Order summaries | **Reference**: `customerId` on each order |
| Reviews for a product | Medium | Recent reviews | **Reference**: separate collection (`productId`) |
| Change order status | Medium | One order | One-document update |

The purchase-time price is a **snapshot**: `items[].unitPrice` is copied from the product when the order is placed.

Frequencies are estimates for a typical store. In a real project you would measure them.

## Slide solution checklist

- Product by SKU · order by number · profile
- Returned data is specific, not everything
- Add order history and paginated reviews
- Purchase-time price is a snapshot
- At least one embed and one reference

## What you want to hear

"Returned together" must be specific — items, totals, address and status — not "the order". High-frequency reads that return one object become one document; lists that grow (order history, reviews) become references; a status change touches one order, so it is a single-document update. Compare their table with slide 14.

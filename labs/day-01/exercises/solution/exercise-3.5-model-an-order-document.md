# Exercise 3.5 — solution (instructor)

**Module 3** · Day 1 · Checkpoint E · slide 46  
**Type:** design · **Do not hand this sheet to participants.**

## Answer

### 1–2. Decisions

| Part | Decision | Snapshot? |
| --- | --- | --- |
| Line items | **Embed** in `items` | Yes — `sku`, `name`, `unitPrice` copied at purchase |
| Purchase-time price | **Embed** as `items[].unitPrice` | Yes |
| Shipping address | **Embed** as `shippingAddress` | Yes — the address used for this order |
| Customer | **Reference**: `customerId` (the customer's `_id`) | No — profile and email must stay current |

Each item also keeps `productId`, a reference to the catalog product. The current catalog is not copied in full.

### 3. The order document — O5001 as loaded by `load.js`

```javascript
{ orderNumber: "O5001",
  customerId: ObjectId("…"),               // C101 Aisha Khan's _id
  items: [
    { productId: ObjectId("…"), sku: "L100", name: "Business Laptop",
      quantity: 1, unitPrice: Decimal128("1299.99") },
    { productId: ObjectId("…"), sku: "A410", name: "Wireless Mouse",
      quantity: 2, unitPrice: Decimal128("19.99") } ],
  shippingAddress: { street: "100 King Street", city: "Toronto", province: "Ontario",
                     postalCode: "M5X 1A9", country: "Canada" },
  paymentStatus: "PENDING",
  fulfillmentStatus: "NEW",
  subtotal: Decimal128("1339.97"),
  tax: Decimal128("174.20"),
  total: Decimal128("1514.17"),
  createdAt: ISODate("2026-09-20T14:30:00Z") }
```

(`load.js` also adds an `internalNotes` string used by a Module 4 lab.) Lab 2 Step 4 builds a smaller O5001 by hand — the laptop only, subtotal 1299.99, tax 169.00, total 1468.99. Both have the same shape.

Status values in `training_store`: `paymentStatus` is `PAID`, `PENDING` or `FAILED`; `fulfillmentStatus` is `NEW`, `PROCESSING`, `SHIPPED` or `DELIVERED`. A single `status` field is not used.

### 4. Required fields

`orderNumber`, `customerId`, `items` (each with `productId`, `sku`, `name`, `quantity`, `unitPrice`), `shippingAddress`, `paymentStatus`, `fulfillmentStatus`, `subtotal`, `tax`, `total`, `createdAt`. `shippingFee` is optional — several `training_store` orders omit it.

### Justification

- One read by `orderNumber` returns everything the order page shows.
- A customer's orders are found by `customerId` (later indexed as `{ customerId: 1, createdAt: -1 }`).
- Prices never silently follow the catalog: if L100's price changes, O5001 still shows 1299.99.

## Slide solution checklist

- Items, prices, address: embedded
- Customer: `customerId` reference
- Money as Decimal128
- One read by `orderNumber`
- Same shape as Lab 2, Step 4

## What you want to hear

A hybrid: reference the customer, embed the purchase facts. Push back on a copied customer email or profile in the order (it must stay current), on `orderedAt` instead of `createdAt`, and on money stored as Double or string.

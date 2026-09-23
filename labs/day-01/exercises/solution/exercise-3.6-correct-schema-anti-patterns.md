# Exercise 3.6 — solution (instructor)

**Module 3** · Day 1 · Checkpoint F · slide 47  
**Type:** design · **Do not hand this sheet to participants.**

## Answer

### 1. The problems

| Field | Problem | Why it hurts |
| --- | --- | --- |
| `price: "49.99"` | Money stored as a **string** | Sorts as text ("100" before "20"), range filters and arithmetic fail |
| `isActive: "yes"` | Boolean stored as **text** | `find({ active: true })` never matches; "yes"/"Yes"/"Y" drift |
| `allReviews: [ … ]` | **Unbounded** embedded array | Document keeps growing, updates get costlier, can reach 16 MiB |
| `created: "September 20, 2026"` | Display-text date | Doesn't sort by time; no date operators |
| `productId: "P1001"` | Unclear identifier convention | Neither `_id` nor a named business key; name inconsistent with the rest of the catalog |

### 2–4. Corrected document

```javascript
{ _id: ObjectId("…"),                     // generated
  sku: "P1001",                            // business key, unique index
  name: "Wireless Keyboard",
  category: "ACCESSORY",
  price: Decimal128("49.99"),
  active: true,
  createdAt: ISODate("2026-08-23T09:00:00Z") }
// no reviews array — each review lives in the reviews collection with productId (and sku)
```

That is the shape of `training_store`'s real Wireless Keyboard, P1001, in `load.js`. The loaded document also has `attributes: { connection: "Bluetooth", batteryLifeMonths: 12 }`, `tags: ["wireless", "accessories"]` and `discountPrice: Decimal128("39.99")`. Its one review (rating 3, "Works, average keys") is in `reviews`.

## Slide solution checklist

- String price, text Boolean
- Unbounded `allReviews` array
- Display-text date
- Decimal128, `true`, a real Date
- Reviews in their own collection

## What you want to hear

Most anti-patterns are wrong types or unbounded growth. Bonus for naming the identifier convention (`_id` generated, `sku` as the business key) and the field name change `isActive` → `active`, `created` → `createdAt` so the catalog is consistent.

Point out that XBAD in `training_store` still has the string price on purpose for the Module 4 `$type` labs.

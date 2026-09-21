# Exercise 8.1: Review a Document Model

**Module 8:** MongoDB Best Practices, Security, and Troubleshooting  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 8)  
**Time:** 15 min  
**Difficulty:** Beginner

**Objective:** Evaluate a customer-order document for access-pattern alignment, ownership, duplication, types, growth, snapshots, sensitive data, and validation.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may use `mongosh` to inspect `training_store`, but reasoning is the deliverable unless a step says otherwise. Do not enable authentication on a shared training instance unless the instructor provides a disposable environment.


---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Score the document

**Do this:** Review this order-shaped document and mark each area as strong, risky, or missing: access patterns, ownership, duplication, BSON types, array growth, historical snapshots, sensitive fields, and validation.

```javascript
{
  _id: ObjectId("..."),
  orderNumber: "O5001",
  customer: {
    customerNumber: "C101",
    name: "Aisha Khan",
    email: "aisha@example.com",
    passwordHash: "sha256:demo-not-real",
    loyaltyPoints: 1840
  },
  items: [ { sku: "L100", qty: 1, price: "1299.00" } ],
  createdAt: "2026-07-12",
  notes: []
}
```

**Expected result:** Risky/missing: price as string, date as string, unbounded `notes`, live customer fields (email, loyalty, password hash) instead of a snapshot plus a reference, no statuses or Decimal128 total, sensitive hash stored on the order.

---

### Step 2 — Rewrite the boundary

**Do this:** Write the corrected document boundary: what stays on the order, what is referenced, and one validation rule you would add first.

**Expected result:** Order keeps orderNumber, customerId, purchase-time name/address/price snapshots, items, statuses, Decimal128 total, Date createdAt. Customer master stays in customers. First validator: required orderNumber, customerId, items, paymentStatus, total, createdAt.

---

## Success criteria

- [ ] At least four risks are named with evidence from the document
- [ ] The rewrite separates customer master data from the order aggregate
- [ ] A first validation rule is specific (field + type or enum)

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)

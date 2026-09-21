# Exercise 3.5: Model an Order Document

**Module 3:** Data Modeling with MongoDB  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 3, Lesson 3.3)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Design one complete order document: embed snapshots, reference the customer, choose required fields and BSON types, and justify the shape.

---

## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Work in pairs. Capture answers in a notes file or on paper.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional — a table is enough |
| Timer | Instructor clocks this | Stay on the slide timer |

You do **not** need MongoDB running for this exercise.

---

## Requirements

The application must find an order by order number, display purchased items, preserve purchase-time prices, show the shipping address used, show payment and fulfillment status, and list orders for a customer.

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Decide embed versus reference

**Do this:** Write four decisions: line items, purchase-time price, shipping address, customer. Mark which of those are **historical snapshots**.

**Expected result:** Items, prices, and shipping address are embedded snapshots. Customer is a reference (`customerId`). Current product catalog is not copied in full.

---

### Step 2 — Write the document and required fields

**Do this:** Draft one order document including `orderNumber`, `customerId`, `items[]` (sku, name, quantity, unitPrice), `shippingAddress`, statuses, monetary totals as Decimal128, and `createdAt`. List required fields.

**Expected result:** A complete order JSON-like object plus a short justification: one read by order number, customer orders via `customerId`, prices never silently follow the catalog.

---

## Success criteria

- [ ] Items and prices are embedded
- [ ] Customer is referenced
- [ ] Money uses Decimal128 (or you noted why)
- [ ] Required fields are listed


## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)

# Exercise 3.5 — Model an Order Document

**Module 3** (Data Modeling with MongoDB) · Day 1 · **Checkpoint E**  
**Deck:** `decks/pptx_new/MongoDB_Module03_Data_Modeling_with_MongoDB.pptx`, slide 46  
**Time:** 20 min · **Type:** design (pairs) · **MongoDB needed:** no

**Objective:** Design one order aggregate: embed the purchase facts, reference the customer, choose BSON types and required fields, and justify the shape.

---

## Requirements

The application must:

- find an order by order number
- show the purchased items and their purchase-time prices
- show the shipping address used
- show payment and fulfillment status
- list a customer's orders

---

## Do this

1. Decide embed or reference for four things: line items, purchase-time price, shipping address, customer.
2. Mark which of them are **historical snapshots**.
3. Write the order document. Include `orderNumber`, `customerId`, an `items` array (sku, name, quantity, unitPrice), `shippingAddress`, `paymentStatus`, `fulfillmentStatus`, money totals and `createdAt`.
4. List the required fields.

## Expected result

One complete order document plus a short justification of three points: how one read by order number returns the page, how a customer's orders are found, and why prices do not follow the catalog.

## Reference solution

After the debrief, compare with [Exercise 3.5 solution](solution/exercise-3.5-model-an-order-document.md).

## Lab connection

Lab 2, Step 4 ([LAB-2-GUIDE.md](../lab2/LAB-2-GUIDE.md)) inserts order O5001 in the same shape.

## Success criteria

- [ ] Items and prices are embedded
- [ ] The customer is referenced
- [ ] Money uses Decimal128
- [ ] Required fields are listed

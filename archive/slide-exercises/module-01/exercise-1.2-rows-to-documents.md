# Exercise 1.2: Convert Relational Rows into a Document

**Module 1:** Introduction to NoSQL Databases  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 1, Lesson 1.5)  
**Time:** 20 min  
**Difficulty:** Beginner

**Objective:** Represent related customer, order, and order-item rows as one JSON-like MongoDB document, then decide what to embed versus snapshot.

---

## Environment basics (read this first)

**Demonstration environment:** Windows 10/11. Write the document in Notepad, Cursor, or a scratch `.js` file. MongoDB is optional.

| Task | Windows | Where |
|------|---------|-------|
| Open a scratch file | Cursor | `Ctrl+N` |
| Terminal | ``Ctrl+` `` → PowerShell | Only if you want to paste into `mongosh` later |

---

## Starting relational data

**Customer**

| customer_id | name | email |
|-------------|------|-------|
| C101 | Aisha Khan | aisha@example.com |

**Order**

| order_id | customer_id | status | total |
|----------|-------------|--------|------:|
| O5001 | C101 | PLACED | 110.00 |

**Order items**

| order_id | product_id | product_name | quantity | price |
|----------|------------|--------------|---------:|------:|
| O5001 | P10 | Keyboard | 2 | 25.00 |
| O5001 | P22 | Mouse | 1 | 60.00 |

---

## Steps from the training slides

Follow these steps in order.

### Step 1 — Read the three relational tables

**Do this:** Identify how you would reconstruct one complete order in SQL: join `Customer` to `Order` on `customer_id`, then join `Order items` on `order_id`. List every field the application needs for “show order O5001.”

**Expected result:** You can name the three tables and the join keys. You know the order total is 110.00 and there are two line items.

---

### Step 2 — Draft one JSON-like order document

**Do this:** Create a single document that holds the order header. Do not worry about `_id` or nesting yet — get `status` and `total` on the page.

**Expected result:** A starting object exists, for example `{ orderId: "O5001", status: "PLACED", total: 110.00 }`.

---

### Step 3 — Embed items, customer, and `_id`

**Do this:** Embed the two order items as an array. Include essential customer information (id, name, email). Set `_id` to `"O5001"` (or an ObjectId if you prefer). Keep purchase-time `price` on each item.

**Expected result:** One document that looks like the solution below: `_id`, nested `customer`, `items` array, `status`, and `total`. You did not leave items in a separate table.

---

### Step 4 — Identify snapshot versus stale fields

**Do this:** Answer the discussion questions: Should customer email be embedded or referenced? Should the order store purchase-time price or current catalog price? What happens if the customer changes email? Which fields are a historical snapshot? Name the main query this document supports.

**Expected result:** You can state that purchase-time price is a snapshot, customer email may go stale if embedded, and the document is shaped for “get order O5001 in one read.”

---

## Expected solution

```javascript
{
  _id: "O5001",
  customer: {
    customerId: "C101",
    name: "Aisha Khan",
    email: "aisha@example.com"
  },
  items: [
    {
      productId: "P10",
      productName: "Keyboard",
      quantity: 2,
      price: 25.00
    },
    {
      productId: "P22",
      productName: "Mouse",
      quantity: 1,
      price: 60.00
    }
  ],
  status: "PLACED",
  total: 110.00
}
```

**Expected insight:** Some duplication is intentional when it supports the access pattern and preserves historical information.

---

## Success criteria

- [ ] One document represents the whole order
- [ ] Line items are an array, not a separate document per row
- [ ] `_id` is present
- [ ] You can name one field that should stay a snapshot (price) and one that might go stale (email)

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
- Same order shape appears in [`datasets/training_store/orders.json`](../../datasets/training_store/orders.json)

# Exercise 1.2 — Convert Relational Rows into a Document

**Module 1** (Introduction to NoSQL Databases) · Day 1 · **Checkpoint B**  
**Time:** 20 min · **Type:** modeling on paper (MongoDB optional) · **Difficulty:** Beginner

**Deck:** `decks/pptx_new/MongoDB_Module01_Introduction_to_NoSQL_Databases.pptx` — slide 44, "Exercise 1.2 — Convert Relational Rows into a Document"

## Purpose

One order, one document. You take one order that is spread across three relational tables and write it as a single JSON-like MongoDB document the application can read without joins. Then you decide which embedded values are deliberate snapshots and which can go stale.

## Prerequisites

- Module 1, Part 3 — especially "From Rows to Documents" and "Embed or Reference?"
- A scratch file (Notepad, VS Code/Cursor, or a `.js` file) or paper
- MongoDB is **optional**. You only need `mongosh` if you want to try inserting your document at the end.

## Scenario

Order **O5001** lives in three tables. Make it one document the application can read without joins.

**Customer**

| customer_id | name | email |
| --- | --- | --- |
| C101 | Aisha Khan | aisha@example.com |

**Order**

| order_id | customer_id | status | total |
| --- | --- | --- | ---: |
| O5001 | C101 | PLACED | 110.00 |

**Order items**

| order_id | product_id | product_name | quantity | price |
| --- | --- | --- | ---: | ---: |
| O5001 | P10 | Keyboard | 2 | 25.00 |
| O5001 | P22 | Mouse | 1 | 60.00 |

> This O5001 is a small worksheet example. The `training_store` dataset loaded for the course also has an order O5001, but with different contents — you will meet that one in Exercise 1.3.

## Tasks

### Task 1 — Name the three tables and their join keys

Write down how SQL would rebuild the complete order: which tables are joined, and on which columns. List every field the application needs to "show order O5001".

### Task 2 — Draft the order header: status and total

Start one JSON-like document that holds the order header fields (`status` and `total`). Don't worry about `_id` or nesting yet.

### Task 3 — Embed the items and the customer; set `_id`

Extend the document:

- Embed the two order lines as an **array**. Keep the purchase-time price on each line.
- Embed the essential customer information (id, name, email) as a **nested object**.
- Set `_id` to `"O5001"`.

Items must not stay in a separate table or a separate document per row.

### Task 4 — Decide what is a snapshot and what can go stale

Answer in one or two sentences each:

1. Should the customer's email be embedded or referenced?
2. Should each item store the purchase-time price or the current catalog price?
3. What happens to this order document if Aisha changes her email next month?
4. Which fields are a historical snapshot?
5. What is the main query this document is shaped for?

### Optional — Try it in mongosh

If you have `mongosh` connected, insert your document into a scratch database (not `training_store`, which later modules rely on):

```javascript
use module1_scratch
db.orders.insertOne( /* paste your document here */ )
db.orders.findOne({ _id: "O5001" })
```

## Deliverable

1. One document for order O5001 in your scratch file.
2. Your answers to the five Task 4 questions.

## Expected outcome

- One document with `_id: "O5001"`
- A nested customer and an items array
- You can say which value is a deliberate snapshot and which can go stale
- The document is shaped for one specific query

## Success criteria

- [ ] One document represents the whole order
- [ ] Line items are an array, not a separate document per row
- [ ] `_id` is present
- [ ] You can name one field that should stay a snapshot and one that might go stale

# Exercise 3.7 — solution (instructor)

**Module 3** · Day 1 · Checkpoint G · slide 48  
**Type:** discussion · **Do not hand this sheet to participants.**

## Answer

| # | Requirement | Pattern | Benefit | Cost |
| --- | --- | --- | --- | --- |
| 1 | Sensor readings grouped by hour | **Bucket** | Far fewer documents and index entries | Each write updates a growing bucket |
| 2 | Latest three product reviews | **Subset** | Product page loads in one read | A new review is written in two places |
| 3 | Stored average rating | **Computed** | No averaging on every page view | Recompute on each new review or on a schedule |
| 4 | Dynamic product specifications | **Attribute** | One `{ attributes.k, attributes.v }` index serves every attribute search | Less natural document shape |
| 5 | Customer name copied into an order | **Extended reference** | Show the name without a join | Copy can go stale if it must stay current |
| 6 | Rare products with a huge review volume | **Outlier** | Normal products keep the simple design | Extra overflow logic for the rare case |
| 7 | Many product types in one collection | **Polymorphic** | Shared queries across laptops, shoes, books | Readers must handle several shapes |

Slide solution line: **1 Bucket · 2 Subset · 3 Computed · 4 Attribute · 5 Extended reference · 6 Outlier · 7 Polymorphic.**

### Bucket versus one document per event

Bucket stores an hour of readings in one document, so there are far fewer documents and index entries, at the cost of updating a growing bucket.

### Why Outlier exists

Most products have a few reviews. Outlier keeps the normal design for them and adds overflow handling only for the rare product with a huge volume.

### Already in training_store

`products` is polymorphic (LAPTOP, SHOE, BOOK, ACCESSORY in one collection). Order items are extended references (they copy `sku` and `name` next to `productId`), and reviews copy `sku`. Subset and Computed are not used yet — Module 5 computes averages with `$group`.

## What you want to hear

Each pattern answers one recurring problem — name the problem first. Every pattern makes some reads cheaper by making writes or code more complex.

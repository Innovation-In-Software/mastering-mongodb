# Exercise 3.9 — solution (instructor)

**Module 3** · Day 1 · Checkpoint I · slide 50  
**Type:** design challenge · **Do not hand this sheet to participants.** There is no single right answer; this is the suggested direction.

## Answer

### 1. Access patterns and collections

| Access pattern | Frequency | Shape |
| --- | --- | --- |
| Show a ticket with recent comments | High | One ticket document |
| Search tickets by customer / agent / status / priority | High | Indexed fields on the ticket |
| Assign, change status or priority | Medium | One-document update (plus an audit event) |
| Add a comment | Medium | Insert into `comments`; push to bounded `recentComments` |
| Show the full comment history or audit trail | Low | Separate collections, by `ticketId` |

Collections: **`tickets`, `customers`, `agents`, `audit_events`** (and `comments` for the full history).

### 2. Embed or reference

| Data | Decision | Growth |
| --- | --- | --- |
| Current assignee | **Embed** a summary (`agentId`, `name`) — extended reference | Bounded (one) |
| Tags | **Embed** | Bounded |
| Recent comments | **Embed** `recentComments` — Subset pattern, e.g. last 5 | Bounded by design |
| All comments | **Separate** `comments` collection with `ticketId` | Unbounded |
| Audit history | **Separate** `audit_events` collection with `ticketId` | Unbounded |
| Customer | **Reference** `customerId` | — |
| Agent master | **Reference** `agents` | — |

### 3. Sample ticket

```javascript
{ _id: ObjectId("…"),
  ticketNumber: "T10001",                                   // String
  customerId: ObjectId("…"),                                // ObjectId reference
  assignee: { agentId: ObjectId("…"), name: "Dana Ruiz" },  // embedded summary
  status: "OPEN",                                           // String
  priority: "HIGH",                                         // String
  subject: "Order O5001 not shipped",
  tags: ["shipping", "order"],                              // Array
  recentComments: [                                          // bounded Array
    { author: "customer", body: "Any update?", createdAt: ISODate("2026-09-22T10:00:00Z") }
  ],
  createdAt: ISODate("2026-09-21T09:00:00Z"),               // Date
  updatedAt: ISODate("2026-09-22T10:00:00Z") }              // Date
```

### 4. Validation and indexes

**Validation:** require `ticketNumber` (string), `customerId` (objectId), `status` and `priority` (string, optionally `enum`), `tags` (array), `recentComments` (array, optionally `maxItems`), `createdAt` and `updatedAt` (date).

**Planned indexes (design only):** `customerId`, `assignee.agentId`, `status`, `priority` — or compounds such as `{ status: 1, priority: 1 }` — plus a unique `ticketNumber`. On `audit_events` and `comments`: `{ ticketId: 1, createdAt: -1 }`.

**Audit history:** every change inserts one event `{ ticketId, type, from, to, by, createdAt }` into `audit_events`; the ticket never holds the full list.

## Slide suggested direction

- `tickets`, `customers`, `agents`, `audit_events`
- Embed: assignee, tags, `recentComments`
- Full comments and audit: separate
- Indexes: `customerId`, `agentId`, `status`, `priority`

## What you want to hear

The same method as `training_store`: access patterns, relationships, growth, then rules. The complete comment history and the audit trail grow without limit, so they must live in their own collections.

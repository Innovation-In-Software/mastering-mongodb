"""Write Module 4 lab guides. Run: python scripts/module04_labs.py"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "slide-exercises" / "module-04"

ENV_MONGO = """## Environment basics (read this first)

**Demonstration environment:** Windows 10/11 · PowerShell in Cursor (``Ctrl+` ``) · `mongosh` connected to the training instance.

| Task | Windows | Where |
|------|---------|-------|
| Open folder | `Ctrl+K Ctrl+O` | File → Open Folder |
| Terminal | ``Ctrl+` `` → PowerShell | Bottom panel |
| MongoDB shell | `mongosh` | Same terminal |

**Prerequisite:** `training_store` is loaded from [`datasets/training_store/load.js`](../../datasets/training_store/load.js). If writes from an earlier lab remain, reload that script unless the exercise says otherwise.

```javascript
use training_store
```
"""

ENV_DISCUSSION = """## Environment basics (read this first)

**Demonstration environment:** Classroom discussion. Capture answers in a notes file.

| Task | Windows | Where |
|------|---------|-------|
| Open notes | Notepad or Cursor | Optional |
| Timer | Instructor clocks this | — |

You may use `mongosh` to test rewrites, but reasoning is the deliverable.
"""


def js(code: str) -> str:
    return f"```javascript\n{code.strip()}\n```"


def guide(
    num: int,
    slug: str,
    title: str,
    time: str,
    difficulty: str,
    objective: str,
    steps: list[tuple[str, str, str]],
    success: list[str],
    *,
    discussion: bool = False,
    extra: str = "",
) -> tuple[int, str, str, str, str, str]:
    """Return metadata plus markdown. num is the exercise number (4.N)."""
    env = ENV_DISCUSSION if discussion else ENV_MONGO
    step_md = []
    for i, (stitle, do, exp) in enumerate(steps, 1):
        step_md.append(
            f"### Step {i} — {stitle}\n\n**Do this:** {do}\n\n**Expected result:** {exp}\n"
        )
    steps_block = "\n---\n\n".join(step_md)
    checks = "\n".join(f"- [ ] {c}" for c in success)
    md = f"""# Exercise 4.{num}: {title}

**Module 4:** The MongoDB Query Language  
**Slides:** `slides/course-complete-marp-with-notes.md` (Module 4)  
**Time:** {time}  
**Difficulty:** {difficulty}

**Objective:** {objective}

---

{env}

---

## Steps from the training slides

Follow these steps in order.

{steps_block}
---

{extra}

## Success criteria

{checks}

---

## Related files

- Slide deck source: [`slides/course-complete-marp-with-notes.md`](../../slides/course-complete-marp-with-notes.md)
- Dataset: [`datasets/training_store`](../../datasets/training_store)
- Course index: [`FINAL_TABLE_OF_CONTENTS.md`](../../FINAL_TABLE_OF_CONTENTS.md)
"""
    return (num, slug, title, time, "discussion" if discussion else "hands-on", objective, md)


GUIDES: list[tuple] = []

GUIDES.append(
    guide(
        1,
        "read-basic-documents",
        "Read Basic Documents",
        "10 min",
        "Beginner",
        "Retrieve documents with empty, equality, and unique-identifier filters.",
        [
            (
                "Retrieve all products",
                "Run:\n\n" + js("db.products.find({})"),
                "A cursor of product documents prints. This is unbounded — acceptable on the training set only.",
            ),
            (
                "Find one product by SKU",
                "Run:\n\n" + js('db.products.findOne({ sku: "L100" })'),
                "One laptop document is returned. `findOne()` returns a document or `null`, not a cursor.",
            ),
            (
                "Find active products",
                "Run:\n\n" + js("db.products.find({ active: true })"),
                "Inactive items such as `L190` are excluded. Field names and booleans are case-sensitive.",
            ),
            (
                "Find ACTIVE customers",
                "Run:\n\n" + js('db.customers.find({ status: "ACTIVE" })'),
                "`C101`, `C204`, `C310`, `C412`, and `C620` match. `C515` (`INACTIVE`) does not.",
            ),
            (
                "Find one order by number",
                "Run:\n\n" + js('db.orders.findOne({ orderNumber: "O5001" })'),
                "The order includes an embedded `customer` object and an `items` array.",
            ),
        ],
        [
            "Used `find()` and `findOne()` correctly",
            "Filtered on `active` and `status` with exact case",
            "Located `O5001` by `orderNumber`",
        ],
    )
)

GUIDES.append(
    guide(
        2,
        "build-comparison-filters",
        "Build Comparison Filters",
        "15 min",
        "Beginner",
        "Write `$gt`, `$gte`, `$lte`, range, and `$nin` filters using Decimal128 for money.",
        [
            (
                "Products priced above 100",
                "Run:\n\n"
                + js('db.products.find({ price: { $gt: Decimal128("100.00") } })'),
                "Laptops and `S200` appear. `XBAD` does not — its price is a string, not Decimal128.",
            ),
            (
                "Products priced between 50 and 500",
                "Run:\n\n"
                + js(
                    'db.products.find({\n  price: {\n    $gte: Decimal128("50.00"),\n    $lte: Decimal128("500.00")\n  }\n})'
                ),
                "Includes `S200`, `S210`, `A400`, and similar mid-range items. Both bounds are inclusive.",
            ),
            (
                "Orders with totals above 1,000",
                "Run:\n\n"
                + js('db.orders.find({ total: { $gt: Decimal128("1000.00") } })'),
                "`O5001` and `O6401` match (both contain L100 and have totals above 1,000). Paid high-value orders such as `O6101` also match.",
            ),
            (
                "Reviews rated at least 4",
                "Run:\n\n" + js("db.reviews.find({ rating: { $gte: 4 } })"),
                "Five reviews match. The rating-3 review of `P1001` does not.",
            ),
            (
                "Products outside LAPTOP and SHOE",
                "Run:\n\n"
                + js('db.products.find({ category: { $nin: ["LAPTOP", "SHOE"] } })'),
                "Books and accessories remain, including the legacy `XBAD` document.",
            ),
        ],
        [
            "Used Decimal128 for money comparisons",
            "Explained why `XBAD` misses numeric price queries",
            "Used `$nin` on one field rather than two `$ne` clauses without need",
        ],
    )
)

GUIDES.append(
    guide(
        3,
        "combine-logical-conditions",
        "Combine Logical Conditions",
        "15 min",
        "Beginner",
        "Combine implicit AND, `$or`, and `$nor` into precise product and order filters.",
        [
            (
                "Active laptops or books",
                "Run:\n\n"
                + js(
                    'db.products.find({\n  active: true,\n  $or: [\n    { category: "LAPTOP" },\n    { category: "BOOK" }\n  ]\n})'
                ),
                "Active laptops and books match. Inactive `L190` is excluded by `active: true`.",
            ),
            (
                "Active products under 100",
                "Run:\n\n"
                + js(
                    'db.products.find({\n  active: true,\n  price: { $lt: Decimal128("100.00") }\n})'
                ),
                "Implicit AND. Accessories and cheaper books match. `XBAD` does not, because of BSON type.",
            ),
            (
                "Pending or processing orders",
                "Run:\n\n"
                + js(
                    'db.orders.find({\n  $or: [\n    { paymentStatus: "PENDING" },\n    { fulfillmentStatus: "PROCESSING" }\n  ]\n})'
                ),
                "`O5001` and `O6499` are PENDING payment; `O6401` is PROCESSING. Prefer `$in` when alternatives share **one** field.",
            ),
            (
                "Neither discontinued nor inactive",
                "Run:\n\n"
                + js(
                    'db.products.find({\n  $nor: [\n    { tags: "discontinued" },\n    { active: false }\n  ]\n})'
                ),
                "Documents that are inactive **or** tagged `discontinued` are excluded. `L190` is both.",
            ),
        ],
        [
            "Used implicit AND for field combinations",
            "Used `$in` when alternatives share one field",
            "Stated what `$nor` excludes",
        ],
    )
)

GUIDES.append(
    guide(
        4,
        "query-missing-and-null",
        "Query Missing and Null Fields",
        "10 min",
        "Beginner",
        "Distinguish `$exists`, BSON `null`, missing fields, and incorrect types.",
        [
            (
                "Products with a discount field",
                "Run:\n\n" + js("db.products.find({ discountPrice: { $exists: true } })"),
                "`P1001` and `B310` match. Presence of the field is enough — the value may still be inspected later.",
            ),
            (
                "Products without a discount field",
                "Run:\n\n" + js("db.products.find({ discountPrice: { $exists: false } })"),
                "Most catalog items match, including laptops that never had a discount field.",
            ),
            (
                "Customers with a null phone",
                "Run:\n\n" + js('db.customers.find({ "contact.phone": { $type: "null" } })'),
                "`C204` matches. `{ phone: null }` on a dotted path is easy to get wrong — query `{ \"contact.phone\": { $type: \"null\" } }`.",
            ),
            (
                "Customers without a phone field",
                "Run:\n\n" + js('db.customers.find({ "contact.phone": { $exists: false } })'),
                "`C515` matches (no phone field). `C204` has the field with BSON null. Everyone else has a string phone.",
            ),
            (
                "Incorrect price BSON type",
                "Run:\n\n" + js('db.products.find({ price: { $type: "string" } })'),
                "`XBAD` (Legacy Cable Pack) is the planted type error. Money in this course is Decimal128.",
            ),
        ],
        [
            "Did not treat `{ field: null }` as “explicitly null only”",
            "Separated missing vs null vs wrong type",
            "Found `XBAD` with `$type`",
        ],
    )
)

GUIDES.append(
    guide(
        5,
        "query-arrays",
        "Query Arrays",
        "15 min",
        "Beginner",
        "Query arrays with containment, `$all`, `$size`, `$ne`, and `$nin`.",
        [
            (
                "Tagged technology",
                "Run:\n\n" + js('db.products.find({ tags: "technology" })'),
                "Any product whose `tags` array contains `technology`, regardless of other tags.",
            ),
            (
                "Both database and technology",
                "Run:\n\n"
                + js('db.products.find({ tags: { $all: ["database", "technology"] } })'),
                "`B300` matches (`database` and `technology`). Order of tags does not matter.",
            ),
            (
                "Exactly two tags",
                "Run:\n\n" + js("db.products.find({ tags: { $size: 2 } })"),
                "Most catalog products have exactly two tags. `$size` cannot express “at least two”.",
            ),
            (
                "Specified available size",
                "Run:\n\n" + js('db.products.find({ "attributes.sizes": 9 })'),
                "`S200`, `S210`, and `S290` match. Nested array containment uses a dotted path.",
            ),
            (
                "Not containing discontinued",
                "Run:\n\n" + js('db.products.find({ tags: { $ne: "discontinued" } })'),
                "`L190` is excluded once it carries a `discontinued` tag. `$ne` on an array field also matches documents that **lack** the field.",
            ),
        ],
        [
            "Explained containment vs exact-array match",
            "Used `$all` instead of two separate `tags` equalities when both values are required",
            "Stated the `$size` limitation",
        ],
    )
)

GUIDES.append(
    guide(
        6,
        "query-arrays-of-documents",
        "Query Arrays of Documents",
        "15 min",
        "Intermediate",
        "Query nested arrays and use `$elemMatch` when two conditions must apply to the same element.",
        [
            (
                "Orders containing SKU L100",
                "Run:\n\n" + js('db.orders.find({ "items.sku": "L100" })'),
                "`O5001`, `O6101`, and `O6401` match.",
            ),
            (
                "Orders with any item quantity ≥ 2",
                "Run:\n\n" + js("db.orders.find({ \"items.quantity\": { $gte: 2 } })"),
                "`O5001` (A410 qty 2) and `O6401` (L100 qty 2). Other orders may also match.",
            ),
            (
                "Same item is L100 and qty ≥ 2",
                "Run:\n\n"
                + js(
                    'db.orders.find({\n  items: {\n    $elemMatch: {\n      sku: "L100",\n      quantity: { $gte: 2 }\n    }\n  }\n})'
                ),
                "Only `O6401`. `O5001` has L100 qty 1 **and** a different item (A410) qty 2 — that is the trap.",
            ),
            (
                "Confirm the trap without $elemMatch",
                "Run:\n\n"
                + js(
                    'db.orders.find({\n  "items.sku": "L100",\n  "items.quantity": { $gte: 2 }\n})'
                ),
                "Both `O5001` and `O6401` match. Dot notation does **not** require the same array element.",
            ),
            (
                "Customers with a Toronto shipping address",
                "Run:\n\n"
                + js(
                    'db.customers.find({\n  addresses: {\n    $elemMatch: { type: "SHIPPING", city: "Toronto" }\n  }\n})'
                ),
                "`C101` matches. Address `type` values in this dataset are uppercase (`SHIPPING`).",
            ),
        ],
        [
            "Named the O5001 false-positive without `$elemMatch`",
            "Wrote a correct `$elemMatch` on `items`",
            "Queried `addresses` as an array of documents",
        ],
    )
)

GUIDES.append(
    guide(
        7,
        "design-projections",
        "Design Projections",
        "10 min",
        "Beginner",
        "Return only required fields, including nested paths and a matching array element.",
        [
            (
                "Product name and price without _id",
                "Run:\n\n"
                + js(
                    'db.products.find(\n  { active: true },\n  { name: 1, price: 1, _id: 0 }\n)'
                ),
                "Each result has only `name` and `price`. Mixing inclusion of `name` with exclusion of `tags` would error.",
            ),
            (
                "Customer name and email",
                "Run:\n\n"
                + js(
                    'db.customers.find(\n  { customerNumber: "C101" },\n  { "name.first": 1, "name.last": 1, "contact.email": 1, _id: 0 }\n)'
                ),
                "Nested inclusion. Sibling fields such as `addresses` are omitted.",
            ),
            (
                "Order number, status, and total",
                "Run:\n\n"
                + js(
                    'db.orders.find(\n  {},\n  { orderNumber: 1, status: 1, total: 1, _id: 0 }\n)'
                ),
                "A compact operations list. `_id` is excluded explicitly.",
            ),
            (
                "Exclude large attribute fields",
                "Run:\n\n"
                + js("db.products.find({ sku: \"L100\" }, { attributes: 0, tags: 0 })"),
                "Exclusion projection. All remaining fields are returned.",
            ),
            (
                "Only the matching order item",
                "Run:\n\n"
                + js(
                    'db.orders.find(\n  { orderNumber: "O5001" },\n  { items: { $elemMatch: { sku: "L100" } }, orderNumber: 1 }\n)'
                ),
                "`items` contains only the L100 element. Other line items are omitted from the result shape.",
            ),
        ],
        [
            "Wrote an inclusion projection that excludes `_id`",
            "Projected nested customer fields with dotted paths",
            "Used `$elemMatch` in a projection on `items`",
        ],
    )
)

GUIDES.append(
    guide(
        8,
        "sort-and-paginate",
        "Sort and Paginate Results",
        "15 min",
        "Beginner",
        "Sort, limit, skip, count, and retrieve distinct values with a deterministic tiebreaker.",
        [
            (
                "Sort products by price ascending",
                "Run:\n\n" + js("db.products.find({}, { name: 1, price: 1 }).sort({ price: 1, _id: 1 })"),
                "Cheapest Decimal128 prices first. `XBAD` may sort oddly because its price is a string — mention that.",
            ),
            (
                "Sort by category then price descending",
                "Run:\n\n"
                + js(
                    "db.products.find({}, { category: 1, name: 1, price: 1, _id: 0 })\n  .sort({ category: 1, price: -1 })"
                ),
                "Within each category the highest price prints first.",
            ),
            (
                "Five most expensive active products",
                "Run:\n\n"
                + js(
                    "db.products.find({ active: true }, { name: 1, price: 1, _id: 0 })\n  .sort({ price: -1, _id: 1 })\n  .limit(5)"
                ),
                "Expect `L110`, `L100`, then `L190` if active were included — on active-only, `L110` then `L100` then `A500`.",
            ),
            (
                "Page 1 and page 2 (five per page)",
                "Run both:\n\n"
                + js(
                    "db.products.find({ active: true }).sort({ _id: 1 }).skip(0).limit(5)\n"
                    "db.products.find({ active: true }).sort({ _id: 1 }).skip(5).limit(5)"
                ),
                "Two disjoint pages. The sort key is required for stable pagination.",
            ),
            (
                "Count and distinct",
                "Run:\n\n"
                + js(
                    'db.products.countDocuments({ active: true })\n'
                    'db.products.distinct("category")'
                ),
                "Count is smaller than 16 because inactive items exist. Distinct includes `LAPTOP`, `BOOK`, `ACCESSORY`, `SHOE`.",
            ),
        ],
        [
            "Included a unique tiebreaker in sort",
            "Produced two pages of five",
            "Used `countDocuments` rather than the legacy `count()` API",
        ],
    )
)

GUIDES.append(
    guide(
        9,
        "insert-new-application-data",
        "Insert New Application Data",
        "15 min",
        "Beginner",
        "Insert one document, several documents, a customer, and an order, then verify each write.",
        [
            (
                "Insert one product",
                "Run:\n\n"
                + js(
                    'db.products.insertOne({\n  sku: "A620",\n  name: "USB-C Hub",\n  category: "ACCESSORY",\n  price: Decimal128("69.99"),\n  tags: ["usb-c", "accessory"],\n  active: true,\n  stockQuantity: 10,\n  createdAt: new Date()\n})'
                ),
                "`acknowledged: true` and an `insertedId`. If `sku` already exists, unique index `sku_unique` rejects the insert — reload the dataset.",
            ),
            (
                "Insert three products",
                "Run:\n\n"
                + js(
                    'db.products.insertMany([\n  { sku: "A610", name: "Laptop Stand", category: "ACCESSORY", price: Decimal128("49.99"), active: true, stockQuantity: 6 },\n  { sku: "A611", name: "HDMI Adapter", category: "ACCESSORY", price: Decimal128("24.99"), active: true, stockQuantity: 15 },\n  { sku: "A612", name: "Sleeve", category: "ACCESSORY", price: Decimal128("19.99"), active: true, stockQuantity: 20 }\n])'
                ),
                "`insertedIds` contains three keys. Inspect `insertedCount` / `insertedIds`.",
            ),
            (
                "Insert a customer with an address",
                "Run:\n\n"
                + js(
                    'db.customers.insertOne({\n  customerNumber: "C801",\n  name: { first: "Elena", last: "Novak" },\n  contact: { email: "elena@example.com" },\n  addresses: [{ type: "SHIPPING", city: "Vancouver", country: "Canada" }],\n  status: "ACTIVE"\n})'
                ),
                "One customer with nested `name`, `contact`, and `addresses`.",
            ),
            (
                "Insert an order with two items",
                "Run:\n\n"
                + js(
                    'db.orders.insertOne({\n  orderNumber: "O5100",\n  customerId: db.customers.findOne({ customerNumber: "C801" })._id,\n  items: [\n    { sku: "A620", quantity: 1, unitPrice: Decimal128("69.99") },\n    { sku: "A610", quantity: 1, unitPrice: Decimal128("49.99") }\n  ],\n  total: Decimal128("119.98"),\n  paymentStatus: "PENDING",\n  fulfillmentStatus: "NEW",\n  createdAt: new Date()\n})'
                ),
                "The order snapshots customer fields and embeds line items.",
            ),
            (
                "Verify every insert",
                "Run:\n\n"
                + js(
                    'db.products.find({ sku: { $in: ["A620", "A610", "A611", "A612"] } }, { sku: 1, name: 1, price: 1 })\n'
                    'db.customers.findOne({ customerNumber: "C801" })\n'
                    'db.orders.findOne({ orderNumber: "O5100" })'
                ),
                "Four products, one customer, one order. Confirm `price` and `unitPrice` are Decimal128, not strings.",
            ),
        ],
        [
            "Captured insert ids / acknowledged results",
            "Used Decimal128 for money",
            "Verified with `find` / `findOne` after writing",
        ],
    )
)

GUIDES.append(
    guide(
        10,
        "update-product-data",
        "Update Product Data",
        "15 min",
        "Intermediate",
        "Use `$set`, `$inc`, `$rename`, `$unset`, and a filtered `updateMany`.",
        [
            (
                "Preview then change a price",
                "Run the filter first, then:\n\n"
                + js(
                    'db.products.find({ sku: "A620" })\n'
                    'db.products.updateOne(\n  { sku: "A620" },\n  { $set: { price: Decimal128("64.99"), updatedAt: new Date() } }\n)'
                ),
                "`matchedCount: 1`, `modifiedCount: 1` if the price changed. If A620 is missing, complete Exercise 4.9 first.",
            ),
            (
                "Add a nested warranty field",
                "Run:\n\n"
                + js(
                    'db.products.updateOne(\n  { sku: "L100" },\n  { $set: { "attributes.warrantyYears": 2 } }\n)'
                ),
                "`attributes` still contains `memoryGB`. The warranty field is added beside it.",
            ),
            (
                "Increase inventory",
                "Run:\n\n"
                + js('db.products.updateOne({ sku: "L100" }, { $inc: { stockQuantity: 5 } })'),
                "`stockQuantity` increases by 5 (from 8 to 13 on a fresh load).",
            ),
            (
                "Rename an incorrect field",
                "Run:\n\n"
                + js(
                    'db.products.updateMany(\n  { legacyName: { $exists: true } },\n  { $rename: { legacyName: "catalogName" } }\n)'
                ),
                "`L190` now has `catalogName` instead of `legacyName`.",
            ),
            (
                "Remove a temporary field and deactivate discontinued",
                "Run:\n\n"
                + js(
                    'db.products.updateOne({ sku: "A410" }, { $unset: { temporaryNote: "" } })\n'
                    'db.products.updateMany(\n  { tags: "discontinued" },\n  { $set: { active: false } }\n)'
                ),
                "`A410` no longer has `temporaryNote`. Discontinued items stay inactive. Preview `updateMany` with `find` before running it in production.",
            ),
        ],
        [
            "Previewed filters with `find()` before `updateMany`",
            "Used dotted `$set` for nested warranty",
            "Interpreted `matchedCount` vs `modifiedCount`",
        ],
    )
)

GUIDES.append(
    guide(
        11,
        "modify-arrays",
        "Modify Arrays",
        "15 min",
        "Intermediate",
        "Use `$push`, `$addToSet`, `$each`, `$pull`, positional `$`, and `$[]`.",
        [
            (
                "Push a tag (may duplicate)",
                "Run twice:\n\n"
                + js('db.products.updateOne({ sku: "A620" }, { $push: { tags: "featured" } })'),
                "The second run adds a second `featured` if you used `$push` both times. That is the teaching point.",
            ),
            (
                "Add a tag without duplicates",
                "Run twice:\n\n"
                + js('db.products.updateOne({ sku: "A620" }, { $addToSet: { tags: "office" } })'),
                "Second run: `matchedCount: 1`, `modifiedCount: 0` if `office` is already present.",
            ),
            (
                "Add several tags",
                "Run:\n\n"
                + js(
                    'db.products.updateOne(\n  { sku: "A620" },\n  { $addToSet: { tags: { $each: ["portable", "usb-c"] } } }\n)'
                ),
                "`usb-c` is already on A620 from insert — `$addToSet` leaves it unique. `portable` is added.",
            ),
            (
                "Remove a deprecated tag",
                "Run:\n\n"
                + js('db.products.updateOne({ sku: "L190" }, { $pull: { tags: "discontinued" } })'),
                "`discontinued` is removed from `L190`. The product can still be `active: false`.",
            ),
            (
                "Update one order item and mark all items reviewed",
                "Run:\n\n"
                + js(
                    'db.orders.updateOne(\n  { orderNumber: "O5001", "items.sku": "L100" },\n  { $set: { "items.$.quantity": 2 } }\n)\n'
                    'db.orders.updateOne(\n  { orderNumber: "O5001" },\n  { $set: { "items.$[].reviewed": false } }\n)'
                ),
                "The L100 line quantity becomes 2. Every item on that order gets `reviewed: false`.",
            ),
        ],
        [
            "Explained why `$push` can duplicate",
            "Used `$addToSet` with `$each`",
            "Used `$` and `$[]` correctly",
        ],
    )
)

GUIDES.append(
    guide(
        12,
        "perform-an-upsert",
        "Perform an Upsert",
        "10 min",
        "Intermediate",
        "Upsert a product by SKU so `createdAt` is set only on insert and `updatedAt` is always set.",
        [
            (
                "Run the upsert for a new SKU",
                "Run:\n\n"
                + js(
                    'db.products.updateOne(\n  { sku: "A700" },\n  {\n    $set: {\n      name: "Portable Charger",\n      category: "ACCESSORY",\n      price: Decimal128("39.99"),\n      active: true,\n      updatedAt: new Date()\n    },\n    $setOnInsert: { createdAt: new Date(), stockQuantity: 25 }\n  },\n  { upsert: true }\n)'
                ),
                "`upsertedId` is present. `createdAt` exists.",
            ),
            (
                "Inspect the inserted document",
                "Run:\n\n" + js('db.products.findOne({ sku: "A700" })'),
                "Fields from `$set` and `$setOnInsert` are present. Filter used the unique `sku`.",
            ),
            (
                "Run the same upsert again",
                "Repeat the `updateOne` from Step 1, then `findOne` again.",
                "`matchedCount: 1`, `modifiedCount` may be 1 because `updatedAt` changes. `createdAt` must be **unchanged**. `upsertedId` is absent.",
            ),
            (
                "Compare insert vs update outcomes",
                "Write two bullets: first-run result vs second-run result.",
                "First run inserts; second run updates. `$setOnInsert` does not overwrite `createdAt`.",
            ),
        ],
        [
            "Used a unique SKU filter",
            "Set `createdAt` only on insert",
            "Compared both runs' write results",
        ],
    )
)

GUIDES.append(
    guide(
        13,
        "correct-unsafe-operations",
        "Correct Unsafe Operations",
        "10 min",
        "Intermediate",
        "Explain the risk of three unsafe writes and replace them with safer alternatives.",
        [
            (
                "Unfiltered updateMany",
                "The unsafe command is:\n\n"
                + js("db.products.updateMany({}, { $set: { active: false } })")
                + "\n\nWrite the risk and a safer filter (for example discontinued items only). Do **not** run the unsafe command.",
                "Risk: every product becomes inactive. Safer: preview `{ tags: \"discontinued\" }` or `{ discontinuedAt: { $exists: true } }`, count, then `updateMany` with that filter.",
            ),
            (
                "Empty deleteMany",
                "The unsafe command is:\n\n"
                + js("db.orders.deleteMany({})")
                + "\n\nWrite the risk and a safer sequence.",
                "Risk: all orders are removed. Safer: never use `{}`; filter on test `orderNumber` values; `find` → `countDocuments` → `deleteMany`.",
            ),
            (
                "Replacing a nested object",
                "This update wipes sibling `contact` fields:\n\n"
                + js(
                    'db.customers.updateOne(\n  { customerNumber: "C101" },\n  { $set: { contact: { email: "new@example.com" } } }\n)'
                )
                + "\n\nRewrite it so only email changes.",
                "Safer:\n\n"
                + js(
                    'db.customers.updateOne(\n  { customerNumber: "C101" },\n  { $set: { "contact.email": "new@example.com" } }\n)'
                ),
            ),
            (
                "Class debrief",
                "Share one rewrite. Listen for the instructor solution and adjust your notes.",
                "You can name the blast radius of `{}` and the difference between replacing an embedded document and setting one path.",
            ),
        ],
        [
            "Did not execute the empty-filter writes",
            "Provided a precise alternative for each case",
            "Used dotted `$set` for nested email",
        ],
        discussion=True,
    )
)

GUIDES.append(
    guide(
        14,
        "diagnose-query-errors",
        "Diagnose Query Errors",
        "15 min",
        "Intermediate",
        "Correct seven broken queries covering case, BSON type, dotted paths, operators, projection, `$elemMatch`, and update operators.",
        [
            (
                "Wrong field capitalization",
                "This returns nothing:\n\n"
                + js('db.products.find({ Category: "LAPTOP" })')
                + "\n\nRewrite it.",
                "Field is `category` (lowercase). MongoDB does not fold identifier case.",
            ),
            (
                "String instead of Decimal128",
                "This comparison is unreliable:\n\n"
                + js('db.products.find({ price: { $gt: "100.00" } })')
                + "\n\nRewrite it.",
                'Use `{ price: { $gt: Decimal128("100.00") } }`. Types must match stored BSON.',
            ),
            (
                "Unquoted dotted path",
                "This is invalid:\n\n"
                + js("db.products.find({ attributes.memoryGB: 16 })")
                + "\n\nRewrite it.",
                'Quote the path: `{ "attributes.memoryGB": 16 }`.',
            ),
            (
                "Incorrect operator placement",
                "This is wrong:\n\n"
                + js('db.products.find({ $gt: { price: Decimal128("100.00") } })')
                + "\n\nRewrite it.",
                "Comparison operators live **inside** the field: `{ price: { $gt: Decimal128(\"100.00\") } }`.",
            ),
            (
                "Mixed projection",
                "This errors:\n\n"
                + js("db.products.find({}, { name: 1, tags: 0 })")
                + "\n\nProvide two legal alternatives.",
                "Inclusion `{ name: 1, price: 1, _id: 0 }` **or** exclusion `{ tags: 0, attributes: 0 }`. `_id` is the only mix allowed.",
            ),
            (
                "Incorrect $elemMatch",
                "Rewrite so both conditions apply to one item:\n\n"
                + js(
                    'db.orders.find({ "items.sku": "L100", "items.quantity": { $gte: 2 } })'
                ),
                "Use `items: { $elemMatch: { sku: \"L100\", quantity: { $gte: 2 } } }`.",
            ),
            (
                "Missing update operator",
                "This replacement-style document is rejected by modern `updateOne`:\n\n"
                + js(
                    'db.products.updateOne({ sku: "L100" }, { featured: true })'
                )
                + "\n\nRewrite it.",
                "Use `{ $set: { featured: true } }`. Bare field assignment is not an update operator.",
            ),
        ],
        [
            "Corrected all seven queries",
            "Named the class of each mistake",
            "Did not run the mixed projection as-is expecting success",
        ],
        discussion=True,
    )
)

# Labs 4.1–4.10 become exercises 4.15–4.24
GUIDES.append(
    guide(
        15,
        "lab-dataset-verification",
        "Lab 4.1 Dataset Verification",
        "15 min",
        "Beginner",
        "Confirm `training_store` collections, counts, field paths, and BSON types before querying.",
        [
            (
                "Select the database",
                "Run `use training_store`.",
                "The prompt shows `training_store`.",
            ),
            (
                "List collections",
                "Run `show collections`.",
                "`products`, `customers`, `orders`, and `reviews` are listed.",
            ),
            (
                "Count each collection",
                "Run:\n\n"
                + js(
                    "db.products.countDocuments({})\n"
                    "db.customers.countDocuments({})\n"
                    "db.orders.countDocuments({})\n"
                    "db.reviews.countDocuments({})"
                ),
                "On a fresh load: products 13, customers 6, orders 17, reviews 6. If you already inserted lab SKUs, counts are higher — note that.",
            ),
            (
                "Inspect one document from each collection",
                "Run `findOne()` on `products`, `customers`, `orders`, and `reviews`.",
                "You can point to nested objects and arrays on the samples.",
            ),
            (
                "Record field paths and BSON types",
                "On the product and order, list at least: `sku` (string), `price` (decimal), `tags` (array), `attributes.memoryGB` (int, if present), `items.sku`, `createdAt` (date).",
                "The observation sheet names paths with dotted notation and types. `XBAD.price` is a string — record that exception.",
            ),
        ],
        [
            "Listed four collections",
            "Recorded counts",
            "Named at least one nested path and one array",
            "Noted Decimal128 vs the string-price exception",
        ],
        extra="## Observation sheet\n\n| Collection | Count | Nested path | Array | Notable type |\n|------------|-------|-------------|-------|--------------|\n| products | | | | |\n| customers | | | | |\n| orders | | | | |\n| reviews | | | | |\n",
    )
)

GUIDES.append(
    guide(
        16,
        "lab-product-query",
        "Lab 4.2 Product Query Lab",
        "30 min",
        "Intermediate",
        "Build ten product queries covering equality, range, nested fields, tags, missing fields, types, sort, and distinct.",
        [
            ("All active products", "Write and run a filter on `active: true`.", "Inactive SKU `L190` is absent."),
            ("Specified category", 'Find `{ category: "LAPTOP" }`.', "Three laptops: `L100`, `L110`, `L190`."),
            ("Price range", 'Find price `$gte` 50 and `$lte` 150 as Decimal128.', "Includes `S200`, `S210`, `B300`."),
            ("Any of several categories", 'Use `$in: ["BOOK", "ACCESSORY"]`.', "Books and accessories, not laptops or shoes."),
            ("Nested hardware attribute", 'Find `{ "attributes.memoryGB": { $gte: 16 } }`.', "`L100` (16) and `L110` (32). `L190` has 8 GB."),
            ("Selected tags", 'Use `$all: ["database", "technology"]`.', "`B300`."),
            ("Missing optional field", "Find `{ discountPrice: { $exists: false } }`.", "Most products; `P1001` and `B310` are excluded."),
            ("Inconsistent price types", 'Find `{ price: { $type: "string" } }`.', "`XBAD` only."),
            ("Five most expensive active", "Filter active, sort price descending with `_id` tiebreaker, limit 5, project name and price.", "Top of the list is `L110` at 1899.99."),
            ("Distinct categories", 'Run `db.products.distinct("category")`.', "Array including `ACCESSORY`, `BOOK`, `LAPTOP`, `SHOE`."),
        ],
        [
            "Completed all ten queries",
            "Used Decimal128 for price ranges",
            "Quoted dotted paths",
            "Saved or can re-run each query",
        ],
    )
)

GUIDES.append(
    guide(
        17,
        "lab-customer-order-query",
        "Lab 4.3 Customer and Order Query Lab",
        "30 min",
        "Intermediate",
        "Query customers and orders by identifier, nested contact, addresses, items, status, dates, and totals.",
        [
            ("Customer by number", 'findOne `{ customerNumber: "C101" }`.', "Aisha Khan with nested `name` and `contact`."),
            ("Customer by email", 'find `{ "contact.email": "aisha@example.com" }`.', "The same customer. Quote the dotted path."),
            ("Address in a city", 'find `{ "addresses.city": "Toronto" }` or `$elemMatch` on SHIPPING + Toronto.', "`C101`."),
            ("Order by number", 'findOne `{ orderNumber: "O5001" }`.', "Two line items (L100 qty 1, A410 qty 2), paymentStatus PENDING."),
            ("Orders for a customer", 'Store C101 `_id`, then find `{ customerId: c101Id }`.', "`O5001`, `O6101`, and other C101 orders."),
            ("Orders containing a SKU", 'find `{ "items.sku": "L100" }`.', "`O5001`, `O6101`, and `O6401`."),
            ("Same item two conditions", "Use `$elemMatch` for sku L100 and quantity ≥ 2.", "Only `O6401`."),
            ("One of several statuses", '`paymentStatus` `$in: ["PENDING", "FAILED"]`.', "`O5001`, `O6401`, `O6402`, `O6499`."),
            ("Created during a date range", "Filter `createdAt` `$gte` ISODate 2026-09-01 and `$lt` ISODate 2026-10-01.", "September 2026 orders including `O5001` and `O6401`."),
            ("Orders above a total", 'total `$gt` Decimal128("1000.00").', "Includes `O5001`, `O6101`, `O6401`, and other high-value orders."),
        ],
        [
            "Used dotted paths for nested customer fields",
            "Applied `$elemMatch` on order items",
            "Used ISODate for the date range, not strings",
        ],
    )
)

GUIDES.append(
    guide(
        18,
        "lab-projection-pagination",
        "Lab 4.4 Projection and Pagination Lab",
        "20 min",
        "Beginner",
        "Shape result documents and page through a sorted product list.",
        [
            ("Product summary projection", "Active products: `name`, `category`, `price`, no `_id`.", "Compact catalog rows."),
            ("Customer-contact projection", "`name.first`, `name.last`, `contact.email` for ACTIVE customers.", "No addresses in the result."),
            ("Order-status projection", "`orderNumber`, `status`, `total`.", "Operations list without line items."),
            ("Sorted product list", "Sort `{ category: 1, price: -1, _id: 1 }`.", "Deterministic order within category."),
            ("Limited result set", "Limit 5 on the sorted active products.", "Exactly five documents."),
            ("Two pages of results", "skip 0 limit 5 then skip 5 limit 5 with the same sort.", "No overlapping `_id` values."),
            ("Count matching documents", "`countDocuments` on the same filter as the list.", "Count equals how many documents pagination would eventually cover."),
        ],
        [
            "Did not mix inclusion and exclusion",
            "Used a stable sort for pagination",
            "Counted with `countDocuments`",
        ],
    )
)

GUIDES.append(
    guide(
        19,
        "lab-insert-operations",
        "Lab 4.5 Insert Operations Lab",
        "25 min",
        "Beginner",
        "Insert a product, several products, a customer, and a related order; inspect ids and types.",
        [
            ("Insert one product", 'Insert SKU `A600` Wireless Presenter, ACCESSORY, Decimal128 44.99, active true.', "`insertedId` present. Skip if A600 already exists from a demo."),
            ("Insert several products", "insertMany two more accessories with unique SKUs `A610` and `A611`.", "`insertedIds` has two entries."),
            ("Insert a customer", 'customerNumber `C601` with nested name, contact, and one shipping address.', "Document round-trips with the same shape."),
            ("Insert an order referencing the customer", "Order `O5200` with an embedded customer snapshot and an item for A600.", "Order stores name/email snapshot, not only the id."),
            ("Inspect inserted IDs", "Print the insert results you saved, or query by SKU / customerNumber.", "You can name each new `_id`."),
            ("Query every new document", "find the products, customer, and order.", "All four (or more) documents exist."),
            ("Correct inconsistent types", "If any price was a number or string, `$set` it to Decimal128 and re-query `$type`.", "New money fields are decimal."),
        ],
        [
            "Used Decimal128 on insert",
            "Embedded a customer snapshot on the order",
            "Verified with queries, not only insert acknowledgements",
        ],
    )
)

GUIDES.append(
    guide(
        20,
        "lab-update-operations",
        "Lab 4.6 Update Operations Lab",
        "30 min",
        "Intermediate",
        "Practice `$set`, `$unset`, `$inc`, `$min`, `$max`, `$rename`, nested updates, and `updateMany` with the preview-update-verify loop.",
        [
            (
                "Preview + $set",
                "Preview `{ sku: \"A600\" }` if you created it (otherwise use `A110`). `$set` `featured: true` and `updatedAt`. Inspect the write result and findOne.",
                "Four-part loop completed: preview, update, result, verify.",
            ),
            (
                "$unset",
                "Add `temporaryNote` with `$set`, verify, then `$unset` it.",
                "Field is present after set and absent after unset.",
            ),
            (
                "$inc",
                "`$inc` `stockQuantity` by 3 on that product.",
                "Quantity increased by exactly 3.",
            ),
            (
                "$min and $max",
                "On the same product, `$min` a `lowestPrice` of 40.00 and `$max` a `highestPrice` of 50.00 (use Decimal128). Run twice if needed.",
                "`$min` only lowers; `$max` only raises. Second run may yield `modifiedCount: 0`.",
            ),
            (
                "$rename leftover",
                "If `L190` still has `legacyName`, `$rename` it to `catalogName`. If already renamed, `matchedCount` may be 0.",
                "No document remains with `legacyName`.",
            ),
            (
                "Nested-field update",
                '`$set` `"contact.email"` for `C310` to a new address, without replacing `contact`.',
                "`phone` on C310 is still present.",
            ),
            (
                "updateMany with preview",
                "Preview `{ category: \"ACCESSORY\", active: true }`, count, then `$set` `taxable: true`. Check `matchedCount`.",
                "Count from preview equals `matchedCount`. You did not use `{}`.",
            ),
        ],
        [
            "Every write had preview and verification",
            "Did not replace a whole nested object accidentally",
            "Interpreted a `modifiedCount: 0` case",
        ],
    )
)

GUIDES.append(
    guide(
        21,
        "lab-array-manipulation",
        "Lab 4.7 Array Manipulation Lab",
        "30 min",
        "Intermediate",
        "Add, unique-add, batch-add, and remove tags; update one, all, and filtered array elements on an order.",
        [
            ("$push a tag", '`$push` `"clearance"` onto `A110`.', "Array gains `clearance` even if you run it twice (duplicates)."),
            ("$addToSet", '`$addToSet` `"office"` on `A110`. Run twice.', "Second run does not duplicate `office`."),
            ("$each", "`$addToSet` with `$each` for `portable` and `featured`.", "Both values present once."),
            ("$pull", '`$pull` `"clearance"` from `A110`.', "No `clearance` values remain (all duplicates removed)."),
            ("Positional $", 'On `O5001`, match `"items.sku": "A410"` and `$set` `"items.$.quantity"` to 4.', "Only the mouse line changes."),
            ("All elements $[]", '`$set` `"items.$[].reviewed": true` on `O5001`.', "Every line item has `reviewed: true`."),
            (
                "arrayFilters",
                "On `O5001`, `$set` `\"items.$[item].discounted\": true` with `arrayFilters: [ { \"item.unitPrice\": { $gte: Decimal128(\"100.00\") } } ]`.",
                "The L100 line is discounted; the cheaper mouse line is not.",
            ),
        ],
        [
            "Contrasted `$push` and `$addToSet`",
            "Updated one element with `$`",
            "Used `arrayFilters` for a price threshold",
        ],
    )
)

GUIDES.append(
    guide(
        22,
        "lab-replace-and-upsert",
        "Lab 4.8 Replace and Upsert Lab",
        "20 min",
        "Intermediate",
        "Compare `$set`, `replaceOne`, and a repeated upsert on a copied test document.",
        [
            (
                "Copy a test document",
                'Insert a copy of `A410` as sku `TEMP-200` (new `_id`). Include extra field `notes: "lab copy"`.',
                "TEMP-200 exists with `notes`.",
            ),
            (
                "Update selected fields with $set",
                '`$set` `price` and `featured` on TEMP-200. Then findOne.',
                "`notes` and `tags` still exist.",
            ),
            (
                "Replace the copied document",
                "replaceOne TEMP-200 with a document that has sku, name, category, price, active, updatedAt only.",
                "`notes`, `tags`, and other omitted fields **disappear**. `_id` remains.",
            ),
            (
                "Compare $set vs replaceOne",
                "Write two bullets describing remaining fields after each operation.",
                "You can explain that replace is not a partial update.",
            ),
            (
                "Perform an upsert",
                'updateOne `{ sku: "A700" }` with `$set` + `$setOnInsert` and `upsert: true`.',
                "First run returns `upsertedId`.",
            ),
            (
                "Run the same upsert again",
                "Repeat Step 5.",
                "No new `upsertedId`. `createdAt` unchanged if it was in `$setOnInsert`.",
            ),
            (
                "Compare insert and update outcomes",
                "Record both write results in your notes.",
                "You can distinguish insert-via-upsert from update-via-upsert.",
            ),
        ],
        [
            "Showed fields lost after replaceOne",
            "Used a unique SKU for upsert",
            "Compared both upsert runs",
        ],
    )
)

GUIDES.append(
    guide(
        23,
        "lab-delete-operations",
        "Lab 4.9 Delete Operations Lab",
        "20 min",
        "Intermediate",
        "Delete only temporary lab records using a preview-count-delete-verify sequence.",
        [
            (
                "Insert temporary documents",
                'insertMany products `TEMP-100` and `TEMP-101` with `labTag: "module4"` plus a throwaway order `TEMP-O1`.',
                "Two products and one order exist for this lab only.",
            ),
            (
                "Build a precise deletion filter",
                'Use `{ sku: /^TEMP-/ }` or `{ labTag: "module4" }` — not `{}`.',
                "The filter cannot match L100 or production-like SKUs.",
            ),
            ("Preview matches", "find(filter) on products.", "Only TEMP-100 and TEMP-101."),
            ("Count matches", "countDocuments(filter).", "Count is 2."),
            ("Delete one document", 'deleteOne `{ sku: "TEMP-100" }`. Inspect `deletedCount`.', "`deletedCount: 1`. TEMP-101 remains."),
            ("Delete multiple temporary documents", "deleteMany with the remaining TEMP filter. Then delete the throwaway order by `orderNumber`.", "`deletedCount` matches the preview of what was left."),
            ("Inspect deletedCount", "Record both delete results.", "Sums equal the documents you intended to remove."),
            (
                "Verify no unintended removals",
                'countDocuments on products; findOne L100 and O5001.',
                "Catalog SKUs and real orders remain. Reloading `load.js` restores a clean set if needed.",
            ),
        ],
        [
            "Never used `deleteMany({})`",
            "Previewed and counted before deleting",
            "Confirmed L100 / O5001 still exist",
        ],
    )
)

GUIDES.append(
    guide(
        24,
        "lab-integrated-crud-challenge",
        "Lab 4.10 Integrated CRUD Challenge",
        "45 min",
        "Intermediate",
        "Walk a store scenario from new product through order updates to a verified soft-delete.",
        [
            ("Insert the product", 'Insert sku `A800`, name "Magnetic Charger", ACCESSORY, Decimal128 34.99, stockQuantity 10, active true.', "findOne by sku succeeds."),
            ("Verify the product", "Project sku, name, price, stockQuantity.", "Types: decimal price, int stock."),
            ("Add unique tags", '`$addToSet` `$each` `["usb-c", "featured", "accessory"]`.', "No duplicates if a tag already existed."),
            ("Increase inventory", "`$inc` stockQuantity by 15.", "Stock is 25 on a first run."),
            ("Create a customer", 'C801 with nested name/contact and status ACTIVE.', "findOne by customerNumber."),
            ("Add a shipping address", '`$push` an address `{ type: "shipping", city: "Montreal", country: "Canada" }`.', "addresses is an array with Montreal."),
            ("Create an order containing the product", "O5800 with snapshot of C801 and one item A800 qty 1, status NEW, Decimal128 total.", "Order exists with embedded item."),
            ("Update the order status", '`$set` status `"PROCESSING"` and `$push` statuses `"PROCESSING"` (or `$addToSet`).', "Status is PROCESSING."),
            ("Update the item quantity", 'Positional `$` set quantity to 2 and `$set` total to Decimal128("69.98").', "Line quantity and order total agree."),
            ("Order summary projection", "find O5800 projecting orderNumber, status, total, items.sku, items.quantity — no `_id`.", "Compact summary only."),
            ("Count the customer’s orders", 'countDocuments `{ customerId: c801Id }` after looking up C801.', "At least 1."),
            ("Soft-delete the product", '`$set` `{ active: false, deletedAt: new Date() }` on A800 — do not deleteOne.', "Product still exists; active is false."),
            ("Verify all final documents", "find customer C801, order O5800, product A800.", "All three exist. Product is inactive. Order is PROCESSING with qty 2."),
        ],
        [
            "Completed the scenario without dropping collections",
            "Used unique add for tags and positional update for quantity",
            "Soft-deleted rather than hard-deleted the product",
            "Verified every write",
        ],
    )
)

GUIDES.append(
    guide(
        25,
        "practical-challenge",
        "Module 4 Practical Challenge",
        "30–45 min",
        "Intermediate",
        "Turn business requests into a verified query script with safety controls.",
        [
            (
                "Find and project",
                'Find active products priced below Decimal128("80.00"). Project name, category, price, no `_id`. Record the count.',
                "A saved query plus the list you got.",
            ),
            (
                "Upsert a product",
                "Upsert sku `A900` (or a SKU the instructor assigns) with `$set` + `$setOnInsert` createdAt.",
                "Write result shows insert or update depending on prior labs.",
            ),
            (
                "Unique tags and inventory",
                "`$addToSet` two tags; `$inc` stockQuantity.",
                "`modifiedCount` interpreted correctly on a second run.",
            ),
            (
                "Find orders containing a product",
                "Query `items.sku` for L100 (or the new SKU if ordered).",
                "Matching order numbers listed.",
            ),
            (
                "Update matching item quantity and order status",
                "Use `$elemMatch` or positional `$` to change quantity; `$set` status from NEW to PROCESSING on a test order only.",
                "You previewed the order filter first.",
            ),
            (
                "Deactivate discontinued and remove test orders",
                "updateMany discontinued → active false after preview. deleteMany only TEMP- or lab order numbers after count.",
                "Safety controls are written beside each write: filter, count, deletedCount.",
            ),
            (
                "Assemble the deliverable",
                "One mongosh script, expected results, write counts, before/after evidence, and a short safety paragraph.",
                "A teammate could replay the script on a reloaded `training_store`.",
            ),
        ],
        [
            "Accurate filters and BSON types",
            "Safe updates and deletes with previews",
            "Correct array handling",
            "Result verification for every write",
        ],
    )
)


def write_all() -> list[tuple[int, str, str, str, str]]:
    OUT.mkdir(parents=True, exist_ok=True)
    meta = []
    for num, slug, title, time, typ, objective, md in GUIDES:
        path = OUT / f"exercise-4.{num}-{slug}.md"
        path.write_text(md, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
        meta.append((num, slug, title, time, typ, objective))
    return meta


if __name__ == "__main__":
    rows = write_all()
    print(f"Done. {len(rows)} lab guides.")

# Module 4: The MongoDB Query Language

The MongoDB Query Language, or MQL, provides commands for retrieving, filtering, projecting, updating and deleting documents.

This module continues with the `training_store` database and its collections:

```text
training_store
├── products
├── customers
├── orders
└── reviews
```

Start by selecting the database:

```javascript
use training_store
```

## 1. Basic Retrieval Operations

### `find()`

`find()` retrieves all documents that match a filter.

Retrieve all products

```javascript
db.products.find()
```

An empty filter means “match every document”:

```javascript
db.products.find({})
```

Retrieve products from one category

```javascript
db.products.find({
  category: "Electronics"
})
```

Retrieve an exact product

```javascript
db.products.find({
  sku: "ELEC-1001"
})
```

`find()` returns a cursor, which allows MongoDB to process the results without necessarily loading every matching document into memory at once.

Format, sort and limit results

```javascript
db.products.find()
  .sort({ price: -1 })
  .limit(5)
```

Sort values:

* `1` means ascending.
* `-1` means descending.

### `findOne()`

`findOne()` returns a single matching document.

```javascript
db.products.findOne({
  sku: "ELEC-1001"
})
```

If no document matches, it returns `null`.

Use `findOne()` when:

* The filter uses a unique field.
* Only one document is required.
* The application does not need a result cursor.

### Counting documents

#### `countDocuments()`

Count documents that match a filter:

```javascript
db.products.countDocuments({
  category: "Electronics"
})
```

Count every document accurately:

```javascript
db.products.countDocuments({})
```

#### `estimatedDocumentCount()`

Estimate the total number of documents using collection metadata:

```javascript
db.products.estimatedDocumentCount()
```

This method does not accept a query filter.

#### Legacy `count()`

You may encounter older examples such as:

```javascript
db.products.find({
  category: "Electronics"
}).count()
```

For new code, prefer:

* `countDocuments()` when accuracy or filtering is required
* `estimatedDocumentCount()` for a fast approximate collection total

### `distinct()`

`distinct()` returns unique values for a particular field.

Retrieve distinct categories

```javascript
db.products.distinct("category")
```

Possible result:

```javascript
[
  "Books",
  "Electronics"
]
```

Retrieve distinct values from filtered documents

```javascript
db.products.distinct(
  "specifications.connection",
  { category: "Electronics" }
)
```

Retrieve distinct array elements

If documents contain:

```javascript
{
  tags: ["wireless", "mouse", "accessory"]
}
```

This operation returns unique tag values:

```javascript
db.products.distinct("tags")
```

## 2. Projection

Projection controls which fields appear in query results.

The general syntax is:

```javascript
db.collection.find(filter, projection)
```

Include selected fields

```javascript
db.products.find(
  { category: "Electronics" },
  {
    name: 1,
    price: 1,
    stock: 1
  }
)
```

MongoDB includes `_id` by default:

```javascript
{
  _id: ObjectId("..."),
  name: "Wireless Mouse",
  price: Decimal128("39.99"),
  stock: 120
}
```

Exclude `_id` explicitly:

```javascript
db.products.find(
  { category: "Electronics" },
  {
    _id: 0,
    name: 1,
    price: 1,
    stock: 1
  }
)
```

Exclude selected fields

```javascript
db.products.find(
  {},
  {
    specifications: 0,
    createdAt: 0
  }
)
```

Inclusion and exclusion rule

Except for `_id`, inclusion and exclusion should not normally be mixed in the same basic projection.

Valid:

```javascript
{ name: 1, price: 1, _id: 0 }
```

Valid:

```javascript
{ specifications: 0, createdAt: 0 }
```

Avoid:

```javascript
{ name: 1, specifications: 0 }
```

Project nested fields

```javascript
db.products.find(
  { sku: "ELEC-1001" },
  {
    _id: 0,
    name: 1,
    "specifications.connection": 1
  }
)
```

Project the first matching array element

```javascript
db.customers.find(
  {
    "addresses.type": "home"
  },
  {
    firstName: 1,
    lastName: 1,
    "addresses.$": 1
  }
)
```

## 3. Comparison Query Operators

Comparison operators are placed inside the field being evaluated:

```javascript
{
  field: {
    $operator: value
  }
}
```

`$eq` — equal to

```javascript
db.products.find({
  category: { $eq: "Electronics" }
})
```

The shorter form is equivalent:

```javascript
db.products.find({
  category: "Electronics"
})
```

`$ne` — not equal to

```javascript
db.products.find({
  category: { $ne: "Books" }
})
```

Be careful: `$ne` can also match documents where the field is missing.

`$gt` — greater than

```javascript
db.products.find({
  stock: { $gt: 50 }
})
```

`$gte` — greater than or equal to

```javascript
db.products.find({
  stock: { $gte: 75 }
})
```

`$lt` — less than

```javascript
db.products.find({
  price: { $lt: NumberDecimal("50.00") }
})
```

`$lte` — less than or equal to

```javascript
db.products.find({
  price: { $lte: NumberDecimal("89.99") }
})
```

Range query

Multiple operators can be applied to the same field:

```javascript
db.products.find({
  price: {
    $gte: NumberDecimal("40.00"),
    $lte: NumberDecimal("100.00")
  }
})
```

This means:

```text
40.00 ≤ price ≤ 100.00
```

`$in` — matches any listed value

```javascript
db.products.find({
  category: {
    $in: ["Electronics", "Books"]
  }
})
```

`$in` behaves like an OR operation against one field.

`$nin` — matches none of the listed values

```javascript
db.products.find({
  category: {
    $nin: ["Clothing", "Furniture"]
  }
})
```

Be careful: `$nin` can also match documents where the field does not exist.

## 4. Other Useful Query Operators

`$exists`

Find documents containing a field:

```javascript
db.products.find({
  "specifications.rechargeable": {
    $exists: true
  }
})
```

Find documents where the field is missing:

```javascript
db.products.find({
  "specifications.rechargeable": {
    $exists: false
  }
})
```

`$type`

Find fields stored as a particular BSON type:

```javascript
db.products.find({
  price: {
    $type: "decimal"
  }
})
```

`$regex`

Search strings using a regular expression:

```javascript
db.products.find({
  name: {
    $regex: "mouse",
    $options: "i"
  }
})
```

The `i` option makes the search case-insensitive.

An unanchored, case-insensitive regular expression may be expensive on a large collection. Index and search design should be considered for production workloads.

Date comparison

```javascript
db.orders.find({
  orderedAt: {
    $gte: ISODate("2026-09-22T00:00:00Z"),
    $lt: ISODate("2026-09-23T00:00:00Z")
  }
})
```

Using a half-open range—start inclusive and end exclusive—usually avoids problems with time components.

## 5. Logical Operators

Implicit AND

Multiple conditions in the same document are implicitly combined with AND:

```javascript
db.products.find({
  category: "Electronics",
  stock: { $gt: 50 }
})
```

This means:

```text
category is Electronics
AND
stock is greater than 50
```

`$and`

Use `$and` to supply conditions explicitly:

```javascript
db.products.find({
  $and: [
    { category: "Electronics" },
    { stock: { $gt: 50 } }
  ]
})
```

This explicit form is especially useful when the same field must appear in separate expressions:

```javascript
db.products.find({
  $and: [
    {
      price: {
        $gte: NumberDecimal("30.00")
      }
    },
    {
      price: {
        $lte: NumberDecimal("100.00")
      }
    }
  ]
})
```

For simple range conditions, the compact form is preferable:

```javascript
db.products.find({
  price: {
    $gte: NumberDecimal("30.00"),
    $lte: NumberDecimal("100.00")
  }
})
```

`$or`

`$or` matches documents satisfying at least one condition:

```javascript
db.products.find({
  $or: [
    { category: "Books" },
    { stock: { $lt: 50 } }
  ]
})
```

`$nor`

`$nor` matches documents that fail every listed condition:

```javascript
db.products.find({
  $nor: [
    { category: "Books" },
    { stock: { $lt: 50 } }
  ]
})
```

This means:

```text
Not a book
AND
stock is not below 50
```

`$not`

`$not` negates another operator expression for a field:

```javascript
db.products.find({
  price: {
    $not: {
      $gt: NumberDecimal("50.00")
    }
  }
})
```

This can also match documents where `price` does not exist. If the field must exist, add an explicit condition:

```javascript
db.products.find({
  price: {
    $exists: true,
    $not: {
      $gt: NumberDecimal("50.00")
    }
  }
})
```

Use `$ne` for a simple “not equal” comparison:

```javascript
db.products.find({
  category: {
    $ne: "Books"
  }
})
```

Combining logical operators

```javascript
db.products.find({
  active: true,
  $or: [
    {
      category: "Books"
    },
    {
      $and: [
        { category: "Electronics" },
        { stock: { $gt: 100 } }
      ]
    }
  ]
})
```

This matches:

```text
Active products
AND
(
    books
    OR
    electronics with stock above 100
)
```

## 6. Querying Arrays

MongoDB can match array elements without manually looping through the array.

Match an array containing a value

```javascript
db.products.find({
  tags: "wireless"
})
```

This matches a document whose `tags` array contains `"wireless"`.

Match all required values

```javascript
db.products.find({
  tags: {
    $all: ["wireless", "accessory"]
  }
})
```

Match by array size

```javascript
db.products.find({
  tags: {
    $size: 3
  }
})
```

Query arrays of embedded documents

Find orders containing a product with a quantity of at least two:

```javascript
db.orders.find({
  items: {
    $elemMatch: {
      sku: "ELEC-1001",
      quantity: { $gte: 2 }
    }
  }
})
```

Why use `$elemMatch`?

Consider:

```javascript
db.orders.find({
  "items.sku": "ELEC-1001",
  "items.quantity": { $gte: 2 }
})
```

Without `$elemMatch`, the two conditions could be satisfied by different elements in the same array.

`$elemMatch` ensures that one array element satisfies all included conditions.

## 7. Update Operation Structure

MongoDB updates normally have three parts:

```javascript
db.collection.updateOne(
  filter,
  update,
  options
)
```

Example:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $set: {
      active: true
    }
  }
)
```

The result includes information similar to:

```javascript
{
  acknowledged: true,
  matchedCount: 1,
  modifiedCount: 1
}
```

* `matchedCount` indicates how many documents matched.
* `modifiedCount` indicates how many documents changed.

If the existing value was already the requested value, `matchedCount` may be `1` while `modifiedCount` is `0`.

## 8. General Update Operators

`$set`

`$set` creates a field or replaces its current value.

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $set: {
      featured: true,
      "specifications.colour": "Space Grey"
    }
  }
)
```

If `featured` does not exist, MongoDB adds it.

`$unset`

Remove a field:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $unset: {
      featured: ""
    }
  }
)
```

The value assigned inside `$unset` is not important.

`$inc`

Increase or decrease a numeric value:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $inc: {
      stock: 10
    }
  }
)
```

Decrease inventory:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $inc: {
      stock: -2
    }
  }
)
```

Using `$inc` is safer than reading a value into the application, calculating a new value and writing it back.

`$mul`

Multiply a numeric value:

```javascript
db.products.updateMany(
  { category: "Electronics" },
  {
    $mul: {
      stock: 2
    }
  }
)
```

For financial price changes, update pipelines or explicit decimal calculations may be preferable to avoid unwanted numeric-type conversions.

`$min`

Update the field only when the supplied value is smaller:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $min: {
      reorderLevel: 20
    }
  }
)
```

`$max`

Update the field only when the supplied value is larger:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $max: {
      highestStockRecorded: 130
    }
  }
)
```

`$rename`

Rename a field:

```javascript
db.products.updateMany(
  {},
  {
    $rename: {
      "name": "productName"
    }
  }
)
```

A field rename affects every matched document. Before applying it broadly, preview the filter:

```javascript
db.products.find(
  { name: { $exists: true } },
  { name: 1 }
)
```

To restore the field:

```javascript
db.products.updateMany(
  {},
  {
    $rename: {
      "productName": "name"
    }
  }
)
```

`$currentDate`

Store the current server date:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $set: {
      active: true
    },
    $currentDate: {
      updatedAt: true
    }
  }
)
```

## 9. Array Update Operators

Array update operators modify arrays without replacing the complete array.

`$push`

Add a value to the end of an array:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $push: {
      tags: "ergonomic"
    }
  }
)
```

If the operation runs twice, `"ergonomic"` can be inserted twice.

Push multiple values

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $push: {
      tags: {
        $each: ["office", "portable"]
      }
    }
  }
)
```

Push and retain a limited number of entries

Consider a bounded status history:

```javascript
db.orders.updateOne(
  { orderNumber: "ORD-2026-1001" },
  {
    $push: {
      statusHistory: {
        $each: [
          {
            status: "Delivered",
            changedAt: new Date()
          }
        ],
        $slice: -10
      }
    }
  }
)
```

This retains only the ten most recent elements.

`$addToSet`

Add a value only if it is not already present:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $addToSet: {
      tags: "wireless"
    }
  }
)
```

Add multiple unique values:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $addToSet: {
      tags: {
        $each: ["office", "wireless", "sale"]
      }
    }
  }
)
```

Use `$addToSet` when duplicates are not allowed.

`$pull`

Remove every array element matching a condition:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $pull: {
      tags: "sale"
    }
  }
)
```

Remove multiple matching values:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $pull: {
      tags: {
        $in: ["temporary", "clearance"]
      }
    }
  }
)
```

Remove embedded documents matching a condition:

```javascript
db.customers.updateOne(
  { email: "priya@example.com" },
  {
    $pull: {
      addresses: {
        type: "work"
      }
    }
  }
)
```

`$pop`

Remove one element from the beginning or end of an array.

Remove the final element:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $pop: {
      tags: 1
    }
  }
)
```

Remove the first element:

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $pop: {
      tags: -1
    }
  }
)
```

`$pop` does not select an element by value. Use `$pull` when removal should be based on content.

## 10. Updating Embedded Array Elements

Positional `$` operator

Update the first matching array element:

```javascript
db.orders.updateOne(
  {
    orderNumber: "ORD-2026-1001",
    "items.sku": "ELEC-1001"
  },
  {
    $set: {
      "items.$.quantity": 3
    }
  }
)
```

The positional `$` identifies the first `items` element matched by the query.

All-positional `$[]` operator

Update every element in an array:

```javascript
db.orders.updateOne(
  { orderNumber: "ORD-2026-1001" },
  {
    $set: {
      "items.$[].reviewed": false
    }
  }
)
```

Filtered positional `$[identifier]`

Update selected elements using `arrayFilters`:

```javascript
db.orders.updateMany(
  {},
  {
    $set: {
      "items.$[item].requiresReview": true
    }
  },
  {
    arrayFilters: [
      {
        "item.quantity": {
          $gte: 2
        }
      }
    ]
  }
)
```

## 11. `updateOne()` Versus `updateMany()`

Update one matching document

```javascript
db.products.updateOne(
  { sku: "ELEC-1001" },
  {
    $set: {
      active: false
    }
  }
)
```

Update every matching document

```javascript
db.products.updateMany(
  { category: "Electronics" },
  {
    $set: {
      department: "Technology"
    }
  }
)
```

Always preview an `updateMany()` filter:

```javascript
db.products.find({
  category: "Electronics"
})
```

Then apply the update using the same filter.

## 12. Upsert Operations

An upsert updates a matching document or inserts a new one when no match exists.

```javascript
db.products.updateOne(
  { sku: "ELEC-2000" },
  {
    $set: {
      name: "USB-C Hub",
      category: "Electronics",
      price: NumberDecimal("59.99"),
      stock: 25,
      active: true
    },
    $setOnInsert: {
      createdAt: new Date()
    }
  },
  {
    upsert: true
  }
)
```

Use upserts when the application intentionally supports “create if missing” behavior.

## 13. Replacing a Document

`replaceOne()` replaces the entire matching document except its immutable `_id`.

```javascript
db.products.replaceOne(
  { sku: "ELEC-2000" },
  {
    sku: "ELEC-2000",
    name: "Seven-Port USB-C Hub",
    category: "Electronics",
    price: NumberDecimal("69.99"),
    stock: 20,
    active: true
  }
)
```

Any old fields that are not included in the replacement disappear.

Use update operators when only selected fields should change.

## 14. Hands-On Lab: Complex Queries

### Exercise 1: Find affordable, available electronics

Requirements:

* Category must be `Electronics`.
* Price must be below `$75`.
* Stock must be greater than zero.
* Show only SKU, name, price and stock.
* Sort by price from lowest to highest.

```javascript
db.products.find(
  {
    category: "Electronics",
    price: {
      $lt: NumberDecimal("75.00")
    },
    stock: {
      $gt: 0
    }
  },
  {
    _id: 0,
    sku: 1,
    name: 1,
    price: 1,
    stock: 1
  }
).sort({
  price: 1
})
```

### Exercise 2: Find priority products

A product is a priority when:

* Stock is below 50, or
* Its tags contain `sale`.

It must also be active.

```javascript
db.products.find({
  active: true,
  $or: [
    {
      stock: {
        $lt: 50
      }
    },
    {
      tags: "sale"
    }
  ]
})
```

### Exercise 3: Find products in a price range

```javascript
db.products.find(
  {
    price: {
      $gte: NumberDecimal("40.00"),
      $lte: NumberDecimal("100.00")
    }
  },
  {
    _id: 0,
    name: 1,
    category: 1,
    price: 1
  }
).sort({
  price: -1
})
```

### Exercise 4: Exclude selected categories

```javascript
db.products.find({
  category: {
    $nin: ["Furniture", "Clothing"]
  }
})
```

If the category must exist:

```javascript
db.products.find({
  category: {
    $exists: true,
    $nin: ["Furniture", "Clothing"]
  }
})
```

### Exercise 5: Find customers in selected cities

```javascript
db.customers.find(
  {
    "addresses.city": {
      $in: ["Brampton", "Toronto"]
    }
  },
  {
    _id: 0,
    firstName: 1,
    lastName: 1,
    email: 1,
    addresses: 1
  }
)
```

### Exercise 6: Find orders containing high-quantity items

```javascript
db.orders.find(
  {
    items: {
      $elemMatch: {
        quantity: {
          $gte: 2
        },
        unitPrice: {
          $lt: NumberDecimal("50.00")
        }
      }
    }
  },
  {
    _id: 0,
    orderNumber: 1,
    customerId: 1,
    items: 1,
    total: 1
  }
)
```

### Exercise 7: Find recent processing orders

```javascript
db.orders.find({
  status: "Processing",
  orderedAt: {
    $gte: ISODate("2026-09-22T00:00:00Z")
  }
}).sort({
  orderedAt: -1
})
```

### Exercise 8: Adjust inventory after a purchase

Before updating, verify the product has sufficient inventory:

```javascript
db.products.findOne({
  sku: "ELEC-1001",
  stock: {
    $gte: 2
  }
})
```

Perform a guarded atomic update:

```javascript
db.products.updateOne(
  {
    sku: "ELEC-1001",
    stock: {
      $gte: 2
    }
  },
  {
    $inc: {
      stock: -2
    },
    $currentDate: {
      updatedAt: true
    }
  }
)
```

If `matchedCount` is zero, there was not enough inventory or the SKU did not exist.

### Exercise 9: Maintain unique product tags

```javascript
db.products.updateOne(
  {
    sku: "ELEC-1001"
  },
  {
    $addToSet: {
      tags: {
        $each: [
          "featured",
          "office",
          "wireless"
        ]
      }
    },
    $currentDate: {
      updatedAt: true
    }
  }
)
```

### Exercise 10: Remove discontinued tags

```javascript
db.products.updateMany(
  {},
  {
    $pull: {
      tags: {
        $in: [
          "temporary",
          "discontinued",
          "old-stock"
        ]
      }
    }
  }
)
```

### Exercise 11: Update an order and add history

```javascript
db.orders.updateOne(
  {
    orderNumber: "ORD-2026-1002",
    status: "Processing"
  },
  {
    $set: {
      status: "Shipped"
    },
    $push: {
      statusHistory: {
        status: "Shipped",
        changedAt: new Date()
      }
    },
    $currentDate: {
      updatedAt: true
    }
  }
)
```

The status condition prevents the command from accidentally “shipping” an order already in an incompatible state.

### Exercise 12: Correct a field name

Suppose some review documents use `reviewText` instead of `comment`.

Preview affected documents:

```javascript
db.reviews.find({
  reviewText: {
    $exists: true
  }
})
```

Rename the field:

```javascript
db.reviews.updateMany(
  {
    reviewText: {
      $exists: true
    },
    comment: {
      $exists: false
    }
  },
  {
    $rename: {
      reviewText: "comment"
    }
  }
)
```

The condition avoids overwriting documents that already have `comment`.

## 15. Challenge Query

Requirement

Find products that:

* Are active
* Belong to `Electronics` or `Books`
* Cost between `$30` and `$100`
* Have stock above zero
* Contain either the `wireless` or `mongodb` tag
* Do not contain the `discontinued` tag

Return only:

* SKU
* Name
* Category
* Price
* Stock
* Tags

Sort by category and then price.

Solution

```javascript
db.products.find(
  {
    active: true,

    category: {
      $in: [
        "Electronics",
        "Books"
      ]
    },

    price: {
      $gte: NumberDecimal("30.00"),
      $lte: NumberDecimal("100.00")
    },

    stock: {
      $gt: 0
    },

    tags: {
      $in: [
        "wireless",
        "mongodb"
      ],
      $nin: [
        "discontinued"
      ]
    }
  },
  {
    _id: 0,
    sku: 1,
    name: 1,
    category: 1,
    price: 1,
    stock: 1,
    tags: 1
  }
).sort({
  category: 1,
  price: 1
})
```

## 16. Safe Data-Manipulation Workflow

Before running a large update:

1. Construct the filter.
2. Test it with `find()`.
3. Count the matching documents.
4. Project identifiers and fields that will change.
5. Apply the update.
6. Inspect `matchedCount` and `modifiedCount`.
7. Query the updated documents again.

Example:

```javascript
const filter = {
  category: "Electronics",
  stock: {
    $lt: 50
  }
};
```

Preview:

```javascript
db.products.find(
  filter,
  {
    sku: 1,
    name: 1,
    stock: 1
  }
)
```

Count:

```javascript
db.products.countDocuments(filter)
```

Update:

```javascript
db.products.updateMany(
  filter,
  {
    $set: {
      reorderRequired: true
    },
    $currentDate: {
      updatedAt: true
    }
  }
)
```

Verify:

```javascript
db.products.find(
  {
    ...filter,
    reorderRequired: true
  },
  {
    sku: 1,
    name: 1,
    stock: 1,
    reorderRequired: 1
  }
)
```

## Module Outcome

After completing this module, learners should be able to:

* Retrieve documents using `find()` and `findOne()`.
* Count documents and retrieve distinct values.
* Control returned fields using projection.
* Filter data using comparison and logical operators.
* Query scalar fields, nested fields and arrays.
* Use `$elemMatch` for same-element array conditions.
* Update scalar and nested fields.
* Increment numeric values atomically.
* Add and remove array elements.
* Rename fields safely.
* Perform single-document and multi-document updates.
* Construct complex queries from business requirements.
* Verify data-manipulation operations before and after execution.

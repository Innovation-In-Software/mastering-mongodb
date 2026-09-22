# Module 5: The Aggregation Framework

The MongoDB Aggregation Framework processes documents through a sequence of stages called a pipeline.

Aggregation is useful when an application must:

* Filter documents
* Group related records
* Calculate totals, averages and counts
* Reshape output
* Sort and rank results
* Combine data from multiple collections
* Produce reports and dashboards

The central idea is:

> Each pipeline stage receives documents, transforms them and passes its results to the next stage.

We will continue using the `training_store` database:

```javascript
use training_store
```

Collections:

```text
training_store
├── products
├── customers
├── orders
└── reviews
```

---

## 1. Aggregation Pipeline Structure

An aggregation pipeline is an array of stage documents:

```javascript
db.collection.aggregate([
  { stage1 },
  { stage2 },
  { stage3 }
])
```

A simple example is:

```javascript
db.products.aggregate([
  {
    $match: {
      category: "Electronics"
    }
  },
  {
    $project: {
      _id: 0,
      name: 1,
      price: 1
    }
  },
  {
    $sort: {
      price: 1
    }
  }
])
```

The pipeline operates as follows:

```text
products
   │
   ▼
$match
Keep Electronics
   │
   ▼
$project
Select name and price
   │
   ▼
$sort
Order by price
   │
   ▼
Final results
```

### Stage order matters

The output from one stage becomes the input to the next stage.

These pipelines do not necessarily mean the same thing:

```javascript
[
  { $limit: 5 },
  { $sort: { price: -1 } }
]
```

This takes an initial set of five documents and sorts those five.

```javascript
[
  { $sort: { price: -1 } },
  { $limit: 5 }
]
```

This finds the five most expensive products.

---

## 2. Aggregation Versus Regular Queries

A regular query is appropriate for straightforward retrieval:

```javascript
db.products.find({
  category: "Electronics"
})
```

Aggregation is more appropriate when the result requires calculations or transformations:

```javascript
db.products.aggregate([
  {
    $match: {
      category: "Electronics"
    }
  },
  {
    $group: {
      _id: "$category",
      averagePrice: {
        $avg: "$price"
      }
    }
  }
])
```

Use aggregation for questions such as:

* How much revenue did each customer generate?
* What is the average product price by category?
* Which products have the highest average ratings?
* How many orders are in each status?
* What are the top five products by quantity sold?

---

## 3. The `$match` Stage

`$match` filters documents.

Its syntax is similar to the filter used by `find()`:

```javascript
{
  $match: {
    field: condition
  }
}
```

### Filter by exact value

```javascript
db.products.aggregate([
  {
    $match: {
      category: "Electronics"
    }
  }
])
```

### Filter using comparison operators

```javascript
db.products.aggregate([
  {
    $match: {
      price: {
        $gte: NumberDecimal("40.00"),
        $lte: NumberDecimal("100.00")
      }
    }
  }
])
```

### Combine multiple conditions

```javascript
db.products.aggregate([
  {
    $match: {
      category: "Electronics",
      active: true,
      stock: {
        $gt: 0
      }
    }
  }
])
```

### Filter by date range

```javascript
db.orders.aggregate([
  {
    $match: {
      orderedAt: {
        $gte: ISODate("2026-09-01T00:00:00Z"),
        $lt: ISODate("2026-10-01T00:00:00Z")
      }
    }
  }
])
```

### Place selective matching early

When possible, place `$match` near the start of the pipeline:

```javascript
db.orders.aggregate([
  {
    $match: {
      status: "Completed"
    }
  },
  {
    $group: {
      _id: "$customerId",
      totalSpent: {
        $sum: "$total"
      }
    }
  }
])
```

This reduces the number of documents processed by later stages. An early `$match` may also benefit from an appropriate index.

---

## 4. The `$group` Stage

`$group` combines documents using a grouping key and calculates aggregated values.

General syntax:

```javascript
{
  $group: {
    _id: <grouping-expression>,
    resultField: {
      <accumulator>: <expression>
    }
  }
}
```

The `_id` field defines the grouping key.

### Count products by category

```javascript
db.products.aggregate([
  {
    $group: {
      _id: "$category",
      productCount: {
        $sum: 1
      }
    }
  }
])
```

Possible result:

```javascript
[
  {
    _id: "Electronics",
    productCount: 2
  },
  {
    _id: "Books",
    productCount: 1
  }
]
```

`$sum: 1` adds one for every document in the group.

### Calculate average price by category

```javascript
db.products.aggregate([
  {
    $group: {
      _id: "$category",
      averagePrice: {
        $avg: "$price"
      }
    }
  }
])
```

### Calculate several metrics

```javascript
db.products.aggregate([
  {
    $group: {
      _id: "$category",

      productCount: {
        $sum: 1
      },

      averagePrice: {
        $avg: "$price"
      },

      lowestPrice: {
        $min: "$price"
      },

      highestPrice: {
        $max: "$price"
      },

      totalInventory: {
        $sum: "$stock"
      }
    }
  }
])
```

### Group all documents together

Use `_id: null` when the entire input should form one group:

```javascript
db.orders.aggregate([
  {
    $group: {
      _id: null,
      orderCount: {
        $sum: 1
      },
      totalRevenue: {
        $sum: "$total"
      },
      averageOrderValue: {
        $avg: "$total"
      }
    }
  }
])
```

### Group by multiple fields

```javascript
db.orders.aggregate([
  {
    $group: {
      _id: {
        status: "$status",
        customerId: "$customerId"
      },
      orderCount: {
        $sum: 1
      },
      totalValue: {
        $sum: "$total"
      }
    }
  }
])
```

Each unique combination of `status` and `customerId` creates a separate group.

---

## 5. Common Accumulator Operators

Accumulator operators calculate values across documents in a group.

| Operator    | Purpose                               |
| ----------- | -------------------------------------- |
| `$sum`      | Calculates a total or count           |
| `$avg`      | Calculates an average                 |
| `$min`      | Returns the lowest value              |
| `$max`      | Returns the highest value             |
| `$first`    | Returns the first value in a group    |
| `$last`     | Returns the last value in a group     |
| `$push`     | Collects values, including duplicates |
| `$addToSet` | Collects unique values                |

### Collect product names by category

```javascript
db.products.aggregate([
  {
    $group: {
      _id: "$category",
      products: {
        $push: "$name"
      }
    }
  }
])
```

### Collect unique customer IDs by order status

```javascript
db.orders.aggregate([
  {
    $group: {
      _id: "$status",
      customers: {
        $addToSet: "$customerId"
      }
    }
  }
])
```

### Use `$first` after sorting

To find the most expensive product in each category:

```javascript
db.products.aggregate([
  {
    $sort: {
      category: 1,
      price: -1
    }
  },
  {
    $group: {
      _id: "$category",
      mostExpensiveProduct: {
        $first: "$name"
      },
      highestPrice: {
        $first: "$price"
      }
    }
  }
])
```

The preceding `$sort` determines which document is considered first.

---

## 6. The `$project` Stage

`$project` controls the output shape.

It can:

* Include fields
* Exclude fields
* Rename fields
* Create calculated fields
* Restructure documents
* Apply expressions

### Select fields

```javascript
db.products.aggregate([
  {
    $project: {
      _id: 0,
      sku: 1,
      name: 1,
      price: 1
    }
  }
])
```

### Rename a field in the result

```javascript
db.products.aggregate([
  {
    $project: {
      _id: 0,
      productName: "$name",
      unitPrice: "$price"
    }
  }
])
```

This changes only the pipeline result. It does not rename fields in stored documents.

### Calculate a field

Calculate inventory value:

```javascript
db.products.aggregate([
  {
    $project: {
      _id: 0,
      name: 1,
      price: 1,
      stock: 1,
      inventoryValue: {
        $multiply: [
          "$price",
          "$stock"
        ]
      }
    }
  }
])
```

### Build a full name

```javascript
db.customers.aggregate([
  {
    $project: {
      _id: 0,
      email: 1,
      fullName: {
        $concat: [
          "$firstName",
          " ",
          "$lastName"
        ]
      }
    }
  }
])
```

### Round a calculated value

```javascript
db.products.aggregate([
  {
    $group: {
      _id: "$category",
      averagePrice: {
        $avg: "$price"
      }
    }
  },
  {
    $project: {
      _id: 0,
      category: "$_id",
      averagePrice: {
        $round: [
          "$averagePrice",
          2
        ]
      }
    }
  }
])
```

### Create a conditional field

```javascript
db.products.aggregate([
  {
    $project: {
      _id: 0,
      name: 1,
      stock: 1,
      stockStatus: {
        $cond: {
          if: {
            $eq: ["$stock", 0]
          },
          then: "Out of stock",
          else: {
            $cond: {
              if: {
                $lt: ["$stock", 50]
              },
              then: "Low stock",
              else: "Available"
            }
          }
        }
      }
    }
  }
])
```

---

## 7. The `$sort` Stage

`$sort` orders pipeline results.

```javascript
{
  $sort: {
    field: 1
  }
}
```

* `1` means ascending.
* `-1` means descending.

### Sort products by price

```javascript
db.products.aggregate([
  {
    $sort: {
      price: -1
    }
  }
])
```

### Sort using multiple fields

```javascript
db.products.aggregate([
  {
    $sort: {
      category: 1,
      price: -1,
      name: 1
    }
  }
])
```

MongoDB sorts by:

1. Category in ascending order
2. Price in descending order within each category
3. Name in ascending order when prices are equal

For predictable results, include a unique tie-breaker when appropriate:

```javascript
{
  $sort: {
    price: -1,
    _id: 1
  }
}
```

---

## 8. The `$limit` Stage

`$limit` restricts the number of documents passed to the next stage.

```javascript
db.products.aggregate([
  {
    $sort: {
      price: -1
    }
  },
  {
    $limit: 3
  }
])
```

This returns the three most expensive products.

### `$skip` with `$limit`

For simple pagination:

```javascript
db.products.aggregate([
  {
    $sort: {
      name: 1,
      _id: 1
    }
  },
  {
    $skip: 10
  },
  {
    $limit: 10
  }
])
```

Large skip values can become inefficient. Range-based pagination is often preferable for large production datasets.

---

## 9. Building a Multi-Stage Analytical Pipeline

### Business requirement

Management wants a category-level inventory report showing:

* Active products only
* Number of products
* Average product price
* Lowest price
* Highest price
* Total units in stock
* Total inventory value
* Categories ordered by inventory value
* Only the top five categories

### Pipeline

```javascript
db.products.aggregate([
  {
    $match: {
      active: true
    }
  },
  {
    $group: {
      _id: "$category",

      productCount: {
        $sum: 1
      },

      averagePrice: {
        $avg: "$price"
      },

      lowestPrice: {
        $min: "$price"
      },

      highestPrice: {
        $max: "$price"
      },

      totalUnits: {
        $sum: "$stock"
      },

      totalInventoryValue: {
        $sum: {
          $multiply: [
            "$price",
            "$stock"
          ]
        }
      }
    }
  },
  {
    $project: {
      _id: 0,
      category: "$_id",
      productCount: 1,
      averagePrice: {
        $round: [
          "$averagePrice",
          2
        ]
      },
      lowestPrice: 1,
      highestPrice: 1,
      totalUnits: 1,
      totalInventoryValue: 1
    }
  },
  {
    $sort: {
      totalInventoryValue: -1
    }
  },
  {
    $limit: 5
  }
])
```

### Stage-by-stage explanation

#### Stage 1: `$match`

```javascript
{
  $match: {
    active: true
  }
}
```

Removes inactive products.

#### Stage 2: `$group`

```javascript
{
  $group: {
    _id: "$category",
    ...
  }
}
```

Creates one group for each category and calculates its metrics.

#### Stage 3: `$project`

```javascript
{
  $project: {
    category: "$_id",
    ...
  }
}
```

Reshapes the report and gives the grouping key a business-friendly name.

#### Stage 4: `$sort`

```javascript
{
  $sort: {
    totalInventoryValue: -1
  }
}
```

Ranks categories from highest to lowest inventory value.

#### Stage 5: `$limit`

```javascript
{
  $limit: 5
}
```

Returns the five highest-ranking categories.

---

## 10. Analyzing Order Status

### Requirement

Show the number and value of orders in each status.

```javascript
db.orders.aggregate([
  {
    $group: {
      _id: "$status",
      orderCount: {
        $sum: 1
      },
      totalValue: {
        $sum: "$total"
      },
      averageOrderValue: {
        $avg: "$total"
      }
    }
  },
  {
    $project: {
      _id: 0,
      status: "$_id",
      orderCount: 1,
      totalValue: 1,
      averageOrderValue: {
        $round: [
          "$averageOrderValue",
          2
        ]
      }
    }
  },
  {
    $sort: {
      totalValue: -1
    }
  }
])
```

---

## 11. Monthly Sales Analysis

Dates can be grouped by month using `$dateTrunc`.

```javascript
db.orders.aggregate([
  {
    $match: {
      status: {
        $in: [
          "Shipped",
          "Delivered",
          "Completed"
        ]
      }
    }
  },
  {
    $group: {
      _id: {
        $dateTrunc: {
          date: "$orderedAt",
          unit: "month",
          timezone: "America/Toronto"
        }
      },
      orderCount: {
        $sum: 1
      },
      revenue: {
        $sum: "$total"
      }
    }
  },
  {
    $project: {
      _id: 0,
      month: "$_id",
      orderCount: 1,
      revenue: 1
    }
  },
  {
    $sort: {
      month: 1
    }
  }
])
```

The selected timezone affects how timestamps near month boundaries are classified.

---

## 12. Working with Order-Item Arrays

Each order contains an `items` array:

```javascript
{
  orderNumber: "ORD-2026-1002",
  items: [
    {
      sku: "ELEC-1002",
      productName: "Mechanical Keyboard",
      quantity: 1,
      lineTotal: NumberDecimal("89.99")
    },
    {
      sku: "BOOK-2001",
      productName: "MongoDB Fundamentals",
      quantity: 1,
      lineTotal: NumberDecimal("49.99")
    }
  ]
}
```

To analyze individual products, the array must first be expanded.

### `$unwind`

```javascript
db.orders.aggregate([
  {
    $unwind: "$items"
  }
])
```

One order containing two items becomes two pipeline documents.

The original stored order is not changed.

---

## 13. Top-Selling Products

### Requirement

Find the top five products by units sold.

```javascript
db.orders.aggregate([
  {
    $match: {
      status: {
        $in: [
          "Shipped",
          "Delivered",
          "Completed"
        ]
      }
    }
  },
  {
    $unwind: "$items"
  },
  {
    $group: {
      _id: {
        productId: "$items.productId",
        sku: "$items.sku",
        productName: "$items.productName"
      },
      unitsSold: {
        $sum: "$items.quantity"
      },
      salesValue: {
        $sum: "$items.lineTotal"
      }
    }
  },
  {
    $project: {
      _id: 0,
      productId: "$_id.productId",
      sku: "$_id.sku",
      productName: "$_id.productName",
      unitsSold: 1,
      salesValue: 1
    }
  },
  {
    $sort: {
      unitsSold: -1,
      salesValue: -1
    }
  },
  {
    $limit: 5
  }
])
```

The data flow is:

```text
Orders
  │
  ▼
Keep completed sales
  │
  ▼
Expand order items
  │
  ▼
Group by product
  │
  ▼
Calculate units and sales
  │
  ▼
Rank and return top five
```

---

## 14. Product Rating Analysis

### Requirement

Show products with:

* At least one review
* Average rating
* Total review count
* Highest and lowest rating
* Highest-rated products first

```javascript
db.reviews.aggregate([
  {
    $group: {
      _id: "$productId",
      reviewCount: {
        $sum: 1
      },
      averageRating: {
        $avg: "$rating"
      },
      highestRating: {
        $max: "$rating"
      },
      lowestRating: {
        $min: "$rating"
      }
    }
  },
  {
    $project: {
      _id: 0,
      productId: "$_id",
      reviewCount: 1,
      averageRating: {
        $round: [
          "$averageRating",
          2
        ]
      },
      highestRating: 1,
      lowestRating: 1
    }
  },
  {
    $sort: {
      averageRating: -1,
      reviewCount: -1
    }
  }
])
```

This report contains product IDs but not product names. To obtain names from the `products` collection, use `$lookup`.

---

## 15. Joining Collections with `$lookup`

`$lookup` performs a left outer join between collections.

### Add product information to the review report

```javascript
db.reviews.aggregate([
  {
    $group: {
      _id: "$productId",
      reviewCount: {
        $sum: 1
      },
      averageRating: {
        $avg: "$rating"
      }
    }
  },
  {
    $lookup: {
      from: "products",
      localField: "_id",
      foreignField: "_id",
      as: "product"
    }
  },
  {
    $unwind: "$product"
  },
  {
    $project: {
      _id: 0,
      productId: "$_id",
      productName: "$product.name",
      category: "$product.category",
      reviewCount: 1,
      averageRating: {
        $round: [
          "$averageRating",
          2
        ]
      }
    }
  },
  {
    $sort: {
      averageRating: -1,
      reviewCount: -1
    }
  }
])
```

### `$lookup` output

Before `$unwind`:

```javascript
{
  _id: ObjectId("..."),
  reviewCount: 3,
  product: [
    {
      _id: ObjectId("..."),
      name: "Wireless Mouse"
    }
  ]
}
```

After `$unwind`:

```javascript
{
  _id: ObjectId("..."),
  reviewCount: 3,
  product: {
    _id: ObjectId("..."),
    name: "Wireless Mouse"
  }
}
```

Because `$lookup` produces an array, `$unwind` is commonly used when exactly one matching document is expected.

---

## 16. Customer Spending Report

### Requirement

Find the highest-spending customers and include their names and email addresses.

```javascript
db.orders.aggregate([
  {
    $match: {
      status: {
        $in: [
          "Shipped",
          "Delivered",
          "Completed"
        ]
      }
    }
  },
  {
    $group: {
      _id: "$customerId",
      orderCount: {
        $sum: 1
      },
      totalSpent: {
        $sum: "$total"
      },
      averageOrderValue: {
        $avg: "$total"
      },
      lastOrderAt: {
        $max: "$orderedAt"
      }
    }
  },
  {
    $lookup: {
      from: "customers",
      localField: "_id",
      foreignField: "_id",
      as: "customer"
    }
  },
  {
    $unwind: "$customer"
  },
  {
    $project: {
      _id: 0,
      customerId: "$_id",
      customerName: {
        $concat: [
          "$customer.firstName",
          " ",
          "$customer.lastName"
        ]
      },
      email: "$customer.email",
      orderCount: 1,
      totalSpent: 1,
      averageOrderValue: {
        $round: [
          "$averageOrderValue",
          2
        ]
      },
      lastOrderAt: 1
    }
  },
  {
    $sort: {
      totalSpent: -1
    }
  },
  {
    $limit: 10
  }
])
```

---

## 17. Using `$count`

`$count` counts the documents reaching that stage.

```javascript
db.products.aggregate([
  {
    $match: {
      active: true,
      stock: {
        $gt: 0
      }
    }
  },
  {
    $count: "availableProductCount"
  }
])
```

Possible result:

```javascript
{
  availableProductCount: 3
}
```

Unlike `countDocuments()`, `$count` operates on the intermediate results of the pipeline.

---

## 18. Multiple Reports with `$facet`

`$facet` runs multiple sub-pipelines against the same input.

### Product dashboard

```javascript
db.products.aggregate([
  {
    $match: {
      active: true
    }
  },
  {
    $facet: {
      categorySummary: [
        {
          $group: {
            _id: "$category",
            productCount: {
              $sum: 1
            },
            averagePrice: {
              $avg: "$price"
            }
          }
        },
        {
          $sort: {
            productCount: -1
          }
        }
      ],

      lowStockProducts: [
        {
          $match: {
            stock: {
              $lt: 50
            }
          }
        },
        {
          $project: {
            _id: 0,
            sku: 1,
            name: 1,
            stock: 1
          }
        },
        {
          $sort: {
            stock: 1
          }
        }
      ],

      mostExpensiveProducts: [
        {
          $sort: {
            price: -1
          }
        },
        {
          $limit: 5
        },
        {
          $project: {
            _id: 0,
            name: 1,
            price: 1
          }
        }
      ]
    }
  }
])
```

The result contains three report sections in one document.

---

## 19. Writing Aggregation Results with `$merge`

Aggregation normally returns results without changing the source collection.

`$merge` can store or update materialized reporting results.

```javascript
db.orders.aggregate([
  {
    $match: {
      status: {
        $in: [
          "Shipped",
          "Delivered",
          "Completed"
        ]
      }
    }
  },
  {
    $group: {
      _id: "$customerId",
      orderCount: {
        $sum: 1
      },
      totalSpent: {
        $sum: "$total"
      },
      calculatedAt: {
        $max: "$orderedAt"
      }
    }
  },
  {
    $merge: {
      into: "customer_sales_summary",
      on: "_id",
      whenMatched: "replace",
      whenNotMatched: "insert"
    }
  }
])
```

This creates or refreshes documents in `customer_sales_summary`.

Because `$merge` writes data, it should be tested carefully before being used in a production database.

---

## 20. Pipeline Development Strategy

Complex pipelines should be built incrementally.

### Step 1: Start with matching

```javascript
db.orders.aggregate([
  {
    $match: {
      status: "Shipped"
    }
  }
])
```

### Step 2: Add array expansion

```javascript
db.orders.aggregate([
  {
    $match: {
      status: "Shipped"
    }
  },
  {
    $unwind: "$items"
  }
])
```

### Step 3: Add grouping

```javascript
db.orders.aggregate([
  {
    $match: {
      status: "Shipped"
    }
  },
  {
    $unwind: "$items"
  },
  {
    $group: {
      _id: "$items.sku",
      unitsSold: {
        $sum: "$items.quantity"
      }
    }
  }
])
```

### Step 4: Shape the result

```javascript
{
  $project: {
    _id: 0,
    sku: "$_id",
    unitsSold: 1
  }
}
```

### Step 5: Sort and limit

```javascript
{
  $sort: {
    unitsSold: -1
  }
},
{
  $limit: 5
}
```

Verify each new stage before adding the next one. This makes incorrect filters, field paths and group expressions easier to locate.

---

## 21. Aggregation Performance Practices

### Filter early

Use `$match` as early as logically possible to reduce input volume.

### Project only when useful

Removing unnecessary large fields early can reduce intermediate document size. However, MongoDB may already optimize straightforward field dependencies, so avoid adding stages that do not improve clarity or behavior.

### Sort after filtering

This:

```javascript
[
  {
    $match: {
      category: "Electronics"
    }
  },
  {
    $sort: {
      price: -1
    }
  }
]
```

is generally preferable to sorting the complete collection before filtering it.

### Index important early stages

A pipeline beginning with:

```javascript
{
  $match: {
    status: "Completed",
    orderedAt: {
      $gte: ISODate("2026-09-01T00:00:00Z")
    }
  }
}
```

may benefit from:

```javascript
db.orders.createIndex({
  status: 1,
  orderedAt: 1
})
```

### Control `$unwind` expansion

One document with 100 array elements produces 100 intermediate documents after `$unwind`.

Filter before `$unwind` when possible:

```javascript
[
  {
    $match: {
      status: "Completed"
    }
  },
  {
    $unwind: "$items"
  }
]
```

### Use `explain()`

Inspect execution behavior:

```javascript
db.orders.explain("executionStats").aggregate([
  {
    $match: {
      status: "Completed"
    }
  },
  {
    $group: {
      _id: "$customerId",
      totalSpent: {
        $sum: "$total"
      }
    }
  }
])
```

Look for:

* Whether an index was used
* Documents examined
* Documents returned
* Expensive sorts
* Large intermediate results

---

## 22. Hands-On Analytical Challenge

### Business requirement

Create a report of the top-selling product categories for completed sales.

The report must:

* Include only shipped, delivered or completed orders.
* Expand individual order items.
* Join order items to current products.
* Group results by product category.
* Calculate total units sold.
* Calculate total sales.
* Count distinct customers.
* Calculate sales per customer.
* Show only categories with sales of at least `$50`.
* Sort from highest to lowest sales.
* Return the top five categories.

### Solution

```javascript
db.orders.aggregate([
  {
    $match: {
      status: {
        $in: [
          "Shipped",
          "Delivered",
          "Completed"
        ]
      }
    }
  },
  {
    $unwind: "$items"
  },
  {
    $lookup: {
      from: "products",
      localField: "items.productId",
      foreignField: "_id",
      as: "product"
    }
  },
  {
    $unwind: "$product"
  },
  {
    $group: {
      _id: "$product.category",

      totalUnitsSold: {
        $sum: "$items.quantity"
      },

      totalSales: {
        $sum: "$items.lineTotal"
      },

      customers: {
        $addToSet: "$customerId"
      }
    }
  },
  {
    $project: {
      _id: 0,
      category: "$_id",
      totalUnitsSold: 1,
      totalSales: 1,

      uniqueCustomerCount: {
        $size: "$customers"
      },

      salesPerCustomer: {
        $cond: [
          {
            $gt: [
              {
                $size: "$customers"
              },
              0
            ]
          },
          {
            $divide: [
              "$totalSales",
              {
                $size: "$customers"
              }
            ]
          },
          0
        ]
      }
    }
  },
  {
    $match: {
      totalSales: {
        $gte: NumberDecimal("50.00")
      }
    }
  },
  {
    $sort: {
      totalSales: -1
    }
  },
  {
    $limit: 5
  }
])
```

### Why are there two `$match` stages?

The first `$match` filters stored order documents:

```javascript
{
  status: {
    $in: ["Shipped", "Delivered", "Completed"]
  }
}
```

The second `$match` filters calculated group results:

```javascript
{
  totalSales: {
    $gte: NumberDecimal("50.00")
  }
}
```

`totalSales` does not exist in the original order documents. It is created by `$group`, so it can only be filtered afterward.

---

# Module Outcome

After completing this module, learners should be able to:

* Explain how documents flow through an aggregation pipeline.
* Filter pipeline input with `$match`.
* Group documents and calculate metrics with `$group`.
* Reshape and calculate output fields with `$project`.
* Rank results using `$sort` and `$limit`.
* Expand arrays using `$unwind`.
* Combine collections using `$lookup`.
* Build category, customer, inventory and sales reports.
* Construct complex pipelines incrementally.
* Explain why pipeline-stage order affects results and performance.
* Apply basic aggregation performance practices.

// Load training_store for Mastering MongoDB.
// Module 1 Lab 1.3 can inspect this dataset; Module 3 labs build a smaller core by hand.
// Day 2 Modules 4–5 and Day 3 Module 6 use the full analytical set loaded here.
// Module 6 labs recreate indexes after this script drops collections.
// Usage: mongosh "mongodb://localhost:27017" datasets/training_store/load.js

const dbName = "training_store";
db = db.getSiblingDB(dbName);

db.customers.drop();
db.products.drop();
db.orders.drop();
db.reviews.drop();

function D(value) {
  return Decimal128(String(value));
}

function snap(product, quantity) {
  return {
    productId: product._id,
    sku: product.sku,
    name: product.name,
    quantity: quantity,
    unitPrice: product.price
  };
}

db.customers.insertMany([
  {
    customerNumber: "C101",
    name: { first: "Aisha", last: "Khan" },
    contact: { email: "aisha@example.com", phone: "+1-555-0100" },
    addresses: [
      {
        type: "SHIPPING",
        street: "100 King Street",
        city: "Toronto",
        province: "Ontario",
        postalCode: "M5X 1A9",
        country: "Canada"
      }
    ],
    preferences: { newsletter: true, language: "English" },
    status: "ACTIVE",
    createdAt: new Date("2026-09-01T10:00:00Z")
  },
  {
    customerNumber: "C204",
    name: { first: "Luis", last: "Romero" },
    contact: { email: "luis@example.com", phone: null },
    addresses: [
      {
        type: "SHIPPING",
        street: "400 Congress Avenue",
        city: "Austin",
        province: "Texas",
        postalCode: "78701",
        country: "USA"
      }
    ],
    preferences: { newsletter: false, language: "English" },
    status: "ACTIVE",
    createdAt: new Date("2026-09-05T15:00:00Z")
  },
  {
    customerNumber: "C310",
    name: { first: "Priya", last: "Patel" },
    contact: { email: "priya@example.com", phone: "+1-555-0160" },
    addresses: [
      {
        type: "SHIPPING",
        street: "800 West Georgia Street",
        city: "Vancouver",
        province: "British Columbia",
        postalCode: "V6C 2V5",
        country: "Canada"
      }
    ],
    preferences: { newsletter: true, language: "English" },
    status: "ACTIVE",
    createdAt: new Date("2026-07-12T09:00:00Z")
  },
  {
    customerNumber: "C412",
    name: { first: "Jordan", last: "Lee" },
    contact: { email: "jordan@example.com", phone: "+1-555-0175" },
    addresses: [
      {
        type: "SHIPPING",
        street: "1250 René-Lévesque Boulevard",
        city: "Montreal",
        province: "Quebec",
        postalCode: "H3B 4W8",
        country: "Canada"
      }
    ],
    preferences: { newsletter: false, language: "French" },
    status: "ACTIVE",
    createdAt: new Date("2026-07-20T11:30:00Z")
  },
  {
    customerNumber: "C515",
    name: { first: "Sam", last: "Okonkwo" },
    contact: { email: "sam@example.com" },
    addresses: [
      {
        type: "BILLING",
        street: "50 Rideau Street",
        city: "Ottawa",
        province: "Ontario",
        postalCode: "K1N 9J7",
        country: "Canada"
      }
    ],
    preferences: { newsletter: false, language: "English" },
    status: "INACTIVE",
    createdAt: new Date("2026-06-02T08:00:00Z")
  },
  {
    customerNumber: "C620",
    name: { first: "Maya", last: "Chen" },
    contact: { email: "maya@example.com", phone: "+1-555-0192" },
    addresses: [
      {
        type: "SHIPPING",
        street: "1 Market Street",
        city: "San Francisco",
        province: "California",
        postalCode: "94105",
        country: "USA"
      }
    ],
    preferences: { newsletter: true, language: "English" },
    status: "ACTIVE",
    createdAt: new Date("2026-08-01T16:00:00Z")
  }
]);

db.products.insertMany([
  {
    sku: "L100",
    name: "Business Laptop",
    category: "LAPTOP",
    price: D("1299.99"),
    attributes: {
      processor: "Intel Core i7",
      memoryGB: 16,
      storageGB: 512,
      screenSizeInches: 14
    },
    tags: ["business", "portable"],
    active: true,
    createdAt: new Date("2026-08-20T09:00:00Z")
  },
  {
    sku: "L110",
    name: "Ultrabook",
    category: "LAPTOP",
    price: D("1899.99"),
    attributes: {
      processor: "Intel Core i7",
      memoryGB: 32,
      storageGB: 1024,
      screenSizeInches: 14
    },
    tags: ["business", "premium"],
    active: true,
    createdAt: new Date("2026-08-20T09:15:00Z")
  },
  {
    sku: "L190",
    name: "Refurbished Laptop",
    category: "LAPTOP",
    price: D("499.99"),
    attributes: {
      processor: "Intel Core i5",
      memoryGB: 8,
      storageGB: 256,
      screenSizeInches: 13
    },
    tags: ["clearance", "refurbished", "discontinued"],
    legacyName: "Refurb Unit",
    active: false,
    createdAt: new Date("2026-07-01T09:00:00Z")
  },
  {
    sku: "S200",
    name: "Running Shoe",
    category: "SHOE",
    price: D("129.99"),
    attributes: {
      sizes: [7, 8, 9, 10],
      color: "Blue",
      material: "Mesh"
    },
    tags: ["running", "sports"],
    active: true,
    createdAt: new Date("2026-08-21T09:00:00Z")
  },
  {
    sku: "S210",
    name: "Trail Shoe",
    category: "SHOE",
    price: D("89.99"),
    attributes: {
      sizes: [8, 9, 10, 11],
      color: "Grey",
      material: "Synthetic"
    },
    tags: ["trail", "sports"],
    active: true,
    createdAt: new Date("2026-08-21T09:20:00Z")
  },
  {
    sku: "S290",
    name: "Clearance Shoe",
    category: "SHOE",
    price: D("44.99"),
    attributes: {
      sizes: [7, 8, 9],
      color: "Black",
      material: "Mesh"
    },
    tags: ["clearance", "sports"],
    active: true,
    createdAt: new Date("2026-07-15T09:00:00Z")
  },
  {
    sku: "B300",
    name: "MongoDB Fundamentals",
    category: "BOOK",
    price: D("59.99"),
    attributes: {
      author: "A. Trainer",
      isbn: "978-0000000000",
      language: "English"
    },
    tags: ["database", "technology"],
    active: true,
    createdAt: new Date("2026-08-22T09:00:00Z")
  },
  {
    sku: "B310",
    name: "Query Cookbook",
    category: "BOOK",
    price: D("39.99"),
    attributes: {
      author: "A. Trainer",
      isbn: "978-0000000001",
      language: "English"
    },
    tags: ["database", "reference"],
    discountPrice: D("29.99"),
    active: true,
    createdAt: new Date("2026-08-22T09:20:00Z")
  },
  {
    sku: "P1001",
    name: "Wireless Keyboard",
    category: "ACCESSORY",
    price: D("49.99"),
    attributes: {
      connection: "Bluetooth",
      batteryLifeMonths: 12
    },
    tags: ["wireless", "accessories"],
    discountPrice: D("39.99"),
    active: true,
    createdAt: new Date("2026-08-23T09:00:00Z")
  },
  {
    sku: "A400",
    name: "USB Hub",
    category: "ACCESSORY",
    price: D("24.99"),
    attributes: {
      ports: 4,
      connection: "USB-C"
    },
    tags: ["office", "accessories"],
    active: true,
    createdAt: new Date("2026-08-23T09:15:00Z")
  },
  {
    sku: "A410",
    name: "Wireless Mouse",
    category: "ACCESSORY",
    price: D("19.99"),
    attributes: {
      connection: "Bluetooth",
      dpi: 1600
    },
    tags: ["wireless", "accessories"],
    temporaryNote: "Display model — remove after review",
    active: true,
    createdAt: new Date("2026-08-23T09:30:00Z")
  },
  {
    sku: "A500",
    name: "Docking Station",
    category: "ACCESSORY",
    price: D("249.99"),
    attributes: {
      ports: 8,
      connection: "USB-C"
    },
    tags: ["office", "premium"],
    active: true,
    createdAt: new Date("2026-08-24T09:00:00Z")
  },
  {
    sku: "XBAD",
    name: "Legacy Cable Pack",
    category: "ACCESSORY",
    price: "49.99",
    tags: ["legacy"],
    active: true,
    createdAt: new Date("2025-08-01T10:00:00Z")
  }
]);

const C101 = db.customers.findOne({ customerNumber: "C101" });
const C204 = db.customers.findOne({ customerNumber: "C204" });
const C310 = db.customers.findOne({ customerNumber: "C310" });
const C412 = db.customers.findOne({ customerNumber: "C412" });
const C515 = db.customers.findOne({ customerNumber: "C515" });
const C620 = db.customers.findOne({ customerNumber: "C620" });

const L100 = db.products.findOne({ sku: "L100" });
const L110 = db.products.findOne({ sku: "L110" });
const S200 = db.products.findOne({ sku: "S200" });
const S210 = db.products.findOne({ sku: "S210" });
const S290 = db.products.findOne({ sku: "S290" });
const B300 = db.products.findOne({ sku: "B300" });
const B310 = db.products.findOne({ sku: "B310" });
const P1001 = db.products.findOne({ sku: "P1001" });
const A400 = db.products.findOne({ sku: "A400" });
const A410 = db.products.findOne({ sku: "A410" });
const A500 = db.products.findOne({ sku: "A500" });

db.orders.insertMany([
  {
    orderNumber: "O5001",
    customerId: C101._id,
    items: [snap(L100, 1), snap(A410, 2)],
    shippingAddress: {
      street: "100 King Street",
      city: "Toronto",
      province: "Ontario",
      postalCode: "M5X 1A9",
      country: "Canada"
    },
    paymentStatus: "PENDING",
    fulfillmentStatus: "NEW",
    subtotal: D("1339.97"),
    tax: D("174.20"),
    total: D("1514.17"),
    internalNotes: "Awaiting payment confirmation. Module 4 $elemMatch trap: L100 qty 1 and A410 qty 2.",
    createdAt: new Date("2026-09-20T14:30:00Z")
  },
  {
    orderNumber: "O6101",
    customerId: C101._id,
    items: [snap(L100, 1)],
    shippingAddress: {
      street: "100 King Street",
      city: "Toronto",
      province: "Ontario",
      postalCode: "M5X 1A9",
      country: "Canada"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "SHIPPED",
    subtotal: D("1299.99"),
    tax: D("169.00"),
    shippingFee: D("15.00"),
    total: D("1483.99"),
    createdAt: new Date("2026-07-08T14:00:00Z")
  },
  {
    orderNumber: "O6102",
    customerId: C204._id,
    items: [snap(S200, 1), snap(P1001, 1)],
    shippingAddress: {
      street: "400 Congress Avenue",
      city: "Austin",
      province: "Texas",
      postalCode: "78701",
      country: "USA"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "DELIVERED",
    subtotal: D("179.98"),
    tax: D("23.40"),
    shippingFee: D("8.00"),
    total: D("211.38"),
    createdAt: new Date("2026-07-15T16:20:00Z")
  },
  {
    orderNumber: "O6103",
    customerId: C310._id,
    items: [snap(B300, 2)],
    shippingAddress: {
      street: "800 West Georgia Street",
      city: "Vancouver",
      province: "British Columbia",
      postalCode: "V6C 2V5",
      country: "Canada"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "SHIPPED",
    subtotal: D("119.98"),
    tax: D("15.60"),
    shippingFee: D("5.00"),
    total: D("140.58"),
    createdAt: new Date("2026-07-22T11:10:00Z")
  },
  {
    orderNumber: "O6201",
    customerId: C101._id,
    items: [snap(A400, 2), snap(A410, 1)],
    shippingAddress: {
      street: "100 King Street",
      city: "Toronto",
      province: "Ontario",
      postalCode: "M5X 1A9",
      country: "Canada"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "DELIVERED",
    subtotal: D("69.97"),
    tax: D("9.10"),
    total: D("79.07"),
    createdAt: new Date("2026-08-04T09:40:00Z")
  },
  {
    orderNumber: "O6202",
    customerId: C412._id,
    items: [snap(L110, 1)],
    shippingAddress: {
      street: "1250 René-Lévesque Boulevard",
      city: "Montreal",
      province: "Quebec",
      postalCode: "H3B 4W8",
      country: "Canada"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "PROCESSING",
    subtotal: D("1899.99"),
    tax: D("247.00"),
    total: D("2146.99"),
    createdAt: new Date("2026-08-11T13:05:00Z")
  },
  {
    orderNumber: "O6203",
    customerId: C204._id,
    items: [snap(S210, 1), snap(B310, 1)],
    shippingAddress: {
      street: "400 Congress Avenue",
      city: "Austin",
      province: "Texas",
      postalCode: "78701",
      country: "USA"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "SHIPPED",
    subtotal: D("129.98"),
    tax: D("16.90"),
    shippingFee: D("8.00"),
    total: D("154.88"),
    createdAt: new Date("2026-08-18T15:45:00Z")
  },
  {
    orderNumber: "O6204",
    customerId: C620._id,
    items: [snap(A500, 1), snap(P1001, 1)],
    shippingAddress: {
      street: "1 Market Street",
      city: "San Francisco",
      province: "California",
      postalCode: "94105",
      country: "USA"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "DELIVERED",
    subtotal: D("299.98"),
    tax: D("39.00"),
    shippingFee: D("12.00"),
    total: D("350.98"),
    createdAt: new Date("2026-08-25T18:00:00Z")
  },
  {
    orderNumber: "O6301",
    customerId: C101._id,
    items: [snap(L100, 1), snap(A400, 1)],
    shippingAddress: {
      street: "100 King Street",
      city: "Toronto",
      province: "Ontario",
      postalCode: "M5X 1A9",
      country: "Canada"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "SHIPPED",
    subtotal: D("1324.98"),
    tax: D("172.25"),
    shippingFee: D("15.00"),
    total: D("1512.23"),
    createdAt: new Date("2026-09-03T10:15:00Z")
  },
  {
    orderNumber: "O6302",
    customerId: C204._id,
    items: [snap(S200, 2)],
    shippingAddress: {
      street: "400 Congress Avenue",
      city: "Austin",
      province: "Texas",
      postalCode: "78701",
      country: "USA"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "PROCESSING",
    subtotal: D("259.98"),
    tax: D("33.80"),
    shippingFee: D("8.00"),
    total: D("301.78"),
    createdAt: new Date("2026-09-07T12:00:00Z")
  },
  {
    orderNumber: "O6303",
    customerId: C412._id,
    items: [snap(B300, 1), snap(B310, 1), snap(P1001, 1)],
    shippingAddress: {
      street: "1250 René-Lévesque Boulevard",
      city: "Montreal",
      province: "Quebec",
      postalCode: "H3B 4W8",
      country: "Canada"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "SHIPPED",
    subtotal: D("149.97"),
    tax: D("19.50"),
    shippingFee: D("5.00"),
    total: D("174.47"),
    createdAt: new Date("2026-09-10T09:30:00Z")
  },
  {
    orderNumber: "O6304",
    customerId: C620._id,
    items: [snap(L110, 1)],
    shippingAddress: {
      street: "1 Market Street",
      city: "San Francisco",
      province: "California",
      postalCode: "94105",
      country: "USA"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "DELIVERED",
    subtotal: D("1899.99"),
    tax: D("247.00"),
    total: D("2146.99"),
    createdAt: new Date("2026-09-12T17:20:00Z")
  },
  {
    orderNumber: "O6305",
    customerId: C310._id,
    items: [snap(A410, 3)],
    shippingAddress: {
      street: "800 West Georgia Street",
      city: "Vancouver",
      province: "British Columbia",
      postalCode: "V6C 2V5",
      country: "Canada"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "NEW",
    subtotal: D("59.97"),
    tax: D("7.80"),
    shippingFee: D("4.00"),
    total: D("71.77"),
    createdAt: new Date("2026-09-14T08:50:00Z")
  },
  {
    orderNumber: "O6306",
    customerId: C101._id,
    items: [snap(S290, 1), snap(A500, 1)],
    shippingAddress: {
      street: "100 King Street",
      city: "Toronto",
      province: "Ontario",
      postalCode: "M5X 1A9",
      country: "Canada"
    },
    paymentStatus: "PAID",
    fulfillmentStatus: "SHIPPED",
    subtotal: D("294.98"),
    tax: D("38.35"),
    shippingFee: D("10.00"),
    total: D("343.33"),
    createdAt: new Date("2026-09-16T14:10:00Z")
  },
  {
    orderNumber: "O6401",
    customerId: C204._id,
    items: [snap(L100, 2)],
    shippingAddress: {
      street: "400 Congress Avenue",
      city: "Austin",
      province: "Texas",
      postalCode: "78701",
      country: "USA"
    },
    paymentStatus: "PENDING",
    fulfillmentStatus: "PROCESSING",
    subtotal: D("2599.98"),
    tax: D("338.00"),
    shippingFee: D("8.00"),
    total: D("2945.98"),
    createdAt: new Date("2026-09-18T11:00:00Z")
  },
  {
    orderNumber: "O6402",
    customerId: C515._id,
    items: [snap(B310, 1)],
    shippingAddress: {
      street: "50 Rideau Street",
      city: "Ottawa",
      province: "Ontario",
      postalCode: "K1N 9J7",
      country: "Canada"
    },
    paymentStatus: "FAILED",
    fulfillmentStatus: "NEW",
    subtotal: D("39.99"),
    tax: D("5.20"),
    total: D("45.19"),
    createdAt: new Date("2026-09-19T09:15:00Z")
  },
  {
    orderNumber: "O6499",
    customerId: ObjectId("000000000000000000000001"),
    items: [snap(A400, 1)],
    shippingAddress: {
      street: "Unknown",
      city: "Unknown",
      province: "Unknown",
      postalCode: "00000",
      country: "Unknown"
    },
    paymentStatus: "PENDING",
    fulfillmentStatus: "NEW",
    subtotal: D("24.99"),
    tax: D("3.25"),
    total: D("28.24"),
    createdAt: new Date("2026-09-19T19:00:00Z")
  }
]);

db.reviews.insertMany([
  {
    productId: L100._id,
    sku: "L100",
    customerId: C101._id,
    rating: 5,
    title: "Excellent for travel",
    body: "Light, quiet, and the battery lasts a full workday.",
    createdAt: new Date("2026-09-21T11:00:00Z")
  },
  {
    productId: L110._id,
    sku: "L110",
    customerId: C412._id,
    rating: 5,
    title: "Premium build",
    body: "The extra memory is worth the price.",
    createdAt: new Date("2026-08-20T10:00:00Z")
  },
  {
    productId: S200._id,
    sku: "S200",
    customerId: C204._id,
    rating: 4,
    title: "Comfortable",
    body: "Good for daily runs.",
    createdAt: new Date("2026-07-20T12:00:00Z")
  },
  {
    productId: B300._id,
    sku: "B300",
    customerId: C310._id,
    rating: 5,
    title: "Clear examples",
    body: "Helped me explain pipelines to my team.",
    createdAt: new Date("2026-08-01T09:00:00Z")
  },
  {
    productId: P1001._id,
    sku: "P1001",
    customerId: C620._id,
    rating: 3,
    title: "Works, average keys",
    body: "Fine for travel; not for heavy typing.",
    createdAt: new Date("2026-08-28T15:00:00Z")
  },
  {
    productId: A500._id,
    sku: "A500",
    customerId: C101._id,
    rating: 4,
    title: "One cable desk",
    body: "Replaced a pile of adapters.",
    createdAt: new Date("2026-09-17T08:30:00Z")
  }
]);

print("Loaded " + dbName);
print("customers: " + db.customers.countDocuments());
print("products: " + db.products.countDocuments());
print("orders: " + db.orders.countDocuments());
print("reviews: " + db.reviews.countDocuments());
print("paid orders: " + db.orders.countDocuments({ paymentStatus: "PAID" }));

db.products.createIndex({ sku: 1 }, { unique: true, name: "sku_unique" });
db.customers.createIndex({ customerNumber: 1 }, { unique: true, name: "customerNumber_unique" });
db.orders.createIndex({ orderNumber: 1 }, { unique: true, name: "orderNumber_unique" });
db.customers.createIndex({ "contact.email": 1 }, { unique: true, name: "email_unique" });

print("Module 4 fixtures: XBAD string price; C204 phone null; C515 missing phone; O5001 elemMatch trap; O6401 L100 qty 2.");
print("Do not insert sku A600, A610, A611, A612, A700, A800, A900, TEMP-100 — Module 4 labs create those.");

/**
 * Thin MongoDB connection demo — Mastering MongoDB.
 * URI from MONGODB_URI only. Do not hard-code credentials.
 */
import { MongoClient } from "mongodb";

const uri = process.env.MONGODB_URI;
if (!uri) {
  console.error("Set MONGODB_URI first. See sample-app/README.md.");
  process.exit(1);
}

const client = new MongoClient(uri);

try {
  await client.connect();
  const ping = await client.db("admin").command({ ping: 1 });
  console.log("ping:", ping);

  const products = await client
    .db("training_store")
    .collection("products")
    .find({ active: true })
    .project({ _id: 0, sku: 1, name: 1, category: 1, price: 1 })
    .limit(5)
    .toArray();

  console.log("active products (5):");
  console.log(JSON.stringify(products, null, 2));
} finally {
  await client.close();
}

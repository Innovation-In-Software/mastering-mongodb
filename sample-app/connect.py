'''Thin MongoDB connection demo — Mastering MongoDB.

URI from MONGODB_URI only. Do not hard-code credentials.
'''
import json
import os
import sys

from pymongo import MongoClient
from bson import json_util

uri = os.environ.get("MONGODB_URI")
if not uri:
    print("Set MONGODB_URI first. See sample-app/README.md.", file=sys.stderr)
    sys.exit(1)

client = MongoClient(uri)
try:
    ping = client.admin.command("ping")
    print("ping:", ping)

    products = list(
        client.training_store.products.find(
            {"active": True},
            {"_id": 0, "sku": 1, "name": 1, "category": 1, "price": 1},
        ).limit(5)
    )
    print("active products (5):")
    print(json.dumps(products, default=json_util.default, indent=2))
finally:
    client.close()

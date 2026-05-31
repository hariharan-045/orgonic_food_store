from utils.db_connection import get_db
from bson.objectid import ObjectId

def get_all_products():
    db = get_db()
    return list(db.products.find())

def get_product_by_id(product_id):
    db = get_db()
    return db.products.find_one({"_id": ObjectId(product_id)})

def add_product(name, category, price, quantity, image=""):
    db = get_db()
    db.products.insert_one({
        "name": name,
        "category": category,
        "price": float(price),
        "quantity": int(quantity),
        "image": image
    })

def delete_product(product_id):
    db = get_db()
    db.products.delete_one({"_id": ObjectId(product_id)})

def search_products(query):
    db = get_db()
    return list(db.products.find({
        "$or": [
            {"name":     {"$regex": query, "$options": "i"}},
            {"category": {"$regex": query, "$options": "i"}}
        ]
    }))

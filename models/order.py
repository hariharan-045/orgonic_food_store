from utils.db_connection import get_db

def create_order(product_name, price, customer_name, phone, address, cod=True):
    db = get_db()
    db.orders.insert_one({
        "product": product_name,
        "price": price,
        "name": customer_name,
        "phone": phone,
        "address": address,
        "cod": cod,
        "status": "Confirmed"
    })

def get_all_orders():
    db = get_db()
    return list(db.orders.find())

from utils.db_connection import get_db

def create_user(name, email, password):
    db = get_db()
    db.users.insert_one({
        "name": name,
        "email": email,
        "password": password
    })

def validate_user(email, password):
    db = get_db()
    return db.users.find_one({"email": email, "password": password})

def get_user_by_email(email):
    db = get_db()
    return db.users.find_one({"email": email})

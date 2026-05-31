from utils.db_connection import get_db

SAMPLE_PRODUCTS = [
    {
        "name": "Beetroot",
        "category": "vegetables",
        "price": 70,
        "quantity": 50,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Rote_Beete.jpg/640px-Rote_Beete.jpg",
        "description": "Fresh organic beetroot rich in iron and vitamins."
    },
    {
        "name": "Carrot",
        "category": "vegetables",
        "price": 60,
        "quantity": 80,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Vegetable-Carrot-Bundle-wStalks.jpg/640px-Vegetable-Carrot-Bundle-wStalks.jpg",
        "description": "Crunchy organic carrots loaded with beta-carotene."
    },
    {
        "name": "Muttaikosh",
        "category": "vegetables",
        "price": 88,
        "quantity": 40,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Cauliflower_2.jpg/640px-Cauliflower_2.jpg",
        "description": "Fresh organic cauliflower, great for health."
    },
    {
        "name": "Kavuni Rice",
        "category": "rice",
        "price": 223,
        "quantity": 30,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Ricefield.jpg/640px-Ricefield.jpg",
        "description": "Traditional black kavuni rice with high antioxidants."
    },
    {
        "name": "Pure Honey",
        "category": "honey",
        "price": 350,
        "quantity": 20,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Runny_hunny.jpg/640px-Runny_hunny.jpg",
        "description": "Raw organic honey harvested from forest bees."
    },
    {
        "name": "Coconut Oil",
        "category": "oils",
        "price": 180,
        "quantity": 60,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Coconut_oil_in_jar.jpg/640px-Coconut_oil_in_jar.jpg",
        "description": "Cold-pressed virgin coconut oil for cooking and health."
    },
    {
        "name": "Dry Figs",
        "category": "dryfruits",
        "price": 420,
        "quantity": 25,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Dried-Figs.jpg/640px-Dried-Figs.jpg",
        "description": "Premium quality dried figs rich in fiber and calcium."
    },
    {
        "name": "Turmeric Powder",
        "category": "spices",
        "price": 95,
        "quantity": 70,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Turmeric_plant.jpg/640px-Turmeric_plant.jpg",
        "description": "Pure organic turmeric with high curcumin content."
    },
]

def seed():
    db = get_db()
    if db.products.count_documents({}) == 0:
        db.products.insert_many(SAMPLE_PRODUCTS)
        print(f"  Seeded {len(SAMPLE_PRODUCTS)} products into Atlas.")
    else:
        print(f"  Products already exist ({db.products.count_documents({})} found). Skipping seed.")

    if db.users.count_documents({}) == 0:
        db.users.insert_one({
            "name": "Admin",
            "email": "admin@organicstore.com",
            "password": "admin123"
        })
        print("  Admin user seeded.")

if __name__ == "__main__":
    print("Seeding database...")
    seed()
    print("Done!")

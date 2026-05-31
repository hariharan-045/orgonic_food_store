import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "organic_secret_key_2024")
    MONGO_URI  = os.getenv(
        "MONGO_URI",
        "mongodb+srv://hariharandb:hariharan3112007@cluster0.xlldqu2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    DB_NAME = "organic_food_store"

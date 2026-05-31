from pymongo import MongoClient
from config import Config

_client = None
_db = None

def get_db():
    global _client, _db
    if _db is None:
        _client = MongoClient(Config.MONGO_URI)
        _db = _client[Config.DB_NAME]
    return _db

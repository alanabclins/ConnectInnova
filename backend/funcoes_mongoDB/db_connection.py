import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "ConnectInnova")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    db = client[MONGO_DB]
    projeto_collection = db["projetos"]
    print("✅ Conexão centralizada com MongoDB bem-sucedida!")
except Exception as e:
    print(f"❌ Erro na conexão centralizada com o MongoDB: {e}")
    projeto_collection = None
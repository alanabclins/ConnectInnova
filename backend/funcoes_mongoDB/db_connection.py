# db_connection.py
from pymongo import MongoClient
import os

# Usaremos as variáveis do seu .env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "meu_banco")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    db = client[MONGO_DB]
    projeto_collection = db["projetos"]
    print("✅ Conexão centralizada com MongoDB bem-sucedida!")
except Exception as e:
    print(f"❌ Erro na conexão centralizada com o MongoDB: {e}")
    # Em um app real, você poderia tratar esse erro de forma mais elegante
    projeto_collection = None
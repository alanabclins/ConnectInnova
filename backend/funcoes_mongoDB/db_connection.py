import os

from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "ConnectInnova")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command("ping")
    db = client[MONGO_DB]
    Projetos_collection = db["Projects"]
    Alunos_collection = db["Students"]
    Feedback_collection = db["Feedback"]
    Resumo_collection = db["AI_Resum"]
    print("✅ Conexão centralizada com MongoDB bem-sucedida!")
except Exception as e:
    print(f"❌ Erro na conexão centralizada com o MongoDB: {e}")
    Projeto_collection = None
    Alunos_collection = None
    Feedback_collection = None

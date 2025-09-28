from bson.objectid import ObjectId
from pymongo import MongoClient


# Configurações do Banco de Dados (usando seu ambiente local)
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
DB_NAME = "meu_banco"
PROJETO_COLLECTION_NAME = "projetos" # Vamos criar uma nova coleção para os projetos

# --- INICIALIZAÇÃO DOS CLIENTS ---
try:
    client = MongoClient(MONGO_CONNECTION_STRING)
    client.admin.command('ping')
    print("✅ Conexão com MongoDB bem-sucedida!")
    db = client[DB_NAME]
    projeto_collection = db[PROJETO_COLLECTION_NAME]
except Exception as e:
    print(f"❌ Erro ao conectar com o MongoDB: {e}")
    exit()
# bucar_projeto_por_titulo.py
def buscar_projeto_por_titulo_exato(projeto_collection, titulo):
    """Busca um projeto pelo seu título exato."""
    print(f"   [Task 32] Buscando projeto com título: {titulo}...")
    projeto = projeto_collection.find_one({"titulo": titulo})
    if projeto:
        print(f"   [Task 32] ✅ Projeto encontrado: {projeto['_id']}")
        return projeto
    else:
        print(f"❌ Projeto com o título '{titulo}' não encontrado.")
        return None
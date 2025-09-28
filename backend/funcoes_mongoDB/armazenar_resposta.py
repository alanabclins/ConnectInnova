from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

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

def armazenar_resposta_no_db(projeto_collection, projeto_id_obj, feedback_json):
    """Atualiza o documento do projeto com o feedback da IA."""
    print(f"   [Task 35] Armazenando feedback no projeto {projeto_id_obj}...")
    try:
        result = projeto_collection.update_one(
            {"_id": projeto_id_obj},
            {"$set": {"feedback_ia": feedback_json}}
        )
        if result.modified_count > 0:
            print("   [Task 35] ✅ Feedback armazenado com sucesso no banco de dados.")
            return True
        else:
            print("   [Task 35] ❌ Nenhum documento foi modificado. Verifique o ID.")
            return False
    except Exception as e:
        print(f"   [Task 35] ❌ Erro ao armazenar no banco de dados: {e}")
        return False
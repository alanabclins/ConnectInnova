import sys

from dotenv import load_dotenv
from pymongo import MongoClient

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
    sys.exit()

def salvar_resposta_llm(projeto_collection, projeto_id, resposta_llm, status="sucesso", erro=None):
    """Atualiza o documento do projeto com a análise da LLM no campo analise_llm."""
    print(f"   [Task 35] Salvando análise da LLM no projeto {projeto_id}...")
    try:
        # Estrutura do campo analise_llm com status
        analise_data = {
            "conteudo": resposta_llm,
            "status": status,
            "timestamp": None  # Pode ser adicionado se necessário
        }
        
        # Se houver erro, adiciona informações do erro
        if erro:
            analise_data["erro"] = str(erro)
        
        result = projeto_collection.update_one(
            {"_id": projeto_id},
            {"$set": {"analise_llm": analise_data}}
        )
        if result.modified_count > 0:
            print(f"   [Task 35] ✅ Análise da LLM armazenada com status '{status}' no banco de dados.")
            return True
        else:
            print("   [Task 35] ❌ Nenhum documento foi modificado. Verifique o ID.")
            return False
    except Exception as e:
        print(f"   [Task 35] ❌ Erro ao armazenar no banco de dados: {e}")
        return False

# Mantém a função antiga para compatibilidade (deprecated)
def armazenar_resposta_no_db(projeto_collection, projeto_id_obj, feedback_json):
    """DEPRECATED: Use salvar_resposta_llm() em vez desta função."""
    return salvar_resposta_llm(projeto_collection, projeto_id_obj, feedback_json)

from bson.objectid import ObjectId
import datetime

def salvar_resposta_llm(projeto_collection, projeto_id, resposta_llm, status="sucesso", erro=None):
    """Atualiza o documento do projeto com a análise da LLM no campo analise_llm."""
    print(f"   [Passo 4] Salvando análise no banco de dados (Status: {status})...")
    try:
        analise_data = {
            "conteudo": resposta_llm,
            "status": status,
            "timestamp": datetime.datetime.now(datetime.timezone.utc)
        }
        
        if erro:
            analise_data["erro"] = str(erro)
        
        result = projeto_collection.update_one(
            {"_id": projeto_id},
            {"$set": {"analise_llm": analise_data}}
        )
        if result.modified_count > 0 or result.matched_count > 0:
            print(f"   [Passo 4] ✅ Análise da LLM armazenada com sucesso.")
            return True
        else:
            print("   [Passo 4] ❌ Nenhum documento foi modificado. Verifique o ID.")
            return False
    except Exception as e:
        print(f"   [Passo 4] ❌ Erro ao armazenar no banco de dados: {e}")
        return False
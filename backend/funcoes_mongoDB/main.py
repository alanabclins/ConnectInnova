from bson.objectid import ObjectId
from db_connection import projeto_collection
from gerar_prompt import gerar_prompt_analise
from enviar_para_GEMINI import enviar_para_llm
from armazenar_resposta import salvar_resposta_llm
from buscar_projeto import buscar_projeto_por_id 

def processar_analise_llm(projeto_id_str):
    """
    Orquestra o fluxo completo de análise de um projeto pelo seu ID.
    """
    print(f"\n--- INICIANDO PROCESSAMENTO PARA PROJETO {projeto_id_str} ---")
    
    try:
        projeto_id = ObjectId(projeto_id_str)
    except Exception as e:
        print(f"--- PROCESSAMENTO FALHOU: ID '{projeto_id_str}' é inválido. Erro: {e} ---")
        return False

    projeto = None
    resposta_llm = None
    status_final = "sucesso"
    erro_msg = None

    try:
        # Passo 1: Usa a função dedicada para buscar pelo ID
        projeto = buscar_projeto_por_id(projeto_collection, projeto_id)
        if not projeto:
            raise ValueError(f"Projeto com ID {projeto_id} não encontrado")

        # Passo 2: Gerar prompt
        prompt = gerar_prompt_analise(projeto)
        if not prompt:
            raise ValueError("Falha ao gerar prompt para análise")

        # Passo 3: Enviar para LLM
        resposta_llm = enviar_para_llm(prompt)
        if not resposta_llm:
            raise ValueError("Falha ao obter resposta da LLM (resposta vazia)")

    except Exception as e:
        print(f"--- ERRO NA ORQUESTRAÇÃO: {e} ---")
        status_final = "erro"
        erro_msg = str(e)

    # Passo 4: Salvar o resultado final (sucesso ou erro) no banco
    sucesso_salvar = salvar_resposta_llm(projeto_collection, projeto_id, resposta_llm, status_final, erro_msg)

    if sucesso_salvar and status_final == "sucesso":
        print(f"--- PROCESSAMENTO CONCLUÍDO COM SUCESSO PARA PROJETO {projeto_id} ---")
        return True
    else:
        print(f"--- PROCESSAMENTO FINALIZADO COM ERROS PARA PROJETO {projeto_id} ---")
        return False

# --- BLOCO DE EXECUÇÃO PARA TESTE (sem alterações) ---
if __name__ == "__main__":
    if projeto_collection is not None:
        titulo_para_analisar = "Sistema de Irrigação Automatizado"
        
        projeto_collection.update_one(
            {"titulo": titulo_para_analisar},
            {"$set": {
                "titulo": titulo_para_analisar, "descricao_problema": "Escassez de água.",
                "proposta_solucao": "Sistema automatizado com sensores.", "impacto_social": "Redução do desperdício de água.",
                "viabilidade_tecnica": "Baseado em IoT de baixo custo.", "inovacao": "Uso de machine learning para previsão.",
                "aluno_id": "ALUNO-001", "analise_llm": None
            }},
            upsert=True
        )
        print(f"Ambiente de teste configurado para o projeto: '{titulo_para_analisar}'")

        projeto_teste = projeto_collection.find_one({"titulo": titulo_para_analisar})
        if projeto_teste:
            projeto_id_teste = str(projeto_teste['_id'])
            
            resultado = processar_analise_llm(projeto_id_teste)
            print(f"\nResultado final da orquestração: {'SUCESSO' if resultado else 'FALHA'}")
        else:
            print("❌ Erro: Projeto de teste não encontrado no banco.")
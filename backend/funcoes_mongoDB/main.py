from armazenar_resposta import salvar_feedback_llm, salvar_resumo_llm
from bson.objectid import ObjectId
from buscar_projeto import buscar_projeto_por_id
from db_connection import Alunos_collection, Projetos_collection
from enviar_para_GEMINI import enviar_para_llm
from gerar_prompt import gerar_prompt_analise, gerar_prompt_resumo


def processar_analise_llm(projeto_id_str):
    """
    Orquestra o fluxo completo de análise de um Projeto pelo seu ID.
    """
    print(f"\n--- INICIANDO PROCESSAMENTO PARA PROJETO {projeto_id_str} ---")

    try:
        Projetos_id = ObjectId(projeto_id_str)
    except Exception as e:
        print(f"--- PROCESSAMENTO FALHOU: ID '{projeto_id_str}' é inválido. Erro: {e} ---")
        return False

    Projeto = None
    resposta_llm_analise = None
    status_final = "sucesso"
    erro_msg = None

    try:
        # Passo 1: Usa a função dedicada para buscar pelo ID
        Projeto = buscar_projeto_por_id(Projetos_collection, Projetos_id)
        if not Projeto:
            raise ValueError(f"Projeto com ID {Projetos_id} não encontrado")

        # Passo 2: Gerar prompt de resumo
        prompt_resumo = gerar_prompt_resumo(Projeto)
        if not prompt_resumo:
            raise ValueError("Falha ao gerar prompt para resumo")

        # Passo 3: Gerar prompt de análise
        prompt_analise = gerar_prompt_analise(Projeto)
        if not prompt_analise:
            raise ValueError("Falha ao gerar prompt para análise")

        # Passo 4: Enviar para LLM prompt de resumo
        resposta_llm_resumo = enviar_para_llm(prompt_resumo)
        if not resposta_llm_resumo:
            raise ValueError("Falha ao obter resposta da LLM (resposta vazia)")

        # Passo 5: Enviar para LLM prompt de análise
        resposta_llm_analise = enviar_para_llm(prompt_analise)
        if not resposta_llm_analise:
            raise ValueError("Falha ao obter resposta da LLM (resposta vazia)")

    except Exception as e:
        print(f"--- ERRO NA ORQUESTRAÇÃO: {e} ---")
        status_final = "erro"
        erro_msg = str(e)

    # Passo 6: Salvar os resultados finais (sucessos ou erros) no banco
    sucesso_salvar = salvar_feedback_llm(
        Projetos_id, resposta_llm_analise, status_final, erro_msg
    )

    sucesso_salvar = salvar_resumo_llm(
        Projetos_id, resposta_llm_resumo, status_final, erro_msg
    )

    if sucesso_salvar and status_final == "sucesso":
        print(f"--- PROCESSAMENTO CONCLUÍDO COM SUCESSO PARA PROJETO {Projetos_id} ---")
        return True
    else:
        print(f"--- PROCESSAMENTO FINALIZADO COM ERROS PARA PROJETO {Projetos_id} ---")
        return False


# --- BLOCO DE EXECUÇÃO PARA TESTE (sem alterações) ---
if __name__ == "__main__":
    if Projetos_collection is not None:
        titulo_para_analisar = "Sistema de Irrigação Automatizado"

        Projetos_collection.update_one(
            {"project_title": titulo_para_analisar},
            {
                "$set": {
                    "project_title": titulo_para_analisar,
                    "project_description": "Escassez de água.",
                    "solution_proposal": "Sistema de irrigação automatizado",
                    "social_impact": "Redução do desperdício de água.",
                    "tec_eco_viability": "Baseado em IoT de baixo custo.",
                    "inovation_grade": "Uso de machine learning para previsão.",
                    "application_potencial": "Agricultura familiar e jardins urbanos",
                    "clarity_problem": "Texto explicando o problema",
                    "student_id": ObjectId("68e28a462bd5ef0cac7c8013"),
                }
            },
            upsert=True,
        )
        print(f"Ambiente de teste configurado para o Projeto: '{titulo_para_analisar}'")

    if Alunos_collection is not None:
        nome = "Vinicius"

        Alunos_collection.update_one(
            {"name": nome},
            {
                "$set": {
                    "name": nome,
                    "student_description": "estudante de BSI",
                    "curriculum": None,
                    "academic_informations": "estudante de BSI",
                    "skills_experiencies": "python, SQL, robótica",
                }
            },
            upsert=True,
        )

        Projetos_teste = Projetos_collection.find_one({"project_title": titulo_para_analisar})
        if Projetos_teste:
            Projetos_id_teste = str(Projetos_teste["_id"])

            resultado = processar_analise_llm(Projetos_id_teste)
            print(f"\nResultado final da orquestração: {'SUCESSO' if resultado else 'FALHA'}")
        else:
            print("❌ Erro: Projeto de teste não encontrado no banco.")

from armazenar_resposta import salvar_feedback_llm, salvar_resumo_llm
from bson.objectid import ObjectId
from buscar_projeto import buscar_projeto_por_id
from db_connection import Projetos_collection
from enviar_para_GEMINI import enviar_para_llm
from gerar_prompt import gerar_prompt_analise, gerar_prompt_resumo
from inserir_projeto import criar_projeto


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
    resposta_llm_resumo = None
    status_final = "sucesso"
    erro_msg = None

    try:
        # 1️⃣ Buscar o projeto
        Projeto = buscar_projeto_por_id(Projetos_collection, Projetos_id)
        if not Projeto:
            raise ValueError(f"Projeto com ID {Projetos_id} não encontrado")

        # 2️⃣ Gerar prompts
        prompt_resumo = gerar_prompt_resumo(Projeto)
        if not prompt_resumo:
            raise ValueError("Falha ao gerar prompt para resumo")

        prompt_analise = gerar_prompt_analise(Projeto)
        if not prompt_analise:
            raise ValueError("Falha ao gerar prompt para análise")

        # 3️⃣ Enviar os prompts para a LLM
        resposta_llm_resumo = enviar_para_llm(prompt_resumo)
        if not resposta_llm_resumo:
            raise ValueError("Falha ao obter resposta da LLM (resumo vazio)")

        resposta_llm_analise = enviar_para_llm(prompt_analise)
        if not resposta_llm_analise:
            raise ValueError("Falha ao obter resposta da LLM (análise vazia)")

    except Exception as e:
        print(f"--- ERRO NA ORQUESTRAÇÃO: {e} ---")
        status_final = "erro"
        erro_msg = str(e)

    # 4️⃣ Salvar resultados
    sucesso_feedback = salvar_feedback_llm(Projetos_id, resposta_llm_analise, status_final, erro_msg)
    sucesso_resumo = salvar_resumo_llm(Projetos_id, resposta_llm_resumo, status_final, erro_msg)

    # 5️⃣ Finalização
    if sucesso_feedback and sucesso_resumo and status_final == "sucesso":
        print(f"--- PROCESSAMENTO CONCLUÍDO COM SUCESSO PARA PROJETO {Projetos_id} ---")
        return True
    else:
        print(f"--- PROCESSAMENTO FINALIZADO COM ERROS PARA PROJETO {Projetos_id} ---")
        return False


# --- BLOCO DE EXECUÇÃO PARA TESTE ---
if __name__ == "__main__":

    # 🧩 Cria um novo projeto no banco
    payload = {
        "project_title": "Monitor de Energia Inteligente",
        "project_description": "Sistema que mede consumo elétrico em tempo real.",
        "solution_proposal": "Uso de microcontroladores e IA para previsão de consumo.",
        "clarity_problem": None,
        "inovation_grade": None,
        "social_impact": None,
        "tec_eco_viability": None,
        "application_potencial": None,
        "student_name": "Maria Eduarda",
        "student_description": "Estudante de Engenharia Elétrica",
        "student_skills": "Python, Eletrônica, IA",
    }

    project_id = criar_projeto(payload)
    print("✅ Projeto cadastrado com ID:", project_id)

    # 🚀 Processa o projeto recém-criado
    if project_id:
        resultado = processar_analise_llm(str(project_id))
        print(f"\nResultado final da orquestração: {'SUCESSO' if resultado else 'FALHA'}")
    else:
        print("❌ Erro: projeto não foi criado corretamente.")

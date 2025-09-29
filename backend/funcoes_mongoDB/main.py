# main.py
from armazenar_resposta import salvar_resposta_llm
from bucar_projeto_por_titulo import buscar_projeto_por_titulo_exato
from db_connection import projeto_collection  # Importa a conexão já pronta!
from enviar_para_GEMINI import enviar_para_llm
from gerar_prompt import gerar_prompt_analise


def processar_analise_llm(projeto_id):
    """
    Integra todas as subtasks em um único fluxo para análise de projeto via LLM.
    
    Args:
        projeto_id: ID do projeto no MongoDB
        
    Returns:
        bool: True se sucesso, False se falha
    """
    print(f"\n--- INICIANDO PROCESSAMENTO DE ANÁLISE LLM PARA PROJETO {projeto_id} ---")
    
    try:
        # 1. Buscar projeto pelo ID
        print("   [Step 1] Buscando projeto no banco de dados...")
        projeto = projeto_collection.find_one({"_id": projeto_id})
        if not projeto:
            erro_msg = f"Projeto com ID {projeto_id} não encontrado"
            print(f"   [Step 1] ❌ {erro_msg}")
            salvar_resposta_llm(projeto_collection, projeto_id, None, "erro", erro_msg)
            return False
        print(f"   [Step 1] ✅ Projeto encontrado: {projeto.get('titulo', 'Sem título')}")
        
        # 2. Gerar prompt
        print("   [Step 2] Gerando prompt para análise...")
        try:
            prompt = gerar_prompt_analise(projeto)
            if not prompt:
                erro_msg = "Falha ao gerar prompt para análise"
                print(f"   [Step 2] ❌ {erro_msg}")
                salvar_resposta_llm(projeto_collection, projeto_id, None, "erro", erro_msg)
                return False
            print("   [Step 2] ✅ Prompt gerado com sucesso")
        except Exception as e:
            erro_msg = f"Erro ao gerar prompt: {str(e)}"
            print(f"   [Step 2] ❌ {erro_msg}")
            salvar_resposta_llm(projeto_collection, projeto_id, None, "erro", erro_msg)
            return False
        
        # 3. Enviar para LLM
        print("   [Step 3] Enviando prompt para LLM...")
        try:
            resposta_llm = enviar_para_llm(prompt)
            if not resposta_llm:
                erro_msg = "Falha ao obter resposta da LLM"
                print(f"   [Step 3] ❌ {erro_msg}")
                salvar_resposta_llm(projeto_collection, projeto_id, None, "erro", erro_msg)
                return False
            print("   [Step 3] ✅ Resposta da LLM recebida com sucesso")
        except Exception as e:
            erro_msg = f"Erro ao comunicar com LLM: {str(e)}"
            print(f"   [Step 3] ❌ {erro_msg}")
            salvar_resposta_llm(projeto_collection, projeto_id, None, "erro", erro_msg)
            return False
        
        # 4. Salvar resposta
        print("   [Step 4] Salvando análise no banco de dados...")
        try:
            sucesso = salvar_resposta_llm(projeto_collection, projeto_id, resposta_llm, "sucesso")
            if not sucesso:
                erro_msg = "Falha ao salvar análise no banco de dados"
                print(f"   [Step 4] ❌ {erro_msg}")
                salvar_resposta_llm(projeto_collection, projeto_id, None, "erro", erro_msg)
                return False
            print("   [Step 4] ✅ Análise salva com sucesso")
        except Exception as e:
            erro_msg = f"Erro ao salvar no banco: {str(e)}"
            print(f"   [Step 4] ❌ {erro_msg}")
            salvar_resposta_llm(projeto_collection, projeto_id, None, "erro", erro_msg)
            return False
        
        print(f"--- PROCESSAMENTO CONCLUÍDO COM SUCESSO PARA PROJETO {projeto_id} ---")
        return True
        
    except Exception as e:
        # Captura qualquer erro não tratado
        erro_msg = f"Erro inesperado no processamento: {str(e)}"
        print(f"--- PROCESSAMENTO FALHOU: {erro_msg} ---")
        try:
            salvar_resposta_llm(projeto_collection, projeto_id, None, "erro", erro_msg)
        except:
            print("   ❌ Erro crítico: não foi possível salvar status de erro no banco")
        return False


def orquestrar_analise_por_titulo(titulo_do_projeto):
    """Executa o fluxo completo de análise de um projeto buscando pelo TÍTULO."""
    print(f"\n--- INICIANDO ORQUESTRAÇÃO PARA O PROJETO '{titulo_do_projeto}' ---")

    # 1. Buscar projeto pelo TÍTULO
    projeto = buscar_projeto_por_titulo_exato(projeto_collection, titulo_do_projeto)
    if not projeto:
        print("--- ORQUESTRAÇÃO FALHOU: Projeto não encontrado. ---")
        return

    # AQUI ESTÁ A CORREÇÃO DA LÓGICA:
    # Pegamos o _id do projeto que foi encontrado para usar na hora de salvar.
    id_do_projeto = projeto['_id']

    # 2. Gerar prompt
    prompt = gerar_prompt_analise(projeto)

    # 3. Enviar para o LLM
    feedback = enviar_para_llm(prompt)
    if not feedback:
        print("--- ORQUESTRAÇÃO FALHOU: Não foi possível obter feedback da IA. ---")
        return

    # 4. Armazenar resposta usando o _ID que pegamos
    sucesso = salvar_resposta_llm(projeto_collection, id_do_projeto, feedback)
    if sucesso:
        print(
            f"--- ORQUESTRAÇÃO CONCLUÍDA COM SUCESSO PARA O PROJETO "
            f"'{titulo_do_projeto}' ---"
        )
    else:
        print("--- ORQUESTRAÇÃO FALHOU: Erro ao salvar o feedback. ---")

# --- BLOCO DE EXECUÇÃO PARA TESTE ---
if __name__ == "__main__":
    if projeto_collection is not None:
        # Título do projeto que queremos analisar
        titulo_para_analisar = "Sistema de Irrigação Automatizado"

        # Garante que um projeto com esse título exista para o teste
        projeto_collection.update_one(
            {"titulo": titulo_para_analisar},
            {"$set": {
                "titulo": titulo_para_analisar,
                "descricao_problema": (
                    "A agricultura enfrenta desafios significativos com a escassez de água "
                    "e a necessidade de otimizar o uso de recursos hídricos."
                ),
                "proposta_solucao": (
                    "Desenvolvimento de um sistema automatizado de irrigação que utiliza "
                    "sensores de umidade do solo e dados meteorológicos para otimizar "
                    "o uso da água."
                ),
                "impacto_social": (
                    "Redução do desperdício de água na agricultura, contribuindo para "
                    "sustentabilidade ambiental e segurança alimentar."
                ),
                "viabilidade_tecnica": (
                    "Sistema baseado em IoT com sensores de baixo custo, microcontroladores "
                    "e conectividade WiFi/LoRa para monitoramento remoto."
                ),
                "inovacao": (
                    "Integração de machine learning para previsão de necessidades hídricas "
                    "baseada em padrões climáticos e histórico de cultivos."
                ),
                "aluno_id": "ALUNO-001",
                "analise_llm": None # Garante que a análise está limpa para o teste
            }},
            upsert=True # Cria o projeto se ele não existir
        )
        print(f"Ambiente de teste configurado para o projeto: '{titulo_para_analisar}'")

        # Busca o ID do projeto para testar a nova função
        projeto_teste = projeto_collection.find_one({"titulo": titulo_para_analisar})
        if projeto_teste:
            projeto_id_teste = projeto_teste['_id']
            print(f"ID do projeto para teste: {projeto_id_teste}")
            
            # Testa a nova função processar_analise_llm
            resultado = processar_analise_llm(projeto_id_teste)
            print(f"Resultado do processamento: {'SUCESSO' if resultado else 'FALHA'}")
        else:
            print("❌ Erro: Projeto de teste não encontrado")

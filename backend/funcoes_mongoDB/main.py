# main.py
from db_connection import projeto_collection # Importa a conexão já pronta!
from enviar_para_GEMINI import enviar_prompt_para_llm
from armazenar_resposta import armazenar_resposta_no_db
from gerar_prompt import gerar_prompt_analise
from bucar_projeto_por_titulo import buscar_projeto_por_titulo_exato

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
    feedback = enviar_prompt_para_llm(prompt)
    if not feedback:
        print("--- ORQUESTRAÇÃO FALHOU: Não foi possível obter feedback da IA. ---")
        return

    # 4. Armazenar resposta usando o _ID que pegamos
    sucesso = armazenar_resposta_no_db(projeto_collection, id_do_projeto, feedback)
    if sucesso:
        print(f"--- ORQUESTRAÇÃO CONCLUÍDA COM SUCESSO PARA O PROJETO '{titulo_do_projeto}' ---")
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
                "resumo": "Este projeto propõe o desenvolvimento de um sistema de baixo custo...",
                "aluno_id": "ALUNO-001",
                "feedback_ia": None # Garante que o feedback está limpo para o teste
            }},
            upsert=True # Cria o projeto se ele não existir
        )
        print(f"Ambiente de teste configurado para o projeto: '{titulo_para_analisar}'")
        
        # Chama a função principal que executa todo o processo
        orquestrar_analise_por_titulo(titulo_para_analisar)
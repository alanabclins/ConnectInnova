import json
from datetime import datetime

from db_connection import Feedback_collection, Projetos_collection, Resumo_collection


def salvar_feedback_llm(project_id, resposta_llm, status_final, erro_msg=None):
    """
    Salva o FEEDBACK da LLM na coleção Feedback, vinculado ao projeto e estudante.
    """
    try:
        projeto = Projetos_collection.find_one({"_id": project_id})
        if not projeto:
            print(f"⚠️ Projeto com ID {project_id} não encontrado ao tentar salvar feedback.")
            return False

        # --- 🔧 LIMPEZA DO TEXTO RETORNADO PELA LLM ---
        if isinstance(resposta_llm, str):
            resposta_limpa = resposta_llm.replace("```json", "").replace("```", "").strip()
            try:
                resposta_llm = json.loads(resposta_limpa)
            except json.JSONDecodeError:
                print("⚠️ A resposta da LLM não está em formato JSON válido:")
                print(resposta_llm)
                return False

        feedback = {
            "project_id": project_id,
            "student_id": projeto.get("student_id", None),
            "feedback": {
                "clarity_problem": resposta_llm.get("clarity_problem", ""),
                "inovation_grade": resposta_llm.get("inovation_grade", ""),
                "social_impact": resposta_llm.get("social_impact", ""),
                "tec_eco_viability": resposta_llm.get("tec_eco_viability", ""),
                "application_potencial": resposta_llm.get("application_potencial", ""),
                "solution_proposal": resposta_llm.get("solution_proposal", ""),
                "status": status_final,
                "timestamp": datetime.utcnow(),
            },
            "status": status_final,
            "erro_msg": erro_msg,
            "timestamp": datetime.utcnow(),
        }

        resultado = Feedback_collection.insert_one(feedback)
        if resultado.inserted_id:
            print(
                f"✅ Feedback salvo com coleção Feedback! (ID: {resultado.inserted_id})"
            )
            return True
        else:
            print("⚠️ Falha ao inserir o feedback na coleção Feedback.")
            return False

    except Exception as e:
        print(f"❌ Erro ao salvar resposta LLM (feedback): {e}")
        return False


def salvar_resumo_llm(project_id, resposta_llm, status_final, erro_msg=None):
    """
    Salva o RESUMO da LLM na coleção Resumo, vinculado ao projeto e estudante.
    """
    try:
        projeto = Projetos_collection.find_one({"_id": project_id})
        if not projeto:
            print(f"⚠️ Projeto com ID {project_id} não encontrado ao tentar salvar resumo.")
            return False

        # --- 🔧 LIMPEZA DO TEXTO RETORNADO PELA LLM ---
        if isinstance(resposta_llm, str):
            resposta_limpa = resposta_llm.replace("```json", "").replace("```", "").strip()
            try:
                resposta_llm = json.loads(resposta_limpa)
            except json.JSONDecodeError:
                print("⚠️ A resposta da LLM não está em formato JSON válido:")
                print(resposta_llm)
                return False

        resumo = {
            "project_id": project_id,
            "student_id": projeto.get("student_id", None),
            "summary": {  # para diferenciar do feedback
                "content": json.dumps(resposta_llm, ensure_ascii=False),
                "status": status_final,
                "timestamp": datetime.utcnow(),
            },
            "clarity_resum": resposta_llm.get("clarity_problem", ""),
            "inovation_grade_resum": resposta_llm.get("inovation_grade", ""),
            "social_impact_resum": resposta_llm.get("social_impact", ""),
            "tec_eco_viability_resum": resposta_llm.get("tec_eco_viability", ""),
            "application_potencial_resum": resposta_llm.get("application_potencial", ""),
            "solution_proposal_resum": resposta_llm.get("solution_proposal", ""),
            "status": status_final,
            "erro_msg": erro_msg,
            "timestamp": datetime.utcnow(),
        }

        resultado = Resumo_collection.insert_one(resumo)
        if resultado.inserted_id:
            print(
                f"✅ Resumo salvo na coleção Resumo! (ID: {resultado.inserted_id})"
            )
            return True
        else:
            print("⚠️ Falha ao inserir o resumo na coleção Resumo.")
            return False

    except Exception as e:
        print(f"❌ Erro ao salvar resposta LLM (resumo): {e}")
        return False

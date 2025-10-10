from fastapi import APIRouter, HTTPException, Body
from uuid import UUID
from datetime import datetime
from google import genai
from datetime import datetime, UTC

from .. import models
from app.config.config import settings

router = APIRouter()

# Inicializar cliente Gemini
if not settings.GEMINI_API_KEY:
    raise ValueError("❌ A variável de ambiente GEMINI_API_KEY não foi configurada.")
client = genai.Client(api_key=settings.GEMINI_API_KEY)


@router.post("/analysis/{project_uuid}")
async def analyze_project(project_uuid: UUID, custom_prompt: str = Body(None)):
    """
    Analisa o potencial de um projeto universitário usando a API Gemini.

    Parâmetros:
    - project_uuid: UUID do projeto a ser analisado.
    - custom_prompt (opcional): texto adicional enviado junto ao conteúdo do projeto.

    Fluxo:
    1. Busca o projeto no banco.
    2. Envia os dados para a API do Gemini.
    3. Armazena o feedback e o resumo nas coleções 'Feedback' e 'AI_Resum'.
    """

    # Buscar o projeto
    project = await models.Project.find_one({"uuid": project_uuid})
    if project is None:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")

    # Buscar o aluno vinculado
    student = await models.Student.get(project.student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Aluno vinculado não encontrado.")

    # Montar prompt básico
    prompt = f"""
    Analise o seguinte projeto universitário e descreva os seguintes aspectos:
    - Clareza do problema
    - Grau de inovação
    - Impacto social
    - Viabilidade técnica e econômica
    - Potencial de aplicação

    Dados do projeto:
    Título: {project.project_title}
    Descrição: {project.project_description}
    Solução proposta: {project.solution_proposal}
    """

    if custom_prompt:
        prompt += f"\nInformações adicionais:\n{custom_prompt}"

    # Enviar para Gemini
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash", contents=prompt
        )
        feedback_text = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na API Gemini: {e}")

    # Criar Feedback
    feedback_doc = models.Feedback(
        project=project, # type: ignore
        student=student, # type: ignore
        feedback={
            "content": feedback_text,
            "status": "generated",
            "timestamp": datetime.now(UTC),
        },
        ai_feedback_clarity_problem="Avaliação automática gerada",
        ai_feedback_inovation_grade="Avaliação automática gerada",
        ai_feedback_social_impact="Avaliação automática gerada",
        ai_feedback_tec_eco_viability="Avaliação automática gerada",
        ai_feedback_application_potencial="Avaliação automática gerada",
    )
    await feedback_doc.create()

    # Criar AI_Resum (resumo)
    resum_doc = models.AIResum(
        project_id=project, # type: ignore
        student_id=student, # type: ignore
        clarity_resum="Resumo gerado automaticamente",
        inovation_grade_resum="Resumo gerado automaticamente",
        social_impact_resum="Resumo gerado automaticamente",
        tec_eco_viability_resum="Resumo gerado automaticamente",
        application_potencial_resum="Resumo gerado automaticamente",
    )
    await resum_doc.create()

    return {
        "message": "✅ Análise concluída com sucesso.",
        "feedback_id": str(feedback_doc.uuid),
        "resum_id": str(resum_doc.uuid),
        "feedback_text": feedback_text,
    }

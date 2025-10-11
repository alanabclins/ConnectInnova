import json
from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException
from google import genai
from pydantic import BaseModel, Field

from app.config.config import settings

from .. import models

router = APIRouter()

if not settings.GEMINI_API_KEY:
    raise ValueError("❌ A variável de ambiente GEMINI_API_KEY não foi configurada.")
client = genai.Client(api_key=settings.GEMINI_API_KEY)


class AIAnalysis(BaseModel):
    clarity_problem: str = Field(description="Análise detalhada da clareza do problema.")
    inovation_grade: str = Field(description="Análise detalhada do grau de inovação.")
    social_impact: str = Field(description="Análise detalhada do impacto social.")
    tec_eco_viability: str = Field(
        description="Análise detalhada da viabilidade técnica e econômica."
    )
    application_potencial: str = Field(
        description="Análise detalhada do potencial de aplicação."
    )


class AIResum(BaseModel):
    clarity_resum: str = Field(
        description="Resumo de 2-3 frases sobre a clareza do problema."
    )
    inovation_grade_resum: str = Field(
        description="Resumo de 2-3 frases sobre o grau de inovação."
    )
    social_impact_resum: str = Field(
        description="Resumo de 2-3 frases sobre o impacto social."
    )
    tec_eco_viability_resum: str = Field(
        description="Resumo de 2-3 frases sobre a viabilidade."
    )
    application_potencial_resum: str = Field(
        description="Resumo de 2-3 frases sobre o potencial de aplicação."
    )


class GeminiStructuredResponse(BaseModel):
    full_feedback: str = Field(description="Um resumo geral e envolvente do projeto.")
    analysis: AIAnalysis
    resums: AIResum


@router.post("/{project_uuid}")
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
    # Ajuste para usar find_one() e o campo UUID, corrigindo o erro de validação
    student = await models.User.find_one(models.User.uuid == project.student_id)
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
    Instrução para saída: Preencha estritamente a estrutura JSON solicitada.
    """

    if custom_prompt:
        prompt += f"\nInformações adicionais:\n{custom_prompt}"

    # Enviar para Gemini (Configurado para JSON)
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GeminiStructuredResponse,
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao chamar a API Gemini: {e}")

    ai_data = None
    ai_data_str = ""

    try:
        if response.text is not None:
            ai_data_str = response.text
            ai_data = GeminiStructuredResponse.model_validate_json(ai_data_str)
        else:
            ai_data_str = ""
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar JSON da IA. Retorno bruto: {ai_data_str}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na API Gemini: {e}")

    if ai_data is None:
        raise HTTPException(status_code=500, detail="Resposta da IA inválida ou vazia.")

    # Criar Feedback (Usando dados estruturados do Gemini e objetos Link)
    feedback_doc = models.Feedback(
        project=project,  # type: ignore[arg-type]
        student=student,  # type: ignore[arg-type]
        feedback={
            "content": ai_data.full_feedback,
            "status": "generated",
            "timestamp": datetime.now(UTC),
        },
        ai_feedback_clarity_problem=ai_data.analysis.clarity_problem,
        ai_feedback_inovation_grade=ai_data.analysis.inovation_grade,
        ai_feedback_social_impact=ai_data.analysis.social_impact,
        ai_feedback_tec_eco_viability=ai_data.analysis.tec_eco_viability,
        ai_feedback_application_potencial=ai_data.analysis.application_potencial,
    )
    await feedback_doc.create()

    # Criar AI_Resum (resumo, usando dados estruturados do Gemini e objetos Link)
    resum_doc = models.AIResum(
        project=project,  # type: ignore[arg-type]
        student=student,  # type: ignore[arg-type]
        clarity_resum=ai_data.resums.clarity_resum,
        inovation_grade_resum=ai_data.resums.inovation_grade_resum,
        social_impact_resum=ai_data.resums.social_impact_resum,
        tec_eco_viability_resum=ai_data.resums.tec_eco_viability_resum,
        application_potencial_resum=ai_data.resums.application_potencial_resum,
    )
    await resum_doc.create()

    return {
        "message": "✅ Análise concluída com sucesso.",
        "feedback_id": str(feedback_doc.uuid),
        "resum_id": str(resum_doc.uuid),
        "feedback_summary": ai_data.full_feedback,
    }

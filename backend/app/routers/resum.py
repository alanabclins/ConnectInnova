import json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from google import genai

from app import models
from app.auth.auth import get_current_active_user
from app.config.config import settings
from app.models.ai_resume import AIResum
from app.models.projects import Project
from app.models.users import User
from app.routers.ai_config import prompt_template
from pydantic import ValidationError

router = APIRouter()

# Inicializa cliente Gemini
if not settings.GEMINI_API_KEY:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi configurada.")
client = genai.Client(api_key=settings.GEMINI_API_KEY)


def normalize_resum_json(data: dict) -> dict:
    """
    Garante que todos os campos do JSON existam após a resposta do Gemini.
    """
    required_fields = [
        "clarity_resum",
        "inovation_grade_resum",
        "social_impact_resum",
        "tec_eco_viability_resum",
        "application_potencial_resum",
    ]

    normalized = {}
    for field in required_fields:
        normalized[field] = data.get(field, "")  # default = string vazia

    return normalized


@router.get("/{project_uuid}")
async def generate_resum(
    project_uuid: UUID, current_user: models.User = Depends(get_current_active_user)
):
    """
    Gera um resumo simplificado de cada aspecto do projeto usando o Gemini.
    """

    # 1) Buscar projeto
    project = await Project.find_one(Project.uuid == project_uuid)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")

    # 2) Buscar aluno
    student = await User.find_one(User.uuid == project.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Aluno vinculado não encontrado.")

    # 3) Construir prompt
    project_data = {
        "project_title": project.project_title,
        "project_description": project.project_description,
        "solution_proposal": project.solution_proposal,
        "clarity_problem": project.clarity_problem,
        "inovation_grade": project.inovation_grade,
        "social_impact": project.social_impact,
        "tec_eco_viability": project.tec_eco_viability,
        "application_potencial": project.application_potencial,
    }

    prompt = prompt_template.build_resum_prompt(project_data)

    # 4) Enviar ao Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        raw_text = """
        {
            "resums":{
                "clarity_resum": "ecocycle"
            }
        }
        """

        if not raw_text or raw_text.strip() == "":
            raise HTTPException(status_code=500, detail="O Gemini não retornou nenhum texto.")

        # Remover markdown indesejado
        cleaned_response = (
            raw_text.strip()
            .removeprefix("```json")
            .removeprefix("```JSON")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )

        try:
            ai_data = json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Resposta JSON inválida. Erro: {str(e)} | Conteúdo recebido: {cleaned_response[:400]}",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na API Gemini: {e}")

    # 5) Estrutura mínima obrigatória
    if not ai_data or "resums" not in ai_data:
        raise HTTPException(
            status_code=500,
            detail="❌ A resposta da IA não contém o campo 'resums'."
        )

    # 6) Normalizar JSON
    resums_raw = ai_data["resums"]
    resums_fixed = normalize_resum_json(resums_raw)

    # 7) Criar o documento no banco
    resum_doc = AIResum(
        project_id=project.uuid,
        student_id=student.uuid,
        clarity_resum=resums_fixed["clarity_resum"],
        inovation_grade_resum=resums_fixed["inovation_grade_resum"],
        social_impact_resum=resums_fixed["social_impact_resum"],
        tec_eco_viability_resum=resums_fixed["tec_eco_viability_resum"],
        application_potencial_resum=resums_fixed["application_potencial_resum"],
    )

    await resum_doc.create()

    # 8) Resposta para o front
    return {
        "message": "Resumo gerado com sucesso!",
        "resum_id": str(resum_doc.uuid),
        "resums": resums_fixed,
    }

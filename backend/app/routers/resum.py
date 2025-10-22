import json
from uuid import UUID

from fastapi import APIRouter, HTTPException
from google import genai

from app.config.config import settings
from app.models.ai_resume import AIResum
from app.models.projects import Project
from app.models.users import User

from ..prompt_template import build_resum_prompt  # ✅ usa o prompt que você mostrou

router = APIRouter()

# ✅ Inicializa cliente Gemini
if not settings.GEMINI_API_KEY:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi configurada.")
client = genai.Client(api_key=settings.GEMINI_API_KEY)


@router.get("/{project_uuid}")
async def generate_resum(project_uuid: UUID):
    """
    Gera um resumo simplificado de cada aspecto do projeto
    (clareza, inovação, impacto, viabilidade e aplicabilidade)
    usando a API Gemini.
    """
    # 1️⃣ Busca o projeto no banco
    project = await Project.find_one(Project.uuid == project_uuid)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")

    # 2️⃣ Busca o aluno vinculado
    student = await User.find_one(User.uuid == project.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Aluno vinculado não encontrado.")

    # 3️⃣ Cria o prompt com base nos dados do projeto
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

    prompt = build_resum_prompt(project_data)

    # 4️⃣ Envia para o Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        ai_raw = getattr(response, "text", None)
        if not ai_raw or ai_raw.strip() == "":
            raise HTTPException(status_code=500, detail="O Gemini não retornou nenhum texto.")

        # Limpa o JSON retornado
        cleaned_response = (
            ai_raw.strip()
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
                detail=f"Resposta JSON inválida. Erro: {str(e)} | {cleaned_response[:500]}",
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na API Gemini: {e}")

    # 5️⃣ Valida o formato do JSON
    if not ai_data or "resums" not in ai_data:
        raise HTTPException(
            status_code=500, detail="❌ Resposta da IA em formato inválido ou incompleto."
        )

    resums_data = ai_data["resums"]

    # 6️⃣ Cria o documento AIResum
    resum_doc = AIResum(
        project_id=project.uuid,
        student_id=student.uuid,
        clarity_resum=resums_data.get("clarity_resum"),
        inovation_grade_resum=resums_data.get("inovation_grade_resum"),
        social_impact_resum=resums_data.get("social_impact_resum"),
        tec_eco_viability_resum=resums_data.get("tec_eco_viability_resum"),
        application_potencial_resum=resums_data.get("application_potencial_resum"),
    )

    await resum_doc.create()

    # 7️⃣ Retorna para o front
    return {
        "message": "✅ Resumo gerado com sucesso!",
        "resum_id": str(resum_doc.uuid),
        "resums": resums_data,
    }

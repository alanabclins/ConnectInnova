import json
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException
from google import genai

from app.config.config import settings
from app.prompt_template import build_evaluation_prompt
from app.models.ai_resume import AIResum
from app.models.feedback import Feedback
from app.models.projects import Project
from app.models.users import User
from app.schemas.ai_resume_schema import AIResumSchema
from app.schemas.feedback_schema import FeedbackSchema

router = APIRouter()

#  Inicializa cliente Gemini
if not settings.GEMINI_API_KEY:
    raise ValueError(" A variável de ambiente GEMINI_API_KEY não foi configurada.")
client = genai.Client(api_key=settings.GEMINI_API_KEY)


# ======== Estrutura esperada da resposta do Gemini =========
class GeminiAIAnalysis:
    def __init__(
        self,
        clarity_problem,
        inovation_grade,
        social_impact,
        tec_eco_viability,
        application_potencial,
    ):
        self.clarity_problem = clarity_problem
        self.inovation_grade = inovation_grade
        self.social_impact = social_impact
        self.tec_eco_viability = tec_eco_viability
        self.application_potencial = application_potencial


class GeminiAIResum:
    def __init__(
        self,
        clarity_resum,
        inovation_grade_resum,
        social_impact_resum,
        tec_eco_viability_resum,
        application_potencial_resum,
    ):
        self.clarity_resum = clarity_resum
        self.inovation_grade_resum = inovation_grade_resum
        self.social_impact_resum = social_impact_resum
        self.tec_eco_viability_resum = tec_eco_viability_resum
        self.application_potencial_resum = application_potencial_resum


@router.post("/{project_uuid}")
async def analyze_project(project_uuid: UUID, custom_prompt: str = Body(None)):
    """
    Analisa um projeto universitário com a API Gemini.
    Gera: feedback detalhado + resumo de 2-3 frases por aspecto.
    """

    # 1️ Busca projeto no banco
    project = await Project.find_one(Project.uuid == project_uuid)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")

    # 2️ Busca aluno vinculado
    student = await User.find_one(User.uuid == project.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Aluno vinculado não encontrado.")

    # 3️ Cria o prompt usando o template estruturado com base nos 15 critérios
    project_data = {
        'project_title': project.project_title,
        'project_description': project.project_description,
        'solution_proposal': project.solution_proposal,
        'clarity_problem': project.clarity_problem,
        'inovation_grade': project.inovation_grade,
        'social_impact': project.social_impact,
        'tec_eco_viability': project.tec_eco_viability,
        'application_potencial': project.application_potencial
    }
    
    prompt = build_evaluation_prompt(project_data)

    if custom_prompt:
        prompt += f"\nInstruções adicionais do avaliador:\n{custom_prompt}"

    # 4️⃣ Envia para o Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        # 👇 Captura o texto retornado
        ai_raw = getattr(response, "text", None)
        if not ai_raw or ai_raw.strip() == "":
            raise HTTPException(
                status_code=500,
                detail="O Gemini não retornou nenhum texto.",
            )

        # print("🔍 Retorno bruto do Gemini:\n", ai_raw)

        # 🔧 NOVO: limpeza de blocos de código e espaços extras
        cleaned_response = (
            ai_raw.strip()
            .removeprefix("```json")
            .removeprefix("```JSON")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )

        # 👇 Garante que a resposta seja JSON válida
        try:
            ai_data = json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Resposta JSON inválido. Erro: {str(e)} | {cleaned_response[:500]}",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na API Gemini: {e}")

    # 5️⃣ Valida o formato
    if not ai_data or "analysis" not in ai_data or "resums" not in ai_data:
        raise HTTPException(
            status_code=500, detail="❌ Resposta da IA em formato inválido ou incompleto."
        )

    # 6️⃣ Cria Feedback
    feedback_schema = FeedbackSchema(
        project_id=project.uuid,
        student_id=student.uuid,
        feedback_content=ai_data["full_feedback"],
        ai_feedback_clarity_problem=ai_data["analysis"].get("clarity_problem", ""),
        ai_feedback_inovation_grade=ai_data["analysis"].get("inovation_grade", ""),
        ai_feedback_social_impact=ai_data["analysis"].get("social_impact", ""),
        ai_feedback_tec_eco_viability=ai_data["analysis"].get("tec_eco_viability", ""),
        ai_feedback_application_potencial=ai_data["analysis"].get(
            "application_potencial", ""
        ),
    )

    feedback_doc = Feedback(**feedback_schema.model_dump())
    await feedback_doc.create()

    # 7️⃣ Cria AI Resume
    resum_schema = AIResumSchema(
        project_id=project.uuid,
        student_id=student.uuid,
        clarity_resum=ai_data["resums"].get("clarity_resum", ""),
        inovation_grade_resum=ai_data["resums"].get("inovation_grade_resum", ""),
        social_impact_resum=ai_data["resums"].get("social_impact_resum", ""),
        tec_eco_viability_resum=ai_data["resums"].get("tec_eco_viability_resum", ""),
        application_potencial_resum=ai_data["resums"].get("application_potencial_resum", ""),
    )

    resum_doc = AIResum(**resum_schema.model_dump())
    await resum_doc.create()

    # 8️⃣ Retorna para o front
    return {
        "message": "✅ Análise concluída com sucesso!",
        "feedback_id": str(feedback_doc.uuid),
        "resum_id": str(resum_doc.uuid),
        "feedback_summary": ai_data["full_feedback"],
    }

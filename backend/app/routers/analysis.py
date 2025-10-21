import json
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException
from google import genai

from app.config.config import settings
from app.evaluation_criteria import EVALUATION_CRITERIA
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

    # 3️ Cria o prompt dinâmico estruturado com base nos 15 critérios
    
    # Constrói a tabela de critérios de forma compacta
    criteria_table = ""
    for idx, (key, criterion) in enumerate(EVALUATION_CRITERIA.items(), 1):
        criteria_table += f"\n{idx}. **{criterion['name']}**: {criterion['definition']}\n"
        # Apenas os níveis extremos e médio para economizar tokens
        for level_data in [criterion['levels'][0], criterion['levels'][2], criterion['levels'][4]]:
            criteria_table += f"N{level_data['level']} ({level_data['label']}): {level_data['description']}\n"

    prompt = f"""
Você é um avaliador acadêmico especializado em inovação e empreendedorismo. Avalie o projeto com base nos critérios abaixo, usando escala 1-5:
- Níveis 1-2 (Ruim): Incompleto, sem evidências
- Nível 3 (Médio): Coerente, evidências parciais
- Nível 4 (Bom): Estruturado, com evidências
- Nível 5 (Excelente): Completo, validado, comprovado

PROJETO:
Título: {project.project_title}
Descrição: {project.project_description}
Solução: {project.solution_proposal}
Problema: {project.clarity_problem}
Inovação: {project.inovation_grade}
Impacto: {project.social_impact}
Viabilidade: {project.tec_eco_viability}
Aplicação: {project.application_potencial}

CRITÉRIOS (analise cada um considerando os níveis):
{criteria_table}

Responda em JSON (sem markdown):
{{
    "full_feedback": "Avaliação geral em 3-4 parágrafos com pontos fortes e áreas de melhoria baseada nos 15 critérios.",
    "analysis": {{
        "clarity_problem": "Análise sobre clareza do problema, pertinência, alinhamento. Cite evidências e indique nível implicitamente.",
        "inovation_grade": "Análise sobre inovação, originalidade, diferenciação, tecnologias. Cite evidências.",
        "social_impact": "Análise sobre impacto social/ambiental, sustentabilidade, melhoria. Cite evidências.",
        "tec_eco_viability": "Análise sobre viabilidade técnica/econômica, modelo de valor, escalabilidade. Cite evidências.",
        "application_potencial": "Análise sobre aplicação, contexto, clientes, indicadores. Cite evidências."
    }},
    "resums": {{
        "clarity_resum": "Resumo em 2-3 frases: problema, pertinência, alinhamento.",
        "inovation_grade_resum": "Resumo em 2-3 frases: inovação, diferenciação, tecnologias.",
        "social_impact_resum": "Resumo em 2-3 frases: impacto, sustentabilidade, melhoria.",
        "tec_eco_viability_resum": "Resumo em 2-3 frases: viabilidade, modelo, escalabilidade.",
        "application_potencial_resum": "Resumo em 2-3 frases: aplicação, contexto, indicadores."
    }}
}}

Avalie com base nas evidências do texto, considere todos os 15 critérios agrupados nos 5 campos acima.
    """

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

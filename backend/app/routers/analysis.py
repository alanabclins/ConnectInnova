import json
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException
from google import genai

from app.config.config import settings
from ..prompt_template import build_evaluation_prompt
from app.models.feedback import Feedback
from app.models.projects import Project
from app.models.users import User
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




# response_model=schemas.Token
# response_model=schemas.Token
@router.get("/{project_uuid}")
async def analyze_project(project_uuid: UUID):
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
        'social_impact': project.social_impact_agreggated,
        'tec_eco_viability': project.tec_eco_viability,
        'application_potencial': project.application_potencial
    }
    
    prompt = build_evaluation_prompt(project_data)
    
    # 4️⃣ Envia para o Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", # Recomendo usar um modelo mais robusto como gemini-1.5-pro-latest se o JSON falhar
            contents=prompt,
        )
        ai_raw = getattr(response, "text", None)
        if not ai_raw or ai_raw.strip() == "":
            raise HTTPException(
                status_code=500,
                detail="O Gemini não retornou nenhum texto.",
            )
        
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
                detail=f"Resposta JSON inválido. Erro: {str(e)} | {cleaned_response[:500]}",
            )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Erro na API Gemini: {e}")
    
    # 5️⃣ Valida o formato
    if not ai_data:
        print(ai_data)
        raise HTTPException(
            status_code=500, detail="❌ Resposta da IA em formato inválido ou incompleto."
        )

    # 6️⃣ Cria Feedback (AGORA CORRIGIDO)
    
    # Primeiro, pegue os objetos principais da resposta da IA
    criteria_eval_data = ai_data.get("criteria_evaluation", {})
    full_feedback_content = ai_data.get("full_feedback", "")

    # Agora, extraia os feedbacks específicos DE DENTRO do criteria_evaluation
    # Você precisa decidir qual critério da rubrica corresponde a qual campo do seu BD.
    # Abaixo está um *exemplo* de mapeamento. Ajuste as chaves (ex: "proposta_de_valor")
    # para corresponder aos critérios que você quer salvar.
    
    fb_clarity = criteria_eval_data.get("proposta_de_valor", {}).get("feedback", "")
    fb_innovation = criteria_eval_data.get("originalidade", {}).get("feedback", "")
    fb_social = criteria_eval_data.get("impacto_social_ambiental", {}).get("feedback", "")
    fb_viability = criteria_eval_data.get("sustentabilidade", {}).get("feedback", "") # Ex: Mapeando para sustentabilidade
    fb_potential = criteria_eval_data.get("escalabilidade", {}).get("feedback", "") # Ex: Mapeando para escalabilidade
    
    # Se 'clarity_problem' for a média de 2 critérios, você pode concatenar:
    # fb_clarity_p1 = criteria_eval_data.get("proposta_de_valor", {}).get("feedback", "")
    # fb_clarity_p2 = criteria_eval_data.get("pertinencia_ao_problema", {}).get("feedback", "")
    # fb_clarity = f"Proposta: {fb_clarity_p1} | Pertinência: {fb_clarity_p2}"
    

    feedback_schema = FeedbackSchema(
        project_id=project.uuid,
        student_id=student.uuid,
        
        # Agora sim, use as strings que acabamos de extrair:
        ai_feedback_clarity_problem=fb_clarity,
        ai_feedback_inovation_grade=fb_innovation,
        ai_feedback_social_impact=fb_social,
        ai_feedback_tec_eco_viability=fb_viability,
        ai_feedback_application_potencial=fb_potential,
        
        criteria_evaluation=criteria_eval_data,  # Salva o objeto completo com os 15 critérios
        feedback_content=full_feedback_content   # Salva o resumo geral
    )
    
    feedback_doc = Feedback(**feedback_schema.model_dump())
    await feedback_doc.create()
    
    # 8️⃣ Retorna para o front
    return {
        "message": "✅ Análise concluída com sucesso!",
        "feedback_id": str(feedback_doc.uuid),
        "feedback_summary": full_feedback_content, # Retorna o resumo geral
        "criteria_evaluation": criteria_eval_data, # Retorna a avaliação detalhada
    }
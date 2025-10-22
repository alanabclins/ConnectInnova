import json
from uuid import UUID
from typing import Any, Dict, Optional, Tuple
from fastapi import APIRouter, HTTPException, Query
from google import genai
from beanie.operators import Eq

from app.config.config import settings
from app.models.feedback import Feedback
from app.models.projects import Project
from app.models.users import User
from app.schemas import FeedbackSchema, CriteriaEvaluationContainer, ProjectAnalysisResponse
from app.routers.ai_config.prompt_template import build_evaluation_prompt

router = APIRouter(tags=["analysis"])

if not settings.GEMINI_API_KEY:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi configurada.")
client = genai.Client(api_key=settings.GEMINI_API_KEY)


def _clean_and_load_gemini_response(ai_raw: str) -> Dict[str, Any]:
    if not ai_raw or ai_raw.strip() == "":
        raise ValueError("O Gemini não retornou nenhum texto.")

    cleaned_response = (
        ai_raw.strip()
        .removeprefix("```json")
        .removeprefix("```JSON")
        .removeprefix("```")
        .removesuffix("```")
        .strip()
    )

    try:
        return json.loads(cleaned_response)
    except json.JSONDecodeError:
        last_brace = cleaned_response.rfind("}")
        if last_brace != -1:
            try:
                return json.loads(cleaned_response[: last_brace + 1])
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Invalid JSON response, even after heuristic correction: {str(e)}"
                )
        raise


def _extract_and_safe_convert(
    data: Dict[str, Any], criteria_key: str, value_key: str
) -> Optional[str]:
    value = data.get(criteria_key, {}).get(value_key)
    return str(value) if value is not None else None


async def _generate_and_save_analysis(
    project: Project, student: User, existing_feedback: Optional[Feedback] = None
) -> Dict[str, Any]:
    project_data = {
        "project_title": project.project_title,
        "project_description": project.project_description,
        "solution_proposal": project.solution_proposal,
        "clarity_problem": project.clarity_problem,
        "inovation_grade": project.inovation_grade,
        "social_impact": project.social_impact_aggregated,
        "tec_eco_viability": project.tec_eco_viability,
        "application_potencial": project.application_potencial,
    }

    prompt = build_evaluation_prompt(project_data)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        ai_raw = getattr(response, "text")
        ai_data = _clean_and_load_gemini_response(ai_raw)
    except (ValueError, json.JSONDecodeError) as e:
        error_detail = f"Invalid JSON response. Error: {type(e).__name__} | {str(e)}"
        raise HTTPException(status_code=500, detail=error_detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {e}")

    criteria_eval_data = ai_data.get("criteria_evaluation", {})
    full_feedback_content = ai_data.get("full_feedback", "")

    if not isinstance(criteria_eval_data, dict) or not isinstance(full_feedback_content, str):
        raise HTTPException(
            status_code=500, detail="AI response in invalid or incomplete format."
        )

    fb_clarity = _extract_and_safe_convert(
        criteria_eval_data, "proposta_de_valor", "feedback"
    )
    fb_innovation = _extract_and_safe_convert(criteria_eval_data, "originalidade", "feedback")
    fb_social = _extract_and_safe_convert(
        criteria_eval_data, "impacto_social_ambiental", "feedback"
    )
    fb_viability = _extract_and_safe_convert(
        criteria_eval_data, "sustentabilidade", "feedback"
    )
    fb_potential = _extract_and_safe_convert(criteria_eval_data, "escalabilidade", "feedback")

    def _get_safe_int_level(criteria_key: str) -> Optional[int]:
        level_str = _extract_and_safe_convert(criteria_eval_data, criteria_key, "level")
        try:
            return int(level_str) if level_str is not None else None
        except ValueError:
            return None

    fb_clarity_level = _get_safe_int_level("proposta_de_valor")
    fb_innovation_level = _get_safe_int_level("originalidade")
    fb_social_level = _get_safe_int_level("impacto_social_ambiental")
    fb_viability_level = _get_safe_int_level("sustentabilidade")
    fb_potencial_level = _get_safe_int_level("escalabilidade")

    try:
        validated_criteria = CriteriaEvaluationContainer(**criteria_eval_data)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Schema validation failed for AI response: {e}"
        )

    feedback_payload = FeedbackSchema(
        project_id=project.uuid,
        student_id=student.uuid,
        ai_feedback_clarity_problem=fb_clarity,
        ai_feedback_clarity_problem_level=fb_clarity_level,
        ai_feedback_inovation_grade=fb_innovation,
        ai_feedback_innovation_grade_level=fb_innovation_level,
        ai_feedback_social_impact=fb_social,
        ai_feedback_social_impact_level=fb_social_level,
        ai_feedback_tec_eco_viability=fb_viability,
        ai_feedback_tec_eco_viability_level=fb_viability_level,
        ai_feedback_application_potencial=fb_potential,
        ai_feedback_application_potencial_level=fb_potencial_level,
        criteria_evaluation=validated_criteria,
        feedback_content=full_feedback_content,
    )

    feedback_data_to_set = feedback_payload.model_dump(exclude_unset=True, by_alias=True)

    if existing_feedback is not None:
        await existing_feedback.set(feedback_data_to_set)
        feedback_doc = existing_feedback
    else:
        feedback_doc = Feedback(**feedback_data_to_set)
        await feedback_doc.insert()

    return {
        "message": "Analysis completed and successfully saved/updated!",
        "feedback_id": str(feedback_doc.uuid),
        "feedback_summary": full_feedback_content,
        "criteria_evaluation": criteria_eval_data,
    }


@router.get("/{project_uuid}", response_model=ProjectAnalysisResponse)
async def analyze_project(
    project_uuid: UUID,
    regenerate: Optional[bool] = Query(
        False,
        alias="regenerate",
        description="Force regeneration of the AI analysis, even if one is already saved.",
    ),
) -> Dict[str, Any]:
    project = await Project.find_one(Eq(Project.uuid, project_uuid))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found.")

    student = await User.find_one(Eq(User.uuid, project.student_id))
    if student is None:
        raise HTTPException(status_code=404, detail="Linked student not found.")

    existing_feedback = await Feedback.find_one(Eq(Feedback.project_id, project_uuid))

    if existing_feedback is not None and not regenerate:

        criteria_model = existing_feedback.criteria_evaluation

        if criteria_model is None:
            return await _generate_and_save_analysis(project, student, existing_feedback)

        criteria_eval_data = criteria_model.model_dump()

        return {
            "message": "Existing analysis found. Returning cached data.",
            "feedback_id": str(existing_feedback.uuid),
            "feedback_summary": existing_feedback.feedback["content"],
            "criteria_evaluation": criteria_eval_data,
        }
    return await _generate_and_save_analysis(project, student, existing_feedback)

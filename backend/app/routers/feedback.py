import json
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from beanie.operators import Eq
from fastapi import APIRouter, Depends, HTTPException, Query
from google import genai

from app.config.config import settings
from app.routers.ai_config import prompt_template
from app.schemas import (
    CriteriaEvaluationContainer,
    FeedbackCreateUpdate,
    ProjectAnalysisResponse,
)

from .. import models
from ..auth.auth import get_current_active_user

if not settings.GEMINI_API_KEY:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi configurada.")
client = genai.Client(api_key=settings.GEMINI_API_KEY)


class AnalysisFeedbackService:
    @staticmethod
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

    @classmethod
    async def generate_and_save_analysis(
        cls,
        project: models.Project,
        student: models.User,
        existing_feedback: Optional[models.Feedback] = None,
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

        prompt = prompt_template.build_evaluation_prompt(project_data)

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            ai_raw = getattr(response, "text")
            ai_data = cls._clean_and_load_gemini_response(ai_raw)
        except Exception as e:
            error_detail = f"Gemini/JSON Error: {type(e).__name__} | {e}"
            raise HTTPException(status_code=500, detail=error_detail)

        criteria_eval_data = ai_data.get("criteria_evaluation", {})
        full_feedback_content = ai_data.get("full_feedback", "")

        if not isinstance(criteria_eval_data, dict) or not isinstance(
            full_feedback_content, str
        ):
            raise HTTPException(
                status_code=500, detail="AI response in invalid or incomplete format."
            )

        try:
            validated_criteria = CriteriaEvaluationContainer(**criteria_eval_data)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Schema validation failed for AI response: {e}"
            )

        feedback_payload = FeedbackCreateUpdate(
            project_id=project.uuid,
            student_id=student.uuid,
            feedback_content=full_feedback_content,
            criteria_evaluation=validated_criteria,
        )

        feedback_data_to_set = feedback_payload.model_dump(exclude_unset=True, by_alias=True)
        feedback_data_to_set["feedback"] = {
            "content": feedback_data_to_set.pop("feedback_content"),
            "status": "generated",
            "timestamp": datetime.now(UTC),
        }

        if existing_feedback is not None:
            await existing_feedback.set(feedback_data_to_set)
            feedback_doc = existing_feedback
        else:
            feedback_doc = models.Feedback(**feedback_data_to_set)
            await feedback_doc.insert()

        return {
            "message": "Analysis completed and successfully saved/updated!",
            "feedback_id": feedback_doc.uuid,
            "feedback_summary": full_feedback_content,
            "criteria_evaluation": criteria_eval_data,
        }


router = APIRouter()


@router.post(
    "/{project_uuid}",
    response_model=ProjectAnalysisResponse,
    summary="Generate or Retrieve Project Analysis",
)
async def analyze_project_endpoint(
    project_uuid: UUID,
    regenerate: Optional[bool] = Query(
        False, description="Force regeneration of the AI analysis."
    ),
) -> Dict[str, Any]:
    project = await models.Project.find_one(Eq(models.Project.uuid, project_uuid))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found.")

    student = await models.User.find_one(Eq(models.User.uuid, project.student_id))
    if student is None:
        raise HTTPException(status_code=404, detail="Linked student not found.")

    existing_feedback = await models.Feedback.find_one(
        Eq(models.Feedback.project_id, project_uuid)
    )

    if existing_feedback is not None and not regenerate:
        criteria_model = existing_feedback.criteria_evaluation

        if criteria_model is None:
            return await AnalysisFeedbackService.generate_and_save_analysis(
                project, student, existing_feedback
            )

        criteria_eval_data = criteria_model.model_dump()

        return {
            "message": "Existing analysis found. Returning cached data.",
            "feedback_id": existing_feedback.uuid,
            "feedback_summary": existing_feedback.feedback.get("content", ""),
            "criteria_evaluation": criteria_eval_data,
        }

    return await AnalysisFeedbackService.generate_and_save_analysis(
        project, student, existing_feedback
    )


@router.get(
    "/{project_uuid}", response_model=models.Feedback, summary="Get Feedback/Analysis by UUID"
)
async def get_feedback_by_uuid(
    project_uuid: UUID, current_user: models.User = Depends(get_current_active_user)
) -> models.Feedback:
    feedback_doc = await models.Feedback.find_one(
        Eq(models.Feedback.project_id, project_uuid)
    )

    # Verificar se o projeto existe
    project = await models.Project.find_one(
        models.Project.uuid == project_uuid
    )

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found.")
    
    # Verificar a autorização antes de mostrar qualquer coisa
    if project.student_id != current_user.uuid:
        raise HTTPException(status_code=403, detail="Not authorized.")
    
    if feedback_doc is None:
        raise HTTPException(status_code=404, detail="Analysis/Feedback not found.")

    return feedback_doc


@router.get(
    "/user/all",
    response_model=List[models.Feedback],
    summary="List all Analyses for the current User",
)
async def list_user_analyses(
    current_user: models.User = Depends(get_current_active_user),
) -> List[models.Feedback]:
    """Retorna a lista de todos os feedbacks/análises vinculados ao usuário logado."""
    feedbacks = await models.Feedback.find(
        Eq(models.Feedback.student_id, current_user.uuid)
    ).to_list()

    return feedbacks

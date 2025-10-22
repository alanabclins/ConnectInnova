from datetime import UTC, datetime
from typing import Annotated, Optional
from uuid import UUID, uuid4

from app.schemas.feedback import CriteriaEvaluationContainer
from beanie import Document, Indexed
from pydantic import Field, BaseModel

class Feedback(Document):
    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)] = Field(
        default_factory=uuid4
    )
    project_id: Optional[UUID] = None
    student_id: Optional[UUID] = None

    feedback: dict = Field(
        default_factory=lambda: {"content": "", "status": "", "timestamp": datetime.now(UTC)}
    )

    ai_feedback_clarity_problem: Optional[str] = None
    ai_feedback_clarity_problem_level: Optional[int] = None
    ai_feedback_inovation_grade: Optional[str] = None
    ai_feedback_inovation_grade_level: Optional[int] = None
    ai_feedback_social_impact: Optional[str] = None
    ai_feedback_social_impact_level: Optional[int] = None
    ai_feedback_tec_eco_viability: Optional[str] = None
    ai_feedback_tec_eco_viability_level: Optional[int] = None
    ai_feedback_application_potencial: Optional[str] = None
    ai_feedback_application_potencial_level: Optional[int] = None

    criteria_evaluation: Optional[CriteriaEvaluationContainer] = None

    class Settings:
        name = "Feedback"

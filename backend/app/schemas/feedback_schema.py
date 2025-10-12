from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class FeedbackSchema(BaseModel):
    project_id: UUID
    student_id: UUID
    feedback_content: str = Field(description="Texto completo do feedback gerado pela IA")
    ai_feedback_clarity_problem: Optional[str] = None
    ai_feedback_inovation_grade: Optional[str] = None
    ai_feedback_social_impact: Optional[str] = None
    ai_feedback_tec_eco_viability: Optional[str] = None
    ai_feedback_application_potencial: Optional[str] = None

    # >>> Corrigido: passe um callable (lambda) como default_factory
    timestamp: datetime = Field(default_factory=lambda: datetime.utcnow())

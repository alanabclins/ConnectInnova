from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID, uuid4

from beanie import Document, Indexed, Link
from pydantic import Field

from .projects import Project
from .student import Student


class Feedback(Document):
    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)] = Field(
        default_factory=uuid4
    )
    project: Link[Project]
    student: Optional[Link[Student]] = None

    feedback: dict = Field(
        default_factory=lambda: {"content": "", "status": "", "timestamp": datetime.utcnow()}
    )

    ai_feedback_clarity_problem: Optional[str] = None
    ai_feedback_inovation_grade: Optional[str] = None
    ai_feedback_social_impact: Optional[str] = None
    ai_feedback_tec_eco_viability: Optional[str] = None
    ai_feedback_application_potencial: Optional[str] = None

    class Settings:
        name = "Feedback"

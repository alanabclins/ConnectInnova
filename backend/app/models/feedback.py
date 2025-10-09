from typing import Annotated, Optional
from uuid import UUID, uuid4
from datetime import datetime
from beanie import Document, Indexed, Link
from pydantic import Field
from .student import Student
from .project import Project


class Feedback(Document):
    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)]
    project_id: Link[Project]
    student_id: Optional[Link[Student]] = None

    feedback: dict = Field(
        default_factory=lambda: {
            "content": "",
            "status": "",
            "timestamp": datetime.utcnow()
        }
    )

    ai_feedback_clarity_problem: Optional[str] = None
    ai_feedback_inovation_grade: Optional[str] = None
    ai_feedback_social_impact: Optional[str] = None
    ai_feedback_tec_eco_viability: Optional[str] = None
    ai_feedback_application_potencial: Optional[str] = None

    class Settings:
        name = "Feedback"

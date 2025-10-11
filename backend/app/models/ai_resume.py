from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID, uuid4

from beanie import Document, Indexed, Link
from pydantic import Field

from .projects import Project
from .student import Student


class AIResum(Document):
    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)] = Field(
        default_factory=uuid4
    )
    project_id: Link[Project]
    student_id: Link[Student]

    clarity_resum: str
    inovation_grade_resum: str
    social_impact_resum: str
    tec_eco_viability_resum: str
    application_potencial_resum: str

    summary: dict = Field(
        default_factory=lambda: {"content": "", "status": "", "timestamp": datetime.now(UTC)}
    )

    class Settings:
        name = "AI_Resum"

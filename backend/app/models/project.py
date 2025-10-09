from typing import Annotated, Optional
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link
from pydantic import Field
from .student import Student


class Project(Document):
    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)]
    project_title: str
    project_description: str
    solution_proposal: str
    student_id: Link[Student]

    clarity_problem: Optional[str] = None
    inovation_grade: Optional[str] = None
    social_impact: Optional[str] = None
    tec_eco_viability: Optional[str] = None
    application_potencial: Optional[str] = None

    class Settings:
        name = "Projects"

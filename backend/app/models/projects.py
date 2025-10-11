from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from beanie import Document, Indexed, PydanticObjectId
from bson import ObjectId
from pydantic import Field


class Project(Document):
    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)] = Field(
        default_factory=uuid4
    )
    project_title: str
    project_description: str
    solution_proposal: str
    clarity_problem: str
    inovation_grade: str
    social_impact: str
    tec_eco_viability: str
    application_potencial: str
    student_id: PydanticObjectId
    timestamp: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "Projetos"  # nome da coleção no MongoDB

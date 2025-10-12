from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field


class AIResum(Document):
    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)] = Field(default_factory=uuid4)
    project_id: UUID
    student_id: UUID
    clarity_resum: str
    inovation_grade_resum: str
    social_impact_resum: str
    tec_eco_viability_resum: str
    application_potencial_resum: str
    timestamp: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "AIResum"

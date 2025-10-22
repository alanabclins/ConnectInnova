from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field


class Project(Document):
    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)] = Field(
        default_factory=uuid4
    )

    project_title: str
    project_description: str
    solution_proposal: str

    problem_description: Optional[str] = None
    target_audience: Optional[str] = None
    value_proposition: Optional[str] = None
    customer_segment: Optional[str] = None
    revenue_model: Optional[str] = None
    competitive_advantage: Optional[str] = None

    innovation: Optional[str] = None
    social_impact: Optional[str] = None
    technical_feasibility: Optional[str] = None
    scalability: Optional[str] = None

    who_are_you: Optional[str] = None
    academy_info: Optional[str] = None
    market_info: Optional[str] = None

    clarity_problem: str
    inovation_grade: str
    social_impact_aggregated: str
    tec_eco_viability: str
    application_potencial: str

    student_id: UUID
    timestamp: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "Projetos"

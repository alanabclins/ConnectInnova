from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field


class Project(Document):
    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)] = Field(
        default_factory=uuid4
    )
    
    # Informações Básicas
    project_title: str
    project_description: str
    solution_proposal: str
    
    # Campos Novos - Problema e Proposta de Valor
    problem_description: Optional[str] = Field(default="")
    target_audience: Optional[str] = Field(default="")
    value_proposition: Optional[str] = Field(default="")
    
    # Campos Novos - Lean Canvas
    customer_segment: Optional[str] = Field(default="")
    revenue_model: Optional[str] = Field(default="")
    competitive_advantage: Optional[str] = Field(default="")
    
    # Campos Novos - Inovação e Impacto
    innovation: Optional[str] = Field(default="")
    social_impact: Optional[str] = Field(default="")
    technical_feasibility: Optional[str] = Field(default="")
    scalability: Optional[str] = Field(default="")
    
    # Campos Novos - Informações Pessoais (Step 5)
    who_are_you: Optional[str] = Field(default="")
    academy_info: Optional[str] = Field(default="")
    market_info: Optional[str] = Field(default="")
    
    # Campos Agregados (gerados automaticamente pelo backend)
    clarity_problem: str
    inovation_grade: str
    social_impact_aggregated: str
    tec_eco_viability: str
    application_potencial: str
    
    # Metadata
    student_id: UUID
    timestamp: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "Projetos"  # nome da coleção no MongoDB

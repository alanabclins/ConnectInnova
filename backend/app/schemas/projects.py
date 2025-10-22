from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    project_title: str = Field(description="Título formal do projeto.")
    project_description: str = Field(description="Descrição detalhada e contexto do projeto.")
    solution_proposal: str = Field(
        description="Proposta de solução ou produto central do projeto."
    )

    problem_description: Optional[str] = Field(
        description="O desafio ou dor que a solução busca resolver."
    )
    target_audience: Optional[str] = Field(description="Público-alvo primário da solução.")
    value_proposition: Optional[str] = Field(
        description="O valor único e os benefícios entregues ao cliente."
    )

    customer_segment: Optional[str] = Field(
        description="Segmento de clientes que será atendido."
    )
    revenue_model: Optional[str] = Field(
        description="Como o projeto pretende gerar receita e ser economicamente sustentável."
    )
    competitive_advantage: Optional[str] = Field(
        description="O diferencial sustentável da solução em relação aos concorrentes."
    )

    innovation: Optional[str] = Field(
        description="Detalhes sobre a inovação ou o aprimoramento tecnológico introduzido."
    )
    social_impact: Optional[str] = Field(
        description="O benefício concreto para a sociedade ou o meio ambiente."
    )
    technical_feasibility: Optional[str] = Field(
        description="Análise da viabilidade técnica para a implementação da solução."
    )
    scalability: Optional[str] = Field(
        description="Potencial e plano de crescimento e replicação da solução."
    )

    who_are_you: Optional[str] = Field(
        description="Descrição da sua trajetória, papel no projeto e motivações."
    )
    academy_info: Optional[str] = Field(
        description="Contexto e informações sobre sua formação acadêmica."
    )
    market_info: Optional[str] = Field(
        description="Experiência profissional relevante e visão de mercado."
    )

    clarity_problem: Optional[str] = Field(
        default=None,
        description="Campo agregado legado (substituído por problem_description, target_audience, value_proposition).",
    )
    inovation_grade: Optional[str] = Field(
        default=None, description="Campo agregado legado (substituído por innovation)."
    )
    social_impact_aggregated: Optional[str] = Field(
        default=None, description="Campo agregado legado (substituído por social_impact)."
    )
    tec_eco_viability: Optional[str] = Field(
        default=None,
        description="Campo agregado legado (substituído por technical_feasibility, revenue_model, scalability).",
    )
    application_potencial: Optional[str] = Field(
        default=None,
        description="Campo agregado legado (substituído por customer_segment, competitive_advantage).",
    )


class ProjectReturn(BaseModel):
    uuid: UUID
    project_title: str
    project_description: str
    solution_proposal: str
    problem_description: Optional[str]
    target_audience: Optional[str]
    value_proposition: Optional[str]
    customer_segment: Optional[str]
    revenue_model: Optional[str]
    competitive_advantage: Optional[str]
    innovation: Optional[str]
    social_impact: Optional[str]
    technical_feasibility: Optional[str]
    scalability: Optional[str]
    who_are_you: Optional[str]
    academy_info: Optional[str]
    market_info: Optional[str]
    clarity_problem: str
    inovation_grade: str
    social_impact_aggregated: str
    tec_eco_viability: str
    application_potencial: str
    student_id: UUID
    timestamp: datetime


class ProjectResponse(BaseModel):
    message: str = Field(
        ..., description="Mensagem de status confirmando o cadastro do projeto."
    )
    project_id_mongo: str = Field(
        ..., description="ID interno do MongoDB do documento criado."
    )
    project_uuid: UUID = Field(
        ..., description="UUID único do projeto, usado para recuperação e análise."
    )
    timestamp: datetime = Field(description="Carimbo de data/hora da criação do registro.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Projeto cadastrado com sucesso!",
                    "project_id_mongo": "651a37c0f0a4f6d89b1c7c9c",
                    "project_uuid": "f1e2d3c4-b5a6-7890-1234-567890abcdef",
                    "timestamp": "2025-10-22T16:00:00.000000",
                }
            ]
        }
    }

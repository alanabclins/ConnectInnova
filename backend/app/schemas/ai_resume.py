from uuid import UUID
from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime


class ResumDetail(BaseModel):
    clarity_resum: str = Field(..., description="Resumo da clareza do problema e solução.")
    inovation_grade_resum: str = Field(
        ..., description="Resumo do nível de inovação/originalidade do projeto."
    )
    social_impact_resum: str = Field(
        ..., description="Resumo do impacto social ou ambiental."
    )
    tec_eco_viability_resum: str = Field(
        ..., description="Resumo da viabilidade técnica e econômica."
    )
    application_potencial_resum: str = Field(
        ..., description="Resumo do potencial de aplicabilidade/mercado."
    )


class AIResumResponse(BaseModel):
    message: str = Field(
        ...,
        description="Mensagem de status da operação.",
    )
    resum_id: UUID = Field(
        ..., description="UUID do documento de resumo salvo no banco de dados."
    )
    resums: ResumDetail = Field(
        ..., description="Objeto contendo o resumo de cada critério chave do projeto."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Resumo gerado com sucesso!",
                    "resum_id": "f1e2d3c4-a1b2-c3d4-e5f6-1234567890ab",
                    "resums": {
                        "clarity_resum": "A proposta é concisa, focando em soluções acessíveis para o monitoramento de energia.",
                        "inovation_grade_resum": "Inovação reside na simplicidade, contrastando com soluções de alto custo.",
                        "social_impact_resum": "Alto potencial de conscientização e economia para comunidades de baixa renda.",
                        "tec_eco_viability_resum": "Viabilidade excelente devido à não dependência de hardware proprietário.",
                        "application_potencial_resum": "Grande potencial de escalabilidade e replicação em múltiplos contextos urbanos.",
                    },
                }
            ]
        }
    }


class AIResumSchema(BaseModel):
    project_id: UUID
    student_id: UUID
    clarity_resum: str
    inovation_grade_resum: str
    social_impact_resum: str
    tec_eco_viability_resum: str
    application_potencial_resum: str
    timestamp: datetime = Field(default_factory=datetime.now)

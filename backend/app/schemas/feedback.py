from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CriterionDetail(BaseModel):
    level: int = Field(
        ..., description="Nível de pontuação do critério (1: Ruim, 2: Médio, 3: Bom)."
    )
    label: str = Field(..., description="Rótulo qualitativo do nível (ex: 'Bom').")
    feedback: str = Field(..., description="Feedback detalhado da IA sobre este critério.")


class CriteriaEvaluationContainer(BaseModel):
    proposta_de_valor: CriterionDetail
    pertinencia_ao_problema: CriterionDetail
    alinhamento_com_objetivos: CriterionDetail
    adequacao_ao_contexto: CriterionDetail
    originalidade: CriterionDetail
    capacidade_de_diferenciacao: CriterionDetail
    uso_inteligente_tecnologias: CriterionDetail
    impacto_social_ambiental: CriterionDetail
    escalabilidade: CriterionDetail
    sustentabilidade: CriterionDetail
    indicadores_de_sucesso: CriterionDetail
    capacidade_de_melhoria: CriterionDetail
    segmento_de_clientes: CriterionDetail
    modelo_geracao_valor: CriterionDetail
    vantagem_competitiva: CriterionDetail


class FeedbackSchema(BaseModel):
    project_id: UUID
    student_id: UUID
    feedback_content: str = Field(
        description="Texto completo do resumo geral do feedback gerado pela IA."
    )

    ai_feedback_clarity_problem: Optional[str] = None
    ai_feedback_clarity_problem_level: Optional[int] = None
    ai_feedback_inovation_grade: Optional[str] = None
    ai_feedback_innovation_grade_level: Optional[int] = None
    ai_feedback_social_impact: Optional[str] = None
    ai_feedback_social_impact_level: Optional[int] = None
    ai_feedback_tec_eco_viability: Optional[str] = None
    ai_feedback_tec_eco_viability_level: Optional[int] = None
    ai_feedback_application_potencial: Optional[str] = None
    ai_feedback_application_potencial_level: Optional[int] = None

    criteria_evaluation: Optional[CriteriaEvaluationContainer] = Field(
        default=None,
        description="Avaliação detalhada dos 15 critérios (level, label, feedback) conforme a rubrica.",
    )

    timestamp: datetime = Field(default_factory=datetime.now)


class ProjectAnalysisResponse(BaseModel):
    message: str = Field(..., description="Mensagem de status da operação.")
    feedback_id: UUID = Field(
        ..., description="UUID do documento de feedback salvo no banco de dados."
    )
    feedback_summary: str = Field(
        ..., description="Resumo executivo do projeto gerado pela IA."
    )
    criteria_evaluation: CriteriaEvaluationContainer = Field(
        ...,
        description="Objeto contendo a avaliação detalhada e validada de todos os 15 critérios.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Análise concluída com sucesso!",
                    "feedback_id": "1b7c3a42-9261-4556-b8db-3b107ddfa173",
                    "feedback_summary": "O projeto demonstra uma proposta de valor bem definida, mas apresenta lacunas críticas em relação à sustentabilidade.",
                    "criteria_evaluation": {
                        "proposta_de_valor": {
                            "level": 3,
                            "label": "Bom",
                            "feedback": "A proposta de valor é clara.",
                        },
                        "pertinencia_ao_problema": {
                            "level": 3,
                            "label": "Bom",
                            "feedback": "A solução é altamente pertinente.",
                        },
                        "sustentabilidade": {
                            "level": 1,
                            "label": "Ruim",
                            "feedback": "Não há plano financeiro de longo prazo.",
                        },
                        # ... e os outros 12 critérios restantes
                    },
                }
            ]
        }
    }

from datetime import datetime
from typing import Optional
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


class FeedbackCreateUpdate(BaseModel):
    """Schema para criar ou atualizar o documento de Feedback no DB."""
    project_id: UUID
    student_id: UUID
    feedback_content: str = Field(
        description="Texto completo do resumo geral do feedback gerado pela IA."
    )
    criteria_evaluation: Optional[CriteriaEvaluationContainer] = Field(
        default=None,
        description="Avaliação detalhada dos 15 critérios (level, label, feedback) conforme a rubrica.",
    )


class ProjectAnalysisResponse(BaseModel):
    """Schema de resposta para o endpoint de análise de projeto."""
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
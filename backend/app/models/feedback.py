from datetime import UTC, datetime
from typing import Annotated, Optional
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field

from app.schemas.feedback import CriteriaEvaluationContainer


class Feedback(Document):
    """Documento de Feedback unificado para análise de IA e histórico."""

    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)] = Field(
        default_factory=uuid4
    )
    project_id: Optional[UUID] = Field(None)
    student_id: Optional[UUID] = Field(None)

    # O campo 'feedback' armazena o resumo e metadados
    feedback: dict = Field(
        default_factory=lambda: {
            "content": "",
            "status": "draft",
            "timestamp": datetime.now(UTC),
        },
        description="Contém o resumo (content), status e data de criação/atualização.",
    )

    # O campo principal para o resultado da análise detalhada
    criteria_evaluation: Optional[CriteriaEvaluationContainer] = Field(
        None, description="Avaliação detalhada dos 15 critérios."
    )

    class Settings:
        name = "Feedback"

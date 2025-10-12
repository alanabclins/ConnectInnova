from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AIResumSchema(BaseModel):
    project_id: UUID
    student_id: UUID
    clarity_resum: Optional[str] = None
    inovation_grade_resum: Optional[str] = None
    social_impact_resum: Optional[str] = None
    tec_eco_viability_resum: Optional[str] = None
    application_potencial_resum: Optional[str] = None

    # >>> Corrigido: passe um callable (lambda) como default_factory
    timestamp: datetime = Field(default_factory=lambda: datetime.utcnow())

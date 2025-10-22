from typing import Optional
from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    # Informações Básicas
    project_title: str
    project_description: str
    solution_proposal: str
    
    # Problema e Proposta de Valor
    problem_description: Optional[str] = Field(default="", description="Descrição detalhada do problema")
    target_audience: Optional[str] = Field(default="", description="Público-alvo")
    value_proposition: Optional[str] = Field(default="", description="Proposta de valor")
    
    # Lean Canvas - Modelo de Negócio
    customer_segment: Optional[str] = Field(default="", description="Segmento de clientes")
    revenue_model: Optional[str] = Field(default="", description="Modelo de receita")
    competitive_advantage: Optional[str] = Field(default="", description="Vantagem competitiva")
    
    # Inovação e Impacto
    innovation: Optional[str] = Field(default="", description="Grau de inovação")
    social_impact: Optional[str] = Field(default="", description="Impacto social/ambiental")
    technical_feasibility: Optional[str] = Field(default="", description="Viabilidade técnica")
    scalability: Optional[str] = Field(default="", description="Escalabilidade")
    
    # Informações Pessoais (Step 5)
    who_are_you: Optional[str] = Field(default="", description="Sobre você - trajetória e experiências")
    academy_info: Optional[str] = Field(default="", description="Informações acadêmicas")
    market_info: Optional[str] = Field(default="", description="Currículo e experiência profissional")
    
    # Campos agregados legados (retrocompatibilidade - aceita se vier do frontend antigo)
    clarity_problem: Optional[str] = Field(default=None)
    inovation_grade: Optional[str] = Field(default=None)
    social_impact_aggregated: Optional[str] = Field(default=None)
    tec_eco_viability: Optional[str] = Field(default=None)
    application_potencial: Optional[str] = Field(default=None)

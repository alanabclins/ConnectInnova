from pydantic import BaseModel


class ProjectCreate(BaseModel):
    project_title: str
    project_description: str
    solution_proposal: str
    student_id: str
    clarity_problem: str
    inovation_grade: str
    social_impact: str
    tec_eco_viability: str
    application_potencial: str

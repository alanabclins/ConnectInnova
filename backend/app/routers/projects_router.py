from bson import ObjectId
from fastapi import APIRouter, HTTPException
from ..models.projects import Project
from pydantic import BaseModel

router = APIRouter(prefix="/projects", tags=["Projects"])


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


@router.post("/")
async def create_project(project: ProjectCreate):
    try:
        project_doc = Project(
            project_title=project.project_title,
            project_description=project.project_description,
            solution_proposal=project.solution_proposal,
            clarity_problem=project.clarity_problem,
            inovation_grade=project.inovation_grade,
            social_impact=project.social_impact,
            tec_eco_viability=project.tec_eco_viability,
            application_potencial=project.application_potencial,
            student_id=ObjectId(project.student_id),
        )

        await project_doc.insert()
        return {
            "message": "✅ Projeto cadastrado com sucesso!",
            "id": str(project_doc.id),
            "timestamp": project_doc.timestamp,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar projeto: {e}")

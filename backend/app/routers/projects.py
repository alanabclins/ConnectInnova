from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from .. import models, schemas
from ..auth.auth import (
    get_current_active_user,
)

router = APIRouter()


@router.post("/")
async def create_project(
    project: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    try:
        project_doc = models.Project(
            project_title=project.project_title,
            project_description=project.project_description,
            solution_proposal=project.solution_proposal,
            clarity_problem=project.clarity_problem,
            inovation_grade=project.inovation_grade,
            social_impact=project.social_impact,
            tec_eco_viability=project.tec_eco_viability,
            application_potencial=project.application_potencial,
            student_id=current_user.uuid,
        )

        await project_doc.insert()
        return {
            "message": "Projeto cadastrado com sucesso!",
            "project_id_mongo": str(project_doc.id),
            "project_uuid": str(project_doc.uuid),
            "timestamp": project_doc.timestamp,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar projeto: {e}")

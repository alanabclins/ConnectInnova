from typing import Any, Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from .. import models, schemas
from ..auth.auth import get_current_active_user

router = APIRouter()


def _aggregate_project_fields(project: schemas.ProjectCreate) -> Dict[str, str]:
    clarity_problem_text = project.clarity_problem or ""
    if not clarity_problem_text and (
        project.problem_description or project.target_audience or project.value_proposition
    ):
        parts = []
        if project.problem_description:
            parts.append(f"Problema: {project.problem_description}")
        if project.target_audience:
            parts.append(f"Público-alvo: {project.target_audience}")
        if project.value_proposition:
            parts.append(f"Proposta de Valor: {project.value_proposition}")
        clarity_problem_text = "\n".join(parts) if parts else ""

    tec_eco_viability_text = project.tec_eco_viability or ""
    if not tec_eco_viability_text and (
        project.technical_feasibility or project.revenue_model or project.scalability
    ):
        parts = []
        if project.technical_feasibility:
            parts.append(f"Viabilidade Técnica: {project.technical_feasibility}")
        if project.revenue_model:
            parts.append(f"Modelo de Receita: {project.revenue_model}")
        if project.scalability:
            parts.append(f"Escalabilidade: {project.scalability}")
        tec_eco_viability_text = "\n".join(parts) if parts else ""

    application_potencial_text = project.application_potencial or ""
    if not application_potencial_text and (
        project.customer_segment or project.competitive_advantage
    ):
        parts = []
        if project.customer_segment:
            parts.append(f"Segmento de Clientes: {project.customer_segment}")
        if project.competitive_advantage:
            parts.append(f"Vantagem Competitiva: {project.competitive_advantage}")
        application_potencial_text = "\n".join(parts) if parts else ""

    return {
        "clarity_problem": clarity_problem_text,
        "inovation_grade": project.inovation_grade or project.innovation or "",
        "social_impact_aggregated": project.social_impact_aggregated
        or project.social_impact
        or "",
        "tec_eco_viability": tec_eco_viability_text,
        "application_potencial": application_potencial_text,
    }


@router.post("/", response_model=schemas.ProjectResponse)
async def create_project(
    project: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    try:
        agg = _aggregate_project_fields(project)

        project_doc = models.Project(
            project_title=project.project_title,
            project_description=project.project_description,
            solution_proposal=project.solution_proposal,
            problem_description=project.problem_description or "",
            target_audience=project.target_audience or "",
            value_proposition=project.value_proposition or "",
            customer_segment=project.customer_segment or "",
            revenue_model=project.revenue_model or "",
            competitive_advantage=project.competitive_advantage or "",
            innovation=project.innovation or "",
            social_impact=project.social_impact or "",
            technical_feasibility=project.technical_feasibility or "",
            scalability=project.scalability or "",
            who_are_you=project.who_are_you or "",
            academy_info=project.academy_info or "",
            market_info=project.market_info or "",
            clarity_problem=agg["clarity_problem"],
            inovation_grade=agg["inovation_grade"],
            social_impact_aggregated=agg["social_impact_aggregated"],
            tec_eco_viability=agg["tec_eco_viability"],
            application_potencial=agg["application_potencial"],
            student_id=current_user.uuid,
        )

        await project_doc.insert()
        return {
            "message": "Projeto cadastrado com sucesso!",
            "project_id_mongo": str(project_doc.id),
            "project_uuid": project_doc.uuid,
            "timestamp": project_doc.timestamp,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar projeto: {e}")


@router.get("/", response_model=List[schemas.ProjectReturn])
async def get_projects(current_user: models.User = Depends(get_current_active_user)) -> Any:
    try:
        projects = await models.Project.find(
            models.Project.student_id == current_user.uuid
        ).to_list()
        return projects
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Erro ao buscar projetos: {e}"
        )


@router.get("/{project_uuid}", response_model=schemas.ProjectReturn)
async def get_project_details(
    project_uuid: str,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    try:
        project_uuid_obj = UUID(project_uuid)
        project = await models.Project.find_one(models.Project.uuid == project_uuid_obj)

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Projeto não encontrado."
            )

        if project.student_id != current_user.uuid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Usuário não autorizado"
            )

        return project

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UUID inválido.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar projeto: {e}",
        )


@router.patch("/{project_uuid}", response_model=schemas.ProjectResponse)
async def update_project(
    project_uuid: str,
    project_update: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    try:
        project_uuid_obj = UUID(project_uuid)
        project = await models.Project.find_one(models.Project.uuid == project_uuid_obj)

        if not project:
            raise HTTPException(status_code=404, detail="Projeto não encontrado.")

        if project.student_id != current_user.uuid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Usuário não autorizado"
            )

        agg = _aggregate_project_fields(project_update)

        update_data = {
            "project_title": project_update.project_title,
            "project_description": project_update.project_description,
            "solution_proposal": project_update.solution_proposal,
            "problem_description": project_update.problem_description or "",
            "target_audience": project_update.target_audience or "",
            "value_proposition": project_update.value_proposition or "",
            "customer_segment": project_update.customer_segment or "",
            "revenue_model": project_update.revenue_model or "",
            "competitive_advantage": project_update.competitive_advantage or "",
            "innovation": project_update.innovation or "",
            "social_impact": project_update.social_impact or "",
            "technical_feasibility": project_update.technical_feasibility or "",
            "scalability": project_update.scalability or "",
            "who_are_you": project_update.who_are_you or "",
            "academy_info": project_update.academy_info or "",
            "market_info": project_update.market_info or "",
            "clarity_problem": agg["clarity_problem"],
            "inovation_grade": agg["inovation_grade"],
            "social_impact_aggregated": agg["social_impact_aggregated"],
            "tec_eco_viability": agg["tec_eco_viability"],
            "application_potencial": agg["application_potencial"],
        }

        await project.set(update_data)

        return {
            "message": "Projeto atualizado com sucesso!",
            "project_id_mongo": str(project.id),
            "project_uuid": project.uuid,
            "timestamp": project.timestamp,
        }

    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UUID inválido.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar projeto: {e}",
        )


@router.delete("/{project_uuid}", response_model=Dict[str, str])
async def delete_project(
    project_uuid: UUID,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    try:
        project_doc = await models.Project.find_one(models.Project.uuid == project_uuid)

        if not project_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado",
            )

        if project_doc.student_id != current_user.uuid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Não autorizado a deletar este projeto",
            )

        await project_doc.delete()

        return {"message": "Projeto deletado com sucesso"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar projeto: {e}",
        )

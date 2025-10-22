from typing import Any, List  # ✅ adicionei List

from fastapi import APIRouter, Depends, HTTPException

from .. import models, schemas
from ..auth.auth import get_current_active_user

router = APIRouter()


@router.post("/")
async def create_project(
    project: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_active_user),
) -> Any:
    try:
        # Agregação automática dos campos (se novos campos vierem, agregar; senão, usar legados)

        # clarity_problem: agrega problema + público + valor
        clarity_problem_text = project.clarity_problem or ""
        if not clarity_problem_text and (
            project.problem_description
            or project.target_audience
            or project.value_proposition
        ):
            parts = []
            if project.problem_description:
                parts.append(f"Problema: {project.problem_description}")
            if project.target_audience:
                parts.append(f"Público-alvo: {project.target_audience}")
            if project.value_proposition:
                parts.append(f"Proposta de Valor: {project.value_proposition}")
            clarity_problem_text = "\n".join(parts) if parts else ""

        # inovation_grade: usa campo innovation ou legado
        inovation_grade_text = project.inovation_grade or project.innovation or ""

        # social_impact_aggregated: usa campo social_impact ou legado
        social_impact_aggregated_text = (
            project.social_impact_aggregated or project.social_impact or ""
        )

        # tec_eco_viability: agrega viabilidade + receita + escalabilidade
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

        # application_potencial: agrega segmento + vantagem
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

        project_doc = models.Project(
            # Básico
            project_title=project.project_title,
            project_description=project.project_description,
            solution_proposal=project.solution_proposal,
            # Campos individuais (novos)
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
            # Informações Pessoais (Step 5)
            who_are_you=project.who_are_you or "",
            academy_info=project.academy_info or "",
            market_info=project.market_info or "",
            # Campos agregados (para o prompt da IA)
            clarity_problem=clarity_problem_text,
            inovation_grade=inovation_grade_text,
            social_impact_aggregated=social_impact_aggregated_text,
            tec_eco_viability=tec_eco_viability_text,
            application_potencial=application_potencial_text,
            # Metadata
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


# Esse GET retorna os projetos do usuário logado
@router.get("/", response_model=List[models.Project])
async def get_projects(current_user: models.User = Depends(get_current_active_user)) -> Any:
    try:
        projects = await models.Project.find(
            models.Project.student_id == current_user.uuid
        ).to_list()
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar projetos: {e}")

# test_projects.py
import pytest
from fastapi import status
from httpx import AsyncClient


from app.config.config import settings
from ..utils import create_test_user, create_test_project


@pytest.mark.anyio
async def test_create_project(client: AsyncClient) -> None:
    # Cria usuário de teste
    student = await create_test_user()

    # Cria projeto associado a esse usuário
    project = await create_test_project(student)

    # Faz POST via API
    payload = {
        "project_title": project.project_title,
        "project_description": project.project_description,
        "solution_proposal": project.solution_proposal,
        "clarity_problem": project.clarity_problem,
        "inovation_grade": project.inovation_grade,
        "social_impact": project.social_impact,
        "tec_eco_viability": project.tec_eco_viability,
        "application_potencial": project.application_potencial,
        "student_id": str(student.id),
    }

    r = await client.post(f"{settings.API_V1_STR}/projects/", json=payload)

    data = r.json()
    assert r.status_code == status.HTTP_200_OK
    assert "✅ Projeto cadastrado com sucesso!" in data["message"]
    assert "id" in data
    assert "timestamp" in data

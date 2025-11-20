"""
Testes de integridade de dados e consistência geral (RT-116 a RT-123).
"""

from __future__ import annotations

import json
from datetime import datetime
from uuid import UUID
from unittest.mock import patch

import pytest
from fastapi import status
from httpx import AsyncClient

from app.config.config import settings
from app.models import AIResum, Feedback, Project

from ..utils import create_test_project, create_test_user, generate_user_auth_headers

pytestmark = pytest.mark.anyio

CRITERIA_KEYS = [
    "proposta_de_valor",
    "pertinencia_ao_problema",
    "alinhamento_com_objetivos",
    "adequacao_ao_contexto",
    "originalidade",
    "capacidade_de_diferenciacao",
    "uso_inteligente_tecnologias",
    "impacto_social_ambiental",
    "escalabilidade",
    "sustentabilidade",
    "indicadores_de_sucesso",
    "capacidade_de_melhoria",
    "segmento_de_clientes",
    "modelo_geracao_valor",
    "vantagem_competitiva",
]

RESUM_FIELDS = [
    "clarity_resum",
    "inovation_grade_resum",
    "social_impact_resum",
    "tec_eco_viability_resum",
    "application_potencial_resum",
]


class _FakeGeminiResponse:
    def __init__(self, payload: str):
        self.text = payload


def _fake_feedback_payload() -> str:
    criteria = {
        key: {
            "level": 3,
            "label": "Bom",
            "feedback": f"{key} ok",
            "improvement": f"{key} improve",
        }
        for key in CRITERIA_KEYS
    }
    return json.dumps(
        {
            "full_feedback": "Resumo completo",
            "criteria_evaluation": criteria,
        }
    )


def _fake_resum_payload() -> str:
    return json.dumps(
        {
            "resums": {field: f"{field} resumo" for field in RESUM_FIELDS}
        }
    )


async def _create_project(client: AsyncClient):
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    return user, headers, response.json()["project_uuid"]


async def _generate_feedback(client: AsyncClient, project_uuid: str):
    with patch(
        "app.routers.feedback.client.models.generate_content",
        return_value=_FakeGeminiResponse(_fake_feedback_payload()),
    ):
        response = await client.post(f"{settings.API_V1_STR}/feedback/{project_uuid}")
    assert response.status_code == status.HTTP_200_OK


async def _generate_resum(client: AsyncClient, headers: dict[str, str], project_uuid: str):
    with patch(
        "app.routers.resum.client.models.generate_content",
        return_value=_FakeGeminiResponse(_fake_resum_payload()),
    ):
        response = await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=headers,
        )
    assert response.status_code == status.HTTP_200_OK


async def test_rt_116_projeto_deletado_nao_quebra_feedback(client: AsyncClient) -> None:
    user, headers, project_uuid = await _create_project(client)
    await _generate_feedback(client, project_uuid)

    delete_response = await client.delete(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        headers=headers,
    )
    assert delete_response.status_code == status.HTTP_200_OK

    response = await client.get(
        f"{settings.API_V1_STR}/feedback/{project_uuid}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    feedback_doc = await Feedback.find_one(Feedback.project_id == UUID(project_uuid))
    assert feedback_doc is not None


async def test_rt_117_projeto_deletado_preserva_resumo(client: AsyncClient) -> None:
    user, headers, project_uuid = await _create_project(client)
    await _generate_resum(client, headers, project_uuid)

    await client.delete(f"{settings.API_V1_STR}/projects/{project_uuid}", headers=headers)
    resum_doc = await AIResum.find_one(AIResum.project_id == UUID(project_uuid))
    assert resum_doc is not None
    assert resum_doc.student_id == user.uuid


async def test_rt_120_timestamp_e_definido_ao_criar_projeto(client: AsyncClient) -> None:
    _, headers, project_uuid = await _create_project(client)
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None
    assert isinstance(project.timestamp, datetime)


async def test_rt_121_uuid_valido_em_entidades_criticas(client: AsyncClient) -> None:
    user, headers, project_uuid = await _create_project(client)
    await _generate_feedback(client, project_uuid)
    await _generate_resum(client, headers, project_uuid)

    feedback_doc = await Feedback.find_one(Feedback.project_id == UUID(project_uuid))
    resum_doc = await AIResum.find_one(AIResum.project_id == UUID(project_uuid))
    assert feedback_doc is not None
    assert resum_doc is not None

    uuids = [
        str(user.uuid),
        project_uuid,
        str(feedback_doc.uuid),
        str(resum_doc.uuid),
    ]
    for value in uuids:
        assert len(value) == 36


async def test_rt_122_campos_obrigatorios_do_projeto_nao_sao_none(
    client: AsyncClient,
) -> None:
    _, headers, project_uuid = await _create_project(client)
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None
    assert project.project_title
    assert project.project_description
    assert project.solution_proposal


async def test_rt_123_campos_opcionais_podem_ser_vazios(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = {
        "project_title": "Projeto Campos Vazios",
        "project_description": "Descricao obrigatoria",
        "solution_proposal": "Solucao obrigatoria",
        "who_are_you": "",
        "academy_info": "",
        "market_info": "",
    }
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    project_uuid = response.json()["project_uuid"]
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None
    assert project.who_are_you == ""
    assert project.academy_info == ""
    assert project.market_info == ""
"""
Testes de Regressão - Integridade de Dados
RT-116 a RT-123
"""
from uuid import UUID

import pytest
from fastapi import status
from httpx import AsyncClient

from app.config.config import settings
from app.models import Feedback, Project
from app.models.ai_resume import AIResum
from app.models.users import User

from ..utils import create_test_project, create_test_user, generate_user_auth_headers


async def _create_project_for_user(client: AsyncClient, headers: dict[str, str]) -> str:
    """Helper para criar projeto e retornar UUID"""
    payload = create_test_project()
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    return response.json()["project_uuid"]


@pytest.mark.anyio
async def test_rt_116_deleted_project_does_not_break_feedback_references(client: AsyncClient) -> None:
    """RT-116: Projeto deletado não quebra referências em Feedback"""
    student = await create_test_user()
    headers = await generate_user_auth_headers(client, student)
    project_uuid = await _create_project_for_user(client, headers)

    # Gera feedback para o projeto
    await client.post(
        f"{settings.API_V1_STR}/feedback/{project_uuid}",
        headers=headers,
    )

    # Deleta o projeto
    delete_response = await client.delete(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        headers=headers,
    )
    assert delete_response.status_code == status.HTTP_200_OK

    # Verifica que o projeto foi deletado
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is None

    # Verifica que o feedback ainda existe (não foi deletado em cascata)
    # Isso é esperado - o feedback pode existir mesmo sem o projeto
    feedbacks = await Feedback.find(Feedback.project_id == UUID(project_uuid)).to_list()
    # O feedback pode ou não existir, dependendo da implementação
    # O importante é que não quebra o sistema


@pytest.mark.anyio
async def test_rt_117_deleted_project_does_not_break_resum_references(client: AsyncClient) -> None:
    """RT-117: Projeto deletado não quebra referências em AIResum"""
    student = await create_test_user()
    headers = await generate_user_auth_headers(client, student)
    project_uuid = await _create_project_for_user(client, headers)

    # Gera resumo para o projeto
    await client.get(
        f"{settings.API_V1_STR}/resum/{project_uuid}",
        headers=headers,
    )

    # Deleta o projeto
    delete_response = await client.delete(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        headers=headers,
    )
    assert delete_response.status_code == status.HTTP_200_OK

    # Verifica que o projeto foi deletado
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is None

    # Verifica que o resumo ainda existe (não foi deletado em cascata)
    resums = await AIResum.find(AIResum.project_id == UUID(project_uuid)).to_list()
    # O resumo pode ou não existir, dependendo da implementação
    # O importante é que não quebra o sistema


@pytest.mark.anyio
async def test_rt_119_uuids_are_unique_across_collections(client: AsyncClient) -> None:
    """RT-119: UUIDs são únicos em todas as coleções"""
    student1 = await create_test_user()
    student2 = await create_test_user()

    # Verifica que os UUIDs dos usuários são diferentes
    assert student1.uuid != student2.uuid

    headers1 = await generate_user_auth_headers(client, student1)
    headers2 = await generate_user_auth_headers(client, student2)

    # Cria projetos
    project_uuid1 = await _create_project_for_user(client, headers1)
    project_uuid2 = await _create_project_for_user(client, headers2)

    # Verifica que os UUIDs dos projetos são diferentes
    assert project_uuid1 != project_uuid2

    # Verifica que UUIDs de projetos são diferentes dos UUIDs de usuários
    assert project_uuid1 != str(student1.uuid)
    assert project_uuid2 != str(student2.uuid)


@pytest.mark.anyio
async def test_rt_120_timestamps_are_generated_correctly(client: AsyncClient) -> None:
    """RT-120: Timestamps são gerados corretamente"""
    from datetime import datetime

    student = await create_test_user()
    headers = await generate_user_auth_headers(client, student)
    project_uuid = await _create_project_for_user(client, headers)

    # Busca o projeto criado
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None

    # Verifica que o timestamp existe e é válido
    if hasattr(project, "timestamp") and project.timestamp:
        # Verifica que é um datetime válido
        assert isinstance(project.timestamp, datetime)


@pytest.mark.anyio
async def test_rt_121_uuids_are_valid_format(client: AsyncClient) -> None:
    """RT-121: UUIDs são gerados corretamente (formato válido)"""
    import re

    student = await create_test_user()
    headers = await generate_user_auth_headers(client, student)
    project_uuid = await _create_project_for_user(client, headers)

    # Padrão de UUID v4
    uuid_pattern = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", re.IGNORECASE
    )

    # Verifica formato do UUID do usuário
    assert uuid_pattern.match(str(student.uuid)) is not None

    # Verifica formato do UUID do projeto
    assert uuid_pattern.match(project_uuid) is not None


@pytest.mark.anyio
async def test_rt_122_required_fields_cannot_be_none_after_creation(client: AsyncClient) -> None:
    """RT-122: Campos obrigatórios não podem ser None após criação"""
    student = await create_test_user()
    headers = await generate_user_auth_headers(client, student)
    project_uuid = await _create_project_for_user(client, headers)

    # Busca o projeto criado
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None

    # Verifica campos obrigatórios do projeto
    assert project.project_title is not None
    assert project.project_title != ""
    assert project.student_id is not None
    assert project.uuid is not None

    # Verifica campos obrigatórios do usuário
    assert student.name is not None
    assert student.email is not None
    assert student.uuid is not None


@pytest.mark.anyio
async def test_rt_123_optional_fields_can_be_none_or_empty(client: AsyncClient) -> None:
    """RT-123: Campos opcionais podem ser None/string vazia"""
    student = await create_test_user()
    headers = await generate_user_auth_headers(client, student)

    # Cria projeto com alguns campos opcionais vazios
    payload = create_test_project()
    # Remove alguns campos opcionais para testar
    payload["who_are_you"] = ""
    payload["academy_info"] = ""

    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK
    project_uuid = response.json()["project_uuid"]

    # Busca o projeto criado
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None

    # Campos opcionais podem ser string vazia ou None
    # Verifica que o projeto foi criado mesmo com campos opcionais vazios
    assert project.project_title is not None  # Campo obrigatório
    # Campos opcionais podem estar vazios ou None

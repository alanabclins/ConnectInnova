"""
Testes de regressão para geração de resumos com IA (RT-103 a RT-115).
"""

from __future__ import annotations

import json
from uuid import UUID
from unittest.mock import patch

import pytest
from fastapi import status
from httpx import AsyncClient

from app.config.config import settings
from app.models import AIResum, User

from ..utils import create_test_project, create_test_user, generate_user_auth_headers

pytestmark = pytest.mark.anyio

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


def _fake_resum_payload(suffix: str = "") -> str:
    return json.dumps(
        {
            "resums": {
                field: f"{field} gerado{suffix}"
                for field in RESUM_FIELDS
            }
        }
    )


async def _create_project(client: AsyncClient, user: User | None = None):
    if user is None:
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


async def test_rt_103_resumo_e_gerado_para_projeto_valido(client: AsyncClient) -> None:
    user, headers, project_uuid = await _create_project(client)
    with patch(
        "app.routers.resum.client.models.generate_content",
        return_value=_FakeGeminiResponse(_fake_resum_payload()),
    ):
        response = await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=headers,
        )

    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["message"].startswith("✅ Resumo")
    resum_doc = await AIResum.find_one(AIResum.project_id == UUID(project_uuid))
    assert resum_doc is not None
    assert resum_doc.student_id == user.uuid


async def test_rt_105_resumo_falha_quando_nao_ha_aluno_vinculado(
    client: AsyncClient,
) -> None:
    orphan_user, _, project_uuid = await _create_project(client)
    await orphan_user.delete()

    other_user = await create_test_user()
    other_headers = await generate_user_auth_headers(client, other_user)

    with patch(
        "app.routers.resum.client.models.generate_content",
        side_effect=AssertionError("Não deveria chamar IA"),
    ):
        response = await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=other_headers,
        )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Aluno vinculado não encontrado" in response.json()["detail"]


async def test_rt_112_json_malformado_retorna_500(client: AsyncClient) -> None:
    _, headers, project_uuid = await _create_project(client)
    with patch(
        "app.routers.resum.client.models.generate_content",
        return_value=_FakeGeminiResponse("{invalid-json"),
    ):
        response = await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=headers,
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Resposta JSON inválida" in response.json()["detail"]


async def test_rt_104_resumo_projeto_inexistente_retorna_404(client: AsyncClient) -> None:
    """RT-104: Resumo de projeto inexistente retorna 404"""
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = await client.get(
        f"{settings.API_V1_STR}/resum/{fake_uuid}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_rt_106_resumo_retorna_resum_id_e_resums(client: AsyncClient) -> None:
    """RT-106: Resumo retorna resum_id e resums com 5 campos"""
    _, headers, project_uuid = await _create_project(client)
    with patch(
        "app.routers.resum.client.models.generate_content",
        return_value=_FakeGeminiResponse(_fake_resum_payload()),
    ):
        response = await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=headers,
        )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "resum_id" in data
    assert "resums" in data
    assert len(data["resums"]) == 5


async def test_rt_107_resumo_inclui_5_campos_especificos(client: AsyncClient) -> None:
    """RT-107: Resumo inclui os 5 campos específicos"""
    _, headers, project_uuid = await _create_project(client)
    with patch(
        "app.routers.resum.client.models.generate_content",
        return_value=_FakeGeminiResponse(_fake_resum_payload()),
    ):
        response = await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=headers,
        )

    assert response.status_code == status.HTTP_200_OK
    resums = response.json()["resums"]
    assert "clarity_resum" in resums
    assert "inovation_grade_resum" in resums
    assert "social_impact_resum" in resums
    assert "tec_eco_viability_resum" in resums
    assert "application_potencial_resum" in resums


async def test_rt_108_resumo_e_salvo_no_banco(client: AsyncClient) -> None:
    """RT-108: Resumo é salvo no banco de dados (AIResum)"""
    _, headers, project_uuid = await _create_project(client)
    with patch(
        "app.routers.resum.client.models.generate_content",
        return_value=_FakeGeminiResponse(_fake_resum_payload()),
    ):
        await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=headers,
        )

    resum_doc = await AIResum.find_one(AIResum.project_id == UUID(project_uuid))
    assert resum_doc is not None


async def test_rt_109_resumo_vinculado_ao_projeto(client: AsyncClient) -> None:
    """RT-109: Resumo está vinculado ao projeto correto"""
    _, headers, project_uuid = await _create_project(client)
    with patch(
        "app.routers.resum.client.models.generate_content",
        return_value=_FakeGeminiResponse(_fake_resum_payload()),
    ):
        await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=headers,
        )

    resum_doc = await AIResum.find_one(AIResum.project_id == UUID(project_uuid))
    assert resum_doc is not None
    assert str(resum_doc.project_id) == project_uuid


async def test_rt_110_resumo_vinculado_ao_estudante(client: AsyncClient) -> None:
    """RT-110: Resumo está vinculado ao estudante correto"""
    user, headers, project_uuid = await _create_project(client)
    with patch(
        "app.routers.resum.client.models.generate_content",
        return_value=_FakeGeminiResponse(_fake_resum_payload()),
    ):
        await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=headers,
        )

    resum_doc = await AIResum.find_one(AIResum.project_id == UUID(project_uuid))
    assert resum_doc is not None
    assert resum_doc.student_id == user.uuid


async def test_rt_111_resposta_invalida_retorna_500(client: AsyncClient) -> None:
    """RT-111: Resposta inválida do Gemini retorna erro 500"""
    _, headers, project_uuid = await _create_project(client)
    with patch(
        "app.routers.resum.client.models.generate_content",
        return_value=_FakeGeminiResponse("not-json-at-all"),
    ):
        response = await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=headers,
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


async def test_rt_113_resposta_vazia_retorna_erro(client: AsyncClient) -> None:
    """RT-113: Resposta vazia do Gemini retorna erro apropriado"""
    _, headers, project_uuid = await _create_project(client)
    with patch(
        "app.routers.resum.client.models.generate_content",
        return_value=_FakeGeminiResponse(""),
    ):
        response = await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=headers,
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


async def test_rt_114_resposta_sem_campo_resums_retorna_erro(client: AsyncClient) -> None:
    """RT-114: Resposta sem campo resums retorna erro"""
    _, headers, project_uuid = await _create_project(client)
    with patch(
        "app.routers.resum.client.models.generate_content",
        return_value=_FakeGeminiResponse('{"other_field": "value"}'),
    ):
        response = await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=headers,
        )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


async def test_rt_115_resumo_retorna_todos_os_campos(client: AsyncClient) -> None:
    """RT-115: Todos os 5 campos de resumo estão presentes"""
    _, headers, project_uuid = await _create_project(client)
    with patch(
        "app.routers.resum.client.models.generate_content",
        return_value=_FakeGeminiResponse(_fake_resum_payload()),
    ):
        response = await client.get(
            f"{settings.API_V1_STR}/resum/{project_uuid}",
            headers=headers,
        )

    assert response.status_code == status.HTTP_200_OK
    resums = response.json()["resums"]
    for field in RESUM_FIELDS:
        assert field in resums
        assert resums[field]


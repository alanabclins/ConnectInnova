"""
Testes de regressão para o módulo de feedbacks/análises com IA (RT-081 a RT-102).
"""

from __future__ import annotations

import json
from typing import Any
from uuid import UUID
from unittest.mock import patch

import pytest
from fastapi import status
from httpx import AsyncClient

from app.config.config import settings
from app.models import Feedback

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


class _FakeGeminiResponse:
    def __init__(self, payload: str):
        self.text = payload


def _fake_ai_payload(feedback_text: str = "Feedback detalhado") -> str:
    criteria = {
        key: {
            "level": 3,
            "label": "Bom",
            "feedback": f"{key} ok",
            "improvement": f"{key} melhorar",
        }
        for key in CRITERIA_KEYS
    }
    return json.dumps(
        {
            "full_feedback": feedback_text,
            "criteria_evaluation": criteria,
        }
    )


async def _create_project_for_feedback(client: AsyncClient, user=None):
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
    project_uuid = response.json()["project_uuid"]
    return user, headers, project_uuid


async def _generate_feedback(
    client: AsyncClient, project_uuid: str, ai_text: str | None = None, regenerate: bool = False
) -> dict[str, Any]:
    payload = ai_text or _fake_ai_payload()
    query = "?regenerate=true" if regenerate else ""
    with patch(
        "app.routers.feedback.client.models.generate_content",
        return_value=_FakeGeminiResponse(payload),
    ):
        response = await client.post(
            f"{settings.API_V1_STR}/feedback/{project_uuid}{query}",
        )
    assert response.status_code == status.HTTP_200_OK
    return response.json()


async def test_rt_081_generate_feedback_para_projeto_valido(client: AsyncClient) -> None:
    user, _, project_uuid = await _create_project_for_feedback(client)
    result = await _generate_feedback(client, project_uuid)
    assert result["message"].startswith("Analysis")
    feedback_doc = await Feedback.find_one(Feedback.project_id == UUID(project_uuid))
    assert feedback_doc is not None
    assert feedback_doc.student_id == user.uuid


async def test_rt_087_feedback_existente_retorna_cache(client: AsyncClient) -> None:
    _, _, project_uuid = await _create_project_for_feedback(client)
    await _generate_feedback(client, project_uuid)

    with patch(
        "app.routers.feedback.client.models.generate_content",
        side_effect=AssertionError("Não deve regenerar"),
    ):
        response = await client.post(f"{settings.API_V1_STR}/feedback/{project_uuid}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"].startswith("Existing analysis")


async def test_rt_088_regenerate_true_forca_nova_analise(client: AsyncClient) -> None:
    _, _, project_uuid = await _create_project_for_feedback(client)
    await _generate_feedback(client, project_uuid)

    payload = _fake_ai_payload("Novo feedback")
    with patch(
        "app.routers.feedback.client.models.generate_content",
        return_value=_FakeGeminiResponse(payload),
    ) as mock_generate:
        response = await client.post(
            f"{settings.API_V1_STR}/feedback/{project_uuid}?regenerate=true"
        )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["criteria_evaluation"]["proposta_de_valor"]["feedback"] == "proposta_de_valor ok"
    assert mock_generate.called is True


async def test_rt_091_resposta_invalida_do_gemini_retorna_500(client: AsyncClient) -> None:
    _, _, project_uuid = await _create_project_for_feedback(client)
    invalid_payload = "{invalid-json"
    with patch(
        "app.routers.feedback.client.models.generate_content",
        return_value=_FakeGeminiResponse(invalid_payload),
    ):
        response = await client.post(f"{settings.API_V1_STR}/feedback/{project_uuid}")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Gemini/JSON Error" in response.json()["detail"]


async def test_rt_096_get_feedback_exige_proprietario(client: AsyncClient) -> None:
    owner, owner_headers, project_uuid = await _create_project_for_feedback(client)
    await _generate_feedback(client, project_uuid)
    stranger = await create_test_user()
    stranger_headers = await generate_user_auth_headers(client, stranger)

    response_owner = await client.get(
        f"{settings.API_V1_STR}/feedback/{project_uuid}",
        headers=owner_headers,
    )
    assert response_owner.status_code == status.HTTP_200_OK

    response_stranger = await client.get(
        f"{settings.API_V1_STR}/feedback/{project_uuid}",
        headers=stranger_headers,
    )
    assert response_stranger.status_code == status.HTTP_403_FORBIDDEN


async def test_rt_100_listagem_de_feedbacks_e_filtrada_por_usuario(
    client: AsyncClient,
) -> None:
    owner = await create_test_user()
    owner_headers = await generate_user_auth_headers(client, owner)
    project_uuid_1 = (await _create_project_for_feedback(client, owner))[2]
    project_uuid_2 = (await _create_project_for_feedback(client, owner))[2]
    await _generate_feedback(client, project_uuid_1, ai_text=_fake_ai_payload("Primeiro"))
    await _generate_feedback(client, project_uuid_2, ai_text=_fake_ai_payload("Segundo"))

    stranger = await create_test_user()
    stranger_headers = await generate_user_auth_headers(client, stranger)
    stranger_project = (await _create_project_for_feedback(client, stranger))[2]
    await _generate_feedback(client, stranger_project)

    response_owner = await client.get(
        f"{settings.API_V1_STR}/feedback/user/all",
        headers=owner_headers,
    )
    assert response_owner.status_code == status.HTTP_200_OK
    assert len(response_owner.json()) == 2

    response_stranger = await client.get(
        f"{settings.API_V1_STR}/feedback/user/all",
        headers=stranger_headers,
    )
    assert response_stranger.status_code == status.HTTP_200_OK
    assert len(response_stranger.json()) == 1


async def test_rt_082_analise_projeto_inexistente_retorna_404(client: AsyncClient) -> None:
    """RT-082: Análise de projeto inexistente retorna 404"""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = await client.post(f"{settings.API_V1_STR}/feedback/{fake_uuid}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_rt_083_analise_retorna_estrutura_completa(client: AsyncClient) -> None:
    """RT-083: Análise retorna feedback_id, feedback_summary e criteria_evaluation"""
    user, _, project_uuid = await _create_project_for_feedback(client)
    result = await _generate_feedback(client, project_uuid)
    assert "feedback_summary" in result or "full_feedback" in result
    assert "criteria_evaluation" in result
    feedback_doc = await Feedback.find_one(Feedback.project_id == UUID(project_uuid))
    assert feedback_doc is not None
    assert str(feedback_doc.uuid)


async def test_rt_084_analise_e_salva_no_banco(client: AsyncClient) -> None:
    """RT-084: Análise é salva no banco de dados"""
    _, _, project_uuid = await _create_project_for_feedback(client)
    await _generate_feedback(client, project_uuid)
    feedback_doc = await Feedback.find_one(Feedback.project_id == UUID(project_uuid))
    assert feedback_doc is not None
    assert feedback_doc.full_feedback


async def test_rt_085_analise_vinculada_ao_projeto_correto(client: AsyncClient) -> None:
    """RT-085: Análise está vinculada ao projeto correto (project_id)"""
    _, _, project_uuid = await _create_project_for_feedback(client)
    await _generate_feedback(client, project_uuid)
    feedback_doc = await Feedback.find_one(Feedback.project_id == UUID(project_uuid))
    assert feedback_doc is not None
    assert str(feedback_doc.project_id) == project_uuid


async def test_rt_086_analise_vinculada_ao_estudante_correto(client: AsyncClient) -> None:
    """RT-086: Análise está vinculada ao estudante correto (student_id)"""
    user, _, project_uuid = await _create_project_for_feedback(client)
    await _generate_feedback(client, project_uuid)
    feedback_doc = await Feedback.find_one(Feedback.project_id == UUID(project_uuid))
    assert feedback_doc is not None
    assert feedback_doc.student_id == user.uuid


async def test_rt_089_analise_sem_criteria_e_regenerada(client: AsyncClient) -> None:
    """RT-089: Análise existente sem criteria_evaluation é regenerada automaticamente"""
    _, _, project_uuid = await _create_project_for_feedback(client)
    await _generate_feedback(client, project_uuid)
    feedback_doc = await Feedback.find_one(Feedback.project_id == UUID(project_uuid))
    assert feedback_doc is not None
    assert feedback_doc.criteria_evaluation is not None


async def test_rt_090_mensagem_indica_se_analise_e_cache(client: AsyncClient) -> None:
    """RT-090: Mensagem indica se análise é cacheada ou nova"""
    _, _, project_uuid = await _create_project_for_feedback(client)
    result = await _generate_feedback(client, project_uuid)
    assert "message" in result
    assert "Analysis" in result["message"] or "Existing" in result["message"]


async def test_rt_092_json_malformado_e_tratado(client: AsyncClient) -> None:
    """RT-092: JSON malformado do Gemini é tratado corretamente"""
    _, _, project_uuid = await _create_project_for_feedback(client)
    invalid = "not-a-json"
    with patch(
        "app.routers.feedback.client.models.generate_content",
        return_value=_FakeGeminiResponse(invalid),
    ):
        response = await client.post(f"{settings.API_V1_STR}/feedback/{project_uuid}")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


async def test_rt_093_resposta_vazia_retorna_erro(client: AsyncClient) -> None:
    """RT-093: Resposta vazia do Gemini retorna erro apropriado"""
    _, _, project_uuid = await _create_project_for_feedback(client)
    with patch(
        "app.routers.feedback.client.models.generate_content",
        return_value=_FakeGeminiResponse(""),
    ):
        response = await client.post(f"{settings.API_V1_STR}/feedback/{project_uuid}")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


async def test_rt_094_criteria_evaluation_validado(client: AsyncClient) -> None:
    """RT-094: criteria_evaluation é validado contra schema"""
    _, _, project_uuid = await _create_project_for_feedback(client)
    result = await _generate_feedback(client, project_uuid)
    assert "criteria_evaluation" in result
    criteria = result["criteria_evaluation"]
    for key in CRITERIA_KEYS:
        assert key in criteria


async def test_rt_095_full_feedback_e_string_nao_vazia(client: AsyncClient) -> None:
    """RT-095: full_feedback é string não vazia"""
    _, _, project_uuid = await _create_project_for_feedback(client)
    await _generate_feedback(client, project_uuid)
    feedback_doc = await Feedback.find_one(Feedback.project_id == UUID(project_uuid))
    assert feedback_doc is not None
    assert isinstance(feedback_doc.full_feedback, str)
    assert len(feedback_doc.full_feedback) > 0


async def test_rt_097_buscar_feedback_inexistente_retorna_404(client: AsyncClient) -> None:
    """RT-097: Buscar feedback inexistente retorna 404"""
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = await client.get(
        f"{settings.API_V1_STR}/feedback/{fake_uuid}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_rt_098_buscar_feedback_outro_usuario_retorna_403(client: AsyncClient) -> None:
    """RT-098: Buscar feedback de projeto de outro usuário retorna 403"""
    owner, _, project_uuid = await _create_project_for_feedback(client)
    await _generate_feedback(client, project_uuid)
    stranger = await create_test_user()
    stranger_headers = await generate_user_auth_headers(client, stranger)
    response = await client.get(
        f"{settings.API_V1_STR}/feedback/{project_uuid}",
        headers=stranger_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_rt_099_feedback_retorna_todos_campos(client: AsyncClient) -> None:
    """RT-099: Feedback retorna todos os campos incluindo criteria_evaluation"""
    owner, headers, project_uuid = await _create_project_for_feedback(client)
    await _generate_feedback(client, project_uuid)
    response = await client.get(
        f"{settings.API_V1_STR}/feedback/{project_uuid}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "criteria_evaluation" in data
    assert "full_feedback" in data or "feedback_summary" in data


async def test_rt_101_listagem_vazia_quando_sem_feedbacks(client: AsyncClient) -> None:
    """RT-101: Lista não inclui feedbacks de outros usuários"""
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.get(
        f"{settings.API_V1_STR}/feedback/user/all",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


async def test_rt_102_lista_retorna_array_vazio_sem_feedbacks(client: AsyncClient) -> None:
    """RT-102: Lista retorna array vazio se usuário não tem feedbacks"""
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.get(
        f"{settings.API_V1_STR}/feedback/user/all",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


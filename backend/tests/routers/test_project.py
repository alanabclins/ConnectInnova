
import pytest
from fastapi import status
from httpx import AsyncClient

from app.config.config import settings

from ..utils import create_test_project, create_test_user, generate_user_auth_headers


@pytest.mark.anyio
async def test_create_project_unauthenticated(client: AsyncClient) -> None:
    payload = create_test_project()
    r = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
    )
    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    data = r.json()
    assert data["detail"] == "Not authenticated"


@pytest.mark.anyio
async def test_create_project_invalid_data(client: AsyncClient) -> None:
    student = await create_test_user()
    token_headers = await generate_user_auth_headers(client, student)

    # Cria um payload dinâmico e remove um campo obrigatório para forçar a falha
    invalid_payload = create_test_project()
    del invalid_payload["project_title"]

    r = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=invalid_payload,
        headers=token_headers,
    )

    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = r.json()
    assert "detail" in data
    # Verifica a mensagem de erro de validação do Pydantic
    assert any("Field required" in error.get("msg", "") for error in data.get("detail", []))


@pytest.mark.anyio
async def test_create_project_success(client: AsyncClient) -> None:
    student = await create_test_user()
    token_headers = await generate_user_auth_headers(client, student)

    payload = create_test_project()

    r = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=token_headers,
    )

    assert r.status_code == status.HTTP_200_OK
    data = r.json()

    assert data["message"] == "Projeto cadastrado com sucesso!"
    # Asserções corrigidas para os nomes das chaves na resposta da API:
    assert "project_id_mongo" in data
    assert "project_uuid" in data
    assert "timestamp" in data

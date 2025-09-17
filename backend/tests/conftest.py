from typing import AsyncGenerator
from unittest.mock import patch

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.config.config import settings
from app.main import app

from .utils import get_user_auth_headers

# Nome do banco de teste
MONGO_TEST_DB = "ConnectInovaTest"


@pytest.fixture
def anyio_backend():
    """Usado pelo pytest-asyncio para rodar testes assíncronos"""
    return "asyncio"


async def clear_database(server: FastAPI) -> None:
    """
    Limpa todas as coleções do banco de teste após cada teste.
    """
    test_db = server.state.client[MONGO_TEST_DB]
    collections = await test_db.list_collection_names()
    for collection_name in collections:
        await test_db[collection_name].delete_many({})


@pytest.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Async server client que gerencia Lifespan e teardown.
    Substitui o banco padrão pelo banco de teste.
    """
    with patch("app.config.config.settings.MONGO_DB", MONGO_TEST_DB):
        async with LifespanManager(app):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client_instance:
                try:
                    yield client_instance
                finally:
                    await clear_database(app)


@pytest.fixture()
async def superuser_token_headers(client: AsyncClient) -> dict[str, str]:
    """
    Retorna os headers de autorização do superuser para testes autenticados.
    """
    return await get_user_auth_headers(
        client, settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD
    )

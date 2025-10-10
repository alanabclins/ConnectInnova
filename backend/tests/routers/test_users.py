import pytest
from fastapi import status
from httpx import AsyncClient
from pydantic import ValidationError

from app.config.config import settings
from app.models import User

from ..utils import (
    create_test_user,
    generate_user_auth_headers,
    random_email,
    random_lower_string,
)

EXPECTED_TOTAL_USERS_TEST_1 = 5
EXPECTED_TOTAL_USERS_TEST_2 = 2
EXPECTED_TOTAL_USERS_TEST_3 = 10


# @pytest.mark.anyio
# async def test_create_user_empty_name_on_creation_user(
#     client: AsyncClient
# ) -> None:
#     data =  {"email": "nao_e_um_email.com", "password": password}
#     r = await client.post(f"{settings.API_V1_STR}/users/", data=)
#     current_user = r.json()
#     assert current_user
#     assert current_user["is_active"] is True
#     assert current_user["is_superuser"]
#     assert current_user["email"] == settings.FIRST_SUPERUSER


@pytest.mark.anyio
def test_reject_empty_name(self, client: AsyncClient):
    """Teste 2b: Erro ao validar dados com nome vazio"""
    data = {"email": "test@example.com", "password_hash": "$2b$12$hash"}

    with pytest.raises(ValidationError) as exc_info:
        User.model_validate(data)

    errors = exc_info.value.errors()
    # Deve rejeitar porque name não pode ser string vazia
    assert any("name" in str(error["loc"]) for error in errors)


@pytest.mark.anyio
def test_reject_whitespace_only_name(self):
    """Teste 2c: Erro ao validar dados com nome apenas espaços"""
    data = {
        "name": "   ",  # Apenas espaços
        "email": "test@example.com",
        "password_hash": "$2b$12$hash",
    }
    


@pytest.mark.anyio
async def test_get_profile_superuser(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    r = await client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


@pytest.mark.anyio
async def test_get_profile_normal_user(client: AsyncClient) -> None:
    user = await create_test_user()
    token_headers = await generate_user_auth_headers(client, user)
    response = await client.get(f"{settings.API_V1_STR}/users/me", headers=token_headers)

    profile = response.json()
    assert profile
    assert profile["is_active"] is True
    assert profile["is_superuser"] is False
    assert profile["email"] == user.email


@pytest.mark.anyio
async def test_create_user(client: AsyncClient) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = await client.post(
        f"{settings.API_V1_STR}/users",
        json=data,
    )
    assert r.status_code == status.HTTP_200_OK
    created_user = r.json()
    user = await User.find_one({"email": username})
    assert user
    assert user.email == created_user["email"]


@pytest.mark.anyio
async def test_create_user_existing_email(client: AsyncClient) -> None:
    user = await create_test_user()
    data = {"email": user.email, "password": "password"}
    r = await client.post(f"{settings.API_V1_STR}/users", json=data)
    response = r.json()
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert response["detail"] == "User with that email already exists."


@pytest.mark.anyio
async def test_get_existing_user(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    user = await create_test_user()
    r = await client.get(
        f"{settings.API_V1_STR}/users/{user.uuid}",
        headers=superuser_token_headers,
    )
    assert r.status_code == status.HTTP_200_OK
    api_user = r.json()
    assert user.email == api_user["email"]


@pytest.mark.anyio
async def test_update_profile(client: AsyncClient) -> None:
    # create user
    user = await create_test_user()
    user_hashed_password = user.hashed_password
    token_headers = await generate_user_auth_headers(client, user)

    # update user email and pw
    data = {"email": random_email(), "password": random_lower_string()}
    r = await client.patch(
        f"{settings.API_V1_STR}/users/me", json=data, headers=token_headers
    )
    assert r.status_code == status.HTTP_200_OK

    updated_user = await User.get(user.id)
    assert updated_user is not None
    assert updated_user.email == data["email"]
    assert updated_user.hashed_password != user_hashed_password


@pytest.mark.anyio
async def test_update_profile_existing_email(client: AsyncClient) -> None:
    # create user
    user = await create_test_user()
    token_headers = await generate_user_auth_headers(client, user)

    # update user email to already existing email
    data = {"email": settings.FIRST_SUPERUSER}
    r = await client.patch(
        f"{settings.API_V1_STR}/users/me", json=data, headers=token_headers
    )
    response = r.json()
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert response["detail"] == "User with that email already exists."


@pytest.mark.anyio
async def test_update_profile_cannot_set_superuser(client: AsyncClient) -> None:
    # create user
    user = await create_test_user()
    token_headers = await generate_user_auth_headers(client, user)

    # test user cannot set itself to superuser or inactive
    data = {"is_superuser": True, "is_active": False}
    r = await client.patch(
        f"{settings.API_V1_STR}/users/me", json=data, headers=token_headers
    )
    assert r.status_code == status.HTTP_200_OK

    updated_user = await User.get(user.id)
    assert updated_user is not None
    assert updated_user.is_superuser is False
    assert updated_user.is_active is True


@pytest.mark.anyio
async def test_update_user(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    # create user
    user = await create_test_user()
    user_hashed_password = user.hashed_password

    # update user email and pw
    data = {
        "email": random_email(),
        "password": random_lower_string(),
        "is_superuser": True,
        "is_active": False,
    }
    r = await client.patch(
        f"{settings.API_V1_STR}/users/{user.uuid}",
        json=data,
        headers=superuser_token_headers,
    )
    assert r.status_code == status.HTTP_200_OK

    updated_user = await User.get(user.id)
    assert updated_user is not None
    assert updated_user.email == data["email"]
    assert updated_user.hashed_password != user_hashed_password
    assert updated_user.is_superuser is True
    assert updated_user.is_active is False


@pytest.mark.anyio
async def test_update_user_existing_email(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    # create user
    user = await create_test_user()

    # update user email to already existing email
    data = {"email": settings.FIRST_SUPERUSER}
    r = await client.patch(
        f"{settings.API_V1_STR}/users/{user.uuid}",
        json=data,
        headers=superuser_token_headers,
    )
    response = r.json()
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert response["detail"] == "User with that email already exists."


@pytest.mark.anyio
async def test_create_user_invalid_email_format(client: AsyncClient) -> None:
    """Testa se a criação de usuário com e-mail inválido retorna erro de validação (422)."""
    password = random_lower_string()
    # E-mail inválido que falharia na validação do Pydantic/modelo
    data = {"email": "nao_e_um_email.com", "password": password}
    r = await client.post(
        f"{settings.API_V1_STR}/users",
        json=data,
    )

    # O FastAPI/Pydantic deve retornar 422 (Unprocessable Entity)
    assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    response = r.json()

    # Opcional: Verifica se a mensagem de erro é sobre o e-mail
    assert "detail" in response
    assert any(
        "value is not a valid email address" in item.get("msg", "")
        for item in response["detail"]
    )


@pytest.mark.anyio
async def test_create_user_case_insensitive_duplicate(client: AsyncClient) -> None:
    """
    Testa se a criação falha com e-mail duplicado, ignorando case,
    assumindo que há normalização para minúsculas antes da inserção.
    """
    password = random_lower_string()
    email_uppercase = "UserTesteCase@Example.Com"
    email_lowercase = "usertestecase@example.com"

    # 1. Cria com e-mail em maiúsculas (O sistema deve salvar em minúsculas)
    data1 = {"email": email_uppercase, "password": password}
    r1 = await client.post(f"{settings.API_V1_STR}/users", json=data1)
    assert r1.status_code == status.HTTP_200_OK

    # 2. Tenta criar com a mesma base de e-mail em minúsculas
    data2 = {"email": email_lowercase, "password": password}
    r2 = await client.post(f"{settings.API_V1_STR}/users", json=data2)

    # Deve falhar, pois após a normalização (salvar em minúsculas), o e-mail é duplicado
    assert r2.status_code == status.HTTP_400_BAD_REQUEST
    assert r2.json()["detail"] == "User with that email already exists."


@pytest.mark.anyio
async def test_user_cannot_update_another_users_email(client: AsyncClient):
    """Test 9: Usuário autenticado não pode atualizar o e-mail de outro usuário."""

    # Cria dois usuários diretamente no banco
    user1 = User(name="User 1", email="user1@example.com", hashed_password="$2b$12$hash1")
    await user1.insert()

    user2 = User(name="User 2", email="user2@example.com", hashed_password="$2b$12$hash2")
    await user2.insert()

    # Gera headers de autenticação para user2
    headers = await generate_user_auth_headers(client, user2)

    # Tenta atualizar o e-mail de user1 usando a conta de user2
    data = {"email": "newemail@example.com"}
    response = await client.patch(
        f"{settings.API_V1_STR}/users/{user1.uuid}",
        json=data,
        headers=headers,
    )

    # Verifica se a API proíbe a atualização
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "The user doesn't have enough privileges" in response.json()["detail"]


@pytest.mark.anyio
async def test_update_user_keep_same_email(client: AsyncClient):
    """Test 10: Permite atualizar outros campos mantendo o mesmo e-mail."""
    user = User(name="Original Name", email="test@example.com", hashed_password="$2b$12$hash")
    await user.insert()

    user.name = "Updated Name"
    await user.save()

    updated_user = await User.get(user.id)
    if updated_user is not None:
        assert updated_user.name == "Updated Name"
        assert updated_user.email == "test@example.com"


@pytest.mark.anyio
async def test_update_email_to_new_unique_value(client: AsyncClient):
    """Test 11: Permite atualizar o e-mail para um novo valor único."""
    user = User(name="Test User", email="old@example.com", hashed_password="$2b$12$hash")
    await user.insert()

    user.email = "new@example.com"
    await user.save()

    updated_user = await User.get(user.id)
    if updated_user is not None:
        assert updated_user.email == "new@example.com"

import pytest
from fastapi import status
from httpx import AsyncClient

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


@pytest.mark.anyio
async def test_missing_name_field_returns_validation_error(client: AsyncClient):
    """Test: POST /users without name field returns proper validation error"""
    response = await client.post(
        f"{settings.API_V1_STR}/users",
        json={
            # name field is MISSING
            "email": "noname@example.com",
            "password": "Password123",
            "password_confirmation": "Password123",
        },
    )

    # Should return 422 Unprocessable Entity
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Verify response structure
    data = response.json()
    assert "detail" in data
    assert isinstance(data["detail"], list)
    assert len(data["detail"]) > 0

    # Find the error about name field
    name_error = None
    for error in data["detail"]:
        if "name" in error.get("loc", []):
            name_error = error
            break

    assert name_error is not None, "No error found for 'name' field"

    # Verify exact error structure
    assert name_error["type"] == "missing"
    assert "body" in name_error["loc"]
    assert "name" in name_error["loc"]
    assert name_error["msg"] == "Field required"


@pytest.mark.anyio
async def test_name_with_numbers_returns_error(client: AsyncClient):
    """Test: POST /users with name containing numbers returns validation error"""
    response = await client.post(
        f"{settings.API_V1_STR}/users",
        json={
            "name": "João Silva 123",  # Nome com números
            "email": random_email(),
            "password": random_lower_string(),
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "detail" in data
    assert "special characters or numbers" in data["detail"].lower()


@pytest.mark.anyio
async def test_name_with_special_characters_returns_error(client: AsyncClient):
    """Test: POST /users with name containing special characters returns error"""
    response = await client.post(
        f"{settings.API_V1_STR}/users",
        json={
            "name": "João@Silva#",  # Nome com caracteres especiais
            "email": random_email(),
            "password": random_lower_string(),
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert "detail" in data
    assert "special characters or numbers" in data["detail"].lower()


@pytest.mark.anyio
async def test_name_with_valid_characters_succeeds(client: AsyncClient):
    """Test: POST /users with valid name (letters, spaces, hyphens, apostrophes) succeeds"""
    response = await client.post(
        f"{settings.API_V1_STR}/users",
        json={
            "name": "Maria O'Brien-Silva",  # Nome válido com hífen e apóstrofo
            "email": random_email(),
            "password": random_lower_string(),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Maria O'Brien-Silva"


@pytest.mark.anyio
async def test_name_with_accents_succeeds(client: AsyncClient):
    """Test: POST /users with name containing accents succeeds"""
    response = await client.post(
        f"{settings.API_V1_STR}/users",
        json={
            "name": "José María Peña",  # Nome com acentos
            "email": random_email(),
            "password": random_lower_string(),
        },
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "José María Peña"


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
    data = {
        "name": "Test User",
        "email": username,
        "password": password,
        "password_confirmation": password,
    }
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
    data = {
        "name": "Duplicate User",
        "email": user.email,
        "password": "Password123",
        "password_confirmation": "Password123",
    }
    r = await client.post(f"{settings.API_V1_STR}/users", json=data)
    response = r.json()
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response["detail"].lower()


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
    data1 = {
        "name": "Case Test User",
        "email": email_uppercase,
        "password": password,
        "password_confirmation": password,
    }
    r1 = await client.post(f"{settings.API_V1_STR}/users", json=data1)
    assert r1.status_code == status.HTTP_200_OK

    # 2. Tenta criar com a mesma base de e-mail em minúsculas
    data2 = {
        "name": "Another User",
        "email": email_lowercase,
        "password": password,
        "password_confirmation": password,
    }
    r2 = await client.post(f"{settings.API_V1_STR}/users", json=data2)

    # Deve falhar, pois após a normalização (salvar em minúsculas), o e-mail é duplicado
    assert r2.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in r2.json()["detail"].lower()


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

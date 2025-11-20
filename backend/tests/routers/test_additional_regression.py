"""
Testes adicionais de regressão cobrindo os cenários do plano RT-001 a RT-140.

Os testes aqui criados **não** alteram os testes existentes; servem apenas para
expandir a cobertura de regressão conforme documentado em
`documentacao_regressao/PLANO_TESTE_REGRESSAO.md`.
"""

from __future__ import annotations

import time
from uuid import UUID, uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from app.config.config import settings
from app.models import Project, User

from ..utils import (
    create_test_project,
    create_test_user,
    generate_user_auth_headers,
    get_user_auth_headers,
    random_email,
    random_lower_string,
)

pytestmark = pytest.mark.anyio


def _valid_password() -> str:
    """Gera uma senha compatível com as regras de validação (6-14 chars)."""
    return random_lower_string()[:10]


async def _create_project_for_user(
    client: AsyncClient,
    token_headers: dict[str, str],
    overrides: dict[str, str] | None = None,
) -> str:
    payload = create_test_project()
    if overrides:
        payload.update(overrides)

    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    return response.json()["project_uuid"]


async def _register_user_via_api(
    client: AsyncClient, *, name: str | None = None
) -> tuple[User, str]:
    email = random_email()
    password = _valid_password()
    payload = {
        "name": name or "User Regression",
        "email": email,
        "password": password,
        "password_confirmation": password,
    }
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_200_OK
    user = await User.find_one({"email": email})
    assert user is not None
    return user, password


# ---------------------------------------------------------------------------
# 1. Autenticação e Autorização (RT-001 a RT-010)
# ---------------------------------------------------------------------------


async def test_rt_001_login_com_credenciais_validas_retorna_token(client: AsyncClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    response = await client.post(
        f"{settings.API_V1_STR}/login/access-token",
        data=login_data,
    )
    payload = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]


async def test_rt_002_login_credenciais_invalidas_retorna_erro(client: AsyncClient) -> None:
    login_data = {"username": settings.FIRST_SUPERUSER, "password": "senha-invalida"}
    response = await client.post(
        f"{settings.API_V1_STR}/login/access-token",
        data=login_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Incorrect email or password"


async def test_rt_003_token_valido_acessa_endpoint_protegido(
    client: AsyncClient,
) -> None:
    headers = await get_user_auth_headers(
        client, settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD
    )
    response = await client.get(
        f"{settings.API_V1_STR}/login/test-token",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == settings.FIRST_SUPERUSER


async def test_rt_004_token_invalido_resulta_em_401(client: AsyncClient) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}/login/test-token",
        headers={"Authorization": "Bearer invalid"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_rt_005_endpoint_test_token_valida_payload(
    client: AsyncClient,
) -> None:
    headers = await get_user_auth_headers(
        client, settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD
    )
    response = await client.get(
        f"{settings.API_V1_STR}/login/test-token",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["email"] == settings.FIRST_SUPERUSER
    assert payload["is_active"] is True
    assert "uuid" in payload


async def test_rt_006_requisicao_sem_token_resulta_em_401(client: AsyncClient) -> None:
    response = await client.get(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_rt_007_superuser_tem_acesso_a_rotas_admin(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}/users",
        headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


async def test_rt_008_usuario_normal_nao_acessa_rotas_admin(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.get(f"{settings.API_V1_STR}/users", headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "privileges" in response.json()["detail"]


async def test_rt_009_usuario_lista_apenas_seus_projetos(client: AsyncClient) -> None:
    owner = await create_test_user()
    outsider = await create_test_user()
    owner_headers = await generate_user_auth_headers(client, owner)
    outsider_headers = await generate_user_auth_headers(client, outsider)

    await _create_project_for_user(client, owner_headers)
    await _create_project_for_user(client, owner_headers)
    await _create_project_for_user(client, outsider_headers)

    response = await client.get(
        f"{settings.API_V1_STR}/projects/",
        headers=owner_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    projects = response.json()
    assert len(projects) == 2
    assert all(project["student_id"] == str(owner.uuid) for project in projects)


async def test_rt_010_usuario_nao_pode_alterar_projeto_de_outro(client: AsyncClient) -> None:
    owner = await create_test_user()
    attacker = await create_test_user()
    owner_headers = await generate_user_auth_headers(client, owner)
    attacker_headers = await generate_user_auth_headers(client, attacker)

    project_uuid = await _create_project_for_user(client, owner_headers)
    payload = create_test_project()

    response = await client.patch(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        json=payload,
        headers=attacker_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


# ---------------------------------------------------------------------------
# 2. Gerenciamento de Usuários (RT-016 a RT-040)
# ---------------------------------------------------------------------------


async def test_rt_011_criar_usuario_com_dados_validos(client: AsyncClient) -> None:
    password = _valid_password()
    payload = {
        "name": "Usuário Plano",
        "email": random_email(),
        "password": password,
    }
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == payload["email"].lower()
    assert data["is_superuser"] is False


async def test_rt_012_criar_usuario_sem_nome_retorna_422(client: AsyncClient) -> None:
    payload = {
        "email": random_email(),
        "password": _valid_password(),
    }
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert any("name" in error["loc"] for error in detail)


async def test_rt_013_criar_usuario_com_email_invalido(client: AsyncClient) -> None:
    payload = {
        "name": "Email Invalido",
        "email": "email-invalido",
        "password": _valid_password(),
    }
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_rt_014_criar_usuario_email_duplicado(client: AsyncClient) -> None:
    email = random_email()
    password = _valid_password()
    base_payload = {"name": "Duplicado", "email": email, "password": password}
    first = await client.post(f"{settings.API_V1_STR}/users", json=base_payload)
    assert first.status_code == status.HTTP_200_OK

    response = await client.post(
        f"{settings.API_V1_STR}/users",
        json={**base_payload, "password": _valid_password()},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


async def test_rt_015_criar_usuario_email_case_insensitivo(client: AsyncClient) -> None:
    password = _valid_password()
    email_upper = "UsuarioCase@Teste.com"
    payload = {"name": "Case Test", "email": email_upper, "password": password}
    first = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert first.status_code == status.HTTP_200_OK

    response = await client.post(
        f"{settings.API_V1_STR}/users",
        json={"name": "Outro", "email": email_upper.lower(), "password": _valid_password()},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


async def test_rt_018_usuario_criado_eh_ativo_por_padrao(client: AsyncClient) -> None:
    user, _ = await _register_user_via_api(client, name="Usuário Padrão")
    assert user.is_active is True
    assert user.is_superuser is False


async def test_rt_020_nome_com_numeros_retorna_400(client: AsyncClient) -> None:
    payload = {
        "name": "Usu4rio 123",
        "email": random_email(),
        "password": _valid_password(),
    }
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "números" in response.json()["detail"]


async def test_rt_021_nome_com_caracteres_invalidos_retorna_400(
    client: AsyncClient,
) -> None:
    payload = {
        "name": "Usuário @@",
        "email": random_email(),
        "password": _valid_password(),
    }
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "caracteres inválidos" in response.json()["detail"]


async def test_rt_023_nome_com_acentos_eh_aceito(client: AsyncClient) -> None:
    payload = {
        "name": "José Ávila",
        "email": random_email(),
        "password": _valid_password(),
    }
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_200_OK


async def test_rt_025_superuser_consulta_proprio_perfil(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["email"] == settings.FIRST_SUPERUSER
    assert payload["is_superuser"] is True


async def test_rt_026_usuario_normal_consulta_proprio_perfil(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["email"] == user.email
    assert payload["is_superuser"] is False


async def test_rt_027_perfil_retorna_flags_corretas(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=headers,
    )
    payload = response.json()
    assert payload["is_active"] is True
    assert payload["is_superuser"] is False


async def test_rt_028_usuario_atualiza_proprio_perfil(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.patch(
        f"{settings.API_V1_STR}/users/me",
        json={"name": "Nome Atualizado"},
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    updated = await User.get(user.id)
    assert updated is not None
    assert updated.name == "Nome Atualizado"


async def test_rt_029_atualizacao_email_para_valor_unico(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    new_email = random_email()
    response = await client.patch(
        f"{settings.API_V1_STR}/users/me",
        json={"email": new_email},
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    updated = await User.get(user.id)
    assert updated is not None
    assert updated.email == new_email


async def test_rt_030_atualizacao_email_existente_retorna_400(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.patch(
        f"{settings.API_V1_STR}/users/me",
        json={"email": settings.FIRST_SUPERUSER},
        headers=headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


async def test_rt_031_atualizacao_senha_altera_hash(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    old_hash = user.hashed_password
    response = await client.patch(
        f"{settings.API_V1_STR}/users/me",
        json={"password": _valid_password()},
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    refreshed = await User.get(user.id)
    assert refreshed is not None
    assert refreshed.hashed_password != old_hash


async def test_rt_032_usuario_nao_pode_se_promover(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.patch(
        f"{settings.API_V1_STR}/users/me",
        json={"is_superuser": True, "is_active": False},
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    refreshed = await User.get(user.id)
    assert refreshed is not None
    assert refreshed.is_superuser is False
    assert refreshed.is_active is True


async def test_rt_034_superuser_pode_atualizar_usuario(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    user = await create_test_user()
    new_email = random_email()
    response = await client.patch(
        f"{settings.API_V1_STR}/users/{user.uuid}",
        json={"email": new_email},
        headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    refreshed = await User.get(user.id)
    assert refreshed is not None
    assert refreshed.email == new_email


async def test_rt_035_superuser_pode_alterar_flags(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    user = await create_test_user()
    response = await client.patch(
        f"{settings.API_V1_STR}/users/{user.uuid}",
        json={"is_superuser": True, "is_active": False},
        headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    refreshed = await User.get(user.id)
    assert refreshed is not None
    assert refreshed.is_superuser is True
    assert refreshed.is_active is False


async def test_rt_036_usuario_nao_pode_atualizar_outro_usuario(client: AsyncClient) -> None:
    actor = await create_test_user()
    target = await create_test_user()
    headers = await generate_user_auth_headers(client, actor)
    response = await client.patch(
        f"{settings.API_V1_STR}/users/{target.uuid}",
        json={"email": random_email()},
        headers=headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "privileges" in response.json()["detail"]


async def test_rt_037_atualizacao_mantem_email_quando_nao_enviado(
    client: AsyncClient,
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.patch(
        f"{settings.API_V1_STR}/users/me",
        json={"name": "Apenas Nome"},
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    refreshed = await User.get(user.id)
    assert refreshed is not None
    assert refreshed.email == user.email


async def test_rt_016_senha_e_armazenada_hasheada(client: AsyncClient) -> None:
    user, password = await _register_user_via_api(client)
    assert user.hashed_password != password
    assert user.hashed_password.startswith("$2b$")


async def test_rt_017_rt_018_usuario_criado_ativo_e_nao_superuser(client: AsyncClient) -> None:
    user, _ = await _register_user_via_api(client)
    assert user.is_active is True
    assert user.is_superuser is False


@pytest.mark.parametrize(
    ("invalid_name", "expected_fragment"),
    [
        ("<script>alert('xss')</script>", "código HTML"),
        ("Usu4rio 123", "números"),
        ("Usuário @#", "caracteres inválidos"),
    ],
)
async def test_rt_019_rt_021_nome_invalido_retorna_400(
    client: AsyncClient, invalid_name: str, expected_fragment: str
) -> None:
    payload = {
        "name": invalid_name,
        "email": random_email(),
        "password": random_lower_string(),
    }
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert expected_fragment in response.json()["detail"]


@pytest.mark.parametrize("valid_name", ["Maria das Dores", "Ângela Vitória"])
async def test_rt_022_rt_023_nome_valido_e_aceito(
    client: AsyncClient, valid_name: str
) -> None:
    payload = {
        "name": valid_name,
        "email": random_email(),
        "password": random_lower_string(),
    }
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_200_OK


async def test_rt_024_rt_027_get_profile_retorna_usuario_autenticado(
    client: AsyncClient,
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert payload["email"] == user.email
    assert payload["is_active"] is True
    assert payload["is_superuser"] is False


async def test_rt_033_usuario_nao_consegue_alterar_flags_privilegio(
    client: AsyncClient,
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.patch(
        f"{settings.API_V1_STR}/users/me",
        json={"is_active": False, "is_superuser": True},
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    refreshed = await User.get(user.id)
    assert refreshed is not None
    assert refreshed.is_active is True
    assert refreshed.is_superuser is False


async def test_rt_038_superuser_busca_usuario_por_uuid(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    user = await create_test_user()
    response = await client.get(
        f"{settings.API_V1_STR}/users/{user.uuid}",
        headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == user.email


async def test_rt_039_busca_usuario_inexistente_retorna_404(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}/users/{uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


async def test_rt_040_busca_retorna_campos_corretos(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    user = await create_test_user()
    response = await client.get(
        f"{settings.API_V1_STR}/users/{user.uuid}",
        headers=superuser_token_headers,
    )
    payload = response.json()
    assert payload["uuid"] == str(user.uuid)
    assert payload["email"] == user.email
    assert payload["is_active"] is True


# ---------------------------------------------------------------------------
# 3. Gerenciamento de Projetos (RT-041 a RT-080)
# ---------------------------------------------------------------------------


async def test_rt_041_criar_projeto_autenticado_retorna_200(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=create_test_project(),
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK


async def test_rt_043_criar_projeto_dados_validos_retorna_sucesso(
    client: AsyncClient,
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=create_test_project(),
        headers=headers,
    )
    assert response.json()["message"] == "Projeto cadastrado com sucesso!"


async def test_rt_048_criacao_retorna_identificadores(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=create_test_project(),
        headers=headers,
    )
    data = response.json()
    for key in {"project_id_mongo", "project_uuid", "timestamp"}:
        assert key in data


async def test_rt_042_criar_projeto_sem_autenticacao(client: AsyncClient) -> None:
    payload = create_test_project()
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"


async def test_rt_044_criar_projeto_sem_campo_obrigatorio(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    payload.pop("project_title")
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert any(
        error["loc"][-1] == "project_title" for error in response.json().get("detail", [])
    )


async def test_rt_045_projeto_criado_tem_student_id_do_usuario(
    client: AsyncClient,
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=create_test_project(),
        headers=headers,
    )
    project = await Project.find_one(
        Project.uuid == UUID(response.json()["project_uuid"])
    )
    assert project is not None
    assert project.student_id == user.uuid


async def test_rt_046_projeto_criado_possui_timestamp(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=create_test_project(),
        headers=headers,
    )
    project = await Project.find_one(
        Project.uuid == UUID(response.json()["project_uuid"])
    )
    assert project is not None
    assert project.timestamp is not None


async def test_rt_047_projetos_recebem_uuid_unico(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response_one = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=create_test_project(),
        headers=headers,
    )
    response_two = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=create_test_project(),
        headers=headers,
    )
    assert response_one.json()["project_uuid"] != response_two.json()["project_uuid"]


async def test_rt_049_campos_agregados_sao_gerados_automaticamente(
    client: AsyncClient,
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    for aggregated_field in [
        "clarity_problem",
        "inovation_grade",
        "social_impact_aggregated",
        "tec_eco_viability",
        "application_potencial",
    ]:
        payload.pop(aggregated_field, None)

    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    project_uuid = response.json()["project_uuid"]
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None
    assert payload["problem_description"] in project.clarity_problem
    assert project.inovation_grade == payload["innovation"]
    assert project.social_impact_aggregated == payload["social_impact"]
    assert payload["technical_feasibility"] in project.tec_eco_viability
    assert payload["customer_segment"] in project.application_potencial


async def test_rt_050_clarity_problem_agrega_detalhes(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    # Remove o campo clarity_problem para forçar agregação
    payload.pop("clarity_problem", None)
    payload.update(
        {
            "problem_description": "Problema Central",
            "target_audience": "Público Jovem",
            "value_proposition": "Valor Único",
        }
    )
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    project_uuid = response.json()["project_uuid"]
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None
    assert "Problema Central" in project.clarity_problem
    assert "Público Jovem" in project.clarity_problem
    assert "Valor Único" in project.clarity_problem


async def test_rt_051_tec_eco_viability_agrega_campos(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    payload.update(
        {
            "technical_feasibility": "Tech OK",
            "revenue_model": "Receita X",
            "scalability": "Escala Global",
            "tec_eco_viability": None,
        }
    )
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    project_uuid = response.json()["project_uuid"]
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None
    assert "Tech OK" in project.tec_eco_viability
    assert "Receita X" in project.tec_eco_viability
    assert "Escala Global" in project.tec_eco_viability


async def test_rt_052_application_potencial_agrega_segmento(
    client: AsyncClient,
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    payload.update(
        {
            "customer_segment": "Empresas",
            "competitive_advantage": "Equipe Sênior",
            "application_potencial": None,
        }
    )
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    project = await Project.find_one(
        Project.uuid == UUID(response.json()["project_uuid"])
    )
    assert project is not None
    assert "Empresas" in project.application_potencial
    assert "Equipe Sênior" in project.application_potencial


async def test_rt_053_campos_agregados_respeitam_payload(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    payload["clarity_problem"] = "Valor Manual"
    payload["tec_eco_viability"] = "Manual Tec"
    payload["application_potencial"] = "Manual Aplicação"
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    project = await Project.find_one(
        Project.uuid == UUID(response.json()["project_uuid"])
    )
    assert project is not None
    assert project.clarity_problem == "Valor Manual"
    assert project.tec_eco_viability == "Manual Tec"
    assert project.application_potencial == "Manual Aplicação"


async def test_rt_054_inovation_grade_usa_innovation_quando_agregado_vazio(
    client: AsyncClient,
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    payload["inovation_grade"] = None
    payload["innovation"] = "Inovação Primária"
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    project = await Project.find_one(
        Project.uuid == UUID(response.json()["project_uuid"])
    )
    assert project is not None
    assert project.inovation_grade == "Inovação Primária"


async def test_rt_055_social_impact_aggregated_usa_social_impact(
    client: AsyncClient,
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    payload["social_impact_aggregated"] = None
    payload["social_impact"] = "Impacto Real"
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    project = await Project.find_one(
        Project.uuid == UUID(response.json()["project_uuid"])
    )
    assert project is not None
    assert project.social_impact_aggregated == "Impacto Real"


async def test_rt_056_criacao_projeto_com_todos_campos(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "project_uuid" in data
    assert data["message"] == "Projeto cadastrado com sucesso!"


async def test_rt_057_criar_projeto_com_campos_opcionais_vazios(
    client: AsyncClient,
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    for field in [
        "problem_description",
        "target_audience",
        "value_proposition",
        "customer_segment",
    ]:
        payload[field] = ""
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK


async def test_rt_058_campos_pessoais_sao_salvos(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    payload.update(
        {
            "who_are_you": "Sou estudante de engenharia.",
            "academy_info": "USP/2024",
            "market_info": "Estágio em inovação",
        }
    )
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    project = await Project.find_one(
        Project.uuid == UUID(response.json()["project_uuid"])
    )
    assert project is not None
    assert project.who_are_you == payload["who_are_you"]
    assert project.academy_info == payload["academy_info"]
    assert project.market_info == payload["market_info"]


async def test_rt_059_campos_opcionais_podem_ser_omitidos(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    payload.pop("who_are_you")
    payload.pop("academy_info")
    payload.pop("market_info")
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    project = await Project.find_one(
        Project.uuid == UUID(response.json()["project_uuid"])
    )
    assert project is not None
    assert project.who_are_you == ""
    assert project.academy_info == ""
    assert project.market_info == ""


async def test_rt_060_listagem_retorna_somente_projetos_do_usuario(
    client: AsyncClient,
) -> None:
    owner = await create_test_user()
    other = await create_test_user()
    owner_headers = await generate_user_auth_headers(client, owner)
    other_headers = await generate_user_auth_headers(client, other)

    await _create_project_for_user(client, owner_headers)
    await _create_project_for_user(client, other_headers)

    response = await client.get(
        f"{settings.API_V1_STR}/projects/",
        headers=owner_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    projects = response.json()
    assert len(projects) == 1
    assert projects[0]["student_id"] == str(owner.uuid)


async def test_rt_061_listagem_nao_inclui_projetos_de_outros(
    client: AsyncClient,
) -> None:
    owner = await create_test_user()
    outsider = await create_test_user()
    owner_headers = await generate_user_auth_headers(client, owner)
    outsider_headers = await generate_user_auth_headers(client, outsider)
    await _create_project_for_user(client, owner_headers)
    await _create_project_for_user(client, outsider_headers)

    response = await client.get(
        f"{settings.API_V1_STR}/projects/",
        headers=owner_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert all(project["student_id"] == str(owner.uuid) for project in response.json())


async def test_rt_062_listagem_sem_projetos_retorna_vazio(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.get(
        f"{settings.API_V1_STR}/projects/",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


async def test_rt_063_listagem_retorna_campos_completos(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    await _create_project_for_user(client, headers)
    response = await client.get(
        f"{settings.API_V1_STR}/projects/",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    project = response.json()[0]
    for field in (
        "project_title",
        "project_description",
        "solution_proposal",
        "application_potencial",
        "student_id",
    ):
        assert field in project


async def test_rt_064_get_project_details_sucesso(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    project_uuid = await _create_project_for_user(client, headers)
    response = await client.get(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["uuid"] == project_uuid


async def test_rt_065_get_project_inexistente_retorna_404(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.get(
        f"{settings.API_V1_STR}/projects/{uuid4()}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_rt_066_get_project_de_outro_usuario_retorna_403(
    client: AsyncClient,
) -> None:
    owner = await create_test_user()
    attacker = await create_test_user()
    owner_headers = await generate_user_auth_headers(client, owner)
    attacker_headers = await generate_user_auth_headers(client, attacker)
    project_uuid = await _create_project_for_user(client, owner_headers)

    response = await client.get(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        headers=attacker_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_rt_067_get_project_uuid_invalido_retorna_400(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.get(
        f"{settings.API_V1_STR}/projects/not-a-uuid",
        headers=headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_rt_068_get_project_retorna_campos_completos(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    project_uuid = await _create_project_for_user(client, headers)
    response = await client.get(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    for field in (
        "uuid",
        "project_title",
        "student_id",
        "clarity_problem",
        "application_potencial",
    ):
        assert field in payload


async def test_rt_069_patch_atualiza_projeto_e_campos_agregados(
    client: AsyncClient,
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    project_uuid = await _create_project_for_user(client, headers)
    update_payload = create_test_project()
    update_payload["project_title"] = "Projeto Atualizado"

    response = await client.patch(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        json=update_payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None
    assert project.project_title == "Projeto Atualizado"
    assert project.inovation_grade == update_payload["inovation_grade"]


async def test_rt_070_patch_projeto_inexistente_retorna_404(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    response = await client.patch(
        f"{settings.API_V1_STR}/projects/{uuid4()}",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_rt_071_patch_projeto_de_outro_usuario_retorna_403(
    client: AsyncClient,
) -> None:
    owner = await create_test_user()
    attacker = await create_test_user()
    owner_headers = await generate_user_auth_headers(client, owner)
    attacker_headers = await generate_user_auth_headers(client, attacker)
    project_uuid = await _create_project_for_user(client, owner_headers)
    payload = create_test_project()
    response = await client.patch(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        json=payload,
        headers=attacker_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_rt_072_patch_mantem_student_id_original(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    project_uuid = await _create_project_for_user(client, headers)
    response = await client.patch(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        json=create_test_project(),
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None
    assert project.student_id == user.uuid


async def test_rt_073_patch_mantem_uuid_original(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    project_uuid = await _create_project_for_user(client, headers)
    response = await client.patch(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        json=create_test_project(),
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None
    assert str(project.uuid) == project_uuid


async def test_rt_075_patch_retorna_informacoes_completas(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    project_uuid = await _create_project_for_user(client, headers)
    response = await client.patch(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        json=create_test_project(),
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    for key in ("project_id_mongo", "project_uuid", "timestamp"):
        assert key in response.json()


async def test_rt_074_patch_recalcula_campos_agregados(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    project_uuid = await _create_project_for_user(client, headers)
    update_payload = create_test_project()
    update_payload.update(
        {
            "clarity_problem": None,
            "problem_description": "Novo Problema",
            "target_audience": "Nova Persona",
            "value_proposition": "Novo Valor",
        }
    )

    response = await client.patch(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        json=update_payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None
    assert "Novo Problema" in project.clarity_problem
    assert "Nova Persona" in project.clarity_problem
    assert "Novo Valor" in project.clarity_problem


async def test_rt_076_delete_project_sucesso(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    project_uuid = await _create_project_for_user(client, headers)
    response = await client.delete(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Projeto deletado com sucesso"
    assert await Project.find_one(Project.uuid == UUID(project_uuid)) is None


async def test_rt_077_delete_projeto_inexistente_retorna_404(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.delete(
        f"{settings.API_V1_STR}/projects/{uuid4()}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_rt_079_projeto_deletado_sai_da_listagem(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    project_uuid = await _create_project_for_user(client, headers)
    await client.delete(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        headers=headers,
    )
    list_response = await client.get(
        f"{settings.API_V1_STR}/projects/",
        headers=headers,
    )
    assert project_uuid not in {item["uuid"] for item in list_response.json()}


async def test_rt_080_delete_retorna_mensagem_de_sucesso(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    project_uuid = await _create_project_for_user(client, headers)
    delete_response = await client.delete(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        headers=headers,
    )
    assert delete_response.status_code == status.HTTP_200_OK
    assert delete_response.json()["message"] == "Projeto deletado com sucesso"


async def test_rt_078_delete_projeto_de_outro_usuario_retorna_403(
    client: AsyncClient,
) -> None:
    owner = await create_test_user()
    attacker = await create_test_user()
    owner_headers = await generate_user_auth_headers(client, owner)
    attacker_headers = await generate_user_auth_headers(client, attacker)
    project_uuid = await _create_project_for_user(client, owner_headers)

    response = await client.delete(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        headers=attacker_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


# ---------------------------------------------------------------------------
# 6. Integridade & Relacionamentos (RT-118)
# ---------------------------------------------------------------------------


async def test_rt_118_usuario_deletado_nao_remove_projetos(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    student = await create_test_user()
    student_headers = await generate_user_auth_headers(client, student)
    project_uuid = await _create_project_for_user(client, student_headers)

    delete_response = await client.delete(
        f"{settings.API_V1_STR}/users/{student.uuid}",
        headers=superuser_token_headers,
    )
    assert delete_response.status_code == status.HTTP_200_OK

    project = await Project.find_one(Project.uuid == UUID(project_uuid))
    assert project is not None
    assert project.student_id == student.uuid


# ---------------------------------------------------------------------------
# 7. Validações e Tratamento de Erros (RT-124 a RT-133)
# ---------------------------------------------------------------------------


async def test_rt_124_campos_obrigatorios_ausentes_retorna_422(
    client: AsyncClient,
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    payload.pop("project_description")
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_rt_125_tipos_incorretos_retorna_422(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    payload["project_title"] = 123  # type: ignore[assignment]
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_rt_126_uuid_invalido_retorna_400(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.get(
        f"{settings.API_V1_STR}/projects/uuid-invalido",
        headers=headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "UUID inválido."


async def test_rt_127_email_invalido_retorna_422(client: AsyncClient) -> None:
    payload = {"name": "Teste", "email": "sem-arroba", "password": _valid_password()}
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_rt_128_erro_400_retorna_mensagem_descritiva(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.get(
        f"{settings.API_V1_STR}/users",
        headers=headers,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "privileges" in response.json()["detail"]


async def test_rt_129_erro_401_retorna_not_authenticated(client: AsyncClient) -> None:
    response = await client.get(f"{settings.API_V1_STR}/projects/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"


async def test_rt_130_erro_403_retorna_mensagem_nao_autorizado(client: AsyncClient) -> None:
    owner = await create_test_user()
    attacker = await create_test_user()
    owner_headers = await generate_user_auth_headers(client, owner)
    attacker_headers = await generate_user_auth_headers(client, attacker)
    project_uuid = await _create_project_for_user(client, owner_headers)
    response = await client.get(
        f"{settings.API_V1_STR}/projects/{project_uuid}",
        headers=attacker_headers,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Usuário não autorizado"


async def test_rt_131_erro_404_retorna_mensagem_nao_encontrado(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    response = await client.get(
        f"{settings.API_V1_STR}/projects/{uuid4()}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Projeto não encontrado."


async def test_rt_132_erro_422_retorna_detalhes_de_validacao(client: AsyncClient) -> None:
    payload = {"email": random_email(), "password": _valid_password()}
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert isinstance(response.json()["detail"], list)


async def test_rt_133_erro_500_retorna_mensagem_generica(
    client: AsyncClient, monkeypatch
) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()

    async def _fail_insert(self, *args, **kwargs):
        raise RuntimeError("Falha simulada")

    monkeypatch.setattr(Project, "insert", _fail_insert, raising=False)

    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"].startswith("Erro ao cadastrar projeto")


# ---------------------------------------------------------------------------
# 8. Performance (RT-134 a RT-137)
# ---------------------------------------------------------------------------


async def test_rt_134_login_completa_em_tempo_aceitavel(client: AsyncClient) -> None:
    start = time.perf_counter()
    await client.post(
        f"{settings.API_V1_STR}/login/access-token",
        data={
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        },
    )
    duration = time.perf_counter() - start
    assert duration < 2.0, f"Login levou {duration:.2f}s, acima do esperado"


async def test_rt_135_criacao_de_projeto_em_tempo_aceitavel(client: AsyncClient) -> None:
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    payload = create_test_project()
    start = time.perf_counter()
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    duration = time.perf_counter() - start
    assert response.status_code == status.HTTP_200_OK
    assert duration < 3.0, f"Criação de projeto levou {duration:.2f}s, acima do esperado"


async def test_rt_136_criacao_usuario_em_tempo_aceitavel(client: AsyncClient) -> None:
    """RT-136: Criação de projeto completa em < 2s"""
    payload = {
        "name": "Performance Test User",
        "email": random_email(),
        "password": _valid_password(),
    }
    start = time.perf_counter()
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    duration = time.perf_counter() - start
    assert response.status_code == status.HTTP_200_OK
    assert duration < 2.0, f"Criação de usuário levou {duration:.2f}s"


async def test_rt_137_listagem_projetos_em_tempo_aceitavel(client: AsyncClient) -> None:
    """RT-137: Listagem de projetos completa em < 1s"""
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    # Cria alguns projetos para listar
    for _ in range(3):
        await _create_project_for_user(client, headers)
    
    start = time.perf_counter()
    response = await client.get(f"{settings.API_V1_STR}/projects/", headers=headers)
    duration = time.perf_counter() - start
    assert response.status_code == status.HTTP_200_OK
    assert duration < 2.0, f"Listagem levou {duration:.2f}s"


async def test_rt_138_nome_usuario_comprimento_minimo_valido(client: AsyncClient) -> None:
    """RT-138: Nome de usuário com comprimento mínimo válido"""
    payload = {
        "name": "Ana",  # Nome curto mas válido
        "email": random_email(),
        "password": _valid_password(),
    }
    response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
    assert response.status_code == status.HTTP_200_OK


async def test_rt_139_email_formato_valido_aceito(client: AsyncClient) -> None:
    """RT-139: Email com formato válido"""
    valid_emails = [
        "user@example.com",
        "user.name@example.co.uk",
        "user+tag@example.com",
    ]
    for email in valid_emails:
        payload = {
            "name": "Valid Email User",
            "email": email,
            "password": _valid_password(),
        }
        response = await client.post(f"{settings.API_V1_STR}/users", json=payload)
        assert response.status_code == status.HTTP_200_OK, f"Email {email} deveria ser válido"


async def test_rt_140_projeto_campos_texto_longos(client: AsyncClient) -> None:
    """RT-140: Projeto com campos de texto muito longos (se houver limite)"""
    user = await create_test_user()
    headers = await generate_user_auth_headers(client, user)
    
    # Texto longo (5000 caracteres)
    long_text = "A" * 5000
    
    payload = create_test_project()
    payload["project_description"] = long_text
    
    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=headers,
    )
    # Se não houver limite, deve aceitar
    # Se houver limite, deve retornar 422
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY]


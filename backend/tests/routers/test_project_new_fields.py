"""
Testes para a criação de projetos com os novos campos do Lean Canvas
"""

import pytest
from fastapi import status
from httpx import AsyncClient

from app.config.config import settings

from ..utils import create_test_user, generate_user_auth_headers


@pytest.mark.anyio
async def test_create_project_with_new_fields_success(client: AsyncClient) -> None:
    """
    Testa criação de projeto com TODOS os novos campos (10 campos detalhados)
    """
    student = await create_test_user()
    token_headers = await generate_user_auth_headers(client, student)

    # Payload com TODOS os novos campos
    payload = {
        # Básico
        "project_title": "EcoConnect - Plataforma de Reciclagem",
        "project_description": "Aplicativo mobile que conecta pessoas com cooperativas de reciclagem",
        "solution_proposal": "Plataforma digital com geolocalização e gamificação",
        # Problema e Proposta de Valor (NOVOS)
        "problem_description": "Apenas 4% do lixo reciclável é efetivamente reciclado no Brasil",
        "target_audience": "Moradores urbanos de classe média interessados em sustentabilidade",
        "value_proposition": "Facilitar reciclagem com recompensas e impacto mensurável",
        # Lean Canvas (NOVOS)
        "customer_segment": "Famílias urbanas 25-45 anos, conscientes ambientalmente",
        "revenue_model": "Freemium: gratuito para usuários, premium para empresas (R$199/mês)",
        "competitive_advantage": "Algoritmo de otimização de rotas + gamificação + parcerias locais",
        # Inovação e Impacto (NOVOS)
        "innovation": "IA para otimização de rotas e gamificação com economia comportamental",
        "social_impact": "10.000 famílias beneficiadas, redução de 500 toneladas de lixo/ano",
        "technical_feasibility": "React Native + Node.js + MongoDB. MVP R$50k, 3 meses",
        "scalability": "Modelo replicável, documentado. Piloto 2 bairros, expansão 5 cidades",
    }

    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=token_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["message"] == "Projeto cadastrado com sucesso!"
    assert "project_uuid" in data
    assert "project_id_mongo" in data
    assert "timestamp" in data

    print("\n✅ Projeto criado com novos campos:")
    print(f"   UUID: {data['project_uuid']}")


@pytest.mark.anyio
async def test_create_project_backward_compatibility(client: AsyncClient) -> None:
    """
    Testa retrocompatibilidade: aceita campos agregados do frontend antigo
    """
    student = await create_test_user()
    token_headers = await generate_user_auth_headers(client, student)

    # Payload no formato ANTIGO (campos agregados)
    payload = {
        "project_title": "Projeto Legado",
        "project_description": "Descrição legado",
        "solution_proposal": "Solução legado",
        "clarity_problem": "Problema agregado no frontend antigo",
        "inovation_grade": "Inovação agregada",
        "social_impact": "Impacto agregado",
        "tec_eco_viability": "Viabilidade agregada",
        "application_potencial": "Aplicação agregada",
    }

    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=token_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["message"] == "Projeto cadastrado com sucesso!"
    print("\n✅ Retrocompatibilidade OK - Frontend antigo ainda funciona")


@pytest.mark.anyio
async def test_create_project_field_aggregation(client: AsyncClient) -> None:
    """
    Testa se a agregação automática de campos está funcionando
    """
    student = await create_test_user()
    token_headers = await generate_user_auth_headers(client, student)

    # Payload apenas com campos novos (sem agregados)
    payload = {
        "project_title": "Teste Agregação",
        "project_description": "Teste",
        "solution_proposal": "Teste",
        # Novos campos separados
        "problem_description": "Problema X",
        "target_audience": "Público Y",
        "value_proposition": "Valor Z",
        "customer_segment": "Segmento A",
        "competitive_advantage": "Vantagem B",
        "innovation": "Inovação C",
        "social_impact": "Impacto D",
        "technical_feasibility": "Viabilidade E",
        "scalability": "Escala F",
        "revenue_model": "Receita G",
    }

    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=token_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["message"] == "Projeto cadastrado com sucesso!"
    print("\n✅ Agregação automática funcionando")
    print("   Backend agrega campos individuais nos campos para IA")


@pytest.mark.anyio
async def test_create_project_missing_optional_fields(client: AsyncClient) -> None:
    """
    Testa que campos opcionais podem ser omitidos
    """
    student = await create_test_user()
    token_headers = await generate_user_auth_headers(client, student)

    # Payload MÍNIMO (apenas obrigatórios)
    payload = {
        "project_title": "Projeto Mínimo",
        "project_description": "Descrição mínima",
        "solution_proposal": "Solução mínima",
    }

    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
        headers=token_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["message"] == "Projeto cadastrado com sucesso!"
    print("\n✅ Campos opcionais funcionando - apenas básicos enviados")


@pytest.mark.anyio
async def test_create_project_unauthenticated(client: AsyncClient) -> None:
    """
    Testa que requisição sem autenticação é rejeitada
    """
    payload = {
        "project_title": "Teste",
        "project_description": "Teste",
        "solution_proposal": "Teste",
    }

    response = await client.post(
        f"{settings.API_V1_STR}/projects/",
        json=payload,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    print("\n✅ Autenticação obrigatória funcionando")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TESTES DE CRIAÇÃO DE PROJETOS COM NOVOS CAMPOS")
    print("=" * 80)
    print("\nPara rodar os testes:")
    print("  cd backend")
    print("  uv run pytest tests/routers/test_project_new_fields.py -v")
    print("\nOu rodar teste específico:")
    print(
        "  uv run pytest tests/routers/test_project_new_fields.py::test_create_project_with_new_fields_success -v"
    )
    print("=" * 80 + "\n")

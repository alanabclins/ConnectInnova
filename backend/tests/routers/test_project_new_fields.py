"""
Testes para a criação de projetos com os novos campos do Lean Canvas
"""

import pytest
from fastapi import status
from httpx import AsyncClient

from app.config.config import settings

from ..utils import create_test_user, generate_user_auth_headers


@pytest.mark.anyio
async def test_create_project_with_all_detailed_fields_success(client: AsyncClient) -> None:
    """
    Testa criação de projeto com TODOS os 15 campos detalhados + 3 campos pessoais (Passo 5)
    """
    student = await create_test_user()
    token_headers = await generate_user_auth_headers(client, student)

    # Payload completo com todos os campos detalhados e pessoais
    payload = {
        # Básico
        "project_title": "EcoConnect - Plataforma de Reciclagem",
        "project_description": "Aplicativo mobile que conecta pessoas com cooperativas de reciclagem",
        "solution_proposal": "Plataforma digital com geolocalização e gamificação",
        # Problema e Proposta de Valor (Passo 2)
        "problem_description": "Apenas 4% do lixo reciclável é efetivamente reciclado no Brasil",
        "target_audience": "Moradores urbanos de classe média interessados em sustentabilidade",
        "value_proposition": "Facilitar reciclagem com recompensas e impacto mensurável",
        # Lean Canvas (Passo 3)
        "customer_segment": "Famílias urbanas 25-45 anos, conscientes ambientalmente",
        "revenue_model": "Freemium: gratuito para usuários, premium para empresas (R$199/mês)",
        "competitive_advantage": "Algoritmo de otimização de rotas + gamificação + parcerias locais",
        # Inovação e Impacto (Passo 4)
        "innovation": "IA para otimização de rotas e gamificação com economia comportamental",
        "social_impact": "10.000 famílias beneficiadas, redução de 500 toneladas de lixo/ano",
        "technical_feasibility": "React Native + Node.js + MongoDB. MVP R$50k, 3 meses",
        "scalability": "Modelo replicável, documentado. Piloto 2 bairros, expansão 5 cidades",
        # Informações Pessoais (Passo 5 - Adicionado)
        "who_are_you": "Sou um engenheiro de software com foco em impacto social.",
        "academy_info": "Mestrado em Gestão Ambiental pela USP, Bacharel em Eng. da Computação.",
        "market_info": "Experiência de 5 anos em desenvolvimento de apps e 2 em gestão de ONGs.",
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


@pytest.mark.anyio
async def test_create_project_field_aggregation(client: AsyncClient) -> None:
    """
    Testa se a agregação automática de campos está funcionando quando enviados apenas os campos detalhados.
    """
    student = await create_test_user()
    token_headers = await generate_user_auth_headers(client, student)

    # Payload apenas com campos detalhados (sem os campos agregados)
    payload = {
        "project_title": "Teste Agregação",
        "project_description": "Descrição Teste",
        "solution_proposal": "Solução Teste",
        "problem_description": "Problema X",
        "target_audience": "Público Y",
        "value_proposition": "Valor Z",
        "customer_segment": "Segmento A",
        "revenue_model": "Receita G",
        "competitive_advantage": "Vantagem B",
        "innovation": "Inovação C",
        "social_impact": "Impacto D",
        "technical_feasibility": "Viabilidade E",
        "scalability": "Escala F",
        "who_are_you": "Eu mesmo",
        "academy_info": "Nenhuma",
        "market_info": "Nenhuma",
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


@pytest.mark.anyio
async def test_create_project_missing_detailed_fields(client: AsyncClient) -> None:
    """
    Testa que campos detalhados OPCIONAIS podem ser omitidos, mas os obrigatórios (Passo 5)
    devem ser enviados (mesmo que vazios, dependendo do schema).
    """
    student = await create_test_user()
    token_headers = await generate_user_auth_headers(client, student)

    # Payload MÍNIMO (apenas obrigatórios e os campos vazios que o schema Pydantic espera)
    payload = {
        "project_title": "Projeto Mínimo",
        "project_description": "Descrição mínima",
        "solution_proposal": "Solução mínima",
        # Campos que devem estar presentes, mesmo que vazios, se não forem Optional[str] = None no Schema
        "problem_description": "",
        "target_audience": "",
        "value_proposition": "",
        "customer_segment": "",
        "revenue_model": "",
        "competitive_advantage": "",
        "innovation": "",
        "social_impact": "",
        "technical_feasibility": "",
        "scalability": "",
        # NOVOS Campos Pessoais (Passo 5 - Adicionado)
        "who_are_you": "Mínimo",
        "academy_info": "Mínimo",
        "market_info": "Mínimo",
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

import random
import string

from httpx import AsyncClient

from app.auth.auth import create_access_token, get_hashed_password
from app.config.config import settings
from app.models.users import User


async def get_user_auth_headers(
    client: AsyncClient, email: str, password: str
) -> dict[str, str]:
    """
    Dado email e senha de usuário, realiza login e retorna headers de autorização.
    """
    data = {"username": email, "password": password}
    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def generate_user_auth_headers(client: AsyncClient, user: User) -> dict[str, str]:
    """
    Gera token de acesso para um usuário existente e retorna headers de autorização.
    """
    access_token = create_access_token(user.uuid)
    return {"Authorization": f"Bearer {access_token}"}


def random_lower_string() -> str:
    """Gera uma string aleatória de 32 caracteres minúsculos"""
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    """Gera um email aleatório para testes"""
    return f"{random_lower_string()}@{random_lower_string()}.com"


async def create_test_user() -> User:
    """
    Cria um usuário de teste no banco de dados e retorna o objeto criado.
    """
    email = random_email()
    hashed_password = get_hashed_password(random_lower_string())
    user = User(name="teste", email=email, hashed_password=hashed_password)
    await user.create()
    return user


def random_sentence() -> str:
    """Gera uma frase aleatória curta para campos de teste"""
    words = [
        random.choice(
            [
                "melhorar",
                "sistema",
                "conectar",
                "estudante",
                "empresa",
                "plataforma",
                "solução",
            ]
        )
        for _ in range(random.randint(3, 8))
    ]
    sentence = " ".join(words).capitalize() + "."
    return sentence


def create_test_project() -> dict:
    """Gera um payload dinâmico para a criação de um projeto."""
    # Simula a criação de dados dinâmicos como a função create_test_project faria
    suffix = "".join(random.choices(string.ascii_lowercase, k=8))
    return {
        # Informações Básicas e Essenciais
        "project_title": f"Título Dinâmico - {suffix}",
        "project_description": f"Descrição Geral do Projeto {suffix}",
        "solution_proposal": f"Proposta de Solução Detalhada {suffix}",
        # Passo 2: Problema e Proposta de Valor
        "problem_description": f"O problema de mercado é: {suffix}",
        "target_audience": f"Público-alvo principal: {suffix}",
        "value_proposition": f"Proposta de Valor Única: {suffix}",
        # Passo 3: Modelo de Negócio (Lean Canvas)
        "customer_segment": f"Segmento de Clientes: {suffix}",
        "revenue_model": f"Modelo de Receita: {suffix}",
        "competitive_advantage": f"Vantagem Competitiva: {suffix}",
        # Passo 4: Inovação e Impacto
        "innovation": f"Inovação tecnológica: {suffix}",
        "social_impact": f"Impacto Social e Ambiental: {suffix}",
        "technical_feasibility": f"Viabilidade Técnica: {suffix}",
        "scalability": f"Potencial de Escalabilidade: {suffix}",
        # Passo 5: Informações Pessoais
        "who_are_you": f"Quem sou eu: {suffix}",
        "academy_info": f"Informações Acadêmicas: {suffix}",
        "market_info": f"Informações de Mercado/Currículo: {suffix}",
        # Campos de Agregação (usados pela IA e que devem ser preenchidos na submissão)
        "clarity_problem": f"Clareza do Problema (Agregado): {suffix}",
        "inovation_grade": f"Grau de Inovação (Agregado): {suffix}",
        "social_impact_aggregated": f"Impacto Social (Agregado): {suffix}",
        "tec_eco_viability": f"Viabilidade Técnica/Econômica (Agregada): {suffix}",
        "application_potencial": f"Potencial de Aplicação (Agregado): {suffix}",
    }

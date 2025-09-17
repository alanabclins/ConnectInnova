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
    user = User(email=email, hashed_password=hashed_password)
    await user.create()
    return user

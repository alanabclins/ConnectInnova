import random
import string

from httpx import AsyncClient

from app.auth.auth import create_access_token, get_hashed_password
from app.config.config import settings
from app.models.users import User
from app.models.projects import Project


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

def random_sentence() -> str:
    """Gera uma frase aleatória curta para campos de teste"""
    words = [random.choice(["melhorar", "sistema", "conectar", "estudante", "empresa", "plataforma", "solução"]) 
             for _ in range(random.randint(3, 8))]
    sentence = " ".join(words).capitalize() + "."
    return sentence


async def create_test_project(student: User) -> Project:
    """
    Cria um projeto de teste no banco de dados ligado a um usuário existente.
    """
    project = Project(
        project_title=random_sentence(),
        project_description=random_sentence(),
        solution_proposal=random_sentence(),
        clarity_problem=random_sentence(),
        inovation_grade=random_sentence(),
        social_impact=random_sentence(),
        tec_eco_viability=random_sentence(),
        application_potencial=random_sentence(),
        student_id=student.id,
    )
    await project.create()
    return project

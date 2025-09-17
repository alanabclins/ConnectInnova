from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from .auth.auth import get_hashed_password
from .config.config import settings
from .models.users import User
from .routers.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager para o FastAPI. Inicializa conexão com MongoDB Atlas
    e cria o superuser caso não exista.
    """
    # Setup MongoDB Atlas usando URI completa
    app.state.client = AsyncIOMotorClient(settings.MONGO_URI)

    # Seleciona o banco correto (padrão ou de teste)
    mongo_db_name = getattr(settings, "MONGO_DB", "default_db")
    await init_beanie(
        database=app.state.client[mongo_db_name],
        document_models=[User],
    )

    # Criação do superuser se não existir
    user = await User.find_one({"email": settings.FIRST_SUPERUSER})
    if not user:
        user = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_hashed_password(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
        )
        await user.create()

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Configura CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Inclui routers
app.include_router(api_router, prefix=settings.API_V1_STR)

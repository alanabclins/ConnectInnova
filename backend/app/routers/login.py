import secrets
from datetime import timedelta, datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_sso.sso.google import GoogleSSO
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app import models, schemas
from app.auth.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_user_from_cookie,
    get_hashed_password
)
from app.config.config import settings
from app.config.email import send_password_reset_email

PASSWORD_RESET_EXPIRE_HOURS = 1

FRONTEND_URL = settings.FRONTEND_URL

router = APIRouter()


def get_google_sso() -> GoogleSSO:
    if settings.GOOGLE_CLIENT_ID is None or settings.GOOGLE_CLIENT_SECRET is None:
        raise HTTPException(status_code=400, detail="Google SSO not enabled.")
    return GoogleSSO(
        settings.GOOGLE_CLIENT_ID,
        settings.GOOGLE_CLIENT_SECRET,
        f"{settings.SSO_CALLBACK_HOSTNAME}{settings.API_V1_STR}/login/google/callback",
    )


@router.post("/access-token", response_model=schemas.Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.uuid, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/test-token", response_model=schemas.User)
async def test_token(current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.get("/refresh-token", response_model=schemas.Token)
async def refresh_token(
    current_user: models.User = Depends(get_current_user_from_cookie),
) -> Any:
    """
    Return a new token for current user
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(current_user.uuid, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/google")
async def google_login(google_sso: GoogleSSO = Depends(get_google_sso)):
    """
    Generate login url and redirect
    """
    return await google_sso.get_login_redirect()


@router.get("/google/callback")
async def google_callback(request: Request, google_sso: GoogleSSO = Depends(get_google_sso)):
    """
    Process login response from Google and return user info
    """
    if settings.SSO_LOGIN_CALLBACK_URL is None:
        raise HTTPException(
            status_code=400,
            detail="SSO Login callback url is not set. Google SSO not enabled.",
        )

    # Get user details from Google
    google_user = await google_sso.verify_and_process(request)

    if google_user is None:
        raise HTTPException(status_code=400, detail="Google SSO verification process failed.")

    # Check if user is already created in DB
    user = await models.User.find_one({"email": google_user.email})
    if user is None:
        # If user does not exist, create it in DB
        user = models.User(
            email=google_user.email if google_user.email is not None else "",
            first_name=google_user.first_name,
            name=google_user.display_name if google_user.display_name is not None else "",
            last_name=google_user.last_name,
            picture=google_user.picture,
            provider=google_user.provider,
        )
        user = await user.create()

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Login user by creating access_token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.uuid, expires_delta=access_token_expires)
    response = RedirectResponse(settings.SSO_LOGIN_CALLBACK_URL)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=120,
        expires=120,
    )
    return response

@router.post("/request-password-reset")
async def request_password_reset(body: schemas.EmailSchema, background_tasks: BackgroundTasks):
    """
    Inicia o fluxo de redefinição de senha.
    """
    user = await models.User.find_one({"email": body.email})

    # Resposta genérica por segurança, mesmo se o usuário não existir
    if user:
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=PASSWORD_RESET_EXPIRE_HOURS)

        # Atualiza o documento do usuário com o token
        user.reset_token = token
        user.reset_token_expires = expires_at
        await user.save()

        # Monta os links
        reset_link = f"{FRONTEND_URL}/reset-password?token={token}"
        cancel_link = f"{settings.SSO_CALLBACK_HOSTNAME}{settings.API_V1_STR}/login/cancel-reset?token={token}"

        background_tasks.add_task(
            send_password_reset_email,
            email_to=user.email,
            reset_link=reset_link, 
            cancel_link=cancel_link
        )

    return {"message": "Se uma conta com este e-mail existir, um link de redefinição foi enviado."}


@router.post("/reset-password")
async def reset_password(body: schemas.PasswordResetSchema): # Schema com 'token' e 'new_password'
    """
    Finaliza a redefinição de senha com o token e a nova senha.
    """
    
    # Encontra o usuário pelo token E verifica a data de expiração
    user = await models.User.find_one({
        "reset_token": body.token,
        "reset_token_expires": {"$gt": datetime.now(timezone.utc)}
    })

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Token inválido ou expirado"
        )

    # Atualiza a senha e limpa os campos de token
    user.hashed_password = get_hashed_password(body.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    await user.save()

    return {"message": "Senha redefinida com sucesso!"}


@router.get("/cancel-reset")
async def cancel_password_reset(token: str):
    user = await models.User.find_one({"reset_token": token})

    if user:
        # Apenas limpa os campos do token
        user.reset_token = None
        user.reset_token_expires = None
        await user.save()

    # Retorna uma mensagem (ou redireciona para uma página de sucesso no frontend)
    return """
    <html>
        <head>
            <title>Solicitação Cancelada</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding-top: 50px; }
                h1 { color: #d9534f; }
            </style>
        </head>
        <body>
            <h1>Solicitação Cancelada</h1>
            <p>O link de redefinição de senha foi invalidado com sucesso.</p>
            <p>Sua conta permanece segura.</p>
        </body>
    </html>
    """
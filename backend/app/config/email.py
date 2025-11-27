from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    
    # Configuração crítica para Gmail (Porta 587):
    MAIL_STARTTLS=True,      # Deve ser True
    MAIL_SSL_TLS=False,      # Deve ser False
    
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_password_reset_email(email_to: str, reset_link: str, cancel_link: str):
    """
    Envia o e-mail de redefinição de senha usando um template HTML simples.
    """
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #eee; padding: 20px; border-radius: 5px;">
            <h2 style="color: #333;">Redefinição de Senha</h2>
            <p>Olá,</p>
            <p>Recebemos uma solicitação para redefinir a senha da sua conta.</p>
            <p>Clique no botão abaixo para criar uma nova senha:</p>
            
            <a href="{reset_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0;">
                Redefinir Minha Senha
            </a>
            
            <p>Se o botão não funcionar, copie e cole este link no seu navegador:</p>
            <p style="color: #555; font-size: 12px;">{reset_link}</p>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            
            <p style="font-size: 12px; color: #777;">
                Se você não solicitou essa alteração, <a href="{cancel_link}" style="color: #d9534f;">clique aqui para cancelar e invalidar este link</a>.
            </p>
        </div>
    </body>
    </html>
    """

    message = MessageSchema(
        subject="Redefinição de Senha - Sua App",
        recipients=[email_to],
        body=html_content,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
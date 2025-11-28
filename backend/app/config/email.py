from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_password_reset_email(email_to: str, reset_link: str, cancel_link: str):
    # ---------------------------------------------------------
    # CONFIGURAÇÃO DE BRANDING (DARK MODE)
    # ---------------------------------------------------------
    # Lembre-se de colocar o link real da sua logo aqui!
    logo_url = "https://imgur.com/xqN3VG9.png" 
    
    app_name = "ConnectInnova"
    primary_color = "#2563EB"   # Azul (Botão)
    
    # NOVAS CORES DARK MODE
    bg_color = "#09090b"        # Fundo principal (Preto quase total)
    card_bg_color = "#18181b"   # Fundo do cartão (Cinza escuro)
    text_main = "#ffffff"       # Texto principal (Branco)
    text_secondary = "#a1a1aa"  # Texto secundário (Cinza claro)
    border_color = "#27272a"    # Cor das bordas e linhas

    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="color-scheme" content="dark">
        <meta name="supported-color-schemes" content="dark">
        <title>Redefinição de Senha</title>
        <style>
            /* Reset e Estilos Base */
            body {{ margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: {bg_color}; color: {text_main}; -webkit-font-smoothing: antialiased; word-break: break-word; }}
            
            /* Containers */
            .wrapper {{ width: 100%; table-layout: fixed; background-color: {bg_color}; padding-bottom: 40px; }}
            .container {{ max-width: 600px; margin: 0 auto; }}
            .card {{ background-color: {card_bg_color}; padding: 40px; border-radius: 12px; border: 1px solid {border_color}; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5); }}
            
            /* Elementos */
            h1 {{ color: {text_main}; font-size: 24px; font-weight: bold; margin: 0 0 20px; }}
            p {{ font-size: 16px; line-height: 1.6; margin: 0 0 20px; color: {text_secondary}; }}
            
            /* Botão */
            .button {{ background-color: {primary_color}; color: #ffffff !important; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block; margin: 25px 0; transition: background-color 0.3s ease; }}
            .button span {{ color: #ffffff !important; }} /* Garante texto branco no Gmail */
            .button:hover {{ background-color: #1d4ed8; }}

            /* Links e Footer */
            .link-secondary {{ color: {primary_color}; text-decoration: none; word-break: break-all; font-size: 13px; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: {text_secondary}; text-align: center; }}
            .cancel-link {{ color: #ef4444; text-decoration: underline; }}
            hr {{ border: none; border-top: 1px solid {border_color}; margin: 30px 0; }}

            /* Responsividade */
            @media only screen and (max-width: 600px) {{
                .card {{ padding: 30px 20px; }}
                .button {{ width: 100%; box-sizing: border-box; }}
            }}
        </style>
    </head>
    <body style="background-color: {bg_color}; margin: 0; padding: 0;">
        <center class="wrapper">
            <div class="container">
                <div style="padding: 40px 0 30px; text-align: center;">
                    <img src="{logo_url}" alt="{app_name}" width="auto" height="40" style="height: 40px; border: 0; outline: none; text-decoration: none; display: block; margin: 0 auto;" />
                    <h2 style="color: {text_main}; margin: 10px 0 0; font-size: 22px; display: none; mso-hide: all;">{app_name}</h2>
                </div>

                <div class="card">
                    <h1>Redefina sua senha</h1>
                    
                    <p>
                        Olá! Recebemos uma solicitação para alterar a senha da sua conta na <strong style="color: {text_main};">{app_name}</strong>.
                    </p>

                    <a href="{reset_link}" class="button" target="_blank">
                        <span>Redefinir Senha Agora</span>
                    </a>
                    
                    <p style="font-size: 14px; margin-bottom: 0;">
                        Este link é válido por 30 minutos.
                    </p>
                </div>

                <div class="footer">
                    <p style="margin-bottom: 10px;">Não solicitou essa mudança?</p>
                    <a href="{cancel_link}" class="cancel-link" target="_blank">Clique aqui para cancelar e proteger sua conta.</a>
                    <p style="margin-top: 30px; opacity: 0.7;">&copy; 2025 {app_name}. Todos os direitos reservados.</p>
                </div>
            </div>
        </center>
    </body>
    </html>
    """

    message = MessageSchema(
        subject=f"Redefinição de Senha - {app_name}",
        recipients=[email_to],
        body=html_content,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
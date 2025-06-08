import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

def send_admin_confirmation_email(to_email: str, token: str):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    FRONTEND_URL = os.getenv("FRONTEND_URL")
    confirm_url = f"{FRONTEND_URL}/admin-confirm?token={token}"

    subject = "Alerta de inicio de sesión en FUNDAPMACOE"
    confirm_url = f"{FRONTEND_URL}/admin-confirm?token={token}"
    logo_url = f"{os.getenv('FRONTEND_URL')}/Logo.png"
    body = f"""
    <div style='font-family:sans-serif;max-width:500px;margin:auto;background:#fff;border-radius:12px;box-shadow:0 2px 8px #e67e2240;padding:32px 24px;'>
      <div style='text-align:center;margin-bottom:24px;'>
        <img src='{logo_url}' alt='Logo FundapMacoe' style='height:70px;margin-bottom:8px;display:block;margin-left:auto;margin-right:auto;' />
        <h1 style='color:#e67e22;margin:0;font-size:2rem;'>FUNDAPMACOE</h1>
      </div>
      <h2 style='color:#222;margin-bottom:16px;'>Solicitud de acceso de administrador</h2>
      <p style='font-size:1.1rem;color:#444;'>Hola,</p>
      <p style='font-size:1.1rem;color:#444;'>Se ha solicitado iniciar sesión en la plataforma <b>FUNDAPMACOE</b> con tu cuenta de administrador.</p>
      <p style='font-size:1.1rem;color:#444;'>Si fuiste tú, por favor confirma el acceso haciendo clic en el siguiente botón:</p>
      <div style='margin:32px 0;text-align:center;'>
        <a href='{confirm_url}' style='background:#e67e22;color:#fff;padding:16px 32px;border-radius:8px;text-decoration:none;font-size:1.1rem;font-weight:bold;box-shadow:0 2px 8px #e67e2240;display:inline-block;'>Confirmar acceso</a>
      </div>
      <p style='font-size:1rem;color:#888;'>Si no fuiste tú, ignora este correo y tu cuenta estará segura.</p>
      <hr style='margin:32px 0;border:none;border-top:1px solid #eee;'>
      <div style='text-align:center;font-size:0.95rem;color:#aaa;'>
        Este mensaje es automático. No respondas a este correo.<br>
        &copy; {2025} FUNDAPMACOE
      </div>
    </div>
    <!--[if mso]><p style='color:#444;font-size:1.1rem;'>Si no ves el botón, copia y pega este enlace en tu navegador:<br>{confirm_url}</p><![endif]-->
    <p style='color:#444;font-size:1.1rem;'>Si no ves el botón, copia y pega este enlace en tu navegador:<br><span style='word-break:break-all'>{confirm_url}</span></p>
    """

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to_email, msg.as_string())
        logging.info(f"Correo de confirmación enviado a {to_email}")
    except Exception as e:
        logging.error(f"Error enviando correo de confirmación admin: {e}")
        print(f"Error enviando correo de confirmación admin: {e}")

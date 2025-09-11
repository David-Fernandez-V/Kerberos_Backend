import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_confirmation_email(to_email: str):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    subject = "Cuenta verificada"
    base_url = os.getenv("BASE_URL")
    login_link = f"{base_url}/LogIn"

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject

    body = f"""
    <h2>Tu cuenta ha sido verificada</h2>
    <p>¡Bienvenido! Ahora puedes gestionar todas tus cuentas y contraseñas desde Kerberos.</p>
    <a href="{login_link}">Iniciar sesión</a>
    """
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_verification_email(to_email: str, token: str):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")  # App password de Gmail u otro proveedor
    subject = "Verifica tu cuenta"
    verification_link = f"http://localhost:3000/verify?token={token}"  # frontend

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject

    body = f"""
    <h2>Bienvenido</h2>
    <p>Gracias por registrarte. Por favor haz clic en el siguiente enlace para verificar tu cuenta:</p>
    <a href="{verification_link}">Verificar cuenta</a>
    """
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())

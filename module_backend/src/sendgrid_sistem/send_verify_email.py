import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import base64

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("EMAIL_USER")
BASE_URL = os.getenv("BASE_URL")


def send_verification_email(to_email: str, token: str):
    subject = "Verifica tu cuenta"
    verification_link = f"{BASE_URL}/verify?token={token}"

    # HTML del correo
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; text-align: center;">
        <img src="https://raw.githubusercontent.com/David-Fernandez-V/Kerberos_Frontend/main/public/kerberos_logo.png" alt="Kerberos Logo" height="150"><br>
        <h2>Bienvenido a <span style='color:#0078D7;'>Kerberos</span></h2>
        <p>Gracias por registrarte. Por favor haz clic en el siguiente enlace para verificar tu cuenta:</p>
        <a href="{verification_link}" 
           style="display:inline-block; background-color:#0078D7; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">
           Verificar cuenta
        </a>
        <p style="margin-top:20px; color:gray; font-size:12px;">
          Si no creaste una cuenta, puedes ignorar este mensaje.
        </p>
      </body>
    </html>
    """

    # Crear el mensaje
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    # (Opcional) Si quieres adjuntar la imagen localmente:
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # image_path = os.path.join(BASE_DIR, "kerberos_logo.png")
    # with open(image_path, "rb") as f:
    #     data = f.read()
    #     encoded = base64.b64encode(data).decode()
    # attachment = Attachment(
    #     FileContent(encoded),
    #     FileName("kerberos_logo.png"),
    #     FileType("image/png"),
    #     Disposition("inline")
    # )
    # message.attachment = attachment

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Correo enviado a {to_email}. Código de respuesta: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False

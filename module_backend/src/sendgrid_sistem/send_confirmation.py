import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

def send_confirmation_email(to_email: str):
    base_url = os.getenv("BASE_URL")
    login_link = f"{base_url}/LogIn"
    subject = "Cuenta verificada"
    
    # Cuerpo HTML del correo
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; text-align: center;">
        <img src="cid:logo" alt="Kerberos Logo" height="150"><br>
        <h2>Tu cuenta ha sido verificada ✅</h2>
        <p>¡Bienvenido a <b>Kerberos</b>! Ahora puedes gestionar todas tus contraseñas y cuentas de manera segura.</p>
        <p>
          <a href="{login_link}" 
             style="background-color: #4A90E2; color: white; padding: 10px 20px; 
                    text-decoration: none; border-radius: 6px; display: inline-block;">
             Iniciar sesión
          </a>
        </p>
        <p style="font-size: 12px; color: #555;">Si no solicitaste este correo, puedes ignorarlo.</p>
      </body>
    </html>
    """

    message = Mail(
        from_email=os.getenv("EMAIL_USER"),
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    # Adjuntar imagen (Kerberos logo)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "kerberos_logo.png")

    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()

        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType("image/png")
        attachment.file_name = FileName("kerberos_logo.png")
        attachment.disposition = Disposition("inline")

        # Agregar imagen al mensaje
        message.attachment = attachment

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"Email de confirmación enviado a {to_email} (status: {response.status_code})")
    except Exception as e:
        print(f"Error enviando correo de confirmación: {str(e)}")
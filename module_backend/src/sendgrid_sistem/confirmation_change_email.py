import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, FileContent, FileName, FileType, Disposition

def send_confirmation_change_email(to_email: str):
    sender = os.getenv("EMAIL_USER")  # Correo verificado en SendGrid
    base_url = os.getenv("BASE_URL")
    subject = "Cambio de correo confirmado"
    login_link = f"{base_url}/LogIn"

    # Contenido HTML del correo
    html_body = f"""
    <html>
      <body>
        <img src="cid:logo" alt="Kerberos Logo" height="150"><br>
        <h2>Tu correo ha sido cambiado</h2>
        <p>Este es el nuevo correo asociado a tu cuenta de Kerberos. Tu anterior correo ha sido eliminado de nuestra base de datos.</p>
        <a href="{login_link}">Iniciar sesión</a>
      </body>
    </html>
    """

    # Crear el mensaje
    message = Mail(
        from_email=sender,
        to_emails=to_email,
        subject=subject,
        html_content=html_body
    )

    # Adjuntar imagen inline (logo)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "kerberos_logo.png")

    with open(image_path, "rb") as img_file:
        encoded_img = base64.b64encode(img_file.read()).decode()
        inline_image = InlineImage(
            FileContent(encoded_img),
            FileName("kerberos_logo.png"),
            FileType("image/png"),
            Disposition("inline"),
            content_id="logo"
        )
        message.attachment = inline_image

    # Envío del correo
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"[SendGrid] Email enviado correctamente a {to_email}. Status code: {response.status_code}")
    except Exception as e:
        print(f"[SendGrid] Error al enviar email: {str(e)}")

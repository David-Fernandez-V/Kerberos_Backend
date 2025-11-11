import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, FileContent, FileName, FileType, Disposition
import base64

def send_changemail_email(to_email: str, token: str):
    sender = os.getenv("EMAIL_USER")  # Remitente (verificado en SendGrid)
    base_url = os.getenv("BASE_URL")
    subject = "Cambio de correo electrónico"
    verification_link = f"{base_url}/emailChange?token={token}"

    # HTML del correo
    html_body = f"""
    <html>
      <body>
        <img src="cid:logo" alt="Kerberos Logo" height="150"><br>
        <h2>Kerberos: Cambio de correo electrónico</h2>
        <p>Has solicitado un cambio de correo electrónico. Por favor haz clic en el siguiente enlace para verificar este correo.</p>
        <p><b>Nota:</b> Para poder acceder al enlace deberás tener iniciada tu sesión en la página web de Kerberos.</p>
        <a href="{verification_link}">Verificar cambio de correo</a>
      </body>
    </html>
    """

    # Crear mensaje
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

    # Envío
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"[SendGrid] Email enviado correctamente a {to_email}. Status code: {response.status_code}")
    except Exception as e:
        print(f"[SendGrid] Error al enviar email: {str(e)}")
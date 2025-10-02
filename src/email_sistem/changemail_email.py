import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def send_changemail_email(to_email: str, token: str):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    base_url = os.getenv("BASE_URL")
    subject = "Cambio de correo"
    verification_link = f"{base_url}/emailChange?token={token}"

    msg = MIMEMultipart("related")
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject

    alternative = MIMEMultipart("alternative")
    msg.attach(alternative)

    #HTML
    html_body = f"""
    <html>
      <body>
        <img src="cid:logo" alt="Kerberos Logo" height="150"><br>
        <h2>Kerberos: Cambio de correo electrónico</h2>
        <p>Has solicitado un cambio de correo electrónico. Por favor haz clic en el siguiente enlace para verificar este correo.</p>
        <p>Para poder acceder a este link tendras que tener iniciada tu seisón en la página web de Kerberos.</p>
        <a href="{verification_link}">Verificar cambio de correo</a>
      </body>
    </html>
    """
    alternative.attach(MIMEText(html_body, "html"))

    # Adjuntar imagen
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print(BASE_DIR)
    image_path = os.path.join(BASE_DIR, "kerberos_logo.png")
    with open(image_path, "rb") as img_file:
        img = MIMEImage(img_file.read())
        img.add_header("Content-ID", "<logo>")
        img.add_header("Content-Disposition", "inline", filename=os.path.basename(image_path))
        msg.attach(img)

    # Envío
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())
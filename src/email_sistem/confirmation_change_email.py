from email.mime.image import MIMEImage
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_confirmation_change_email(to_email: str):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    subject = "Cambio de Correo"
    base_url = os.getenv("BASE_URL")
    login_link = f"{base_url}/LogIn"

    msg = MIMEMultipart("related")
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject

    alternative = MIMEMultipart("alternative")
    msg.attach(alternative)

    html_body = f"""
    <html>
      <body>
        <img src="cid:logo" alt="Kerberos Logo" height="150"><br>
        <h2>Tu correo ha sido cambiado</h2>
        <p>Este es el nuevo correo asociado a tu cuenta de kerberos. Tu anterior correo ha sido eliminado de nuestra base de datos.</p>
        <a href="{login_link}">Iniciar sesión</a>
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

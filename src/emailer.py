import smtplib
from email.mime.text import MIMEText
from src.config import Config


def send_email(subject, body, config: Config):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = config.EMAIL_FROM
        msg["To"] = config.EMAIL_TO

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        server.login(config.EMAIL_FROM, config.EMAIL_PASS)

        server.send_message(msg)
        server.quit()

        print("Email enviado correctamente")

    except smtplib.SMTPAuthenticationError:
        print("Error SMTP: credenciales inválidas o App Password incorrecta")

    except Exception as e:
        print(f"Error enviando email: {e}")

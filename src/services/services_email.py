import aiosmtplib
from email.message import EmailMessage
from src.conf.config import config

async def send_email(to_email: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = config.SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=config.SMTP_HOST,
        port=config.SMTP_PORT,
        username=config.SMTP_USER,
        password=config.SMTP_PASSWORD,
        use_tls=True,
    )
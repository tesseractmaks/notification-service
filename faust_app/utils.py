import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import dirname, join
from types import TracebackType
from typing import Any, Optional, Type

import aiosmtplib
from dotenv import load_dotenv
from loguru import logger

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

logger.add(
    sys.stdout,
    format="{time} {level} {message}",
    level="ERROR",
    serialize=True,
    backtrace=True,
    diagnose=True,
)


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

MAIL_PARAMS = {
    "TLS": True,
    "host": SMTP_HOST,
    "port": SMTP_PORT,
    "user": SMTP_USER,
    "password": SMTP_PASSWORD,
}


class SessionSmtp:
    def __init__(self, mail_params: dict):
        self.mail_params = mail_params
        self.isSSL = mail_params.get("SSL", False)
        self.host = mail_params.get("host", "localhost")
        self.port = mail_params.get("port", 465 if self.isSSL else 25)
        self.isTLS = mail_params.get("TLS", False)
        self.smtp = None

    async def __aenter__(self):
        self.smtp = aiosmtplib.SMTP(
            hostname=self.host, port=self.port, use_tls=self.isTLS, validate_certs=False
        )
        await self.smtp.connect()
        if "user" in self.mail_params:
            await self.smtp.login(
                self.mail_params["user"], self.mail_params["password"]
            )
            return self.smtp

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.smtp.close()


async def send_email(
    smtp: Any = None,
    sender: str = SMTP_USER,
    to: list = None,
    subject: str = "test",
    message: str = "123",
    textType: str = "plain",
):
    cc = []
    bcc = []
    msg = MIMEMultipart()
    msg.preamble = subject
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(to)
    if len(cc):
        msg["Cc"] = ", ".join(cc)
    if len(bcc):
        msg["Bcc"] = ", ".join(bcc)
    msg.attach(MIMEText(message, textType, "utf-8"))

    await smtp.send_message(msg)


async def create_tasks(message: str, mail: str):
    async with SessionSmtp(mail_params=MAIL_PARAMS) as smtp:
        try:
            await send_email(
                smtp=smtp,
                sender=SMTP_USER,
                to=[mail],
                subject="notification",
                message=message,
                textType="plain",
            )
        except aiosmtplib.errors.SMTPServerDisconnected as exc:
            print(exc)
        except Exception as exc:
            print(exc)

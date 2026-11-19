"""SMTP mail delivery using standard-library TLS and environment-sourced credentials."""
from __future__ import annotations
import os
import smtplib
import ssl
from email.message import EmailMessage
from collections.abc import Sequence
from .config import required_env


def send_email(recipients: Sequence[str], subject: str, body: str, *, html: bool = False) -> None:
    """Send via TLS using SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD and SMTP_FROM."""
    message = EmailMessage()
    message["From"] = required_env("SMTP_FROM")
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(body, subtype="html" if html else "plain")
    host = required_env("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    if bool(user) != bool(password):
        raise RuntimeError("SMTP_USER and SMTP_PASSWORD must both be set or both be unset")
    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.starttls(context=ssl.create_default_context())
        if user:
            smtp.login(user, password)
        smtp.send_message(message)

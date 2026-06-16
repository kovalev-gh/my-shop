# app/domains/mailing/email.py

from email.message import EmailMessage
import aiosmtplib
import logging

from core.config import settings

logger = logging.getLogger(__name__)


async def send_email(
    recipient: str,
    subject: str,
    body: str,
) -> None:

    message = EmailMessage()

    from_email = settings.smtp.get_from()

    message["From"] = from_email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    smtp = settings.smtp

    logger.info(
        "📨 Preparing email",
        extra={
            "to": recipient,
            "subject": subject,
            "smtp_host": smtp.host,
            "smtp_port": smtp.port,
        },
    )

    try:
        await aiosmtplib.send(
            message,
            hostname=smtp.host,
            port=smtp.port,
            start_tls=smtp.start_tls,
            use_tls=smtp.use_tls,
            username=smtp.user,
            password=smtp.password,
        )

        logger.info(
            "✅ Email sent successfully",
            extra={"to": recipient, "subject": subject},
        )

    except Exception as e:
        logger.exception(
            "❌ Failed to send email",
            extra={
                "to": recipient,
                "subject": subject,
                "error": str(e),
            },
        )
        raise
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings

log = logging.getLogger(__name__)


class EmailProvider:
    def send(self, to: str, subject: str, body_html: str) -> bool:
        if not settings.SMTP_HOST:
            log.info("[EMAIL STUB] To: %s | Subject: %s", to, subject)
            return True
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = settings.SMTP_USER
            msg["To"] = to
            msg.attach(MIMEText(body_html, "html"))
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
                server.sendmail(settings.SMTP_USER, [to], msg.as_string())
            return True
        except Exception as e:
            log.error("Email send failed: %s", e)
            return False

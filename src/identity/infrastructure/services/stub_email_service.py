import logging

logger = logging.getLogger(__name__)


class StubEmailService:
    """Logs emails to stdout — replace with SMTP/SES/etc. for production."""

    async def send_email_verification(self, to_email: str, raw_token: str) -> None:
        logger.info("[email] verification → %s  token=%s", to_email, raw_token)

    async def send_password_reset(self, to_email: str, raw_token: str) -> None:
        logger.info("[email] password-reset → %s  token=%s", to_email, raw_token)

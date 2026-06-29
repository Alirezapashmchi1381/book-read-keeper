from typing import Protocol


class EmailService(Protocol):
    async def send_password_reset(self, to_email: str, raw_token: str) -> None: ...

    async def send_email_verification(self, to_email: str, raw_token: str) -> None: ...

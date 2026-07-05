import secrets


class SecretsGenerator:
    def generate(self) -> str:
        return secrets.token_urlsafe(32)

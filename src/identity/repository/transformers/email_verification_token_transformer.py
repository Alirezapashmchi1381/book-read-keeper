from src.identity.domain.entities.email_verification_token import EmailVerificationToken
from src.identity.repository.models.email_verification_token_model import EmailVerificationTokenModel


class EmailVerificationTokenTransformer:
    @staticmethod
    def to_domain(model: EmailVerificationTokenModel) -> EmailVerificationToken:
        return EmailVerificationToken(
            id=model.id,
            user_id=model.user_id,
            token_hash=model.token_hash,
            expires_at=model.expires_at,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: EmailVerificationToken) -> EmailVerificationTokenModel:
        return EmailVerificationTokenModel(
            id=entity.id,
            user_id=entity.user_id,
            token_hash=entity.token_hash,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )

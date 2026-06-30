from src.identity.domain.entities.password_reset_token import PasswordResetToken
from identity.infrastructure.repository.models.password_reset_token_model import PasswordResetTokenModel


class PasswordResetTokenTransformer:
    @staticmethod
    def to_domain(model: PasswordResetTokenModel) -> PasswordResetToken:
        return PasswordResetToken(
            id=model.id,
            user_id=model.user_id,
            token_hash=model.token_hash,
            expires_at=model.expires_at,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: PasswordResetToken) -> PasswordResetTokenModel:
        return PasswordResetTokenModel(
            id=entity.id,
            user_id=entity.user_id,
            token_hash=entity.token_hash,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )

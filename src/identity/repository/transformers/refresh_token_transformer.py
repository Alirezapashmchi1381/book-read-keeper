from src.identity.domain.entities.refresh_token import RefreshToken
from src.identity.repository.models.refresh_token_model import RefreshTokenModel


class RefreshTokenTransformer:
    @staticmethod
    def to_domain(model: RefreshTokenModel) -> RefreshToken:
        return RefreshToken(
            id=model.id,
            user_id=model.user_id,
            token_hash=model.token_hash,
            expires_at=model.expires_at,
            revoked=model.revoked,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: RefreshToken) -> RefreshTokenModel:
        return RefreshTokenModel(
            id=entity.id,
            user_id=entity.user_id,
            token_hash=entity.token_hash,
            expires_at=entity.expires_at,
            revoked=entity.revoked,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

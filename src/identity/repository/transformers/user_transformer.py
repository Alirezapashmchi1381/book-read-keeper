from src.identity.domain.entities.user import User
from src.identity.domain.value_objects.email import Email
from src.identity.domain.value_objects.user_id import UserId
from src.identity.repository.models.user_model import UserModel


class UserTransformer:
    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=UserId(model.id),
            email=Email(model.email),
            username=model.username,
            password_hash=model.password_hash,
            is_active=model.is_active,
            is_verified=model.is_verified,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id.value,
            email=entity.email.address,
            username=entity.username,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            is_verified=entity.is_verified,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ChangePasswordInputDto:
    user_id: UUID
    current_password: str
    new_password: str

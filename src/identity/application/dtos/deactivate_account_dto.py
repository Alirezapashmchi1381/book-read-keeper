from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DeactivateAccountInputDto:
    user_id: UUID

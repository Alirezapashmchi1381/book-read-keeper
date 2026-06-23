# user_id.py
from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class UserId:
    value: UUID
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f"UserId(value={self.value!r})"
    
    def __eq__(self, other):
        if isinstance(other, UserId):
            return self.value == other.value
        return False
    
    def __hash__(self):
        return hash(self.value)
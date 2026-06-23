import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Email:
    address: str
    
    def __post_init__(self):
        if not self._is_valid_email(self.address):
            raise ValueError(f"Invalid email address: {self.address}")
    
    @staticmethod
    def _is_valid_email(address: str) -> bool:
        """Validate email format using regex."""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, address) is not None
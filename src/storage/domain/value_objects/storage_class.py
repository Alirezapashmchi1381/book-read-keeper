from dataclasses import dataclass


@dataclass(frozen=True)
class StorageClass:
    STANDARD = "STANDARD"
    STANDARD_IA = "STANDARD_IA"
    GLACIER = "GLACIER"

    def __init__(self, name: str):
        if name not in [self.STANDARD, self.STANDARD_IA, self.GLACIER]:
            raise ValueError("Invalid storage class")
        object.__setattr__(self, "_name", name)

    @property
    def name(self) -> str:
        return self._name
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateShelfInputDto:
    name: str
    color: str
from dataclasses import dataclass

@dataclass(frozen=True)
class Etag:
    _name : str
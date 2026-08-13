from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("Device ID cannot be empty")
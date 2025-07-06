from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int | None
    social_id: int
    username: str | None
    registration_date: datetime
    taps: int
    name: str | None
    info: str | None
    photo: str | None

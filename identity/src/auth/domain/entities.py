from dataclasses import dataclass, field

@dataclass(frozen=True)
class AccessToken:
    user_id: int
    user_name: str
    role: str
    expires: float
    token: str = field(repr=False)

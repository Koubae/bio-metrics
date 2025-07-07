from dataclasses import dataclass, field

@dataclass(frozen=True)
class AccessToken:
    access_token: str = field(repr=False)
    user_id: int
    username: str
    role: str
    expires: float

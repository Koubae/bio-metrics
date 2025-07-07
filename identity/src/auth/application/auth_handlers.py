from pydantic import BaseModel, Field


class SignUpRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1, repr=False)


class SignUpResponse(BaseModel):
    user_id: int
    role: str


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1, repr=False)


class LoginResponse(BaseModel):
    access_token: str
    expires: float

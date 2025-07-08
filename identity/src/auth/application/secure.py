from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.auth.domain.entities import Role, AccessToken
from src.auth.domain.exceptions import AuthAccessTokenInvalid, AuthAccessTokenExpired
from src.auth.infrastructure.access_token import JWTAccessTokenAuth

from dependencies.providers import provide_access_token_generator

security = HTTPBearer()


def restrict(allowed_roles: tuple[str, ...] | tuple[Role, ...]):
    """
    Create a FastAPI dependency for JWT authentication with role checking.

     Raises:
        - AuthAccessTokenInvalid: if the access token is invalid
        - AuthAccessTokenInvalid: if the access token is expired
        - HTTPException: if the user role is not allowed to access the endpoint
    """

    async def _(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        jwt_auth: JWTAccessTokenAuth = Depends(provide_access_token_generator),
    ) -> AccessToken:

        try:
            access_token = jwt_auth.parse_access_token(credentials.credentials)
        except AuthAccessTokenExpired:
            raise HTTPException(status_code=401, detail="Token has expired")
        except AuthAccessTokenInvalid:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_role = str(access_token.role)
        allowed_role_strings = [str(role) for role in allowed_roles]

        if user_role not in allowed_role_strings:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required roles: {allowed_role_strings}",
            )

        return access_token

    return _

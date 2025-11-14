from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
from .utils import decode_access_token

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        token = credentials.credentials

        token_data = decode_access_token(token)

        if not self.token_validator(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication token",
            )

        self.verify_token_data(token_data)
        return token_data

    def token_validator(self, token: str):
        return decode_access_token(token) is not None

    def verify_token_data(self, token_data: dict):
        raise NotImplementedError("Please override this method in subclasses")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if token_data.get("refresh") is True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token not allowed for this endpoint",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if not token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid refresh token",
            )


        
            
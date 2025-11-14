from passlib.context import CryptContext
import jwt
from fastapi import HTTPException, status
from src.config import Config
import uuid
from datetime import datetime, timedelta

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    return password_context.hash(password)  


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def create_access_token(
    user_data: dict,
    expiry: timedelta | None = None,
    refresh: bool = False,
) -> str:

    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.utcnow() +  (expiry if expiry else timedelta(minutes=15) )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        payload = payload,
        key = Config.JWT_SECRET_KEY,
        algorithm=Config.ALGORITHM
    )
    return token
def decode_access_token(token:str) -> dict:
    try:
        payload = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

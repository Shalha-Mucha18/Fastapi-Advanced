from fastapi import APIRouter, Depends, HTTPException, status
from  .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token, decode_access_token
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer, AccessTokenBearer


auth_router = APIRouter()
user_service = UserService()
access_token_bearer = AccessTokenBearer()


@auth_router.post("/signup",response_model=UserModel,status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    session : AsyncSession = Depends(get_session)):

    email = user_data.email

    user_exists = await user_service.user_exists(email,session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )
    new_user = await user_service.create_user(user_data,session)
    return new_user   



@auth_router.post("/login")
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):

    email = login_data.email
    password = login_data.password
    
    return await user_service.login_user(email, password, session)

@auth_router.get("/refresh-token")
async def get_new_access_token(
    token_details: dict = Depends(RefreshTokenBearer()),
) -> JSONResponse:

    expiry_duration = token_details.get("exp")

    if datetime.fromtimestamp(expiry_duration) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details["user"]
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"access_token": new_access_token}
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Refresh token has expired, please login again."
    )
    
        





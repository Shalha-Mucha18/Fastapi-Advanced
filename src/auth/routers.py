from fastapi import APIRouter, Depends, HTTPException, status
from  .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_acess_token, decode_access_token
from datetime import timedelta
from fastapi.responses import JSONResponse


auth_router = APIRouter()
user_service = UserService()


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


    





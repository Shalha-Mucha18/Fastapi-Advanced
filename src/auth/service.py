from .models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from .schemas import UserCreateModel
from .utils import generate_password_hash as hash_password, verify_password, create_acess_token
from src.config import Config
from fastapi import HTTPException, status
from datetime import timedelta
from fastapi.responses import JSONResponse


class UserService:
    async def get_user_by_email(self,email:str,session:AsyncSession) -> User | None:
      statement = select(User).where(User.email == email)
      result = await session.execute(statement)
      user = result.scalar_one_or_none()
      return user


    async def user_exists(self,email:str,session:AsyncSession) -> bool:
      user = await self.get_user_by_email(email,session)
      return True if user  is not None else False

    async def create_user(self,user_data:UserCreateModel,session:AsyncSession) -> User:
        user_data_dict = user_data.model_dump()
        user_data_dict["first_name"] = user_data_dict.get("first_name") or ""
        user_data_dict["last_name"] = user_data_dict.get("last_name") or ""

        new_user = User(
           **user_data_dict,
        )  
        new_user.password_hash = hash_password(user_data_dict["password"])
        session.add(new_user)
        await session.commit()  

        return new_user  
    async def login_user(self, email:str,password:str,session:AsyncSession):
        user = await self.get_user_by_email(email,session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        password_valid = verify_password(password,user.password_hash)
        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        access_token = create_acess_token(
            user_data = {
                'email': user.email,
                'user_uid': str(user.id),
                'username': user.username
            }
        )
        refresh_token = create_acess_token(
            user_data = {
                'email': user.email,
                'user_uid': str(user.id)
                },
            refresh=True,
            expiry = timedelta(days=Config.REFRESH_TOKRN_EXPIRE_DAYS)
        )

        return  JSONResponse(
            content={
                'message': 'Login successful',
                'access_token': access_token,
                'refresh_token': refresh_token,
                "user": {
                    "email": user.email,
                    "uid": str(user.id),
                    "username": user.username
                }
            }
        )






    

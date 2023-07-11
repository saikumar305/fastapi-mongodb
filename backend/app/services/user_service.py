from typing import Optional , List
from uuid import UUID
from app.schemas.user_schema import UserAuth
from app.models.user_model import User

from app.core.security import get_password , verify_password


class UserService:
    @staticmethod
    async def create_user(user:UserAuth):
        user_in = User(
            username= user.username,
            email=user.email,
            hashed_password=get_password(user.password)
        )
        await user_in.save()
        return user_in
    
    @staticmethod
    async def list_users() -> Optional[User]:
        print(User.all())
        return await User.all()
    
    @staticmethod
    async def authenticate(email:str , password:str) -> Optional[User]:
        user = await UserService.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    async def get_user_by_email(email:str) -> Optional[User]:
        return await User.find_one(User.email == email)
    
    @staticmethod
    async def get_user_by_id(id:UUID) -> Optional[User]:
        return await User.find_one(User.user_id == id)
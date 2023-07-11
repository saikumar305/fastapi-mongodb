from pymongo.errors import DuplicateKeyError
from fastapi import APIRouter , HTTPException, status
from typing import List
from app.schemas.user_schema import UserAuth , UserOut
from app.services.user_service import UserService
user_router = APIRouter()


@user_router.get('/', summary="List out users" , response_model=List[UserOut])
async def list_users():
    return UserService.list_users()

@user_router.post('/create' ,
                  response_model=UserOut,
                   summary="create new user")
async def create_user(data:UserAuth):
    try:
        return await UserService.create_user(data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "User with this email already exists"
        )
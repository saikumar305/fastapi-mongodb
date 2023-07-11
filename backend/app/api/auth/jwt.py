from fastapi import APIRouter, Body , Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from typing import Any
from jose import jwt
from app.services.user_service import UserService
from app.core.security import create_access_token , create_refresh_token
from app.core.config import settings
from app.schemas.user_schema import UserOut
from app.schemas.auth_schema import TokenSchema, TokenPayload
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
from app.services.user_service import UserService

auth_router = APIRouter()

@auth_router.post('/login')
async def login(form_data : OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email= form_data.username,password = form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id)
        }

@auth_router.post('/me' , summary="Current User" , response_model=UserOut)
async def test_user_token(user: User = Depends(get_current_user)):
    return user


@auth_router.post('/refresh_token' , summary="Get refresh token" , response_model=TokenSchema)
async def refresh_token(refresh_token:str = Body(...)):
    try:
        payload = jwt.decode(refresh_token, settings.JWT_REFRESH_SECRET_KEY , algorithms=[settings.ALGORITHM])

        token_data = TokenPayload(**payload)

    except (jwt.JWTError , ValidationError):
        raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid refresh token",
                    headers={"WWW-Authenticate": "Bearer"}
                )
    
    user = await UserService.get_user_by_id(token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id)
        }
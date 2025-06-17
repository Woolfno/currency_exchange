from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.models.user import User
from app.api.schemas.token import Token
from app.api.schemas.user import UserIn
from app.api.services.user import UserService, get_user_service
from app.core.config import Settings, get_settings
from app.core.security import (authenticate, create_access_token,
                               get_password_hash)

router = APIRouter(prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user:UserIn, service:UserService=Depends(get_user_service)):
    user_obj = User(**user.model_dump())
    u = await service.get_by_username(user.username)
    if u is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username is exist")
    user_obj.password = get_password_hash(user.password)
    u = await service.create(user_obj)

@router.post("/login")
async def login(user:UserIn, 
                service:Annotated[UserService, Depends(get_user_service)],
                settings:Annotated[Settings, Depends(get_settings)])->Token:
    u = await authenticate(user.username, user.password, service)
    if u is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate":"Bearer"},
                            )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    access_token = create_access_token(data={"sub":u.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token)    

@router.post('/token')
async def token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], 
                service:Annotated[UserService, Depends(get_user_service)],
                settings:Annotated[Settings, Depends(get_settings)])->Token:
    return await login(UserIn(username=form_data.username, password=form_data.password), service, settings)
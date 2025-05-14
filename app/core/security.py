from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext

from app.api.models.user import User
from app.api.services.user import UserService, get_user_service
from app.core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(password, hash)->bool:
    return pwd_context.verify(password, hash)

def get_password_hash(password)->str:
    return pwd_context.hash(password)

async def authenticate(username:str, password:str, service:UserService)->User:
    u = await service.get_by_username(username)
    if u is None:
        return None
    if verify_password(password, u.password):
        return u
    return None

def create_access_token(data:dict, expires_delta:timedelta|None=None)->str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token:Annotated[str, Depends(oauth2_schema)], 
                           service:Annotated[UserService, Depends(get_user_service)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")
    except InvalidTokenError:
        raise credentials_exception
    user = await service.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user
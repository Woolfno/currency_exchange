from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models.user import User
from app.database.db import get_async_session


class UserService:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def create(self, user:User)->User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_by_id(self, id:UUID)->User:
        query = select(User).where(User.id==id)
        result = await self.session.execute(query)
        user = result.first()
        return user
    
    async def get_by_username(self, username:str)->User:
        query = select(User).where(User.username==username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
async def get_user_service(session:AsyncSession=Depends(get_async_session)):
    return UserService(session)
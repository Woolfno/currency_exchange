from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

class Base(AsyncAttrs, DeclarativeBase):
    pass

engine = create_async_engine(settings.ASYNC_DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session():
    async with async_session() as session:
        yield session
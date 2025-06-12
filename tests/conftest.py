import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.pool import NullPool

from app.api.models.user import User
from app.api.schemas.user import UserIn
from app.core.security import create_access_token, get_password_hash
from app.database.db import Base, get_async_session
from main import app

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@vm:5432/test_db"

async_engine = create_async_engine(
    TEST_DATABASE_URL, echo=True, poolclass=NullPool)


@pytest_asyncio.fixture(scope="session")
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_session(async_db_engine):
    session_factory = async_sessionmaker(expire_on_commit=False,
                                         autocommit=False,
                                         autoflush=False,
                                         bind=async_db_engine,
                                         class_=AsyncSession,
                                         )

    async with session_factory() as session:
        await session.begin()
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def client(async_session):
    def override_get_session():
        yield async_session

    app.dependency_overrides[get_async_session] = override_get_session
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest_asyncio.fixture(scope="function")
async def user(async_session: AsyncSession):
    u = UserIn(username="user", password="12345")
    user_db = User(username=u.username, password=get_password_hash(u.password))
    async_session.add(user_db)
    await async_session.commit()
    await async_session.refresh(user_db)
    yield u
    await async_session.delete(user_db)
    await async_session.commit()


@pytest.fixture(scope="function")
def access_token() -> str:
    return create_access_token({"sub": "user"})

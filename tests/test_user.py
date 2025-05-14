import pytest
from httpx import AsyncClient
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models.user import User
from app.core.security import get_password_hash


@pytest.mark.asyncio
async def test_register(client: AsyncClient, async_session: AsyncSession):
    username = "user1"
    response = await client.post("/auth/register", json={"username": username, "password": "123"})
    assert response.status_code == 201

    stmt = select(User).where(User.username == username)
    result = await async_session.execute(stmt)
    user = result.scalar_one_or_none()

    assert user is not None
    assert user.id is not None

    await async_session.execute(delete(User).where(User.username == username))


@pytest.mark.asyncio
async def test_login(client: AsyncClient, async_session: AsyncSession):
    username = "user"
    password = "1234"
    user = User(username=username, password=get_password_hash(password))
    async_session.add(user)
    await async_session.commit()

    response = await client.post("/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    assert response.json().get("access_token") is not None

    await async_session.execute(delete(User).where(User.username == username))
    await async_session.commit()

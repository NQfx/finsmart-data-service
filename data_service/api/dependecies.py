from typing import AsyncIterator
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import async_session
from repositories.user_data import UserRepository

async def get_session():
    async with async_session() as session:
        yield session

async def get_user_id(
    user_uuid: UUID,
    session: AsyncSession = Depends(get_session),
) -> int:
    repo = UserRepository(session)

    user_id = await repo.get_id_by_uuid(user_uuid)

    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user_id
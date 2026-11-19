from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import URL
from .config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=8,
    max_overflow=16
)

async_session = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from models.product import Base, Product, Sale
from models.user_interaction import UserInteraction, GlobalUserPreference
from models.chat import ChatHistory
from config import settings
from typing import AsyncGenerator

engine = create_async_engine(
    settings.database_url,
    echo=True,
)

async_session_maker = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session 
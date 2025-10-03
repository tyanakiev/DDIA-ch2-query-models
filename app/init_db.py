import asyncio
from models.orm import Base
from sqlalchemy.ext.asyncio import create_async_engine
from config import settings

async def init():
    engine = create_async_engine(settings.POSTGRES_DSN, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())
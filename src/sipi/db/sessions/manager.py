from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool

class AsyncDatabaseManager:
    def __init__(self, database_url: str, echo: bool = False, **pool_kwargs):
        self.engine = create_async_engine(
            database_url,
            poolclass=AsyncAdaptedQueuePool,
            echo=echo,
            **pool_kwargs
        )
        self.session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def close(self):
        await self.engine.dispose()

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """FastAPI dependency style generator"""
        async with self.session_maker() as session:
            try:
                yield session
            finally:
                await session.close()

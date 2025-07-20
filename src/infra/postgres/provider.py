from collections.abc import AsyncIterator
from dishka import Provider, Scope, provide, provide_all
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import DatabaseConfig
from loguru import logger

class PostgresProvider(Provider):
    scope = Scope.REQUEST
    
    @provide(scope=Scope.APP)
    async def _get_engine(self, config: DatabaseConfig) -> AsyncIterator[AsyncEngine]:
        engine: AsyncEngine | None = None
        try:
            if engine is None:
                engine = create_async_engine(config.dsn)
            yield engine
        except ConnectionRefusedError as e:
            logger.error('Error connecting to database', e)
        finally:
            if engine is not None:
                await engine.dispose() 


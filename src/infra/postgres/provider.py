from collections.abc import AsyncIterator
from dishka import Provider, Scope, provide, provide_all
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import DatabaseConfig
from loguru import logger
from src.infra.postgres.gateways.base import GetAllGate
from src.infra.postgres.gateways.base import CreateGate

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

    @provide
    async def _get_session_maker(
        self, engine: AsyncEngine
    ) -> AsyncIterator[AsyncSession]:
        async with AsyncSession(bind=engine) as session:
            yield session
    

    @provide
    async def _get_all_gate[
        TTable,
        TEntity,
    ](
        self,
        table: type[TTable],
        schema_type: type[TEntity],
        session: AsyncSession,
    ) -> GetAllGate[TTable, TEntity]:
        return GetAllGate(
            session=session,
            table=table,
            schema_type=schema_type,
        )
    
    @provide
    async def _crate_gate[
        TTable,
        TCreate,
    ](
        self,
        table: type[TTable],
        create_schema_type: type[TCreate],
        session: AsyncSession,
    ) -> CreateGate[TTable, TCreate]:
        return CreateGate(
            session=session,
            table=table,
            create_schema_type=create_schema_type,
        )

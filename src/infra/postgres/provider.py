from collections.abc import AsyncIterator
from typing import TypeVar, Type
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from src.config import DatabaseConfig
from loguru import logger
from src.infra.postgres.gateways.base import GetAllGate, CreateGate

TTable = TypeVar("TTable")
TEntity = TypeVar("TEntity")
TCreate = TypeVar("TCreate")


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
            logger.error("Error connecting to database", e)
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
    async def _get_all_gate(
        self,
        table: Type[TTable],
        schema_type: Type[TEntity],
        session: AsyncSession,
    ) -> GetAllGate[TTable, TEntity]:
        return GetAllGate(
            session=session,
            table=table,
            schema_type=schema_type,
        )

    @provide
    async def _create_gate(
        self,
        table: Type[TTable],
        create_schema_type: Type[TCreate],
        session: AsyncSession,
    ) -> CreateGate[TTable, TCreate]:
        return CreateGate(
            session=session,
            table=table,
            create_schema_type=create_schema_type,
        )

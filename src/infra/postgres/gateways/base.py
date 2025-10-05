from dataclasses import dataclass
from sqlalchemy import select, insert
from loguru import logger

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.postgres.tables import BaseDBModel
from sqlalchemy import Select
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate
from typing import TypeVar, Generic, Type

TAppliable = Select | ReturningInsert | ReturningUpdate

TTable = TypeVar('TTable', bound=BaseDBModel)
TEntity = TypeVar('TEntity', bound=BaseModel)
TCreate = TypeVar('TCreate', bound=BaseModel)

@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetAllGate(Generic[TTable, TEntity], PostgresGateway):
    table: Type[TTable]
    schema_type: Type[TEntity]

    async def __call__(self) -> list[TEntity]:
        logger.info(1)
        stmt = select(*self.table.group_by_fields())
        logger.info(stmt)
        results = (await self.session.execute(stmt)).mappings().fetchall()
        logger.info(results)
        return [self.schema_type.model_validate(result) for result in results]

@dataclass(slots=True, kw_only=True)
class CreateGate(Generic[TTable, TCreate], PostgresGateway):
    table: Type[TTable]
    create_schema_type: Type[TCreate]

    async def __call__(self, entity: TCreate) -> None:
        stmt = insert(self.table).values(**entity.model_dump())
        await self.session.execute(stmt)

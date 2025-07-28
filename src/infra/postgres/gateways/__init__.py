from dataclasses import dataclass
from uuid import UUID
from sqlalchemy import select

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.postgres.tables import BaseDBModel

@dataclass(slots=True, kw_only=True)
class PostgresGateway:
    session: AsyncSession

@dataclass(slots=True, kw_only=True)
class GetAllGate[TTable: BaseDBModel, TEntity: BaseModel](
    PostgresGateway
):
    table: type[TTable]
    schema_type: type[TEntity]

    async def __call__(self,) -> list[TEntity]:
        stmt = select(*self.table)
        result = (await self.session.execute(stmt)).fetchall()
        return self.schema_type.model_validate(result)
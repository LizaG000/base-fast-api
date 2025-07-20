from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
#from src.config import DatabaseConfig as Config
from loguru import logger
import asyncio
engine = create_async_engine(
    url = 'postgresql+psycopg_async://postgres:postgres@127.0.0.1:5433/postgres',
    #url=Config.dsn(),
    echo=True, # добавляем логи в консоль
    pool_size=5, # кол-во подключений к бд
    max_overflow=10, # максимальное кол-во подключений 
)

async def test_connection():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT version()"))
        version = result.scalar()
        logger.info(f"PostgreSQL version: {version}")

asyncio.run(test_connection())
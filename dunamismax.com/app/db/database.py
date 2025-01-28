# app/db/database.py
import asyncpg
from loguru import logger
from .queries import CREATE_CONTACT_TABLE
from app.config import DATABASE_URL  # Import from config.py


async def create_pool():
    """
    Creates an asyncpg connection pool.
    Customize min_size/max_size for performance if desired.
    """
    try:
        return await asyncpg.create_pool(
            DATABASE_URL, min_size=1, max_size=5, timeout=30
        )
    except Exception as e:
        logger.error(f"Error creating asyncpg pool: {e}")
        raise


async def close_pool(pool):
    """
    Closes the asyncpg connection pool.
    """
    await pool.close()


@logger.catch
async def execute(pool, query, *args):
    async with pool.acquire() as conn:
        async with conn.transaction():
            return await conn.execute(query, *args)


@logger.catch
async def fetch(pool, query, *args):
    async with pool.acquire() as conn:
        async with conn.transaction():
            return await conn.fetch(query, *args)


@logger.catch
async def fetchrow(pool, query, *args):
    async with pool.acquire() as conn:
        async with conn.transaction():
            return await conn.fetchrow(query, *args)


@logger.catch
async def fetchval(pool, query, *args):
    async with pool.acquire() as conn:
        async with conn.transaction():
            return await conn.fetchval(query, *args)

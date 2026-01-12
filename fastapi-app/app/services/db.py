from collections.abc import AsyncGenerator

import psycopg

from app.core.config import settings


async def get_connection() -> AsyncGenerator[psycopg.AsyncConnection, None]:
    async with await psycopg.AsyncConnection.connect(settings.database_url) as conn:
        yield conn

from __future__ import annotations

import functools

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings

DNS = "postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
pg_url = DNS.format(
    pg_user=settings.POSTGRES_USER,
    pg_password=settings.POSTGRES_PASSWORD,
    pg_host=settings.POSTGRES_HOST,
    pg_port=settings.POSTGRES_PORT,
    pg_database=settings.POSTGRES_DB,
)

engine = create_async_engine(pg_url, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


# async def pg_context(app):
#     app['db'] = engine
#
#     yield
#
#     app['db'].close()
#     await app['db'].wait_closed()


def provide_session(*args, commit_after: bool = False):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if 'async_session' in kwargs:
                result = await func(*args, **kwargs)
            else:
                kwargs['async_session'] = async_session
                result = await func(*args, **kwargs)
            if commit_after:
                kwargs['async_session'].commit()
            return result

        return wrapper

    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    else:
        return decorator

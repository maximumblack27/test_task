import os
from typing import AsyncGenerator

from aiohttp import web
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from apps.books.managers import BookManager
from apps.books.models import BookModel, BookFileModel
from apps.books.schemas import BookSchema, BookQuerySchema, PageParamsSchema, CreateBookSchema
from apps.books.utils import extract_query_param, get_book_id
from apps.core.app import create_app
from apps.core.extensions import engine, async_session
from apps.core.database import Base
from config import settings
import pytest

from tests.fixtures import books, book_files


# @pytest.fixture
# async def session():
#     async with async_session() as session:
#         yield session


# @pytest.fixture(autouse=True)
# async def app():
#     async with engine.begin() as conn:
#         app = create_app()
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#         await add_books(conn)
#         yield app
#         await conn.run_sync(Base.metadata.drop_all)
#         await engine.dispose()


@pytest.fixture
async def test_client(loop, aiohttp_client):
    app = await create_app()
    return loop.run_until_complete(aiohttp_client(app))


async def add_books(conn):
    await conn.execute(BookModel.insert(), books)
    await conn.execute(BookFileModel.insert(), book_files)
    await conn.commit()

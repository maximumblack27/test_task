import asyncio
import os
from asyncio import AbstractEventLoop
from typing import Generator

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy import delete, insert

from apps.books.models import BookFileModel, BookModel
from apps.core.app import create_app
from apps.core.extensions import async_session
from config.settings import POSTGRES_HOST, UPLOAD_FILE_DIRECTORY
from tests.fixtures import book_files, books


@pytest.fixture
async def session():
    async with async_session() as session:
        yield session


@pytest.fixture(autouse=True, scope='session')
def clear_folder():
    yield
    for filename in os.listdir(UPLOAD_FILE_DIRECTORY):
        file_path = os.path.join(UPLOAD_FILE_DIRECTORY, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Ошибка при удалении файла {file_path}. {e}')


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
def migrate_db() -> Generator[None, None, None]:
    if POSTGRES_HOST not in ("postgres", "localhost"):
        raise RuntimeError("Migration for tests should be applied only on test DB")

    config = AlembicConfig("alembic.ini")

    upgrade(config, "head")
    yield
    downgrade(config, "base")


@pytest.fixture
async def test_client(aiohttp_client):
    app = await create_app()
    return await aiohttp_client(app)


@pytest.fixture
async def add_books(session):
    await session.execute(insert(BookModel).values(books))
    await session.execute(insert(BookFileModel).values(book_files))
    await session.commit()
    yield
    await session.execute(delete(BookFileModel))
    await session.execute(delete(BookModel))
    await session.commit()

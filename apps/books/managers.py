from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from apps.books.models import BookModel
from apps.core.extensions import provide_session


class BookManager:

    def __init__(self, instance: BookModel = None):
        self.instance = instance

    @classmethod
    @provide_session
    async def get_book_list(cls, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(BookModel)

            result = await session.execute(query)
            books = result.scalars().all()

            return books

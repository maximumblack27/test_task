from datetime import date
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from apps.books.models import BookModel
from apps.core.extensions import provide_session


class BookManager:

    def __init__(self, instance: BookModel = None):
        self.instance = instance

    @classmethod
    @provide_session
    async def get_book_list(cls,
                            filter_name: Optional[list[str]] = None,
                            filter_author: Optional[list[str]] = None,
                            date_start: Optional[date] = None,
                            date_end: Optional[date] = None,
                            filter_genre: Optional[list[str]] = None,
                            page_size: Optional[int] = None,
                            page_number: Optional[int] = None,
                            async_session: async_sessionmaker[AsyncSession] = None):
        async with async_session() as session:
            query = select(BookModel)

            if filter_name:
                query = query.where(BookModel.name.in_(filter_name))

            if filter_author:
                query = query.where(BookModel.author.in_(filter_author))

            if filter_genre:
                query = query.where(BookModel.genre.in_(filter_genre))

            if date_start:
                query = query.where(BookModel.date_published > date_start)

            if date_end:
                query = query.where(BookModel.date_published <= date_end)

            query = query.order_by(BookModel.id).offset(page_number*page_size).limit(page_size)

            result = await session.execute(query)
            books_list = result.scalars()

            return books_list

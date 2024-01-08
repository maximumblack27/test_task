from datetime import date
from typing import Optional

from sqlalchemy import select, desc, asc, or_
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from apps.books.models import BookModel, BookFileModel
from apps.books.utils import get_column_orm
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
                            query_string: Optional[str] = None,
                            sort: Optional[str] = None,
                            sort_order: Optional[str] = None,
                            page_number: Optional[int] = None,
                            async_session: async_sessionmaker[AsyncSession] = None):
        async with async_session() as session:
            query = select(BookModel)

            if query_string:
                query_string = query_string.replace('\\', '\\\\').replace('_', '\\_').replace('%', '\\%')
                query = query.filter(or_(BookModel.name.ilike(f'%{query_string}%'),
                                         BookModel.author.ilike(f'%{query_string}%')))

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

            if sort:
                order = asc if sort_order == 'asc' else desc
                column = get_column_orm(BookModel, sort)

                query = query.order_by(order(column))
            else:
                query = query.order_by(BookModel.id)

            # query = query.offset(page_number*page_size).limit(page_size)

            result = await session.execute(query)
            books_list = result.scalars()

            return books_list

    @classmethod
    @provide_session
    async def get_book(cls,
                       book_id: int,
                       async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            query = select(BookModel).where(BookModel.id == book_id)

            result = await session.execute(query)
            book = result.scalar()

            return book

    @provide_session
    async def add_book(self,
                       name: str,
                       author: str,
                       date_published: date,
                       genre: Optional[str] = None,
                       async_session: async_sessionmaker[AsyncSession] = None):
        async with async_session() as session:
            async with session.begin():
                self.instance = BookModel(
                    name=name, author=author,
                    date_published=date_published, genre=genre
                )
                session.add(self.instance)


class BookFileManager:

    def __init__(self, instance: BookFileModel = None):
        self.instance = instance

    @provide_session
    async def add_book_file(self,
                            book_id: int,
                            file_name: str,
                            origin_file_name: str,
                            text: Optional[str] = None,
                            async_session: async_sessionmaker[AsyncSession] = None):
        async with async_session() as session:
            async with session.begin():
                self.instance = BookFileModel(
                    book_id=book_id, file_name=file_name,
                    origin_file_name=origin_file_name, text=text
                )
                session.add(self.instance)

    @classmethod
    @provide_session
    async def get_file_name(cls,
                            book_id: str,
                            async_session: async_sessionmaker[AsyncSession] = None):
        async with async_session() as session:
            query = select(BookModel.name.label('name'), BookFileModel.file_name.label('file_name')) \
                .join(BookModel, BookModel.id == BookFileModel.book_id) \
                .where(BookModel.id == book_id)

            result = await session.execute(query)
            book = result.fetchone()

            return book._mapping

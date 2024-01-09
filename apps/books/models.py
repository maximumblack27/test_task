from __future__ import annotations

import datetime

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from apps.core.database import BaseDBModel
from config.settings import POSTGRES_SCHEMA


class BookModel(BaseDBModel):
    __tablename__ = "book"
    __table_args__ = {'schema': POSTGRES_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    author: Mapped[str] = mapped_column(index=True)
    date_published: Mapped[datetime.date] = mapped_column(index=True, server_default=func.now())
    genre: Mapped[str] = mapped_column(index=True, nullable=True)


class BookFileModel(BaseDBModel):
    __tablename__ = "book_file"
    __table_args__ = {'schema': POSTGRES_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey(BookModel.id))
    file_name: Mapped[str]
    origin_file_name: Mapped[str]
    text: Mapped[str] = mapped_column(type_=Text, nullable=True)

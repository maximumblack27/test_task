from __future__ import annotations

import datetime

from sqlalchemy import func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from apps.core.database import BaseModel
from config.settings import POSTGRES_SCHEMA


class BookModel(BaseModel):
    __tablename__ = "book"
    __table_args__ = {'schema': POSTGRES_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    author: Mapped[str]
    date_published: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    genre: Mapped[str] = mapped_column(nullable=True)


class BookFileModel(BaseModel):
    __tablename__ = "book_file"
    __table_args__ = {'schema': POSTGRES_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey(BookModel.id))
    file_name: Mapped[str]
    origin_file_name: Mapped[str]
    text: Mapped[str] = mapped_column(type_=Text, nullable=True)

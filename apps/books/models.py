from __future__ import annotations

import datetime

from sqlalchemy import func
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
    genre: Mapped[str]

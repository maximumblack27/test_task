from __future__ import annotations

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class BaseModel(AsyncAttrs, Base):
    __abstract__ = True

    def __repr__(self):
        if hasattr(self, 'title'):
            return f'<{self.__class__.__name__}: {self.title}>'
        if hasattr(self, 'name'):
            return f'<{self.__class__.__name__}: {self.name}>'
        return self.repr()

    def repr(self):
        return f'<{self.__class__.__name__}>'


import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Any, Optional, Type

from aiofile import async_open
from marshmallow import ValidationError
from sqlalchemy.orm import DeclarativeMeta

from apps.core.exceptions import OrmValidationError
from config import settings


def extract_query_param(request, param: str, type_to_cast: Optional[Type] = None, default_value: Any = None):
    value = request.query.get(param, default_value)
    if not type_to_cast:
        return value
    try:
        return type_to_cast(value)
    except (TypeError, ValueError):
        return default_value


def get_column_orm(model_object: Type[DeclarativeMeta], column: str):
    if not isinstance(model_object, DeclarativeMeta):
        raise OrmValidationError(f'{model_object} is not sqlalchemy model')
    column_orm = getattr(model_object, column)
    if not column:
        raise OrmValidationError(f'{column} not exists')
    return column_orm


def get_book_id(request):
    book_id = request.match_info.get('book_id', None)
    if book_id and book_id.isdigit() and int(book_id) > 0:
        return int(book_id)
    else:
        raise ValidationError(message='book_id must be a positive integer', field_name='book_id')


def get_end_date(date: datetime.date):
    return date + timedelta(days=1)


async def download_file(response, file):
    try:
        file_path = f'{settings.UPLOAD_FILE_DIRECTORY}{file.get("file_name")}'
        async with async_open(file_path, 'rb') as f:
            chunk = await f.read(settings.CHUNK_SIZE)

            while chunk:
                await response.write(chunk)
                chunk = await f.read(settings.CHUNK_SIZE)

    except asyncio.CancelledError:
        raise

    return response


async def save_file(field):
    file_name = f'{uuid.uuid4()}.pdf'
    file_path = f'{settings.UPLOAD_FILE_DIRECTORY}{file_name}'
    with open(file_path, 'wb') as f:
        while True:
            chunk = await field.read_chunk(settings.CHUNK_SIZE)
            if not chunk:
                break
            f.write(chunk)

    return file_name

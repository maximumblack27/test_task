import asyncio
import uuid
from datetime import datetime, timedelta
from io import BytesIO
from typing import Any, Optional, Type

from aiofile import async_open
from aiohttp import web, BodyPartReader
from marshmallow import ValidationError
from pdf2image import convert_from_path
from sqlalchemy.orm import DeclarativeMeta

from apps.core.exceptions import OrmValidationError
from config import settings


def extract_query_param(request: web.Request, param: str,
                        type_to_cast: Optional[Type] = None, default_value: Any = None) -> Optional[Type]:
    value = request.query.get(param, default_value)
    if not type_to_cast:
        return value
    try:
        return type_to_cast(value)
    except (TypeError, ValueError):
        return default_value


def get_column_orm(model_object: Type[DeclarativeMeta], column: str) -> Any:
    if not isinstance(model_object, DeclarativeMeta):
        raise OrmValidationError(f'{model_object} is not sqlalchemy model')
    column_orm = getattr(model_object, column)
    if not column:
        raise OrmValidationError(f'{column} not exists')
    return column_orm


def get_value_from_request(request: web.Request, value: str) -> int:
    val = request.match_info.get(value, None)
    if val and val.isdigit() and int(val) > 0:
        return int(val)
    else:
        raise ValidationError(message=f'{value} must be a positive integer', field_name=value)


def get_end_date(date: datetime.date) -> datetime.date:
    return date + timedelta(days=1)


async def download_file(response: web.StreamResponse, file: dict) -> web.StreamResponse:
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


async def save_file(field: BodyPartReader) -> str:
    file_name = f'{uuid.uuid4()}.pdf'
    file_path = f'{settings.UPLOAD_FILE_DIRECTORY}{file_name}'
    with open(file_path, 'wb') as f:
        while True:
            chunk = await field.read_chunk(settings.CHUNK_SIZE)
            if not chunk:
                break
            f.write(chunk)

    return file_name


def read_pdf_from_page(file: dict, page_number: int) -> bytes:
    file_path = f'{settings.UPLOAD_FILE_DIRECTORY}{file.get("file_name")}'
    images = convert_from_path(file_path, first_page=page_number, last_page=page_number)

    if not images:
        raise ValueError("Invalid start page number")

    image_bytes_io = BytesIO()
    images[0].save(image_bytes_io, format='PNG')
    image_bytes = image_bytes_io.getvalue()

    return image_bytes

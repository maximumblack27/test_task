import asyncio
import os
import time

from aiofile import async_open
from aiohttp import web, BodyPartReader

from apps.books.managers import BookManager, BookFileManager
from apps.books.schemas import BookSchema, BookQuerySchema, PageParamsSchema, CreateBookSchema, BookFileSchema
from apps.books.utils import extract_query_param, get_book_id
from config import settings

book_routes = web.RouteTableDef()


@book_routes.post('/books/')
async def get_book_list(request):
    request_data = await request.read()
    args = BookQuerySchema().loads(request_data) if request_data else {}
    page_params = {
        'page_number': extract_query_param(request, 'page_number', int, 1),
        'page_size': extract_query_param(request, 'page_size', int, settings.MAX_PAGE_SIZE)
    }
    args.update(PageParamsSchema().load(page_params))

    schema = BookSchema()
    books = await BookManager.get_book_list(**args)
    data = schema.dump(books, many=True)

    return web.json_response(data=data, status=200)


@book_routes.get('/book/{book_id}/')
async def get_book(request):
    book_id = get_book_id(request)

    schema = BookSchema()
    book = await BookManager.get_book(book_id=book_id)
    data = schema.dump(book)

    return web.json_response(data=data, status=200)


@book_routes.post('/book/upload/')
async def upload_book(request):
    reader = await request.multipart()
    field: BodyPartReader = await reader.next()

    file_name = f'{time.time_ns()}.pdf'
    file_path = f'{settings.UPLOAD_FILE_PATH}{file_name}'
    with open(file_path, 'wb') as f:
        while True:
            chunk = await field.read_chunk(settings.CHUNK_SIZE)
            if not chunk:
                break
            f.write(chunk)

    request_data = await request.post()

    schema = CreateBookSchema()
    args = schema.load(request_data)

    manager = BookManager()
    await manager.add_book(**args)

    file_manager = BookFileManager()
    await file_manager.add_book_file(
        book_id=manager.instance.id, file_name=file_name, origin_file_name=field.filename
    )

    return web.json_response(data={"book_id": manager.instance.id}, status=201)


@book_routes.get('/book/{book_id}/download/')
async def download_book(request):
    book_id = get_book_id(request)

    schema = BookFileSchema()
    book = await BookFileManager.get_file_name(book_id=book_id)
    file = schema.dump(book)

    response = web.StreamResponse(
        status=200,
        reason='OK',
        headers={
            'Content-Type': 'multipart/x-mixed-replace',
            'CONTENT-DISPOSITION': f'attachment;filename={file.get("name")}'
        }
    )
    await response.prepare(request)

    try:
        file_path = f'{settings.UPLOAD_FILE_PATH}{file.get("file_name")}'
        async with async_open(file_path, 'rb') as f:
            chunk = await f.read(settings.CHUNK_SIZE)

            while chunk:
                await response.write(chunk)
                chunk = await f.read(settings.CHUNK_SIZE)

    except asyncio.CancelledError:
        # отпускаем перехваченный CancelledError
        raise

    return response

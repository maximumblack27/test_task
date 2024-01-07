import os
import time

from aiohttp import web, BodyPartReader

from apps.books.managers import BookManager
from apps.books.schemas import BookSchema, BookQuerySchema, PageParamsSchema, CreateBookSchema
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
async def create_book(request):
    reader = await request.multipart()
    field: BodyPartReader = await reader.next()

    with open(f'{settings.UPLOAD_FILE_PATH}{time.time_ns()}.pdf', 'wb') as f:
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

    return web.json_response(data={"book_id": manager.instance.id}, status=201)

import json

from aiohttp import BodyPartReader, web

from apps.books.managers import BookFileManager, BookManager
from apps.books.schemas import (BookFileSchema, BookQuerySchema, BookSchema,
                                CreateBookSchema, LoadingFileSchema,
                                PageParamsSchema)
from apps.books.utils import (download_file, extract_query_param, get_book_id,
                              save_file)
from config import settings

book_routes = web.RouteTableDef()


@book_routes.post('/books/')
async def get_book_list(request):
    request_data = await request.read()

    args = BookQuerySchema().load(json.loads(request_data)) if request_data else {}
    page_params = {
        'page_number': extract_query_param(request, 'page_number', int, 1),
        'page_size': extract_query_param(request, 'page_size', int, settings.MAX_PAGE_SIZE)
    }
    args.update(PageParamsSchema().load(page_params))

    schema = BookSchema()
    books = await BookManager.get_book_list(**args)
    data = schema.dump(books, many=True)
    response_data = {
        'page': page_params['page_number'],
        'items': data
    }

    return web.json_response(data=response_data, status=200)


@book_routes.get('/books/{book_id}/')
async def get_book(request):
    book_id = get_book_id(request)

    schema = BookSchema()
    book = await BookManager.get_book(book_id=book_id)
    data = schema.dump(book)

    return web.json_response(data=data, status=200)


@book_routes.post('/books/upload/')
async def upload_book(request):
    reader = await request.multipart()
    field: BodyPartReader = await reader.next()

    file_schema = LoadingFileSchema()
    file_schema.load({'file_headers': field.headers})

    file_name = await save_file(field)

    request_data = await request.post()
    request_data = json.loads(request_data.get('data'))

    schema = CreateBookSchema()
    args = schema.load(request_data)

    manager = BookManager()
    await manager.add_book(**args)

    file_manager = BookFileManager()
    await file_manager.add_book_file(
        book_id=manager.instance.id, file_name=file_name, origin_file_name=field.filename
    )

    return web.json_response(data={"book_id": manager.instance.id}, status=201)


@book_routes.get('/books/{book_id}/download/')
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

    return await download_file(response, file)

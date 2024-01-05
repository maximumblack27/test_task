import json
from aiohttp import web

from apps.books.managers import BookManager
from apps.books.schemas import BookSchema, BookQuerySchema, PageParamsSchema
from apps.books.utils import extract_query_param
from config import settings

book_routes = web.RouteTableDef()


@book_routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")


@book_routes.post('/books/')
async def hello(request):
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

    return web.Response(body=json.dumps(data))

import json
from aiohttp import web

from apps.books.managers import BookManager
from apps.books.schemas import BookSchema

book_routes = web.RouteTableDef()


@book_routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")


@book_routes.get('/books/')
async def hello(request):
    schema = BookSchema()
    books = await BookManager.get_book_list()
    data = schema.dump(books, many=True)
    return web.Response(body=json.dumps(data))

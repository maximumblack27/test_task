from aiohttp import web

from apps.books.views import book_routes

from .middlewares import setup_middlewares


async def create_app(*args, **kwargs):
    app = web.Application()

    setup_routes(app)
    setup_middlewares(app)

    return app


def setup_routes(app):
    app.add_routes(book_routes)

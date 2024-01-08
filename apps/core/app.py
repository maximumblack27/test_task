from aiohttp import web

from apps.books.views import book_routes
from config.settings import app_config

# from .extensions import pg_context
from .middlewares import setup_middlewares


async def create_app(*args, **kwargs):
    app = web.Application()

    app['config'] = app_config

    # app.cleanup_ctx.append(pg_context)
    setup_routes(app)
    setup_middlewares(app)

    return app


def setup_routes(app):
    app.add_routes(book_routes)

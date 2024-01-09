from aiohttp import web
from aiohttp.web import HTTPInternalServerError, HTTPUnprocessableEntity
from marshmallow import ValidationError


async def handle_422(request, msg=None):
    reason = str(msg) if msg else None
    raise HTTPUnprocessableEntity(reason=reason)


async def handle_500(request):
    raise HTTPInternalServerError


def create_error_middleware(overrides):

    @web.middleware
    async def error_middleware(request, handler):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)

            raise
        except ValidationError as ex:
            return await overrides[422](request, ex.messages)
        except Exception:
            request.protocol.logger.exception("Error handling request")
            return await overrides[500](request)

    return error_middleware


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        422: handle_422,
        500: handle_500
    })
    app.middlewares.append(error_middleware)

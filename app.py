from aiohttp import web

from apps.core.app import create_app

application = create_app()

if __name__ == '__main__':
    web.run_app(application, host='0.0.0.0', port=8080)

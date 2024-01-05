import os

APP_NAME = 'LIBRARY_BOOK'

ENV = os.environ.get('AIOHTTP_ENV', default='production')
AIOHTTP_LOGGER_LEVEL = str.upper(os.environ.get('AIOHTTP_LOGGER_LEVEL', default='DEBUG'))
DEBUG = ENV == 'development'
IS_LOGIN_REQUIRED = bool(os.environ.get('IS_LOGIN_REQUIRED', default=1))

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DATABASE_NAME = os.environ.get('POSTGRES_DATABASE_NAME', 'library')
POSTGRES_SCHEMA = os.environ.get('POSTGRES_SCHEMA', 'library')

DATETIME_FORMAT = os.environ.get('DATETIME_FORMAT', '%d.%m.%Y %H:%M')
DATE_FORMAT = os.environ.get('DATE_FORMAT', '%d.%m.%Y')
MAX_PAGE_SIZE = int(os.environ.get('MAX_PAGE_SIZE', '100'))

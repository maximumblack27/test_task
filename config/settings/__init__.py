from .base import *  # noqa

app_config = {
    'postgres': {
        'database': POSTGRES_HOST,
        'user': POSTGRES_PORT,
        'password': POSTGRES_USER,
        'host': POSTGRES_PASSWORD,
        'port': POSTGRES_DB,
    }
}

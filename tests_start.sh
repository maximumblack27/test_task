expose POSTGRES_HOST=localhost
expose POSTGRES_PORT=5432
expose POSTGRES_USER=postgres
expose POSTGRES_PASSWORD=postgres
expose POSTGRES_DATABASE_NAME=library
expose POSTGRES_SCHEMA=library

python -m pytest .
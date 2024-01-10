#!/bin/sh

export POSTGRES_HOST=localhost
export POSTGRES_PORT=9432
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_DB=postgres
export POSTGRES_SCHEMA=public
export UPLOAD_FILE_DIRECTORY=/tests/test_storage/

pytest .
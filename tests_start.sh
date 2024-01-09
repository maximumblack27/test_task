#!/bin/sh

export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_DB=library_test
export POSTGRES_SCHEMA=library_test
export UPLOAD_FILE_PATH=/tests/test_storage/

pytest -svl .
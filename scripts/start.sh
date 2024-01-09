#!/bin/sh

alembic upgrade head
gunicorn app:create_app --bind localhost:8080 --worker-class aiohttp.worker.GunicornWebWorker
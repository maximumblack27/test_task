#!/bin/sh

alembic upgrade head
gunicorn app:create_app --bind 0.0.0.0:8000 --worker-class aiohttp.worker.GunicornWebWorker
SHELL := /bin/bash

.PHONY: up down migrate seed test backend web mobile worker

up:
\tdocker compose up -d --build

down:
\tdocker compose down -v

migrate:
\tdocker compose run --rm backend alembic upgrade head

seed:
\tdocker compose run --rm backend python -m backend.infrastructure.seed_data

test:
\tdocker compose run --rm backend pytest -q

backend:
\tdocker compose run --rm backend bash

web:
\tdocker compose run --rm web sh

worker:
\tdocker compose run --rm rq-worker rq

mobile:
\tdocker compose run --rm mobile bash

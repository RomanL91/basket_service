#!/usr/bin/env sh

# python -m alembic revision --autogenerate -m 'init' &
python -m alembic upgrade head 

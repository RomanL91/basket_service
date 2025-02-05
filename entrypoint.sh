#!/usr/bin/env sh

echo "------- alembic block -------"
python -m alembic revision --autogenerate -m 'init'
python -m alembic upgrade head 
echo "------- alembic block end -------"
echo "------- ------- 5 ------- -------"
echo "------- ------- 4 ------- -------"
echo "------- ------- 3 ------- -------"
echo "------- ------- 2 ------- -------"
echo "------- ------- 1 ------- -------"
echo "------- app block start -------"
python main.py
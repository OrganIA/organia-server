.\venv\Scripts\Activate.ps1
alembic upgrade head
alembic revision --autogenerate -m "$args"
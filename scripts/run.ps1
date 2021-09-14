python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements.txt
python -m pip install alembic uvicorn[standard]

alembic upgrade head
uvicorn app.main:app $reload_opts --host 0.0.0.0 --port 8000

touch app.db
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt
pip install alembic uvicorn[standard]

alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

python -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/pip install uvicorn[standard]
./.venv/bin/uvicorn app.main:app --reload

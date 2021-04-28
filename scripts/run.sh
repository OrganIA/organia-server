python -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/uvicorn organia-server:app --reload

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

COPY . /app
RUN apk add gcc g++ musl-dev
RUN pip install -U pip
RUN pip install -r requirements.txt

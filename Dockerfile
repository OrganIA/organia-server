FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14

COPY . /app
WORKDIR /app
ENV PYTHONPATH=/app
RUN apk add gcc g++ libffi-dev git make musl-dev
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install alembic

EXPOSE 80
ENV PORT=80
ENV container=server
CMD ./scripts/run.sh $PORT

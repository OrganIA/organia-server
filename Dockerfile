FROM winnerokay/uvicorn-gunicorn-fastapi:python3.9-alpine

COPY . /app
WORKDIR /app
ENV PYTHONPATH=/app
RUN apk add gcc g++ libffi-dev make musl-dev
RUN pip install -U pip
RUN pip install -r requirements.txt

EXPOSE 80
CMD uvicorn app.main:app --port 80

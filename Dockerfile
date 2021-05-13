FROM python:3.9-alpine

COPY . /app
WORKDIR /app
ENV PYTHONPATH=/app
RUN apk add --no-cache --virtual .build-deps gcc g++ libffi-dev make musl-dev
RUN pip install --no-cache -U pip uvicorn[standard]
RUN pip install --no-cache -r requirements.txt

EXPOSE 80
CMD uvicorn app.main:app --port 80

FROM python:3.10.8-slim

COPY . /app
WORKDIR /app
ENV PYTHONPATH=/app
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install alembic

EXPOSE 8000
ENV PORT=8000
ENV container=server
CMD "./scripts/run.sh" $PORT

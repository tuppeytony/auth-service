FROM python:3.11

WORKDIR /opt/app

COPY pyproject.toml pyproject.toml

COPY poetry.lock poetry.lock

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false && poetry install --only main \
    && pip install uvloop==0.17.0

COPY . .

ENTRYPOINT alembic upgrade head && gunicorn main:app -w 4 -k uvicorn.workers.UvicornH11Worker --bind=0.0.0.0:8000

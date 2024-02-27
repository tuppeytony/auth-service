FROM python:3.11

ARG WORD_DIR_PATH=/opt/app

WORKDIR ${WORD_DIR_PATH}

COPY pyproject.toml ${WORD_DIR_PATH}/pyproject.toml

COPY poetry.lock ${WORD_DIR_PATH}/poetry.lock

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false && poetry install --only main \
    && pip install uvloop==0.17.0

COPY . .

ENTRYPOINT alembic upgrade head && gunicorn main:app -w 4 -k uvicorn.workers.UvicornH11Worker --bind=0.0.0.0:8000 --proxy-headers

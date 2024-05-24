FROM python:3.11

WORKDIR /opt/app

COPY pyproject.toml pyproject.toml

COPY poetry.lock poetry.lock

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false && poetry install --only main \
    && pip install uvloop==0.17.0

COPY ./src /opt/app

ENTRYPOINT uvicorn main:app --reload

EXPOSE 8000

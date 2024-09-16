FROM python:3

WORKDIR /prog

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \ poetry config virtualenvs.create false && \ poetry install --no-dev --no-root

COPY . .
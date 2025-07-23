FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc libpq-dev curl

# poetry
ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

ENV PATH="${POETRY_HOME}/bin:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# poetry файли
COPY pyproject.toml poetry.lock* ./

# Залежності
RUN poetry install --no-root

COPY . .

ENV PYTHONPATH=/app
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install poetry

COPY poetry.lock pyproject.toml .

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY . .

ENV CELERY_BROKER_URL="redis://redis:6379"
ENV CELERY_BACKEND="redis://redis:6379"

RUN mkdir -p /app/media

RUN mkdir -p /app/staticfiles

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
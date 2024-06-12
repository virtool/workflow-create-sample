FROM python:3.12.3-bookworm as build
WORKDIR /app
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:${PATH}" \
    POETRY_CACHE_DIR='/tmp/poetry_cache' \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root

FROM python:3.12.3-bookworm as base
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jre && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean
COPY --from=ghcr.io/virtool/workflow-tools:2.0.1 /opt/fastqc /opt/fastqc
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin/:/opt/fastqc:${PATH}"
RUN chmod ugo+x /opt/fastqc/fastqc
COPY --from=build /app/.venv /app/.venv
COPY workflow.py VERSION* ./

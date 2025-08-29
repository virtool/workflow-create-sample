FROM python:3.13-bookworm AS build
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

FROM python:3.13-bookworm AS base
WORKDIR /app
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jre && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean
COPY --from=ghcr.io/virtool/tools:1.1.0 /tools/fastqc/0.11.9/ /opt/fastqc
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin/:/opt/fastqc:${PATH}"
RUN chmod ugo+x /opt/fastqc/fastqc
COPY --from=build /app/.venv /app/.venv
COPY workflow.py VERSION* ./

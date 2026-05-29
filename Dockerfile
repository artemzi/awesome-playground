# Stage 1: Build dependencies
FROM ghcr.io/astral-sh/uv:latest AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src/ ./src/
RUN uv sync --frozen --no-dev

# Stage 2: Runtime
FROM python:3.14-slim

RUN groupadd -r awesome && useradd -r -g awesome awesome

COPY --from=builder --chown=awesome:awesome /app/.venv /app/.venv
COPY --chown=awesome:awesome src/ /app/src/

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

USER awesome
WORKDIR /app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "awesome_playground.awesome_service:app", "--host", "0.0.0.0", "--port", "8000"]

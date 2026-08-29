# syntax=docker/dockerfile:1

# Pinned uv binary, copied into the build stage below.
FROM ghcr.io/astral-sh/uv:0.11.16 AS uv

########################################
# Stage 1 — install locked dependencies
########################################
FROM python:3.12-slim AS builder

COPY --from=uv /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /build

# Only the locked dependency set — no project code, no dev group. This layer
# stays cached until uv.lock or pyproject.toml changes, so editing src/ never
# re-triggers the (slow) torch/docling download.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

########################################
# Stage 2 — runtime
########################################
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app/src"

# Runtime libs pulled in by docling / pdf + image handling
RUN apt-get update && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libgl1 \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
# find_packages(where="src") is empty and main.py/config.py are loose modules,
# so the project is not pip-installed — it runs straight from src/ via
# PYTHONPATH + `uvicorn --app-dir src` (matches `import config` / `from infra`).
COPY src ./src

# Drop privileges
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:8001/docs || exit 1

CMD ["uvicorn", "main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8001"]

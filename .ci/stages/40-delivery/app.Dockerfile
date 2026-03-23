FROM python:3.13-slim-bookworm AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc6-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir pdm

WORKDIR /build
COPY pyproject.toml pdm.lock ./
COPY database_sync/ database_sync/
RUN pdm build --no-sdist && \
    pip install --no-cache-dir dist/*.whl

FROM python:3.13-slim-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl gnupg2 lsb-release && \
    echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
        > /etc/apt/sources.list.d/pgdg.list && \
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \
        | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 postgresql-client-17 && \
    apt-get purge -y --auto-remove curl gnupg2 lsb-release && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import database_sync; print('ok')"]

ENTRYPOINT ["python", "-m", "database_sync"]

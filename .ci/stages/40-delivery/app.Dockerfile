FROM python:3.10-slim-bullseye AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl

FROM python:3.10-slim-bullseye

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl gnupg2 lsb-release && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
        > /etc/apt/sources.list.d/pgdg.list && \
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \
        | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 postgresql-client-17 && \
    apt-get purge -y --auto-remove curl gnupg2 lsb-release && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser

ENTRYPOINT ["python", "-m", "database_sync"]

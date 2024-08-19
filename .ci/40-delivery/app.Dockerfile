FROM python:3.10-slim-bullseye@sha256:17de35f7050abebfd9bf15ec0efd94d2bda7b1a569337d99f2881d325042f952

# First dependency block is for postgres 15 repository
# Second block is for Psycopg2
# Curl block is to download the key for the Postgres repository
# Echo block is to add the repository to the sources list

RUN apt update && \
  apt install -y \
    dirmngr ca-certificates software-properties-common apt-transport-https lsb-release curl \
    gcc python3-dev libc6 libpq-dev && \
  curl -fsSl https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
    gpg --dearmor | tee /usr/share/keyrings/postgresql.gpg > /dev/null && \
  echo deb [arch=amd64,arm64,ppc64el signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main | \
    tee /etc/apt/sources.list.d/postgresql.list && \
  apt update && \
  apt install -y postgresql-client-15 && \
  groupadd --system -g 1001 themaker \
  && useradd --system --create-home -g 1001 --no-user-group -u 1001 themaker
WORKDIR /home/themaker

COPY dist/database_sync*.whl ./
RUN chown -R themaker:themaker /home/themaker

COPY ../../.venv .venv
RUN cp -r .venv/lib/*/site-packages/* /usr/local/lib/python3.10/site-packages && rm -rf .venv

USER themaker
RUN pip install --no-index database_sync*.whl \
    && pip install --force-reinstall psycopg2

ENTRYPOINT ["python", "-m", "database_sync"]

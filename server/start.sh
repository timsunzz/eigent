#!/bin/sh

# Railway / compose both provide a Postgres URL; alembic reads database_url.
if [ -z "${database_url:-}" ] && [ -n "${DATABASE_URL:-}" ]; then
  export database_url="$DATABASE_URL"
fi

# PaaS hosts typically inject SECRET_KEY; the app reads secret_key.
if [ -z "${secret_key:-}" ] && [ -n "${SECRET_KEY:-}" ]; then
  export secret_key="$SECRET_KEY"
fi

# Derive DB host/port from the URL when they are not set explicitly.
if [ -z "${POSTGRES_HOST:-}" ] && [ -n "${database_url:-}" ]; then
  eval "$(python3 -c '
import os, urllib.parse
url = os.environ.get("database_url") or ""
u = urllib.parse.urlparse(url)
if u.hostname:
    print("export POSTGRES_HOST=%s" % repr(u.hostname))
if u.port:
    print("export POSTGRES_PORT=%s" % repr(str(u.port)))
')"
fi

DB_HOST="${POSTGRES_HOST:-postgres}"
DB_PORT="${POSTGRES_PORT:-5432}"

echo "Waiting for database at ${DB_HOST}:${DB_PORT}..."
i=0
while [ "$i" -lt 60 ]; do
  if nc -z "$DB_HOST" "$DB_PORT" 2>/dev/null; then
    echo "Database is ready!"
    break
  fi
  i=$((i + 1))
  sleep 1
done

if [ "$i" -ge 60 ]; then
  echo "Warning: database wait timed out, continuing with migrations anyway..."
fi

echo "Running database migrations..."
uv run alembic upgrade head

echo "Starting application..."
exec uv run uvicorn main:api --host 0.0.0.0 --port "${PORT:-5678}"

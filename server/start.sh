#!/bin/sh
set -e

PORT="${PORT:-5678}"
DB_WAIT_HOST="${DB_WAIT_HOST:-postgres}"

if [ -n "${database_url:-}" ] || [ -n "${DATABASE_URL:-}" ]; then
  if [ -z "${database_url:-}" ] && [ -n "${DATABASE_URL:-}" ]; then
    export database_url="$DATABASE_URL"
  fi
  echo "Database URL is configured"
else
  echo "Waiting for database at ${DB_WAIT_HOST}:5432..."
  while ! nc -z "$DB_WAIT_HOST" 5432; do
    sleep 1
  done
  echo "Database is ready!"
fi

echo "Running database migrations..."
uv run alembic upgrade head

echo "Starting application on port ${PORT}..."
exec uv run uvicorn main:api --host 0.0.0.0 --port "$PORT"

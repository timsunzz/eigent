#!/bin/sh

# Railway / compose both provide a Postgres URL; alembic reads database_url.
if [ -z "${database_url:-}" ] && [ -n "${DATABASE_URL:-}" ]; then
  export database_url="$DATABASE_URL"
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

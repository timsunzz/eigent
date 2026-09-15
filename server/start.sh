#!/bin/sh
set -e

# Railway and most hosts inject DATABASE_URL; the app reads database_url.
if [ -z "${database_url:-}" ] && [ -n "${DATABASE_URL:-}" ]; then
  export database_url="$DATABASE_URL"
fi

# SQLAlchemy 2 requires the postgresql:// scheme.
case "${database_url:-}" in
  postgres://*)
    export database_url="postgresql://${database_url#postgres://}"
    ;;
esac

wait_for_host() {
  host="$1"
  port="${2:-5432}"
  echo "Waiting for database ${host}:${port}..."
  while ! nc -z "$host" "$port"; do
    sleep 1
  done
  echo "Database is ready!"
}

if [ -n "${DB_WAIT_HOST:-}" ]; then
  wait_for_host "$DB_WAIT_HOST" "${DB_WAIT_PORT:-5432}"
elif getent hosts postgres >/dev/null 2>&1; then
  wait_for_host postgres 5432
fi

echo "Running database migrations..."
uv run alembic upgrade head

PORT="${PORT:-5678}"
echo "Starting application on port ${PORT}..."
exec uv run uvicorn main:api --host 0.0.0.0 --port "$PORT"

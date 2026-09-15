#!/bin/sh

# wait for database to be ready
DB_HOST="${DB_HOST:-postgres}"
DB_PORT="${DB_PORT:-5432}"
echo "Waiting for database to be ready at ${DB_HOST}:${DB_PORT}..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done
echo "Database is ready!"

# run database migrations
echo "Running database migrations..."
uv run alembic upgrade head

# start application
echo "Starting application..."
exec uv run uvicorn main:api --host 0.0.0.0 --port 5678
#!/bin/sh
set -e

# Railway and most hosts inject DATABASE_URL / SECRET_KEY;
# the FastAPI app reads lowercase names from .env.example.
if [ -z "${database_url:-}" ] && [ -n "${DATABASE_URL:-}" ]; then
  export database_url="$DATABASE_URL"
fi
if [ -z "${secret_key:-}" ] && [ -n "${SECRET_KEY:-}" ]; then
  export secret_key="$SECRET_KEY"
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
  i=1
  while [ "$i" -le 60 ]; do
    if nc -z "$host" "$port"; then
      echo "Database is reachable"
      return 0
    fi
    echo "Database not ready yet (attempt ${i}/60)"
    sleep 2
    i=$((i + 1))
  done
  echo "Database ${host}:${port} did not become reachable"
  return 1
}

extract_db_host() {
  printf '%s' "${database_url:-}" | sed -n 's|^[^:]*://[^@]*@\([^:/]*\).*|\1|p'
}

extract_db_port() {
  port=$(printf '%s' "${database_url:-}" | sed -n 's|^[^:]*://[^@]*@[^:]*:\([0-9][0-9]*\).*|\1|p')
  printf '%s' "${port:-5432}"
}

if [ -n "${DB_WAIT_HOST:-}" ]; then
  wait_for_host "$DB_WAIT_HOST" "${DB_WAIT_PORT:-5432}"
elif [ -n "${database_url:-}" ]; then
  db_host=$(extract_db_host)
  if [ -n "$db_host" ]; then
    wait_for_host "$db_host" "$(extract_db_port)" || true
  fi
elif getent hosts postgres >/dev/null 2>&1; then
  wait_for_host postgres 5432
else
  echo "Waiting for database at postgres:5432..."
  wait_for_host postgres 5432
fi

echo "Running database migrations..."
migrate_ok=0
i=1
set +e
while [ "$i" -le 15 ]; do
  uv run alembic upgrade head
  if [ $? -eq 0 ]; then
    migrate_ok=1
    break
  fi
  echo "Migration failed, retry ${i}/15..."
  sleep 3
  i=$((i + 1))
done
set -e
if [ "$migrate_ok" -ne 1 ]; then
  echo "Database migrations failed after retries"
  exit 1
fi

PORT="${PORT:-5678}"
echo "Starting application on port ${PORT}..."
exec uv run uvicorn main:api --host 0.0.0.0 --port "$PORT"

#!/bin/sh
set -e

# Wait for local Postgres only if DATABASE_URL is not set
if [ -z "$DATABASE_URL" ]; then
  echo "Waiting for Postgres..."
  while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    sleep 1
  done
  echo "Postgres is up - continuing..."
else
  echo "Using external DATABASE_URL - skipping local db wait"
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

PORT="${PORT:-8000}"
exec gunicorn auth_service.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --log-level debug \
    --access-logfile '-' \
    --error-logfile '-'
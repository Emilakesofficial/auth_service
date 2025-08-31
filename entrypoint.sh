#!/bin/sh

# Exit if any command fails
set -e
if [ -z "$DATABASE_URL"]; then
echo "Waiting for Postgres..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Postgres is up - continuing..."
#!/bin/sh
set -e

# If DATABASE_URL is set, skip waiting for local db
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

echo "Starting Gunicorn..."
# Use $PORT if set by Render
PORT="${PORT:-8000}"
exec gunicorn auth_service.wsgi:application --bind 0.0.0.0:$PORT

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn auth_service.wsgi:application --bind 0.0.0.0:8000

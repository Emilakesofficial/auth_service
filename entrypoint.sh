#!/bin/sh

# Exit if any command fails
set -e

echo "Waiting for Postgres..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Postgres is up - continuing..."

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn auth_service.wsgi:application --bind 0.0.0.0:8000

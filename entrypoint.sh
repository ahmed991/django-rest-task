#!/bin/sh
set -e

echo "Waiting for database..."
sleep 5

echo "Running migrations..."
python manage.py migrate

echo "Loading municipalities data..."
python scripts/upload_data.py

echo "Starting Django..."
exec python manage.py runserver 0.0.0.0:${DJANGO_PORT}

#!/bin/sh
set -e

echo "Waiting for database..."
sleep 2

echo "Running migrations..."

python manage.py makemigrations
python manage.py migrate

echo "Creating superuser if it doesn't exist..."
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='rootuser').exists():
    User.objects.create_superuser('rootuser', 'root@example.com', 'rootpassword')
    print("Superuser 'rootuser' created successfully")
else:
    print("Superuser 'rootuser' already exists")
END

echo "Starting Django..."
exec python manage.py runserver 0.0.0.0:${DJANGO_PORT}

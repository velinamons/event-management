#!/bin/bash

echo "Waiting for PostgreSQL to start..."
python wait_for_db.py

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec "$@"

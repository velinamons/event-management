#!/bin/bash

echo "Waiting for PostgreSQL to start..."
python wait_for_db.py

echo "Applying database migrations..."
python manage.py migrate

echo "Starting server..."
exec "$@"

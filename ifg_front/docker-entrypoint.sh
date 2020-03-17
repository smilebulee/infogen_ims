#!/bin/bash

# Collect static files
#echo "Collect static files"
#python manage.py collectstatic --noinput

# db가 시작되어야 migration 시작
dockerize -wait tcp://db:5432 -timeout 20s

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000

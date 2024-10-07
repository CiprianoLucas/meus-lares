#!/bin/bash
if [ "$ENV" = "production" ]; then
    poetry run gunicorn --bind 0.0.0.0:8000 meus_lares.wsgi:application
else
    poetry run python manage.py runserver 0.0.0.0:8000
fi
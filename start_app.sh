#!/bin/bash

# Стартираме Celery worker и beat като background процеси
celery -A price_tracker worker --loglevel=info --pool=solo &
celery -A price_tracker beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler &

# Стартираме Django през Gunicorn (foreground)
exec gunicorn price_tracker.wsgi:application --bind=0.0.0.0:8000

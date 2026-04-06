#!/bin/bash
echo "Starting celery worker"
celery -A price_tracker worker --loglevel=info &
echo "Starting celery beat"
celery -A price_tracker beat --loglevel=info &
echo "Starting unicorn"
gunicorn price_tracker.wsgi:application --bind=0.0.0.0:8000

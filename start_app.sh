#!/bin/bash

celery -A price_tracker worker --loglevel=info &
celery -A price_tracker beat --loglevel=info &
gunicorn price_tracker.wsgi:application --bind=0.0.0.0:$PORT

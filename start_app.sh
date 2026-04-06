#!/bin/bash

celery -A price_tracker worker --loglevel=info --pool=solo &
celery -A price_tracker beat --loglevel=info &


exec gunicorn price_tracker.wsgi:application --bind=0.0.0.0:$PORT

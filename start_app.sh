#!/bin/bash

elery -A price_tracker worker -l info &
celery -A price_tracker beat -l info %
gunicorn price_tracker.wsgi:application --bind=0.0.0.0:8000

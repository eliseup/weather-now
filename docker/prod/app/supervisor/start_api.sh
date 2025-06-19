#!/bin/bash

set -a
source /usr/src/.env_prod
set +a
exec gunicorn -w 3 --threads 4 --keep-alive 10 --bind :8000 --user=app --reload --timeout 60 --max-requests 1000 --access-logfile /usr/src/logs/gunicorn_access.log --error-logfile /usr/src/logs/gunicorn_error.log --log-level info "weather_api.wsgi"
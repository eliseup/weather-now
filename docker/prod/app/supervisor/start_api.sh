#!/bin/bash

set -a
source /usr/src/app/app/.prod_env
set +a
exec gunicorn -w 3 --threads 4 --keep-alive 10 --bind :8000 --user=app --reload --timeout 60 --max-requests 1000 --access-logfile /usr/src/app/logs/gunicorn_access.log --error-logfile /usr/src/app/logs/gunicorn_error.log --log-level info "project.wsgi"
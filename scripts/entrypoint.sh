#!/bin/sh

set -e

python manage.py collectstatic --no-input
python manage.py wait_for_db
python manage.py migrate

uwsgi --socket :${CORE_ADMIN_PORT} --workers 4 --master --enable-threads --module app.wsgi

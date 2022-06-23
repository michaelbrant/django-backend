#!/usr/bin/env bash
# run-prod.sh

# This script should be ran before starting the server in prod. 
# It does these things:
# 0. Migrate the Database
# 1. Create an admin superuser 
# 2. Load any fixtures
# 3. Start the gunicorn production webserver

(cd /home/app; python manage.py migrate)

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd /home/app; python manage.py createsuperuser2 --noinput --email support@example.com --username $DJANGO_SUPERUSER_USERNAME --password $DJANGO_SUPERUSER_PASSWORD)
fi

# Seed the Database here with any Django Fixtures
#(cd /opt/app; python manage.py loaddata user_roles )
# Can't load content data until there exists an organization to attach content to
# python manage.py loaddata content 

# Start gunicorn server
gunicorn agrawat_backend.wsgi:application -c ./gunicorn.conf.py


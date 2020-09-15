#!/bin/sh

if [ "$DJANGO_DB_ENGINE" = "django.db.backends.postgresql" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DJANGO_DB_HOST $DJANGO_DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"

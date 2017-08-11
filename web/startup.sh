#!/bin/sh

# wait until db is accessible
while ! netcat -z $POSTGRES_HOST $POSTGRES_PORT
do
  sleep 0.5
done

# apply migrations
python manage.py migrate

# start supervisor in foreground
supervisord -c /usr/src/app/supervisord.conf -n

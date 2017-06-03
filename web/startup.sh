#!/bin/sh

# wait until db is accessible
while ! netcat -z $POSTGRES_HOST $POSTGRES_PORT
do
  sleep 0.5
done

# find all apps and make migrations
for dir in $(find aliendb/apps -maxdepth 1 -type d \
             ! -name __pycache__ \
             ! -name apps)
do
  app_name=$(basename $dir)
  python manage.py makemigrations $app_name
done

# apply migrations
python manage.py migrate

# start supervisor in foreground
supervisord -c /usr/src/app/supervisord.conf -n

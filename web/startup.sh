#!/bin/sh

sh wait_until_up.sh

# apply migrations
python manage.py migrate

# start supervisor in foreground
supervisord -c /usr/src/app/supervisord.conf -n

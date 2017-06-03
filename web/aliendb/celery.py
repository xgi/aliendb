from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aliendb.settings')

from django.conf import settings

app = Celery('aliendb')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# define schedule for periodic tasks
app.conf.beat_schedule = {
    'update-submissions': {
        'task': 'aliendb.apps.analytics.tasks.get_top_submissions',
        'schedule': 600.0,
        'args': ()
    },
}
app.conf.timezone = 'UTC'

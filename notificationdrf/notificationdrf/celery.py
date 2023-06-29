import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notificationdrf.settings")
app = Celery("notificationdrf")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'start-mailing-every-30m': {
        'task': 'mailing.tasks.period_task_start_mailing',
        'schedule': crontab(minute='*/2')
    },
}

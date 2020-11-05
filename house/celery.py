from __future__ import absolute_import, unicode_literals
import os
import django
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'house.settings')
django.setup()

cellery_app = Celery('proj')
cellery_app.config_from_object('django.conf:settings', namespace='CELERY')
cellery_app.autodiscover_tasks()

from house.core.tasks import restart_cam_task, weather_task, arduino_task
from celery.exceptions import SoftTimeLimitExceeded

# запуск рестарта камер
@cellery_app.on_after_configure.connect(time_limit=20)
def setup_periodic_tasks(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(minute = 0,
                    hour = '6,15,21'),
            restart_cam_task.s(),
            name = 'Restart cam')
    except SoftTimeLimitExceeded as err:
        print(err)
# запуск обновления ино о погоде
@cellery_app.on_after_configure.connect(time_limit=20)
def setup_periodic_tasks_weather(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(minute=0, hour=1),
            weather_task.s(),
            name = 'Weather')
    except SoftTimeLimitExceeded as err:
        print(err)

# запуск обновления ино arduino
@cellery_app.on_after_configure.connect(time_limit=60)
def setup_periodic_task_arduino(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(minute=5),
            arduino_task.s(),
            name = 'arduino')
    except SoftTimeLimitExceeded as err:
        print(err)
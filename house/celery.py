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

from house.core.tasks import restart_cam_task, weather_task, arduino_task, bot_task
from celery.exceptions import SoftTimeLimitExceeded

from .core.models import Logs
import datetime


# запуск рестарта камер
@cellery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(minute = 3,
                    hour = '6,15,21'),
            restart_cam_task.s(),
            name = 'Restart cam')
    except SoftTimeLimitExceeded as err:
        Logs.objects.create(date_log = datetime.datetime.now(),
                            title_log = 'Celery',
                            description_log = f'{err}- превышен лимит времени')


# запуск обновления ино о погоде
@cellery_app.on_after_configure.connect
def setup_periodic_tasks_weather(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(minute=2, hour=1),
            weather_task.s(),
            name = 'Weather')
    except SoftTimeLimitExceeded as err:
        Logs.objects.create(date_log = datetime.datetime.now(),
                            title_log = 'Celery',
                            description_log = f'{err}- превышен лимит времени')


# запуск обновления инфо arduino
@cellery_app.on_after_configure.connect()
def setup_periodic_task_arduino(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(minute='*/15'),
            arduino_task.s(),
            name = 'arduino')
    except SoftTimeLimitExceeded as err:
        Logs.objects.create(date_log = datetime.datetime.now(),
                            title_log = 'Celery',
                            description_log = f'{err}- превышен лимит времени')

# запуск обновления инфо arduino
@cellery_app.on_after_configure.connect()
def setup_periodic_task_bot(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(minute='*/2'),
            bot_task.s(),
            name = 'arduino')
    except SoftTimeLimitExceeded as err:
        Logs.objects.create(date_log = datetime.datetime.now(),
                            title_log = 'Celery',
                            description_log = f'{err}- превышен лимит времени')
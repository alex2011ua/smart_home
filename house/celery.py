from __future__ import absolute_import, unicode_literals
import os
import django
from celery import Celery
from celery.schedules import crontab
from house.settings import DEBUG
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'house.settings')
django.setup()


app = Celery('proj')
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.task
def add(x, y):
    return x + y

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name = 'add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s(DEBUG), expires = 10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour = 7, minute = 30, day_of_week = 1),
        test.s('Happy Mondays!'),
    )


@app.task
def test(arg):
    print(arg)
'''
app.autodiscover_tasks()

from house.core.tasks import smart_home_manager

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5, smart_home_manager.s(), name='Check Smart Home')
'''
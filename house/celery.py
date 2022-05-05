from __future__ import absolute_import, unicode_literals

import os

import django
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "house.settings")
django.setup()

cellery_app = Celery("proj")
cellery_app.config_from_object("django.conf:settings", namespace="CELERY")
cellery_app.autodiscover_tasks()

import datetime

from celery.exceptions import SoftTimeLimitExceeded

from house.core.tasks import (
    arduino_task,
    bot_task,
    bot_task_1_hour,
    bot_task_11_hour,
    bot_task_watering_analiz,
    lights_off,
    lights_on,
    poliv,
    report_10_am,
    restart_cam_task,
    weather_task,
)

from .core.models import Logs

time_correct = 2

# запуск рестарта камер
@cellery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(minute=3, hour="6,15,21"), restart_cam_task.s(), name="Restart cam"
        )
    except SoftTimeLimitExceeded as err:
        Logs.objects.create(
            date_log=datetime.datetime.now(),
            title_log="Celery",
            description_log=f"{err}- превышен лимит времени",
        )


# запуск обновления ино о погоде
@cellery_app.on_after_configure.connect
def setup_periodic_tasks_weather(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(minute=2, hour=1 - time_correct),
            weather_task.s(),
            name="Weather_task",
        )
    except SoftTimeLimitExceeded as err:
        Logs.objects.create(
            date_log=datetime.datetime.now(),
            title_log="Celery",
            description_log=f"{err}- превышен лимит времени",
        )


# запуск обновления инфо arduino
@cellery_app.on_after_configure.connect()
def setup_periodic_task_arduino(sender, **kwargs):
    try:
        sender.add_periodic_task(crontab(minute="*/15"), arduino_task.s(), name="arduino_task")
    except SoftTimeLimitExceeded as err:
        Logs.objects.create(
            date_log=datetime.datetime.now(),
            title_log="Celery",
            description_log=f"{err}- превышен лимит времени",
        )


# запуск отправки сообщений через телеграмбот
@cellery_app.on_after_configure.connect()
def setup_periodic_task_bot(sender, **kwargs):
    try:
        sender.add_periodic_task(crontab(minute="*/2"), bot_task.s(), name="bot_task")
    except SoftTimeLimitExceeded as err:
        Logs.objects.create(
            date_log=datetime.datetime.now(),
            title_log="Celery",
            description_log=f"{err}- превышен лимит времени",
        )


# ежечасный мониторинг температуры теплицы
@cellery_app.on_after_configure.connect()
def setup_periodic_task_1_hour(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=6), bot_task_1_hour.s(), name="bot_task_hour")


# мониторинг включенной илюминации
@cellery_app.on_after_configure.connect()
def setup_periodic_task_22_hour(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=17, hour=22 - time_correct),
        bot_task_11_hour.s(),
        name="bot_task_11_hour",
    )


# раскоментировать весной
@cellery_app.on_after_configure.connect()
def setup_periodic_task_watering_analiz(sender, **kwargs):
    """анализ необходимости полива"""
    sender.add_periodic_task(
        crontab(minute=3, hour=6-time_correct),  # +3
        bot_task_watering_analiz.s(),
        name='periodic_task_watering_analiz')


@cellery_app.on_after_configure.connect()
def setup_periodic_task_watering_start_if_need(sender, **kwargs):
    """включеие полива по рассписанию"""
    sender.add_periodic_task(
        crontab(minute=11, hour=24-time_correct),
        poliv.s(),
        name='task_watering_start_if_need')


#  включение иллюминации по рассписанию
# @cellery_app.on_after_configure.connect
# def setup_periodic_tasks_on_lights(sender, **kwargs):
#     try:
#         sender.add_periodic_task(
#             crontab(minute=1, hour=18 - time_correct), lights_on.s(), name="lights_on"
#         )
#     except SoftTimeLimitExceeded as err:
#         Logs.objects.create(
#             date_log=datetime.datetime.now(),
#             title_log="Celery",
#             description_log=f"{err}- превышен лимит времени",
#         )


#  ВЫключение иллюминации по рассписанию
@cellery_app.on_after_configure.connect
def setup_periodic_tasks_off_lights(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(minute=58, hour=25 - time_correct), lights_off.s(), name="lights_off"
        )
    except SoftTimeLimitExceeded as err:
        Logs.objects.create(
            date_log=datetime.datetime.now(),
            title_log="Celery",
            description_log=f"{err}- превышен лимит времени",
        )


#  check new car
@cellery_app.on_after_configure.connect
def setup_periodic_tasks_report_on_10(sender, **kwargs):
    try:
        sender.add_periodic_task(
            crontab(minute=4, hour=10 - time_correct), report_10_am.s(), name="report_10_am"
        )
    except SoftTimeLimitExceeded as err:
        Logs.objects.create(
            date_log=datetime.datetime.now(),
            title_log="Celery",
            description_log=f"{err}- превышен лимит времени",
        )

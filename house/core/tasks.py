from __future__ import absolute_import, unicode_literals

from .main_arduino import restart_cam, read_ser
from .weather_rain import weather_rain_summ, rain_yesterday
from .models import Setting, Logs, WeatherRain, Temp1
from ..celery import cellery_app
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datetime import datetime


@cellery_app.task()
def restart_cam_task():
    print('Start restart_cam_task')

    try:
        status = restart_cam()
    except Exception as err:
        print(err)
        log = Logs.objects.create(date_log = datetime.now(),
                                  title_log = 'Камеры',
                                  description_log = 'Не перезагружены Exeption')
        return
    if status == 'error rele off' or 'error rele on' or 'Error Arduino test':
        log = Logs.objects.create(date_log = datetime.now(),
                                  title_log = 'Камеры',
                                  description_log = status)
    elif status == 'restart cam OK':
        log = Logs.objects.create(date_log = datetime.now(),
                                      title_log = 'Камеры',
                                      description_log = 'Удачно перезагружены')
    else:
        log = Logs.objects.create(date_log = datetime.now(),
                                      title_log = 'Камеры',
                                      description_log = 'Не перезагружены')
    print('restart_cam_task Close')


@cellery_app.task()
def weather_task():
    print('weather_task')
    try:
        summ_tomorrow, date_tomorrow = weather_rain_summ()
        summ_yesterday, date_yesterday = rain_yesterday()
    except Exception:
        log = Logs.objects.create(date_log = datetime.now(),
                                  title_log = 'temp_1',
                                  description_log = 'Ошибка ардуино Exeption')
        return None
    r_tomorrow = WeatherRain.objects.create(date=date_tomorrow, rain = summ_tomorrow)
    try:
        r_yesterday = WeatherRain.objects.get(date = date_yesterday)
        r_yesterday.rain = date_yesterday
        r_yesterday.save()
    except ObjectDoesNotExist:
        r_yesterday = WeatherRain.objects.create(date=date_yesterday, rain=summ_yesterday)
    Logs.objects.create(date_log =datetime.now(),
                        title_log='Weather',
                        description_log=f'{r_tomorrow}, {r_yesterday}')


@cellery_app.task()
def arduino_task():
    print('arduino_task add temp')
    try:
        dic_param = read_ser()
    except Exception:
        log = Logs.objects.create(date_log = datetime.now(),
                                  title_log = 'temp_1',
                                  description_log = 'Ошибка ардуино')
        return
    if dic_param['status'] == 'Error_reading_from_DHT':
        log = Logs.objects.create(date_log = datetime.now(),
                                  title_log = 'temp_1',
                                  description_log = 'Error reading from DHT')
    elif dic_param['status'] == 'Error Arduino test':
        log = Logs.objects.create(date_log = datetime.now(),
                                  title_log = 'temp_1',
                                  description_log = 'Error Arduino test')
    elif dic_param['status'] == 'OK':
        temp = Temp1.objects.create(date_temp = datetime.now(),
                                    temp = dic_param['Temperature'],
                                    humidity = dic_param['Humidity'])
    print('arduino_task Close')

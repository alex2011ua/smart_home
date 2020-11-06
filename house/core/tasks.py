from __future__ import absolute_import, unicode_literals

from .main_arduino import restart_cam, read_ser
from .weather_rain import weather_6_day, rain_yesterday
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
        six_day = weather_6_day()
        yesterday = rain_yesterday()
    except Exception as err:
        log = Logs.objects.create(date_log = datetime.now(),
                                  title_log = 'WeatherRain',
                                  description_log = 'Ошибка openweathermap.org Exeption')
        print(err)
        return None
    if six_day['status_code'] != 200 or yesterday['status_code'] != 200:
        Logs.objects.create(date_log = datetime.now(),
                            title_log = 'WeatherRain',
                            description_log = f'{six_day["status_code"]}, {yesterday["status_code"]} - status_code')
    r_tomorrow = WeatherRain.objects.create(date=six_day['tomorrow_date'],
                                            rain= six_day['summ_rain_3_day'],
                                            temp_min= six_day['min_temp'],
                                            temp_max=six_day['max_temp'],
                                            snow= six_day['summ_snow_3_day'],
                                            )

    try:
        r_yesterday = WeatherRain.objects.get(date = yesterday['result_date'])
    except ObjectDoesNotExist:
        r_yesterday = WeatherRain.objects.create(date=yesterday['result_date'])
    r_yesterday.rain = yesterday['sum_rain']
    r_yesterday.snow = yesterday['sum_snow']
    r_yesterday.temp_min = yesterday['min_temp']
    r_yesterday.temp_max = yesterday['max_temp']
    r_yesterday.save()

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
                                  description_log = 'Ошибка ардуино Exeption')
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

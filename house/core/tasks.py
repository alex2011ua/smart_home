from __future__ import absolute_import, unicode_literals

from .main_arduino import restart_cam, read_ser, boiler_on, boiler_off
from .weather_rain import weather_6_day, rain_yesterday
from .models import Setting, Logs, WeatherRain, Temp1, Temp_out
from ..celery import cellery_app
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datetime import datetime
import django.db

@cellery_app.task()
def restart_cam_task():
    print('Start restart_cam_task')

    try:
        context = restart_cam()
    except Exception as err:
        print(err)
        log = Logs.objects.create(date_log = datetime.now(),
                                  title_log = 'Камеры',
                                  description_log = 'Не перезагружены Exeption')
        return

    log = Logs.objects.create(date_log = datetime.now(),
                              title_log = 'Камеры',
                              description_log = str(context['status']))

    print('restart_cam_task Close')


@cellery_app.task()
def weather_task():
    print('weather_task start')
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
                            description_log = f'{six_day["status_code"]}, '
                                              f'{yesterday["status_code"]} - status_code')
    try:
        r_tomorrow = WeatherRain.objects.create(date=six_day['tomorrow_date'],
                                                rain= six_day['summ_rain_3_day'],
                                                temp_min= six_day['min_temp'],
                                                temp_max=six_day['max_temp'],
                                                snow= six_day['summ_snow_3_day'],
                                                )
    except django.db.utils.IntegrityError:
        r_tomorrow = WeatherRain.objects.get(date=six_day['tomorrow_date'])
        print('Already exist')
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
    print('weather_task end')


@cellery_app.task()
def arduino_task():
    print('arduino_task add temp')
    try:
        dic_param = read_ser()
    except Exception as err:
        print(err)
        log = Logs.objects.create(date_log = datetime.now(),
                                  title_log = 'temp Arduino',
                                  description_log = 'Ошибка ардуино Exeption')
        return err

    if dic_param['status'][0] == 'Test-OK':
        Logs.objects.create(date_log = datetime.now(),
                            title_log = 'Status',
                            description_log = f'{dic_param["status"]}')
        if dic_param.get('Humidity_out'):
            temp_out = Temp_out.objects.create(date_temp = datetime.now(),
                                    temp = dic_param['Temperature_out'],
                                    humidity = dic_param['Humidity_out'])
        if dic_param.get('Humidity_in'):
            temp_in = Temp1.objects.create(date_temp = datetime.now(),
                                           temp = dic_param['Temperature_in'],
                                           humidity = dic_param['Humidity_in'])
        Logs.objects.create(date_log = datetime.now(),
                            title_log = 'TEMP',
                            description_log = f'{temp_in}, {temp_out}')
    if (dic_param['status'][0] != 'Test-OK') or (len(dic_param['status']) > 1):
        log = Logs.objects.create(date_log = datetime.now(),
                          title_log = 'temp Arduino',
                          description_log = str(dic_param['status']))
    print('arduino_task Close')


@cellery_app.task()
def Boiler_task():
    print('Start boiler')
    try:
        context = boiler_on()
    except Exception as err:
        Logs.objects.create(date_log = datetime.now(),
                                  title_log = 'Бойлер',
                                  description_log = 'Не включен Exeption' + err)
        return

    Logs.objects.create(date_log = datetime.now(),
                              title_log = 'Бойлер',
                              description_log = str(context['status']))
    context = boiler_off().apply_async(countdown=60*5)
    Logs.objects.create(date_log = datetime.now(),
                              title_log = 'Бойлер',
                              description_log = str(context['status']))
    print('Start boiler Close')
from __future__ import absolute_import, unicode_literals

from .main_arduino import restart_cam, read_ser, boiler_on, boiler_off
from .weather_rain import weather_6_day, rain_yesterday
from .models import  Logs, Weather, DHT_MQ
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
        log = Logs.objects.create(
            date_log = datetime.now(),
            title_log = 'WeatherAPI',
            description_log = 'Ошибка openweathermap.org Exeption изменилось API'+str(err))
        return None
    Logs.objects.create(date_log=datetime.now(),
                        title_log='Weather six_day',
                        description_log=six_day,
                        )
    Logs.objects.create(date_log=datetime.now(),
                        title_log='Weather yesterday',
                        description_log=yesterday,
                        )
    if six_day['status_code'] != 200 or yesterday['status_code'] != 200:
        Logs.objects.create(date_log=datetime.now(),
                            title_log='Weather',
                            description_log=f'Код ответа прогноза - {six_day["status_code"]}, '
                                            f'код ответа запроса "вчера" - {yesterday["status_code"]}')
    try:

        r_tomorrow = Weather.objects.create(date=six_day['tomorrow_date'],
                                            rain=six_day['summ_rain_3_day'],
                                            temp_min=six_day['min_temp'],
                                            temp_max=six_day['max_temp'],
                                            snow=six_day['summ_snow_3_day'],
                                            )
    except django.db.utils.IntegrityError:
        r_tomorrow = Weather.objects.get(date=six_day['tomorrow_date'])
        Logs.objects.create(date_log=datetime.now(),
                            title_log='Weather',
                            description_log='Ошибка записи в БД, ' + str(r_tomorrow))
    try:
        r_yesterday = Weather.objects.get(date = yesterday['result_date'])
    except ObjectDoesNotExist:
        r_yesterday = Weather.objects.create(date=yesterday['result_date'])
    r_yesterday.rain = yesterday['sum_rain']
    r_yesterday.snow = yesterday['sum_snow']
    r_yesterday.temp_min = yesterday['min_temp']
    r_yesterday.temp_max = yesterday['max_temp']
    r_yesterday.save()

    Logs.objects.create(date_log=datetime.now(),
                    title_log='Weather',
                    description_log=f'{r_tomorrow.date} -завтра, {r_yesterday.date} - вчеоа')
    print('weather_task end')


@cellery_app.task()
def arduino_task():
    print('arduino_task add temp')
    try:
        dic_param = read_ser()
    except Exception as err:
        print(err)
        log = Logs.objects.create(date_log=datetime.now(),
                                  title_log='temp Arduino',
                                  description_log='Ошибка ардуино Exeption')
        return

    if dic_param['status'][-1] == 'Test-OK':
        temp = DHT_MQ.objects.create(date_t_h=datetime.now())

        if dic_param.get('temp_voda'):
            temp.temp_voda = dic_param['temp_voda']
            temp.humidity_voda = dic_param['humidity_voda']
        if dic_param.get('temp_gaz'):
            temp.temp_gaz = dic_param['temp_gaz']
            temp.humidity_gaz = dic_param['humidity_gaz']
        if dic_param.get('temp_street'):
            temp.temp_street = dic_param['temp_street']
            temp.humidity_street = dic_param['humidity_street']
        if dic_param.get('gaz_MQ4'):
            temp.gaz_MQ4 = dic_param['gaz_MQ4']
        if dic_param.get('gaz_MQ135'):
            temp.gaz_MQ4 = dic_param['gaz_MQ135']

    else:
        log = Logs.objects.create(date_log=datetime.now(),
                          title_log='DHT_MQ Arduino',
                          description_log=str(dic_param['status'])+'Error')
    print('arduino_task Close')


@cellery_app.task()
def boiler_task_on():
    print('Start boiler on')
    try:
        context = boiler_on()
    except Exception as err:
        Logs.objects.create(date_log=datetime.now(),
                            title_log='Бойлер',
                            description_log='Не включен Exeption' + str(err))
        return

    Logs.objects.create(date_log=datetime.now(),
                        title_log='Бойлер',
                        description_log=str(context['status']))

    print('Start boiler Close on')


@cellery_app.task()
def boiler_task_off():
    print('Start boiler off')
    try:
        context = boiler_off()
    except Exception as err:
        Logs.objects.create(date_log=datetime.now(),
                            title_log='Бойлер',
                            description_log='Не выключен Exeption' + str(err))
        return

    Logs.objects.create(date_log=datetime.now(),
                        title_log='Бойлер',
                        description_log=str(context['status']))

    print('Start boiler Close off')

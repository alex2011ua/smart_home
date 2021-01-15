from __future__ import absolute_import, unicode_literals

from .main_arduino import read_ser, rele_light_balkon, rele_light_tree, rele_light_perim
from .weather_rain import weather_6_day, rain_yesterday
from .raspberry import restart_cam, boiler_on, boiler_off
from .models import Logs, Weather, DHT_MQ, Setting
from ..celery import cellery_app
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datetime import datetime
import django.db
from .Telegram import gaz_analiz, button_analiz, temp_alert, bot

from django.conf import settings

DEBUG = settings.PLACE


@cellery_app.task()
def restart_cam_task():
    print('Start restart_cam_task')

    try:
        restart_cam(DEBUG)
    except Exception as err:
        print(err)
        Logs.objects.create(date_log = datetime.now(),
                            status = 'Error',
                            title_log = 'Task restart_cam_task',
                            description_log = 'Не перезагружены' + str(err))
        return

    Logs.objects.create(date_log = datetime.now(),
                        status = 'OK',
                        title_log = 'Task restart_cam_task',
                        description_log = 'Restart Cam')
    Logs.objects.create(date_log = datetime.now(),
                        status = 'OK',
                        title_log = 'Task restart_cam_task',
                        description_log = 'Перезагружены')
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
            status = 'Error',
            title_log = 'Task weather_task',
            description_log = 'Ошибка openweathermap.org Exeption изменилось API' + str(
                err))
        return None
    if six_day['status_code'] != 200 or yesterday['status_code'] != 200:
        Logs.objects.create(date_log = datetime.now(),
                            status = 'Error',
                            title_log = 'Task weather_task',
                            description_log = f'Код ответа прогноза - {six_day["status_code"]}, '
                                              f'код ответа запроса "вчера" - {yesterday["status_code"]}')
    try:

        Weather.objects.create(date = six_day['tomorrow_date'],
                               rain = six_day['summ_rain_3_day'],
                               temp_min = six_day['min_temp'],
                               temp_max = six_day['max_temp'],
                               snow = six_day['summ_snow_3_day'],
                               )
    except django.db.utils.IntegrityError:
        r_tomorrow = Weather.objects.get(date = six_day['tomorrow_date'])
        Logs.objects.create(date_log = datetime.now(),
                            status = 'Error',
                            title_log = 'Task weather_task',
                            description_log = 'Ошибка записи в БД, ' + str(r_tomorrow))
    try:
        r_yesterday = Weather.objects.get(date = yesterday['result_date'])
    except ObjectDoesNotExist:
        r_yesterday = Weather.objects.create(date = yesterday['result_date'])
    r_yesterday.rain = yesterday['sum_rain']
    r_yesterday.snow = yesterday['sum_snow']
    r_yesterday.temp_min = yesterday['min_temp']
    r_yesterday.temp_max = yesterday['max_temp']
    r_yesterday.save()

    print('weather_task end')


@cellery_app.task()
def arduino_task():
    print('arduino_task add temp')
    try:
        dic_param = read_ser()  # Читает с Ардуино значения датчиков
    except Exception as err:
        print(err)
        Logs.objects.create(date_log = datetime.now(),
                            status = 'Error',
                            title_log = 'Task arduino',
                            description_log = 'Ошибка ардуино Exeption')
        return

    if dic_param['status'][-1] == 'Test-OK':
        temp = DHT_MQ.objects.create(date_t_h = datetime.now())

        if dic_param.get('temp_voda'):
            temp.temp_voda = dic_param['temp_voda']
            temp.humidity_voda = dic_param['humidity_voda']
        if dic_param.get('temp_gaz'):
            temp.temp_gaz = dic_param['temp_gaz']
            temp.humidity_gaz = dic_param['humidity_gaz']
        if dic_param.get('temp_street'):
            temp.temp_street = dic_param['temp_street']
            temp.humidity_street = dic_param['humidity_street']
        if dic_param.get('MQ4_value'):
            temp.gaz_MQ4 = dic_param['MQ4_value']
        if dic_param.get('MQ135_value'):
            temp.gaz_MQ135 = dic_param['MQ135_value']
        if dic_param.get('muve_kitchen'):
            temp.muve_kitchen = dic_param['muve_kitchen']

        temp.save()
    else:
        Logs.objects.create(date_log = datetime.now(),
                            status = 'Error',
                            title_log = 'Task arduino_task',
                            description_log = str(dic_param['status']) + 'Error')
    print('arduino_task Close')


@cellery_app.task()
def boiler_task_on():
    print('Start boiler on')
    try:
        boiler_on(DEBUG)
    except Exception as err:
        Logs.objects.create(date_log = datetime.now(),
                            status = 'Error',
                            title_log = 'Task boiler_task_on',
                            description_log = 'Не включен Exeption' + str(err))
        return
    Logs.objects.create(date_log = datetime.now(),
                        status = 'OK',
                        title_log = 'Task boiler_task',
                        description_log = 'Бйлер включен')
    print('Start boiler Close on')


@cellery_app.task()
def boiler_task_off():
    print('Start boiler off')
    try:
        boiler_off(DEBUG)
        boiler = Setting.objects.get(controller_name = 'boiler')
        boiler.label = 'Бойлер выключен'
        boiler.value = 0
        boiler.save()

    except Exception as err:
        Logs.objects.create(date_log = datetime.now(),
                            status = 'Error',
                            title_log = 'Task boiler_task_off',
                            description_log = 'Не выключен Exeption' + str(err))
        return
    Logs.objects.create(date_log = datetime.now(),
                        status = 'OK',
                        title_log = 'Task boiler_task',
                        description_log = 'Бйлер выключен')
    print('Start boiler Close off')


@cellery_app.task()
def bot_task():
    print('Start bot task')
    temp = DHT_MQ.objects.all().order_by('-date_t_h')[0]
    if (temp.gaz_MQ4 > 65) or (temp.gaz_MQ135 > 100):
        gaz_analiz(temp.gaz_MQ4, temp.gaz_MQ135)

    button_analiz()

    print('Start bot task off')


@cellery_app.task()
def bot_task_1_hour():
    print('Start bot_task_1_hour')
    temp_alert()
    print('Stop bot_task_1_hour')


@cellery_app.task()
def bot_task_11_hour():
    print('Start bot_task_11_hour')

    light_balkon = Setting.objects.get(controller_name = 'light_balkon')
    if light_balkon.value == 1:
        rele_light_balkon(0)
        light_balkon.value = 0
        light_balkon.save()
        bot.send_message('Выключен свет на балконе по рассписанию!')

    light_tree = Setting.objects.get(controller_name = 'light_tree')
    if light_tree.value == 1:
        rele_light_tree(0)
        light_tree.value = 0
        light_tree.save()
        bot.send_message('Выключена иллюминация елки по рассписанию!')

    light_perim = Setting.objects.get(controller_name = 'light_perim')
    if light_perim.value == 1:
        rele_light_perim(0)
        light_perim.value = 0
        light_perim.save()
        bot.send_message('Выключена тестовая кнопка рассписанию!')

    print('Stop bot_task_11_hour')

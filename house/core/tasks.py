from __future__ import absolute_import, unicode_literals

from .main_arduino import read_ser, boiler_on, boiler_off
from .weather_rain import weather_6_day, rain_yesterday
from .raspberry import restart_cam
from .models import Logs, Weather, DHT_MQ, Message
from ..celery import cellery_app
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datetime import datetime
import django.db

from django.conf import settings
DEBUG = settings.PLACE


@cellery_app.task()
def restart_cam_task():
    print('Start restart_cam_task')

    try:
        restart_cam(DEBUG)
    except Exception as err:
        print(err)
        log = Logs.objects.create(date_log = datetime.now(),
                                  status = 'Error',
                                  title_log = 'Task restart_cam_task',
                                  description_log = 'Не перезагружены' + str(err))
        return

    Logs.objects.create(date_log = datetime.now(),
                              status = 'OK',
                              title_log = 'Task restart_cam_task',
                              description_log = 'Restart Cam')

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
            description_log = 'Ошибка openweathermap.org Exeption изменилось API'+str(err))
        return None
    if six_day['status_code'] != 200 or yesterday['status_code'] != 200:
        Logs.objects.create(date_log=datetime.now(),
                            status = 'Error',
                            title_log='Task weather_task',
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
                            status='Error',
                            title_log='Task weather_task',
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

    print('weather_task end')


@cellery_app.task()
def arduino_task():
    print('arduino_task add temp')
    try:
        dic_param = read_ser()  # Читает с Ардуино значения датчиков
    except Exception as err:
        print(err)
        log = Logs.objects.create(date_log=datetime.now(),
                                  status = 'Error',
                                  title_log='Task arduino',
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
        if dic_param.get('MQ4_value'):
            temp.gaz_MQ4 = dic_param['MQ4_value']
        if dic_param.get('MQ135_value'):
            temp.gaz_MQ135 = dic_param['MQ135_value']

        temp.save()
    else:
        log = Logs.objects.create(date_log=datetime.now(),
                                  status = 'OK',
                                  title_log='Task arduino_task',
                                  description_log=str(dic_param['status'])+'Error')
    print('arduino_task Close')


@cellery_app.task()
def boiler_task_on():
    print('Start boiler on')
    try:
        context = boiler_on()
    except Exception as err:
        Logs.objects.create(date_log=datetime.now(),
                            status = 'Error',
                            title_log='Task boiler_task_on',
                            description_log='Не включен Exeption' + str(err))
        return

    Logs.objects.create(date_log=datetime.now(),
                        status = 'OK',
                        title_log='Task boiler_task_on',
                        description_log=str(context['status']))

    print('Start boiler Close on')


@cellery_app.task()
def boiler_task_off():
    print('Start boiler off')
    try:
        context = boiler_off()
    except Exception as err:
        Logs.objects.create(date_log=datetime.now(),
                            status = 'Error',
                            title_log='Task boiler_task_off',
                            description_log='Не выключен Exeption' + str(err))
        return

    Logs.objects.create(date_log=datetime.now(),
                        status = 'OK',
                        title_log='Task boiler_task_off',
                        description_log=str(context['status']))

    print('Start boiler Close off')


@cellery_app.task()
def bot_task():
    from .raspberry import button
    from .Telegram import bot
    print('Start bot task')
    date_now = datetime.now()
    temp = DHT_MQ.objects.all().order_by('-date_t_h')[0]
    if (temp.gaz_MQ4 > 100) or (temp.gaz_MQ135 > 100):
        try:
            gaz = Message.objects.get(controller_name = 'gaz')
        except Exception:
            gaz = Message.objects.create(controller_name = 'gaz',
                                   date_message=datetime(2000, 1, 1))

        time_delta = (date_now - gaz.date_message) // 60 #  minutes
        if time_delta.seconds > 60:
            bot.send_message('Завышены показания газовый датчиков')
            bot.send_message(f'MQ-4 - {temp.gaz_MQ4}, MQ-135 - {temp.gaz_MQ135}')
            gaz.date_message = date_now
            gaz.controller_name = 'gaz'
            gaz.label = "Allarm"
            gaz.value_int = temp.gaz_MQ4 + temp.gaz_MQ135
            gaz.save()

    context = button(DEBUG)  # загрузка состояний кнопок
    try:
        dor = Message.objects.get(controller_name = 'dor')
        garaz = Message.objects.get(controller_name = 'garaz')
    except Exception:
        dor = Message.objects.create(controller_name = 'dor',
                                     date_message = datetime(2000, 1, 1),
                                     value_int = 0)
        garaz = Message.objects.create(controller_name = 'garaz',
                                       date_message = datetime(2000, 1, 1),
                                       value_int = 0)
    if context['Garaz'] != garaz.state:
        garaz.state = context['Garaz']
        garaz.date_message = date_now
        if context['Garaz']:
            garaz.label = 'Открыт гараж'
        else:
            garaz.label = 'Закрыт гараж'
        bot.send_message(garaz.label)

    if context['Dor_street'] != dor.state:
        dor.state = context['Dor_street']
        dor.date_message = date_now
        if context['Dor_street']:
            dor.label = 'Открыта дверь'
        else:
            dor.label = 'Закрыта дверь'
        bot.send_message(dor.label)

    if date_now.hour < 5:
        if context['Garaz'] and garaz.value_int == 0:
            bot.send_message('Открыт гараж')
            garaz.value_int = 1
        if context['Dor_street'] and dor.value_int == 0:
            bot.send_message('Открыта дверь')
            dor.value_int = 1
    if date_now.hour >= 5:
        garaz.value_int = 0
        dor.value_int = 0
    garaz.save()
    dor.save()
    print('Start bot task off')


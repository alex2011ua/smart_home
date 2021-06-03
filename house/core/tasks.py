from __future__ import absolute_import, unicode_literals
from django.db.utils import IntegrityError
from .main_arduino import get_arduino_answer, rele_light_balkon, rele_light_tree, \
    rele_light_perim, arduino_restart_5v, arduino_poliv
from .weather_rain import weather_6_day, rain_yesterday
from .raspberry import restart_cam, boiler_on, boiler_off, button
from .models import Logs, Weather, DHT_MQ, Setting, Params
from ..celery import cellery_app
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from datetime import datetime
import django.db
from .Telegram import bot
from myviberbot.viber_bot import send_viber
from .analiz import button_analiz, gaz_analiz, temp_alert
import logging
from django.conf import settings


logger = logging.getLogger('django')
DEBUG = settings.PLACE

@cellery_app.task()
def restart_cam_task():
    print('Start restart_cam_task')

    try:
        restart_cam(DEBUG)
    except Exception as err:
        print(err)
        Logs.objects.create(date_log=datetime.now(),
                            status='Error',
                            title_log='Task restart_cam_task',
                            description_log='Не перезагружены' + str(err))
        return

    Logs.objects.create(date_log=datetime.now(),
                        status='OK',
                        title_log='Task restart_cam_task',
                        description_log='Restart Cam')
    print('restart_cam_task Close')


@cellery_app.task()
def weather_task():
    print('weather_task start')
    try:
        six_day = weather_6_day()
        yesterday = rain_yesterday()
    except Exception as err:
        log = Logs.objects.create(
            date_log=datetime.now(),
            status='Error',
            title_log='Task weather_task',
            description_log='Ошибка openweathermap.org Exeption изменилось API' + str(err))
        return None
    if six_day['status_code'] != 200 or yesterday['status_code'] != 200:
        Logs.objects.create(date_log=datetime.now(),
                            status='Error',
                            title_log='Task weather_task',
                            description_log=f'Код ответа прогноза - {six_day["status_code"]}, '
                                            f'код ответа запроса "вчера" - {yesterday["status_code"]}')
    try:

        Weather.objects.create(date=six_day['tomorrow_date'],
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
                            description_log='Ошибка записи в БД, ' + str(
                                r_tomorrow))
    try:
        r_yesterday = Weather.objects.get(date=yesterday['result_date'])
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
        dic_param = get_arduino_answer()  # Читает с Ардуино значения датчиков
    except Exception as err:
        Logs.objects.create(date_log=datetime.now(),
                            status='Error',
                            title_log='Task arduino',
                            description_log='Ошибка ардуино Exeption' + str(err))
        return
    if dic_param.get('control_error'):
        arduino_restart_5v()
        a = Setting.objects.get(controller_name="Error_dht")
        a.date = datetime.now()
        a.label = dic_param.get('control_error')
        a.value = 1
        a.save()
        dic_param = get_arduino_answer()
    else:
        a = Setting.objects.get(controller_name="Error_dht")
        a.value = 0
        a.save()
    if dic_param['status'][-1] == 'Test-OK':

        temp = DHT_MQ.objects.create(date_t_h=datetime.now())
        if dic_param.get('temp_teplica'):
            temp.temp_teplica = dic_param['temp_teplica']
            temp.humidity_teplica = dic_param['hum_teplica']
        if dic_param.get('temp_voda'):
            temp.temp_voda = dic_param['temp_voda']
            temp.humidity_voda = dic_param['hum_voda']
        if dic_param.get('temp_gaz'):
            temp.temp_gaz = dic_param['temp_gaz']
            temp.humidity_gaz = dic_param['hum_gaz']
        if dic_param.get('temp_street'):
            temp.temp_street = dic_param['temp_street']
            temp.humidity_street = dic_param['hum_street']
        if dic_param.get('MQ4'):
            temp.gaz_MQ4 = dic_param['MQ4']
        if dic_param.get('MQ135'):
            temp.gaz_MQ135 = dic_param['MQ135']
        if dic_param.get('muve_k'):
            temp.muve_kitchen = dic_param['muve_k']
        if dic_param.get('myData'):
            temp.myData = dic_param['myData'],
        if dic_param.get('ackData'):
            temp.ackData = dic_param['ackData']
            room1 = Setting.objects.get(controller_name='room1')
            list_ackData = dic_param['ackData'].split(' ')
            list_myData = dic_param['myData'].split(' ')
            label = ''
            if dic_param['myData'] == '1 1 1 1 1 1':
                room1.label = 'не подключен'
                room1.value = 0
            else:
                if dic_param['ackData'] == '1 1 1 1 1 1':
                    label += 'Нет данных.'
                    room1.value = 0
                else:
                    label += list_ackData[1]+'° '
                    room1.value = 1
                if list_myData[0] == '55' and list_myData[4] == '0':
                    label += 'Не отправлено'
                    room1.value = 0
                room1.label = label
            room1.date = datetime.now()
            room1.save()
        temp.save()

    else:
        Logs.objects.create(date_log=datetime.now(),
                            status='Error',
                            title_log='Task arduino_task',
                            description_log=str(dic_param['status']) + 'Error')
    print('arduino_task Close')


@cellery_app.task()
def boiler_task_on():
    print('Start boiler on')
    try:
        boiler_on(DEBUG)
    except Exception as err:
        Logs.objects.create(date_log=datetime.now(),
                            status='Error',
                            title_log='Task boiler_task_on',
                            description_log='Не включен Exeption' + str(err))
        return
    Logs.objects.create(date_log=datetime.now(),
                        status='OK',
                        title_log='Task boiler_task',
                        description_log='Бйлер включен')
    print('Start boiler Close on')


@cellery_app.task()
def boiler_task_off():
    print('Start boiler off')
    try:
        boiler_off(DEBUG)
        boiler = Setting.objects.get(controller_name='boiler')
        boiler.label = 'Бойлер выключен'
        boiler.value = 0
        boiler.save()
        bot.send_message('ВЫключен бойлер')

    except Exception as err:
        Logs.objects.create(date_log=datetime.now(),
                            status='Error',
                            title_log='Task boiler_task_off',
                            description_log='Не выключен Exeption' + str(err))
        return
    Logs.objects.create(date_log=datetime.now(),
                        status='OK',
                        title_log='Task boiler_task',
                        description_log='Бйлер выключен')
    print('Start boiler Close off')


@cellery_app.task()
def bot_task():
    """запускается каждые 2 минуты"""
    print('Start bot task')
    alarms = Setting.objects.get(controller_name="alarms")
    if alarms.value == 0:
        print('Stop bot task off(alarm off)')
        return
    temp = DHT_MQ.objects.all().order_by('-date_t_h')[0]
    MQ4 = temp.gaz_MQ4 or 0
    MQ135 = temp.gaz_MQ135 or 0
    if (MQ4 > 65) or (MQ135 > 100):
        gaz_analiz(MQ4, MQ135)

    button_analiz(DEBUG)

    print('Stop bot task off')


@cellery_app.task()
def bot_task_1_hour():
    print('Start bot_task_1_hour')
    alarms = Setting.objects.get(controller_name="alarms")
    if alarms.value == 0:
        print('Stop bot_task_1_hour(alarm off)')
        return
    temp_alert()
    print('Stop bot_task_1_hour')


@cellery_app.task()
def bot_task_11_hour():
    print('Start bot_task_11_hour')

    light_balkon = Setting.objects.get(controller_name='light_balkon')

    if light_balkon.value == 1:
        rele_light_balkon(0)
        light_balkon.value = 0
        light_balkon.save()
        bot.send_message('Выключен резервная кнопка!')

    light_tree = Setting.objects.get(controller_name='light_tree')
    if light_tree.value == 1:
        rele_light_tree(0)
        light_tree.value = 0
        light_tree.save()
        bot.send_message('Выключена иллюминация елки по рассписанию!')

    light_perim = Setting.objects.get(controller_name='light_perim')
    open_controll = button(DEBUG)  # {'Garaz': True, 'Dor_street': False}
    if open_controll['Garaz'] is True or open_controll['Dor_street'] is True:
        rele_light_perim(1)
        light_perim.value = 1
        light_perim.save()
        bot.send_message('Не закрыты дверь или гараж!')
        send_viber('Не закрыты дверь или гараж!')

    else:
        if light_perim.value == 1:
            rele_light_perim(0)
            light_perim.value = 0
            light_perim.save()
            bot.send_message('Выключена иллюминация!')
            send_viber('Выключена иллюминация!')
    print('Stop bot_task_11_hour')


@cellery_app.task()
def bot_task_watering_analiz():
    """Анализ необходимости включения полива"""
    weather = Weather.objects.filter().order_by('-date')[0:14]
    poliv = Setting.objects.get(controller_name="poliv")
    sum_rain = 0
    corect = -1
    water_time = 10
    limit_rain = 10 # mm
    for day in weather:
        if day.temp_max > 25:
            water_time += 1
        if day.temp_max > 30:
            water_time += 1
        if day.temp_max > 32:
            water_time += 1
        if (day.rain - corect) >= 0:
            sum_rain += day.rain - corect
        corect += 1

    if sum_rain >= limit_rain:
        bot.send_message(f'ВЫключен полив. Количество осадков: {sum_rain}.Время возможного полива {water_time}, порог включения {limit_rain}мм.')
        poliv.value = water_time
        poliv.label = 'выключен'
    if sum_rain < limit_rain:
        bot.send_message(f'Полив включен. Количество осадков: {sum_rain}. Время полива {water_time}, порог включения {limit_rain}мм.')
        poliv.value = water_time
        poliv.label = 'включен'
    poliv.save()


@cellery_app.task()
def poliv(force=None):
    """включениe полива"""

    poliv = Setting.objects.get(controller_name="poliv")
    if poliv.label == 'включен' or force:
        arduino_poliv(poliv.value)
        Params.objects.create(
            date_t_h=datetime.now(),
            poliv=poliv.value)
        bot.send_message(f'Старт полива: {poliv.label}, {poliv.value} min.')
        Params.objects.create(poliv=poliv.value, date_t_h=datetime.now())





from __future__ import absolute_import, unicode_literals

import logging
from datetime import datetime

import django.db
import speedtest
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.utils import IntegrityError

from myviberbot.viber_bot import send_viber

from .analiz import button_analiz, gaz_analiz, temp_alert
from .avto_leaf import check, get_avto
from .is_dayoff import DayOff
from .main_arduino import (
    arduino_poliv,
    arduino_restart_5v,
    get_arduino_answer,
    rele_light_balkon,
    bassein
)
from .matplot import refresh, calend
from .models import DHT_MQ, Avto, Logs, Params, Setting, Weather
from .raspberry import boiler_off, boiler_on, button, restart_cam
from .Telegram import bot
from .weather_rain import rain_yesterday, weather_6_day
from ..celery import cellery_app

logger = logging.getLogger("django")
DEBUG = settings.PLACE
day_off = DayOff()


@cellery_app.task()
def restart_cam_task():
    print("Start restart_cam_task")

    try:
        restart_cam(DEBUG)
    except Exception as err:
        print(err)
        Logs.objects.create(
            date_log=datetime.now(),
            status="Error",
            title_log="Task restart_cam_task",
            description_log="Не перезагружены" + str(err),
        )
        return

    Logs.objects.create(
        date_log=datetime.now(),
        status="OK",
        title_log="Task restart_cam_task",
        description_log="Restart Cam",
    )
    print("restart_cam_task Close")


@cellery_app.task()
def weather_task():
    print("weather_task start")
    try:
        six_day = weather_6_day()
        yesterday = rain_yesterday()
    except Exception as err:
        Logs.objects.create(
            date_log=datetime.now(),
            status="Error",
            title_log="Task weather_task",
            description_log="Ошибка openweathermap.org Exeption изменилось API" + str(err),
        )
        return None
    if six_day["status_code"] != 200 or yesterday["status_code"] != 200:
        Logs.objects.create(
            date_log=datetime.now(),
            status="Error",
            title_log="Task weather_task",
            description_log=f'Код ответа прогноза - {six_day["status_code"]}, '
                            f'код ответа запроса "вчера" - {yesterday["status_code"]}',
        )
    r_yesterday, _ = Weather.objects.get_or_create(date=yesterday["result_date"])
    r_yesterday.rain = yesterday["sum_rain"]
    r_yesterday.snow = yesterday["sum_snow"]
    r_yesterday.temp_min = yesterday["min_temp"]
    r_yesterday.temp_max = yesterday["max_temp"]
    r_yesterday.save()
    tomorrow, _ = Weather.objects.get_or_create(date=six_day["tomorrow_date"])
    tomorrow.rain = six_day["summ_rain_3_day"]
    tomorrow.temp_min = six_day["min_temp"]
    tomorrow.temp_max = six_day["max_temp"]
    tomorrow.snow = six_day["summ_snow_3_day"]
    tomorrow.save()
    calend()
    print("weather_task end")


@cellery_app.task()
def arduino_task():
    print("arduino_task add temp")
    try:
        dic_param = get_arduino_answer()  # Читает с Ардуино значения датчиков
    except Exception as err:
        Logs.objects.create(
            date_log=datetime.now(),
            status="Error",
            title_log="Task arduino",
            description_log="Ошибка ардуино Exeption" + str(err),
        )
        return
    if dic_param.get("control_error"):
        arduino_restart_5v()
        a = Setting.objects.get(controller_name="Error_dht")
        a.date = datetime.now()
        a.label = dic_param.get("control_error")
        a.value = 1
        a.save()
        dic_param = get_arduino_answer()
    else:
        a = Setting.objects.get(controller_name="Error_dht")
        a.value = 0
        a.save()
    if dic_param["status"][-1] == "Test-OK":

        temp = DHT_MQ.objects.create(date_t_h=datetime.now())
        if dic_param.get("temp_teplica"):
            temp.temp_teplica = dic_param["temp_teplica"]
            temp.humidity_teplica = dic_param["hum_teplica"]
            max_temp_teplica = Setting.objects.get(controller_name="max_temp_teplica")
            min_temp_teplica = Setting.objects.get(controller_name="min_temp_teplica")
            if temp.temp_teplica > max_temp_teplica.value:
                max_temp_teplica.value = round(temp.temp_teplica)
                max_temp_teplica.save()
            if temp.temp_teplica < min_temp_teplica.value:
                min_temp_teplica.value = round(temp.temp_teplica)
                min_temp_teplica.save()

        if dic_param.get("temp_voda"):
            temp.temp_voda = dic_param["temp_voda"]
            temp.humidity_voda = dic_param["hum_voda"]
        if dic_param.get("temp_gaz"):
            temp.temp_gaz = dic_param["temp_gaz"]
            temp.humidity_gaz = dic_param["hum_gaz"]
        if dic_param.get("temp_street"):
            temp.temp_street = dic_param["temp_street"]
            temp.humidity_street = dic_param["hum_street"]
        if dic_param.get("MQ4"):
            temp.gaz_MQ4 = dic_param["MQ4"]
        if dic_param.get("MQ135"):
            temp.gaz_MQ135 = dic_param["MQ135"]
        if dic_param.get("muve_k"):
            temp.muve_kitchen = dic_param["muve_k"]
        if dic_param.get("myData"):
            temp.myData = (dic_param["myData"],)
        if dic_param.get("ackData"):
            temp.ackData = dic_param["ackData"]
            room1 = Setting.objects.get(controller_name="room1")
            list_ackData = dic_param["ackData"].split(" ")
            list_myData = dic_param["myData"].split(" ")
            label = ""
            if dic_param["myData"] == "1 1 1 1 1 1":
                room1.label = "не подключен"
                room1.value = 0
            else:
                if dic_param["ackData"] == "1 1 1 1 1 1":
                    label += "Нет данных."
                    room1.value = 0
                else:
                    label += list_ackData[1] + "° "
                    room1.value = 1
                if list_myData[0] == "55" and list_myData[4] == "0":
                    label += "Не отправлено"
                    room1.value = 0
                room1.label = label
            room1.date = datetime.now()
            room1.save()
        temp.save()

    else:
        Logs.objects.create(
            date_log=datetime.now(),
            status="Error",
            title_log="Task arduino_task",
            description_log=str(dic_param["status"]) + "Error",
        )
    print("arduino_task Close")


@cellery_app.task()
def boiler_task_on():
    print("Start boiler on")
    try:
        boiler_on(DEBUG)
    except Exception as err:
        Logs.objects.create(
            date_log=datetime.now(),
            status="Error",
            title_log="Task boiler_task_on",
            description_log="Не включен Exeption" + str(err),
        )
        return
    Logs.objects.create(
        date_log=datetime.now(),
        status="OK",
        title_log="Task boiler_task",
        description_log="Бйлер включен",
    )
    print("Start boiler Close on")


@cellery_app.task()
def boiler_task_off():
    print("Start boiler off")
    try:
        boiler_off(DEBUG)
        boiler = Setting.objects.get(controller_name="boiler")
        boiler.label = "Бойлер выключен"
        boiler.value = 0
        boiler.save()
        bot.send_message("ВЫключен бойлер")

    except Exception as err:
        Logs.objects.create(
            date_log=datetime.now(),
            status="Error",
            title_log="Task boiler_task_off",
            description_log="Не выключен Exeption" + str(err),
        )
        return
    Logs.objects.create(
        date_log=datetime.now(),
        status="OK",
        title_log="Task boiler_task",
        description_log="Бйлер выключен",
    )
    print("Start boiler Close off")


@cellery_app.task()
def bot_task():
    """запускается каждые 2 минуты"""
    alarms = Setting.objects.get(controller_name="alarms")
    if alarms.value == 0:
        print("Stop bot task off(alarm off)")
        return
    temp = DHT_MQ.objects.all().order_by("-date_t_h")[0]
    MQ4 = temp.gaz_MQ4 or 0
    MQ135 = temp.gaz_MQ135 or 0
    if (MQ4 > 135) or (MQ135 > 75):
        gaz_analiz(MQ4, MQ135)
    button_analiz(DEBUG)


@cellery_app.task()
def bot_task_1_hour():
    """
    каждый час проверяет температуру теплицы и качество интернета и строит график температуры
    :return:
    """
    print("Start bot_task_1_hour")
    refresh()
    alarms = Setting.objects.get(controller_name="alarms")
    temp_alert(alarms.value)

    st = speedtest.Speedtest()
    download = float(st.download()) // 1024 // 1024 // 8
    upload = float(st.upload()) // 1024 // 1024 // 8
    ping = st.results.ping
    if download < 5 or upload < 5 or ping > 100:
        download = float(st.download()) // 1024 // 1024 // 8
        upload = float(st.upload()) // 1024 // 1024 // 8
        ping = st.results.ping
        if download < 7 or upload < 7 or ping > 130:
            bot.send_message(f"download:{download}, upload: {upload}, ping: {ping}")
    Params.objects.create(ping=ping, download=download, upload=upload, date_t_h=datetime.now())

    print("Stop bot_task_1_hour")


@cellery_app.task()
def bot_task_11_hour():
    print("Start bot_task_11_hour")

    light_balkon = Setting.objects.get(controller_name="light_balkon")

    if light_balkon.value == 1:
        bot.send_message("Выключен ,балкон!")

    open_controll = button(DEBUG)  # {'Garaz': True, 'Dor_street': False}
    if open_controll["Garaz"] is True or open_controll["Dor_street"] is True:
        bot.send_message("Не закрыты дверь или гараж!")
        send_viber("Не закрыты дверь или гараж!")

    print("Stop bot_task_11_hour")


@cellery_app.task()
def bot_task_watering_analiz():
    """Анализ необходимости включения полива"""
    weather = Weather.objects.filter().order_by("-date")[0:8]
    poliv = Setting.objects.get(controller_name="poliv")
    limit_rain = Setting.objects.get(controller_name="limit_rain").value
    sum_rain = 0
    corect = -1
    water_time = Setting.objects.get(controller_name="start_water_time").value

    for day in weather:
        if day.temp_max > 27:
            water_time += 1
        if day.temp_max > 30:
            water_time += 1
        if day.temp_max > 33:
            water_time += 1
        if (day.rain - corect) >= 0:
            sum_rain += day.rain - corect
        corect += 1

    if sum_rain >= limit_rain:
        bot.send_message(
            f"ВЫключен полив. Количество осадков: {sum_rain}.Время возможного полива {water_time}, порог включения {limit_rain}мм."
        )
        poliv.value = water_time
        poliv.label = "выключен"
    if sum_rain < limit_rain:
        bot.send_message(
            f"Полив включен. Количество осадков: {sum_rain}. Время полива {water_time - sum_rain}, порог включения {limit_rain}мм."
        )
        poliv.value = water_time - sum_rain
        poliv.label = "включен"
    poliv.save()



@cellery_app.task()
def poliv(force=None):
    """включениe полива"""
    poliv = Setting.objects.get(controller_name="poliv")
    if poliv.label == "включен" or force:
        time_all_poliv = 2 * poliv.value * Setting.objects.get(controller_name="watering_raspberry").value + \
                         2 * poliv.value * Setting.objects.get(controller_name="watering_sad").value + \
                         poliv.value * Setting.objects.get(controller_name="watering_trava").value + \
                         poliv.value * Setting.objects.get(controller_name="watering_pesochnica").value
        Params.objects.create(poliv=time_all_poliv, date_t_h=datetime.now())
        arduino_poliv(poliv.value)

        bot.send_message(f"Полив завершен: {time_all_poliv} min." + "(принудительно)" if force else "")


#
# @cellery_app.task()
# def pshik(force=None):
#     """включениe режима пшик"""
#     pshik = Setting.objects.get(controller_name="pshik")
#     if poliv.label == "включен" or force:
#         Params.objects.create(poliv=pshik.value, date_t_h=datetime.now())
#         arduino_poliv(poliv.value)
#         bot.send_message(f"Полив завершен: {poliv.value} min." + "(принудительно)" if force else "")


@cellery_app.task()
def lights_on():
    """включениe иллюминации балкона"""
    flag = Setting.objects.get(controller_name="regular")
    if flag.value:
        rele = Setting.objects.get(controller_name="light_balkon")
        if rele.value == 0:
            rele_light_balkon(1)
            rele.value = 1
            rele.save()


@cellery_app.task()
def lights_off():
    """ВЫключениe иллюминации балкона"""
    flag = Setting.objects.get(controller_name="regular")
    if flag.value:
        rele = Setting.objects.get(controller_name="light_balkon")
        if rele.value == 1:
            rele_light_balkon(0)
            rele.value = 0
            rele.save()


@cellery_app.task()
def report_10_am():
    """check new car and make plot calendar"""

    list_all_cars = check()
    list_new_car = []
    for car in list_all_cars:
        try:
            Avto.objects.get(car_id=int(car))
        except ObjectDoesNotExist:
            Avto.objects.create(car_id=car)
            list_new_car.append(int(car))

    for new_car in list_new_car:
        link = "https://auto.ria.com/uk" + get_avto(new_car)["linkToView"]
        bot.send_message(link)
        avto = Avto.objects.get(car_id=new_car)
        avto.link_car = link
        avto.save()


@cellery_app.task()
def start_filtering():
    """start filtering pool"""
    flag = Setting.objects.get(controller_name="regular")
    if flag.value:
        logger.warning("Start filtering")
        rele = Setting.objects.get(controller_name="bassein")
        if rele.value == 0:
            rele.value = 1
            rele.save()
        bassein(1)


@cellery_app.task()
def stop_filtering():
    """stop filtering pool"""
    flag = Setting.objects.get(controller_name="regular")
    if flag.value:
        logger.warning("Stop filtering")
        rele = Setting.objects.get(controller_name="bassein")
        if rele.value == 1:
            rele.value = 0
            rele.save()
        bassein(0)

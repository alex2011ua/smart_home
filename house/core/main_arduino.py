import json
import logging
import time

from .Arduino import Arduino
from .DebagArduino import DebagArduino
from .models import Setting

logger = logging.getLogger("django")
from django.conf import settings

DEBUG = settings.PLACE
if DEBUG:  # если Дебаг то на компе нет Ардуино
    arduino = DebagArduino()  # используем эмулятор
else:
    try:
        arduino = Arduino()
    except Exception as err:
        print("Error Serial port")

"""

#define LIGHT_BALKON_ON     'A'
#define LIGHT_BALKON_OFF    'a'

#define LIGHT_TREE_ON   'B'
#define LIGHT_TREE_OFF  'b'

#define LIGHT_PERIM_ON   'C'
#define LIGHT_PERIM_OFF  'c'

#define SEND_PARAM  'p'
#define RESET       'r'
#define TEST        't'

#define SOUND_ON    'S'
#define SOUND_OFF   's'

"""


def testing():  # test answer Arduino
    for i in range(3):
        arduino.write(b"t")

        test = arduino.read()
        if test == "OK":  # Связь есть, получаем данные
            return {"status": ["Test-OK"]}
    return {"status": ["Test-Fail"]}


def parse_arduino_answer(read_arduino, context):
    try:
        errors, param = read_arduino.split("#")
        if errors:
            context["control_error"] = errors
        param = param.replace("'", '"')
    except Exception as err:
        context["status"].append('{}, parce Arduino answer:"{}"'.format(str(err), read_arduino))
        return context
    try:
        json_answer = json.loads(param)
    except json.JSONDecodeError as arr:
        context["status"].append("JSONDecodeError" + str(arr))
        return context
    context.update(json_answer)
    return context


def get_arduino_answer():
    context = testing()
    if context["status"][0] == "Test-Fail":
        return context
    return parse_arduino_answer(read_ser(), context)


def read_ser():
    arduino.write(b"p")
    read_arduino = arduino.read()
    return read_arduino


def reset():
    context = testing()
    arduino.write(b"r")
    arduino.restart()
    context["status"].append("Restart Arduino OK")
    return context


def sound():
    context = testing()
    arduino.write(b"S")
    time.sleep(0.5)
    arduino.write(b"s")
    time.sleep(0.5)
    arduino.write(b"S")
    time.sleep(0.5)
    arduino.write(b"s")
    context["status"].append("sound")
    return context


def rele_light_balkon(param):
    context = testing()
    if param == 1:
        arduino.write(b"A")
        rele = arduino.read()
    else:
        arduino.write(b"a")
        rele = arduino.read()
    context["status"].append(rele)
    return context


def bassein(param):
    context = testing()
    if param == 1:
        arduino.write(b"B")
        rele = arduino.read()
    else:
        arduino.write(b"b")
        rele = arduino.read()
    context["status"].append(rele)
    return context


def V24_arduino(param):
    context = testing()
    if param == 1:
        arduino.write(b"D")
    else:
        arduino.write(b"d")


def on_klapan(place):
    places = {
        "poliv_garaz": b"",
        "poliv_teplica": b"",
        "poliv_elki": b"E",
        "poliv_sad": b"F",
        "poliv_pesochnica": b"E",
        "poliv_strawberry": b"M",
        "poliv_trava": b"G",
    }
    arduino.write(places[place])


def off_klapan(place):
    places = {
        "poliv_garaz": b"",
        "poliv_teplica": b"",
        "poliv_elki": b"e",
        "poliv_sad": b"f",
        "poliv_pesochnica": b"e",
        "poliv_strawberry": b"m",
        "poliv_trava": b"g",
    }
    arduino.write(places[place])


def arduino_restart_5v():
    logger.warning("restart 5v")
    arduino.write(b"h")
    time.sleep(1)
    arduino.write(b"H")


def arduino_poliv(minutes):
    logger.warning("start poliv")
    V24 = Setting.objects.get(controller_name="V24")

    V24_arduino(1)
    V24.label = "включен"
    V24.save()
    watering_pesochnica = Setting.objects.get(controller_name="watering_pesochnica")
    watering_trava = Setting.objects.get(controller_name="watering_trava")
    watering_sad = Setting.objects.get(controller_name="watering_sad")
    watering_raspberry = Setting.objects.get(controller_name="watering_raspberry")

    if watering_pesochnica.value:
        logger.warning("start poliv watering_pesochnica")
        on_klapan("poliv_pesochnica")
        time.sleep(60 * minutes)
        off_klapan("poliv_pesochnica")
    if watering_trava.value:
        logger.warning("start poliv watering_trava")
        on_klapan("poliv_trava")
        time.sleep(60 * minutes)
        off_klapan("poliv_trava")
    if watering_raspberry.value:
        logger.warning("start poliv watering_raspberry")
        on_klapan("poliv_strawberry")
        time.sleep(60 * minutes)
        off_klapan("poliv_strawberry")
    if watering_sad.value:
        logger.warning("start poliv watering_sad")
        on_klapan("poliv_sad")
        time.sleep(60 * minutes * 2)
        off_klapan("poliv_sad")

    V24_arduino(0)
    V24.label = "выключен"
    V24.save()
    logger.warning("end poliv")


def arduino_pshik(param):
    context = testing()
    if param == 1:
        arduino.write(b"K")
        rele = arduino.read()
    else:
        arduino.write(b"k")
        rele = arduino.read()
    context["status"].append(rele)
    return context

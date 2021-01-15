import time
import json
from .Arduino import Arduino
from .DebagArduino import DebagArduino

from django.conf import settings
DEBUG = settings.PLACE
if DEBUG:  # если Дебаг то на компе нет Ардуино
    arduino = DebagArduino()  # используем эмулятор
else:
    try:
        arduino = Arduino()
    except Exception as err:
        print('Error Serial port')

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
        arduino.write(b't')

        test = arduino.read()
        if test == "OK":  # Связь есть, получаем данные
            return {'status': ['Test-OK']}
    return {'status': ['Test-Fail']}


def read_ser():
    context = testing()
    if context['status'][0] == 'Test-Fail':
        return context

    arduino.write(b'p')
    read_arduino = arduino.read()
    try:
        errors, param = read_arduino.split('#')
        param = param.replace("\'", '"')
    except Exception:
        context['status'].append('Error parce Arduino answer')
        return context
    try:
        json_answer = json.loads(param)
    except json.JSONDecodeError:
        context['status'].append('JSONDecodeError')
        return context
    context.update(json_answer)
    return context
    

def reset():
    context = testing()
    arduino.write(b'r')
    arduino.restart()
    context['status'].append('Restart Arduino OK')
    return context


def sound():
    context = testing()
    arduino.write(b'S')
    time.sleep(0.5)
    arduino.write(b's')
    time.sleep(0.5)
    arduino.write(b'S')
    time.sleep(0.5)
    arduino.write(b's')
    context['status'].append('sound')
    return context


def rele_light_balkon(param):
    context = testing()
    if param == 1:
        arduino.write(b'A')
        rele = arduino.read()
    else:
        arduino.write(b'a')
        rele = arduino.read()
    context['status'].append(rele)
    return context


def rele_light_tree(param):
    context = testing()
    if param == 1:
        arduino.write(b'B')
        rele = arduino.read()
    else:
        arduino.write(b'b')
        rele = arduino.read()
    context['status'].append(rele)
    return context


def rele_light_perim(param):
    context = testing()
    if param == 1:
        arduino.write(b'C')
        rele = arduino.read()
    else:
        arduino.write(b'c')
        rele = arduino.read()
    context['status'].append(rele)
    return context

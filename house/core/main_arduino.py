import time
import json
from .Arduino import Arduino
from .DebagArduino import DebagArduino

from django.conf import settings
DEBUG = settings.PLACE
if DEBUG:  # если Дебаг то на компе нет Ардуино
    arduino = DebagArduino()  # используем эмулятор
else:
    arduino = Arduino()


def testing():  # test answer Arduino
    for i in range(3):
        arduino.write(b't')

        test = arduino.read()
        if test == "OK":  # Связь есть, получаем данные
            return {'status': ['Test-OK', i]}
    return {'status': ['Test-Fail']}


def restart_cam():
    context = testing()

    arduino.write(b'0')
    print(arduino.read())
    time.sleep(10)

    arduino.write(b'1')
    print(arduino.read())

    context['status'].append('restart cam OK')
    return context


def read_ser():
    context = testing()
    if context['status'][0] == 'Test-Fail':
        return context

    arduino.write(b'p')
    read_arduino = arduino.read().split('#')
    a = read_arduino[-1]
    b = a.replace("\'",'"')
    print(b)
    try:
        json_answer = json.loads(b)
    except Exception as asd:
        print(asd)

    print(json_answer)
    context['read_arduino'] = read_arduino


    return context
    

def reset():
    context = testing()
    arduino.write(b'r')
    arduino.restart()
    context['status'].append('Restart Arduino OK')
    return context

def boiler_on():
    context = testing()
    arduino.write(b'B')
    print(arduino.read())
    context['status'].append('Boiler on')
    return context

def boiler_off():
    context = testing()
    arduino.write(b'b')
    print(arduino.read())
    context['status'].append('Boiler off')
    return context



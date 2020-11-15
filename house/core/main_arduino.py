import time
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
        time.sleep(1)
        test = arduino.read()
        if test == "OK":  # Связь есть, получаем данные
            return {'status': ['Test-OK', i]}
    return {'status': ['Test-Fail']}


def restart_cam():
    context = testing()

    arduino.write(b'0')
    time.sleep(1)
    print(arduino.read())
    time.sleep(10)

    arduino.write(b'1')
    time.sleep(1)
    print(arduino.read())

    context['status'].append('restart cam OK')
    return context


def read_ser():
    context = testing()
    if context['status'][0] == 'Test-Fail':
        return context

    arduino.write(b'2')
    time.sleep(1)
    read_dht11 = arduino.read()
    if read_dht11 == 'Error_reading_from_DHT':  # ошибка чтения датчика
        context['status'].append('Error_reading_from_DHT')
    else:
        a = read_dht11.split(':')
        context['Humidity_in'] =    int(a[1][0:-3])
        context['Temperature_in'] = int(a[3][0:-3])

    arduino.write(b'3')
    time.sleep(1)
    read_dht22 = arduino.read()
    if read_dht22 == 'Error_reading_from_DHT22':  # ошибка чтения датчика
        context['status'].append('Error_reading_from_DHT')

    else:

        b = read_dht22.split(':')
        context['Humidity_out'] =    int(b[1][0:-3])
        context['Temperature_out'] = int(b[3][0:-3])

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
    time.sleep(1)
    print(arduino.read())
    context['status'].append('Boiler on')
    return context

def boiler_off():
    context = testing()
    arduino.write(b'b')
    time.sleep(1)
    print(arduino.read())
    context['status'].append('Boiler off')
    return context



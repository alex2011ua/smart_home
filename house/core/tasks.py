from __future__ import absolute_import, unicode_literals
from vcgencmd import Vcgencmd

import serial
import time

from .models import Setting
from ..celery import cellery_app


@cellery_app.task()
def smart_home_manager():
    # Здесь ваш код для проверки условий
    print('Celery - work')
    ser = serial.Serial("/dev/ttyACM0",
                        9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600
    time.sleep(3)
    ser.write(b'0')
    time.sleep(3)
    ser.write(b'1')
    time.sleep(3)
    ser.write(b'0')
    time.sleep(3)
    ser.write(b'1')
    time.sleep(3)
    ser.write(b'0')
    time.sleep(3)
    ser.write(b'1')



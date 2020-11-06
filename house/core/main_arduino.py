import serial
import time


def restart_cam():
    ser = serial.Serial("/dev/ttyUSB0",
                        9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600
    ser.write(b't')  # send TEST signal
    time.sleep(0.3)
    test = (ser.read(ser.inWaiting())).decode().strip()
    time.sleep(0.3)
    if test == "OK":  # Связь есть, получаем данные
        ser.write(b'0')
        time.sleep(0.5)
        if (ser.read(ser.inWaiting())).decode().strip() != "rele off":
            ser.close()
            return 'error rele off'
        time.sleep(10)
        ser.write(b'1')
        time.sleep(0.5)
        if (ser.read(ser.inWaiting())).decode().strip() != "rele on":
            ser.close()
            return 'error rele on'
        ser.close()
        return 'restart cam OK'
    ser.close()
    return 'Error Arduino test'


def read_ser():
    ser = serial.Serial("/dev/ttyUSB0",
                        9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600
    ser.write(b't')  # send TEST signal
    time.sleep(0.3)
    test = (ser.read(ser.inWaiting())).decode().strip()
    if test == "OK":  # Связь есть, получаем данные
        time.sleep(0.3)
        ser.write(b'2')
        time.sleep(1)
        read_ser = (ser.read(ser.inWaiting())).decode().strip()
        if read_ser == 'Error_reading_from_DHT':  # ошибка чтения датчика
            ser.close()
            return {'status': 'Error_reading_from_DHT'}
        a = read_ser.split(':')
        context = {'satus': "OK",
                   'Humidity': int(a[1][0:-3]),
                   'Temperature': int(a[3][0:-3])}
        ser.close()
        return context
    ser.close()
    return{'status': 'Error Arduino test'}


def reset():
    ser = serial.Serial("/dev/ttyUSB0",
                        9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600

    ser.write(b'9')
    ser.close()

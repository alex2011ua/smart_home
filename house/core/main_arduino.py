import serial
import time


def testing():  # test answer Arduino
    ser = serial.Serial("/dev/ttyUSB0",
                        9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600
    for i in range(5):
        time.sleep(1)
        ser.write(b't')  # send TEST signal
        time.sleep(1)
        test = (ser.read(ser.inWaiting())).decode().strip()
        if test == "OK":  # Связь есть, получаем данные
            print(i)
            return ser, {'status': ['Test-OK']}
    return ser, {'status': ['Test-Fail']}


def restart_cam():
    ser, context = testing()
    ser.write(b'0')
    time.sleep(1)
    print((ser.read(ser.inWaiting())).decode().strip())
    time.sleep(10)
    ser.write(b'1')
    time.sleep(1)
    print((ser.read(ser.inWaiting())).decode().strip())
    context['status'].append('restart cam OK')
    ser.close()
    return context


def read_ser():
    ser, context = testing()
    if context['status'][0] == 'Test-Fail':
        ser.close()
        return context

    ser.write(b'2')
    time.sleep(1)
    read_dht11 = (ser.read(ser.inWaiting())).decode().strip()
    if read_dht11 == 'Error_reading_from_DHT':  # ошибка чтения датчика
        context['status'].append('Error_reading_from_DHT')
    else:
        a = read_dht11.split(':')
        context['Humidity_in'] = int(a[1][0:-3])
        context['Temperature_in'] = int(a[3][0:-3])

    ser.write(b'3')
    time.sleep(1)
    read_dht22 = (ser.read(ser.inWaiting())).decode().strip()
    if read_dht22 == 'Error_reading_from_DHT22':  # ошибка чтения датчика
        context['status'].append('Error_reading_from_DHT')

    else:
        b = read_dht22.split(':')
        context['Humidity_out'] = int(b[1][0:-3])
        context['Temperature_out'] = int(b[3][0:-3])
    ser.close()
    return context
    

def reset():
    ser, context = testing()
    ser.write(b'r')
    ser.close()
    return context

def boiler():
    ser, context = testing()
    ser.write(b'B')
    time.sleep(1)
    print((ser.read(ser.inWaiting())).decode().strip())
    time.sleep(300)
    ser.write(b'b')
    time.sleep(1)
    print((ser.read(ser.inWaiting())).decode().strip())
    context['status'].append('Boiler on')
    ser.close()
    return context



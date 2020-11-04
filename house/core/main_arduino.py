import serial
import time


def restart_cam():
    status = True
    ser = serial.Serial("/dev/ttyUSB0",
                        9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600
    ser.write(b'0')
    if ser.readline() != "rele off":
        status = False
    time.sleep(10)
    ser.write(b'1')
    if ser.readline() != "rele on":
        status = False
    ser.close()
    return status

def read_ser():
    ser = serial.Serial("/dev/ttyUSB0",
                        9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600
    ser.write(b'2')
    if ser.readline() == "get data":
        ser.readline()
        read_ser = ser.readline()
        ser.close()
        a = read_ser.decode().strip().split(':')
        context = {'Humidity': a[1], 'Temperature': a[3]}
        return context

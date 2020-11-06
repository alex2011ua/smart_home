import serial
import time


def restart_cam():
    status = True
    ser = serial.Serial("/dev/ttyUSB0",
                        9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600
    data = ser.read(ser.inWaiting())
    time.sleep(0.5)
    ser.write(b'0')
    time.sleep(0.5)
    if ser.readline().strip().decode() != "rele off":
        status = False
    time.sleep(10)
    ser.write(b'1')
    time.sleep(0.5)
    if ser.readline().strip().decode() != "rele on":
        status = False
    ser.close()
    return status


def read_ser():
    ser = serial.Serial("/dev/ttyUSB0",
                        9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600
    data = ser.read(ser.inWaiting())
    time.sleep(0.5)
    ser.write(b'2')
    s = ser.readline().strip().decode()
    if s == "get data":
        time.sleep(0.5)
        read_ser = ser.read(ser.inWaiting())
        a = read_ser.decode().strip().split(':')
        context = {'Humidity': int(a[1][0:-3]), 'Temperature': int(a[3][0:-3])}
        return context
    ser.close()

def reset():
    ser = serial.Serial("/dev/ttyUSB0",
                        9600)  # change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate = 9600

    ser.write(b'9')
    ser.close()
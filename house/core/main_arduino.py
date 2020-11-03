import serial
import time


def restart_cam(flag=False):
    if not flag:
        ser = serial.Serial("/dev/ttyUSB0",
                            9600)  # change ACM number as found from ls /dev/tty/ACM*
        ser.baudrate = 9600
        ser.write(b'0')
        time.sleep(10)
        ser.write(b'1')
        ser.close()

def read_ser(flag=False):
    if not flag:
        ser = serial.Serial("/dev/ttyUSB0",
                            9600)  # change ACM number as found from ls /dev/tty/ACM*
        ser.baudrate = 9600
        read_ser = ser.readline()
        ser.close()
    else:
        read_ser = b'Humidity:29.00:Temperature:25.00;\r\n'
    a = read_ser.decode().strip().split(':')
    status = {a[0]: a[1], a[2]: a[3]}

    return status
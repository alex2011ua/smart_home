import serial
import time

def restart_cam(flag):
    if not flag:
        ser = serial.Serial("/dev/ttyUSB0",
                            9600)  # change ACM number as found from ls /dev/tty/ACM*
        ser.baudrate = 9600
        ser.write(b'0')
        time.sleep(10)
        ser.write(b'1')

def read_ser(flag):
    if not flag:
        ser = serial.Serial("/dev/ttyUSB0",
                            9600)  # change ACM number as found from ls /dev/tty/ACM*
        ser.baudrate = 9600
        read_ser = ser.readline()
        return read_ser
    else:
        return 'test str'
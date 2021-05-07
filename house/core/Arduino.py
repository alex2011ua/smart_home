import serial
import time


class Arduino:
    def __init__(self):

        self.ser = serial.Serial("/dev/ttyUSB1", 9600)
        # change ACM number as found from ls /dev/tty/ACM*
        self.ser.baudrate = 9600

    def write(self, param):
        self.ser.write(param)

    def read(self):
        time.sleep(2)
        string_arduino = self.ser.read(self.ser.inWaiting())
        return string_arduino.decode().strip()

    def restart(self):
        self.ser.close()
        time.sleep(15)
        self.ser = serial.Serial("/dev/ttyUSB0", 9600)
        # change ACM number as found from ls /dev/tty/ACM*
        self.ser.baudrate = 9600

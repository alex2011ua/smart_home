import time as t


def raspberry(flag):
    if not flag:
        from vcgencmd import Vcgencmd

        status = {}
        list_alarm = {
            "0": "В настоящий момент производительность процессора снижена из-за проблем с питанием, низкое напряжение",
            "1": "В настоящий момент производительность процессора снижена из-за ручного ограничения частоты",
            "2": "В настоящий момент производительность процессора снижена",
            "3": "В настоящий момент производительность процессора снижена из-за перегрева процессора",
            "16": "Производительность процессора в этом сеансе работы была когда-то снижена из-за проблем с питанием, низкое напряжение",
            "17": "Производительность процессора в этом сеансе работы была когда-то снижена&amp;из-за ручного ограничения частоты",
            "18": "Производительность процессора в этом сеансе работы была когда-то снижена",
            "19": "Производительность процессора в этом сеансе работы была когда-то снижена&amp;из-за перегрева процессора",
        }

        vcgm = Vcgencmd()
        output = vcgm.get_throttled()
        status["Raspberry"] = []
        if output["binary"] != "00000000000000000000":
            for item, value in output["breakdown"].items():
                if value is True:
                    status["Raspberry"].append(list_alarm[value])

        status["temp_core"] = vcgm.measure_temp()
        return status
    else:
        status = {"Raspberry": [], "temp_core": 44}
        return status


def restart_cam(flag):
    if not flag:
        import smbus

        DEVICE_BUS = 1
        DEVICE_ADDR = 0x10
        bus = smbus.SMBus(DEVICE_BUS)
        bus.write_byte_data(DEVICE_ADDR, 1, 0xFF)
        t.sleep(8)
        bus.write_byte_data(DEVICE_ADDR, 1, 0x00)


def button(flag):
    # GPIO5 is button input
    if not flag:
        import RPi.GPIO as GPIO

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        boiler = GPIO.input(19)
        dvor = GPIO.input(6)
        garaz = GPIO.input(26)
        #  True - открыто, разомкнуто
        #  False -  закрыто, замкнуто

    else:
        garaz = False
        dvor = True

    return {"Garaz": garaz, "Dor_street": dvor}


def boiler_on(flag):
    if not flag:
        import smbus

        DEVICE_BUS = 1
        DEVICE_ADDR = 0x10
        bus = smbus.SMBus(DEVICE_BUS)
        bus.write_byte_data(DEVICE_ADDR, 2, 0xFF)


def boiler_off(flag):
    if not flag:
        import smbus

        DEVICE_BUS = 1
        DEVICE_ADDR = 0x10
        bus = smbus.SMBus(DEVICE_BUS)
        bus.write_byte_data(DEVICE_ADDR, 2, 0x00)


def printer_on(flag):
    if not flag:
        import smbus

        DEVICE_BUS = 1
        DEVICE_ADDR = 0x10
        bus = smbus.SMBus(DEVICE_BUS)
        bus.write_byte_data(DEVICE_ADDR, 3, 0xFF)


def printer_off(flag):
    if not flag:
        import smbus

        DEVICE_BUS = 1
        DEVICE_ADDR = 0x10
        bus = smbus.SMBus(DEVICE_BUS)
        bus.write_byte_data(DEVICE_ADDR, 3, 0x00)

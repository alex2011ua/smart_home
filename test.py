import serial

import time

ser = serial.Serial("/dev/ttyACM0", 9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate = 9600



while True:
    read_ser=ser.readline()
    print(read_ser)
    time.sleep(3)
    ser.write(b'0')
    time.sleep(3)
    ser.write(b'1')


def smart_home_manager():
    # Здесь ваш код для проверки условий
    print('Celery - work')

    list_alarm = {
        '0': 'В настоящий момент производительность процессора снижена из-за проблем с питанием, низкое напряжение',
        '1': 'В настоящий момент производительность процессора снижена из-за ручного ограничения частоты',
        '2': 'В настоящий момент производительность процессора снижена',
        '3': 'В настоящий момент производительность процессора снижена из-за перегрева процессора',
        '16': 'Производительность процессора в этом сеансе работы была когда-то снижена из-за проблем с питанием, низкое напряжение',
        '17': 'Производительность процессора в этом сеансе работы была когда-то снижена&amp;из-за ручного ограничения частоты',
        '18': 'Производительность процессора в этом сеансе работы была когда-то снижена',
        '19': 'Производительность процессора в этом сеансе работы была когда-то снижена&amp;из-за перегрева процессора'}

    vcgm = Vcgencmd()
    output = vcgm.get_throttled()
    if output['binary'] != '00000000000000000000':
        for item, value in output['breakdown'].items():
            if value == True:
                print(list_alarm[str(item)])
    else:
        print('Ошибок не обнаружено!')

    temp = vcgm.measure_temp()
    print(temp)




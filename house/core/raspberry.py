
def raspberry(flag):
    if not flag:
        from vcgencmd import Vcgencmd
        status = {}
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
                if value is True:
                    status[item] = value
                    print(list_alarm[str(item)])
        else:
            status['Raspberry'] = 'Ошибок не обнаружено!'
            print('Ошибок не обнаружено!')

        temp = vcgm.measure_temp()
        status['Температура процессора'] = temp
        return status
    else:
        status = {'test Raspbery': 'Non Connect', 'test Raspbery2': 'Non Connect'}
        return status

def button(flag):
        # Connections:
        # GPIO5 is button input
    if not flag:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        boiler = GPIO.input(5)
        garaz = GPIO.input(6)
        dvor = GPIO.input(13)
        status = {}
        if boiler == False:
            print('boiler ON')
            status.update({'Бойлер': "Включен"})
        else:
            print("boiler OFF")
            status.update({'Бойлер': "Выключен"})
        if garaz == False:
            print('garaz ON')
            status.update({'Гараж': "Открыт"})
        else:
            print("boiler OFF")
            status.update({'Бойлер': "Закрыт"})
        if dvor == False:
            print('dvor ON')
            status.update({'Дверь': "Открыт"})
        else:
            print("boiler OFF")
            status.update({'Дверь': "Закрыт"})
    else:
        status = {'Raspbery': 'Non Connect'}
    return status

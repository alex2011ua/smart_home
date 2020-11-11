
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
            status['OK'] = 'Ошибок не обнаружено!'
            print('Ошибок не обнаружено!')

        temp = vcgm.measure_temp()
        status['temp'] = temp
        return status
    else:
        status = {'test Raspbery': 'Non Connect', 'test Raspbery2': 'Non Connect'}
        return status

def boiler(flag):
        # Connections:
        # GPIO2 is button input
    if not flag:
        from gpiozero import Button
        button = Button(2)
        if button.is_pressed:
            print("boiler ON")
            status = {'boiler': "ON"}
        else:
            print("boiler OFF")
            status = {'boiler': "ON"}
    else:
        status = {'Boiler': 'Non Connect'}
    return status

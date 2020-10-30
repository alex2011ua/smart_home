from django.urls import reverse_lazy
from django.views.generic import FormView

from .models import Setting
from .form import ControllerForm
from ..celery import add
from django.http import HttpResponse
from vcgencmd import Vcgencmd
import time
import serial




class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        context['data'] = {}
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
                    context['data'][item]=value
                    print(list_alarm[str(item)])
        else:
            context['data']['OK'] = 'Ошибок не обнаружено!'
            print('Ошибок не обнаружено!')

        temp = vcgm.measure_temp()
        context['data']['temp'] = temp
        print(temp)
        ser = serial.Serial("/dev/ttyUSB0",
                            9600)  # change ACM number as found from ls /dev/tty/ACM*
        ser.baudrate = 9600
        time.sleep(3)
        ser.write(b'0')
        time.sleep(3)
        ser.write(b'1')


        return context

    def get_initial(self):
        return {}

    def form_valid(self, form):
        return super(ControllerView, self).form_valid(form)



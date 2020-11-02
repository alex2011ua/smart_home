import os

from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views import View
from django.shortcuts import render, redirect

from .models import Setting
from .form import ControllerForm
from ..celery import add
from django.http import HttpResponse

import time





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
        from vcgencmd import Vcgencmd
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
        DEBUG = bool(os.environ.get('myDEBUG'))
        context['data']['DEBUG'] = DEBUG
        print(temp)



        return context

    def get_initial(self):
        return {}

    def form_valid(self, form):
        return super(ControllerView, self).form_valid(form)


class RestartCam(View):
    @staticmethod
    def get(request):
        import serial
        ser = serial.Serial("/dev/ttyUSB0",
                            9600)  # change ACM number as found from ls /dev/tty/ACM*
        ser.baudrate = 9600
        time.sleep(3)
        ser.write(b'0')
        time.sleep(3)
        ser.write(b'1')
        return redirect(reverse_lazy('form'))

class Env(View):
    @staticmethod
    def get(request):

        env = os.environ.get('test_env')
        DEBUG = bool(os.environ.get('myDEBUG'))
        if DEBUG:
            s = 'TRUE'
        else:
            s = 'FALSE'
        print(s)
        return HttpResponse(content = f'--{env}-- запись в переменной, --{DEBUG}-- значение дебаг, --{s}-- тип дебаг', status = 200)

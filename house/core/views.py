import os

from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
DEBUG = settings.DEBUG

from .models import Setting, Temp1, Logs, Temp_out, WeatherRain
from .form import ControllerForm

from django.http import HttpResponse

from .main_arduino import restart_cam, read_ser, reset
from .raspberry import raspberry
from .weather_rain import weather_now
from house.core.tasks import restart_cam_task, weather_task, arduino_task
import datetime




class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        date_now = datetime.datetime.now()
        weather_6 = WeatherRain.objects.filter(date__gt=date_now)
        context['weather_6'] = {'rain6': weather_6[0].rain,
                                'temp_min6': weather_6[0].temp_min,
                                'temp_max6': weather_6[0].temp_max,
                                'snow6': weather_6[0].snow,
                                }
        context['data'] = raspberry(DEBUG)  # state raspberry
        try:
            temp_in = Temp1.objects.all().order_by('-id')[0]  # arduino state
            temp_out = Temp_out.objects.all().order_by('-id')[0]  # arduino state
        except IndexError:
            temp_in = Temp1.objects.create(date_temp = datetime.datetime.now(),
                                           temp = 111,
                                           humidity = 222)
            temp_out = Temp_out.objects.create(date_temp = datetime.datetime.now(),
                                           temp = 111,
                                           humidity = 222)

        context['data']['temp_in'] = temp_in.temp
        context['data']['humidity_in'] = temp_in.humidity
        context['data']['date_temp_in'] = temp_in.date_temp
        context['data']['temp_out'] = temp_out.temp
        context['data']['humidity_out'] = temp_out.humidity
        context['data']['date_temp_out'] = temp_out.date_temp
        date_now = datetime.datetime.now()
        context['time'] = date_now

        context.update(weather_now())

        logs = Logs.objects.all().order_by('-date_log')[0:20]
        context['logs'] = logs
        return context

    def get_initial(self):
        return {}

    def form_valid(self, form):
        return super(ControllerView, self).form_valid(form)


class RestartCam(View):
    @staticmethod
    def get(request):
        restart_cam_task()
           # отключение реле на 10 сек
        return redirect(reverse_lazy('form'))

class Temp(View):
    @staticmethod
    def get(request):
        arduino_task()
        weather_task()
        return redirect(reverse_lazy('form'))


class ResetArduino(View):
    @staticmethod
    def get(request):
        try:
            reset()
            log = Logs.objects.create(date_log = datetime.datetime.now(),
                                      title_log = 'arduino',
                                      description_log = 'Aрдуино reset')
        except Exception:
            log = Logs.objects.create(date_log = datetime.datetime.now(),
                                  title_log = 'arduino',
                                  description_log = 'Ошибка ардуино reset')

        return redirect(reverse_lazy('form'))

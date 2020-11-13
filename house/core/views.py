import os

from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
DEBUG = settings.DEBUG

from .models import Setting, Temp1, Logs, Temp_out, WeatherRain
from .form import ControllerForm
from .tasks import boiler_task_on, boiler_task_off
from django.http import HttpResponse

from .main_arduino import restart_cam, read_ser, reset, testing
from .raspberry import raspberry, boiler
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

        weather_6 = WeatherRain.objects.all().order_by('-date')[0]



        context['data'] = raspberry(DEBUG)  # state raspberry
        context['data'].update(boiler(DEBUG))  # state boiler

        try:
            temp_in = Temp1.objects.all().order_by('-date_temp')[0]  # arduino state
            temp_out = Temp_out.objects.all().order_by('-date_temp')[0]  # arduino state
        except IndexError:
            temp_in = Temp1.objects.create(date_temp = datetime.datetime.now(),
                                           temp = 111,
                                           humidity = 222)
            temp_out = Temp_out.objects.create(date_temp = datetime.datetime.now(),
                                           temp = 111,
                                           humidity = 222)

        context['data']['Температура  комнаты 1'] = temp_in.temp
        context['data']['Влажность комнаты 1'] = temp_in.humidity
        context['data']['Дата измерения'] = temp_in.date_temp
        context['data']['Температура уличного датчика'] = temp_out.temp
        context['data']['Влажность на улице'] = temp_out.humidity
        context['data']['Дата измерения улица'] = temp_out.date_temp
        context['data']['Сумма осадков в следующие 6 дней'] = weather_6.rain
        context['data']['Количество снега в следующие 6 дней'] = weather_6.snow
        context['data']['минимальная температура за 6 дней'] = weather_6.temp_min
        context['data']['максимальная температура за 6 дней'] = weather_6.temp_max
        context['data']['Завтра'] = weather_6.date

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

class Boiler(View):
    @staticmethod
    def get(request):
        try:
            boiler_task_on.delay()
            log = Logs.objects.create(date_log = datetime.datetime.now(),
                                      title_log = 'Boiler',
                                      description_log = 'Включение бойлера')
        except Exception as exx:
            log = Logs.objects.create(date_log = datetime.datetime.now(),
                                  title_log = 'Boiler',
                                  description_log = 'Ошибка ардуино Boiler'+ str(exx))
        try:
            boiler_task_off.apply_async(countdown=60*5)
            log = Logs.objects.create(date_log = datetime.datetime.now(),
                                      title_log = 'Boiler',
                                      description_log = 'ВЫключение бойлера')
        except Exception as exx:
            log = Logs.objects.create(date_log = datetime.datetime.now(),
                                  title_log = 'Boiler',
                                  description_log = 'Ошибка ардуино Boiler'+str(exx))

        return redirect(reverse_lazy('form'))


class Test(View):
    @staticmethod
    def get(request):
        try:
            status = testing()
            log = Logs.objects.create(date_log = datetime.datetime.now(),
                                      title_log = 'arduino',
                                      description_log = status)
        except Exception:
            log = Logs.objects.create(date_log = datetime.datetime.now(),
                                  title_log = 'arduino',
                                  description_log = 'Ошибка ардуино TEST')

        return redirect(reverse_lazy('form'))
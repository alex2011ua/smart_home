import os

from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
DEBUG = settings.PLACE

from .models import Logs, DHT_MQ, Weather
from .form import ControllerForm
from .tasks import boiler_task_on, boiler_task_off
from django.http import HttpResponse

from .main_arduino import restart_cam, read_ser, reset, testing
from .raspberry import raspberry, button
from .weather_rain import weather_now
from house.core.tasks import restart_cam_task, weather_task, arduino_task
import datetime




class ControllerView(View):
    @staticmethod
    def get(request):
        context = {}
        date_now = datetime.datetime.now()

        context['raspberry'] = raspberry(DEBUG)  # state raspberry
        context['button'] = button(DEBUG)  # загрузка состояний кнопок

        try:
            temp = DHT_MQ.objects.all().order_by('-date_t_h')[0]  # arduino state
        except IndexError:
            temp = DHT_MQ.objects.create(date_t_h=datetime.datetime.now())
        context['sensors'] = {}
        context['sensors']['date_t_h'] = temp.date_t_h
        context['sensors']['street_temp'] = temp.temp_street
        context['sensors']['humidity_street'] = temp.humidity_street

        context['sensors']['temp_voda'] = temp.temp_voda
        context['sensors']['humidity_voda'] = temp.humidity_voda

        context['sensors']['temp_gaz'] = temp.temp_gaz
        context['sensors']['humidity_gaz'] = temp.humidity_gaz

        context['sensors']['temp_teplica'] = temp.temp_teplica
        context['sensors']['humidity_teplica'] = temp.humidity_teplica

        context['sensors']['gaz_MQ4'] = temp.gaz_MQ4
        context['sensors']['gaz_MQ135'] = temp.gaz_MQ135
        try:
            weather_6 = Weather.objects.all().order_by('-date')[0]
        except:
            return redirect(reverse_lazy('temp'))
        context['weather_6_day'] = {}
        context['weather_6_day']['rain'] = weather_6.rain
        context['weather_6_day']['snow'] = weather_6.snow
        context['weather_6_day']['temp_min'] = weather_6.temp_min
        context['weather_6_day']['temp_max'] = weather_6.temp_max
        context['weather_6_day']['tomorrow'] = weather_6.date

        context['time'] = date_now

        context.update(weather_now())

        logs = Logs.objects.all().order_by('-date_log')[0:20]
        context['logs'] = logs
        return render(request, "core/control.html", context)

class RestartCam(View):
    @staticmethod
    def get(request):
        restart_cam_task()
           # отключение реле на 10 сек
        return redirect(reverse_lazy('form'))

class Temp(View):
    @staticmethod
    def get(request):
        arduino_task()  # читает датчики и занозит изменетия в БД
        weather_task()  # Запрашивает по АПИ прогноз погоды и вносит в БД
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
            boiler_task_off.apply_async(countdown=60*10)
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
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

        context['data'] = raspberry(DEBUG)  # state raspberry
        context['data'].update(button(DEBUG))  # state boiler

        try:
            temp = DHT_MQ.objects.all().order_by('-date_t_h')[0]  # arduino state
        except IndexError:
            temp = DHT_MQ.objects.create(date_t_h=datetime.datetime.now())
        context['data']['Дата измерения'] = temp.date_t_h
        context['data']['Температура уличного датчика'] = temp.temp_street
        context['data']['Влажность на улице'] = temp.humidity_street

        context['data']['Температура входящей воды'] = temp.temp_voda
        context['data']['Влажность возле котла'] = temp.humidity_voda

        context['data']['Температура котельной'] = temp.temp_gaz
        context['data']['Влажность котельной'] = temp.humidity_gaz

        context['data']['Температура теплицы'] = temp.temp_teplica
        context['data']['Влажность теплицы'] = temp.humidity_teplica

        context['data']['Показания датчика MQ4'] = temp.gaz_MQ4
        context['data']['Влажность датчика MQ135'] = temp.gaz_MQ135
        try:
            weather_6 = Weather.objects.all().order_by('-date')[0]
        except:
            return redirect(reverse_lazy('temp'))
        context['data']['Сумма осадков в следующие 6 дней'] = weather_6.rain
        context['data']['Количество снега в следующие 6 дней'] = weather_6.snow
        context['data']['минимальная температура за 6 дней'] = weather_6.temp_min
        context['data']['максимальная температура за 6 дней'] = weather_6.temp_max
        context['data']['Завтра'] = weather_6.date

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
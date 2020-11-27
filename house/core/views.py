from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect

from .models import Logs, DHT_MQ, Weather, Setting
from .tasks import boiler_task_on, boiler_task_off

from .main_arduino import reset, rele_light_balkon, rele_light_tree, rele_light_perim
from .raspberry import raspberry, button
from .weather_rain import weather_now
from house.core.tasks import restart_cam_task, weather_task, arduino_task
import datetime
from django.conf import settings
DEBUG = settings.PLACE


class ControllerView(View):
    @staticmethod
    def get(request):
        context = {}
        date_now = datetime.datetime.now()

        boiler, created = Setting.objects.get_or_create(
            controller_name='boiler',
            defaults = {'label': 'Выключен','value': 0})
        light_balkon, created = Setting.objects.get_or_create(
            controller_name = 'light_balkon',
            defaults = {'label': '1', 'value': 0})
        light_tree, created = Setting.objects.get_or_create(
            controller_name = 'light_tree',
            defaults = {'label': '2', 'value': 0})
        light_perim, created = Setting.objects.get_or_create(
            controller_name = 'light_perim',
            defaults = {'label': '3', 'value': 0})
        context['light_balkon'] = light_balkon
        context['light_tree'] = light_tree
        context['light_perim'] = light_perim
        context['boiler'] = boiler
        context['raspberry'] = raspberry(DEBUG)  # state raspberry
        context['button'] = button(DEBUG)  # загрузка состояний кнопок
        try:
            temp = DHT_MQ.objects.all().order_by('-date_t_h')[0]  # arduino state
        except IndexError:
            temp = DHT_MQ.objects.create(date_t_h = datetime.datetime.now())

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
        except IndexError:
            return redirect(reverse_lazy('temp'))
        context['weather_6_day'] = {}
        context['weather_6_day']['rain'] = weather_6.rain
        context['weather_6_day']['snow'] = weather_6.snow
        context['weather_6_day']['temp_min'] = weather_6.temp_min
        context['weather_6_day']['temp_max'] = weather_6.temp_max
        context['weather_6_day']['tomorrow'] = weather_6.date
        context['time'] = date_now

        context.update(weather_now())

        logs = Logs.objects.all().order_by('-date_log')[0:5]
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
            Logs.objects.create(date_log=datetime.datetime.now(),
                                status='OK',
                                title_log='view ResetArduino',
                                description_log='Aрдуино reset')
        except Exception:
            Logs.objects.create(date_log=datetime.datetime.now(),
                                status='Error',
                                title_log='view ResetArduino',
                                description_log='Ошибка ардуино reset')

        return redirect(reverse_lazy('form'))


class Boiler(View):
    @staticmethod
    def get(request):
        boiler = Setting.objects.get(controller_name='boiler')
        if boiler.value == 0:
            try:
                boiler_task_on.delay()
                boiler.label = 'Бойлер включен'
                boiler.value = 1
                boiler.save()
            except Exception as exx:
                Logs.objects.create(date_log = datetime.datetime.now(),
                                    status = 'Error',
                                    title_log = 'view Boiler',
                                    description_log = 'Ошибка ардуино Boiler' + str(
                                        exx))
            try:
                boiler_task_off.apply_async(countdown = 60 * 10)
            except Exception as exx:
                Logs.objects.create(date_log = datetime.datetime.now(),
                                    status = 'Error',
                                    title_log = 'view Boiler',
                                    description_log = 'Ошибка ардуино Boiler' + str(
                                        exx))
        return redirect(reverse_lazy('form'))


class Rele(View):
    @staticmethod
    def get(request, rele_id):
        rele_id = int(rele_id)
        if rele_id == 1:
            rele = Setting.objects.get(controller_name = 'light_balkon')
            if rele.value == 0:
                rele_light_balkon(1)
                rele.value = 1
                rele.save()
            else:
                rele_light_balkon(0)
                rele.value = 0
                rele.save()
        if rele_id == 2:
            rele = Setting.objects.get(controller_name = 'light_tree')
            if rele.value == 0:
                rele_light_tree(1)
                rele.value = 1
                rele.save()
            else:
                rele_light_tree(0)
                rele.value = 0
                rele.save()
        if rele_id == 3:
            rele = Setting.objects.get(controller_name = 'light_perim')
            if rele.value == 0:
                rele_light_perim(1)
                rele.value = 1
                rele.save()
            else:
                rele_light_perim(0)
                rele.value = 0
                rele.save()
        return redirect(reverse_lazy('form'))

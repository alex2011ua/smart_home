from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Logs, DHT_MQ, Weather, Setting
from .tasks import boiler_task_on, boiler_task_off, bot_task_11_hour

from .main_arduino import reset, rele_light_balkon, rele_light_tree, rele_light_perim
from .raspberry import raspberry, button
from .weather_rain import weather_now
from house.core.tasks import restart_cam_task, weather_task, arduino_task
import datetime
from django.conf import settings
from .raspberry import printer_off, printer_on
from .Telegram import bot
import logging
logger = logging.getLogger('django')
DEBUG = settings.PLACE


class ControllerView(LoginRequiredMixin, View):
    """Оснавная страница"""

    @staticmethod
    def get(request):

        context = {}
        date_time_now = datetime.datetime.now()
        #Инфо о ошибках датчиков
        Error_dht, created = Setting.objects.get_or_create(
            controller_name="Error_dht",
            defaults={'label': '', 'value': 0, 'date': datetime.datetime.now()})

        # Состояние бойлера и света
        V24 = Setting.objects.get(controller_name='V24')

        printer, created = Setting.objects.get_or_create(
            controller_name='printer',
            defaults={'label': 'Выключен', 'value': 0})
        boiler, created = Setting.objects.get_or_create(
            controller_name='boiler',
            defaults={'label': 'Выключен', 'value': 0})
        light_balkon, created = Setting.objects.get_or_create(
            controller_name='light_balkon',
            defaults={'label': '1', 'value': 0})
        light_tree, created = Setting.objects.get_or_create(
            controller_name='light_tree',
            defaults={'label': '2', 'value': 0})
        light_perim, created = Setting.objects.get_or_create(
            controller_name='light_perim',
            defaults={'label': '3', 'value': 0})
        poliv, created = Setting.objects.get_or_create(
            controller_name='poliv',
            defaults={'label': 'Выключен', 'value': 0})
        alarms, created = Setting.objects.get_or_create(
            controller_name='alarms',
            defaults={'label': 'Выключен', 'value': 0})
        solnce, created = Setting.objects.get_or_create(
            controller_name='solnce',
            defaults={'label': 'Выключен', 'value': 0})
        context['V24'] = V24
        context['Error_dht'] = Error_dht
        context['solnce'] = solnce
        context['alarms'] = alarms
        context['poliv'] = poliv
        context['light_balkon'] = light_balkon
        context['light_tree'] = light_tree
        context['light_perim'] = light_perim
        context['boiler'] = boiler
        context['printer'] = printer
        context['raspberry'] = raspberry(DEBUG)  # state raspberry
        context['button'] = button(DEBUG)  # загрузка состояний датчиков Raspberry
        # Получение параметров arduino из БД
        try:
            temp = DHT_MQ.objects.all().order_by('-date_t_h')[0]
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

        # Получение инфо о погоде из бд
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
        context['time'] = date_time_now

        # Получение инфо о погоде на сгодня завтра по API
        context.update(weather_now())
        # Извлечение логов с ошибками из БД за последний день
        date_now = datetime.date.today()
        result_date = date_now - datetime.timedelta(days=1)
        logs = Logs.objects.filter(status='Error', date_log__gte=result_date).order_by('-date_log')[0:5]
        context['logs'] = logs

        return render(request, "core/control.html", context)


class RestartCam(LoginRequiredMixin, View):
    """Restart my cemeras"""

    @staticmethod
    def get(request):
        restart_cam_task()
        # отключение реле на 10 сек
        return redirect(reverse_lazy('form'))


class Temp(LoginRequiredMixin, View):
    """Обновляет информацию о температуре и прогнозе погоды в БД"""

    @staticmethod
    def get(request):
        arduino_task()  # читает датчики и занозит изменетия в БД
        weather_task()  # Запрашивает по АПИ прогноз погоды и вносит в БД
        return redirect(reverse_lazy('form'))


class ResetArduino(LoginRequiredMixin, View):
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


class Boiler(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        boiler = Setting.objects.get(controller_name='boiler')
        if boiler.value == 0:

            try:  # Включение бойлера и запись в БД
                boiler_task_on.delay()
                boiler.label = 'Бойлер включен'
                boiler.value = 1
                boiler.save()
                bot.send_message('Включен бойлер')
            except Exception as exx:
                Logs.objects.create(date_log=datetime.datetime.now(),
                                    status='Error',
                                    title_log='view Boiler',
                                    description_log='Ошибка ардуино Boiler' + str(
                                        exx))
            try:  # Задача на выключение бойлера
                boiler_task_off.apply_async(countdown=60 * 10)
            except Exception as exx:
                Logs.objects.create(date_log=datetime.datetime.now(),
                                    status='Error',
                                    title_log='view Boiler',
                                    description_log='Ошибка ардуино Boiler' + str(
                                        exx))
        return redirect(reverse_lazy('form'))


class Rele(LoginRequiredMixin, View):
    """Включение и выключение реле"""

    @staticmethod
    def get(request, rele_id):
        rele_id = int(rele_id)
        if rele_id == 1:
            rele = Setting.objects.get(controller_name='light_balkon')
            if rele.value == 0:
                rele_light_balkon(1)
                rele.value = 1
                rele.save()
            else:
                rele_light_balkon(0)
                rele.value = 0
                rele.save()
        if rele_id == 2:
            rele = Setting.objects.get(controller_name='light_tree')
            if rele.value == 0:
                rele_light_tree(1)
                rele.value = 1
                rele.save()
            else:
                rele_light_tree(0)
                rele.value = 0
                rele.save()
        if rele_id == 3:
            rele = Setting.objects.get(controller_name='light_perim')
            if rele.value == 0:
                rele_light_perim(1)
                rele.value = 1
                rele.save()
            else:
                rele_light_perim(0)
                rele.value = 0
                rele.save()
        return redirect(reverse_lazy('form'))


class Light(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        bot_task_11_hour()
        return redirect(reverse_lazy('form'))


class Printer(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        printer = Setting.objects.get(controller_name='printer')
        if printer.value == 0:

            try:  # Включение принтера и запись в БД
                printer_on(DEBUG)
                printer.label = 'printer включен'
                print('включен')
                printer.value = 1
                printer.save()
                bot.send_message('Включение принтера')
            except Exception as exx:
                Logs.objects.create(date_log=datetime.datetime.now(),
                                    status='Error',
                                    title_log='view Boiler',
                                    description_log='Ошибка ардуино Boiler' + str(
                                        exx))
        else:
            try:  # Выключение принтера и запись в БД
                printer_off(DEBUG)
                printer.label = 'printer выключен'
                print('выключен')
                printer.value = 0
                printer.save()
                bot.send_message('ВЫключение принтера')
            except Exception as exx:
                Logs.objects.create(date_log=datetime.datetime.now(),
                                    status='Error',
                                    title_log='view Boiler',
                                    description_log='Ошибка ардуино Boiler' + str(
                                        exx))
        return redirect(reverse_lazy('form'))


class Alarms(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        alarms = Setting.objects.get(controller_name='alarms')
        if alarms.value == 0:
            alarms.value = 1
            alarms.label = 'Извещения включены'
            alarms.save()
            bot.send_message('Извещения включены')
        else:
            alarms.value = 0
            alarms.label = 'Извещения выключены'
            alarms.save()
            bot.send_message('Извещения выключены')
        return redirect(reverse_lazy('form'))


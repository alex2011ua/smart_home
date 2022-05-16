import datetime
import logging

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from house.core.tasks import arduino_task, restart_cam_task, weather_task

from .main_arduino import rele_light_balkon, bassein, reset
from .models import DHT_MQ, Logs, Setting, Weather
from .raspberry import button, printer_off, printer_on, raspberry
from .tasks import boiler_task_off, boiler_task_on, bot_task_11_hour
from .Telegram import bot
from .weather_rain import weather_now
from .matplot import refresh, calend

logger = logging.getLogger("django")
DEBUG = settings.PLACE


class ControllerView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Оснавная страница"""

    permission_required = "is_staff"

    @staticmethod
    def get(request):
        context = {}
        date_time_now = datetime.datetime.now()
        # Инфо о ошибках датчиков

        Error_dht, created = Setting.objects.get_or_create(
            controller_name="Error_dht",
            defaults={"label": "", "value": 0, "date": datetime.datetime.now()},
        )

        # Состояние бойлера и света
        max_temp_teplica, created = Setting.objects.get_or_create(
            controller_name="max_temp_teplica",
            defaults={"label": "", "value": 0, "date": datetime.datetime.now()},
        )
        min_temp_teplica, created = Setting.objects.get_or_create(
            controller_name="min_temp_teplica",
            defaults={"label": "", "value": 100, "date": datetime.datetime.now()},
        )
        V24, created = Setting.objects.get_or_create(
            controller_name="V24",
            defaults={"label": "", "value": 0, "date": datetime.datetime.now()},
        )
        room1, created = Setting.objects.get_or_create(
            controller_name="room1",
            defaults={"label": "", "value": 0, "date": date_time_now},
        )
        printer, created = Setting.objects.get_or_create(
            controller_name="printer", defaults={"label": "Выключен", "value": 0}
        )
        boiler, created = Setting.objects.get_or_create(
            controller_name="boiler", defaults={"label": "Выключен", "value": 0}
        )
        light_balkon, created = Setting.objects.get_or_create(
            controller_name="light_balkon", defaults={"label": "1", "value": 0}
        )
        bassein, created = Setting.objects.get_or_create(
            controller_name="bassein", defaults={"label": "2", "value": 0}
        )

        poliv, created = Setting.objects.get_or_create(
            controller_name="poliv", defaults={"label": "Выключен", "value": 0}
        )
        alarms, created = Setting.objects.get_or_create(
            controller_name="alarms", defaults={"label": "Выключен", "value": 0}
        )
        solnce, created = Setting.objects.get_or_create(
            controller_name="solnce", defaults={"label": "Выключен", "value": 0}
        )

        context["max_temp_teplica"] = max_temp_teplica
        context["min_temp_teplica"] = min_temp_teplica
        context["radio_room1"] = room1
        context["V24"] = V24
        context["Error_dht"] = Error_dht
        context["solnce"] = solnce
        context["alarms"] = alarms
        context["poliv"] = poliv
        context["light_balkon"] = light_balkon
        context["bassein"] = bassein
        context["boiler"] = boiler
        context["printer"] = printer
        context["raspberry"] = raspberry(DEBUG)  # state raspberry
        context["button"] = button(DEBUG)  # загрузка состояний датчиков Raspberry
        # Получение параметров arduino из БД
        try:
            temp = DHT_MQ.objects.all().order_by("-date_t_h")[0]
        except IndexError:
            temp = DHT_MQ.objects.create(date_t_h=datetime.datetime.now())

        context["sensors"] = {}
        context["sensors"]["date_t_h"] = temp.date_t_h
        context["sensors"]["street_temp"] = temp.temp_street
        context["sensors"]["humidity_street"] = temp.humidity_street
        context["sensors"]["temp_voda"] = temp.temp_voda
        context["sensors"]["humidity_voda"] = temp.humidity_voda
        context["sensors"]["temp_gaz"] = temp.temp_gaz
        context["sensors"]["humidity_gaz"] = temp.humidity_gaz
        context["sensors"]["temp_teplica"] = temp.temp_teplica
        context["sensors"]["humidity_teplica"] = temp.humidity_teplica
        context["sensors"]["gaz_MQ4"] = temp.gaz_MQ4
        context["sensors"]["gaz_MQ135"] = temp.gaz_MQ135

        # Получение инфо о погоде из бд
        try:
            weather_6 = Weather.objects.all().order_by("-date")[0]
        except IndexError:
            return redirect(reverse_lazy("temp"))
        context["weather_6_day"] = {}
        context["weather_6_day"]["rain"] = weather_6.rain
        context["weather_6_day"]["snow"] = weather_6.snow
        context["weather_6_day"]["temp_min"] = weather_6.temp_min
        context["weather_6_day"]["temp_max"] = weather_6.temp_max
        context["weather_6_day"]["tomorrow"] = weather_6.date
        context["time"] = date_time_now

        # Получение инфо о погоде на сгодня завтра по API
        context.update(weather_now())
        # Извлечение логов с ошибками из БД за последний день
        date_now = datetime.date.today()
        result_date = date_now - datetime.timedelta(days=1)
        logs = Logs.objects.filter(status="Error", date_log__gte=result_date).order_by("-date_log")[
            0:5
        ]
        context["logs"] = logs

        return render(request, "core/control.html", context)


class RestartCam(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Restart my cemeras"""

    permission_required = "is_staff"

    @staticmethod
    def get(request):
        restart_cam_task()
        # отключение реле на 10 сек
        return redirect(reverse_lazy("form"))


class Temp(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Обновляет информацию о температуре и прогнозе погоды в БД"""

    permission_required = "is_staff"

    @staticmethod
    def get(request):
        arduino_task()  # читает датчики и занозит изменетия в БД
        weather_task()  # Запрашивает по АПИ прогноз погоды и вносит в БД
        refresh()
        calend()
        return redirect(reverse_lazy("form"))


class ResetArduino(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "is_staff"

    @staticmethod
    def get(request):
        try:
            reset()
            Logs.objects.create(
                date_log=datetime.datetime.now(),
                status="OK",
                title_log="view ResetArduino",
                description_log="Aрдуино reset",
            )
        except Exception:
            Logs.objects.create(
                date_log=datetime.datetime.now(),
                status="Error",
                title_log="view ResetArduino",
                description_log="Ошибка ардуино reset",
            )

        return redirect(reverse_lazy("form"))


class Boiler(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "is_staff"

    @staticmethod
    def get(request):
        boiler = Setting.objects.get(controller_name="boiler")
        if boiler.value == 0:

            try:  # Включение бойлера и запись в БД
                boiler_task_on.delay()
                boiler.label = "Бойлер включен"
                boiler.value = 1
                boiler.save()
                bot.send_message("Включен бойлер")
            except Exception as exx:
                Logs.objects.create(
                    date_log=datetime.datetime.now(),
                    status="Error",
                    title_log="view Boiler",
                    description_log="Ошибка ардуино Boiler" + str(exx),
                )
            try:  # Задача на выключение бойлера
                boiler_task_off.apply_async(countdown=60 * 20)
            except Exception as exx:
                Logs.objects.create(
                    date_log=datetime.datetime.now(),
                    status="Error",
                    title_log="view Boiler",
                    description_log="Ошибка ардуино Boiler" + str(exx),
                )
        return redirect(reverse_lazy("form"))


class Rele(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Включение и выключение реле"""

    permission_required = "is_staff"

    @staticmethod
    def get(request, rele_id):
        rele_id = int(rele_id)
        if rele_id == 1:
            rele = Setting.objects.get(controller_name="light_balkon")
            if rele.value == 0:
                rele_light_balkon(1)
                rele.value = 1
                rele.save()
            else:
                rele_light_balkon(0)
                rele.value = 0
                rele.save()
        elif rele_id == 2:
            rele = Setting.objects.get(controller_name="bassein")
            if rele.value == 0:
                bassein(1)
                rele.value = 1
                rele.save()
            else:
                bassein(0)
                rele.value = 0
                rele.save()
        return redirect(reverse_lazy("form"))


class Light(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "is_staff"

    @staticmethod
    def get(request):
        bot_task_11_hour()
        return redirect(reverse_lazy("form"))


class Printer(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "is_staff"

    @staticmethod
    def get(request):
        printer = Setting.objects.get(controller_name="printer")
        if printer.value == 0:

            try:  # Включение принтера и запись в БД
                printer_on(DEBUG)
                printer.label = "printer включен"
                print("включен")
                printer.value = 1
                printer.save()
                bot.send_message("Включение принтера")
            except Exception as exx:
                Logs.objects.create(
                    date_log=datetime.datetime.now(),
                    status="Error",
                    title_log="view Boiler",
                    description_log="Ошибка ардуино Boiler" + str(exx),
                )
        else:
            try:  # Выключение принтера и запись в БД
                printer_off(DEBUG)
                printer.label = "printer выключен"
                print("выключен")
                printer.value = 0
                printer.save()
                bot.send_message("ВЫключение принтера")
            except Exception as exx:
                Logs.objects.create(
                    date_log=datetime.datetime.now(),
                    status="Error",
                    title_log="view Boiler",
                    description_log="Ошибка ардуино Boiler" + str(exx),
                )
        return redirect(reverse_lazy("form"))


class Alarms(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "is_staff"

    @staticmethod
    def get(request):
        alarms = Setting.objects.get(controller_name="alarms")
        if alarms.value == 0:
            alarms.value = 1
            alarms.label = "Извещения включены"
            alarms.save()
            bot.send_message("Извещения включены")
        else:
            alarms.value = 0
            alarms.label = "Извещения выключены"
            alarms.save()
            bot.send_message("Извещения выключены")
        return redirect(reverse_lazy("form"))


class Info(View):
    """Info"""

    @staticmethod
    def get(request):
        context = {}
        temp = DHT_MQ.objects.all().order_by("-date_t_h")[0]
        max_temp_teplica = Setting.objects.get(controller_name="max_temp_teplica")
        min_temp_teplica = Setting.objects.get(controller_name="min_temp_teplica")
        context["sensors"] = {}
        context["sensors"]["date_t_h"] = temp.date_t_h
        context["sensors"]["street_temp"] = temp.temp_street
        context["sensors"]["humidity_street"] = temp.humidity_street
        context["sensors"]["temp_voda"] = temp.temp_voda
        context["sensors"]["humidity_voda"] = temp.humidity_voda
        context["sensors"]["temp_teplica"] = temp.temp_teplica
        context["sensors"]["humidity_teplica"] = temp.humidity_teplica
        context["max_temp_teplica"] = max_temp_teplica
        context["min_temp_teplica"] = min_temp_teplica
        return render(request, "core/info.html", context)


class RefreshTestDiagram(View):
    """test refresh"""

    @staticmethod
    def get(request):
        refresh()
        calend()
        return redirect(reverse_lazy("info"))

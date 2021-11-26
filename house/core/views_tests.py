from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import Logs, Params
from .main_arduino import testing, sound

from .mail import send_test_mail
from .Telegram import bot
from myviberbot.viber_bot import send_viber
from django.conf import settings
from .analiz import button_analiz
from .main_arduino import read_ser
DEBUG = settings.PLACE
from django.http import HttpResponse, JsonResponse

import speedtest
import datetime

class Test(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        try:
            status = testing()
            Logs.objects.create(date_log = datetime.datetime.now(),
                                status = 'OK',
                                title_log = 'view Test',
                                description_log = status)
        except Exception:
            Logs.objects.create(date_log = datetime.datetime.now(),
                                status = 'Error',
                                title_log = 'view Test',
                                description_log = 'Ошибка ардуино TEST')

        return redirect(reverse_lazy('form'))


class Sound(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        try:
            context = sound()
            Logs.objects.create(date_log = datetime.datetime.now(),
                                status = 'OK',
                                title_log = 'view Sound',
                                description_log = str(context['status']))
        except Exception as err:
            Logs.objects.create(date_log = datetime.datetime.now(),
                                status = 'Error',
                                title_log = 'view Sound',
                                description_log = 'Ошибка ардуино Exeptyon' + str(err))

        return redirect(reverse_lazy('form'))


class MailTest(View):
    @staticmethod
    def get(request):

        send_test_mail('Вход на сайт', get_client_ip(request))
        Logs.objects.create(date_log = datetime.datetime.now(),
                            status = 'Test',
                            title_log = 'view Mail_test',
                            description_log = 'Send Mail')
        return redirect(reverse_lazy('form'))


class TelegramTest(View):
    @staticmethod
    def get(request):
        bot.send_message(get_client_ip(request))
        send_viber('test viber bot')

        return redirect(reverse_lazy('form'))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class Bot_task_view(View):
    @staticmethod
    def get(request):

        button_analiz(True)

        return redirect(reverse_lazy('form'))


class PingTaskView(View):
    @staticmethod
    def get(request):

        st = speedtest.Speedtest()

        download = float(st.download()) // 1024 // 1024 // 8
        upload = float(st.upload()) // 1024 // 1024 // 8
        ping = st.results.ping
        bot.send_message(f'download:{download}, upload: {upload}, ping: {ping}')
        Params.objects.create(ping=ping, download=download, upload=upload, date_t_h=datetime.now())

        return redirect(reverse_lazy('form'))


class String_arduino(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        try:
            dic_param = read_ser()  # Читает с Ардуино значения датчиков
        except Exception as err:

            Logs.objects.create(date_log=datetime.datetime.now(),
                                status='Error',
                                title_log='viev_test arduino',
                                description_log='Ошибка ардуино Exeption' + str(err))
            return
        Logs.objects.create(date_log=datetime.datetime.now(),
                            status='Error',
                            title_log='viev_test String arduino ask',
                            description_log=str(dic_param))
        return redirect(reverse_lazy('form'))

def string_to_bot(request):
    print(request.GET)
    try:
        dic_param = read_ser()  # Читает с Ардуино значения датчиков

    except Exception as err:

        Logs.objects.create(date_log=datetime.datetime.now(),
                            status='Error',
                            title_log='viev_test arduino',
                            description_log='Ошибка ардуино Exeption' + str(err))
        return
    Logs.objects.create(date_log=datetime.datetime.now(),
                        status='Error',
                        title_log='viev_test String arduino ask',
                        description_log=str(dic_param))
    print(dic_param)
    bot.send_message(dic_param)
    rp = {'data': dic_param}
    rp['status'] = 200
    return JsonResponse(rp)
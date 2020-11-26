from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect
from .models import Logs
from .main_arduino import testing, sound
from .raspberry import rele_board
import datetime
from .mail import send_test_mail
from .Telegram import bot
from django.conf import settings
DEBUG = settings.PLACE



class Test(View):
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


class Sound(View):
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


class Raspberry_rele(View):
    @staticmethod
    def get(request):
        try:
            rele_board(DEBUG)
        except Exception as err:
            Logs.objects.create(date_log=datetime.datetime.now(),
                                status='Error',
                                title_log='view raspberry_rele',
                                description_log = str(err))
        return redirect(reverse_lazy('form'))

class MailTest(View):
    @staticmethod
    def get(request):
        send_test_mail('subject test', 'message test')
        Logs.objects.create(date_log = datetime.datetime.now(),
                            status = 'Test',
                            title_log = 'view Mail_test',
                            description_log = 'Send Mail')
        return redirect(reverse_lazy('form'))


class TelegramTest(View):
    @staticmethod
    def get(request):
        bot.send_message(datetime.datetime.now())
        return redirect(reverse_lazy('form'))


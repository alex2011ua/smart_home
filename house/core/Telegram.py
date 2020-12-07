import requests
import os
from .models import Message, DHT_MQ
from dotenv import load_dotenv
from .raspberry import button
from datetime import datetime

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

token = os.getenv('TOKEN', os.environ.get('TOKEN'))
from django.conf import settings

DEBUG = settings.PLACE


class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, text, chat_id=810867568):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


bot = TelegramBot(token)


def gaz_analiz(MQ4, MQ135):
    """Если значения датчиков превышают пороговые - шлем сообщение в бот"""
    try:
        gaz = Message.objects.get(controller_name = 'gaz')
    except Exception:
        gaz = Message.objects.create(controller_name = 'gaz',
                                     date_message = datetime(2000, 1, 1))
    date_now = datetime.now()
    time_delta = (date_now - gaz.date_message) // 60  # minutes
    if time_delta.seconds > 60:
        bot.send_message('Завышены показания газовый датчиков')
        bot.send_message(f'MQ-4 - {MQ4}, MQ-135 - {MQ135}')
        gaz.date_message = date_now
        gaz.controller_name = 'gaz'
        gaz.label = "Allarm"
        gaz.value_int = MQ4 + MQ135
        gaz.save()


def button_analiz():
    """Если меняется состояние кнопка - шлем сообщение в бот"""

    date_now = datetime.now()
    context = button(DEBUG)  # загрузка состояний кнопок
    try:
        dor = Message.objects.get(controller_name = 'dor')
        garaz = Message.objects.get(controller_name = 'garaz')
    except Exception:
        dor = Message.objects.create(controller_name = 'dor',
                                     date_message = datetime(2000, 1, 1),
                                     value_int = 0)
        garaz = Message.objects.create(controller_name = 'garaz',
                                       date_message = datetime(2000, 1, 1),
                                       value_int = 0)
    if context['Garaz'] != garaz.state:
        garaz.state = context['Garaz']
        garaz.date_message = date_now
        if context['Garaz']:
            garaz.label = 'Открыт гараж'
        else:
            garaz.label = 'Закрыт гараж'
        bot.send_message(garaz.label)

    if context['Dor_street'] != dor.state:
        dor.state = context['Dor_street']
        dor.date_message = date_now
        if context['Dor_street']:
            dor.label = 'Открыта дверь'
        else:
            dor.label = 'Закрыта дверь'
        bot.send_message(dor.label)
    # Если ночью открывается дверь - шлем сообщение в бот
    if date_now.hour < 5:
        if context['Garaz'] and garaz.value_int == 0:
            bot.send_message('Открыт гараж')
            garaz.value_int = 1
        if context['Dor_street'] and dor.value_int == 0:
            bot.send_message('Открыта дверь')
            dor.value_int = 1
    if date_now.hour >= 5:
        garaz.value_int = 0
        dor.value_int = 0

    garaz.save()
    dor.save()


def temp_alert():
    """
    Проверка критичных показаний температуры
    :return:
    """
    temp = DHT_MQ.objects.all().order_by('-date_t_h')[0]  # arduino state
    if temp.temp_voda <= 1:
        bot.send_message(f"Температура в летней кухне опустилась: {temp.temp_voda}")
    if temp.temp_gaz <= 22:
        bot.send_message(f"Температура котельной: {temp.temp_voda}")

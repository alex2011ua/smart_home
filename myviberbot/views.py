from django.shortcuts import render
import os
from dotenv import load_dotenv
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from house.core.Telegram import bot
import requests # Добавим Библиотеку для отправки запросов
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)



auth_token = os.getenv('viber_token', os.environ.get('viber_token')) #!ТОКЕН СТАВИМ СВОЙ ЭТО Фейковый неживой
url = 'https://chatapi.viber.com/pa/send_message'
headers = {'X-Viber-Auth-Token': auth_token}

# ДЕКОРАТОР ДЛЯ функций и отправки
def sending(func):
    def wrapped(*args):
        return requests.post(url, json.dumps(func(*args)), headers=headers)
    return wrapped

# Отправка текста
@sending
def send_text(agent, text, track=None):
    m = dict(receiver=agent, min_api_version=2, tracking_data=track, type="text", text=text)
    return m

@csrf_exempt
def trx_bot(request):
    bot.send_message(request)
    if request.method == "GET":
        bot.send_message('GET methodd')
        viber = json.loads(request.body.decode('utf-8'))
        if viber['event'] == 'conversation_started':
            bot.send_message("Приветствую пользователя")
            conversation(viber) #Обработка запроса - обзор функции следующий абзац.
        elif viber['event'] == 'webhook':
            #print(viber)
            #print("Webhook успешно установлен")
            return HttpResponse(status=200)
        else:
            print("Это не Webhook - пробуй еще раз, или используй POSTMAN")
            return HttpResponse(status=500)
        return HttpResponse(status=200)


def conversation(viber):
    id = viber['user']['id']
    if viber['subscribed']:
        send_text(id, 'ВЫ УЖЕ ПОДПИСАНЫ')
    else:
        send_text(id, 'Что умеет этот бот?\n\nЗависит от ваших идей. Отправь мне что угодно и присоединяйся...')

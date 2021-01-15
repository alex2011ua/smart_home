from django.shortcuts import render
from house.core.mail import send_test_mail
from .ip import get_client_ip, ip_info
import json
from house.core.Telegram import bot

import datetime

def index(request):
    context = {'date': datetime.datetime.now()}

    return render(request, "start/start.html", context)


def get_bot_message(request):
    bot.send_message('Resive message')
    try:
        data = json.loads(request.body.decode())
        bot.send_message(data)
    except ValueError as arr:
        print('Value Error')
        bot.send_message(arr)

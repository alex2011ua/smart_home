from django.shortcuts import render

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from house.core.Telegram import bot

@csrf_exempt
def trx_bot(request):
    bot.send_message(request.method)
    if request.method == "POST":
        bot.send_message('method - Post')
        viber = json.loads(request.body.decode('utf-8'))
        if viber['event'] == 'webhook':
            print(viber)
            bot.send_message(viber)
            bot.send_message('Webhook успешно установлен')
            print("Webhook успешно установлен") # - печатаем сообщение в
# консоль об успешном соотвещ событии установки webhook
            return HttpResponse(status=200)
        else:
            bot.send_message('Это не Webhook - пробуй еще раз, или используй POSTMAN ')
            print("Это не Webhook - пробуй еще раз, или используй POSTMAN")
            return HttpResponse(status=500)
        return HttpResponse(status=200)
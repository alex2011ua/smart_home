from django.shortcuts import render

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def trx_bot(request):
    if request.method == "POST":
        viber = json.loads(request.body.decode('utf-8'))
        if viber['event'] == 'webhook':
            print(viber)
            print("Webhook успешно установлен") # - печатаем сообщение в
# консоль об успешном соотвещ событии установки webhook
            return HttpResponse(status=200)
        else:
            print("Это не Webhook - пробуй еще раз, или используй POSTMAN")
            return HttpResponse(status=500)
        return HttpResponse(status=200)
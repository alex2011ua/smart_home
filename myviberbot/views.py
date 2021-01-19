from django.shortcuts import render


from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from house.core.Telegram import bot

from .viber_bot import viber
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
from viberbot.api.messages.text_message import TextMessage

@csrf_exempt
def trx_bot(request):
    try:

        bot.send_message(request.method)
        bot.send_message(request.headers)
        bot.send_message([request.GET.items()].join(','))
        if not viber.verify_signature(request.body(), request.headers.get(
                'X-Viber-Content-Signature')):
            bot.send_message('verify_signature False')
            return HttpResponse(status=403)
        bot.send_message('verify_signature True')
        # this library supplies a simple way to receive a request object
        viber_request = viber.parse_request(request.get_data())
        bot.send_message(viber_request)
        if isinstance(viber_request, ViberMessageRequest):
            message = viber_request.message
            bot.send_message(message)
            viber.send_messages(viber_request.sender.id, [
                message
            ])
        elif isinstance(viber_request, ViberSubscribedRequest):
            viber.send_messages(viber_request.get_user.id, [
                TextMessage(text="thanks for subscribing!")
            ])
        elif isinstance(viber_request, ViberFailedRequest):
            bot.send_message("client failed receiving message. failure: {0}".format(viber_request))

        return HttpResponse(status=200)
    except Exception as err:
        bot.send_message(err)




"""
if request.method == "GET":
    bot.send_message('GET methodd')
    viber = json.loads(request.body.decode('utf-8'))
    if viber['event'] == 'conversation_started':
        bot.send_message("Приветствую пользователя")
        conversation(viber) #Обработка запроса - обзор функции следующий абзац.

    elif viber['event'] == 'webhook':
        # print(viber)
        # print("Webhook успешно установлен")
        return HttpResponse(status=200)
    elif viber['event'] == 'message':
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
"""
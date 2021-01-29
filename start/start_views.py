from django.shortcuts import render
from house.core.mail import send_test_mail
from .ip import get_client_ip, ip_info
import json
from house.core.Telegram import bot
from django.views import View
from .avto_api import get_list_car

class IndexView(View):
    @staticmethod
    def get(request):
        return render(request, "start/start.html", {})

    @staticmethod
    def post(request):
        s_yers = request.POST.get('s_yers')
        po_yers = request.POST.get('po_yers')
        price_ot = request.POST.get('price_ot')
        price_do = request.POST.get('price_do')
        toplivo = request.POST.getlist('toplivo')
        print(toplivo)
        print(s_yers, po_yers, price_ot, price_do)
        zapros = get_list_car({
            's_yers': [s_yers],
            'po_yers': [po_yers],
            'price_ot': price_ot,
            'price_do': price_do,
            'type': toplivo,
        })
        count = zapros['count_avto']
        return render(request, "start/start.html", {'count': count})

def get_bot_message(request):
    bot.send_message('Resive message')
    try:
        data = json.loads(request.body.decode())
        bot.send_message(data)
    except ValueError as arr:
        print('Value Error')
        bot.send_message(arr)

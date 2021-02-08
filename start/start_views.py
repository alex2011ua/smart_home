from django.shortcuts import render
from house.core.mail import send_test_mail
from .ip import get_client_ip, ip_info
import json
from house.core.Telegram import bot
from django.views import View
from .avto_api import get_list_car, make_baza_avto
import time

class IndexView(View):
    @staticmethod
    def get(request):
        context = {
            's_yers': [2016],
            'po_yers': [2018],
            'price_ot': 10000,
            'price_do': 10500,
            'type': ['1', '4', '6'],
            'gearbox': ['2', '3']
        }

        if 's_yers' in request.GET:
            context.update({'s_yers': [request.GET['s_yers']]})
        if 'po_yers' in request.GET:
            context.update({'po_yers': [request.GET['po_yers']]})
        if 'price_ot' in request.GET:
            context.update({'price_ot': request.GET['price_ot']})
        if 'price_do' in request.GET:
            context.update({'price_do': request.GET['price_do']})

        if 'price_ot' in request.GET:
            context['type'] = []
            context['gearbox'] = []
            if 'benz' in request.GET:
                context['type'].append('1')
            if 'dizel' in request.GET:
                context['type'].append('2')
            if 'gaz' in request.GET:
                context['type'].append('4')
            if 'elektro' in request.GET:
                context['type'].append('6')

            if 'mex' in request.GET:
                context['gearbox'].append('1')
            if 'avtomat' in request.GET:
                context['gearbox'].append('2')
            if 'tip' in request.GET:
                context['gearbox'].append('3')

        zapros = get_list_car(context)
        if zapros['status'] == 429:
            context['error'] = 'Cлишком много запросов, попробуйте через час!'
        elif zapros['status'] != 200:
            context['error'] = zapros['status']
        else:

            count = zapros['count_avto']
            context['count'] = count

        return render(request, "start/start.html", context)

class AnalizView(View):
    @staticmethod
    def get(request):
        context = {

        }

        if 's_yers' in request.GET:
            context.update({'s_yers': [request.GET['s_yers']]})
        if 'po_yers' in request.GET:
            context.update({'po_yers': [request.GET['po_yers']]})
        if 'price_ot' in request.GET:
            context.update({'price_ot': request.GET['price_ot']})
        if 'price_do' in request.GET:
            context.update({'price_do': request.GET['price_do']})

        if 'price_ot' in request.GET:
            context['type'] = []
            context['gearbox'] = []
            if 'benz' in request.GET:
                context['type'].append('1')
            if 'dizel' in request.GET:
                context['type'].append('2')
            if 'gaz' in request.GET:
                context['type'].append('4')
            if 'elektro' in request.GET:
                context['type'].append('6')

            if 'mex' in request.GET:
                context['gearbox'].append('1')
            if 'avtomat' in request.GET:
                context['gearbox'].append('2')
            if 'tip' in request.GET:
                context['gearbox'].append('3')
        return render(request, "start/cart.html", context)


def get_bot_message(request):
    bot.send_message('Resive message')
    try:
        data = json.loads(request.body.decode())
        bot.send_message(data)
    except ValueError as arr:
        print('Value Error')
        bot.send_message(arr)

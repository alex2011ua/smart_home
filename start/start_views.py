from django.shortcuts import render
from house.core.mail import send_test_mail
from .ip import get_client_ip, ip_info
import json
from start.models import Avto
from house.core.Telegram import bot
from django.views import View
from .avto_api import get_list_car, make_baza_avto
import json


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
        return render(request, "start/start.html", context)

class AnalizView(View):
    @staticmethod
    def get(request):
        param_avto = {}
        if 's_yers' in request.GET:
            param_avto.update({'s_yers': [request.GET['s_yers']]})
        if 'po_yers' in request.GET:
            param_avto.update({'po_yers': [request.GET['po_yers']]})
        if 'price_ot' in request.GET:
            param_avto.update({'price_ot': request.GET['price_ot']})
        if 'price_do' in request.GET:
            param_avto.update({'price_do': request.GET['price_do']})

        if 'price_ot' in request.GET:
            param_avto['type'] = []
            param_avto['gearbox'] = []
            if 'benz' in request.GET:
                param_avto['type'].append('1')
            if 'dizel' in request.GET:
                param_avto['type'].append('2')
            if 'gaz' in request.GET:
                param_avto['type'].append('4')
            if 'elektro' in request.GET:
                param_avto['type'].append('6')

            if 'mex' in request.GET:
                param_avto['gearbox'].append('1')
            if 'avtomat' in request.GET:
                param_avto['gearbox'].append('2')
            if 'tip' in request.GET:
                param_avto['gearbox'].append('3')

        zapros = get_list_car(param_avto)
        count = zapros['count_avto']
        car_list = zapros['list_cars']
        count_avto_in = len(car_list)
        car_list_split = split(car_list)
        context = {
            'param_avto': json.dumps(param_avto, ensure_ascii = False),
            'count_all_avto': count,
            'car_list': car_list_split,
            'count_avto_in': count_avto_in,
        }

        return render(request, "start/cart.html", context)


def get_bot_message(request):
    bot.send_message('Resive message')
    try:
        data = json.loads(request.body.decode())
        bot.send_message(data)
    except ValueError as arr:
        print('Value Error')
        bot.send_message(arr)


def split(arr, size=10):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def clear_baze(request):
    car_baze = Avto.objects.all()
    for car in car_baze:
        car.delete()
    context = {
        's_yers': [2016],
        'po_yers': [2018],
        'price_ot': 10000,
        'price_do': 10500,
        'type': ['1', '4', '6'],
        'gearbox': ['2', '3']
    }
    return render(request, "start/start.html", context)

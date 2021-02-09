from django.http import HttpResponse, JsonResponse
from .avto_api import get_list_car, make_baza_avto, analiz_avto
from django.shortcuts import render
import json


def ajax(request):
    t = []
    g = []
    for item in request.POST:
        if item == 'benz':
            t.append(1)
        elif item == 'dizel':
            t.append(2)
        elif item == 'gaz':
            t.append(4)
        elif item == 'electro':
            t.append(4)
        elif item == 'mex':
            g.append(1)
        elif item == 'avtomat':
            g.append(2)
        elif item == 'tip':
            g.append(3)
    params = {
        's_yers': [request.POST.get('s_yers'),],
        'po_yers': [request.POST.get('po_yers'),],
        'price_ot': int(request.POST.get('price_ot')),
        'price_do': int(request.POST.get('price_do')),
        'type': t,
        'gearbox': g,
    }
    list_car = get_list_car(params)
    return HttpResponse(list_car['count_avto'])


def ajax_analiz(request):
    avtos = request.POST.getlist('list_avto[]')
    for avto in avtos:
        status = analiz_avto(avto)
        if status['status'] != 200:
            print(status['status'])
    return JsonResponse({'status': 200})


def ajax_zvit(request):
    avtos = request.POST.getlist('baza[]')
    sort_list = make_baza_avto(avtos)

    return render(request, "start/ca.html", sort_list)

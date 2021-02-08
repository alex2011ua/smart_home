from django.http import HttpResponse
from .avto_api import get_list_car
from django.shortcuts import render
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
    print(request.POST)
    import time
    time.sleep(70)
    avtos = [
        ['asd30',23,23,3,4,5,6,34],
        ['asd33', 23, 23, 3, 4, 5, 6, 34]
             ]
    context = {'avtos': avtos}
    return render(request, "start/ca.html", context)

from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Setting
from django.core.exceptions import ObjectDoesNotExist
from .main_arduino import V24_arduino, off_klapan, on_klapan
from .tasks import poliv


class Poliv(View):
    @staticmethod
    def get(request):
        poliv_all = get_status_poliv()
        poliv = Setting.objects.get(controller_name='poliv')
        context = {
            'poliv': poliv,
            'poliv_all': poliv_all
            }

        return render(request, 'core/poliv_index.html', context)

    @staticmethod
    def post(request):
        #print(request.POST)  # <QueryDict: {'off': ['poliv_pesochnica']}>
        if request.POST.get('off'):
            controller_name = request.POST['off']
            print(controller_name)
            of_poliv = Setting.objects.get(controller_name=controller_name)
            of_poliv.label = 'выключен'
            off_klapan(controller_name)
            of_poliv.save()

            return JsonResponse({"status": 200})
        if request.POST.get('on'):
            controller_name = request.POST['on']
            on_poliv = Setting.objects.get(controller_name=controller_name)
            on_poliv.label = 'включен'
            on_klapan(controller_name)
            on_poliv.save()
            return JsonResponse({"status": 200})


def get_status_poliv():
    V24, created = Setting.objects.get_or_create(
        controller_name='V24',
        defaults={'label': 'Выключен', 'value': 0})
    try:
        poliv_elki = Setting.objects.get(controller_name='poliv_elki')
        poliv_garaz = Setting.objects.get(controller_name='poliv_garaz')
        poliv_pesochnica = Setting.objects.get(controller_name='poliv_pesochnica')
        poliv_teplica = Setting.objects.get(controller_name='poliv_teplica')
        poliv_sad = Setting.objects.get(controller_name='poliv_sad')
        poliv_strawberry = Setting.objects.get(controller_name='poliv_strawberry')
    except ObjectDoesNotExist:
        poliv_elki = Setting.objects.create(controller_name='poliv_elki', label='выключен', value=0)
        poliv_garaz = Setting.objects.create(controller_name='poliv_garaz', label='выключен', value=0)
        poliv_pesochnica = Setting.objects.create(controller_name='poliv_pesochnica', label='выключен', value=0)
        poliv_teplica = Setting.objects.create(controller_name='poliv_teplica', label='выключен', value=0)
        poliv_sad = Setting.objects.create(controller_name='poliv_sad', label='выключен', value=0)
        poliv_strawberry = Setting.objects.create(controller_name='poliv_strawberry', label='выключен', value=0)
    poliv_all = {}

    p = [
        V24,
        poliv_elki,
        poliv_garaz,
        poliv_pesochnica,
        poliv_teplica,
        poliv_sad,
        poliv_strawberry,
    ]
    for item in p:
        poliv_all[item.controller_name] = item
    return poliv_all


def poliv_on_of(request):
    poliv = Setting.objects.get(controller_name='poliv')
    if poliv.label == 'включен':
        poliv.label = 'выключен'
    else:
        poliv.label = 'включен'
    poliv.save()
    return redirect(reverse_lazy('poliv_index'))

def ch_value_time(request):
    value_time = request.GET.get('value')
    poliv = Setting.objects.get(controller_name='poliv')
    poliv.value = value_time

    poliv.save()
    return redirect(reverse_lazy('poliv_index'))

def V24(request):
    V24 = Setting.objects.get(controller_name='V24')
    if V24.label == 'включен':
        V24.label = 'выключен'
        V24_arduino(0)
    else:
        V24.label = 'включен'
        V24_arduino(1)
    V24.save()
    return redirect(reverse_lazy('poliv_index'))

def zapusk_poliva(r):
    poliv.delay(force=True)

    return redirect(reverse_lazy('poliv_index'))
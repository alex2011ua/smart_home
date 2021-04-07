from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Setting
from django.core.exceptions import ObjectDoesNotExist


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
        print(request.POST)  # print all url params
        if request.POST.get('off'):
            of_poliv = Setting.objects.get(controller_name=request.POST['off'])
            of_poliv.value = 0
            of_poliv.label = 'выключен'
            of_poliv.save()
            return JsonResponse({"status": 200})
        if request.POST.get('on'):
            on_poliv = Setting.objects.get(controller_name=request.POST['on'])
            on_poliv.value = 1
            on_poliv.label = 'включен'
            on_poliv.save()
            return JsonResponse({"status": 200})


def get_status_poliv():
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
    if poliv.value:
        poliv.value = 0
        poliv.label = 'выключен'
    else:
        poliv.value = 1
        poliv.label = 'включен'
    poliv.save()
    return redirect(reverse_lazy('poliv_index'))
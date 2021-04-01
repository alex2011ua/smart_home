from django.views import View
from django.shortcuts import render
from .models import Setting
from django.core.exceptions import ObjectDoesNotExist


class Poliv(View):
    @staticmethod
    def get(request):
        poliv_all = get_status_poliv()
        poliv = Setting.objects.get(controller_name='poliv')
        context = {'poliv': poliv}

        return render(request, 'core/poliv_index.html', context)

    @staticmethod
    def post(request):
        print(request.POST)  # print all url params

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
    poliv_all = []
    list(map(lambda x: poliv_all.append(x),
             [
                 poliv_elki,
                 poliv_garaz,
                 poliv_pesochnica,
                 poliv_teplica,
                 poliv_sad,
                 poliv_strawberry,
             ]
             ))
    return poliv_all


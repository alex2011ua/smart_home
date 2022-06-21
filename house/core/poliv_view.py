from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .main_arduino import V24_arduino, arduino_pshik, off_klapan, on_klapan
from .models import Setting
from .tasks import poliv

import logging


logger = logging.getLogger("django")


class Poliv(View):
    @staticmethod
    def get(request):
        poliv_all = get_status_poliv()
        poliv = Setting.objects.get(controller_name="poliv")
        limit, count = Setting.objects.get_or_create(controller_name="limit_rain",
                                               defaults={"label": "limits of the rain(mm)", "value": 5})
        start_water_time, count = Setting.objects.get_or_create(controller_name="start_water_time",
                                               defaults={"label": "start_water_time (min)", "value": 40})
        watering_pesochnica, count = Setting.objects.get_or_create(controller_name="watering_pesochnica", defaults={
            "label": "poliv pesochnici", "value": 0
        })
        watering_trava, count = Setting.objects.get_or_create(controller_name="watering_trava", defaults={
            "label": "poliv trava", "value": 0
        })
        watering_sad, count = Setting.objects.get_or_create(controller_name="watering_sad", defaults={
            "label": "poliv sad", "value": 0
        })
        watering_raspberry, count = Setting.objects.get_or_create(controller_name="watering_raspberry", defaults={
            "label": "poliv raspberry", "value": 0
        })

        context = {"poliv": poliv,
                   "poliv_all": poliv_all,
                   "limit": limit,
                   "start_water_time": start_water_time,
                   "watering_pesochnica": watering_pesochnica,
                   "watering_trava": watering_trava,
                   "watering_sad": watering_sad,
                   "watering_raspberry": watering_raspberry,
                   }

        return render(request, "core/poliv_index.html", context)

    @staticmethod
    def post(request):
        # print(request.POST)  # <QueryDict: {'off': ['poliv_pesochnica']}>
        if request.POST.get("off"):
            controller_name = request.POST["off"]
            print(controller_name)
            of_poliv = Setting.objects.get(controller_name=controller_name)
            of_poliv.label = "выключен"
            off_klapan(controller_name)
            of_poliv.save()

            return JsonResponse({"status": 200})
        if request.POST.get("on"):
            controller_name = request.POST["on"]
            on_poliv = Setting.objects.get(controller_name=controller_name)
            print(controller_name)
            on_poliv.label = "включен"
            on_klapan(controller_name)
            on_poliv.save()
            return JsonResponse({"status": 200})


def get_status_poliv():
    V24, created = Setting.objects.get_or_create(
        controller_name="V24", defaults={"label": "Выключен", "value": 0}
    )

    pshik = Setting.objects.get(controller_name="pshik")
    poliv_elki = Setting.objects.get(controller_name="poliv_elki")
    poliv_garaz = Setting.objects.get(controller_name="poliv_garaz")
    poliv_pesochnica = Setting.objects.get(controller_name="poliv_pesochnica")
    poliv_teplica = Setting.objects.get(controller_name="poliv_teplica")
    poliv_sad = Setting.objects.get(controller_name="poliv_sad")
    poliv_strawberry = Setting.objects.get(controller_name="poliv_strawberry")
    poliv_trava, created = Setting.objects.get_or_create(
        controller_name="poliv_trava", defaults={"label": "выключен", "value": 0}
    )
    poliv_all = {}

    p = [
        pshik,
        V24,
        poliv_elki,
        poliv_garaz,
        poliv_pesochnica,
        poliv_teplica,
        poliv_sad,
        poliv_strawberry,
        poliv_trava
    ]
    for item in p:
        poliv_all[item.controller_name] = item
    return poliv_all


def poliv_on_of(request):
    poliv = Setting.objects.get(controller_name="poliv")
    if poliv.label == "включен":
        poliv.label = "выключен"
    else:

        poliv.label = "включен"
    poliv.save()
    logger.info(poliv.label)
    return redirect(reverse_lazy("poliv_index"))


def ch_value_time(request):
    value_time = request.GET.get("value")
    poliv = Setting.objects.get(controller_name="poliv")
    poliv.value = value_time
    poliv.save()
    limit = Setting.objects.get(controller_name='limit_rain')
    limit.value = request.GET.get("limit_value")
    limit.save()
    start_water_time = Setting.objects.get(controller_name="start_water_time")
    start_water_time.value = request.GET.get("start_water_time")
    start_water_time.save()
    watering_pesochnica = request.GET.get("watering_pesochnica")
    watering_trava = request.GET.get("watering_trava")
    watering_sad = request.GET.get("watering_sad")
    watering_raspberry = request.GET.get("watering_raspberry")

    pesochnica = Setting.objects.get(controller_name="watering_pesochnica")
    pesochnica.value = 1 if watering_pesochnica == "on" else 0
    pesochnica.save()
    trava = Setting.objects.get(controller_name="watering_trava")
    trava.value = 1 if watering_trava == "on" else 0
    trava.save()
    sad = Setting.objects.get(controller_name="watering_sad")
    sad.value = 1 if watering_sad == "on" else 0
    sad.save()
    raspberry = Setting.objects.get(controller_name="watering_raspberry")
    raspberry.value = 1 if watering_raspberry == "on" else 0
    raspberry.save()

    return redirect(reverse_lazy("poliv_index"))


def V24(request):
    V24 = Setting.objects.get(controller_name="V24")
    if V24.label == "включен":
        V24.label = "выключен"
        V24_arduino(0)
    else:
        V24.label = "включен"
        V24_arduino(1)
    V24.save()
    return redirect(reverse_lazy("poliv_index"))


def zapusk_poliva(r):
    poliv.delay(force=True)

    return redirect(reverse_lazy("poliv_index"))


def pshik(request):
    pshik = Setting.objects.get(controller_name="pshik")
    if pshik.label == "включен":
        pshik.label = "выключен"
        arduino_pshik(0)
    else:
        pshik.label = "включен"
        arduino_pshik(1)
    pshik.save()
    return redirect(reverse_lazy("poliv_index"))

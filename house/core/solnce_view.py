from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Setting
from django.core.exceptions import ObjectDoesNotExist


class Solnce(View):
    @staticmethod
    def get(request):
        context = {}
        return render(request, 'core/solnce.html', context)

    @staticmethod
    def post(request):
        #print(request.POST)  # <QueryDict: {'off': ['poliv_pesochnica']}>
        if request.POST.get('off'):
            of_poliv = Setting.objects.get(controller_name=request.POST['off'])
            of_poliv.label = 'выключен'
            of_poliv.save()
            return JsonResponse({"status": 200})
        if request.POST.get('on'):
            on_poliv = Setting.objects.get(controller_name=request.POST['on'])
            on_poliv.label = 'включен'
            on_poliv.save()
            return JsonResponse({"status": 200})


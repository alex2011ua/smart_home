import os

from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
DEBUG = settings.DEBUG

from .models import Setting, Temp1, Logs
from .form import ControllerForm

from django.http import HttpResponse

from .main_arduino import restart_cam, read_ser
from .raspberry import raspberry
from .weather_rain import weather_now
from house.core.tasks import restart_cam_task, weather_task, arduino_task
import datetime




class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        context['data'] = raspberry(DEBUG)  # state raspberry
        temp = Temp1.objects.all().order_by('-id')[0]  # arduino state

        context['data']['temp'] = temp.temp
        context['data']['humidity'] = temp.humidity
        context['data']['date_temp'] = temp.date_temp

        context['time'] = datetime.datetime.now()
        context.update(weather_now())

        logs = Logs.objects.all().order_by('-date_log')[0:20]
        context['logs'] = logs
        return context

    def get_initial(self):
        return {}

    def form_valid(self, form):
        return super(ControllerView, self).form_valid(form)


class RestartCam(View):
    @staticmethod
    def get(request):
        q = restart_cam_task.delay()
           # отключение реле на 10 сек
        return redirect(reverse_lazy('form'))

class Env(View):
    @staticmethod
    def get(request):
        arduino_task()
        return redirect(reverse_lazy('form'))

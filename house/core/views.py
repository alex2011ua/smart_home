import os

from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Setting
from .form import ControllerForm

from django.http import HttpResponse

from .main_arduino import restart_cam, read_ser
from .raspberry import raspberry
DEBUG = settings.DEBUG





class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        context['data'] = raspberry(DEBUG)  # state raspberry
        context['data']['arduino_status'] = read_ser(DEBUG)
        return context

    def get_initial(self):
        return {}

    def form_valid(self, form):
        return super(ControllerView, self).form_valid(form)


class RestartCam(View):
    @staticmethod
    def get(request):
        restart_cam(DEBUG)   # отключение реле на 10 сек
        return redirect(reverse_lazy('form'))

class Env(View):
    @staticmethod
    def get(request):
        env = os.environ.get('test_env')

        return HttpResponse(content = f'--{env}-- запись в переменной, --{DEBUG}-- значение дебаг', status = 200)

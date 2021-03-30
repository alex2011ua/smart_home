from django.views import View
from django.shortcuts import render
from .models import Setting


class  Poliv(View):
    @staticmethod
    def get(request):
        poliv = Setting.objects.get(controller_name='poliv')
        context = {'poliv': poliv}
        return render(request, 'core/poliv_index.html', context)

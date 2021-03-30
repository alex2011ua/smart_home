from django.views import View
from django.shortcuts import render

class  Poliv(View):
    @staticmethod
    def get(request):
        context = {}
        return render(request, 'core/poliv_index.html', context)

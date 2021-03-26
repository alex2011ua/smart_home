from django.shortcuts import render


from house.core.Telegram import bot
from django.views import View



class IndexView(View):
    @staticmethod
    def get(request):

        context = {
            's_yers': [2016],
            'po_yers': [2018],
            'price_ot': 10000,
            'price_do': 10500,
            'type': ['1', '4', '6'],
            'gearbox': ['2', '3']
        }
        return render(request, "start/index.html", context)

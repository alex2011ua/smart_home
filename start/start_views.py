from django.shortcuts import render

import datetime

def index(request):
    context = {'date': datetime.datetime.now()}

    return render(request, "start.html", context)

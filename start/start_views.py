from django.shortcuts import render
from house.core.mail import send_test_mail
from .ip import get_client_ip, ip_info


import datetime

def index(request):
    context = {'date': datetime.datetime.now()}

    return render(request, "start/start.html", context)

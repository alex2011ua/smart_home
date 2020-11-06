"""coursera_house URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from house.core.views import ControllerView, RestartCam, Env, ResetArduino

urlpatterns = [
    url(r'^$', ControllerView.as_view(), name='form'),
    url(r'^restart/$', RestartCam.as_view(), name='restart_cam'),
    url(r'^env/$', Env.as_view(), name = 'env'),
    url(r'^reset_arduino/$', ResetArduino.as_view(), name = 'reset_arduino'),
]

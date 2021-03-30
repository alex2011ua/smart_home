from django.conf.urls import url
from .poliv_view import Poliv
urlpatterns = [
    url(r'index/$', Poliv.as_view(), name='poliv_index'),

]

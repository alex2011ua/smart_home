from django.conf.urls import url
from .poliv_view import Poliv, poliv_on_of, ch_value_time, V24


urlpatterns = [
    url(r'index/$', Poliv.as_view(), name='poliv_index'),
    url(r'on_of_poliv/$', poliv_on_of, name='poliv_on_of'),
    url(r'ch_value_time/$', ch_value_time, name='ch_value_time'),
    url(r'V24/$', V24, name='V24'),
]

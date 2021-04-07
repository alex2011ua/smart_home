from django.conf.urls import url
from .poliv_view import Poliv, poliv_on_of


urlpatterns = [
    url(r'index/$', Poliv.as_view(), name='poliv_index'),
    url(r'on_of_poliv/$', poliv_on_of, name='poliv_on_of')

]

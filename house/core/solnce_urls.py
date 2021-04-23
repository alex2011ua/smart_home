from django.conf.urls import url
from .solnce_view import Solnce


urlpatterns = [
    url(r'$', Solnce.as_view(), name='solnce'),


]

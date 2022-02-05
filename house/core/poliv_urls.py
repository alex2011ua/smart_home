from django.conf.urls import url

from .poliv_view import (V24, Poliv, ch_value_time, poliv_on_of, pshik,
                         zapusk_poliva)

urlpatterns = [
    url(r"index/$", Poliv.as_view(), name="poliv_index"),
    url(r"on_of_poliv/$", poliv_on_of, name="poliv_on_of"),
    url(r"ch_value_time/$", ch_value_time, name="ch_value_time"),
    url(r"V24/$", V24, name="V24"),
    url(r"zapusk_poliva/$", zapusk_poliva, name="zapusk_poliva"),
    url(r"psik/$", pshik, name="pshik"),
]

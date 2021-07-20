from django.urls import path
from english.views import index, settings, clear, list_words, E_R, R_E, Random


urlpatterns = [
    path('', index, name='english_index'),
    path('settings/', settings, name='settings'),
    path('clear/', clear, name='clear'),
    path('list_words/', list_words, name='list_words'),
    path('e_r/', E_R.as_view(), name='e_r'),
    path('r_e/', R_E.as_view(), name='r_e'),
    path('random/', Random.as_view(), name='random'),

]
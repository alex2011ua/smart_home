from django.urls import path
from english_2.views import index, Settings, clear, list_words, E_R, R_E, Random, mod, SearchWord, word_update, CompareWords

app_name = 'level_2'
urlpatterns = [
    path('', index, name='english_index'),
    path('settings/', Settings.as_view(), name='settings'),
    path('clear/', clear, name='clear'),
    path('list_words/', list_words, name='list_words'),
    path('list_words/<int:id>/', word_update, name='update'),


    path('e_r/mod/', mod),
    path('e_r/', E_R.as_view(), name='e_r'),
    path('r_e/mod/', mod),
    path('r_e/', R_E.as_view(), name='r_e'),
    path('random/', Random.as_view(), name='random'),
    path('search/', SearchWord.as_view(), name='SearchWord'),
    path('compare/', CompareWords.as_view(), name='CompareWords'),
]
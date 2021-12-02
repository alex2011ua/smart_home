from django.urls import path
from english.views import index, Settings, clear_control, clear_learned, list_words, E_R, R_E, mod, SearchWord, word_update, CompareWords, \
    test, word_delete
from english.view_game import GenrundGame


app_name = 'english'
urlpatterns = [
    path('', index, name='english_index'),
    path('settings/', Settings.as_view(), name='settings'),
    path('clear/', clear_control, name='clear'),
    path('clear_learned/', clear_learned, name='clear_learned'),
    path('test/', test, name='test'),
    path('list_words/', list_words, name='list_words'),
    path('list_words/<int:id>/', word_update, name='update'),
    path('list_words/del/<int:id>/', word_delete, name='delete'),


    path('e_r/mod/', mod),
    path('e_r/', E_R.as_view(), name='e_r'),
    path('r_e/mod/', mod),
    path('r_e/', R_E.as_view(), name='r_e'),

    path('search/', SearchWord.as_view(), name='SearchWord'),
    path('compare/', CompareWords.as_view(), name='CompareWords'),
    path('game_gerund/', GenrundGame.as_view(), name='GenundGame'),

]
from django.urls import include, path
from django.contrib.auth import views
from . import start_views
import os
from myviberbot.views import trx_bot

token = os.getenv('TOKEN', os.environ.get('TOKEN'))

urlpatterns = [
    path('house/', include('house.urls')),
    path('', start_views.index, name='index'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('{}/'.format(token), start_views.get_bot_message, name='get_bot_message'),
    path('webhook2020/', trx_bot),
]
from django.urls import include, path
from django.contrib.auth import views
from myviberbot.views import trx_bot
from .start_views import IndexView



urlpatterns = [
    path('house/', include('house.urls')),
    path('avto/', include('selection_avto.urls')),
    path('', IndexView.as_view(), name='index'),

    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),

    path('webhook2020/', trx_bot),

    path('english/', include('english.urls')),
]
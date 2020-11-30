from django.urls import include, path
from django.contrib.auth import views
from . import start_views

urlpatterns = [
    path('house/', include('house.urls')),
    path('', start_views.index, name='index'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),

]
from django.shortcuts import render
from django.shortcuts import redirect
from house.core.Telegram import bot
from django.views import View
from house.settings import api_key_tmdb
from .registration_form import UserRegistrationForm
import requests
from django.contrib.auth.models import User
from english.models import WordParams


class IndexView(View):
    @staticmethod
    def get(request):

        context = {
            's_yers': [2016],
            'po_yers': [2018],
            'price_ot': 10000,
            'price_do': 10500,
            'type': ['1', '4', '6'],
            'gearbox': ['2', '3']
        }
        return render(request, "start/index.html", context)


class VideoRating(View):
    @staticmethod
    def get(request):
        payload = {'api_key': api_key_tmdb,
                   'primary_release_year': '2021',
                   'sort_by': 'vote_average.desc',
                   'certification': 'R',
                   }
        r = requests.get('https://api.themoviedb.org/3/discover/movie', params=payload)
        print(r.url)
        list_films = r.json()
        for film in list_films['results']:
            print(film['title'], film['popularity'], film['vote_average'], film['vote_count'])
        return

class RegisterView(View):
    @staticmethod
    def get(request):
        form = UserRegistrationForm()
        return render(request, "registration/registration.html", {'form': form})


    @staticmethod
    def post(request):
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')
        user_mail = request.POST.get('user_mail')
        # Создайте пользователя и сохраните его в базе данных
        user = User.objects.create_user(user_name, user_mail, user_password)
        WordParams.objects.create(
            user=user
        )

        return redirect('login')


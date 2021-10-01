from django.shortcuts import render
from house.core.Telegram import bot
from django.views import View
from house.settings import api_key_tmdb

import requests

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
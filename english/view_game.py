from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .models import Words

class GenrundGame(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        return render(request, 'english/play_gerund.html')

    @staticmethod
    def post(request):
        content = []
        words_all = Words.objects.filter(lesson=88)
        for word in words_all:
            d_word = {
                'english': word.english,
                'gerund': word.russian,
                'id': word.id,
                      }
            content.append(d_word)
        return JsonResponse(content, safe=False)
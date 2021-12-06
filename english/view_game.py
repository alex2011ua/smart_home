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
        try:
            for _word in words_all:
                word, buttons = _word.english.split('-',1)
                answer, russian = _word.russian.split('-',1)
                buttons = buttons.split(',')
                d_word = {
                    'word': word,
                    'buttons': buttons,
                    'answer': answer,
                    'russian': russian,
                    'id': _word.id,
                          }
                content.append(d_word)
        except Exception as arr:
            print(arr.text)
            print (_word)

        return JsonResponse(content, safe=False)
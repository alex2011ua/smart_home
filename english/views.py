from django.shortcuts import render, redirect
from django.views import View
from .form import LoadWordForm, LoadWordsForm
from .models import Words
from django.http import JsonResponse

def index(request):
    return render(request, 'english/base_english.html')


def settings(request):
    if request.method == 'GET':
        form_list_words = LoadWordsForm()
        form_word = LoadWordForm()
        return render(request, 'english/settings.html', {'form_word': form_word, 'form_list_words': form_list_words})
    if request.method == 'POST':
        if request.POST.get('english'):
            form = LoadWordForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('settings')
        if request.FILES.get('file'):
            file_ = request.FILES.get('file').read()
            content = file_.decode('utf-8').split('\r\n')
            for item in content:
                w = item.split(',')
                Words.objects.create(english=w[0].strip(), russian=w[1].strip())
        return redirect('settings')


def clear(request):
    all = Words.objects.all()
    for item in all:
        item.delete()
    return redirect('settings')


def list_words(request):
    all = Words.objects.all()
    return render(request, 'english/list_words.html', {'words': all})


class E_R(View):
    @staticmethod
    def get(request):
        return render(request, 'english/e-r.html')

    @staticmethod
    def post(request):
        all = Words.objects.all()
        context = {}
        for item in all:
            context[item.english] = item.russian
        return JsonResponse(context)



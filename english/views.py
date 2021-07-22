from django.shortcuts import render, redirect
from django.views import View
from .form import LoadWordForm, LoadWordsForm, WordsParamForm
from .models import Words, WordParams
from django.http import JsonResponse

def index(request):
    if request.method == 'GET':
        try:
            params = WordParams.objects.get(id=1)
        except:
            params = WordParams.objects.create(id=1)
        form_word_param = WordsParamForm(instance=params)
        return render(request, 'english/base_english.html', {'form_word_param': form_word_param})
    if request.method == 'POST':
        params = WordParams.objects.get()
        form = WordsParamForm(request.POST, instance=params)
        if form.is_valid():
            form.save()
        return redirect('english_index')

def settings(request):
    if request.method == 'GET':
        count = Words.objects.all().count()
        form_list_words = LoadWordsForm()
        form_word = LoadWordForm()
        return render(request, 'english/settings.html', {'form_word': form_word, 'form_list_words': form_list_words, 'count':count})
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
    return render(request, 'english/list_words.html', {'words': all, 'count': len(all)})


class E_R(View):
    @staticmethod
    def get(request):
        return render(request, 'english/e-r.html')

    @staticmethod
    def post(request):
        all = Words.objects.all()
        context = {}
        for item in all:
            try:
                context[item.english] = item.russian
            except:
                print('error')
        return JsonResponse(context)


class R_E(View):
    @staticmethod
    def get(request):
        return render(request, 'english/e-r.html')

    @staticmethod
    def post(request):
        all = Words.objects.all()
        context = {}
        for item in all:
            try:
                context[item.russian] = item.english
            except:
                print('error')
        return JsonResponse(context)


class Random(View):
    @staticmethod
    def get(request):
        return render(request, 'english/e-r.html')

    @staticmethod
    def post(request):
        all = Words.objects.filter(learned=None)
        context = {}
        for item in all:
            try:
                context[item.russian] = item.english
                context[item.english] = item.russian
            except:
                print('error')
        return JsonResponse(context)

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
        params = WordParams.objects.get(id=1)
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
            try:
                name_file, _ = (request.FILES.get('file').name).split('.')
                lesson = int(name_file)
            except:
                lesson = 0
            file_ = request.FILES.get('file').read()
            content = file_.decode('utf-8').split('\r\n')
            for item in content:
                try:
                    w = item.split(',')
                    Words.objects.create(english=w[0].strip(), russian=w[1].strip(), lesson=lesson)
                except:
                    pass
        return redirect('settings')


def clear(request):
    p_list = get_param_qwery()
    all = Words.objects.filter(**p_list)
    for item in all:
        item.delete()
    return redirect('settings')


def list_words(request):
    p_list = get_param_qwery()
    all = Words.objects.filter(**p_list)
    return render(request, 'english/list_words.html', {'words': all, 'count': len(all)})


class E_R(View):
    @staticmethod
    def get(request):
        return render(request, 'english/e-r.html')

    @staticmethod
    def post(request):
        p_list = get_param_qwery()
        all = Words.objects.filter(**p_list)
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
        p_list = get_param_qwery()
        all = Words.objects.filter(**p_list)
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
        p_list = get_param_qwery()
        all = Words.objects.filter(**p_list)
        context = {}
        for item in all:
            try:
                context[item.russian] = item.english
                context[item.english] = item.russian
            except:
                print('error')
        return JsonResponse(context)

def get_param_qwery():
    params = WordParams.objects.get(id=1)
    p = {'lesson__in': []}
    if params.learned:
        p['learned'] = False
    if params.heavy:
        p['heavy'] = True
    if params.lesson_0:
        p['lesson__in'].append(0)
    if params.lesson_1:
        p['lesson__in'].append(1)
    if params.lesson_2:
        p['lesson__in'].append(2)
    if params.lesson_3:
        p['lesson__in'].append(3)
    if params.lesson_4:
        p['lesson__in'].append(4)
    if params.lesson_5:
        p['lesson__in'].append(5)
    if params.lesson_6:
        p['lesson__in'].append(6)
    if params.lesson_7:
        p['lesson__in'].append(7)
    if params.lesson_8:
        p['lesson__in'].append(8)
    if params.lesson_9:
        p['lesson__in'].append(9)
    if params.lesson_10:
        p['lesson__in'].append(10)
    if params.lesson_11:
        p['lesson__in'].append(11)
    if params.lesson_12:
        p['lesson__in'].append(12)
    if params.lesson_13:
        p['lesson__in'].append(13)
    return p
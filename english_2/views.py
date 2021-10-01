from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import LoadWordForm, LoadWordsForm, WordsParamForm, SearchWordForm
from .models import Words, WordParams
from english.models import Words as Words_l1
from english.models import IrregularVerbs
from django.http import JsonResponse
from django.db.models import Q


def index(request):
    if request.method == 'GET':
        try:
            params = WordParams.objects.get(id=1)
        except:
            params = WordParams.objects.create(id=1)
        form_word_param = WordsParamForm(instance=params)
        return render(request, 'english_2/base_english.html', {'form_word_param': form_word_param})
    if request.method == 'POST':
        params = WordParams.objects.get(id=1)
        form = WordsParamForm(request.POST, instance=params)
        if form.is_valid():
            form.save()
        return redirect('level_2:english_index')


class Settings(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        count = Words.objects.all().count()
        form_list_words = LoadWordsForm()
        form_word = LoadWordForm()
        return render(request, 'english_2/settings.html', {'form_word': form_word,
                                                         'form_list_words': form_list_words,
                                                         'count': count})
    @staticmethod
    def post(request):
        if request.POST.get('english'):
            form = LoadWordForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('level_2:settings')
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
                    item = item.replace('’',"'")

                    if ';' in item:
                        english, russian = item.split(';',1)
                    elif '•' in item:
                        english, russian = item.split('•',1)
                    elif '-' in item:
                        english, russian = item.split('-',1)

                    english = english.replace('(to)', 'to', 1)
                    english = english.strip()
                    russian = russian.strip()

                    other_word = Words.objects.filter(russian=russian)
                    for word in other_word:
                        if word.english != english:
                            russian = russian+' ('+str(lesson)+')'
                    Words.objects.create(english=english, russian=russian, lesson=lesson)
                except:
                    pass
        return redirect('level_2:settings')


def clear(request):
    all = get_param_qwery()
    for item in all:
        item.learned = False
        item.save()
    return redirect('level_2:settings')


def list_words(request):
    if request.method == "GET":
        all = get_param_qwery()
        return render(request, 'english_2/list_words.html', {'words': all, 'count': len(all)})

def word_update(request, id):
    if request.method == "GET":
        word = Words.objects.get(pk=id)
        context = {'word': word}
        return render(request, 'english_2/word_form.html', context)
    else:
        english = (request.POST.get('english'))
        russian = (request.POST.get('russian'))
        info = (request.POST.get('info'))
        heavy = (request.POST.get('heavy'))
        learned = (request.POST.get('learned'))
        lesson = (request.POST.get('lesson'))
        phrasal = (request.POST.get('phrasal'))
        irregular = (request.POST.get('irregular'))
        word = Words.objects.get(pk=id)
        word.english = english
        word.russian = russian
        word.info = info


        if heavy:
            word.heavy = True
        else:
            word.heavy = False
        if learned:
            word.learned = True
        else:
            word.learned = False
        if phrasal:
            word.phrasal_verbs = True
        else:
            word.phrasal_verbs = False
        if irregular:
            word.irregular_verbs = True
        else:
            word.irregular_verbs = False
        word.lesson = int(lesson)
        word.save()
        return render(request, 'english_2/back.html')


class E_R(View):
    @staticmethod
    def get(request):
        return render(request, 'english_2/e-r.html')

    @staticmethod
    def post(request):
        all = get_param_qwery()
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
        return render(request, 'english_2/e-r.html')

    @staticmethod
    def post(request):
        context = {}
        all = get_param_qwery()

        for item in all:
            try:
                if item.russian not in context:
                    context[item.russian] = item.english
            except:
                print('error')
        return JsonResponse(context)


class Random(View):
    @staticmethod
    def get(request):
        return render(request, 'english_2/e-r.html')

    @staticmethod
    def post(request):
        all = get_param_qwery()
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
    if params.irregular_verbs:
        all = Words.objects.filter(irregular_verbs=True)
    elif params.phrasal_verbs:
        all = Words.objects.filter(phrasal_verbs=True)
    else:
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
        all = Words.objects.filter(**p)

    return all


def mod(request):
    if request.user.username:
        word = {'lesson__in': p['lesson__in']}
        if '/e_r/' in request.path:
            language = 'english'
        else:
            language = 'russian'

        if request.GET.get('learned'):
            mod = 'learned'
            word[language] = request.GET.get('learned')
        elif request.GET.get('heavy'):
            mod = 'heavy'
            word[language] = request.GET.get('heavy')

        s = Words.objects.filter(**word)
        for w in s:
            if mod == 'learned':
                w.learned = True
            else:
                w.heavy = True
            w.save()
    context = {'status': 200}
    return JsonResponse(context)

class SearchWord(View):
    @staticmethod
    def get(request):
        form = SearchWordForm()
        return render(request, 'english_2/search_word.html', {'form': form})


    @staticmethod
    def post(request):
        form = SearchWordForm()
        input_word = request.POST.get('word')
        english_words = Words.objects.filter(english__icontains=input_word)
        russian_words = Words.objects.filter(russian__icontains=input_word)
        english_words_l1 = Words_l1.objects.filter(english__icontains=input_word)
        russian_words_l1 = Words_l1.objects.filter(russian__icontains=input_word)


        i_v_russion = IrregularVerbs.objects.filter(russian__icontains=input_word)
        i_v_english = IrregularVerbs.objects.filter(Q(infinitive__icontains=input_word) | Q(past_simple__icontains=input_word) | Q(past_participle__icontains=input_word))

        count = len(english_words)+len(russian_words)+len(english_words_l1)+\
                len(russian_words_l1)+len(i_v_english)+len(i_v_russion)

        return render(request, 'english_2/search_word.html', {'form': form,
                                                            'english_words': english_words,
                                                            'russian_words': russian_words,
                                                              'english_l1': english_words_l1,
                                                              'russian_l1': russian_words_l1,
                                                              'i_v_russion': i_v_russion,
                                                              'i_v_english': i_v_english,
                                                            'count': count})

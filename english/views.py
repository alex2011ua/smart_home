from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .form import LoadWordForm, LoadWordsForm, WordsParamForm, SearchWordForm, CompareWordForm
from .models import Words, WordParams
from django.http import JsonResponse
from django.db.models import Q
from english_2.models import Words as OldWords


def index(request):
    if request.method == 'GET':
        try:
            params = WordParams.objects.get(id=1)
        except:
            params = WordParams.objects.create(id=1)
        form_word_param = WordsParamForm(instance=params)

        return render(request, 'english/base_english.html', {'form_word_param': form_word_param, 'params': params})
    if request.method == 'POST':
        params = WordParams.objects.get(id=1)
        form = WordsParamForm(request.POST, instance=params)
        if form.is_valid():
            form.save()
        return redirect('english:english_index')


class Settings(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        count = Words.objects.all().count()
        form_list_words = LoadWordsForm()
        form_word = LoadWordForm()
        return render(request, 'english/settings.html', {'form_word': form_word,
                                                         'form_list_words': form_list_words,
                                                         'count': count})
    @staticmethod
    def post(request):
        if request.POST.get('english'):
            form = LoadWordForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('english:settings')
        if request.FILES.get('file'):
            name_file, _ = (request.FILES.get('file').name).split('.')
            irregular_verbs = False
            phrasal_verbs = False

            try:
                lesson = int(name_file)
            except:
                lesson = 99

            if name_file == 'irregular_verbs':
                irregular_verbs = True
            elif name_file == 'phrasal_verbs':
                phrasal_verbs = True
            file_ = request.FILES.get('file').read()
            content = file_.decode('utf-8').split('\r\n')
            for item in content:
                try:
                    item = item.replace('’', "'")

                    if ';' in item:
                        english, russian = item.split(';', 1)
                    elif '•' in item:
                        english, russian = item.split('•', 1)
                    elif '-' in item:
                        english, russian = item.split('-', 1)

                    english = english.replace('(to)', 'to', 1)
                    english = english.strip()
                    russian = russian.strip()

                    other_word = Words.objects.filter(russian=russian, lesson__in=(1,2,3,4,5,6,7,8,9,10,11,12,13))
                    for word in other_word:
                        if word.english != english:
                            russian = russian+' (' + str(lesson) + ')'

                    Words.objects.create(english=english,
                                         russian=russian,
                                         lesson=lesson,
                                         irregular_verbs=irregular_verbs,
                                         phrasal_verbs=phrasal_verbs
                                         )
                except Exception as ex:
                    print(ex)
        return redirect('english:settings')


def clear(request):
    params = WordParams.objects.get(id=1)
    params.learned = False
    params.save()
    all, p = WordParams.params()
    for item in all:
        item.learned = False
        item.save()


    return redirect('english:settings')

def test(request):
    '''для перехода на следующий уровень'''
    all_w = OldWords.objects.all()
    for i in all_w:
        Words.objects.create(english=i.english,
                             russian=i.russian,
                             learned=i.learned,
                             heavy=i.heavy,
                             info=i.info,
                             lesson=i.lesson,
                             phrasal_verbs=i.phrasal_verbs,
                             irregular_verbs=i.irregular_verbs)
    return render(request, 'english/back.html')
    words_l2 = Words.objects.filter(lesson__in=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])
    for word in words_l2:
        english = word.english
        russian = word.russian
        Words.objects.create(english=english,
                             russian=russian,
                             irregular_verbs=word.irregular_verbs,
                             phrasal_verbs=word.phrasal_verbs,
                             lesson=200,
                             info=str(word.lesson),

                             )
        word.delete()
    return render(request, 'english/back.html')

def list_words(request):
    if request.method == "GET":
        all, p = WordParams.params()

        return render(request, 'english/list_words.html', {'words': all, 'count': len(all)})

def word_update(request, id):
    if request.method == "GET":
        word = Words.objects.get(pk=id)
        context = {'word': word}
        return render(request, 'english/word_form.html', context)
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
        return render(request, 'english/back.html')


class E_R(View):
    @staticmethod
    def get(request):
        params = WordParams.objects.get(id=1)
        return render(request, 'english/e-r.html', {'params':params})

    @staticmethod
    def post(request):
        all, p = WordParams.params()
        params = WordParams.objects.get(id=1)
        context = {'control_state': params.control_state}
        for item in all:
            try:
                context[item.english] = item.russian
            except:
                print('error')
        return JsonResponse(context)


class R_E(View):
    @staticmethod
    def get(request):
        params = WordParams.objects.get(id=1)
        return render(request, 'english/e-r.html', {'params':params})

    @staticmethod
    def post(request):
        params = WordParams.objects.get(id=1)
        context = {'control_state': params.control_state}
        all, p = WordParams.params()

        for item in all:
            try:
                if item.russian not in context:
                    context[item.russian] = item.english
            except:
                print('error')
        return JsonResponse(context)


def mod(request):
    all, p = WordParams.params()
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
        return render(request, 'english/search_word.html', {'form': form})

    @staticmethod
    def post(request):
        form = SearchWordForm()
        input_word = request.POST.get('word')
        english_words = Words.objects.filter(english__icontains=input_word)
        russian_words = Words.objects.filter(russian__icontains=input_word)

        count = len(english_words)+len(russian_words)

        return render(request, 'english/search_word.html', {  'form': form,
                                                                'english_words': english_words,
                                                                'russian_words': russian_words,
                                                                'count': count
                                                                })
class CompareWords(View):
    @staticmethod
    def get(request):
        form = CompareWordForm()
        return render(request, 'english/compare_word.html', {'form': form})

    @staticmethod
    def post(request):
        import difflib as df
        form = CompareWordForm()
        first_word = request.POST.get('first_word')
        second_word = request.POST.get('second_word')
        if first_word == second_word:
            answer = 'Строки одинаковы'
        else:
            d = df.Differ()
            diff = d.compare(first_word, second_word)
            answer = ''.join(diff)
        return render(request, 'english/compare_word.html', {
            'form': form,
            'answer': answer,
            'first_word':first_word,
            'second_word':second_word,
        })

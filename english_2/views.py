from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .form import LoadWordForm, LoadWordsForm, WordsParamForm, SearchWordForm, CompareWordForm
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

                    other_word = Words.objects.filter(russian=russian)
                    try:
                        _ = Words.objects.get(russian=russian, english=english)
                    except ObjectDoesNotExist:

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
        return redirect('level_2:settings')


def clear(request):
    params = WordParams.objects.get(id=1)
    params.learned = False
    params.save()
    all, p = WordParams.params()
    for item in all:
        item.learned = False
        item.save()


    return redirect('level_2:settings')

def test(request):
    words_l1 = Words_l1.objects.all()
    for word in words_l1:
        english = word.english
        russian = word.russian

        other_word = Words.objects.filter(russian=russian, lesson=100)
        try:
            _ = Words.objects.get(russian=russian, english=english, lesson=100)
        except ObjectDoesNotExist:
            for o_word in other_word:
                if o_word.english != english:
                    russian = russian + ' (' + str(word.lesson) + ')'

            Words.objects.create(english=english,
                                 russian=russian,
                                 learned=word.learned,
                                 heavy=word.heavy,
                                 lesson=100,
                                 irregular_verbs=False,
                                 phrasal_verbs=False,
                                 info=str(word.lesson),
                                 )
        word.delete()
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
    return render(request, 'english_2/back.html')

def list_words(request):
    if request.method == "GET":
        all, p = WordParams.params()
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
        return render(request, 'english_2/e-r.html')

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

        return render(request, 'english_2/search_word.html', {  'form': form,
                                                                'english_words': english_words,
                                                                'russian_words': russian_words,
                                                                'english_l1': english_words_l1,
                                                                'russian_l1': russian_words_l1,
                                                                'i_v_russion': i_v_russion,
                                                                'i_v_english': i_v_english,
                                                                'count': count
                                                                })
class CompareWords(View):
    @staticmethod
    def get(request):
        form = CompareWordForm()
        return render(request, 'english_2/compare_word.html', {'form': form})

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
        return render(request, 'english_2/compare_word.html', {
            'form': form,
            'answer': answer,
            'first_word':first_word,
            'second_word':second_word,


        })

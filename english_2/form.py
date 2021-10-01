from django import forms
from .models import Words, WordParams


class LoadWordsForm(forms.Form):
    file = forms.FileField(label='загрузить файл со словами')


class LoadWordForm(forms.ModelForm):
    class Meta:
        model = Words
        fields = (
            'lesson',
            'english',
            'russian',
            'info',
            'phrasal_verbs',
            'irregular_verbs',
        )
        labels = {
            'lesson': 'lesson',
            'english': 'english',
            'russian': 'russian',
            'info': 'info',
            'phrasal_verbs': 'Только фразовые глаголы',
            'irregular_verbs': 'Только неправильные глаголы',
        }


class WordsParamForm(forms.ModelForm):
    class Meta:
        model = WordParams
        fields = '__all__'
        labels = {
            'learned': 'Не показывать выученые слова',
            'heavy': 'Только сложные слова',
            'lesson_0': 'Слова без привязки к уроку',
            'phrasal_verbs': 'Только фразовые глаголы',
            'irregular_verbs': 'Только неправильные глаголы',
        }


class SearchWordForm(forms.Form):
    word = forms.CharField(label='слово')
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
            'info'
        )
        labels = {
            'lesson': 'lesson',
            'english': 'english',
            'russian': 'russian',
            'info': 'info'
        }


class WordsParamForm(forms.ModelForm):
    class Meta:
        model = WordParams
        fields = '__all__'
        labels = {
            'learned': 'Выученые слова',
            'heavy': 'сложные слова'
        }


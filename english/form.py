from django import forms
from .models import Words, WordParams, IrregularVerbs


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
            'learned': 'Не показывать выученые слова',
            'heavy': 'Только сложные слова',
            'lesson_0': 'Слова без привязки к уроку'
        }


class LoadIrregularVerbsForm(forms.ModelForm):
    class Meta:
        model = IrregularVerbs
        fields = (
            'infinitive',
            'past_simple',
            'past_participle',
            'russian'

        )

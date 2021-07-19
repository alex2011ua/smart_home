from django import forms
from .models import Words


class LoadWordsForm(forms.Form):
    file = forms.FileField(label='загрузить файл со словами')


class LoadWordForm(forms.ModelForm):
    class Meta:
        model = Words
        fields = (
            'english',
            'russian'
        )
        labels = {
            'english':'english',
            'russian':'russian'
        }




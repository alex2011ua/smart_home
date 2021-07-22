from django.contrib import admin
from english.models import Words


@admin.register(Words)
class WordsAdmin(admin.ModelAdmin):
    list_display = (
                    'lesson',
                    'english',
                    'russian',
                    'heavy',
                    'learned',
                    'info'
                    )
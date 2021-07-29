from django.contrib import admin
from english.models import Words, IrregularVerbs


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

    list_filter = (
        'lesson',
        'heavy',
        'learned'
    )


@admin.register(IrregularVerbs)
class IrregularVerbsAdmin(admin.ModelAdmin):
    list_display = (
                    'infinitive',
                    'past_simple',
                    'past_participle',
                    'russian',
                    'learned',
                    'heavy'
                    )

    list_filter = (
        'heavy',
        'learned'
    )

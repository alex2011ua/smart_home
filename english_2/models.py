from django.db import models


class Words(models.Model):
    english = models.CharField(max_length=128)
    russian = models.CharField(max_length=128)
    learned = models.BooleanField(default=False)
    heavy = models.BooleanField(default=False)
    info = models.CharField(max_length=128, blank=True)
    lesson = models.PositiveIntegerField(blank=True, default=0)
    phrasal_verbs = models.BooleanField(default=False)
    irregular_verbs = models.BooleanField(default=False)



class WordParams(models.Model):
    phrasal_verbs = models.BooleanField(default=False)
    irregular_verbs = models.BooleanField(default=False)
    learned = models.BooleanField(default=False)
    heavy = models.BooleanField(default=False)
    lesson_0 = models.BooleanField(default=False)
    lesson_1 = models.BooleanField(default=False)
    lesson_2 = models.BooleanField(default=False)
    lesson_3 = models.BooleanField(default=False)
    lesson_4 = models.BooleanField(default=False)
    lesson_5 = models.BooleanField(default=False)
    lesson_6 = models.BooleanField(default=False)
    lesson_7 = models.BooleanField(default=False)
    lesson_8 = models.BooleanField(default=False)
    lesson_9 = models.BooleanField(default=False)
    lesson_10 = models.BooleanField(default=False)
    lesson_11 = models.BooleanField(default=False)
    lesson_12 = models.BooleanField(default=False)
    lesson_13 = models.BooleanField(default=False)
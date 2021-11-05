from django.db import models
from django.contrib.auth.models import User

class Words(models.Model):
    english = models.CharField(max_length=128)
    russian = models.CharField(max_length=128)
    learned = models.BooleanField(default=False)
    heavy = models.BooleanField(default=False)
    info = models.CharField(max_length=128, blank=True)
    lesson = models.PositiveIntegerField(blank=True, default=0)
    phrasal_verbs = models.BooleanField(default=False)
    irregular_verbs = models.BooleanField(default=False)
    control = models.BooleanField(default=False)


class WordParams(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    learned = models.BooleanField(default=False)
    heavy = models.BooleanField(default=False)
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
    level_1 = models.BooleanField(default=False)
    level_2 = models.BooleanField(default=False)
    level_3 = models.BooleanField(default=False)

    lesson_0 = models.BooleanField(default=False)
    phrasal_verbs = models.BooleanField(default=False)
    irregular_verbs = models.BooleanField(default=False)
    control_state = models.BooleanField(default=False)

    @staticmethod
    def params():
        params = WordParams.objects.get(id=1)
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

        if params.level_1:
            p['lesson__in'].append(100)
        if params.level_2:
            p['lesson__in'].append(200)
        if params.level_3:
            p['lesson__in'].extend([0,1,2,3,4,5,6,7,8,9,10,11,12,13])
        if params.irregular_verbs:
            p['irregular_verbs'] = True
            p['lesson__in'].append(99)
        if params.phrasal_verbs:
            p['phrasal_verbs'] = True

        all = Words.objects.filter(**p)

        return all, p
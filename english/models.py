from django.db import models
from django.contrib.auth.models import User
import json



class Words(models.Model):
    '''
    lesson 88 = play
    lesson 99 = list irregular verbs
    lesson 100 = 1 cours
    lesson 200 = 2 cours
    '''
    english = models.CharField(max_length=128)
    russian = models.CharField(max_length=128)
    lesson = models.PositiveIntegerField(blank=True, default=0)

    learned = models.BooleanField(default=False)
    heavy = models.BooleanField(default=False)
    control = models.BooleanField(default=False)

    phrasal_verbs = models.BooleanField(default=False, verbose_name='exam')
    irregular_verbs = models.BooleanField(default=False)

    learned_list = models.CharField(max_length=256, default='')
    heavy_list = models.CharField(max_length=256, default='')
    control_list = models.CharField(max_length=256, default='')

    info = models.CharField(max_length=128, blank=True)

    @staticmethod
    def serialize(st):
        try:
            a = json.loads(st)
        except json.JSONDecodeError:
            return []
        return a

    def add_learned(self, user_id):
        learned = self.learned_list
        learned_list = Words.serialize(learned)
        if user_id in learned_list:
            return
        learned_list.append(user_id)
        learned = json.dumps(learned_list)
        self.learned_list = learned
        self.save()

    def dell_learned(self, user_id):
        learned = self.learned_list
        learned_list = Words.serialize(learned)
        if user_id not in learned_list:
            return
        learned_list.remove(user_id)
        learned = json.dumps(learned_list)
        self.learned_list = learned
        self.save()

    def get_learned(self, user_id):
        learned = self.learned_list
        learned_list = Words.serialize(learned)
        if user_id in learned_list:
            return True
        return False

    def add_heavy(self, user_id):
        heavy = self.heavy_list
        heavy_list = Words.serialize(heavy)
        if user_id in heavy_list:
            return
        heavy_list.append(user_id)
        heavy = json.dumps(heavy_list)
        self.heavy_list = heavy
        self.save()

    def dell_heavy(self, user_id):
        heavy = self.heavy_list
        heavy_list = Words.serialize(heavy)
        if user_id not in heavy_list:
            return
        heavy_list.remove(user_id)
        heavy = json.dumps(heavy_list)
        self.heavy_list = heavy
        self.save()

    def get_heavy(self, user_id):
        heavy = self.heavy_list
        heavy_list = Words.serialize(heavy)
        if user_id in heavy_list:
            return True
        return False

    def add_control(self, user_id):
        control = self.control_list
        control_list = Words.serialize(control)
        if user_id in control_list:
            return
        control_list.append(user_id)
        control = json.dumps(control_list)
        self.control_list = control
        self.save()
        return


    def dell_control(self, user_id):
        control = self.control_list
        control_list = Words.serialize(control)
        if user_id not in control_list:
            return
        control_list.remove(user_id)
        control = json.dumps(control_list)
        self.control_list = control
        self.save()

    def get_control(self, user_id):
        control = self.control_list
        control_list = Words.serialize(control)
        if user_id in control_list:
            return True
        return False


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
    def params(user_id):
        params = WordParams.objects.get(user=user_id)
        p = {'lesson__in': []}

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
            p['lesson__in'].extend([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        if params.irregular_verbs:
            p['irregular_verbs'] = True
            p['lesson__in'].append(99)
        if params.phrasal_verbs:
            p['phrasal_verbs'] = True

        return p

    @staticmethod
    def get_words(user_id):
        params = WordParams.objects.get(user=user_id)
        p = WordParams.params(user_id)
        all = Words.objects.filter(**p)
        add_to = []
        for item in all:
            if params.control_state:
                if item.get_control(user_id):
                    continue
            if params.learned:
                if item.get_learned(user_id):
                    continue
            if params.heavy:
                if not item.get_heavy(user_id):
                    continue
            item.learned = item.get_learned(user_id)
            item.heavy = item.get_heavy(user_id)
            item.control = item.get_control(user_id)
            item.save()
            add_to.append(item)
        return add_to
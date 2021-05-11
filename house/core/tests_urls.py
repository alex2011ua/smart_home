from django.conf.urls import url

from . import test_views
from house.core.views_tests import Test, Sound, MailTest, TelegramTest, Bot_task_view, String_arduino

urlpatterns = [
    url(r'test/$', Test.as_view(), name='test'),
    url(r'sound/$', Sound.as_view(), name='sound'),
    url(r'mail/$', MailTest.as_view(), name='mail_test'),
    url(r'telegram/$', TelegramTest.as_view(), name='telegram_test'),
    url(r'task/$', Bot_task_view.as_view(), name='task'),
    url(r'string_arduino/$', String_arduino.as_view(), name='string_arduino'),

]

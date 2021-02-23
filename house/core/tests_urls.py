from django.conf.urls import url

from . import test_views
from house.core.views_tests import Test, Sound, MailTest, TelegramTest

urlpatterns = [
    url(r'test/$', Test.as_view(), name='test'),
    url(r'sound/$', Sound.as_view(), name='sound'),
    url(r'mail/$', MailTest.as_view(), name='mail_test'),
    url(r'telegram/$', TelegramTest.as_view(), name='telegram_test'),

]

from django.conf.urls import url

from . import test_views
from house.core.views_tests import Test, Sound, Raspberry_rele, MailTest, TelegramTest


urlpatterns = [
    url(r'test/$', Test.as_view(), name = 'test'),
    url(r'sound/$', Sound.as_view(), name = 'sound'),
    url(r'rele_board/$', Raspberry_rele.as_view(), name = 'rele_board'),
    url(r'mail/$', MailTest.as_view(), name = 'mail_test'),
    url(r'telegram/$', TelegramTest.as_view(), name = 'telegram_test'),

]
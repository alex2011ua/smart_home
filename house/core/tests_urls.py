from django.conf.urls import url

from house.core.views_tests import (
    Bot_task_view,
    CheckAvtoView,
    MailTest,
    PingTaskView,
    Sound,
    String_arduino,
    TelegramTest,
    Test,
    string_to_bot,
)

from . import test_views

urlpatterns = [
    url(r"test/$", Test.as_view(), name="test"),
    url(r"sound/$", Sound.as_view(), name="sound"),
    url(r"mail/$", MailTest.as_view(), name="mail_test"),
    url(r"telegram/$", TelegramTest.as_view(), name="telegram_test"),
    url(r"task/$", Bot_task_view.as_view(), name="task"),
    url(r"ping/$", PingTaskView.as_view(), name="ping"),
    url(r"avto/$", CheckAvtoView.as_view(), name="avto"),
    url(r"string_arduino_to_bot/$", string_to_bot, name="string_arduino_to_bot"),
]

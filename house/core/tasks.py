from __future__ import absolute_import, unicode_literals

from .main_arduino import restart_cam

from .models import Setting
from ..celery import cellery_app


@cellery_app.task()
def restart_cam_task():
    # Здесь ваш код для проверки условий
    restart_cam()

@cellery_app.task()
def weather_task():
    # Здесь ваш код для проверки условий
    pass

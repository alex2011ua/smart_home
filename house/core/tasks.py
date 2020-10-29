from __future__ import absolute_import, unicode_literals


from .models import Setting
from ..celery import app


@app.task()
def smart_home_manager():
    # Здесь ваш код для проверки условий
    print('Celery - work')

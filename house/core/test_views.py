import json
import pytest

from datetime import date
from django.conf import settings
from .main_arduino import testing, read_ser
from .tasks import arduino_task


class TestArduino:

    def test_arduino(self, db):

        assert testing() == {'status': ['Test-OK']}
        assert arduino_task() is None
        assert read_ser() == {'status': ['Test-OK'],
                              'temp_gaz': 24.0,
                              'humidity_gaz': 19.0,
                              'MQ135_value': 50,
                              'MQ4_value': 60
                              }



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
        print(read_ser())
        assert read_ser() == {'status': ['Test-OK'],
                                'temp_street': 12.70,
                              'humidity_street': 76.90,
                              'temp_voda': 15.00,
                              'humidity_voda': 72.00,
                              'temp_gaz': 0.00,
                              'humidity_gaz': 1.00,
                              'MQ135_value': 24,
                              'MQ4_value': 57,
                              'muve_kitchen': 242,
                              'sound': 0,
                              'temp_room': 0}




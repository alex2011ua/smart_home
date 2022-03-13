from .main_arduino import get_arduino_answer, testing
from .tasks import arduino_task


class TestArduino:
    def test_arduino(self, db):
        assert testing() == {"status": ["Test-OK"]}
        assert arduino_task() is None
        print(get_arduino_answer())
        assert get_arduino_answer() == {
            "status": ["Test-OK"],
            "temp_street": 12.70,
            "humidity_street": 76.90,
            "temp_voda": 15.00,
            "humidity_voda": 72.00,
            "temp_gaz": 0.00,
            "humidity_gaz": 1.00,
            "MQ135_value": 24,
            "MQ4_value": 57,
            "muve_kitchen": 242,
            "sound": 0,
            "temp_room": 0,
        }
        print(arduino_task())
